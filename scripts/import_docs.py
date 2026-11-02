#!/usr/bin/env python3
"""Retrieve manifest-declared documentation and prepare one MkDocs build."""
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
GENERATED = ROOT / ".generated-docs"
CONFIG = ROOT / ".generated-mkdocs.yml"
CACHE = ROOT / ".cache" / "docs-sources"

def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)

def checkout(name: str, repo: str, local_root: Path | None) -> Path:
    """Get a fresh source snapshot. Never modify user checkouts."""
    if local_root:
        for candidate in (local_root / name, local_root / repo.rsplit("/", 1)[-1]):
            if (candidate / ".git").exists():
                return candidate
        raise FileNotFoundError(f"local checkout missing: {name}")
    target = CACHE / name
    CACHE.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        raise ValueError(f"refusing symlinked cache directory: {name}")
    # Managed cache only: a fresh shallow clone follows the current default
    # branch, preventing old documents and renamed default branches from lingering.
    if target.exists():
        shutil.rmtree(target)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token and shutil.which("gh"):
        run("gh", "repo", "clone", repo, str(target), "--", "--depth=1")
    else:
        run("git", "clone", "--depth=1", f"https://github.com/{repo}.git", str(target))
    return target

def copy_path(source: Path, target: Path, relative: str, *, optional: bool = False) -> set[Path]:
    """Import Markdown and benign assets only, preserving source paths."""
    rel = Path(relative.rstrip("/"))
    if not relative or rel.is_absolute() or ".." in rel.parts or any(p.startswith(".") for p in rel.parts):
        raise ValueError(f"unsafe documentation path: {relative!r}")
    src = source / rel
    if src.is_symlink():
        raise ValueError(f"symlinked documentation root: {relative}")
    if not src.exists():
        if optional:
            return set()
        raise FileNotFoundError(f"declared documentation path missing: {source.name}/{relative}")
    allowed = {".md", ".markdown", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".pdf", ".txt"}
    files = [src] if src.is_file() else sorted(src.rglob("*"))
    included: set[Path] = set()
    for file in files:
        path = file.relative_to(source)
        if any(p.startswith(".") or p == "__pycache__" for p in path.parts):
            continue
        if file.is_symlink():
            raise ValueError(f"symlinked documentation file: {path}")
        if not file.is_file() or file.suffix.lower() not in allowed:
            continue
        destination = target / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, destination)
        included.add(path)
    return included


def rewrite_source_links(target: Path, source: Path, repo: str, revision: str) -> None:
    """Keep imported pages navigable; link missing files to immutable source SHA."""
    import posixpath
    from urllib.parse import unquote, urlsplit
    for page in target.rglob("*.md"):
        relative_page = page.relative_to(target)
        text = page.read_text(encoding="utf-8")
        def replace(match: re.Match[str]) -> str:
            link = match.group(1)
            if not link or link.startswith(("#", "/", "//", "<")):
                return match.group(0)
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                return match.group(0)
            raw_path = unquote(parsed.path)
            if "\\" in raw_path:
                return match.group(0)
            normalized = posixpath.normpath(posixpath.join(relative_page.parent.as_posix(), raw_path))
            if normalized == ".." or normalized.startswith("../"):
                return match.group(0)
            relative = Path(normalized)
            imported = next((p for p in (relative, relative / "README.md", relative / "index.md")
                             if (target / p).is_file()), None)
            if imported:
                destination = posixpath.relpath(imported.as_posix(), relative_page.parent.as_posix())
                url = quote(destination, safe="/._-")
            else:
                kind = "tree" if raw_path.endswith("/") else "blob"
                url = f"https://github.com/{repo}/{kind}/{revision}/{quote(relative.as_posix(), safe='/._-')}"
            if parsed.query:
                url += "?" + parsed.query
            if parsed.fragment:
                url += "#" + parsed.fragment
            return "](" + url + ")"
        page.write_text(re.sub(r"\]\(([^)\s]+)\)", replace, text), encoding="utf-8")

