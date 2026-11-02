"""Offline tests: the v2 source collector must never broaden imports by itself."""
from pathlib import Path
import importlib.util
import subprocess
import tempfile
import unittest

script = Path(__file__).resolve().parents[1] / "scripts" / "curate.py"
spec = importlib.util.spec_from_file_location("curate_v2", script)
curate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(curate)


class SourceTests(unittest.TestCase):
    def test_no_selection_means_no_repository_checkout(self):
        with tempfile.TemporaryDirectory() as temp:
            config, count = curate.prepare(output=Path(temp) / "out")
            self.assertEqual(count, 0)
            self.assertFalse((config.parent / "docs/repositories").exists())
            self.assertIn("Quellstand", config.read_text())

    def test_explicit_local_readme_docs_links_and_commit(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "repos" / "demo"
            (source / "docs").mkdir(parents=True)
            subprocess.run(["git", "init", "-q", str(source)], check=True)
            subprocess.run(["git", "-C", str(source), "config", "user.name", "Test"], check=True)
            subprocess.run(["git", "-C", str(source), "config", "user.email", "test@example.invalid"], check=True)
            (source / "README.md").write_text("# Demo\n[Guide](docs/guide.md) [Other](missing.md)\n")
            (source / "docs/guide.md").write_text("# Guide\n[Back](../README.md)\n")
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(["git", "-C", str(source), "commit", "-qm", "fixture"], check=True)
            manifest = base / "private.yml"
            manifest.write_text("sources:\n  - name: demo\n    repo: ffworker/demo\n    paths: [README.md, docs/]\n")
            config, count = curate.prepare(manifest, base / "repos", base / "out")
            self.assertEqual(count, 1)
            self.assertIn("repositories/demo/README.md", config.read_text())
            readme = (base / "out/docs/repositories/demo/README.md").read_text()
            self.assertIn("](docs/guide.md)", readme)
            self.assertIn("https://github.com/ffworker/demo/blob/", readme)
            self.assertIn("](../README.md)", (base / "out/docs/repositories/demo/docs/guide.md").read_text())
            self.assertIn("demo", (base / "out/docs/quellstand.md").read_text())

    def test_invalid_sources_fail_before_checkout(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "sources.yml"
            examples = [
                "sources:\n  - name: demo\n    repo: other/demo\n    paths: [README.md]\n",
                "sources:\n  - name: demo\n    repo: ffworker/demo\n    paths: [../secrets]\n",
                "sources:\n  - name: demo\n    repo: ffworker/demo\n    paths: [README.md]\n  - name: demo\n    repo: ffworker/demo\n    paths: [README.md]\n",
            ]
            for text in examples:
                manifest.write_text(text)
                with self.assertRaises(ValueError):
                    curate.manifest_items(manifest)

    def test_symlinked_docs_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            (base / "docs").mkdir()
            (base / "outside.md").write_text("private")
            (base / "docs/unsafe.md").symlink_to(base / "outside.md")
            with self.assertRaises(ValueError):
                curate.copy_docs(base, base / "output", ["docs/"])


if __name__ == "__main__":
    unittest.main()
