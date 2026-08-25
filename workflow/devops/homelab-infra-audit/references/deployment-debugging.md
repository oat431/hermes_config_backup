# Live Deployment Debugging — Reference

Session transcripts and patterns from debugging real homelab deployments after
documents were approved and the user started deploying by hand.

---

## Case 1: Keycloak 502 Bad Gateway (Panomete Platform, 2026-07-23)

### Symptom

User deployed Keycloak via `docker run` with volume mount for realm import, set
up Nginx reverse proxy, then `https://auth.panomete.com` returned 502 Bad Gateway.

### Diagnosis chain (ran via single SSH heredoc)

1. **Container running?** → Yes, but "Up 15 seconds" (recent restart)
2. **Restart count?** → **7** — crash loop confirmed
3. **Port 8001 listening?** → Yes, `127.0.0.1:8001` was bound
4. **Local health?** → No response (container never finished starting)
5. **Nginx config?** → Present and correct (`auth.conf` → `127.0.0.1:8001`)
6. **Nginx test?** → Syntax OK
7. **Logs?** → The smoking gun:
   ```
   ERROR: /opt/keycloak/data/import/panomete-realm.json (Is a directory)
   ERROR: Failed to run import
   ```

### Root cause: Docker volume directory-creation trap

The user mounted:
```
/home/flowero/platform/keycloak/flowero-guard/panomete-realm.json
  → /opt/keycloak/data/import/panomete-realm.json
```

But `panomete-realm.json` **didn't exist on the host** when the container
started. Docker's behavior: it creates a **directory** at the missing path
rather than failing. Keycloak then tried to import a directory as a JSON file
and crashed. Restart policy (`unless-stopped`) kept restarting → 7 crashes.

**Confirmed via:**
```bash
ls -la /home/flowero/platform/keycloak/flowero-guard/panomete-realm.json
# drwxr-xr-x ... panomete-realm.json   ← "d" = directory!
```

### Fix steps given to user (manual)

1. Stop the container: `docker stop flowero-guard && docker rm flowero-guard`
2. Remove the auto-created directory: `rm -rf /home/flowero/platform/.../panomete-realm.json`
3. Create the actual JSON file at that path (use `templates/realm-template.json`)
4. Recreate the container: `docker compose up -d flowero-guard` (or `docker run`)
5. Wait 15-30s for Liquibase + realm import
6. Verify: `curl -sf http://localhost:8001/health/ready`

### Key diagnostic commands

```bash
# Check container state + restart count (single most useful command)
docker inspect flowero-guard --format '{{.State.Status}} | Restarts: {{.RestartCount}}'

# Check what Docker actually mounted (file vs directory)
docker exec flowero-guard ls -la /opt/keycloak/data/import/

# Find the realm file on host and check if it's a dir
ls -la /home/flowero/platform/keycloak/flowero-guard/
```

### Lesson encoded in SKILL.md

The volume directory-creation trap is now Phase 7's headline pitfall. The
`templates/realm-template.json` exists so the file can be created on the host
BEFORE the container starts. The `scripts/502-debug-ladder.sh` automates the
full diagnostic chain.

---

## Case 2: Deployment sequencing (avoiding rework)

### Scenario

User proposed deployment order: Keycloak → Gateway → Discovery.

### Analysis

Gateway needs Eureka for `lb://` route resolution. Deploying Gateway before
Discovery forces either:
- Hardcoded routes (`http://service:port`) → later rewrite to `lb://service`
- Eureka disabled → Gateway can't route anything

### Resolution

Swap to: Keycloak → Discovery → Gateway (least-dependent first).

This is a general principle: **deploy in dependency order.** The most-dependent
service goes last so it can be wired correctly in one pass.

### When to raise this

Whenever the user proposes a deployment order, check: does any service depend
on a service that deploys later? If yes, suggest the swap with the rework
argument. But if the user insists, proceed with their order — they may have
reasons (e.g., wanting to learn the gateway internals before building
discovery).

---

## Case 3: Keycloak config file location (nginx)

When the user creates Nginx configs by hand, they may name the file
differently than expected. In this session, the config for `auth.panomete.com`
was saved as `/etc/nginx/sites-available/auth.conf` (not
`auth.panomete.com`), then symlinked as `auth.conf` in sites-enabled.

**Lesson:** Don't assume the filename matches the domain. When debugging,
search for the domain in ALL site configs:
```bash
grep -r "server_name" /etc/nginx/sites-available/
```
The 502 debug ladder script now checks multiple naming patterns.

---

## Case 4: Keycloak JGroups clustering timeout (same session, 2026-07-23)

### Symptom

After fixing the realm file (Case 1), Keycloak container showed "Up 43 seconds"
but `curl http://localhost:8001/health/ready` returned nothing. Logs showed
repeated warnings:

```
WARN: f2d7a7b058aa-20949: JOIN(...) sent to f2d7a7b058aa-25393 timed out (after 2000 ms)
```

117 JOIN timeout messages accumulated across restarts.

### Root cause

Keycloak uses JGroups/Infinispan for distributed caching. On startup it tries
to discover and JOIN other cluster members via JDBC_PING. On a single-node
homelab, there ARE no other members — so it times out 10 times (10×2s = 20s
wasted) before giving up and becoming a singleton. Each restart repeats this.

Additionally, the logs showed:
```
WARN: Hostname v1 options [proxy] are still in use
WARN: Likely misconfiguration detected. With HTTPS not enabled, `proxy-headers` unset
```

