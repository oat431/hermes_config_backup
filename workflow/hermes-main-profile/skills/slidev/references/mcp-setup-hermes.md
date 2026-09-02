# Slidev MCP Server Setup for Hermes Agent

Connect Hermes to a running Slidev dev server for AI-driven slide editing (read, update, insert, remove, reorder, navigate).

## Setup

```bash
hermes config set mcp_servers.slidev.url "http://localhost:PORT/__mcp"
hermes config set mcp_servers.slidev.connect_timeout 10
hermes config set mcp_servers.slidev.timeout 30
```

Replace `PORT` with the actual port from `bun run dev` output (usually 3030, but increments if port is busy).

**Restart Hermes** after config change — MCP servers are discovered at startup only (no hot-reload).

## Available Tools (registered as `mcp_slidev_*`)

| Tool | Description |
|------|-------------|
| `get-info` | Deck overview: entry, title, slide count, files |
| `list-slides` | All slides with number, title, layout, source file |
| `get-slide` | Full source of one slide (frontmatter, content, note) |
| `update-slide` | Edit content, note, and/or frontmatter |
| `insert-slide` | Insert new slide after existing one |
| `remove-slide` | Remove a slide |
| `move-slide` | Reorder slides (before/after another) |
| `goto-slide` | Navigate live presentation to a slide |

## Pitfalls

- **Port changes** on each `bun run dev` restart. Check the output for the actual port.
- **`mcp_reload_confirm: true`** in config means Hermes asks before reloading MCP connections.
- Tools operate on **1-based slide numbers** as shown in the presentation.
- Edits are saved to markdown files; dev server hot-reloads instantly.
- First slide of entry file cannot be removed/moved (it's the deck headmatter).
- Slides imported via `src:` are edited in their own file; moves cannot cross files.
