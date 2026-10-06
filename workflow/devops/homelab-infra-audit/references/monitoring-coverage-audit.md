# Monitoring Coverage Audit (Uptime Kuma × Nginx / Cloudflare)

"How should I be monitoring?" is an audit question, not a guess. "Container
`Up (healthy)`" does NOT mean "monitored." Cross-reference the exposed public
surface against the live monitor list, then verify real HTTP codes so you don't
create monitors that false-alarm.

## 1. Enumerate the public surface (Nginx)

`sites-enabled` entries are symlinks; `grep -r` does NOT follow symlinks and
will silently miss most of them. Use the glob form (grep reads explicit
filenames through symlinks):

```bash
grep -HnE "server_name" /etc/nginx/sites-enabled/*
```

For the full ingress picture, also read the tunnel config:

```bash
grep -E "hostname:|service:" ~/.cloudflared/config.yml /etc/cloudflared/config.yml 2>/dev/null
```

## 2. Enumerate current monitors (Uptime Kuma)

`better-sqlite3` is NOT importable via `docker exec uptime-kuma node -e …`
(the bundled dep isn't on the require path — `require('better-sqlite3')` throws
`MODULE_NOT_FOUND`). Copy the DB out and read it on the host instead:

```bash
docker cp uptime-kuma:/app/data/kuma.db /tmp/kuma.db
python3 - << 'PY'
import sqlite3
c = sqlite3.connect('/tmp/kuma.db'); c.row_factory = sqlite3.Row
for r in c.execute("SELECT id,name,type,url,active FROM monitor ORDER BY id"):
    print(f"#{r['id']}\t{r['name']}\t{r['type']}\t{r['url']}\tactive={r['active']}")
PY
rm -f /tmp/kuma.db
```

## 3. Cross-reference → gaps, then verify codes

For each `server_name` with no matching monitor, `curl` it to learn the real
expected code BEFORE adding it (so you set "expected status" correctly and avoid
false DOWN/UP):

```bash
for d in a.panomete.com b.panomete.com …; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "https://$d/")
  echo "$code  https://$d/"
done
```

## Gotchas (false-positive / false-negative traps)

- **Rate-limited frontends → 429.** SearXNG with the limiter on returns `429` to
  a monitor's periodic probe even when healthy → permanent false DOWN. Fix: add
  the monitor's source IP to the limiter passlist, or monitor a non-rate-limited
  path.
- **`proxy_pass https://127.0.0.1:PORT` to a plain-HTTP backend → 502.** Nginx
  tries TLS against a backend that speaks HTTP → `502 Bad Gateway` even though
  the app is up. Diagnose: `curl http://127.0.0.1:PORT/` directly — if it answers
  (even `403`/`401`), the app is fine and the Nginx scheme is wrong. Fix the
  `proxy_pass` to `http://`.
- **Self-monitoring caveat.** Monitoring the Uptime Kuma status page itself
  (`status.panomete.com`) is pointless unless a SECOND watchdog exists — if
  Uptime Kuma is down it can't alert on itself.
- **Expected-code semantics.** `302` = login redirect (fine for
  Keycloak/Grafana/AdGuard); `401` = gateway demanding auth (fine); `403` from
  an S3 API root is normal (unsigned request). Prefer a real health path over
  root `/` where one exists: `/actuator/health`, `/-/healthy`, `/_up`,
  `/api/health`, `/ready`.

## Prioritization

Public-facing product services first (design/Penpot, sync/CouchDB LiveSync,
secrets manager, utility apps), then admin dashboards (Portainer, AdGuard), then
internal infra (databases via TCP-port monitors, Prometheus `/-/healthy`, Loki
`/ready`, Grafana `/api/health`).
