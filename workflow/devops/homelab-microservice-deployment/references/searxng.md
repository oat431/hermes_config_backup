# SearXNG — Homelab Configuration

> Verified on SearXNG latest (Python 3.14), Docker 29.6.2, Panomete homelab.

## Container Details

| Item | Value |
|------|-------|
| Image | `docker.io/searxng/searxng:latest` |
| Port | `127.0.0.1:7004` |
| Config dir | `~/application/searxng/core-config/` (mounted as `/etc/searxng/:Z`) |
| Cache volume | `searxng_core-data` → `/var/cache/searxng/` |
| Internal UID | 977 (searxng user) |

## Valkey/Redis Connection

SearXNG uses Valkey (Redis-compatible) for query caching and rate limiting.

### settings.yml (correct — uses `valkey.url`)

```yaml
use_default_settings: true

server:
  secret_key: "..."
  image_proxy: true

valkey:
  url: redis://:PASSWORD@valkey:6379/0
```

### Pitfalls

1. **`redis.url` is DEPRECATED** — SearXNG logs `DeprecationWarning: setting redis.url is deprecated, use valkey.url`. Use the `valkey:` key in settings.yml.

2. **`SEARXNG_REDIS_URL` env var OVERRIDES settings.yml** — If both are set, the env var wins. This can cause the deprecation warning if the env var uses the old `redis://` scheme internally. Pick ONE approach:
   - **Option A:** Set in `settings.yml` only (recommended — no env var needed)
   - **Option B:** Set `SEARXNG_REDIS_URL` env var only (don't also set in settings.yml)

3. **Password in URL format:** `redis://:PASSWORD@host:6379/0` (note the colon before password, no username).

4. **File permissions:** `settings.yml` is owned by UID 977 (container internal user). Host user `flowero` (UID 1000) cannot write directly. Use:
   ```bash
   sudo tee ~/application/searxng/core-config/settings.yml > /dev/null << 'EOF'
   ...content...
   EOF
   ```

## Rate Limiter — keep it OFF on this instance (critical)

**Current state: `limiter: false`.** This is a PRIVATE instance (Tailscale + Cloudflare tunnel + `noindex`), and SearXNG's bot-detection limiter — built for public instances — silently breaks AI/API clients here:

- Its checks (`http_user_agent`, `http_accept`, `http_sec_fetch`, …) block non-browser clients outright: curl / Python / MCP tools get `429 Too Many Requests`.
- It enforces a hardcoded **API_WINDOW limit: 4 requests/hour** for any `format != html` request — every AI/MCP call is an API call.
- It resolves the **true client IP through trusted proxy chains** (Cloudflare → cloudflared → Nginx), so public visitors can never match a passlist. A passlist cannot whitelist "the internet" — the old limiter+passlist design could never work for the public URL.

### Diagnosing "SearXNG refuses to respond" (429s)

1. Test the SAME request on all three paths: direct `http://127.0.0.1:7004`, via Nginx (`-H "Host: search.panomete.com" http://127.0.0.1:80/`), and the public URL.
2. Vary the User-Agent: browser (Chrome string), `curl` default, `python-urllib` — each with and without `format=json`. **Browser-UA testing hides the bug**; always test with the exact client a real consumer uses.
3. **Limiter block messages log at DEBUG level** — invisible in `docker logs`; only `PASS … matched PASSLIST` shows (WARNING level). No block logs ≠ nothing was blocked.
4. To see the real proxy chain, add a temporary Nginx location echoing `$remote_addr` / `$http_x_forwarded_for`, request it, then remove it.
5. Definitive MCP-path test: drive the MCP server over raw stdio JSON-RPC — spawn `node <npx-cache>/mcp-searxng/dist/cli.js` with `SEARXNG_URL` set; send `initialize` → `notifications/initialized` → `tools/call` (`searxng_web_search`); read the newline-delimited JSON responses. Distinguishes "server broken" from "client path blocked".

### settings.yml (current working state)

```yaml
server:
  limiter: false          # private instance — see above
  method: "GET"           # GET is better for API/MCP usage

real_ip:
  x_for: 1               # kept for logging fidelity (real client IPs)

search:
  formats:
    - html
    - json                # Required for MCP / API usage
```

### limiter.toml — only if the limiter is ever re-enabled

Kept at `core-config/limiter.toml` (inert while `limiter: false`). The schema is STRICT — only keys from the built-in schema are allowed. Invalid keys cause `TypeError: schema of /etc/searxng/limiter.toml is invalid!` and the container crashes.

**Valid keys only:**

```toml
[botdetection]

trusted_proxies = [
  "127.0.0.0/8",
  "::1",
  "172.16.0.0/12",
  "172.20.0.0/16",
]

[botdetection.ip_limit]

filter_link_local = false
link_token = true

[botdetection.ip_lists]

pass_ip = [
  "127.0.0.0/8",
  "10.0.0.0/8",
  "172.16.0.0/12",
  "192.168.0.0/16",
  "100.64.0.0/10",      # Tailscale CGNAT range
  "::1",
  "fd00::/8",
]

block_ip = []

pass_searxng_org = false
```

### limiter.toml Pitfalls

1. **Schema validation is strict** — the validator checks every key against the built-in `searx/limiter.toml` schema. Unknown keys cause startup crash. Do NOT add custom keys like `filter_link_token` or `pass` — use `filter_link_local` and `pass_ip`.

2. **`link_token = true`** — enables anti-bot token method. Works for browser access but may cause issues for pure API/MCP callers that don't follow HTML. Set to `false` if MCP gets unexpected 403s.

3. **`pass_ip` bypasses all rate limiting** — internal Docker IPs should be in the passlist so Nginx-proxied requests aren't throttled. The Docker gateway IP (e.g., `172.20.0.1`) matches `172.16.0.0/12`. Include `100.64.0.0/10` (Tailscale CGNAT range) so direct Tailscale access from the host machine isn't throttled either — Docker may pass the real Tailscale IP instead of NAT-ing to the gateway.

4. **Container must be recreated** (`docker compose down && up -d`) after changing `limiter.toml` — restart alone doesn't pick up the new file.

### Upstream Engine Suspensions

Even with the limiter, upstream engines will suspend after too many requests:

| Error | Engine | Suspension | Fix |
|-------|--------|------------|-----|
| `CAPTCHA` | Startpage | 3600s (1 hour) | Disable Startpage, use alternatives |
| `HTTP error 403` | Wikidata | 180s | None — wait |
| `HTTP error 429` | Various | 180s | Spread load across engines |

To reduce upstream rate limits:
- Enable multiple engines (bing, google, mojeek, yandex)
- Disable any engine that starts CAPTCHA'ing from your IP (startpage, brave, duckduckgo so far)
- Add delay between MCP queries if the tool supports it

## Compose File (consolidated — shared valkey)

```yaml
name: searxng

services:
  core:
    container_name: searxng-core
    image: docker.io/searxng/searxng:${SEARXNG_VERSION:-latest}
    restart: always
    ports:
      - ${SEARXNG_HOST:+${SEARXNG_HOST}:}${SEARXNG_PORT:-8080}:${SEARXNG_PORT:-8080}
    env_file: ./.env
    volumes:
      - ./core-config/:/etc/searxng/:Z
      - core-data:/var/cache/searxng/
    networks:
      - db-network

volumes:
  core-data:

networks:
  db-network:
    external: true
```

## .env

```
SEARXNG_VERSION=latest
SEARXNG_HOST=0.0.0.0    # 0.0.0.0 for Tailscale access, 127.0.0.1 for localhost-only
SEARXNG_PORT=7004
VALKEY_PASSWORD=<from platform .env>
```

**When to use `0.0.0.0`:** When MCP or other tools on the Tailscale network need direct access (bypassing Nginx/Cloudflare). UFW blocks public access by default — only Tailscale peers can reach it.

**When to keep `127.0.0.1`:** When all access goes through Nginx reverse proxy and no direct Tailscale access is needed.

## Engine Management

### Enable/Disable Engines

Override engines in `settings.yml` using the `engines:` key. With `use_default_settings: true`, only specify engines you want to change:

```yaml
use_default_settings: true

engines:
  # Enable a disabled engine
  - name: bing
    disabled: false

  # Enable an inactive engine
  - name: google
    inactive: false

  # Disable a problematic engine
  - name: startpage
    disabled: true
```

### `disabled` vs `inactive`

| Flag | Meaning | Effect |
|------|---------|--------|
| `disabled: true` | Opt-in engine, off by default | Not used unless user enables in UI |
| `inactive: true` | Engine has issues, marked broken | Not used, shown as "inactive" in UI |
| `disabled: false` | Enable a disabled engine | Engine participates in searches |
| `inactive: false` | Re-activate an inactive engine | Engine participates in searches |

### Recommended Engines for Load Spreading

For a private instance used by MCP/API, enable 5+ engines to distribute load:

| Engine | Default | Recommendation | Notes |
|--------|---------|----------------|-------|
| DuckDuckGo | ✅ active | **DISABLED** | CAPTCHAs on every request from this IP — pure latency; re-test before re-enabling |
| Brave | ✅ active | **DISABLED** | 429s after ~3 rapid MCP calls |
| Qwant | ✅ active | Keep | European engine |
| Google CSE | ✅ active | Keep | Limited results vs full Google |
| Google | ❌ inactive | Enable (`inactive: false`) | Full Google results |
| Bing | ❌ disabled | Enable (`disabled: false`) | Good backup |
| Mojeek | ❌ disabled | Enable (`disabled: false`) | Independent, no CAPTCHA |
| Yandex | ❌ disabled | Enable | Good for non-English |
| Startpage | ✅ active | **DISABLE** | Aggressive CAPTCHAs, 1hr suspension |

**Engine sets are not permanent.** Residential/datacenter IPs get CAPTCHA'd or 429'd on different engines over time (Startpage, Brave, and DuckDuckGo all ended up disabled this way). When searches degrade, check `unresponsive_engines` in the JSON response and disable whatever is failing; current working set: bing + google (cse) + mojeek + yandex.

### Verify Engines Working

```bash
curl -s "http://127.0.0.1:7004/search?q=hello+world&format=json" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
engines = set()
for r in d.get('results', []):
    engines.update(r.get('engines', []))
    engines.add(r.get('engine', ''))
print('Results:', len(d.get('results', [])))
print('Engines:', sorted(engines))
"
```

## MCP Integration (Critical)

When SearXNG is used as an MCP backend (e.g., `mcp-searxng` npm package), the MCP tool connects from the **host machine** (Windows), not from the Docker network. This creates a routing problem:

### Routing rule

Run MCP against the **Tailscale URL**, not the public URL:

```
MCP (Windows) ── Tailscale ──► 100.73.143.25:7004 ──► SearXNG
```

All Hermes profiles set `SEARXNG_URL: http://100.73.143.25:7004`. This path skips Cloudflare entirely (faster, fewer edge hiccups) — and while the limiter was enabled it was the ONLY path that worked: public-URL requests resolved to real public IPs through the trusted proxy chain, and no passlist can cover those.

### The Fix (both steps required)

1. **Bind SearXNG to `0.0.0.0`** (safe behind UFW + Tailscale):
   ```env
   # .env
   SEARXNG_HOST=0.0.0.0
   ```
   UFW blocks public access to 7004 by default. Tailscale traffic bypasses UFW.

2. **Point MCP at the Tailscale IP**:
   ```
   SEARXNG_URL=http://100.73.143.25:7004
   ```
   Get the server's Tailscale IP: `tailscale status | grep <hostname>`

3. **Configure the MCP server** (profile `config.yaml`):
   ```yaml
   mcp_servers:
     searxng:
       command: npx
       args: [-y, mcp-searxng]
       env:
         SEARXNG_URL: http://100.73.143.25:7004
   ```

### Why This Works

Tailscale traffic reaches the container without a Cloudflare hop, from IPs the passlist could cover (Tailscale CGNAT / docker gateway). With the limiter now disabled the public URL works too — Tailscale stays primary because it is faster and independent of Cloudflare.

### Brave 429 Issue

Brave search engine also rate-limits aggressively (429 after ~3 rapid MCP calls). If Brave is consistently hitting 429, disable it alongside Startpage:

```yaml
engines:
  - name: brave
    disabled: true
  - name: brave.images
    disabled: true
  - name: brave.news
    disabled: true
  - name: brave.videos
    disabled: true
```

Keep: Bing, Google (cse), Mojeek, Yandex — verify each with a live search. DuckDuckGo later joined Brave/Startpage on the disabled list (per-IP CAPTCHAs).

## Common Log Errors (not our problem)

| Error | Cause | Action |
|-------|-------|--------|
| `wikidata: engine init was not successful` (403) | Wikidata API rate limit | None — external API issue |
| `ahmia: can't register engine` | Tor engine, needs Tor | None — can disable in settings |
| `torch: can't register engine` | Tor engine, needs Tor | None — can disable in settings |
| `X-Forwarded-For nor X-Real-IP header is set` | No reverse proxy | Expected when hitting directly; goes away with Nginx |
| `PASS 172.20.0.1/32: matched PASSLIST` | Limiter working correctly | Info — internal IP bypassed as expected |

## Verification Checklist

After deploying or modifying:

- [ ] `docker ps` shows container on `db-network`
- [ ] `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:7004/` → 200
- [ ] `docker logs searxng-core 2>&1 | grep -i deprecat` → empty (no deprecation warnings)
- [ ] `docker logs searxng-core 2>&1 | grep -i "refused\|connect"` → no connection errors
- [ ] `curl -s "http://127.0.0.1:7004/search?q=test&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results',[])),'results')"` → returns results (JSON format works for MCP)
