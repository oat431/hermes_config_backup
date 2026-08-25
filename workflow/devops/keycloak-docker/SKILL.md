---
name: keycloak-docker
description: Deploy, configure, and troubleshoot Keycloak in Docker containers. Covers realm-as-code, proxy configuration, single-node optimizations, and common pitfalls.
triggers:
  - keycloak deployment
  - keycloak docker
  - keycloak troubleshooting
  - realm import failed
  - keycloak proxy headers
  - keycloak admin bootstrap
---

# Keycloak Docker Deployment

Deploy and operate Keycloak as a Docker container. Covers configuration, realm management, proxy setup, and the most common pitfalls that cause deployment failures.

## When to Use

- Deploying Keycloak for the first time in Docker
- Troubleshooting Keycloak container crashes or startup failures
- Configuring Keycloak behind a reverse proxy (Nginx, Cloudflare)
- Managing realm configuration as code (JSON export/import)

## Prerequisites

- Docker + Docker Compose
- PostgreSQL (shared or dedicated)
- Reverse proxy (Nginx) if exposing externally
- Realm JSON file (if importing on startup)

## Deployment

### Docker Compose Template

```yaml
services:
  keycloak:
    image: quay.io/keycloak/keycloak:latest
    container_name: flowero-guard
    ports:
      - "127.0.0.1:8001:8080"   # Always bind to localhost behind reverse proxy
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://<pg-container>:5432/<db-name>
      KC_DB_USERNAME: <db-user>
      KC_DB_PASSWORD: ${KC_DB_PASSWORD}
      KC_BOOTSTRAP_ADMIN_USERNAME: ${KC_BOOTSTRAP_ADMIN_USERNAME}  # NOT KEYCLOAK_ADMIN (deprecated in KC 26+)
      KC_BOOTSTRAP_ADMIN_PASSWORD: ${KC_BOOTSTRAP_ADMIN_PASSWORD}
      KC_HOSTNAME: <external-domain>
      KC_HTTP_ENABLED: "true"
      KC_PROXY_HEADERS: xforwarded   # NOT KC_PROXY=edge (deprecated)
      KC_CACHE: local                # Required for single-node deployments
    command: ["start", "--import-realm"]
    volumes:
      - ./realm.json:/opt/keycloak/data/import/realm.json:ro
    networks:
      - shared-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G

networks:
  shared-network:
    external: true
    name: db-network  # Or whatever the shared network is called
```

### Key Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `KC_DB` | `postgres` | Database vendor |
| `KC_DB_URL` | `jdbc:postgresql://<container>:5432/<db>` | Use container name on Docker network, NOT `host.docker.internal` |
| `KC_BOOTSTRAP_ADMIN_USERNAME` | `admin` | Creates TEMPORARY admin (KC 26+). Use Post Install to create permanent admin. |
| `KC_BOOTSTRAP_ADMIN_PASSWORD` | *(from .env)* | Never commit |
| `KC_HOSTNAME` | `auth.example.com` | Must match reverse proxy `server_name` |
| `KC_HTTP_ENABLED` | `true` | Accept HTTP internally (proxy handles TLS) |
| `KC_PROXY_HEADERS` | `xforwarded` | Trust X-Forwarded-* headers from proxy |
| `KC_CACHE` | `local` | **Critical for single-node** — disables JGroups clustering |

## Nginx Reverse Proxy

```nginx
server {
    server_name auth.example.com;
    client_max_body_size 10M;  # Keycloak POST bodies can be large

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;  # HARDCODE https when behind Cloudflare
        proxy_set_header X-Forwarded-Host $host;
    }
}
```

**Critical:** When behind Cloudflare Tunnel, Nginx receives HTTP (Cloudflare terminates TLS). `$scheme` would be `http`, causing Keycloak to reject requests with "HTTPS required". Hardcode `X-Forwarded-Proto: https`.

## Realm Management

### Import on Startup

Mount realm JSON to `/opt/keycloak/data/import/` and use `--import-realm` flag:
```yaml
command: ["start", "--import-realm"]
volumes:
  - ./realm.json:/opt/keycloak/data/import/realm.json:ro
```

### Export After Changes

After ANY change in Admin Console:
1. Admin Console → Realm Settings → Action → Partial Export
2. Check "Include groups and roles" + "Include clients"
3. Save JSON to version control

### Realm JSON Rules

- `"sslRequired": "none"` when behind proxy that handles TLS
- Remove `default-roles-panomete` composite client role references (Keycloak creates defaults automatically)
- `optionalClientScopes` must reference scopes that exist in `clientScopes` array
- No plaintext passwords in JSON

## Common Pitfalls

See `references/pitfalls.md` for detailed error messages and fixes.

1. **Docker creates directory instead of file** — If realm JSON doesn't exist on host when container starts, Docker auto-creates a directory at the bind mount path
2. **JGroups clustering timeout** — Without `KC_CACHE=local`, single-node deployments waste 20+ seconds on cluster JOIN attempts
3. **Deprecated env vars** — `KC_PROXY=edge` → `KC_PROXY_HEADERS=xforwarded`; `KEYCLOAK_ADMIN` → `KC_BOOTSTRAP_ADMIN_USERNAME`
4. **HTTPS required error** — Nginx must hardcode `X-Forwarded-Proto: https` when behind Cloudflare
5. **Temporary admin warning** — By design in KC 26+. Create permanent admin via Admin Console, delete temporary one.
6. **Composite role import failure** — Remove client role references from `default-roles-panomete` in realm JSON
7. **curl not in JRE images** — Health checks using `curl` fail in minimal JRE images. Install curl in Dockerfile.

## Post Install (First Deploy)

1. Log in with temporary admin (`KC_BOOTSTRAP_ADMIN_USERNAME`)
2. Users → Create new user → set credentials (Temporary: OFF) → assign `admin` role
3. Log out, log in with permanent admin
4. Delete temporary admin
5. Update `.env` to document new username (password in password manager only)

## Verification

```bash
# Health
curl -sf http://localhost:8001/health/ready

# OIDC Discovery
curl -sf https://auth.example.com/realms/<realm>/.well-known/openid-configuration | jq .issuer

# JWKS
curl -sf https://auth.example.com/realms/<realm>/protocol/openid-connect/certs | jq '.keys | length'

# Admin Console
curl -sf -o /dev/null -w '%{http_code}' https://auth.example.com/admin/
# 302 = redirect to login = working
```
