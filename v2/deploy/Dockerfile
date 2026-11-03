# The upstream Caddy binary carries cap_net_bind_service=+ep.
# With cap_drop: ALL this triggers execve(EPERM) even when Caddy listens on 8080.
# Static docs need no privileged port, so remove the binary file capability.
# Keep the non-root user, drop-all, no-new-privileges and read-only rootfs.
FROM caddy:2.10.2-alpine
RUN setcap -r /usr/bin/caddy && test -z "$(getcap /usr/bin/caddy)"
