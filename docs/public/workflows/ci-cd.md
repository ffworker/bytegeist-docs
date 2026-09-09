# CI/CD

Application repositories own their tests, builds, deployment workflows, and deployment targets. `local-ragbot` intentionally has CI but no production CD. `coach-potato-app` uses a manual staging/VPS-alpha path. CamDash uses a manual environment-gated deployment. Signaturee requires live reconciliation before deployment changes.

Infrastructure CI validates repository artifacts, but infrastructure deployment remains explicitly approval-gated.
