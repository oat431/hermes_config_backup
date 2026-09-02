---
name: hermes-setup-replication
description: "Replicate a Hermes install onto a new Windows machine."
version: 1.0.0
author: OraMesLita (Hermes Agent)
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [hermes, setup, replication, windows, searxng, openrouter, profiles, handoff]
---

# Hermes Setup Replication (Windows)

## When to Use

- User wants "their Hermes setup" on a new computer — own machine broke, or installing for a friend.
- Rebuilding a machine from scratch and restoring Hermes.
- Preparing a handoff pack (souls, skills, profiles) to carry to another machine.
- Answering "how do I install Hermes with searxng + OpenRouter on a fresh PC?"

## Core Facts (verified 2026-08)

- Windows HERMES_HOME = `%LOCALAPPDATA%\hermes` (never `~/.hermes` on Windows).
- Windows install one-liner (PowerShell, no admin): `iex (irm https://hermes-agent.nousresearch.com/install.ps1)` — installs uv, Python 3.11, Node.js, ripgrep, ffmpeg, and a portable Git Bash (MinGit) into `%LOCALAPPDATA%\hermes\git`.
- Canonical runbook lives in the backup repo: `F:\obsidian_note\hermes_config_backup\Hermes-Setup-Install.md`. Update it when the reference setup changes; the skill stays the condensed procedure.
- Backup repo (canonical handoff source): `F:\obsidian_note\hermes_config_backup` → GitHub `oat431/hermes_config_backup`. Layout: `soul-collection/` (14 souls), `workflow/hermes-main-profile/` (22 main skills), `workflow/<profile>/` (per-profile skills). See `references/backup-repo-layout.md`.
- Panomete's fleet: 12+ profiles, each with SOUL.md + config.yaml (provider/model/MCP). Main profile config has its own model block. Profiles carry their own custom skills under `profiles/<name>/skills/` — back those up per-profile, they do NOT live in the main skills dir.

## Workflow

1. **Recon the source machine first** — never guess from memory: `model:` section in config.yaml, `.env` key NAMES only (never values), `profiles/` listing, skill folder layout, soul-collection contents.
2. **Prepare the handoff pack** — lean copies, no secrets, no caches (see below).
3. **Target machine** — install Hermes → wire OpenRouter → stand up local searxng (Docker) → copy skills by folder → copy soul → copy profile.
4. **Verify** with the checklist at the end.

## Handoff Pack (run on the source machine)

