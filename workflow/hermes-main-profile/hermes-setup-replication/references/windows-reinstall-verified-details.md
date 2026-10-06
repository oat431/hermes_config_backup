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

## QwenCloud Token Plan — model ladder (verified 2026-08-29)

Single provider for main + all 14 profiles. All 6 models on the Personal Edition:

| Model | Good for |
|---|---|
| `qwen3.8-max` | strongest Qwen — general/writing |
| `qwen3.8-flash` | fast Qwen — bulk/light work |
| `qwen3.7-max` | prior-gen Qwen max |
| `deepseek-v4-pro` | heavy reasoning — code, infra, analysis |
| `deepseek-v4-flash-0731` | **default** — fast + capable, good all-rounder |
| `glm-5.2` | multimodal + reasoning — visual/teaching tasks |

Config:
```yaml
model:
  default: deepseek-v4-flash-0731
  provider: alibaba
```

Env (REQUIRED in every profile's `.env` — NOT inherited from main):
```ini
DASHSCOPE_API_KEY=<token-plan-key>
DASHSCOPE_BASE_URL=https://token-plan.ap-southeast-1.maas.aliyuncs.com/apps/anthropic
```

⚠️ The `alibaba` provider defaults to OpenAI-compatible `dashscope-intl.aliyuncs.com`,
but the Token Plan key only works against the Anthropic-protocol token-plan gateway.
`DASHSCOPE_BASE_URL` is **required** — without it, the provider resolves the wrong
endpoint and auth fails silently.

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
