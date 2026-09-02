# Keycloak on a Homelab Server — Deployment Reference

Non-obvious configuration details for deploying Keycloak behind a
Cloudflare → Nginx → Docker stack on a Linux homelab. Capture from real
deployments — these settings are the difference between a working Keycloak
and a silent failure.

---

## Docker Compose service definition (verified pattern)

```yaml
services:
  flowero-guard:                      # or your service name
    image: quay.io/keycloak/keycloak:latest
    container_name: flowero-guard
    ports:
      - "127.0.0.1:8001:8080"         # Keycloak internal :8080 → host :8001
                                      # MUST bind 127.0.0.1 for Nginx proxy
    environment:
      KC_DB: postgres
      # Container name, NOT host.docker.internal (Linux Docker):
      KC_DB_URL: jdbc:postgresql://local-postgres:5432/keycloak
      KC_DB_USERNAME: ${KC_DB_USERNAME}
      KC_DB_PASSWORD: ${KC_DB_PASSWORD}
      KEYCLOAK_ADMIN: ${KEYCLOAK_ADMIN}
      KEYCLOAK_ADMIN_PASSWORD: ${KEYCLOAK_ADMIN_PASSWORD}
      KC_HOSTNAME: auth.example.com   # external hostname Keycloak advertises
      KC_HTTP_ENABLED: "true"         # accept HTTP internally (CF handles TLS)
      KC_PROXY_HEADERS: xforwarded    # trust X-Forwarded-* from Nginx/Cloudflare
                                      # (replaces deprecated KC_PROXY=edge in Keycloak 25+)
      KC_CACHE: local                 # single-node only — disables JGroups distributed caching
                                      # without this, startup delays 20s+ from cluster JOIN timeouts
    command: ["start", "--import-realm"]
    volumes:
      - ./panomete-realm.json:/opt/keycloak/data/import/panomete-realm.json:ro
    networks:
      - shared-network                # join db-network for DB access
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G                  # Keycloak is JVM-heavy

networks:
  shared-network:
    external: true
    name: db-network
```

---

## Environment variables — what each does

| Variable | Purpose | Why it matters |
|----------|---------|----------------|
| `KC_PROXY_HEADERS: xforwarded` | Tells Keycloak to trust X-Forwarded-* headers from the reverse proxy | Without this, Keycloak generates wrong redirect URLs and CORS checks fail with 403. Replaces deprecated `KC_PROXY=edge` in Keycloak 25+. |
| `KC_HTTP_ENABLED: "true"` | Allows Keycloak to accept plain HTTP internally | Required because Cloudflare terminates TLS externally and Nginx → Keycloak is plain HTTP on the trusted network |
| `KC_CACHE: local` | Disables JGroups distributed caching | Single-node only. Without this, Keycloak tries to form a cluster with other nodes, timing out 10×2s=20s per boot. Logs fill with `JOIN sent to xxx timed out`. |
| `KC_HOSTNAME` | The external hostname Keycloak uses in tokens and OIDC discovery | Must match the domain in Nginx/Cloudflare. Tokens' `iss` claim uses this. |
| `--import-realm` (command flag) | Imports realm JSON on startup | Realm config lives in version-controlled JSON, not manually configured via Admin Console |
| `KC_DB_URL` | JDBC connection string | Must use container name (`local-postgres`), not `host.docker.internal` (Linux Docker) |
| `KC_BOOTSTRAP_ADMIN_USERNAME` | Bootstrap admin username | **Deprecated:** `KEYCLOAK_ADMIN` (KC 26+). Always creates a TEMPORARY admin — user must create permanent admin via Admin Console. See "Post Install" below. |
| `KC_BOOTSTRAP_ADMIN_PASSWORD` | Bootstrap admin password | **Deprecated:** `KEYCLOAK_ADMIN_PASSWORD` (KC 26+). Same temporary-only behavior. |

---

## PostgreSQL provisioning (run before first boot)

```sql
CREATE ROLE keycloak WITH LOGIN PASSWORD '<password>';
CREATE DATABASE keycloak
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    OWNER keycloak;
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
GRANT ALL ON SCHEMA public TO keycloak;
```

Keycloak uses Liquibase to create its own schema (~50+ tables) on first boot.
Do NOT write DDL for Keycloak's internal tables — Liquibase manages them.

---

## Nginx server block

```nginx
server {
    server_name auth.example.com;
    client_max_body_size 10M;          # Keycloak POST bodies can be large

    location / {
        proxy_pass http://127.0.0.1:8001;   # 127.0.0.1, not container name
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;   # ← HARDCODE 'https', NOT $scheme
        # Cloudflare terminates TLS and sends HTTP to Nginx via tunnel.
        # $scheme is 'http' behind Cloudflare — Keycloak sees HTTP and rejects
        # with "HTTPS required" (403). Hardcoding 'https' fixes this.
    }
}
```

