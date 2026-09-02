# Machine Replication & Skill Publishing — Verified Run (2026-08-06)

Session-tested detail behind the "Replicating the Setup to a New Machine" section. Everything here was executed and verified on Panomete's Windows box + `oat431/oralita_md`.

## Handoff source layout (oat431/oralita_md, public, Unlicense)

| Path | Role |
|---|---|
| `workflow/<skill>/` | Canonical dev copies of custom skills |
| `skills/<skill>/` | Published copies (created by `hermes skills publish`) |
| `soul-collection/` | Souls: `hermes-main-soul.md`, `profile-registry.md`, `AI-SDLC/`, `Life Styles/` |
| `profiles/<name>/` | Sanitized profile handoffs (SOUL.md + memories/ + sanitized config.yaml) |
| `Quick Note/Hermes-Setup-Install.md` | The user-facing runbook |

Verified: `workflow/` and `skills/` copies of a skill are byte-identical after CRLF normalization (published copies land CRLF from Windows installs). Keep both in sync on edits — or pick one canonical and mirror.

## Windows install (native, no admin)

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Installs uv, Python 3.11, Node.js, ripgrep, ffmpeg, portable Git Bash (MinGit at `%LOCALAPPDATA%\hermes\git`). Everything under `%LOCALAPPDATA%\hermes`. The `install.sh` script is Linux/macOS/Android-only — Windows must use the PowerShell installer.

Antivirus false positive: ML engines flag `%LOCALAPPDATA%\hermes\bin\uv.exe` (unsigned Rust binary). Whitelist the **folder**, not the hash (hash changes every update): `Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\hermes\bin"`.

## Local searxng (Docker) — Hermes requires JSON format

- `searxng-docker` repo is **deprecated**; use the official compose template: `https://raw.githubusercontent.com/searxng/searxng/master/container/docker-compose.yml` (+ `.env.example`), `searxng-core` + `searxng-valkey` services, `./core-config/:/etc/searxng/` volume.
- **Remove the `:Z` mount flag** (SELinux-only; breaks on Windows Docker Desktop).
- **Hermes' searxng backend needs `format=json`** — the auto-generated defaults may not include it. Minimal `core-config/settings.yml`:
  ```yaml
  server:
    secret_key: "any-long-random-string"
  search:
    formats:
      - html
      - json
  ```
- Verify: `curl "http://127.0.0.1:7004/search?q=test&format=json"` → JSON with `results`. A 400 `invalid format` = settings.yml not mounted → `docker compose restart`.
- Hermes wiring: `hermes config set web.backend searxng` + `SEARXNG_URL=http://127.0.0.1:7004` in `%LOCALAPPDATA%\hermes\.env`. Searxng is keyless for search; `web_extract` still needs a keyed extractor (tavily/firecrawl/exa) — for doc pages, `curl` the raw URL instead.

## Skill install paths

- Tap: `hermes skills tap add oat431/oralita_md` → registers with path `skills/` (default). Skills not under `skills/` are **invisible to taps** — `hermes skills install <name>` then fails with "No skill named ... found in any source". Do not conclude taps are broken; the repo layout is the issue.
- Direct URL (works regardless of layout): `hermes skills install "https://raw.githubusercontent.com/<owner>/<repo>/main/<path>/SKILL.md"` — use `main`, not `master`.
- Preview without installing: `hermes skills inspect <url-or-name>`.

## Profile handoff

- `hermes profile export <name> -o out.tar.gz` — full archive but includes caches: observed **105 MB** (delegation logs, audio_cache, state.db, sessions).
- Lean copy (≈28 KB): `SOUL.md` + `memories/` + `config.yaml`. Skip `state.db`, `sessions/`, `cache/`, `audio_cache/`.
- Restore: `hermes profile import <archive>.tar.gz` or folder copy into `%LOCALAPPDATA%\hermes\profiles\<name>\`; sticky default via `hermes profile use <name>`.
- Educator profile's config already carried `provider: openrouter, model: z-ai/glm-5.2` — good reference config for OpenRouter wiring.

## 🔴 GH013 incident (the lesson)

Copying `profiles/educator/config.yaml` verbatim into the repo included `mcp_servers.github.env.GITHUB_PERSONAL_ACCESS_TOKEN` (live PAT, same value as `$HERMES_HOME/.env` GITHUB_TOKEN) — line 12. Push rejected:

```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - GITHUB PUSH PROTECTION — Push cannot contain secrets
remote:   - commit: 6e5dfcb... path: profiles/educator/config.yaml:12
```

Facts + correct response:
1. The push was rejected **before storage** — nothing landed on GitHub. But the data **transited GitHub's servers**, so token rotation is the responsible recommendation.
2. The secret existed in the **local commit** — scrub with `git commit --amend` (safe: never pushed) so no trace remains in local history either.
3. Secret-scan the whole staged tree before re-pushing:
   ```bash
   grep -r -n -E "ghp_[A-Za-z0-9]|gho_[A-Za-z0-9]|github_pat_|sk-or-[A-Za-z0-9]|BEGIN [A-Z ]*PRIVATE KEY|password: *[^<\"]" .
   ```
4. Sanitized handoff config = model block only:
   ```yaml
   model:
     provider: openrouter
     default: z-ai/glm-5.2
   _config_version: 33
   ```
   MCP servers are machine-local (tokens, localhost DB URLs); they never belong in a public repo.
5. Read the FULL push error — `git push 2>&1 | tail -3` truncated the violation detail (which file/line). Use `head -40` or full output.

## `hermes skills publish` flow

1. `hermes skills publish --to github --repo oat431/oralita_md <skill_path>` — scans first (execution/obfuscation findings → CAUTION/BLOCKED verdict, harmless for normal skills; `--force` overrides), then creates a **PR** (branch `add-skill-<name>`) — it never pushes to main directly.
2. Published skill lands at `skills/<name>/` (SKILL.md + references/ + scripts/).
3. **Merging:** `POST /repos/<owner>/<repo>/pulls/N/merge` returned **404 even with `repo`-scope token** on the bot-created PR (GET works fine — quirk with tool-created PRs). Workaround:
   ```bash
   git fetch origin pull/1/head:add-skill-oralita-book-sum-obs
   git merge --squash add-skill-oralita-book-sum-obs   # one clean commit
   git reset -q "skills/<name>/scripts/__pycache__"    # drop compiled junk
   git commit -m "Add skill: <name>" && git push
   ```
   Then close the PR (`PATCH pulls/N {"state":"closed"}`) and delete the branch (`DELETE git/refs/heads/add-skill-<name>` — 204).
4. Merged copy is CRLF on Windows — normalize before diffing against LF canonicals.

## OpenRouter model ladder (prices move — fetch, don't hardcode)

```bash
curl -fsSL https://openrouter.ai/api/v1/models | python -c "
import json,sys
for m in json.load(sys.stdin)['data']:
    p=m.get('pricing',{})
    print(m['id'], float(p.get('prompt',0)), float(p.get('completion',0)))
"
```

Tiers observed (2026-08-06): frontier `anthropic/claude-opus-4.8` ($5/$25 per 1M) / `claude-sonnet-5` ($2/$10) / `google/gemini-2.5-pro` ($1/$10); Chinese mid `deepseek/deepseek-v4-pro`, `qwen/qwen3.7-plus`, `z-ai/glm-4.7-flash`, `moonshotai/kimi-k2.5`; near-free `deepseek/deepseek-v4-flash`, `qwen/qwen3.7-flash`, `google/gemini-2.5-flash-lite`. `~`-prefixed IDs track "latest".
