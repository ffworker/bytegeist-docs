# Bytegeist Docs v2 — isolated local preview

**Experiment, not production.** This is a clean, small documentation-site prototype, not a refactor or deploy of the old VPS02 publisher.

## Intent

- The operator deliberately chooses which repositories and whether root `README.md` and/or root `docs/` are useful. No automatic account-wide import.
- Each selected source stays canonical in its own Git repo.
- No private code, hostnames, tokens, source inventories or credentials are present in this public preview.
- Repository freshness and real operational verification are **different** things.
- Markdown, a reading-friendly interface, and a regenerable static site remain the whole product.
- Existing `scripts/import_docs.py`, v1 CI, VPS02 pipeline, NetBird, servers and blog are untouched.

## Local preview

Use a Python virtual environment (no Docker required):

```sh
python -m pip install "mkdocs-material>=9.6,<10"
cd v2
mkdocs serve
```

Open http://127.0.0.1:8000/ . The preview contains only synthetic content.

## Side-by-side engine comparison

Try [Zensical](https://zensical.org/docs/compatibility/mkdocs/migration/) using the same `mkdocs.yml`:

```sh
python -m pip install zensical
cd v2
zensical build
```

The optional GitHub Actions preview check builds both engines **without using private repo credentials or publishing site artifacts**. Compare search, navigation, typography, responsive layout and offline behavior before choosing a generator.

## What this intentionally does not do

No real repository checkouts. No background refresh. No search indexing of all GitHub repos. No production ingress, NetBird/VPS02/CD changes. No automated catalog generation. No assertions that any operating system or service is healthy.

Source review and deployment decisions: [Linear BYT-108](https://linear.app/bytegeist/issue/BYT-108).
