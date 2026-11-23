---
name: artcraft-mcp-wiring
description: "Wire PhotoCraft/LightCraft/DeckCraft/FigCraft MCP."
version: 1.0.0
author: devops
license: MIT
triggers:
  - wire photocraft / lightcraft / deckcraft as MCP servers into a Hermes profile
  - add or update an ArtCraft app MCP server in a Hermes profile
  - debug a craft MCP server that fails to connect
  - switch craft servers to connect/bridge mode (drive the running app)
  - update craft CLI versions and re-verify the MCP wiring
metadata:
  hermes:
    tags: [mcp, artcraft, photo-editing, presentations, hermes-profiles, windows]
    related_skills: []
---

# ArtCraft MCP Wiring (PhotoCraft / LightCraft / DeckCraft / FigCraft)

## When to Use

- Wiring an ArtCraft app CLI (PhotoCraft, LightCraft, DeckCraft, FigCraft, PdfCraft) as an MCP server in a Hermes profile
- A craft MCP server fails to connect, times out, or floods the client with too many tools
- Adding connect/bridge-mode variants so the agent can drive the running desktop app
- Re-verifying the wiring after an ArtCraft Launcher update

The storytold "ArtCraft" desktop apps install a CLI next to the GUI; the CLI doubles as a stdio MCP server (`<app>-cli mcp`). Wiring = an `mcp_servers` entry in a Hermes profile's `config.yaml`; verify with the `hermes` CLI.

## Installed artifacts (Windows; via ArtCraft Launcher)

| App | CLI exe | Version seen |
|---|---|---|
| PhotoCraft | `C:\Program Files\PhotoCraft\photocraft-cli.exe` | 0.7.0 |
| LightCraft | `C:\Program Files\LightCraft\lightcraft-cli.exe` | 0.6.0 |
| DeckCraft | `C:\Program Files\DeckCraft\deckcraft-cli.exe` | 0.6.1 |
| FigCraft | `C:\Program Files\FigCraft\figcraft-cli.exe` | 0.6.0 |
| PdfCraft | `C:\Program Files\PdfCraft\pdfcraft-cli.exe` | (not wired anywhere yet) |

Updates ship through the ArtCraft Launcher, not the CLIs. Wiring survives version bumps — re-verify with `hermes mcp test` after updates.

## Invocations

- **PhotoCraft**: `photocraft-cli mcp [--bridge 127.0.0.1:PORT] [--control-token <64-hex>|--control-token-file <f>] [--automation-read-root DIR] [--automation-write-root DIR]`
  - Headless default: the roots are the ONLY filesystem authority; in-memory commands work without roots. Bridge mode drives `photocraft --control PORT` via its token file. 21 tools.
  - Other subcommands: `convert`, `info`, `run`, `batch`, `droplet`, `commands`, `serve` (persistent JSON-lines headless session).
- **LightCraft**: `lightcraft-cli mcp [--compact] [--library DIR] [--connect [127.0.0.1:7980]] [--demo] [FILES/FOLDERS…]`
  - Full tool list: 318 (301 are per-command `cmd_*`). `--compact` = 17 helpers covering the whole workflow (import → develop → render → export; every command still reachable via `run_command`/`command_run`). Use compact unless the user explicitly wants every command as a tool.
  - Library lock: ONE program at a time (`catalog.lock` in the library). While the desktop app has the library open, `--library` refuses; while the headless server has it, the GUI can't open it. Use `--connect` (GUI started with `--control 7980`) for simultaneous live co-editing.
  - GUI default library: `~/Pictures/LightCraft Library`.
- **DeckCraft**: `deckcraft-cli mcp [--connect PORT] [--sample]` — headless default, 25 tools. Connect drives an app started with `--control 7990`. CLI helper: `deckcraft-cli describe ID`.
- **FigCraft**: `figcraft-cli mcp [--attach PORT|host:port]` (+ global `--no-system-fonts` / `FIGCRAFT_NO_SYSTEM_FONTS=1` for CI-stable renders). Headless default = one untitled document, 18 tools (Figma-class: nodes, auto layout, components, variables, prototyping, Dev Mode code export). Attach drives an app started with `figcraft --control 7979` (loopback only). Starter templates via `run_command` `template.list` → `file.newFromTemplate` (mobile-app, landing-page, dashboard, design-system, wireframe-kit, social-posts, slides, icon-set); MCP prompts: mobile_screen, design_system, landing_page, prototype_flow; resources `figcraft://document|commands|node/{id}|command/{id}`. No roots/sandbox — `open_file`/`save_file`/`export` take arbitrary paths.
- All: newline-delimited JSON-RPC over stdio (protocol 2025-06-18 accepted), logs to stderr, exit on stdin EOF.

