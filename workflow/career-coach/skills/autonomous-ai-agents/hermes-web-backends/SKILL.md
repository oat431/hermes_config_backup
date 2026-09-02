---
name: hermes-web-backends
description: "Fix or configure Hermes web_search/web_extract backends."
version: 1.0.0
author: OraMesLita (curator)
license: MIT
metadata:
  hermes:
    tags: [hermes, web, search, extract, backend, searxng, firecrawl, tavily, exa, config]
    related_skills: [hermes-agent, mcp-server-patterns]
---

# Hermes Web Search & Extract Backends

Configuring and troubleshooting which provider powers `web_search` / `web_extract` in Hermes. Providers are plugins under `$HERMES_HOME/hermes-agent/plugins/web/<name>/` (built-in, `kind: backend`), selected via `web.*` config keys. Reference: `references/web-provider-docs.md` (verbatim docs excerpt).

## Provider capability matrix

| Provider | Env var (in $HERMES_HOME/.env) | Search | Extract | Key needed? |
|---|---|---|---|---|
| firecrawl (default) | FIRECRAWL_API_KEY (or FIRECRAWL_API_URL self-hosted) | ✔ | ✔ | yes (or self-host) |
| searxng | SEARXNG_URL | ✔ | — | no (self-hosted) |
| parallel | PARALLEL_API_KEY | ✔ | ✔ | yes |
| tavily | TAVILY_API_KEY | ✔ | ✔ | yes (free tier: app.tavily.com) |
| exa | EXA_API_KEY | ✔ | ✔ | yes (free tier: exa.ai) |
| ddgs | (pip install ddgs) | ✔ | — | no |
| brave-free | — | ✔ | — | no |

**Hard fact: there is NO keyless extract backend.** Extract always needs firecrawl/tavily/exa/parallel (or self-hosted Firecrawl). Search can be free via searxng/ddgs/brave-free.

## Config keys & resolution

```yaml
web:
  backend: searxng            # fallback: firecrawl | searxng | parallel | tavily | exa | ddgs | brave-free
  search_backend: searxng     # optional per-capability override (mix free search + paid extract)
  extract_backend: firecrawl  # optional per-capability override
  extract_char_limit: 15000
```

- Explicit `web.search_backend` / `web.extract_backend` win for their capability.
- If `web.backend` is unset → auto-detect from keys: SEARXNG_URL → searxng; EXA_API_KEY → exa; TAVILY_API_KEY → tavily; PARALLEL_API_KEY → parallel; else firecrawl.
- Registry fallback order (filtered by capability): firecrawl → parallel → tavily → exa → searxng → brave-free → ddgs.

## Fix recipe: "ddgs is a search-only backend and cannot extract"

Symptom: `web_extract` errors with `Set web.extract_backend to firecrawl, tavily, exa, or parallel` (because `web.backend: ddgs` is search-only).

1. **Search** — point at the user's searxng (free, works live):
   ```bash
   H="$HERMES_HOME"
   printf '\nSEARXNG_URL=http://<instance-ip:port>\n' >> "$H/.env"
   hermes config set web.backend searxng
   ```
2. **Extract** — needs a keyed provider. User signs up (free tiers: Tavily 1k credits/mo, Firecrawl 500/mo, Exa), then:
   ```bash
   printf '\nTAVILY_API_KEY=<key>\n' >> "$H/.env"
   hermes config set web.extract_backend tavily
   ```
3. **Verify**: call `web_search` — results mean provider resolution worked.

**`web.*` config changes take effect LIVE (per-call registry resolution) — no session reset needed** (verified 2026-08-06). This differs from toolset changes, which need `/reset`.

## Pitfalls

- **$HOME trap**: `~/.hermes` may NOT be the real home. Always use `$HERMES_HOME` (on Panomete's box: `C:\Users\Admin\AppData\Local\hermes`; `~/.hermes` does not exist). `hermes config get web` reads the right file regardless.
- Use `hermes config set KEY VAL` — never hand-edit config.yaml.
- `.env` vars are read via config-aware lookup (os.environ first, then `$HERMES_HOME/.env`) so gateway sessions/delegate children see them too.
- The searxng **MCP** server config (config.yaml → `mcp.servers.searxng.env.SEARXNG_URL`) is SEPARATE from the native web backend — fixing one does not fix the other. MCP searxng's `web_url_read` CAN extract, so it's the workaround while native extract is unconfigured.
- Never print `.env` values; list key names only: `grep -oE '^[A-Z_0-9]+=' "$H/.env"`.
- Docs: https://hermes-agent.nousresearch.com/docs/user-guide/configuration → "Web Search Backends". If `web_extract` is broken, curl the docs page and strip HTML with python (`re.sub(r'<[^>]+>', ' ', ...)`) — avoids the broken extract path entirely.
- Self-hosted Firecrawl: set FIRECRAWL_API_URL, key becomes optional (server-side `USE_DB_AUTHENTICATION`). Needs Docker — check daemon state first (Panomete's Docker was DOWN at 2026-08-05).
- Provider plugins only advertise capabilities they implement (`supports_search` / `supports_extract`); registry routes each call to the right provider.

## Signup links

- Tavily: https://app.tavily.com/home · Exa: https://exa.ai · Firecrawl: https://firecrawl.dev · Parallel: https://parallel.ai
