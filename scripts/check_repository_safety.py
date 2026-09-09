#!/usr/bin/env python3
"""Check that the public orchestration repository contains no private output."""
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]
tracked=subprocess.check_output(['git','ls-files'],cwd=root,text=True).splitlines()
for path in tracked:
    if path.startswith(('docs/','README.md','docs-sources.yml')) and (root/path).is_file():
        text=(root/path).read_text(errors='ignore')
        for marker in ('ghp_','github_pat_','100.96.','10.10.0.','10.99.0.','Bearer '):
            if marker in text:
                raise SystemExit(f'public repository safety marker {marker!r} found in {path}')
if any((root/p).exists() and (p.startswith('.generated-') or p.startswith('site/') or p.startswith('docs/public/')) for p in tracked):
    raise SystemExit('generated or obsolete public-site paths are tracked')
print('public repository safety invariants verified')