`client_max_body_size 10M` is required — without it, large OAuth POST requests
(especially during login with SAML or large JWT exchanges) get silently
truncated and fail with confusing errors.

**Pitfall:** The `X-Forwarded-Proto` must be `https` (hardcoded), not `$scheme`.
Cloudflare Tunnel terminates TLS and sends plain HTTP to Nginx. `$scheme` would
be `http`, causing Keycloak to reject external requests with `"HTTPS required"`.
This is the #1 cause of 403 errors on `auth.*.com` endpoints.

---

## First-boot behavior

On first startup, Keycloak:
1. Connects to PostgreSQL via JDBC
2. Runs Liquibase migrations (creates 50+ tables in the `keycloak` DB)
3. Imports realm JSON (if `--import-realm` and file is mounted)
4. Becomes ready (`/health/ready` returns 200)

This takes **15-60 seconds** depending on hardware. Subsequent starts are
faster (Liquibase only checks for pending changes).

### ⚠️ CRITICAL: The volume mount directory-creation trap

If the realm JSON file **does not exist on the host** when the container starts,
Docker **silently creates a DIRECTORY** at the mount path instead of failing.
Keycloak then crashes on import:

```
ERROR: /opt/keycloak/data/import/panomete-realm.json (Is a directory)
ERROR: Failed to run import
```

The container enters a restart loop (RestartCount climbs to 7+). This is the
**#1 cause of Keycloak crash loops on first deploy.**

**Prevention:** ALWAYS create the realm JSON file on the host BEFORE starting
the container. Use `templates/realm-template.json` as a starting point.

**Fix if already happened:**
```bash
docker stop flowero-guard && docker rm flowero-guard
rm -rf /path/to/panomete-realm.json     # remove the auto-created directory
# Create the actual JSON file at that path, then:
docker compose up -d flowero-guard      # must RECREATE, not just restart
```

**Verify the mount is a file, not a directory:**
```bash
ls -la /path/to/panomete-realm.json
# -rw-r--r-- = file ✅
# drwxr-xr-x = directory ❌ (Docker trap)
```

If the realm JSON isn't mounted or the `--import-realm` flag is missing,
Keycloak starts but only the `master` realm exists — the project realm is
missing. Diagnose with:
```bash
docker exec flowero-guard ls /opt/keycloak/data/import/
docker inspect flowero-guard --format '{{.Config.Cmd}}'
```

---

## CI/CD — Keycloak is config-only (no Java to compile)

Unlike Spring Boot services, Keycloak's "source code" is the realm JSON. The
CI pipeline validates the JSON rather than compiling code:

```yaml
jobs:
  validate-realm:
    steps:
      - run: jq . panomete-realm.json > /dev/null          # valid JSON
      - run: |                                              # required fields
          REALM=$(jq -r '.realm' panomete-realm.json)
          [ "$REALM" = "panomete" ] || exit 1
      - run: |                                              # required roles exist
          for ROLE in admin user viewer; do
            jq -e --arg r "$ROLE" '.roles.realm[].name == $r' panomete-realm.json || exit 1
          done
      - run: |                                              # no plaintext secrets
          grep -qiE '(password|secret).{0,5}:.{0,5}["'\''][^"'\'']{6,}' panomete-realm.json && exit 1 || true
```

---

## Common troubleshooting (from real deployment)

