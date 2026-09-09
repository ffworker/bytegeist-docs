\
#!/usr/bin/env python3
"""Fetch declared repository docs into generated MkDocs input."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs-sources.yml"
GENERATED = ROOT / ".generated-docs"
CACHE = ROOT / ".cache" / "docs-sources"


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def source_checkout(name: str, repo: str, local_root: Path | None) -> Path:
    if local_root:
        candidates = [local_root / name, local_root / repo.rsplit("/", 1)[-1]]
        for candidate in candidates:
            if (candidate / ".git").exists():
                return candidate
    target = CACHE / name
    CACHE.mkdir(parents=True, exist_ok=True)
    if not (target / ".git").exists():
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        url = f"https://github.com/{repo}.git"
        if token and shutil.which("gh"):
            run("gh", "repo", "clone", repo, str(target), "--", "--depth=1")
        elif token:
            run("git", "clone", "--depth=1", url, str(target))
        else:
            run("git", "clone", "--depth=1", url, str(target))
    return target


def copy_declared(source: Path, destination: Path, relative: str) -> None:
    src = source / relative
    if not src.exists():
        raise SystemExit(f"Declared documentation path does not exist: {source.name}/{relative}")
    if src.is_dir():
        target = destination / relative.rstrip("/")
        shutil.copytree(src, target, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))
    else:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)


def label(path: str) -> str:
    return path.rsplit("/", 1)[-1].replace(".md", "").replace("_", " ").replace("-", " ").title()


def rewrite_relative_links(target: Path, source: Path, repo: str) -> None:
    """Point unresolved/source-relative links back to their canonical GitHub source."""
    import re
    from urllib.parse import quote
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-repos-dir", type=Path,
                        help="Use sibling local clones instead of fetching repositories")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    if args.clean:
        shutil.rmtree(GENERATED, ignore_errors=True)
        (ROOT / ".generated-mkdocs.yml").unlink(missing_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)
    # Global pages are authored in bytegeist-docs; repository pages are generated.
    shutil.copytree(ROOT / "docs", GENERATED, dirs_exist_ok=True)
    source_data = yaml.safe_load(MANIFEST.read_text())
    repositories = source_data.get("repositories", {})
    imported_nav = []
    for name, config in repositories.items():
        source = source_checkout(name, config["repo"], args.local_repos_dir)
        target = GENERATED / "repositories" / name
        for path in config["paths"]:
            copy_declared(source, target, path)
        rewrite_relative_links(target, source, config["repo"])
        files = sorted((target).rglob("*.md"))
        entries = []
        for file in files:
            rel = file.relative_to(GENERATED).as_posix()
            entries.append({label(file.stem): rel})
        imported_nav.append({name: entries})

    # Build a complete generated MkDocs config so strict mode sees every imported page.
    config = {
        "site_name": "Bytegeist Docs",
        "site_description": "Global Bytegeist architecture, workflows, and repository documentation portal.",
        "site_url": "https://docs.lab.bytegeist.info/",
        "docs_dir": ".generated-docs",
        "strict": True,
        "theme": {"name": "material", "language": "en", "font": False,
                  "features": ["navigation.sections", "navigation.top", "search.suggest", "search.highlight"]},
        "nav": [
            {"Home": "index.md"},
            {"Architecture": [
                {"Overview": "architecture/overview.md"},
                {"Homelab": "architecture/homelab.md"},
                {"Infrastructure": "architecture/infrastructure.md"},
                {"AI Workflow": "architecture/ai-workflow.md"},
            ]},
            {"Repositories": [{"Overview": "repositories/index.md"}]},
            {"Workflows": [
                {"Linear and GitHub": "workflows/linear-github.md"},
                {"Development": "workflows/development.md"},
                {"CI/CD": "workflows/ci-cd.md"},
                {"Documentation": "workflows/documentation.md"},
            ]},
            {"Systems": [
                {"GitHub": "systems/github.md"},
                {"Forgejo": "systems/forgejo.md"},
                {"Linear": "systems/linear.md"},
                {"Hermes and Larry": "systems/hermes-larry.md"},
            ]},
            {"Decisions": "decisions/index.md"},
            {"Imported repository documentation": imported_nav},
        ],
        "plugins": ["search"],
        "markdown_extensions": ["admonition", "tables", "pymdownx.details", "pymdownx.superfences",
                                {"toc": {"permalink": True}}],
    }
    (ROOT / ".generated-mkdocs.yml").write_text(yaml.safe_dump(config, sort_keys=False))
    print(f"Imported {len(repositories)} repositories into {GENERATED}")


if __name__ == "__main__":
    main()