Handshake probe (git-bash):

```bash
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}\n' | "<exe>" mcp [flags...] | head -c 800
```

## Hermes config block (verified shape)

```yaml
mcp_servers:
  photocraft:
    command: C:/Program Files/PhotoCraft/photocraft-cli.exe
    args:
      - mcp
      - --automation-read-root
      - F:\photo
      - --automation-write-root
      - F:\photo\exports
    connect_timeout: 60
    timeout: 300
```

- Valid keys (Hermes MCP reference): `command`, `args`, `env`, `url`, `headers`, `enabled`, `timeout`, `connect_timeout`, `tools.include/exclude`, `supports_parallel_tool_calls`.
- Forward-slash exe paths work (spawned directly, no shell — spaces are fine); YAML plain scalars take `F:\...` args as-is.
- `timeout: 300` — renders/exports legitimately run long. `connect_timeout: 60` — generous for first library open on big catalogs (Hermes' default bound is 30s).

## Procedure

1. Recon: `ls "/c/Program Files" | grep -i craft` → `<exe> --version` → handshake probe above.
2. Backup config: `cp <profile>/config.yaml <scratch>/<profile>-config.yaml.bak-$(date +%Y%m%d-%H%M%S)`.
3. **Patch** (never whole-file write — see pitfalls) the `mcp_servers:` block in `profiles/<name>/config.yaml`.
4. Validate YAML: hermes venv python — `import yaml; yaml.safe_load(open(r'<cfg>', encoding='utf-8'))` — then confirm secrets in the file were untouched.
5. Verify: `hermes -p <profile> mcp list` → `hermes -p <profile> mcp test <server>` (shows connect status + discovered tools).
6. End-to-end: `hermes -p <profile> -z "<read-only prompt that calls one craft tool>"` — proves the profile's agent sees and can call the tools.
7. Reload: new session in the desktop app, or `/reload-mcp` in an open session.

## Pitfalls

- **Never `write_file` a config you read** — the model sees secrets as `***` (redaction); a whole-file write replaces real tokens with `***`. Use surgical `patch` only.
- Collection-built Hermes profiles can ship a broken `github: {command: npx}` stub (no args) — connect stalls ~30s per attempt. Fix: `enabled: false` (+ comment), or add args + token to make it live.
- MSYS/git-bash: path conversion is off — pass native `C:/…` or `F:\…` paths as exe arguments; keep scratch files under `$TMPDIR`.
- `hermes -p <profile> <cmd>` targets a profile for ALL CLI commands (mcp list/test/etc.).
- Counts differ slightly from raw server counts: Hermes adds `list_resources`/`read_resource` wrappers (e.g. LightCraft 17 → 19 visible, PhotoCraft 21 → 23, DeckCraft 25 → 27).
- LightCraft library is created on first open if the path doesn't exist — a headless `mcp test` is enough to seed it.

## Wired state (last updated 2026-10-13)

- `photo-artisan` profile: `photocraft` (read `F:\photo`, write `F:\photo\exports`), `lightcraft` (`--compact --library "F:\photo\LightCraft Library"`); broken `github` stub disabled. E2E verified: agent called `doc_inspect` / saw 19 + 23 tools.
- `deck` profile: `deckcraft` (headless); `github` stub disabled; existing `powerpoint` (uvx ppt-mcp) server untouched. E2E verified: `new_presentation` + `inspect_document`, 27 tools visible.
- `ui-ux` profile: `figcraft` (headless); E2E verified: built `mobile-app` starter template, screenshot described by the agent, PNG exported to disk (227 KB), 22 tools visible (18 + resource/prompt wrappers). Note: ui-ux `searxng` still points at `http://localhost:7008` (suspect stale; fleet uses the Tailscale URL) — flagged, not changed.
