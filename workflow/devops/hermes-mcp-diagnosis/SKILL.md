---
name: hermes-mcp-diagnosis
description: "Use when a Hermes MCP server looks down or outdated."
---

# Diagnosing & Upgrading a Hermes MCP Server

## When to Use

- A Hermes MCP server appears "down", throws invalid-argument or schema errors, or returns results
  that look stale compared to what the upstream service offers
- The user asks whether an MCP integration is outdated, or wants to move off a deprecated
  npm/stdio MCP package onto the vendor's official server
- Tool names the agent expects are missing even though the config file looks correct

"MCP is down" is usually one of four things: actually down, invalid arguments, a stale client surface,
or a deprecated package. Prove which before changing config.

## 1. Prove liveness before believing "down"

Call 2-3 **read-only** tools from the server (e.g. `search_repositories`, `list_commits`,
`get_file_contents`). Real data back = the server is alive; the problem is elsewhere.
Never test liveness with a write tool.

## 2. Check package health (the usual root cause)

```bash
npm view <pkg> version deprecated time.modified
```

`deprecated: Package no longer supported` = frozen package. Record the publish date and compare
with today; `2025.4.8` in late 2026 means ~19 months of missing API coverage.

## 3. Separate "syntax error" from invalid arguments

Old TS servers ship `"additionalProperties": false` plus counter-intuitive names (`q` not `query`,
`pull_number` not `number`). A schema-invalid call returns `missing required argument(s): q` — that is
a frozen schema, not corruption. `tool_describe` the tool and read `required` before judging.

## 4. Probe the official replacement before touching config

The GitHub official server is remote HTTP: `https://api.githubcopilot.com/mcp/`. Verify with the
user's existing token (never print it; extract from config on the fly):

- `POST` an `initialize` body (`protocolVersion: 2025-06-18`) with
  `Authorization: Bearer $TOKEN`, `Accept: application/json, text/event-stream`
- capture `Mcp-Session-Id` from response headers, send `notifications/initialized`,
  then `tools/list` (follow `nextCursor`)
- Responses are SSE (`data: {...}` lines), not bare JSON.

Default remote toolset is **repos/issues/PRs only** — no CI or security. Add
`X-MCP-Toolsets: repos,issues,pull_requests,actions,code_security,dependabot,...`
(`all` = ~113 tools, heavy context cost; the devops mix is ~62).

## 5. Hermes remote-server config shape

```yaml
mcp_servers:
  github:
    url: https://api.githubcopilot.com/mcp/
    headers:
      Authorization: "Bearer ${MCP_GITHUB_API_KEY}"
      X-MCP-Toolsets: all
```

Hermes supports streamable HTTP and interpolates `${VAR}` in `url`/`headers` from the profile `.env`.
Key name convention from `hermes mcp add --auth header`: `MCP_<NAME>_API_KEY`, so the secret leaves
plaintext `config.yaml`. Migrate an existing inline token to `.env` **without echoing it**: read config
in Python, regex the token, write `.env`, rewrite the block by line range (a plaintext token cannot be
matched with the `patch` tool because it is redacted in tool output).

## 6. The gateway owns MCP — config changes need `/reload-mcp`

This is the trap. On desktop/CLI, **every turn executes in the gateway process**, which discovered and
registered MCP tools at its own startup:

- `hermes -z "..."` routes to the running gateway (`platform=local` in `logs/gateway.log`), so it
  reports the OLD tool surface and proves nothing about a config change.
- `hermes mcp test <name>` is the honest config-level proof: it connects with the new config and prints
  transport, latency and tool count.
- **A config probe is not a live registry.** An MCP settings page or `mcp test` reporting "113 connected"
  only proves the config connects. The agent's actual surface is per-session and stays stale until the
  gateway reloads. Verify the *registry* — `tool_search` returns
  `available_sources: [{name: github, tool_count: 26}]` — and confirm a brand-new session sees the new
  count before declaring success.
- Apply at runtime with the `/reload-mcp` slash command (user action) or an app restart. There is **no**
  `hermes mcp reload` and no `reload-mcp` control-socket verb; `_PROFILE_RESCAN_INTERVAL_SECS` only
  rescans profile adapters.
- **Never** `hermes gateway restart` mid-conversation: the executing agent runs inside that process, so
  it kills its own turn.

Windows: a gateway-free agent is impossible (`Error: Gateway inaccessible: windows_breakaway_unavailable`),
so a throwaway `HERMES_HOME` cannot be used for E2E verification.

## 7. Clear stale schema cache

`<profile>/cache/mcp_schema_cache.json` holds per-server manifests keyed by a fingerprint of
`command/args/url/transport/tools-include/exclude`. It is a **miss** when the transport changes, so it
cannot serve the wrong tools — but delete the server's key anyway when migrating, to rule out a lazy
registration from an old manifest. Lazy cache use requires `lazy: true` on the server.

## 8. Migration is a breaking rename — say so

Method-based collapse breaks hardcoded tool names. For GitHub v2025.4.8 → official:

| Old | New |
|---|---|
| `get_issue` | `issue_read` `method=get` (+ `get_comments`, `get_labels`, `get_sub_issues`) |
| `create_issue` / `update_issue` | `issue_write` `method=create` / `update` |
| `get_pull_request`, `_comments`, `_files`, `_reviews`, `_status` | `pull_request_read` `method=get` / `get_comments` / `get_files` / `get_reviews` / `get_status` |
| `create_pull_request_review` | `pull_request_review_write` `method=create` |

Compute the diff in code (`set(old) - set(new)`) rather than eyeballing lists; report both the renames
and the gained capabilities.

## Reporting

Give the user hypothesis/result/evidence as a table, state plainly that the server was never down when
that is what the evidence shows, then ask which upgrade path they want before editing config or moving
credentials.
