"""Offline regression tests for the private repository-documentation aggregator."""
from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "import_docs.py"
spec = importlib.util.spec_from_file_location("docs_importer", SCRIPT)
docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs)


class SourcesTest(unittest.TestCase):
    def test_optional_docs_import_and_links_stay_in_portal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target = root / "source", root / "out"
            (source / "docs").mkdir(parents=True)
            (source / "README.md").write_text("# Entry\n[Guide](docs/intro.md) [Missing](extra.md)\n")
            (source / "docs/intro.md").write_text("# Intro\n[Back](../README.md)\n")
            (source / "docs/pic.png").write_bytes(b"image")
            included = set()
            included.update(docs.copy_path(source, target, "README.md", optional=True))
            included.update(docs.copy_path(source, target, "docs/", optional=True))
            assert len(included) == 3
            docs.rewrite_source_links(target, source, "ffworker/example", "a" * 40)
            start = (target / "README.md").read_text()
            self.assertIn("](docs/intro.md)", start)
            self.assertIn("/blob/" + "a" * 40 + "/extra.md", start)
            self.assertIn("](../README.md)", (target / "docs/intro.md").read_text())

    def test_optional_missing_docs_but_strict_explicit_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            root.joinpath("README.md").write_text("# Only README")
            self.assertEqual(docs.copy_path(root, root / "output", "docs/", optional=True), set())
            with self.assertRaises(FileNotFoundError):
                docs.copy_path(root, root / "output", "docs/")
            for unsafe in ("../secrets/", "/etc/", ".git/"):
                with self.assertRaises(ValueError):
                    docs.copy_path(root, root / "output", unsafe)

    def test_source_symlinks_not_imported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "private.md").write_text("private")
            (root / "docs/escape.md").symlink_to(root / "private.md")
            with self.assertRaisesRegex(ValueError, "symlinked"):
                docs.copy_path(root, root / "site", "docs/")

    def test_preexisting_cache_is_replaced_with_fresh_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_cache = docs.CACHE
            docs.CACHE = root
            try:
                (root / "example").mkdir()
                (root / "example/old.md").write_text("stale")
                def fake_clone(*args):
                    self.assertEqual(args[:3], ("git", "clone", "--depth=1"))
                    (root / "example").mkdir()
                    (root / "example/README.md").write_text("fresh")
                with patch.object(docs, "run", side_effect=fake_clone), patch.dict(os.environ, {"GH_TOKEN": "", "GITHUB_TOKEN": ""}):
                    output = docs.checkout("example", "ffworker/example", None)
                self.assertTrue((output / "README.md").is_file())
                self.assertFalse((output / "old.md").exists())
            finally:
                docs.CACHE = old_cache

    def test_manifest_contains_new_public_sources(self):
        manifest = docs.MANIFEST.read_text()
        for name in ("signaturee-win", "signaturee-linux", "cka-lab", "homelab-talos"):
            self.assertIn("repo: ffworker/" + name, manifest)


if __name__ == "__main__":
    unittest.main()