| Symptom | Cause | Fix |
|---------|-------|-----|
| OAuth redirects to `http://` instead of `https://` | Missing `KC_PROXY_HEADERS` or using deprecated `KC_PROXY=edge` | Replace with `KC_PROXY_HEADERS: xforwarded` |
| `WARN: Likely misconfiguration detected. With HTTPS not enabled, proxy-headers unset` | Missing `KC_PROXY_HEADERS` — Keycloak doesn't know it's behind Nginx/Cloudflare | Add `KC_PROXY_HEADERS: xforwarded` to compose env |
| `WARN: Hostname v1 options [proxy] are still in use` | `KC_PROXY=edge` is deprecated in Keycloak 25+ | Remove `KC_PROXY=edge`, add `KC_PROXY_HEADERS=xforwarded` |
| `JOIN sent to xxx timed out` (repeated 10+ times, startup takes 60s+) | JGroups trying to form distributed cluster on single-node deployment | Add `KC_CACHE: local` to compose env. Cuts startup from ~60s to ~15s. |
| Token `iss` claim has wrong hostname | Missing or wrong `KC_HOSTNAME` | Set `KC_HOSTNAME: auth.example.com` |
| Realm "panomete" missing, only "master" exists | Realm JSON not mounted or `--import-realm` missing | Check volume mount + command |
| Container starts then exits — JDBC error | Wrong `KC_DB_URL` (e.g., `host.docker.internal`) or DB/role missing | Use container name; verify DB + role exist |
| Large POST requests fail silently | Missing `client_max_body_size` in Nginx | Add `client_max_body_size 10M` |
| `HTTPS required` (403 on external access) | Keycloak rejects HTTP from Nginx — `$scheme` is `http` behind Cloudflare tunnel | Hardcode `proxy_set_header X-Forwarded-Proto https;` in Nginx (not `$scheme`). Cloudflare terminates TLS, so Nginx always receives HTTP. |
| `Unable to find composite client role: view-profile` | Realm JSON composite role references client roles that don't exist in the JSON | Remove client role references from composite, or define the client roles explicitly. Drop DB + re-import with fixed JSON. |
| `KEYCLOAK_ADMIN is deprecated, use KC_BOOTSTRAP_ADMIN_USERNAME` | Keycloak 26+ renamed the admin bootstrap env vars | Replace `KEYCLOAK_ADMIN` → `KC_BOOTSTRAP_ADMIN_USERNAME`, `KEYCLOAK_ADMIN_PASSWORD` → `KC_BOOTSTRAP_ADMIN_PASSWORD` |
| Warning: "You are logged in as a temporary admin user" | `KC_BOOTSTRAP_ADMIN_*` always creates temporary admins (by design in KC 26+) | Create permanent admin via Admin Console → Users → Create → set password (Temporary: OFF) → assign `admin` role → delete temp admin |
| `sslRequired` env var ignored | Realm JSON `"sslRequired": "external"` overrides `KC_SSL_REQUIRED` env var | Either change realm JSON to `"sslRequired": "none"`, or fix Nginx to send `X-Forwarded-Proto https` (preferred) |
| Startup takes very long (> 60s) | First-boot Liquibase migrations | Normal — wait. Subsequent starts are fast. |
| "too many clients" from PostgreSQL | Connection pool exhausted | Increase `KC_DB_POOL_MAX_SIZE` (default 20) |

---

## Realm export workflow

After ANY realm change via Admin Console (new client, role, user):
1. Admin Console → Realm Settings → Action → Partial Export
2. Check "Include groups and roles" + "Include clients"
3. Download JSON → save to repo as `panomete-realm.json`
4. Commit: `chore(guard): export realm config YYYY-MM-DD`
5. The next CI/deploy pipeline picks it up via `--import-realm`

---

## Post Install — create permanent admin (Keycloak 26+)

`KC_BOOTSTRAP_ADMIN_USERNAME` / `KC_BOOTSTRAP_ADMIN_PASSWORD` always create a
**temporary** admin — this is by design ([GitHub #34768](https://github.com/keycloak/keycloak/issues/34768)).
There's no way to make it permanent via env vars.

After first boot:
1. Log in to Admin Console with the temporary admin
2. Users → Create new user (username, email, name)
3. Credentials tab → Set password → **Temporary: OFF** → Save
4. Role mapping tab → Assign role → `admin`
5. Log out → log in with new permanent admin
6. Delete the temporary `admin` user

The warning "You are logged in as a temporary admin user" disappears once
logged in as the permanent admin.

---

## Realm JSON pitfalls

### Composite roles referencing undefined client roles → crash

If a composite role references client roles that don't exist in the JSON:
```json
{
  "name": "default-roles-panomete",
  "composite": true,
  "composites": {
    "realm": ["user"],
    "client": {
      "account": ["view-profile", "manage-account"]  ← NOT DEFINED → CRASH
    }
  }
}
```

Keycloak crashes with: `Unable to find composite client role: view-profile`

**Fix:** Remove client role references from composites, or define the client
roles explicitly in the `clients` section. Drop DB + re-import with fixed JSON.

### `sslRequired` in realm JSON overrides env var

The realm JSON's `"sslRequired": "external"` takes precedence over the
`KC_SSL_REQUIRED` env var. If you set `KC_SSL_REQUIRED=none` but the realm
JSON says `"external"`, Keycloak still requires HTTPS.

**Fix:** Either change the realm JSON to `"sslRequired": "none"`, or (preferred)
fix Nginx to send `X-Forwarded-Proto https` so Keycloak sees the original HTTPS.

### `optionalClientScopes` referencing undefined scopes → warnings

Referencing scopes like `address`, `phone`, `microprofile-jwt` in client
`optionalClientScopes` without defining them in `clientScopes` produces warnings
(not errors): `Referenced client scope 'address' doesn't exist. Ignoring`

**Fix:** Either define the scopes in `clientScopes`, or remove them from
`optionalClientScopes`. These are warnings, not crashes — but a clean JSON
avoids noise in logs.
