# Bytegeist Docs v2 — private, host-independent deployment

The renderer has no credentials and the web container has **no GitHub access**.
Build the selected content on a trusted machine with read-only access to the
approved repositories; then serve only the generated static files. Never put
the private manifest, its source names, repository clone cache or generated
site in a public commit, GitHub Actions artifact or public registry image.

## Required host (not VPS02)

Choose a maintained Linux host with Docker Compose, a persistent volume,
independent backup/recovery, and an enrolled NetBird peer. This deployment is
**not** a Talos/cluster or VPS02 rollout by default. Check that the host
continues to serve recovery docs during the failure domains you care about.

Before enabling: obtain the host's *actual* NetBird IPv4, decide the peer
groups allowed to read Docs, configure a **deny-by-default NetBird access
policy for the site port**, and verify access from both allowed and denied
peers. NetBird connectivity alone is not access control. Do not use public
DNS/tunnels, `0.0.0.0`, a host LAN IP, wildcard bind, or a shared VPS02 proxy.

## Initial build (inside trusted checkout, on chosen host)

```sh
# Requires python3, git, gh, Docker Compose and an authorized GitHub account.
# gh auth login is performed interactively by the operator, never in a CI log.
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r v2/requirements.txt
cd v2

# The approved manifest MUST be from a separate PRIVATE location.
# Do not copy it to the public repository, or set a public CI variable.
python scripts/curate.py --manifest /secure/private/sources.yml
zensical build --strict --clean -f .generated/mkdocs.yml
test -s .generated/site/index.html
test -s .generated/site/quellstand/index.html
```

Inspect the generated pages and scan for credentials, internal company/customer
material or unexpected source files **before** serving them. The source
collector intentionally skips `_archive` and `evidence` directories; it does
not replace human confidentiality review. Verify the included commit hashes
and date on the Quellstand page. A Git commit is not live system health.

## Private serving

```sh
cd v2
# Export these in the shell or in a private ignored deployment environment.
export NETBIRD_IPV4=REPLACE_WITH_VERIFIED_HOST_NETBIRD_IPV4
export DOCS_PORT=8085
docker compose -f deploy/compose.yaml config
docker compose -f deploy/compose.yaml up -d
docker compose -f deploy/compose.yaml ps
```

The Compose host-port mapping binds **only to NETBIRD_IPV4**, not all host
interfaces; site files are mounted read-only into an unprivileged Caddy
container. NetBird policies and host/router firewall remain separate required
controls. Access is over the encrypted NetBird overlay (HTTP inside the VPN).

## Acceptance and rollback gates

1. Confirm the chosen host is not VPS02 and its static build succeeds from
   only the explicitly approved sources. Check links, search, styling,
   source provenance and absence of stale/archived operational content.
2. From a permitted enrolled peer, open `http://NETBIRD_IPV4:8085/`; from
   a peer outside the authorized NetBird group, verify access is denied.
   Probe the host's LAN and public interfaces and confirm the docs port
   is **not** listening there.
3. Rebuild after a controlled source change and verify the new commit hash
   appears. Preserve an offline export of critical recovery runbooks on
   storage independent of the serving host.
4. Prove recovery on the chosen host before making the v1 URL disappear.
   On failure, retain the last known-good static output and do not retire v1.
5. Only after owner-approved E2E acceptance, follow root
   `v1-retirement.md` for a **dedicated-docs-only**, backed-up VPS02
   decommission. Never remove shared Traefik, NetBird, Termix or Vaultwarden.

No scheduled publishing is enabled by this Compose file. Establish a separate
scoped refresh service/timer only **after** the first private live acceptance,
so failures cannot silently overwrite the last verified site.
