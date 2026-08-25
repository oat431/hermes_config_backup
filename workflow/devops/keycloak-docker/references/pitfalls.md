# Keycloak Docker Pitfalls — Session Reference

Specific errors encountered and their fixes. Organized by error message for quick lookup.

## "panomete-realm.json (Is a directory)"

**Error:**
```
ERROR: /opt/keycloak/bin/../data/import/panomete-realm.json (Is a directory)
ERROR: Failed to run import
ERROR: Failed to start server in (production) mode
```

**Cause:** Docker bind mount creates a directory when the source path doesn't exist. If you start the container before creating the realm JSON file, Docker auto-creates a directory at that path.

**Verify:**
```bash
docker exec <container> ls -la /opt/keycloak/data/import/
# drwxr-xr-x ... panomete-realm.json  ← DIRECTORY (wrong)
# -rw-r--r-- ... panomete-realm.json  ← FILE (correct)
```

**Fix:**
```bash
docker stop <container> && docker rm <container>
rm -rf /path/to/realm.json   # Remove the auto-created directory
# Create the actual JSON file first
cat > /path/to/realm.json << 'EOF'
{ ... }
EOF
# Then restart
docker compose up -d
```

**Prevention:** Always create the realm JSON file on the host BEFORE starting the container.

---

## "Unable to find composite client role: view-profile"

**Error:**
```
ERROR: Unable to find composite client role: view-profile
ERROR: Failed to start server in (production) mode
```

**Cause:** The `default-roles-panomete` composite role in realm JSON references client roles (`view-profile`, `manage-account`) on the `account` client that don't exist yet. Keycloak can't find them during import.

**Fix:** Remove client role references from the composite role:
```json
{
    "name": "default-roles-panomete",
    "composite": true,
    "composites": {
        "realm": ["user"]
        // Remove: "client": { "account": ["view-profile", "manage-account"] }
    }
}
```

**Prevention:** Don't include `default-roles-panomete` in realm JSON at all — Keycloak creates it automatically with the correct defaults.

---

## "WARN: Hostname v1 options [proxy] are still in use"

**Error:**
```
WARNING: Hostname v1 options [proxy] are still in use, please review your configuration
```

**Cause:** `KC_PROXY=edge` is deprecated in Keycloak 26+.

**Fix:** Remove `KC_PROXY=edge`, add `KC_PROXY_HEADERS=xforwarded`:
```yaml
# Old (deprecated)
KC_PROXY: edge

# New
KC_PROXY_HEADERS: xforwarded
```

---

## "WARN: Likely misconfiguration detected. With HTTPS not enabled, proxy-headers unset"

**Error:**
```
WARNING: Likely misconfiguration detected. With HTTPS not enabled, `proxy-headers` unset, and a non-URL `hostname`, the server is running in an insecure context.
```

**Cause:** Missing `KC_PROXY_HEADERS` — Keycloak doesn't know it's behind a reverse proxy.

**Fix:** Add `KC_PROXY_HEADERS: xforwarded` to compose environment.

---

## "HTTPS required" (403 on external access)

**Error:**
```json
{"error":"invalid_request","error_description":"HTTPS required"}
```

**Cause:** Keycloak rejects HTTP requests because it doesn't know the original request was HTTPS (Cloudflare handles TLS, Nginx sends HTTP).

**Fix:** Hardcode `X-Forwarded-Proto: https` in Nginx config:
```nginx
proxy_set_header X-Forwarded-Proto https;  # NOT $scheme (would be 'http')
```

**Why:** Cloudflare Tunnel terminates TLS. Nginx receives HTTP on port 80. `$scheme` = `http`. Keycloak sees HTTP and rejects it.

---

## "KEYCLOAK_ADMIN is deprecated, use KC_BOOTSTRAP_ADMIN_USERNAME instead"

**Error:**
```
WARN [org.keycloak.services] KC-SERVICES0110: Environment variable 'KEYCLOAK_ADMIN' is deprecated, use 'KC_BOOTSTRAP_ADMIN_USERNAME' instead
```

**Cause:** Keycloak 26+ renamed the admin bootstrap environment variables.

**Fix:**
```yaml
# Old (deprecated)
KEYCLOAK_ADMIN: admin
KEYCLOAK_ADMIN_PASSWORD: ***

# New
KC_BOOTSTRAP_ADMIN_USERNAME: admin
KC_BOOTSTRAP_ADMIN_PASSWORD: ***
```

---

## "JOIN sent to xxx timed out" (repeated many times)

**Error:**
```
WARN [org.jgroups.protocols.pbcast.GMS] JOIN(xxx) sent to yyy timed out (after 2000 ms), on try 1
... (repeats 10+ times)
```

**Cause:** Keycloak tries to form a distributed cache cluster (Infinispan/JGroups) with other nodes. On single-node deployments, there are no other nodes — it wastes 20+ seconds on JOIN attempts before becoming a singleton.

**Fix:** Add `KC_CACHE: local` to compose environment:
```yaml
KC_CACHE: local  # Disables distributed caching, cuts startup from ~60s to ~15s
```

---

## "You are logged in as a temporary admin user"

**Not an error — by design in Keycloak 26+.**

`KC_BOOTSTRAP_ADMIN_USERNAME`/`KC_BOOTSTRAP_ADMIN_PASSWORD` always create a temporary admin. This is intentional ([GitHub #34768](https://github.com/keycloak/keycloak/issues/34768)).

**Fix (Post Install):**
1. Log in with temporary admin
2. Users → Create new user → Credentials (Temporary: OFF) → Role mapping (admin)
3. Log out, log in with permanent admin
4. Delete temporary admin

---

## Container shows "unhealthy" in Portainer

**Cause:** Health check uses `curl` but it's not installed in `eclipse-temurin:25-jre-noble` (minimal JRE image).

**Verify:**
```bash
docker exec <container> which curl
# "not found" → curl is missing
```

**Fix:** Add curl to Dockerfile runtime stage:
```dockerfile
FROM eclipse-temurin:25-jre-noble
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
```

---

## "host.docker.internal: Name or service not known"

**Cause:** `host.docker.internal` is a Docker Desktop feature (Mac/Windows). On Linux, it doesn't resolve by default.

**Fix:** Use container names on a shared Docker network instead:
```yaml
# Wrong (Linux)
KC_DB_URL: jdbc:postgresql://host.docker.internal:5432/keycloak

# Correct
KC_DB_URL: jdbc:postgresql://local-postgres:5432/keycloak
```

**Prerequisite:** Both containers must be on the same Docker network (`db-network`).
