---
name: keycloak-deployment
description: Deploy, configure, and troubleshoot Keycloak in Docker behind Nginx plus Cloudflare Tunnel on a homelab server. Covers realm JSON authoring, compose configuration, common startup failures, and the full troubleshooting path discovered during Panomete Platform Sprint 1.
tags: [keycloak, iam, oauth2, oidc, docker, homelab, devops, panomete]
triggers:
  - keycloak deploy / setup / install / configure
  - keycloak not starting / crash loop / 502 / error
  - realm JSON import fails
  - HTTPS required on auth subdomain
  - KC_PROXY / KC_CACHE / KC_SSL_REQUIRED
  - flowero-guard container issues
---

# Keycloak Deployment & Troubleshooting

## Overview

Deploy Keycloak as a Docker container (`flowero-guard`) on a homelab server behind Nginx reverse proxy and Cloudflare Tunnel. Keycloak is the identity provider (IAM) for the Panomete Platform — it IS Flowero Guard (no wrapper service).

## Prerequisites

- PostgreSQL running on `db-network` (container: `local-postgres`)
- Nginx running on host port 80
- Cloudflare Tunnel active with `*.panomete.com` wildcard
- `keycloak` database + role created on PostgreSQL (see references/database-setup.md)

## Critical Pitfalls (Lessons Learned)

### 1. Docker bind mount creates directory if file doesn't exist

If the `panomete-realm.json` file doesn't exist on the host when the container starts, Docker **auto-creates a directory** at that path. Keycloak then tries to import a directory and crash-loops with:
```
ERROR: /opt/keycloak/data/import/panomete-realm.json (Is a directory)
```

**Prevention:** Always create the realm JSON file on the host BEFORE starting the container. Verify it's a file, not a directory:
```bash
ls -la /path/to/panomete-realm.json
# Must show: -rw-r--r-- ... (file)
# NOT:       drwxr-xr-x ... (directory)
```

**Fix:** `rm -rf` the directory, create the actual file, restart.

### 2. JGroups clustering timeout on single-node deployment

Keycloak tries to form a distributed cache cluster (Infinispan/JGroups) even on a single node. This causes 20+ seconds of JOIN timeout warnings on every boot.

**Fix:** Add `KC_CACHE: local` to compose environment. Cuts startup from ~60s to ~15s.

### 3. `KC_PROXY=edge` is deprecated in Keycloak 26+

**Fix:** Replace with `KC_PROXY_HEADERS: xforwarded`. Remove `KC_PROXY=edge` entirely.

### 4. `sslRequired` in realm JSON overrides the `KC_SSL_REQUIRED` env var

If the realm JSON has `"sslRequired": "external"`, Keycloak rejects HTTP requests even if `KC_SSL_REQUIRED=none` is set. The realm-level setting wins.

**Fix:** Set `"sslRequired": "none"` in the realm JSON for homelab behind Cloudflare, OR fix Nginx to send proper proxy headers (see pitfall 5).

### 5. `X-Forwarded-Proto` must be hardcoded to `https`

Nginx's `$scheme` variable reflects the incoming request scheme. Since Cloudflare terminates TLS and sends HTTP to Nginx, `$scheme` = `http`. Keycloak sees HTTP and rejects with "HTTPS required".

**Fix in Nginx:**
```nginx
proxy_set_header X-Forwarded-Proto https;    # NOT $scheme
proxy_set_header X-Forwarded-Host $host;
```

### 6. `KEYCLOAK_ADMIN` / `KEYCLOAK_ADMIN_PASSWORD` are deprecated

Keycloak 26+ renamed these to:
- `KC_BOOTSTRAP_ADMIN_USERNAME`
- `KC_BOOTSTRAP_ADMIN_PASSWORD`

### 7. Bootstrap admin is ALWAYS temporary by design

