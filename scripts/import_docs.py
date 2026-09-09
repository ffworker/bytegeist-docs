#!/usr/bin/env python3
"""Retrieve declared docs and generate deterministic MkDocs configurations."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs-sources.yml"
PRIVATE_DOCS = ROOT / ".generated-docs"
PUBLIC_DOCS = ROOT / ".generated-public-docs"
PRIVATE_CONFIG = ROOT / ".generated-mkdocs.yml"
PUBLIC_CONFIG = ROOT / ".generated-public-mkdocs.yml"
CACHE = ROOT / ".cache" / "docs-sources"


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def checkout(name: str, repo: str, local_root: Path | None) -> Path:
    if local_root:
        for candidate in (local_root / name, local_root / repo.rsplit("/", 1)[-1]):
            if (candidate / ".git").exists():
                return candidate
    target = CACHE / name
    if not (target / ".git").exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if token and shutil.which("gh"):
            run("gh", "repo", "clone", repo, str(target), "--", "--depth=1")
        else:
            run("git", "clone", "--depth=1", f"https://github.com/{repo}.git", str(target))
    return target


def copy_path(source: Path, target: Path, relative: str) -> None:
    src = source / relative
    if not src.exists():
        raise SystemExit(f"Declared documentation path does not exist: {source.name}/{relative}")
    dst = target / relative.rstrip("/")
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def rewrite_source_links(target: Path, source: Path, repo: str) -> None:
    for page in target.rglob("*.md"):
        source_page = source / page.relative_to(target)
        text = page.read_text()
        def replace(match: re.Match[str]) -> str:
            link = match.group(1)
            if not link or link.startswith(("#", "/", "http:", "https:", "mailto:", "tel:")):
                return match.group(0)
            path, sep, anchor = link.partition("#")
            resolved = (source_page.parent / path).resolve()
            try:
                relative = resolved.relative_to(source.resolve()).as_posix()
            except ValueError:
                return match.group(0)
            kind = "tree" if resolved.is_dir() else "blob"
            url = f"https://github.com/{repo}/{kind}/main/{quote(relative, safe='/._-')}"
            return f"]({url}{sep + anchor if sep else ''})"
        page.write_text(re.sub(r"\]\(([^)]+)\)", replace, text))


def title(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").title()


def navigation(root: Path, relative: Path = Path(".")) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    directory = root / relative
    for child in sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        if child.name.startswith(".") or child.suffix not in (".md", ""):
            continue
        rel = (relative / child.name).as_posix().lstrip("./")
        if child.is_dir():
            nested = navigation(root, relative / child.name)
            if nested:
                items.append({title(child): nested})
        elif child.suffix == ".md":
            items.append({title(child): rel})
    return items


def write_config(path: Path, docs_dir: str) -> None:
    config = {
        "site_name": "Bytegeist Docs",
        "site_description": "Bytegeist documentation portal",
        "site_url": "https://docs.lab.bytegeist.info/",
        "docs_dir": docs_dir,
        "strict": True,
        "theme": {"name": "material", "language": "en", "font": False,
                  "features": ["navigation.sections", "navigation.top", "search.suggest", "search.highlight"]},
        "nav": navigation(ROOT / docs_dir),
        "plugins": ["search"],
        "markdown_extensions": ["admonition", "tables", "pymdownx.details", "pymdownx.superfences",
                                {"toc": {"permalink": True}}],
    }
    path.write_text(yaml.safe_dump(config, sort_keys=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", action="store_true", help="Generate only docs/public content")
    parser.add_argument("--local-repos-dir", type=Path)
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    if args.clean:
        shutil.rmtree(PRIVATE_DOCS, ignore_errors=True)
        shutil.rmtree(PUBLIC_DOCS, ignore_errors=True)
        PRIVATE_CONFIG.unlink(missing_ok=True)
        PUBLIC_CONFIG.unlink(missing_ok=True)
    if args.public:
        shutil.copytree(ROOT / "docs" / "public", PUBLIC_DOCS, dirs_exist_ok=True)
        write_config(PUBLIC_CONFIG, PUBLIC_DOCS.name)
        print(f"Prepared public-safe documentation in {PUBLIC_DOCS}")
        return

    shutil.copytree(ROOT / "docs", PRIVATE_DOCS, dirs_exist_ok=True)
    data = yaml.safe_load(MANIFEST.read_text())
    repositories = data.get("repositories", {})
    for name, config in repositories.items():
        source = checkout(name, config["repo"], args.local_repos_dir)
        target = PRIVATE_DOCS / "repositories" / name
        for path in config["paths"]:
            copy_path(source, target, path)
        rewrite_source_links(target, source, config["repo"])
    write_config(PRIVATE_CONFIG, PRIVATE_DOCS.name)
    print(f"Prepared private/full documentation for {len(repositories)} repositories in {PRIVATE_DOCS}")


if __name__ == "__main__":
    main()
