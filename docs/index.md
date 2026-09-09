# Bytegeist Documentation

Global and cross-repository documentation portal for the Bytegeist system.

The public-safe build uses only [`docs/public/`](public/index.md). The private/full
build additionally includes the global private pages in this repository and
read-only generated documentation from the repositories declared in
`docs-sources.yml`. Generated imports are build input, never canonical copies.

## Boundaries

- Linear owns work, tickets, ideas, and status.
- GitHub owns implementation history, PRs, CI, and CD.
- `infra-configs` owns infrastructure desired state and operational docs.
- `cka-lab` owns learning and lab material.
- Forgejo is mirror/recovery only.
- Hermes/Larry orchestrates but does not replace these systems.

See the public-safe pages for the shareable workflow and architecture view.