`KC_BOOTSTRAP_ADMIN_*` creates a temporary admin user. The warning "You are logged in as a temporary admin user" cannot be suppressed via env vars. This is by design (GitHub issue #34768).

**Fix:** Log in with temporary admin, create a permanent admin user in the Admin Console, assign `admin` role, log in as permanent admin, delete temporary admin.

### 8. Realm JSON composite roles must reference existing client roles

If a composite role references client roles (e.g., `account.view-profile`) that aren't defined in the realm JSON, Keycloak fails with:
```
ERROR: Unable to find composite client role: view-profile
```

**Fix:** Remove client role references from composite roles, or define the client roles in the JSON. Safest: remove `default-roles-panomete` entirely — Keycloak creates it automatically.

### 9. Missing `optionalClientScopes` cause warnings but not crashes

Referencing client scopes like `address`, `phone`, `microprofile-jwt` in `optionalClientScopes` that aren't defined in `clientScopes` produces warnings. Not fatal, but noisy.

**Fix:** Remove undefined scopes from `optionalClientScopes`, or define them in `clientScopes`.

### 10. `Permission denied` when editing realm JSON inside container volume

If the realm JSON was created by Docker (as root), the `flowero` user can't edit it.

**Fix:** `sudo chown flowero:flowero /path/to/panomete-realm.json`

## Recommended Compose Environment

```yaml
environment:
  KC_DB: postgres
  KC_DB_URL: jdbc:postgresql://local-postgres:5432/keycloak
  KC_DB_USERNAME: ${KC_DB_USERNAME}
  KC_DB_PASSWORD: ${KC_DB_PASSWORD}
  KC_BOOTSTRAP_ADMIN_USERNAME: ${KC_BOOTSTRAP_ADMIN_USERNAME}
  KC_BOOTSTRAP_ADMIN_PASSWORD: ${KC_BOOTSTRAP_ADMIN_PASSWORD}
  KC_HOSTNAME: auth.panomete.com
  KC_HTTP_ENABLED: "true"
  KC_PROXY_HEADERS: xforwarded    # Trust X-Forwarded-* from Nginx
  KC_CACHE: local                  # Single-node, no JGroups clustering
```

**Do NOT add:** `KC_SSL_REQUIRED` (not needed with proper proxy headers + realm JSON `sslRequired: none`)

## Nginx Config

```nginx
server {
    server_name auth.panomete.com;
    client_max_body_size 10M;    # Keycloak POST bodies can be large

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;    # Hardcoded, NOT $scheme
        proxy_set_header X-Forwarded-Host $host;
    }
}
```

## Management Port 9000 (Keycloak 26+ with Quarkus)

Keycloak runs a **separate management interface** on port 9000. Health and metrics endpoints are on this port, NOT the main application port 8080.

| Endpoint | Port | URL |
|----------|:----:|-----|
| Main application | 8080 | `http://localhost:8080/realms/panomete` |
| Health | 9000 | `http://localhost:9000/health/ready` |
| Metrics | 9000 | `http://localhost:9000/metrics` |

**Compose changes needed:**
```yaml
ports:
  - "127.0.0.1:8001:8080"   # Main app
  - "127.0.0.1:9000:9000"   # Management (health + metrics)
environment:
  KC_METRICS_ENABLED: "true"   # Enable /metrics on port 9000
  KC_HEALTH_ENABLED: "true"    # Enable /health on port 9000
healthcheck:
  test: ["CMD-SHELL", "timeout 5 bash -c '</dev/tcp/localhost:8080' || exit 1"]
  # Keycloak image has NO tools (no curl, wget, which) — use TCP check
```

**Prometheus scrape target must use port 9000:**
```yaml
- job_name: "flowero-guard"
  metrics_path: "/metrics"
  static_configs:
    - targets: ["flowero-guard:9000"]  # NOT 8080
```

## Verification Checklist

After deployment, verify all endpoints:
```bash
# Health — management port 9000 (NOT 8001)
curl -sf http://localhost:9000/health/ready

# Metrics — management port 9000
curl -sf http://localhost:9000/metrics | head -5

# OIDC Discovery — main port 8001 (maps to 8080)
curl -sf https://auth.panomete.com/realms/panomete/.well-known/openid-configuration | jq .issuer

# JWKS (critical for Gate's JWT validation)
curl -sf https://auth.panomete.com/realms/panomete/protocol/openid-connect/certs | jq '.keys | length'

# Admin Console
curl -sf -o /dev/null -w '%{http_code}' https://auth.panomete.com/admin/  # Should be 302

# Realm endpoint
curl -sf https://auth.panomete.com/realms/panomete | jq .public_key
```

## Database Cleanup (When Realm Import Corrupts)

```bash
docker stop flowero-guard
docker exec local-postgres psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='keycloak';"
docker exec local-postgres psql -U postgres -c "DROP DATABASE IF EXISTS keycloak;"
docker exec local-postgres psql -U postgres -c "CREATE DATABASE keycloak WITH ENCODING 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8' OWNER keycloak;"
docker exec local-postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;"
# Then restart — Keycloak re-runs Liquibase + re-imports realm from JSON
```

## Related Skills

- `homelab-infra-audit` — Infrastructure verification before deployment