def title(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").title()

def navigation(root: Path, relative: Path = Path(".")) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    directory = root / relative
    for child in sorted(directory.iterdir(), key=lambda p: (p.name != "index.md" if relative == Path(".") else p.is_file(), p.name.lower())):
        if child.name.startswith("."):
            continue
        if child.is_dir():
            nested = navigation(root, relative / child.name)
            if nested:
                items.append({title(child): nested})
        elif child.suffix == ".md":
            label = "Start here" if relative == Path(".") and child.name == "index.md" else title(child)
            items.append({label: (relative / child.name).as_posix().lstrip("./")})
    return items

def write_config() -> None:
    config = {
        "site_name": "Bytegeist Docs",
        "site_description": "Private Bytegeist documentation portal",
        "site_url": "https://docs.lab.bytegeist.info/",
        "docs_dir": GENERATED.name,
        "strict": True,
        "theme": {"name": "material", "language": "en", "font": False,
                  "features": ["navigation.sections", "navigation.top", "search.suggest", "search.highlight"]},
        "nav": navigation(GENERATED),
        "plugins": ["search"],
        "markdown_extensions": ["admonition", "tables", "pymdownx.details", "pymdownx.superfences", {"toc": {"permalink": True}}],
    }
    CONFIG.write_text(yaml.safe_dump(config, sort_keys=False))

def make_repository_directory(catalog_path: Path, enrolled: dict[str, dict]) -> str:
    """Build a private reader-facing index from the private infra-configs inventory.

    This public repository must never contain the private catalog contents.
    The import allowlist is independent: other repositories are only linked.
    """
    if not catalog_path.is_file():
        raise FileNotFoundError(f"private repository catalog unavailable: {catalog_path}")
    data = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    entries = data.get("repositories") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ValueError("private repository catalog must contain a nonempty repositories list")
    imported = {cfg["repo"]: alias for alias, cfg in enrolled.items()}
    seen: set[str] = set()
    lines = [
        "# Alle Repositories", "",
        "Dieses **private Verzeichnis** zeigt die zuletzt inventarisierten GitHub-Repositories. "
        "Die technischen Inhalte bleiben in den jeweiligen Quell-Repositories.", "",
        "**Im Portal:** README und ausgewählte docs-Seiten wurden beim letzten erfolgreichen "
        "Build importiert. **GitHub:** nur ein Link zur Originalquelle; private Repositories "
        "erfordern zusätzlich eigene GitHub-Berechtigung.", "",
        "| Repository | README | docs/ | Zugriff |",
        "| --- | --- | --- | --- |",
    ]
    for entry in sorted(entries, key=lambda e: str(e.get("repo", "")).casefold() if isinstance(e, dict) else ""):
        if not isinstance(entry, dict):
            raise ValueError("invalid repository catalog entry")
        repo, branch, readme = entry.get("repo"), entry.get("branch"), entry.get("readme")
        has_docs, archived = entry.get("docs"), entry.get("archived")
        if not isinstance(repo, str) or not re.fullmatch(r"ffworker/[A-Za-z0-9][A-Za-z0-9_.-]*", repo):
            raise ValueError("invalid private catalog repository")
        if not isinstance(branch, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", branch):
            raise ValueError(f"invalid default branch for {repo}")
        if readme is not None and (not isinstance(readme, str) or not re.fullmatch(r"(?i)readme(?:\.md|\.markdown)?", readme)):
            raise ValueError(f"invalid root README path for {repo}")
        if type(has_docs) is not bool or type(archived) is not bool or repo in seen:
            raise ValueError(f"invalid or duplicate catalog record: {repo}")
        seen.add(repo)
        root = f"https://github.com/{repo}"
        name = repo.rsplit("/", 1)[1]
        label = f"[{name}]({root})" + (" (archiviert)" if archived else "")
        if readme:
            url = (f"{quote(imported[repo], safe='')}/{quote(readme, safe='')}"
                   if repo in imported else f"{root}/blob/{branch}/{quote(readme, safe='')}")
            readme_link = f"[README]({url})"
        else:
            readme_link = "—"
        docs_link = f"[docs/]({root}/tree/{branch}/docs)" if has_docs else "—"
        status = "Im Portal" if repo in imported else "Nur GitHub"
        if not readme and not has_docs:
            status = "Noch keine README/docs"
        lines.append(f"| {label} | {readme_link} | {docs_link} | {status} |")
    if set(imported) - seen:
        raise ValueError("source manifest absent from private repository catalog")
    lines.extend([
        "", f"**Inventar:** {len(seen)} Repositories. "
        "Diese Liste ist eine datierte Bestandsaufnahme, keine automatische Synchronisation.",
        "", "Neue Repositories zunächst im privaten Inventar von infra-configs ergänzen. "
        "Eine weitere Quell-Importfreigabe ist davon getrennt.",
        "", "Git-Commit bedeutet nicht aktuelle Dienstgesundheit oder getesteten Restore.", "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-repos-dir", type=Path)
    parser.add_argument("--no-sources", action="store_true", help="Build only committed safe documentation; never retrieve repositories")
    parser.add_argument("--list-sources", action="store_true",
                        help="Check source manifest and list configured repos without cloning")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("repositories"), dict):
        raise ValueError("docs-sources.yml needs a repositories mapping")
    repositories = data["repositories"]
    for name, config in repositories.items():
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name):
            raise ValueError(f"unsafe source name: {name!r}")
        if not isinstance(config, dict) or not re.fullmatch(r"ffworker/[A-Za-z0-9][A-Za-z0-9_.-]*", str(config.get("repo", ""))):
            raise ValueError(f"unsafe repository for {name}")
        if "paths" in config and (not isinstance(config["paths"], list) or not config["paths"]):
            raise ValueError(f"paths for {name} must be a non-empty list")
    if args.list_sources:
        for name, config in repositories.items():
            print(f"{name}: {config['repo']} {config.get('paths', ['README.md', 'docs/'])}")
        return
    if args.clean:
        shutil.rmtree(GENERATED, ignore_errors=True)
        CONFIG.unlink(missing_ok=True)
    shutil.copytree(ROOT / "docs", GENERATED, dirs_exist_ok=True)
    if not args.no_sources:
        private_catalog_path = None
        provenance = ["# Documentation sources", "",
                      "These are build-time Git snapshots, not proof of the live infrastructure state.",
                      "Each document remains owned by its source repository.", "",
                      "| Source | Commit | Imported pages |", "|---|---|---:|"]
        for name, config in repositories.items():
            source = checkout(name, config["repo"], args.local_repos_dir)
            if config["repo"] == "ffworker/infra-configs":
                private_catalog_path = source / "docs/bytegeist-docs-repository-catalog.yml"
            revision = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
            target = GENERATED / "repositories" / name
            auto_paths = "paths" not in config
            selected = config.get("paths", ["README.md", "docs/"])
            included = set()
            for relative in selected:
                included.update(copy_path(source, target, relative, optional=auto_paths))
            count = sum(p.suffix.lower() in (".md", ".markdown") for p in included)
            if not count:
                raise ValueError(f"no Markdown imported for {name}: check source paths")
            rewrite_source_links(target, source, config["repo"], revision)
            provenance.append(f"| [{name}](../repositories/{quote(name)}/README.md) | `{revision}` | {count} |")
            print(f"IMPORT {name}: {count} pages from {revision[:12]}")
        (GENERATED / "sources").mkdir(parents=True, exist_ok=True)
        (GENERATED / "sources/index.md").write_text("\n".join(provenance) + "\n", encoding="utf-8")
        if private_catalog_path is None:
            raise ValueError("private infra-configs source is needed for repository directory")
        (GENERATED / "repositories/index.md").write_text(
            make_repository_directory(private_catalog_path, repositories), encoding="utf-8")
    write_config()
    mode = "safe committed" if args.no_sources else "full private"
    print(f"Prepared {mode} documentation for {len(repositories)} enrolled repositories")

if __name__ == "__main__":
    main()
