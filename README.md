# bytegeist-docs

Global and cross-repository documentation portal for Bytegeist.

## Local build

Requires sibling read-only clones of the repositories in `docs-sources.yml`,
or a GitHub token for fetching them:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python scripts/import_docs.py --clean --local-repos-dir ../
mkdocs build --strict -f .generated-mkdocs.yml
mkdocs serve -f .generated-mkdocs.yml
```

The CI workflow needs a repository read token in the `DOCS_REPO_TOKEN` secret
with read access to the private source repositories. Local builds can avoid a
token by using sibling clones with `--local-repos-dir`.

The imported files under `.generated-docs/` are generated build input. Do not
edit them or commit them. Edit the canonical source repository instead.

## Ownership

- Global/cross-repository architecture and workflows: this repository.
- Application code and technical docs: the application repository.
- Infrastructure desired state and operational docs: `infra-configs`.
- Learning material: `cka-lab`.
- Work and status: Linear.
- GitHub: canonical Git, PR, and CI/CD platform.
- Forgejo: mirror/recovery only.
