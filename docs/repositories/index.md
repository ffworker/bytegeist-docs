# Repository Index

Only the following repositories are in the permanent working architecture. Detailed documentation is owned by each repository and imported here at build time from `docs-sources.yml`.

## Active Engineering

| Repository | Purpose | Linear workflow | CI/CD | Documentation source |
| --- | --- | --- | --- | --- |
| [Signaturee](https://github.com/ffworker/Signaturee) | Outlook signature automation | Yes | CI/quality gates; deployment waits for live reconciliation | `README.md`, `docs/` |
| [mywebsite](https://github.com/ffworker/mywebsite) | `cv.bytegeist.dev` public website | Yes | Static validation and existing Pages delivery | `README.md` |
| [coach-potato-app](https://github.com/ffworker/coach-potato-app) | Phone-first training application | Yes | CI plus manual `vps-alpha` delivery | `README.md`, `docs/` |
| [camdash-board](https://github.com/ffworker/camdash-board) | Authenticated camera dashboards | Yes | Tests, image builds, Compose validation, gated deployment | `README.md` |
| [local-ragbot](https://github.com/ffworker/local-ragbot) | Local-first private RAG incubator | Yes | CI only; no production CD | `README.md`, `docs/` |

## Infrastructure

| Repository | Purpose | Workflow | Documentation source |
| --- | --- | --- | --- |
| [infra-configs](https://github.com/ffworker/infra-configs) | Infrastructure desired state and operational knowledge | Linear plus reviewed PRs; deployment approval-gated | `README.md`, `docs/`, `labs/proxmox/docs/` |

## Learning

| Repository | Purpose | Workflow | Documentation source |
| --- | --- | --- | --- |
| [cka-lab](https://github.com/ffworker/cka-lab) | Learning, labs, notes, and QA | Linear when work is requested; no product CD | `README.md`, `docs/` |

## Documentation

- [bytegeist-docs](https://github.com/ffworker/bytegeist-docs) — this global portal.

## Archived

- [Peirates](https://github.com/ffworker/Peirates)
- [Dennaar](https://github.com/ffworker/Dennaar)

Archived and superseded repositories are not normal agent/task automation targets.
