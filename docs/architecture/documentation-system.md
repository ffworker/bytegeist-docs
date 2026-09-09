# Documentation System

Repository-specific technical information stays with its owning repository.
Infrastructure operations stay in `infra-configs`. Learning material stays in
`cka-lab`. Cross-repository and global workflow information is owned here.

## Build outputs

- Public output: only `docs/public/`; safe for a future public Pages deployment.
- Private/full output: all global docs plus generated source-repository docs;
  retained only as a private GitHub Actions artifact.

The public build has a separate generated directory and separate MkDocs
configuration. It cannot accidentally receive the private import tree.

## Update rule

Ask: **Does someone or another agent need to know this later?**

- Repo-specific technical information → that repo's README/docs in the same PR.
- Infrastructure operational information → `infra-configs`.
- Global/cross-repository information → `bytegeist-docs`.
- Learning information → `cka-lab`.

Do not maintain two editable canonical copies of the same explanation.
