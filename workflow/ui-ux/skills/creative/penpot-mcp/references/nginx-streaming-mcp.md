# nginx streaming proxy — diagnosis & fixes (SSE / MCP streams)

Applies to ANY long-lived streaming endpoint behind nginx (Penpot MCP `/mcp/stream`, SSE event feeds, etc.).

## The three nginx defaults that kill streams

| Default | Effect on a stream |
|---|---|
| `proxy_buffering on` | nginx holds upstream responses in a buffer and won't flush events to the client until it fills or the connection closes → SSE events never arrive |
| `proxy_read_timeout 60s` | nginx kills the upstream connection after 60s of silence → stream dies after a minute |
| `proxy_http_version 1.0` | Wrong semantics for long-lived streams; chunked encoding / keep-alive breaks |

Smoking gun in `/var/log/nginx/error.log`:
```
upstream timed out (110: Connection timed out) while reading response header from upstream, ... request: "GET /mcp/stream?userToken=..."
```

## Required settings for a streaming location

```nginx
location /mcp/ws {
    # MUST come BEFORE the /mcp/ location — see the location-ordering pitfall below.
    proxy_pass http://127.0.0.1:7009;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header X-Forwarded-Host $host;
    proxy_read_timeout 1d;
    proxy_send_timeout 1d;
}

location /mcp/ {
    proxy_pass http://127.0.0.1:7009;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header Connection "";

    proxy_buffering off;          # critical: flush events immediately
    proxy_cache off;
    chunked_transfer_encoding on;
    proxy_read_timeout 1d;        # keep the stream alive
    proxy_send_timeout 1d;
    proxy_connect_timeout 10s;
    gzip off;                     # don't compress the event stream
}
```

### CRITICAL pitfall — `Connection ""` in the `/mcp/` block breaks the `/mcp/ws` WebSocket

nginx location matching is by longest PREFIX — `/mcp/ws` matches `/mcp/` too. If the
streaming block sets `proxy_set_header Connection ""` (correct for the HTTP stream), it
ALSO rewrites the `Connection: upgrade` header on the WebSocket bridge, killing the
handshake silently. Symptom: user clicks "Connect here", Penpot UI looks fine, but the
MCP server never logs `New WebSocket connection established (token provided)` and every
tool call fails with `No plugin instance connected for user token`.

**Fix: dedicated `/mcp/ws` location placed BEFORE `/mcp/`** that passes
`Upgrade $http_upgrade` + `Connection "upgrade"`. Verified: internal handshake returns
`HTTP 101` (see verification below).

Note the `$host` / `$remote_addr` / `$http_upgrade` escaping when writing via `sudo tee ... << 'EOF'` over SSH — inside single-quoted heredocs nginx variables like `$host` must stay literal (do NOT escape them), but inside double-quoted heredocs you MUST escape them as `\$host` or the local shell expands them.

## Penpot-specific: two nginx hops, both need fixing

1. **Host nginx** — `/etc/nginx/sites-available/<site>.conf`, proxies to `127.0.0.1:7009` (penpot-frontend). Add the streaming location above.
2. **Container nginx** — the official `penpotapp/frontend` image bakes `/mcp/` routes into `/etc/nginx/overrides/server.d/mcp-locations.conf` (checked in Penpot 2.16):
   - `/mcp/ws` → `penpot-mcp:4402` (WebSocket, needs `Upgrade` headers)
   - `/mcp/stream` → `penpot-mcp:4401/mcp`
   - `/mcp/sse` → `penpot-mcp:4401/sse`
   Its own globals are `proxy_read_timeout 300s` — too short for session-long streams.

## Durable fix: shadow baked-in container config with a bind mount

Editing inside the container dies on `docker compose up -d` (recreate). Instead:

1. Copy the baked-in file to the host compose dir and add streaming settings:
   `/home/<user>/application/penpot/nginx/mcp-locations.conf`
2. Add a bind mount in `docker-compose.yaml` under the frontend service:
   ```yaml
   volumes:
     - penpot_assets:/opt/data/assets
     - ./nginx/mcp-locations.conf:/etc/nginx/overrides/server.d/mcp-locations.conf:ro
   ```
3. `docker compose config --quiet` (validate) then `docker compose up -d penpot-frontend`
4. Verify inside: `docker exec <frontend> sh -c 'grep -c proxy_buffering /etc/nginx/overrides/server.d/mcp-locations.conf; nginx -t'`

## Fixed container mcp-locations.conf (Penpot 2.16 baseline + streaming)

```nginx
location /mcp/ws {
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_pass http://penpot-mcp:4402;
    proxy_http_version 1.1;
    proxy_buffering off;
    proxy_read_timeout 1d;
    proxy_send_timeout 1d;
}

location /mcp/stream {
    proxy_pass http://penpot-mcp:4401/mcp;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_buffering off;
    proxy_cache off;
    chunked_transfer_encoding on;
    proxy_read_timeout 1d;
    proxy_send_timeout 1d;
    gzip off;
}

location /mcp/sse {
    proxy_pass http://penpot-mcp:4401/sse;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_buffering off;
    proxy_cache off;
    chunked_transfer_encoding on;
    proxy_read_timeout 1d;
    proxy_send_timeout 1d;
    gzip off;
}
```

## Verification sequence

```bash
# 1. host config syntax + reload
sudo nginx -t && sudo systemctl reload nginx

# 2. endpoint responds through full chain (406 = correct rejection of bad token, not a timeout)
curl -s -o /dev/null -w 'HTTP %{http_code} in %{time_total}s\n' \
  https://<host>/mcp/stream?userToken=dummy --max-time 15 -N

# 2b. WebSocket handshake — test from INSIDE the server (not through the public URL):
#     101 = upgrade works end-to-end
curl -s -o /dev/null -w 'HTTP %{http_code}\n' \
  'http://127.0.0.1/mcp/ws?userToken=dummytest' \
  -H 'Host: <host>' -H 'Connection: Upgrade' -H 'Upgrade: websocket' \
  -H 'Sec-WebSocket-Version: 13' -H 'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ=='

# 3. confirm no NEW 'upstream timed out' entries (note timestamps vs server `date`)
sudo tail -5 /var/log/nginx/error.log
```

External `curl` against the public HTTPS URL returns **HTTP 426** for the WS route — that is a curl artifact (no WebSocket-over-HTTP/2 support), NOT a server fault. Browsers negotiate WS-over-H2 fine. Always verify the WS hop from inside the server as in 2b.

## Gotchas

- Compose patch via python heredoc: a `volumes:` pattern may match multiple services — anchor the match on the service name block (e.g. include `penpot-frontend:` header in `old`), assert `s.count(old) == 1`.
- Back up before editing: `sudo cp file file.bak.$(date +%Y%m%d)` — host nginx AND compose yaml.
- `docker compose config | grep` for verification can silently return nothing on multi-line YAML; use `sed -n '/service:/,/next-service:/p'` instead.
