---
name: nginx-streaming-proxy
description: Configure nginx for streaming endpoints (SSE, MCP, WS).
---

# Nginx Reverse Proxy for Streaming Endpoints

## When to use
- Long-lived HTTP streams (SSE, streamable MCP, event streams) that stall, drop after ~60s, or deliver events in bursts
- WebSocket endpoints that fail behind a new nginx location
- Any symptom of "the stream connects but nothing flows" through a reverse proxy

## Defaults that break streaming (memorize)

| nginx default | What it does to a stream |
|---|---|
| `proxy_buffering on` | Buffers the upstream response; SSE events sit in the buffer instead of flushing to the client |
| `proxy_read_timeout 60s` | Kills the upstream connection after 60s of silence |
| `proxy_http_version 1.0` | Connection-close semantics; breaks chunked/long-lived streams |
| gzip (if enabled globally) | Can delay or re-chunk event streams |

## The fix — dedicated location block

Copy `templates/streaming-location.conf` and adapt the upstream. Essential lines:

```nginx
location /stream-or-sse-path/ {
    proxy_pass http://upstream;
    proxy_http_version 1.1;
    proxy_set_header Connection "";

    proxy_buffering off;          # critical: flush events immediately
    proxy_cache off;
    chunked_transfer_encoding on;
    proxy_read_timeout 1d;        # keep the stream alive
    proxy_send_timeout 1d;
    proxy_connect_timeout 10s;
    gzip off;
}
```

## WebSocket variant

Add these two headers (and long timeouts still help):
```nginx
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

## Verification

1. `sudo nginx -t && sudo systemctl reload nginx`
2. `curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' -N https://host/path`
   — a fast response means the endpoint is alive. HTTP 406 for a dummy token on an
   authenticated stream endpoint is a *correct rejection*, not a failure.
3. `sudo tail /var/log/nginx/error.log` — `upstream timed out (110) while reading
   response header` on the stream path = the 60s timeout default is still in effect.
4. WebSocket endpoint liveness: send an upgrade handshake and look for **101** —
   `curl -s -o /dev/null -w '%{http_code}\n' -H 'Connection: Upgrade' -H 'Upgrade: websocket' -H 'Sec-WebSocket-Version: 13' -H 'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==' http://host/ws-path`
   (curl may exit non-zero because the server closes the unauthenticated socket — the `101`
   line in the output is the signal, ignore the exit code).

## Every hop in the chain matters

When the app runs in Docker behind host nginx (typical: host nginx → container nginx → app),
**both** proxy hops need the streaming settings. Host-level `proxy_buffering off` is useless
if the container's own nginx still buffers the internal hop.

## Container nginx configs baked into images

Official images (e.g. penpot frontend) bake override files into the image; in-container
edits die on container recreate. Durable pattern:

1. Copy the baked file content to the compose project dir (e.g. `./nginx/<file>.conf`)
2. Add the streaming directives
3. Bind-mount over the baked path in docker-compose:
   `- ./nginx/<file>.conf:/etc/nginx/overrides/.../<file>.conf:ro`
4. `docker compose up -d <service>`, then verify the mount inside the container
   (`docker exec <c> grep -c proxy_buffering <path>` + `nginx -t`)

## Pitfalls

- Editing only the host config when the container hop also buffers → still broken. Check both.
- `proxy_read_timeout` values are per-hop; set them on every hop.
- Patching docker-compose with a shared volume pattern (e.g. `penpot_assets:/opt/data/assets`
  appearing in multiple services) — anchor the replacement to the *service block*, not the
  volume line alone, or the patch hits the wrong service.

## Related

- `penpot-mcp` — worked example: MCP stream behind two nginx hops (host + container)
