# Documentation Workflow

Ask: **Does someone or another agent need to know this later?**

- Repo-specific technical information → update that repository's README/docs in the same PR.
- Infrastructure operational information → update `infra-configs` documentation.
- Cross-repository, global architecture, or workflow information → update `bytegeist-docs`.
- Learning material → update `cka-lab`.

Avoid maintaining the same canonical explanation in multiple repositories. Imported pages in this portal are generated build input, not separately edited copies.
