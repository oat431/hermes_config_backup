# MediaWiki API Quirks & Test Harness

Tested behaviors from live sessions against bg3.wiki (wiki.gg), baldursgate.fandom.com, and the @professional-wiki/mediawiki-mcp-server npm package (v0.17.0).

## API Endpoint Locations

| Host | api.php path | Notes |
|---|---|---|
| bg3.wiki (wiki.gg) | `/w/api.php` | `/api.php` and `/mw/api.php` return nginx 404 |
| *.fandom.com | `/api.php` | scriptpath is empty string |
| wikipedia.org | `/w/api.php` | classic |

Resolve any unknown wiki via `action=query&meta=siteinfo&siprop=general` and read `scriptpath` from the response — or call the MCP `get-site-info` tool.

## Tested Query Patterns

```
# 1. Find exact titles (do this FIRST — quest pages have non-obvious names)
GET <api>?action=query&format=json&list=search&srsearch=<urlencoded>&srlimit=5

# 2. Pull plain-text extract (ONE title per request — see quirks)
GET <api>?action=query&format=json&prop=extracts&explaintext=1&titles=<one urlencoded title>&redirects=1

# 3. Intro-only variant (lighter): add &exintro=1

# 4. Site info / extension detection (which structured-data tools apply)
GET <api>?action=query&format=json&meta=siteinfo&siprop=general|extensions
```

## Quirks (verified live)

- **`prop=extracts` fills only the FIRST full extract per multi-title request** — remaining pages return 0-char extracts. Batch page *discovery*, never batch *extracts*.
- **Cargo detection**: siteinfo `extensions` list contains `Cargo` on bg3.wiki. Fandom wikis: no Cargo. wiki.gg may rebrand it as `LIBRARIAN`.
- **cargo-query (action=cargoquery) is anonymous-blocked on bg3.wiki** — `permissiondenied: You don't have permission to run arbitrary Cargo queries`. Same denial via the MCP `cargo-query` tool. Needs a wiki account (OAuth/bot password). `cargo-list-tables` and `cargo-describe-table` DO work anonymously.
- **Send a descriptive User-Agent** with curl (`-A "HermesAgent/1.0 (contact: …)"`). Bare curl worked against Fandom but is poor API etiquette and may hit CDN bot filters on wiki.gg.
- **Fandom wiki merges**: `baldursgate3.fandom.com` redirects to `baldursgate.fandom.com` (the classic-saga wiki). A wiki being reachable ≠ it covering your game. Probe with a character you know exists in the target game before trusting search results.

## MCP Server: stdio test harness pattern

To smoke-test an MCP server without wiring it into Hermes, speak newline-delimited JSON-RPC over the subprocess's stdin/stdout:

1. `subprocess.Popen(["npx", "-y", "<package>"], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True, bufsize=1, shell=True)` (shell=True needed on Windows to resolve npx)
2. Reader thread pushes stdout lines into a `queue.Queue`
3. Send `initialize` request → wait for matching `id` → send `notifications/initialized` notification → `tools/list` → `tools/call`
4. Windows note: when the harness script lives in the profile workspace, invoke it with a forward-slash absolute path (`python "C:/Users/.../script.py"`) — `$HERMES_HOME` inside the terminal shell already resolves to the profile dir, so `$HERMES_HOME/profiles/<name>/...` double-counts the segment.

Working reference implementation from the 2026-08-20 session: `workspace/test_mediawiki_mcp.py` and `workspace/test_mediawiki_mcp2.py` under this profile.

## Registering a custom MCP server into Hermes

```
echo Y | hermes mcp add <name> --command npx --args -y <npm-package> --env CONFIG=<abs path to config json>
hermes mcp list   # verify enabled
hermes mcp test <name>   # live connection + tool discovery check
```

- `hermes mcp add` prompts "Enable all tools? [Y/n/select]" interactively — pipe `echo Y` in non-TTY contexts or it cancels.
- `setup_mcp` consent-card tool only covers **catalog** entries; custom servers go through `hermes mcp add`.
- MCP tools inject at session **startup** — a session started before registration must wait for a new session (or use the raw-API curl path above).
- Restart required after add/remove; no hot-reload.
