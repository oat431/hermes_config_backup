# Docker DNS loopback trap — containers get `getaddrinfo ENOTFOUND`

A single-server homelab often runs a local DNS resolver (AdGuard Home, Pi-hole,
Blocky) in a container bound to `0.0.0.0:53`, then points the host's
`/etc/resolv.conf` at `127.0.0.1`. This silently breaks public-DNS resolution
inside a whole class of Docker containers. Full real-world case below.

## Symptom

- A container's job that depends on resolving public hostnames fails. Classic
  example: **Uptime Kuma** — every monitor flips to DOWN with
  `getaddrinfo ENOTFOUND <domain>` (e.g. `auth.panomete.com`), even though the
  monitored sites are actually up.
- Containers still show `(healthy)` and still resolve *internal* container
  names — so the stack "looks fine" while public DNS is dead.
- `docker exec <c> node -e 'require("dns").resolve4("example.com",(e,a)=>console.log(e.code))'`
  → `ESERVFAIL` (or `ENOTFOUND`).

## Root cause

1. Host `/etc/resolv.conf` has a **loopback** nameserver first:
   ```
   nameserver 127.0.0.1     # AdGuard in a container, owns 0.0.0.0:53
   nameserver 1.1.1.1       # fallback added later
   ```
2. Docker's embedded DNS (`127.0.0.11` in every container) forwards external
   queries to upstreams it derives from the host's `resolv.conf` — but it
   **ignores loopback (`127.0.0.0/8`) nameservers**.
3. During any window where `resolv.conf` had *only* the loopback nameserver,
   the embedded resolver had **no upstream** → it answers every external query
   with `SERVFAIL`.
4. Docker writes each container's `/etc/resolv.conf` **at container creation
   and never updates it** on running containers. So containers created during
   that window keep the broken config even after the host `resolv.conf` is
   fixed and the daemon has re-read it. New containers are fine; old ones are
   not — hence the delayed, "sudden" failure.

## Detection

Compare a broken container vs a fresh one on the same network:

```bash
# BROKEN container:
docker exec <name> cat /etc/resolv.conf
#   nameserver 127.0.0.11
#   # NO EXTERNAL NAMESERVERS DEFINED
#   # Based on host file: '' (internal resolver)

# WORKING (fresh) container on the same network:
docker run --rm --network db-network alpine:3.20 cat /etc/resolv.conf
#   nameserver 127.0.0.11
#   # ExtServers: [host(127.0.0.1) host(1.1.1.1)]
```

Key discriminator: `NO EXTERNAL NAMESERVERS DEFINED` (broken) vs
`ExtServers: [...]` (working). Also prove the fix path: the fresh container
resolves (`nslookup example.com` succeeds) while the old one SERVFAILs.

Enumerate the blast radius in one pass:

```bash
for c in $(docker ps --format '{{.Names}}'); do
  docker exec "$c" cat /etc/resolv.conf 2>/dev/null \
    | grep -q 'NO EXTERNAL NAMESERVERS DEFINED' && echo "BROKEN: $c"
done
```

## Fix — recreate (NOT restart)

A plain `docker restart` keeps the same container and its stale
`resolv.conf`. You must **recreate** so Docker regenerates the file:

```bash
# per service (data safe — all state is in named volumes):
cd <compose-dir> && docker compose up -d --force-recreate <service>

# bulk, grouped by compose file, dependencies-aware order:
#   observability -> discover -> databases (one at a time) -> apps -> DNS-resolver LAST
```

The DNS resolver container itself (AdGuard) is the one recreation that has a
real blast radius — it owns `:53`, so recreating it is a ~2s DNS blip for the
whole host/network. Do it last, and only if it's actually broken (it often
isn't — AdGuard uses its own upstream config, not the container's resolv.conf).

**Verify** after recreate: `docker exec <c> cat /etc/resolv.conf` now shows
`ExtServers: [...]`, and a `curl -s -o /dev/null -w '%{http_code}' https://<domain>`
full-path check returns the expected code. Watch for a transient 502 on the
service you just recreated (it fires while the container is briefly down) —
it clears on the next check cycle.

## Prevention (permanent guard)

Pin explicit upstreams in `/etc/docker/daemon.json` so the embedded resolver
always has a non-loopback upstream regardless of host `resolv.conf` edits:

```json
{ "dns": ["1.1.1.1", "8.8.8.8"] }
```

Requires `systemctl restart docker` (restarts ALL containers — ~1 min outage,
needs a maintenance window). Trade-off: containers then bypass the local
resolver's ad-blocking/rewrites, which is acceptable for public-domain
monitors and usually fine for a homelab.

## When this bites vs. the 502 ladder

The 502 ladder (container → port → Nginx → logs) does NOT catch this — the
container is up and healthy, Nginx is fine, the *target* is fine. When the
error is `getaddrinfo ENOTFOUND` / `SERVFAIL` / `ESERVFAIL`, skip the ladder and
go straight to the resolv.conf comparison above.
