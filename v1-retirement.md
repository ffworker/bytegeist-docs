# Bytegeist Docs v1 — decommission plan (VPS02)

**This file is a checklist, not permission to delete running services. Status: NOT EXECUTED.**

## Step 1 — prevent accidental republishing

- Disable legacy nightly and workflow dispatch as a publisher; keep the previous site reachable until replacement acceptance if still needed.
- Keep existing private source documentation, Git history and build evidence.

## Step 2 — accept v2 independently of VPS02

- Operator selects and approves a minimal private source set, then Zensical builds and indexes only those docs.
- Deploy to a **non-VPS02** private endpoint with appropriate NetBird ACL and test permitted and denied access.
- Verify search, source provenance and an offline export of critical recovery runbooks. Prove rollback.

## Step 3 — decommission only dedicated v1 components (manual, owner-reviewed)

1. On VPS02 inventory the actual Docs container, Compose service, mounts, filesystem ownership, readers and Traefik references. Record outputs before changing anything.
2. Preserve a last-good v1 export or backup and verify it can be read independently.
3. Remove **only** the dedicated Docs Traefik router/service references from the shared config; preserve NetBird control plane, Termix, Vaultwarden, other TLS, authentication and monitoring.
4. Stop/remove the dedicated Docs container, after verifying no other consumer is affected.
5. Remove only confirmed obsolete `/opt/bytegeist-docs` content, when backups and owners are approved.
6. Revoke only the dedicated Docs deployment SSH identity, GitHub Actions secrets and disposable NetBird setup key after checking their actual consumers. Never remove shared NetBird credentials.
7. Re-test all unrelated VPS02 services and record completion/rollback.

**Do not repair the old `Permission denied` error through broad ownership changes, chmod 777 or root CI.** Build v2 instead.

Tracking: https://linear.app/bytegeist/issue/BYT-108