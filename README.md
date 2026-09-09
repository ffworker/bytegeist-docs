# Bytegeist Docs

[![Documentation CI](https://github.com/ffworker/bytegeist-docs/actions/workflows/ci.yml/badge.svg)](https://github.com/ffworker/bytegeist-docs/actions/workflows/ci.yml)
[![Nightly private documentation CD](https://github.com/ffworker/bytegeist-docs/actions/workflows/nightly.yml/badge.svg)](https://github.com/ffworker/bytegeist-docs/actions/workflows/nightly.yml)

This public repository demonstrates distributed documentation ownership and
safe aggregation. Application, infrastructure, and learning repositories keep
their own canonical README/docs content. Trusted automation retrieves selected
paths, validates the complete documentation universe, and builds a private
static site without committing or publicly storing imported content.

```text
source README/docs
  -> change-triggered aggregate validation
  -> 23:45 Europe/Berlin frozen build
  -> private deployment target: docs.lab.bytegeist.info
```

The public showcase is this repository and its workflows—not a public rendered
documentation website. GitHub Pages is not used. Full builds run only in trusted
workflow contexts with the approved read credential; untrusted fork PRs build
only the safe documentation committed here and never receive private access.

## Ownership

- Application technical docs: the owning application repository.
- Infrastructure operational docs: `infra-configs`.
- Learning, labs, and QA: `cka-lab`.
- Global workflow and cross-repository orchestration: this repository.
- Work/status: Linear; implementation, PRs, CI/CD, and history: GitHub.
- Forgejo: mirror/recovery only.

See [`docs-sources.yml`](docs-sources.yml) for the public manifest of source
repositories and imported paths. Imported contents are generated build inputs,
not editable copies.

## Operations

Source repositories notify `ffworker/bytegeist-docs` with a narrow
`repository_dispatch` event after documentation paths change on `main`. Each
source repository needs a secret named `DOCS_DISPATCH_TOKEN` containing a
fine-grained token limited to `ffworker/bytegeist-docs` with only Contents:
Read and write permission (used for the dispatch endpoint). The token must not
be included in event payloads.

The full private build uses `DOCS_REPO_TOKEN` only in trusted workflows. It is
never used by pull-request builds and never uploaded as an Actions artifact.
Static documentation replacement is the only permitted automatic deployment
exception; changes to cluster infrastructure, ingress, DNS, authentication,
networking, storage, or secrets remain approval-gated.

The nightly/manual workflow connects to the existing private NetBird network, transfers the generated site over pinned-key SSH, atomically replaces `/opt/bytegeist-docs/site` on VPS02, and verifies the private HTTPS endpoint. This is the narrow static-content deployment exception; infrastructure changes remain approval-gated.
