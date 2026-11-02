#!/usr/bin/env python3
"""Opt-in source collector for Zensical v2; no account discovery and no deployment."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import os
from urllib.parse import quote, unquote, urlsplit
import yaml

ROOT = Path(__file__).resolve().parents[1]
SAFE = {".md", ".markdown", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf"}


def manifest_items(path):
    if path is None:
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    items = data.get("sources") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise ValueError("private selection requires sources: []")
    seen = set()
    for item in items:
        if not isinstance(item, dict) or set(item) != {"name", "repo", "paths"}:
            raise ValueError("source requires name, repo, paths")
        name, repo, paths = item["name"], item["repo"], item["paths"]
        if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", name):
            raise ValueError("invalid source alias")
        if not isinstance(repo, str) or not re.fullmatch(r"ffworker/[a-zA-Z0-9][a-zA-Z0-9_.-]*", repo):
            raise ValueError("invalid repository")
        if name in seen or repo in seen:
            raise ValueError("duplicate selection")
        seen.update((name, repo))
        if not isinstance(paths, list) or not paths or any(p not in ("README.md", "docs/") for p in paths):
            raise ValueError("choose README.md and/or docs/")
        if len(set(paths)) != len(paths):
            raise ValueError("duplicate path")
    return items


def checkout(item, local_root, cache):
    name, repo = item["name"], item["repo"]
    if local_root:
        path = local_root / name
        if path.is_symlink() or not (path / ".git").exists():
            raise ValueError("missing local Git checkout for selected source")
        return path
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / name
    if target.is_symlink():
        raise ValueError("symlinked checkout target")
    if target.exists():
        shutil.rmtree(target)
    if (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")) and shutil.which("gh"):
        cmd = ["gh", "repo", "clone", repo, str(target), "--", "--depth=1"]
    else:
        cmd = ["git", "clone", "--depth=1", "https://github.com/" + repo + ".git", str(target)]
    subprocess.run(cmd, check=True)
    return target


def copy_docs(source, dest, paths):
    copied = []
    for path in paths:
        start = source / path.rstrip("/")
        if start.is_symlink() or not start.exists():
            raise ValueError("declared README/docs path missing or symlinked")
        for file in ([start] if start.is_file() else sorted(start.rglob("*"))):
            rel = file.relative_to(source)
            if file.is_symlink():
                raise ValueError("symlink in selected documentation")
            if any(x.startswith(".") for x in rel.parts) or not file.is_file() or file.suffix.lower() not in SAFE:
                continue
            to = dest / rel
            to.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, to)
            copied.append(rel)
    if not any(x.suffix.lower() in (".md", ".markdown") for x in copied):
        raise ValueError("no Markdown documents selected")
    return copied


def relink(dest, repo, sha):
    for page in dest.rglob("*.md"):
        parent = page.relative_to(dest).parent.as_posix()
        def fix(match):
            url = match.group(1)
            parsed = urlsplit(url)
            if not parsed.path or url.startswith(("#", "/", "<")) or parsed.scheme or parsed.netloc:
                return match.group(0)
            raw = unquote(parsed.path)
            if "\\" in raw:
                return match.group(0)
            rel = posixpath.normpath(posixpath.join(parent, raw))
            if rel.startswith("../") or rel == "..":
                return match.group(0)
            options = (Path(rel), Path(rel) / "README.md", Path(rel) / "index.md")
            found = next((p for p in options if (dest / p).is_file()), None)
            if found:
                link = quote(posixpath.relpath(found.as_posix(), parent), safe="/._-")
            else:
                kind = "tree" if raw.endswith("/") else "blob"
                link = "https://github.com/" + repo + "/" + kind + "/" + sha + "/" + quote(rel, safe="/._-")
            if parsed.query:
                link += "?" + parsed.query
            if parsed.fragment:
                link += "#" + parsed.fragment
            return "](" + link + ")"
        page.write_text(re.sub(r"\]\(([^)\s]+)\)", fix, page.read_text(encoding="utf-8")), encoding="utf-8")


def prepare(manifest=None, local_root=None, output=None):
    items = manifest_items(manifest)
    output = output or ROOT / ".generated"
    if output.is_symlink():
        raise ValueError("unsafe generated output")
    if output.exists():
        shutil.rmtree(output)
    docs = output / "docs"
    shutil.copytree(ROOT / "docs", docs)
    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    config["docs_dir"] = "docs"
    config["site_dir"] = "site"
    nav = list(config["nav"])
    lines = ["# Quellen", "", "Quellrevision ist kein Live-Status.", "", "| Quelle | Commit | Abgerufen (UTC) |", "| --- | --- | --- |"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    for item in items:
        source = checkout(item, local_root, output / "cache")
        sha = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
        dest = docs / "repositories" / item["name"]
        copied = copy_docs(source, dest, item["paths"])
        relink(dest, item["repo"], sha)
        md = [p for p in copied if p.suffix.lower() in (".md", ".markdown")]
        md.sort(key=lambda p: (p.name != "README.md", p.as_posix()))
        nav.append({item["name"]: [{p.stem: "repositories/" + item["name"] + "/" + p.as_posix()} for p in md]})
        lines.append("| " + item["name"] + " | " + sha[:12] + " | " + now + " |")
    (docs / "quellstand.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    nav.append({"Quellstand": "quellstand.md"})
    config["nav"] = nav
    cfg = output / "mkdocs.yml"
    cfg.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return cfg, len(items)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, help="explicit PRIVATE YAML; omit to import nothing")
    parser.add_argument("--local-root", type=Path, help="directory of local checkouts named by alias")
    args = parser.parse_args()
    config, count = prepare(args.manifest, args.local_root)
    print(f"Selected {count} source(s). Build with: zensical build --strict -f {config}")
