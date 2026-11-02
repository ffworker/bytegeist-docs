# Bytegeist Docs v2 — isolated local preview

**Experiment, not production.** This is a clean, small documentation-site prototype, not a refactor or deploy of the old VPS02 publisher.

## Intent

- The operator deliberately chooses which repositories and whether root `README.md` and/or root `docs/` are useful. No automatic account-wide import.
- Each selected source stays canonical in its own Git repo.
- No private code, hostnames, tokens, source inventories or credentials are present in this public preview.
- Repository freshness and real operational verification are **different** things.
- Markdown, a reading-friendly interface, and a regenerable static site remain the whole product.
- Existing `scripts/import_docs.py`, v1 CI, VPS02 pipeline, NetBird, servers and blog are untouched.

## Renderer decision: Zensical

**Zensical is the chosen engine for Bytegeist Docs v2.** The original site ran on MkDocs Material, which helped prove the source ownership and Markdown approach. Zensical comes from the same creators, supports existing `mkdocs.yml` projects, and provides its own **modern** theme variant. Its pre-1.0 compatibility needs to remain covered by tests.

The existing `v2/mkdocs.yml` is intentionally kept as the Zensical configuration: Zensical officially supports it. We do not need a migration to TOML just to claim a clean start. The v1 importer, deploy jobs, VPS02 paths and permissions are not used by this preview.

## Local preview: Zensical

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install zensical
cd v2
zensical build --strict
zensical serve
```

Open http://127.0.0.1:8000/ . The prototype contains **only synthetic example pages**.

The new v2 CI runs a clean strict Zensical build **without private credentials** and checks that the custom Bytegeist styles and pages are present. The previously verified Material renderer is just historical comparison evidence, not a second runtime we will continue to maintain.

## Selected sources: ready, but empty until you decide

The v2 collector is an **opt-in local tool**. There is no automatic repo inventory, no live deployment, and the default configuration imports **nothing**.

From the repository root, after installing Zensical and PyYAML:

```sh
cp v2/sources.example.yml v2/sources.private.yml
# Edit sources.private.yml with only the repositories you approve.
cd v2
python -m pip install PyYAML zensical
python scripts/curate.py --manifest sources.private.yml
zensical build --strict -f .generated/mkdocs.yml
zensical serve -f .generated/mkdocs.yml
```

Example entry for **your private local manifest only**:

```yaml
sources:
  - name: chosen-project
    repo: ffworker/chosen-project
    paths:
      - README.md
      - docs/
```

Choose just `README.md` or just `docs/` when appropriate. For private repos, authenticate with GitHub CLI so that `gh repo clone` can read the chosen source. The site generator never requests rights it doesn't already have. Your local manifest and generated site are gitignored; never publish them as a public PR, CI artifact, or static website. For offline tests supply `--local-root` containing checkouts named after the source aliases.

Zensical builds from **.generated/mkdocs.yml**, which adds only the explicitly chosen source pages to the fixed v2 UI. The original `mkdocs.yml` remains the public synthetic preview. Imported pages record the source SHA and retrieval time, not live health.

## Real content remains deliberately unselected

The private, operator-reviewed 29-repository inventory and proposed `KEEP / REVIEW / EXCLUDE` decisions are tracked separately under [BYT-108](https://linear.app/bytegeist/issue/BYT-108). Nothing from that list is loaded here until the operator approves a subset. This is intentional: more scraped content was the mistake that made v1 less useful.

## What this intentionally does not do

No real repository checkouts by default. An explicitly selected local build can clone only its approved sources. No background refresh. No search indexing of all GitHub repos. No production ingress, NetBird/VPS02/CD changes. No automated catalog generation. No assertions that any operating system or service is healthy.

Source review and deployment decisions: [Linear BYT-108](https://linear.app/bytegeist/issue/BYT-108).