- **Backup repo is the pack.** `F:\obsidian_note\hermes_config_backup` (pushed to GitHub `oat431/hermes_config_backup`) is the canonical restore source — souls, skills, runbook. `oralita_md` is STALE legacy; never point a new machine there.
- **Main skills:** copy folders from `workflow/hermes-main-profile/<skill>\` → target `%LOCALAPPDATA%\hermes\skills\<category>\<skill>\`. `hermes skills install` accepts ONLY registry IDs or URLs — folder copy is the manual install path, and the only path for manual/protected skills.
- **Profile skills:** each profile's custom skills are backed up under `workflow/<profile-name>\`. Restore: copy `workflow/<name>/*` → `%LOCALAPPDATA%\hermes\profiles\<name>\skills\`. They are NOT in the main skills dir — forgetting them loses per-profile capabilities (devops has 6, educator 10, full-stack 11, product-owner 12, qa 6, etc.).
- `oralita-book-sum-obs` requires its 3 related skills to work fully: `obsidian`, `bok-essential-documents`, `ocr-and-documents` (copy their whole category folders).
- **Soul:** canonical copy = `F:\obsidian_note\hermes_config_backup\soul-collection\hermes-main-soul.md` → target `%LOCALAPPDATA%\hermes\SOUL.md` (back up the fresh default first). Profile souls live in `soul-collection\AI-SDLC\` and `soul-collection\Life Styles\` — hash-verify live `SOUL.md` vs backup when syncing (`md5` match = synced).
- **Profile config:** lean copy = `SOUL.md` + `memories/` + `config.yaml` (~28 KB). `hermes profile export` works but ships 100+ MB of caches (state.db, sessions, audio_cache, delegation logs) — prefer lean unless full fidelity is explicitly wanted. NOTE: each profile's config.yaml needs its own `mcp_servers` block (not inherited from main) and `_config_version` (missing it triggers "gateway needs setup" on load).
- **NEVER put real API keys in the pack.** Each machine owns its own keys (target owner pastes their own). Secret-scan the pack before committing: `grep -rE 'ghp_|sk-[A-Za-z0-9]{20,}|API_KEY\s*=\s*\S' workflow/ soul-collection/`.

## Target Machine Steps (condensed)

1. Install: PowerShell → `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`; verify `hermes --version`.
2. OpenRouter: `hermes setup` (pick OpenRouter, paste key, pick model) — or manual: `hermes config set model.provider openrouter`, `hermes config set model.default <id>`, `OPENROUTER_API_KEY=...` in `%LOCALAPPDATA%\hermes\.env`.
3. Local searxng: `winget install --id Docker.DockerDesktop` → compose from `templates/searxng-docker-compose.yml` + `templates/searxng-settings.yml` → `docker compose up -d` → verify `curl "http://127.0.0.1:7004/search?q=test&format=json"`.
4. Wire searxng: `hermes config set web.backend searxng` + `SEARXNG_URL=http://127.0.0.1:7004` in `.env`.
5. Skills: copy handoff folders into `%LOCALAPPDATA%\hermes\skills\<category>\`; verify `hermes skills list`.
6. Soul: copy `hermes-main-soul.md` → `%LOCALAPPDATA%\hermes\SOUL.md`; restart Hermes.
7. Profile: `mkdir profiles\educator`, copy SOUL.md + memories + config.yaml; `hermes profile use educator` (or leave main as default); verify `hermes profile list`.
8. Final: `hermes desktop`, `hermes doctor`, chat test, web-search test, `docker ps`.

## Pitfalls

- **searxng-docker repo is DEPRECATED** — use the official compose template from the searxng/searxng repo `container/` folder (embedded in templates/ here).
- The official compose template's `:Z` SELinux mount flag **breaks on Windows** — remove it.
- searxng's default settings do NOT guarantee the JSON API — `settings.yml` must include `search.formats: [html, json]`, or Hermes gets `invalid format` 400 responses.
- Antivirus flags `uv.exe` (unsigned Rust binary) as malware — false positive; whitelist the `%LOCALAPPDATA%\hermes\bin` FOLDER (hash changes every update).
- `web_extract` has no keyless backend — searxng only does search; page extraction still needs tavily/firecrawl/exa/parallel. Set expectations when the target asks about "reading" web pages.
- OpenRouter model prices move — fetch live from `https://openrouter.ai/api/v1/models` before recommending (see references/ for the dated ladder).
- `hermes profile export` includes caches — use lean copy for handoffs (see Handoff Pack).

## Verification Checklist

- [ ] `hermes --version` works; `hermes doctor` clean
- [ ] Chat responds via OpenRouter (model from the ladder)
- [ ] Web search returns live results (searxng JSON API)
- [ ] `hermes skills list` shows `oralita-book-sum-obs`
- [ ] `hermes profile list` shows the imported profile
- [ ] `docker ps` shows `searxng-core` + `searxng-valkey` running

## Support Files

- `templates/searxng-docker-compose.yml` — Windows-ready searxng compose (port 7004, no `:Z`).
- `templates/searxng-settings.yml` — minimal settings enabling the JSON API Hermes requires.
- `references/windows-reinstall-verified-details.md` — dated verified facts: exact handoff commands, OpenRouter price ladder, profile structure/sizes, source-machine recon recipe.
- `references/backup-repo-layout.md` — canonical backup repo structure (soul-collection/ + workflow/hermes-main-profile/ + per-profile folders), profile-skill inventory, sync + restore + secret-scan procedure.
