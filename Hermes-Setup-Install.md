---
title: "Hermes Setup Install"
tags: [hermes, setup, guide, xiaomi, mimo, searxng, windows]
---

# Hermes Setup Install — Step-by-Step

> **Purpose:** Replicate Panomete's Hermes setup on any Windows computer — a new machine (old one broke) or a friend's machine.
> **Target spec:** Hermes desktop app + **QwenCloud Token Plan** (Alibaba) as the single provider for the main agent + all 14 specialist profiles + searxng (homelab via Tailscale, or local Docker) + user skills + main soul + soul-collection.
> **Handoff source:** GitHub repo `github.com/oat431/hermes_config_backup` (public — souls in `soul-collection/`, user skills in `workflow/`). USB copy is the offline fallback.
> **Target paths:** `%LOCALAPPDATA%\hermes` (HERMES_HOME on Windows). `~/.hermes` does **not** exist on Windows — always resolve via `$env:LOCALAPPDATA\hermes`.

```mermaid
flowchart LR
    A[Step 0: Push backup repo<br/>on your machine] --> B[Step 1: Install Hermes<br/>PowerShell one-liner]
    B --> C[Step 2: Model provider<br/>QwenCloud Token Plan]
    C --> D[Step 3: searxng<br/>Tailscale or local Docker]
    D --> E[Step 4: Wire searxng into Hermes]
    E --> F[Step 5: User skills<br/>from workflow/]
    F --> G[Step 6: Main soul]
    G --> H[Step 7: Profiles<br/>from soul-collection/]
    H --> I[Step 8: MCP servers]
    I --> J[Step 9: Desktop + verify]
```

---

## Current setup at a glance (what you're replicating)

| Layer | What | Where it lives |
|---|---|---|
| Main model | `mimo-v2.6-pro` via **xiaomi** | main `config.yaml` + `XIAOMI_API_KEY` in `.env` |
| Profile models | `mimo-v2.6-pro` via **xiaomi** — same model + provider for all profiles | each profile's `config.yaml` + `XIAOMI_API_KEY` in `.env` |
| Search | searxng backend, homelab instance `http://100.73.143.25:7004` (Tailscale) or local Docker | `SEARXNG_URL` in `.env` |
| MCP | github, postgres, drawio, filesystem, searxng | `mcp_servers` in main + every profile `config.yaml` |
| Skills | user skills (+ `archived/` old iterations) | `workflow/` in this repo → `%LOCALAPPDATA%\hermes\skills\` |
| Souls | main soul + 14 profile souls + registry | `soul-collection/` in this repo |
| Memory | limits 4000 (memory) / 2500 (user profile) chars | main `config.yaml` |

**Model assignment:** every profile + the main agent run `mimo-v2.6-pro` via `xiaomi` (single uniform default). Xiaomi MiMo v2.6 models:

| Model | Good for |
|---|---|
| `mimo-v2.6-pro` | **default** — capable all-rounder |
| `mimo-v2.6-flash` | fast, lightweight tasks |
| `mimo-v2.6-pro-ultraspeed` | ultra-low latency |
| `mimo-v2.5-pro` | previous-gen pro |

---

## Step 0 — Push the backup repo (on YOUR machine, before going)

The whole handoff is the GitHub repo. Make sure it's current:

```bash
cd 'F:/obsidian_note/hermes_config_backup'
git add -A
git commit -m "chore: sync souls/skills/guide"
git push
```

- What lives where: `soul-collection/` (souls + `profile-registry.md`), `workflow/` (user skills), `Hermes-Setup-Install.md` (this guide).
- ⚠️ Repo is **public** — anything pushed is world-readable. The `.gitignore` already excludes the **financial-advisor soul** (personal finance details). Keep it that way; carry that one on USB if needed.
- **Offline fallback (USB):** zip the repo (or copy `soul-collection/` + `workflow/`) — steps 5–7 then read from USB instead of the internet.

---

## Step 1 — Install Hermes (on the target)

Open **PowerShell** (Win+X → Terminal) and run:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

What the installer does (no admin needed):
- Installs uv, Python 3.11, Node.js, ripgrep, ffmpeg, and a **portable Git Bash** (MinGit unpacked to `%LOCALAPPDATA%\hermes\git` — isolated from any system Git)
- Everything lands in `%LOCALAPPDATA%\hermes`

Verify:

```powershell
hermes --version
```

> ⚠️ **Windows Defender / antivirus flags `uv.exe`?** False positive on Astral's uv (unsigned Rust binary). Whitelist the folder, not the hash: PowerShell as Admin → `Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\hermes\bin"`.

---

## Step 2 — Model provider (Xiaomi MiMo v2.6, single provider)

Everything — the main agent and all 16 profiles — runs on **Xiaomi MiMo v2.6**, `provider: xiaomi`. One key covers every agent.