`KC_PROXY=edge` is deprecated in Keycloak 25+. The correct variable is
`KC_PROXY_HEADERS=xforwarded`.

### Fix

Add two environment variables to the compose file:

```yaml
KC_PROXY_HEADERS: xforwarded   # replaces deprecated KC_PROXY=edge
KC_CACHE: local                 # disables JGroups, single-node only
```

Then `docker compose up -d --force-recreate flowero-guard`.

### Result

Startup time dropped from 60s+ to ~15s. No more JGroups timeout spam in logs.

### Lesson

Always add `KC_CACHE: local` for single-node Keycloak deployments. The default
(distributed caching via JGroups) is designed for clustered Kubernetes
environments, not homelab Docker Compose setups.

---

## General debugging principles

1. **RestartCount is the crash-loop signal.** `docker inspect <name> --format
   '{{.RestartCount}}'` — anything above 3 with `unless-stopped` policy means
   the container is crash-looping, not just slow to start.

2. **Logs reveal the real error.** Always read the last 30 lines of container
   logs before guessing. The error message is usually explicit ("Is a directory",
   "connection refused", "authentication failed").

3. **Volume mounts need files to exist on the host first.** Docker creates
   directories for missing bind-mount paths. This is the most common cause of
   crash loops when mounting config files (realm JSON, application.yml).

4. **Nginx 502 = upstream not responding.** If the Nginx config is valid
   (`nginx -t` passes) and the domain routes correctly, the 502 is always the
   backend service — not Nginx. Focus debugging on the container.

5. **One batched SSH call, not fifteen.** Run the entire diagnostic chain in a
   single `ssh host 'bash -s' << 'EOF'` heredoc. See `scripts/502-debug-ladder.sh`.

---

## Case 5: Keycloak "HTTPS required" 403 on external access (same session, 2026-07-23)

### Symptom

After fixing realm file and JGroups issues, `https://auth.panomete.com` returned:
```json
{"error":"invalid_request","error_description":"HTTPS required"}
```

Internal access worked. OIDC discovery returned correct issuer when hit directly.
But external access through Cloudflare → Nginx → Keycloak returned 403.

### Diagnosis

```bash
docker exec flowero-guard env | grep KC_PROXY KC_SSL KC_HOSTNAME
# KC_PROXY_HEADERS=xforwarded ✅
# KC_SSL_REQUIRED=none ✅
# KC_HOSTNAME=auth.panomete.com ✅

# But the realm JSON had:
# "sslRequired": "external"
```

### Root cause

Two issues:
1. Realm JSON `"sslRequired": "external"` **overrides** the `KC_SSL_REQUIRED` env var
2. Nginx used `proxy_set_header X-Forwarded-Proto $scheme;` — but `$scheme` is `http` behind Cloudflare Tunnel (CF terminates TLS, sends HTTP to Nginx)

### Fix

1. **Nginx:** `X-Forwarded-Proto $scheme` → `X-Forwarded-Proto https` (hardcode)
2. **Realm JSON:** `"sslRequired": "external"` → `"sslRequired": "none"`

Both applied → all external endpoints worked.

### Lesson

`KC_PROXY_HEADERS: xforwarded` tells Keycloak to TRUST the headers, but Nginx
must SEND the correct values. `$scheme` is `http` behind Cloudflare Tunnel.
Always hardcode `X-Forwarded-Proto https` for services behind Cloudflare.

---

## Case 6: Realm JSON composite role crash (same session, 2026-07-23)

### Symptom

Keycloak crash-looped: `Unable to find composite client role: view-profile`

### Root cause

Composite role referenced client roles not defined in the JSON:
```json
"composites": {"client": {"account": ["view-profile", "manage-account"]}}
```
But `account` client didn't define those roles → crash on import.

### Fix

Remove client role references from composite. Drop DB + re-import with fixed JSON.

### Lesson

Either define client roles explicitly in `clients`, or don't reference them in
composites. Safest: omit `default-roles-panomete` entirely — Keycloak creates
it automatically with correct composites.

---

## Case 7: SSH heredoc escaping failures (same session, 2026-07-23)

### Symptom

`ssh host 'python3 -c "..."'` with embedded JSON/quotes broke bash escaping.

### Fix

Write script to file first, then execute:
```bash
ssh host 'cat > /tmp/script.py << '"'"'PYEOF'"'"'
import json
# ... script content ...
PYEOF'
ssh host 'python3 /tmp/script.py'
```

Or scp a local script: `scp script.py host:/tmp/ && ssh host 'python3 /tmp/script.py'`

### Lesson

Don't fight bash escaping for complex scripts over SSH. Write to file first,
then execute. Two commands, zero escaping headaches.

---

## Case 8: Docker Compose YAML append breaks structure (same session, 2026-07-23)

### Symptom

`cat >> docker-compose.yml` nested new service under `networks:` instead of
`services:`. Docker Compose rejected it.

### Fix

Rewrite entire file with Python yaml.dump over SSH:
```python
import yaml
compose = {"services": {...}, "networks": {...}}
with open("docker-compose.platform.yml", "w") as f:
    yaml.dump(compose, f, default_flow_style=False, sort_keys=False)
```

### Lesson

Never `cat >>` a YAML file with multiple top-level keys. Always rewrite the
entire file. Python `yaml.dump` over SSH is the reliable pattern.
