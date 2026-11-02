---
title: "Hermes Config Review 2026-10-23"
tags: [hermes, config, review, audit, security, maintenance]
created: 2026-10-23
---

# Hermes Config Review — 2026-10-23

> Full pass over `%LOCALAPPDATA%\hermes` right after today's gateway-multiplex migration. Scope: gateway topology, MCP servers, credentials, disk hygiene, `hermes doctor` output. Findings ranked by what actually needs a decision vs. what's already fine.

## What changed today (for the record)

Desktop app was stuck in a boot loop (`Gateway inaccessible (profile_parked)`). Root cause had two layers:

1. Four profiles (`deck`, `devops`, `full-stack`, `gym`) had leftover Windows Scheduled-Task / Startup-folder gateway launchers from before they moved to the shared gateway — no live process, just stale install artifacts `hermes gateway migrate --multiplex` wanted to remove.
2. That migration was fully **blocked**: six profiles (`audiophile`, `book-summarizer`, `career-coach`, `data-engineer`, `journey-writer`, `security-engineer`) held the same `DISCORD_BOT_TOKEN` as `default`, and Hermes refuses to change anything while a credential conflict exists.

Fixed: removed the duplicate `DISCORD_BOT_TOKEN` / `DISCORD_ALLOWED_USERS` from those six profiles' `.env` files, then ran `hermes gateway migrate --multiplex -y`. Confirmed via `hermes gateway list` and `hermes doctor` — all 18 profiles now run under one multiplexed gateway process, no standalone warnings left.

## 🔴 Needs a decision — privacy exposure in the public repo

**`soul-collection/Life Styles/financial-advisor-soul.md` is tracked and already live on `github.com/oat431/hermes_config_backup`**, even though this repo's own `README.md` says it's excluded:

> "The `.gitignore` already excludes the **financial-advisor soul** (personal finance details)."

Checked directly: `.gitignore` has no rule matching that path, `git log --follow` shows it was added in commit `9a76187 "backup: finance soul"`, and the local branch isn't ahead of `origin/main` — so it has been pushed and is sitting in the public repo's history right now, not just staged locally.

- **Going forward:** add the real path to `.gitignore`, e.g. `/soul-collection/Life Styles/financial-advisor-soul.md`.
- **Already exposed:** removing the file only stops *future* pushes — it stays retrievable from GitHub's commit history (and any fork) until the history itself is rewritten. If that content shouldn't be public, the real fixes are `git filter-repo` / BFG to purge it from history plus a force-push, or making the repo private. I didn't touch git history or push anything — that's a judgment call on exposure/impact that's yours to make, and rewriting published history is disruptive for anyone else who's cloned the repo.

## 🟠 Broken — the `github` MCP server

`config.yaml → mcp_servers.github` is just:

```yaml
github:
  command: npx
```

No `args` — unlike every other entry (`postgres`, `drawio`, `filesystem`, `searxng`), which all pass `-y <package-name>`. This spawns bare `npx` with nothing to run. `logs/gateway-stdio.log` confirms it's been failing on every connection attempt: the MCP client tries to parse `npx`'s own help/banner text as a JSON-RPC message, fails, and the connection eventually gives up with `CancelledError`. `hermes doctor` shows your `GITHUB_TOKEN` is valid and accepted by `api.github.com`, so the credential is fine — it's purely a missing server definition. Likely intended shape:

```yaml
github:
  command: npx
  args:
    - -y
    - '@modelcontextprotocol/server-github'
  env:
    GITHUB_PERSONAL_ACCESS_TOKEN: ${GITHUB_TOKEN}
```

(Exact package name depends on which GitHub MCP server you meant to wire up — ask and I'll fix it directly.)

## 🟡 Likely-dead config

- **Telegram**: `agent.platforms.telegram.streaming: true` is set, but `hermes doctor` reports `python-telegram-bot (optional, not installed)`. Telegram almost certainly isn't functional right now. Either install the package (`pip install python-telegram-bot`, or run `hermes setup`) or drop the `telegram:` block if it's not in use.
- **DASHSCOPE_API_KEY** and **AWS Bedrock** credentials in the root `.env`: `doctor` flags both as failing (DashScope: HTTP 429 + invalid key for the China endpoint; Bedrock: invalid security token), but grepping every profile's `config.yaml` shows **none** of them use `dashscope` or `bedrock` as a provider — everything runs on `xiaomi` / `mimo-v2.6-pro` with `deepseek` as the fallback. These read as leftovers from earlier experimentation. Safe to ignore, or delete the keys to quiet the warnings.

## 🟡 Disk hygiene — ~1.36 GB reclaimable, low risk

| Item | Size | Age |
|---|---|---|
| `state.db.pre-update-emergency-2026-09-20T11-45-21-487Z.bak` | 344 MB | Sep 20 |
| `state.db.pre-update-emergency-2026-09-20T19-17-17-656Z.bak` | 344 MB | Sep 20 |
| `state.db.pre-update-emergency-2026-09-22T09-37-45-360Z.bak` | 344 MB | Sep 22 |
| `state-snapshots/20260721-135938-pre-update/` | 331 MB | Jul 21 |

These are auto-made safety nets from past `hermes update` runs. Hermes has updated cleanly multiple times since (now on v0.22.4, `doctor` reports no problems with the live 33.5 MB `state.db`), so these are very likely dead weight. `cache/` has also grown to 737 MB — Hermes regenerates it automatically, safe to clear whenever disk space matters. Didn't delete any of this — flagging only, since it's chat history / update safety data and that's your call.

## 🟢 Already resolved / no action needed

- **Gateway topology** — fixed today; all 18 profiles now share one multiplexed gateway (confirmed via `hermes gateway list`).
- The transient `Gateway start via direct spawn FAILED` message during today's migration is a known Windows "Job Object" race in Hermes's restart path — upstream is routing that handoff through a transient Scheduled Task to fix it for good (see refs below). It already self-recovered via exactly that scheduled-task fallback. No action needed unless it recurs.
- `web` / `ui-tui` npm workspace vulnerabilities (1 high + a few moderate each, per `hermes doctor`) — upstream lockfile issue, resolves itself on the next `hermes update`.
- Hermes itself is current (v0.22.4, confirmed up to date).

## Optional, not urgent

- Six profiles (`audiophile`, `book-summarizer`, `career-coach`, `data-engineer`, `journey-writer`, `security-engineer`) no longer have their own Discord token, so they're silent on Discord now. If any of them should still answer there, decide per-profile between giving it a dedicated bot token or routing it through `default` via `gateway.profile_routes`.

## References

- [NousResearch/hermes-agent#42116 — Windows detached gateway /restart fails in job objects (WinError 5)](https://github.com/NousResearch/hermes-agent/issues/42116)
- [Hermes Agent v0.22.0 — "The Threshold Release" (gateway multiplex consolidation)](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.0)
