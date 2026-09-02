# Keycloak 26+ Pitfalls

> Encountered during Panomete Platform deployment (2026-07-23). All verified on Keycloak 26.7.0.

## 1. Deprecated Environment Variables

| Old (deprecated) | New | Version |
|---|---|---|
| `KC_PROXY=edge` | `KC_PROXY_HEADERS=xforwarded` | 26+ |
| `KEYCLOAK_ADMIN` | `KC_BOOTSTRAP_ADMIN_USERNAME` | 26+ |
| `KEYCLOAK_ADMIN_PASSWORD` | `KC_BOOTSTRAP_ADMIN_PASSWORD` | 26+ |

## 2. Bootstrap Admin is Always Temporary

`KC_BOOTSTRAP_ADMIN_USERNAME`/`KC_BOOTSTRAP_ADMIN_PASSWORD` always create a **temporary** admin. The Admin Console shows a warning banner. There is no way to make it permanent via env vars. ([GitHub #34768](https://github.com/keycloak/keycloak/issues/34768) — closed as "by design")

**Fix:** Create a permanent admin via Admin Console → Users → Create user → Set password (Temporary: OFF) → Assign `admin` role → Log in as new user → Delete temporary admin.

## 3. KC_CACHE=local Required for Single-Node

Without `KC_CACHE=local`, Keycloak tries to form a JGroups distributed cluster. On a single node, JOIN attempts timeout 10× (20+ seconds wasted per boot). Logs show:

```
WARN: JOIN(...) sent to ... timed out (after 2000 ms), on try N
```

**Fix:** Add `KC_CACHE: local` to compose environment.

## 4. HTTPS Required Error Behind Cloudflare

Keycloak returns `{"error":"invalid_request","error_description":"HTTPS required"}` when accessed through Nginx + Cloudflare.

**Root cause:** Cloudflare terminates TLS. Nginx receives HTTP. Keycloak's `sslRequired=external` rejects HTTP. Even with `KC_PROXY_HEADERS=xforwarded`, the realm's `sslRequired` setting takes precedence.

**Fix (two parts):**
1. In realm JSON: set `"sslRequired": "none"`
2. In Nginx: hardcode `proxy_set_header X-Forwarded-Proto https;` (not `$scheme`, which would be `http`)

## 5. Docker Bind Mount Creates Directory

When a Docker bind mount source path doesn't exist, Docker **creates a directory** at that path instead of failing. Keycloak then tries to import a directory as a realm JSON file and crashes:

```
ERROR: /opt/keycloak/data/import/panomete-realm.json (Is a directory)
```

**Fix:** Always create the file on the host BEFORE starting the container. Verify with `ls -la` — it should be `-rw-r--r--`, not `drwxr-xr-x`.

**Recovery:**
```bash
docker stop flowero-guard && docker rm flowero-guard
rm -rf /path/to/panomete-realm.json   # Remove the directory
# Create the actual file, then restart
```

## 6. Realm Import Failures

### Missing composite client roles
```
ERROR: Unable to find composite client role: view-profile
```

**Cause:** `default-roles-panomete` composite role references `account` client roles (`view-profile`, `manage-account`) that aren't defined in the realm JSON.

**Fix:** Remove client role references from the composite. Let Keycloak create default roles automatically:
```json
"composites": {
    "realm": ["user"]
    // Remove "client": {"account": ["view-profile", "manage-account"]}
}
```

### Missing client scopes
```
WARN: Referenced client scope 'address' doesn't exist. Ignoring
```

**Cause:** `optionalClientScopes` in client definitions reference scopes not defined in `clientScopes`.

**Fix:** Either define the scopes or remove them from `optionalClientScopes`.

## 7. Management Port 9000 (Separate from Main Port 8080)

Keycloak 26+ with Quarkus runs a **separate management interface** on port 9000. This is where health and metrics endpoints live.

| Endpoint | Port | URL |
|----------|:----:|-----|
| Main application | 8080 | `http://localhost:8080/realms/panomete` |
| Health | 9000 | `http://localhost:9000/health/ready` |
| Metrics | 9000 | `http://localhost:9000/metrics` |

**Pitfall 1:** Prometheus scrape target must use port 9000, NOT 8080:
```yaml
# ✅ Correct
- targets: ["flowero-guard:9000"]
# ❌ Wrong — returns 404
- targets: ["flowero-guard:8080"]
```

**Pitfall 2:** The Keycloak Docker image has NO tools (no curl, wget, which, or even bash builtins). Healthchecks must use TCP check:
```yaml
healthcheck:
  test: ["CMD-SHELL", "timeout 5 bash -c '</dev/tcp/localhost/8080' || exit 1"]
```

**Pitfall 3:** To enable metrics, add `KC_METRICS_ENABLED=true` to compose environment. Without it, `/metrics` returns 404.

**Pitfall 4:** To enable health endpoints, add `KC_HEALTH_ENABLED=true` to compose environment.

## 8. Proxy Configuration for Nginx + Cloudflare

The correct compose environment for Keycloak behind Nginx + Cloudflare Tunnel:

```yaml
environment:
  KC_HOSTNAME: auth.panomete.com
  KC_HTTP_ENABLED: "true"
  KC_PROXY_HEADERS: xforwarded   # Trust X-Forwarded-* from Nginx
  KC_CACHE: local                 # No distributed caching
  # Do NOT set KC_SSL_REQUIRED — let realm JSON handle it ("none")
```

And the Nginx config must hardcode HTTPS proto:
```nginx
proxy_set_header X-Forwarded-Proto https;  # Not $scheme
```
