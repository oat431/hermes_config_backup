# Backup Repo Layout — hermes_config_backup

Canonical handoff source: `F:\obsidian_note\hermes_config_backup` → GitHub `oat431/hermes_config_backup` (public). `oralita_md` local folder is STALE legacy — no longer the backup home.

## Top-level structure

```
hermes_config_backup/
├── Hermes-Setup-Install.md      ← the runbook (update when setup changes)
├── README.md
├── soul-collection/             ← profile souls + main soul + registry (live dir is the source of truth for counts)
│   ├── hermes-main-soul.md
│   ├── hermes-main-soul-v1.md
│   ├── profile-registry.md      ← routing table + re-install manifest
│   ├── AI-SDLC/                 ← engineering souls (data-engineer, devops, full-stack,
│   │                              llmops, product-owner, qa, security-engineer, ui-ux…)
│   ├── Life Styles/             ← lifestyle souls (audiophile, book-summarizer, career-coach,
│   │                              deck, educator, financial-advisor, gym, journey-writer…)
│   └── _archive/                ← dated pre-overwrite soul stashes
└── workflow/
    ├── Overview.md              ← LIVE skills map + restore instructions (counts live here, not in this file)
    ├── archived/                ← consolidated/old skills (full-stack-monorepo, homelab-setup…)
    ├── hermes-main-profile/     ← main-profile skills (flat skill dirs)
    ├── shared-skills/           ← cross-profile dedup layer (divergent variants stay per-profile)
    └── <profile-name>/          ← per-profile custom skills (flat skill dirs — see shallow rule)
        └── <skill>/             ← SKILL.md + references/ scripts/ templates/
```

## User's preferred organization (asked explicitly)

- **Main profile skills** live under `workflow/hermes-main-profile/` — NOT flat at workflow root.
- **Each profile's skills** get their own top-level folder `workflow/<profile-name>/` — NOT a nested `profiles/` wrapper.
- Empty profile folders (no custom skills) are omitted entirely.
- **Shallow rule (hard):** every entry is a skill dir directly under its folder — never copy a live `skills/` tree wholesale. A deep `workflow/<profile>/skills/...` copy swallows ~90–118 preloaded skills per profile (clone bloat; Hermes ships those anyway) and buried real user skills have been lost to purges before. Rescue orphans by author + bundle-hash classification BEFORE any purge.

## What is / isn't backed up

| Content | Backed up? | Where |
|---|---|---|
| Profile souls | ✅ hash-synced | `soul-collection/<category>/` |
| Main skills | ✅ | `workflow/hermes-main-profile/` |
| Shared universal skills | ✅ | `workflow/shared-skills/` |
| Profile-custom skills | ✅ | `workflow/<profile>/` |
| Community/bundled/preloaded skills | ❌ reinstallable | skills.sh / bundled |
| financial-advisor soul | ⚠️ gitignored | exists locally, not committed (private) |
| config.yaml / .env | ❌ NEVER | live tokens |

**Author gate:** back up only user-created skills (author: Panomete / OraMesLita / profile persona / curator). Hash-check candidates against the bundled tree at `$HERMES_HOME/hermes-agent/skills/` — name-matching alone misses renamed or re-grouped copies. Per-profile skill counts and names: `workflow/Overview.md` (updated every sync; don't duplicate them here).

## Sync procedure (source machine → backup repo)

1. **Recon + classify:** walk `$HERMES_HOME/skills/` (main) and `$HERMES_HOME/profiles/<name>/skills/` (per-profile) for SKILL.md dirs. Profile-custom = in profile but NOT in main skills set. Apply the author gate (above) — preloaded/community copies never enter the backup. If a deep `skills/` tree already exists in the backup, rescue user-created orphans out of it first (author + bundle-hash), then delete the tree.
2. **Souls:** hash-verify each live `profiles/<name>/SOUL.md` against `soul-collection/` copy (md5 match = synced). Normalize CRLF before concluding a diff is real. Update backup if content genuinely differs.
3. **Copy skills (shallow only):** copy each classified skill dir → `workflow/hermes-main-profile/<skill>/` or `workflow/<profile>/<skill>/` (or `workflow/shared-skills/<skill>/` after hash-dedup). Preserve references/ scripts/ templates/ subdirs inside the skill dir. NEVER `copytree` a whole `skills/` directory.
4. **Secret scan before commit:** `grep -rE 'ghp_|sk-[A-Za-z0-9]{20,}|API_KEY\s*=\s*\S' workflow/ soul-collection/` — must return nothing (token placeholders in examples are fine, real tokens are not).
5. **Update Overview.md** — skills map, counts, restore instructions.
6. Git: stage (rename detection handles moved dirs), commit, push. Never commit `config.yaml` or `.env`.

## Restore (target machine)

```bash
# Main skills
cp -r F:/obsidian_note/hermes_config_backup/workflow/hermes-main-profile/* ~/AppData/Local/hermes/skills/
# Per-profile skills (for each profile <name>)
cp -r F:/obsidian_note/hermes_config_backup/workflow/<name>/* ~/AppData/Local/hermes/profiles/<name>/skills/
# Souls
# hermes-main-soul.md → $HERMES_HOME/SOUL.md ; <name>-soul.md → profiles/<name>/SOUL.md
# Config: each profile needs own mcp_servers block + _config_version (see runbook)
# MCP extra: everyfile bridge script lives at $HERMES_HOME/everyfile_mcp_server.py
# (not in the backup repo — rebuild from the mcp-server-patterns skill template)
```

## MCP servers in the fleet

Standard set on all profiles + main:
- `github` — `@modelcontextprotocol/server-github`
- `postgres` — `@modelcontextprotocol/server-postgres`
- `drawio` — `@drawio/mcp`
- `filesystem` — `@modelcontextprotocol/server-filesystem` (F:\projects, F:\obsidian_note, ...)
- `searxng` — `mcp-searxng` (homelab `http://100.73.143.25:7004`)
- `everyfile` — custom Python bridge to VoidTools Everything (see `mcp-server-patterns` skill)

ui-ux additionally: `penpot` MCP.
