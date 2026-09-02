# Windows Hermes Replication — Verified Details (2026-08-06)

Everything below was verified live against the source machine and official
sources on 2026-08-06. Re-verify anything that smells stale before trusting it.

## Source-machine recon recipe

```bash
# model/provider config
grep -B2 -A8 "^model:" "$HERMES_HOME/config.yaml"
# web backend section
grep -A 10 -i "web:" "$HERMES_HOME/config.yaml"
# .env key NAMES only (never print values)
sed 's/=.*/=<redacted>/' "$HERMES_HOME/.env"
# profiles / skills / soul collection layout
ls "$HERMES_HOME/profiles/" && ls "$HERMES_HOME/skills/"
ls 'F:/obsidian_note/oralita_md/soul-collection/'
```

## Install facts

- Windows install: `iex (irm https://hermes-agent.nousresearch.com/install.ps1)` (PowerShell).
- Installer provides: uv, Python 3.11, Node.js, ripgrep, ffmpeg, portable Git Bash
  (MinGit at `%LOCALAPPDATA%\hermes\git`, isolated from system Git).
- Everything under `%LOCALAPPDATA%\hermes`; `hermes` launcher is a venv binary at
  `$HERMES_HOME\hermes-agent\venv\Scripts\hermes` on git-installed boxes.
- Antivirus false positive on `uv.exe` → whitelist folder:
  `Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\hermes\bin"` (folder, not hash).

## OpenRouter model ladder (prices fetched live 2026-08-06, $ per 1M tokens, in/out)

| Tier | Model ID | ≈ in / out |
|---|---|---|
| Frontier | anthropic/claude-opus-4.8 | $5 / $25 |
| Frontier | anthropic/claude-sonnet-5 | $2 / $10 |
| Frontier | google/gemini-2.5-pro | $1 / $10 |
| Like-me (Chinese) | deepseek/deepseek-v4-pro | ~$0 / ~$1 |
| Like-me (Chinese) | qwen/qwen3.7-plus | ~$1 / ~$1 |
| Like-me (Chinese) | z-ai/glm-4.7-flash | ≈ $0 |
| Like-me (Chinese) | moonshotai/kimi-k2.5 | $1 / $3 |
| Budget | deepseek/deepseek-v4-flash | ≈ $0 |
| Budget | qwen/qwen3.7-flash | ≈ $0 |
| Budget | google/gemini-2.5-flash-lite | ≈ $0 |

- `~`-prefixed IDs (e.g. `~anthropic/claude-opus-latest`) auto-track latest.
- Panomete's own educator profile uses `openrouter` + `z-ai/glm-5.2` (reference pick).
- Refresh: `curl -fsSL https://openrouter.ai/api/v1/models` and filter with python/jq.

## searxng facts

- `searxng/searxng-docker` repo is SUPERSEDED — official install path:
  https://docs.searxng.org/admin/installation-docker.html (compose instancing).
- Compose template source: `searxng/searxng` repo, `container/docker-compose.yml`.
- The official template has a `:Z` SELinux mount suffix that breaks on Windows — strip it.
- Default settings.yml does not necessarily expose the JSON format — add
  `search.formats: [html, json]`; verify with
  `curl "http://127.0.0.1:7004/search?q=test&format=json"`.
- Hermes wiring: `hermes config set web.backend searxng` + `SEARXNG_URL=http://127.0.0.1:7004`
  in `%LOCALAPPDATA%\hermes\.env`. No key needed for search; web_extract still needs
  a keyed provider (tavily/firecrawl/exa/parallel).

## Profile structure / sizes (source machine, educator profile)

- Full profile dir: SOUL.md (8K), memories/ (12K: MEMORY.md + USER.md), skills/ (49M,
  mirrors the standard bundled categories), config.yaml (4K, `_config_version: 33`),
  plus state.db / sessions / audio_cache / cache / logs (the 100+ MB bulk).
- `hermes profile export <name>` → tar.gz INCLUDES caches (measured 105 MB) — fine for
  backup, wasteful for handoff. Import: `hermes profile import <archive>.tar.gz [--name X]`.
- Profile switching: `hermes profile use <name>` (sticky default), `hermes profile list`.
- `hermes skills install` takes registry IDs or URLs only — local folders are installed
  by copying into `$HERMES_HOME\skills\<category>\`.

## Skill dependency set for oralita-book-sum-obs

- oralita-book-sum-obs + obsidian + bok-essential-documents + ocr-and-documents
  (sizes: 280K personal-agents-skill/, 12K obsidian, 24K bok-essential-documents, 17K ocr).
