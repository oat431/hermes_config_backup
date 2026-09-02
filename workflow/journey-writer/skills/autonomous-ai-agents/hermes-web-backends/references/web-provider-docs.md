# Hermes Docs — "Web Search Backends" (verbatim excerpt)

Source: https://hermes-agent.nousresearch.com/docs/user-guide/configuration (fetched 2026-08-06; docs page downloaded via curl + HTML-stripped with python because web_extract was down at the time).

> The web_search and web_extract tools support five backend providers. Configure the backend in config.yaml or via `hermes tools`:
>
> ```yaml
> web:
>   backend: firecrawl        # firecrawl | searxng | parallel | tavily | exa
>   # Or use per-capability keys to mix providers (e.g. free search + paid extract):
>   search_backend: "searxng"
>   extract_backend: "firecrawl"
> ```
>
> | Backend | Env Var | Search | Extract |
> |---|---|---|---|
> | Firecrawl (default) | FIRECRAWL_API_KEY | ✔ | ✔ |
> | SearXNG | SEARXNG_URL | ✔ | — |
> | Parallel | PARALLEL_API_KEY | ✔ | ✔ |
> | Tavily | TAVILY_API_KEY | ✔ | ✔ |
> | Exa | EXA_API_KEY | ✔ | ✔ |
>
> **Backend selection:** If `web.backend` is not set, the backend is auto-detected from available API keys. If only `SEARXNG_URL` is set, SearXNG is used. If only `EXA_API_KEY` is set, Exa is used. If only `TAVILY_API_KEY` is set, Tavily is used. If only `PARALLEL_API_KEY` is set, Parallel is used. Otherwise Firecrawl is the default.
>
> SearXNG is a free, self-hosted, privacy-respecting metasearch engine that queries 70+ search engines. No API key needed — just set `SEARXNG_URL` to your instance (e.g., `http://localhost:8080`). **SearXNG is search-only; web_extract requires a separate extract provider** (set `web.extract_backend`).
>
> Self-hosted Firecrawl: Set `FIRECRAWL_API_URL` to point at your own instance. When a custom URL is set, the API key becomes optional (set `USE_DB_AUTHENTICATION=...` on the server to disable auth).
>
> Parallel search modes: Set `PARALLEL_SEARCH_MODE` to control search behavior — `fast`, `one-shot`, or `agentic` (default: agentic).
>
> Exa: Set `EXA_API_KEY` in `~/.hermes/.env`. Supports category filtering (`company`, `research paper`, `news`, `people`, `personal site`, `pdf`) and domain/date filters.

## Source-code facts (from $HERMES_HOME/hermes-agent/, 2026-08-06)

- Provider ABC: `agent/web_search_provider.py` — `get_provider_env(name)` checks `os.environ` first, then `~/.hermes/.env` (config-aware; gateway/delegate children see .env values).
- Registry: `agent/web_search_registry.py` — legacy preference order `firecrawl → parallel → tavily → exa → searxng → brave-free → ddgs`, filtered by capability at every step.
- Built-in plugins: `plugins/web/{brave_free,ddgs,exa,firecrawl,parallel,searxng,tavily,xai}/plugin.yaml`, all `kind: backend`, advertise `provides_web_providers`.
- Config changes to `web.*` resolve per tool call — no session reset required (verified live 2026-08-06 after `hermes config set web.backend searxng`).
