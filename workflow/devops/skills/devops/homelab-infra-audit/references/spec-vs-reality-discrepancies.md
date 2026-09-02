# Spec-vs-Reality Discrepancies

Classic pitfalls found when design specs meet a real Linux homelab server.
These recur across projects — check for every one during Phase 4 of the audit.

---

## 1. `host.docker.internal` — does NOT exist on Linux Docker

**Specs say:** `jdbc:postgresql://host.docker.internal:5432/mydb`
**Reality:** `ping: host.docker.internal: Name or service not known`

`host.docker.internal` is a Docker Desktop feature (Mac/Windows). On Linux
Docker, services reach databases by **container name** on a shared Docker
network.

**Fix in specs + compose:**
```yaml
# WRONG (design doc assumption)
KC_DB_URL: jdbc:postgresql://host.docker.internal:5432/keycloak

# RIGHT (actual server)
KC_DB_URL: jdbc:postgresql://local-postgres:5432/keycloak
```
The service container must join the shared network (`db-network`) for name
resolution to work.

**How to prove it during audit:**
```bash
ssh host 'ping -c1 host.docker.internal'   # fails on Linux
ssh host 'docker exec <svc> ping -c1 local-postgres'  # works if same network
```

---

## 2. Host-level Nginx cannot resolve Docker container names

**Specs say:** `proxy_pass http://flowero-guard:8001;`
**Reality:** Nginx runs as a **host process**, not in a container. It cannot
resolve Docker container names. Every existing config uses `127.0.0.1:PORT`.

**Fix:** Services bind to `127.0.0.1` in compose; Nginx proxies to `127.0.0.1`:
```yaml
# docker-compose.yml — bind to localhost
ports:
  - "127.0.0.1:8001:8080"   # ✅ Nginx can reach via 127.0.0.1:8001
  # - "8001:8080"            # ❌ would expose to LAN/internet
```
```nginx
# Nginx site config
proxy_pass http://127.0.0.1:8001;   # ✅ not http://flowero-guard:8001
```

**Diagnostic:** Check how existing services are configured. If all existing
Nginx configs use `127.0.0.1:PORT`, the new ones must too.

---

## 3. Password-protected databases not in specs

**Specs say:** `host: valkey` (no password field)
**Reality:** Valkey/Redis runs with `--requirepass <password>`.

**How to find the password during audit:**
```bash
docker inspect local-valkey --format '{{range .Config.Cmd}}{{println .}}{{end}}'
# Output:
# valkey-server
# --requirepass
# Saha_6462          ← the actual password, not in any doc
```

**Fix in app config:**
```yaml
spring:
  data:
    redis:
      host: local-valkey      # container name, not "valkey"
      port: 6379
      password: ${VALKEY_PASSWORD}   # must include this!
```

---

## 4. Wildcard DNS = subdomain DNS already done

**MM03 says:** "Add DNS records for auth/api/discovery subdomains"
**Reality:** Cloudflare tunnel config has `*.domain.com → localhost:80`.
Every subdomain works automatically — zero DNS work needed.

**Check:** `sudo cat ~/.cloudflared/config.yml` — look for a `*.` wildcard
ingress rule. If present, flag the "add DNS records" task as ✅ already done.

---

## 5. Non-standard port assumptions (e.g., Eureka dual-port)

**Specs say:** Eureka runs on two ports — 8999 (API) + 3999 (dashboard)
**Reality:** Standard Spring Cloud Netflix Eureka serves BOTH the REST API and
the HTML dashboard on a **single port** (the dashboard is at `/`, the API at
`/eureka/**`). Splitting them requires custom config or a second embedded server.

**Flag as 🟡 non-blocking concern** — the Dev should verify feasibility before
implementing the story.

---

## 6. Stale configs from previous iterations

**Found:** `gateway.panomete.com` Nginx config pointing to `:8000` left over
from an earlier design. The new design uses `api.panomete.com`.

**Action:** Identify stale configs by comparing Nginx site files against the
current architecture. Remove/replace as part of deployment prep.

---

## 7. `$scheme` is `http` behind Cloudflare Tunnel

**Specs say:** `proxy_set_header X-Forwarded-Proto $scheme;`
**Reality:** Cloudflare Tunnel terminates TLS and sends plain HTTP to Nginx.
`$scheme` is `http`, not `https`. Services that check the protocol (Keycloak
with `sslRequired: external`) reject requests with `"HTTPS required"` (403).

**Fix:** Hardcode `proxy_set_header X-Forwarded-Proto https;` in Nginx configs
for services behind Cloudflare. The proxy headers config (`KC_PROXY_HEADERS:
xforwarded` for Keycloak) tells the service to TRUST the headers, but Nginx
must SEND the correct values.

**Diagnostic:**
```bash
# Check what Nginx sends
curl -sv -H 'Host: auth.example.com' http://localhost/realms/.../openid-configuration 2>&1 | grep -i x-forwarded
# If X-Forwarded-Proto: http → that's the problem
```

---

## 8. Realm JSON `sslRequired` overrides env var

**Specs say:** `KC_SSL_REQUIRED=none` in compose environment
**Reality:** The realm JSON's `"sslRequired": "external"` takes precedence over
the env var. Keycloak uses the realm-level setting, not the global one.

**Fix:** Either change realm JSON to `"sslRequired": "none"`, or fix Nginx to
send `X-Forwarded-Proto https` (preferred — keeps HTTPS enforcement).

---

## 9. Deprecated Keycloak admin env vars (KC 26+)

**Specs say:** `KEYCLOAK_ADMIN` / `KEYCLOAK_ADMIN_PASSWORD`
**Reality:** Keycloak 26+ renamed to `KC_BOOTSTRAP_ADMIN_USERNAME` /
`KC_BOOTSTRAP_ADMIN_PASSWORD`. The old names produce deprecation warnings.
Additionally, the bootstrap admin is always **temporary** — user must create
a permanent admin via Admin Console.

**Fix:** Update compose env vars. Document "Post Install" step for permanent
admin creation.

---

## Audit checklist — run through all 9 every time

- [ ] Does any spec reference `host.docker.internal`? → replace with container name
- [ ] Do any Nginx proxy targets use container names? → replace with `127.0.0.1:PORT`
- [ ] Are databases password-protected? Is the password in the app config?
- [ ] Is DNS wildcard? Are "add DNS" tasks redundant?
- [ ] Are there non-standard port/architecture assumptions? Flag for Dev.
- [ ] Are there stale configs from prior design iterations?
- [ ] Does any Nginx config use `$scheme` behind Cloudflare? → hardcode `https`
- [ ] Do Keycloak env vars use deprecated `KEYCLOAK_ADMIN`? → update to `KC_BOOTSTRAP_ADMIN_*`
- [ ] Does realm JSON have `sslRequired` that might override env vars?