```bash
hermes config set model.provider xiaomi
hermes config set model.default mimo-v2.6-pro
```

Key goes into `%LOCALAPPDATA%\hermes\.env` as:

```ini
XIAOMI_API_KEY=<your-xiaomi-api-key>
```

> ⚠️ **Xiaomi API key** is stored in `auth.json` (credential_pool) or `.env` as `XIAOMI_API_KEY`. The provider resolves its own base_url (`https://api.xiaomimimo.com/v1`) — no per-profile `.env` needed for xiaomi.

Per-profile config block (identical for all 14):

```yaml
model:
  default: mimo-v2.6-pro
  provider: xiaomi
```

> ⚠️ **Protocol rule:** `provider` decides which API protocol Hermes speaks; `base_url` decides where requests go. Don't leave a stale `base_url` pointing at z.ai / DeepSeek / OpenRouter / alibaba in a profile that now uses `xiaomi` — you'll get protocol errors. If `base_url` is unset in `config.yaml`, the provider resolves its own default endpoint (recommended — don't set `base_url` per-profile).

**Model quick-picks (Xiaomi MiMo v2.6):**

| Model | Good for |
|---|---|
| `mimo-v2.6-pro` | **default** — capable all-rounder |
| `mimo-v2.6-flash` | fast, lightweight tasks |
| `mimo-v2.6-pro-ultraspeed` | ultra-low latency |
| `mimo-v2.5-pro` | previous-gen pro |

Switch anytime: `hermes -m <model>` per session, or `hermes config set model.default <model>` + `/reset` globally.

---

## Step 3 — searxng (two options)

### Option A — Homelab instance via Tailscale (zero install)

If the new machine joins your Tailnet (IP `100.73.143.25`, port `7004`): **no Docker needed**. The instance is already running. Skip to Step 4 and use:

```ini
SEARXNG_URL=http://100.73.143.25:7004
```

### Option B — Local Docker (works offline from the homelab)

**3.1 Install Docker Desktop** (free, WSL2 backend):

```powershell
winget install --id Docker.DockerDesktop
```

- Reboot if asked; start Docker Desktop and wait for the whale icon to go steady.
- No WSL2 yet? Docker Desktop offers to install it during first run.

**3.2 Create the searxng folder** (`C:\searxng` — or anywhere):

```powershell
mkdir C:\searxng\core-config
```

**3.3 `C:\searxng\docker-compose.yml`** (official template, `:Z` mount flag removed — SELinux-only, breaks on Windows):

```yaml
name: searxng

services:
  core:
    container_name: searxng-core
    image: docker.io/searxng/searxng:${SEARXNG_VERSION:-latest}
    restart: always
    ports:
      - ${SEARXNG_HOST:+${SEARXNG_HOST}:}${SEARXNG_PORT:-7004}:${SEARXNG_PORT:-7004}
    env_file: ./.env
    volumes:
      - ./core-config/:/etc/searxng/
      - core-data:/var/cache/searxng/

  valkey:
    container_name: searxng-valkey
    image: docker.io/valkey/valkey:9-alpine
    command: valkey-server --save 30 1 --loglevel warning
    restart: always
    volumes:
      - valkey-data:/data/

volumes:
  core-data:
  valkey-data:
```

**3.4 `C:\searxng\.env`**:

```ini
SEARXNG_PORT=7004
```

**3.5 `C:\searxng\core-config\settings.yml`** — the **JSON format is required by Hermes**. Minimal override (searxng deep-merges it over defaults):

```yaml
server:
  secret_key: "paste-any-long-random-string-here"

search:
  formats:
    - html
    - json
```

**3.6 Start it:**

```powershell
cd C:\searxng
docker compose up -d
```

**3.7 Verify the JSON API works:**

```powershell
curl "http://127.0.0.1:7004/search?q=test&format=json"
```

Expect a JSON response with `results`. (A 400 `invalid format` = settings.yml not picked up — `docker compose restart`.)

---

## Step 4 — Wire searxng into Hermes

```powershell
hermes config set web.backend searxng
```

Then add to `%LOCALAPPDATA%\hermes\.env` (homelab IP if on Tailscale, `127.0.0.1` if local Docker):

```ini
SEARXNG_URL=http://100.73.143.25:7004
```

Verify — ask Hermes: *"search the web for 'what is hermes agent'"* — it should return live results. (No key needed: searxng is the keyless search backend; `web_extract` still needs a keyed provider like tavily/firecrawl — set `web.extract_backend` if page fetches matter.)

---

## Step 5 — Install user skills (from `workflow/`)

21 skills + `archived/` (old iterations — skip unless you want them back). Fastest way on a new machine: clone the repo and **folder-copy is the install**:

```powershell
git clone https://github.com/oat431/hermes_config_backup.git D:\hermes-backup

# copy each skill folder into the skills tree, e.g.:
Copy-Item -Recurse D:\hermes-backup\workflow\oralita-book-sum-obs $env:LOCALAPPDATA\hermes\skills\personal-agents-skill\
Copy-Item -Recurse D:\hermes-backup\workflow\go-fiber-api $env:LOCALAPPDATA\hermes\skills\software-development\
```

Or one-by-one via URL (no clone needed):

```powershell
hermes skills install "https://raw.githubusercontent.com/oat431/hermes_config_backup/main/workflow/oralita-book-sum-obs/SKILL.md"
```

> Category folder is cosmetic grouping — Hermes indexes every `SKILL.md` it finds under `skills\`. Put each skill wherever it fits; just keep one skill per folder.

Current user skill set (as of 2026-08-22):

| Category | Skills |
|---|---|
| Book/vault | oralita-book-sum-obs ⭐, bok-essential-documents, vault-completion, obsidian-vault-filling, obsidian-vault-builder, obsidian-vault-maintenance |
| Docs/spec | document_template-authoring, md-project-document_templates, project-document_templates, project-launch-checklist, software-specification, skill-library-maintenance |
| Decks | pptx-deck-series, presentation-from-vault |
| Dev | go-fiber-api, mcp-server-patterns, hermes-profile-setup, full-stack-monorepo |
| Homelab | homelab-infra-setup, homelab-infrastructure, homelab-server-setup |

⭐ = protected skill (`oralita-book-sum-obs`) — never delete.

Verify:

```powershell
hermes skills list
```

> ⚠️ Community skill packs (productivity, creative, github, mlops, …) are **not** backed up here — they're reinstallable from skills.sh anytime. Only `workflow/` content is yours.

---

## Step 6 — Install the main soul (from repo)

```powershell
# back up the fresh default first
Copy-Item $env:LOCALAPPDATA\hermes\SOUL.md $env:LOCALAPPDATA\hermes\SOUL.md.default
Invoke-WebRequest "https://raw.githubusercontent.com/oat431/hermes_config_backup/main/soul-collection/hermes-main-soul.md" -OutFile $env:LOCALAPPDATA\hermes\SOUL.md
```

This replaces the default persona with OraMesLita (the router + general helper). Restart Hermes to load it.

---

## Step 7 — Install the 14 profiles (from `soul-collection/`)

Souls live in `soul-collection/AI-SDLC/` (dev roles) and `soul-collection/Life Styles/` (life roles). Workflow: copy the soul as the profile's `SOUL.md`, then write a small `config.yaml` (model + MCP block).

```powershell
$H = "$env:LOCALAPPDATA\hermes\profiles"
$S = "D:\hermes-backup\soul-collection"   # from the clone in Step 5

# example: full-stack
mkdir -Force "$H\full-stack"
Copy-Item "$S\AI-SDLC\full-stack-developer-soul.md" "$H\full-stack\SOUL.md"
```

Minimal profile `config.yaml` (this is the whole file — every profile uses the same model):

```yaml
model:
  default: mimo-v2.6-pro
  provider: xiaomi
```

> MCP servers are **per-profile config**, not inherited from the main config — to give a profile MCP, copy the `mcp_servers` block from Step 8 into its `config.yaml` too (that's how the current machine does it: all profiles carry the block).

> ⚠️ `financial-advisor` soul is **gitignored** (private) — copy it from USB/private storage, not the repo.

Repeat for all 14 (soul filename → profile). All use `deepseek-v4-flash-0731` / `alibaba`:

| Profile           | Soul file                                  |
| ----------------- | ------------------------------------------ |
| product-owner*    | `AI-SDLC/product-owner-soul.md`            |
| full-stack        | `AI-SDLC/full-stack-developer-soul.md`     |
| devops            | `AI-SDLC/devops-engineer-soul.md`          |
| qa                | `AI-SDLC/qa-engineer-soul.md`              |
| security-engineer | `AI-SDLC/security-engineer-soul.md`        |
| ui-ux             | `AI-SDLC/ui-ux-designer-soul.md`           |
| data-engineer     | `AI-SDLC/data-engineer-soul.md`            |
| educator          | `Life Styles/educator-soul.md`             |
| book-summarizer   | `Life Styles/book-summarizer-soul.md`      |
| career-coach      | `Life Styles/career-coach-soul.md`         |
| financial-advisor | `Life Styles/financial-advisor-soul.md` 🔒 |
| gym               | `Life Styles/gym-soul.md`                  |
| journey-writer    | `Life Styles/journey-writer-soul.md`       |
| deck*             | `Life Styles/deck-soul.md`                 |

\* = soul exists, profile may not be installed — create only if wanted. 🔒 = private, not in repo.

Check: `hermes profile list`. Full-fidelity alternative: `hermes profile import <profile.tar.gz>`.

---

## Step 8 — MCP servers (5)

Add to main `config.yaml` **and** each profile `config.yaml` that needs them (sanitized template — fill your own values):

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "<your-github-pat>"
    timeout: 60

  postgres:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@host:5432/dbname"]

  drawio:
    command: "npx"
    args: ["-y", "@drawio/mcp"]

  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem",
           "F:\\projects", "F:\\obsidian_note", "C:\\Users\\Admin\\.openclaw\\workspace"]

  searxng:
    command: "npx"
    args: ["-y", "mcp-searxng"]
    env:
      SEARXNG_URL: "http://100.73.143.25:7004"
    timeout: 30
```

> ⚠️ **Never commit live tokens.** The repo copy of any `config.yaml` must stay sanitized (model block only). MCP env lives in the machine-local file.
> ui-ux additionally runs a `penpot` MCP server — keep it there if you use Penpot.

> Requires Node.js/npx (installed by Hermes in Step 1). Changes need an agent restart — no hot-reload.

---

## Step 9 — Desktop app + final verification

```powershell
hermes desktop
```

Checklist (in order):

- [ ] `hermes --version` works
- [ ] `hermes doctor` — no red flags
- [ ] Chat test: *"hello"* — responds via deepseek-v4-flash-0731
- [ ] Profile test: switch to `full-stack`, ask *"what model are you"* — deepseek-v4-flash-0731 via alibaba
- [ ] Search test: *"search the web for X"* — searxng returns live results
- [ ] MCP test: ask any profile to *"list github repos"* — github MCP responds
- [ ] `hermes skills list` — oralita-book-sum-obs present
- [ ] `hermes profile list` — all created profiles present
- [ ] Docker (Option B only): `docker ps` shows `searxng-core` + `searxng-valkey` running

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Antivirus flags `uv.exe` | False positive — whitelist `%LOCALAPPDATA%\hermes\bin` folder (see Step 1) |
| `cat ~/.hermes/...` fails | Windows: HERMES_HOME is `%LOCALAPPDATA%\hermes`, not `~/.hermes` |
| Profile uses wrong model / provider errors | Check the profile's own `config.yaml` — profiles don't inherit the main model block. `provider` and `base_url` must agree; unset `base_url` to let the provider resolve it |
| Profile can't see MCP servers | `mcp_servers` block missing from that profile's `config.yaml` — copy from Step 8, then restart |
| searxng returns `invalid format` | `settings.yml` missing `formats: [html, json]` or not mounted → `docker compose restart` |
| Homelab searxng unreachable | Not on Tailscale (or homelab down) — join the Tailnet or fall back to local Docker (Option B) |
| Port 7004 already in use | Change `SEARXNG_PORT` in `.env` **and** `SEARXNG_URL` in Hermes `.env` |
| `hermes skills install` fails | Check branch is `main` in the URL; check network; retry — or folder-copy from the clone |
| Push blocked: "Push cannot contain secrets" | A `config.yaml` in the push has live MCP credentials. Sanitize — keep the model block, strip `mcp_servers` env values |
| Search works but web page fetch fails | Expected: `web_extract` needs a keyed provider (tavily/firecrawl/exa) — set `web.extract_backend` |
| Memory at capacity warnings | `hermes config set memory.memory_char_limit 4000` + `hermes config set memory.user_char_limit 2500`, then `/reset` |
| Model responds slow | Switch tier: `hermes -m qwen3.8-flash` (fast) or back via `hermes model` |

## Maintenance & backup notes

- **The repo IS the backup.** `git push` after any soul/skill/guide change = offsite backup. Habit: `git add -A && git commit && git push` after sessions that changed skills/souls.
- **Sync pattern (live → repo):** copy changed skill folders from `%LOCALAPPDATA%\hermes\skills\<category>\<skill>\` into `workflow/\<skill>\`; souls from `%LOCALAPPDATA%\hermes\profiles\<name>\SOUL.md` back into `soul-collection\<group>\<name>-soul.md`. Verify with a diff before committing.
- **Community packs are not backed up** — reinstallable from skills.sh. Only `workflow/` is yours.
- **Keys are the owner's responsibility.** `DASHSCOPE_API_KEY`, `DASHSCOPE_BASE_URL`, `GITHUB_TOKEN`… live only in `%LOCALAPPDATA%\hermes\.env` (and each profile's `.env`). Never in chats, logs, or the repo.
- **Profiles aren't repo-backed beyond souls** (decision 2026-08-22): draft in chat, create on Hermes desktop. Souls + this guide are the restore path.
- Update Hermes: `hermes update`. Health check: `hermes doctor`. Computer-use issues: `hermes computer-use doctor`.
- Legacy note: `oat431/oralita_md` was the old handoff repo — its `skills/`+`workflow/`+`soul-collection/` copies are **stale**. `hermes_config_backup` is canonical now.
