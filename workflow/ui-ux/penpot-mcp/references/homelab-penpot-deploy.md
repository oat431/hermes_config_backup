# Penpot deployment topology (this user's homelab)

Discovered 2026-08 — durable facts for operating Penpot MCP here.

## Access

- Host: `remote.panomete.com` (LAN `192.168.1.121`), SSH user `flowero`, key `~/.ssh/id_homelab`
- Penpot UI: `https://design.panomete.com` (self-hosted, Penpot 2.16, docker compose)
- Compose project dir: `/home/flowero/application/penpot/docker-compose.yaml`
- MCP stream endpoint: `/mcp/stream?userToken=<JWT>` — token key shown in UI at
  Settings → Integrations → MCP Server ("Beta", toggle, key has "No expiration date")

## Containers (all on `db-network`)

| Container | Image | Ports / role |
|---|---|---|
| penpot-frontend | penpotapp/frontend:2.16 | host `127.0.0.1:7009→8080` and `0.0.0.0:9001→8080`; its internal nginx routes `/mcp/*` to penpot-mcp |
| penpot-mcp | penpotapp/mcp:2.16 | stream HTTP on 4401, WS on 4402 (internal only) |
| penpot-backend / exporter / mailcatch | 2.16 | app backend |
| valkey | shared on db-network | session state |

## Proxy chain (both hops needed the streaming fix)

1. Host nginx `/etc/nginx/sites-available/design.conf` → `127.0.0.1:7009` (frontend).
   Fixed by adding a dedicated `location /mcp/` block: `proxy_buffering off`,
   `proxy_read_timeout 1d`, HTTP/1.1, `gzip off` (backup: `design.conf.bak.20260813`).
2. Frontend container's baked `/etc/nginx/overrides/server.d/mcp-locations.conf` →
   `penpot-mcp:4401` (stream/sse) and `:4402` (ws). Fixed durably by bind-mounting
   `./nginx/mcp-locations.conf` from the compose dir over the baked path (`:ro`),
   then `docker compose up -d penpot-frontend`.

## Verification commands that worked

```bash
# endpoint alive through the chain (406 = correct dummy-token rejection):
curl -s -o /dev/null -w '%{http_code}\n' -N 'https://design.panomete.com/mcp/stream?userToken=dummy'
# WS bridge endpoint accepts upgrade handshakes (101 = healthy; curl may report exit!=0
# because the server closes the unauthenticated socket — the 101 line is the signal):
docker exec penpot-penpot-frontend-1 curl -s -o /dev/null -w 'HTTP %{http_code}\n' \
  -H 'Connection: Upgrade' -H 'Upgrade: websocket' -H 'Sec-WebSocket-Version: 13' \
  -H 'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==' http://penpot-mcp:4402/
# mount took effect inside container:
docker exec penpot-penpot-frontend-1 grep -c proxy_buffering /etc/nginx/overrides/server.d/mcp-locations.conf
# smoking gun for the old bug (pre-fix log):
#   upstream timed out (110) while reading response header ... /mcp/stream?userToken=...
```

## PluginBridge handshake details (traced from /opt/penpot/mcp/index.js)

- The bridge WS (`/mcp/ws`, port 4402) reads the token from the query string:
  `url.searchParams.get("userToken")`. In multi-user mode, missing token → WARN
  `Connection attempt without userToken in multi-user mode - rejecting` + close(1008).
- The frontend supplies the token from **profile state** — so a tab loaded before the MCP
  key was enabled connects token-less and gets rejected. Remedy: Ctrl+F5 hard-refresh,
  then MCP → Connect here.
- `docker logs penpot-penpot-mcp-1` shows every Hermes session request with
  `userTokenFp=<first 8 chars of JWT payload>` — use it to verify the config token
  matches the Integrations page without pasting tokens.

## Gotcha

`docker compose config` output and the compose file both contain a shared
`penpot_assets:/opt/data/assets` volume line in TWO services (frontend and backend).
When patching the frontend volumes, anchor on the `penpot-frontend:` service block,
not on the volume line, or the patch matches twice.
