# CI/CD

`bytegeist-docs` has two explicit outputs:

- PR/push CI builds the public-safe site on every documentation change and builds the private/full site when the approved private-source read credential is available.
- Nightly CD runs at **23:45 Europe/Berlin** using the latest `main` state and latest default branches of all configured source repositories. It also supports `workflow_dispatch`.

The private/full site is retained only as a short-lived private GitHub Actions artifact. The public Pages artifact is built from `docs/public/` only. The workflow cannot use the private generated tree as public deployment input.

Public Pages deployment is conditional on the repository variable `ENABLE_PUBLIC_PAGES=true` and the GitHub Pages target being enabled. Until Dennis performs that account-level setup, the nightly run uploads and verifies the public-safe artifact but skips deployment.

Application repositories own their tests, builds, deployment workflows, and deployment targets. `local-ragbot` intentionally has CI but no production CD. `coach-potato-app` uses a manual staging/VPS-alpha path. CamDash uses a manual environment-gated deployment. Signaturee requires live reconciliation before deployment changes.

Infrastructure CI validates repository artifacts, but infrastructure deployment remains explicitly approval-gated.
