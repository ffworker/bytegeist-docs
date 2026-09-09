#!/usr/bin/env python3
"""Reject private-only material from the public documentation source tree."""
from pathlib import Path

root = Path(__file__).resolve().parents[1] / ".generated-public-docs"
forbidden_paths = {"private", ".cache", ".generated-docs"}
found_paths = forbidden_paths.intersection(p.name for p in root.iterdir()) if root.exists() else set()
if found_paths:
    raise SystemExit(f"public build contains forbidden generated paths: {sorted(found_paths)}")
for page in root.rglob("*.md"):
    text = page.read_text()
    for marker in ("DOCS_REPO_TOKEN", "100.96.", "10.10.0.", "10.99."):
        if marker in text:
            raise SystemExit(f"public safety marker {marker!r} found in {page}")
print("public documentation boundary verified")
