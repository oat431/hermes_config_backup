# Backup Repo Layout — hermes_config_backup (verified 2026-08-24)

Canonical handoff source: `F:\obsidian_note\hermes_config_backup` → GitHub `oat431/hermes_config_backup` (public). `oralita_md` local folder is STALE legacy — no longer the backup home.

## Top-level structure

```
hermes_config_backup/
├── Hermes-Setup-Install.md      ← the runbook (update when setup changes)
├── README.md
├── soul-collection/             ← 14 profile souls + main soul + registry
│   ├── hermes-main-soul.md
│   ├── hermes-main-soul-v1.md
│   ├── profile-registry.md      ← routing table + re-install manifest
│   ├── AI-SDLC/                 ← data-engineer, devops, full-stack, product-owner,
│   │                              qa, security-engineer, ui-ux souls
│   └── Life Styles/             ← book-summarizer, career-coach, deck, educator,
│                                  financial-advisor, gym, journey-writer souls
└── workflow/
    ├── Overview.md              ← skills map + restore instructions
    ├── archived/                ← consolidated/old skills (full-stack-monorepo, homelab-setup...)
    ├── hermes-main-profile/     ← 22 main-profile skills (flat skill dirs)
    └── <profile-name>/          ← per-profile custom skills (11 profiles have them)
        └── <skill>/             ← SKILL.md + references/ scripts/ templates/
```

## User's preferred organization (asked explicitly 2026-08-24)

- **Main profile skills** live under `workflow/hermes-main-profile/` — NOT flat at workflow root.
- **Each profile's skills** get their own top-level folder `workflow/<profile-name>/` — NOT a nested `profiles/` wrapper.
- Empty profile folders (no custom skills) are omitted entirely (book-summarizer, data-engineer, financial-advisor have none).

## What is / isn't backed up

| Content | Backed up? | Where |
|---|---|---|
| Profile souls | ✅ hash-synced | `soul-collection/<category>/` |
| Main skills | ✅ | `workflow/hermes-main-profile/` |
| Profile-custom skills | ✅ | `workflow/<profile>/` (58 total) |
| Community/bundled skills | ❌ reinstallable | skills.sh / bundled |
| financial-advisor soul | ⚠️ gitignored | exists locally, not committed (private) |
| config.yaml / .env | ❌ NEVER | live tokens |

## Profile custom-skill inventory (2026-08-24)

| Profile | Skills |
|---|---|
| product-owner (12) | po-requirements-elicitation, go-hexagonal-api, go-backend-api, go-backend-service, go-fiber-backend-development, spec-document-elicitation, grill-me-requirements, requirements-to-backlog, project-spec-authoring, knowledge-base-quality-audit, evidence-based-document-audit, privacy-regulatory-research |
| full-stack (11) | go-fiber-api-server, go-background-scheduler-api-poller, react-vite-spa, spec-driven-design, full-stack-repository-bootstrap, construction-docs, checklist-review, github-pr-qa-followup, interview-prep-coaching, interview-answer-cards, web-research |
| educator (10) | curriculum-vault-authoring, educational-content-authoring, career-guidance-authoring, career-path-overlay-authoring, educational-notes-bilingual, multilingual-note-conversion, obsidian-note-authoring, obsidian-vault-restructuring, exercise-authoring, iso-standards-compliance-review |
| devops (6) | homelab-infra-audit, homelab-microservice-deployment, keycloak-deployment, keycloak-docker, devops-doc-authoring, release-readiness-audit |
| qa (6) | spec-driven-qa-authoring, spec-driven-code-review, github-pr-follow-up-review, checklist-audit, knowledge-vault-audit, obsidian-vault-audit |
| journey-writer (3) | campaign-journal, wiki-lore-research, writing-practice-audit |
| ui-ux (3) | penpot-mcp, project-spec-docs, nginx-streaming-proxy |
| career-coach (2) | career-artifact-prep, career-coaching |
| gym (2) | fitness-coaching, weekly-training-review |
| security-engineer (2) | security-review-pass, tor-darkweb-exploration |
| deck (1) | presentation-design |

## Sync procedure (source machine → backup repo)

1. **Recon:** walk `$HERMES_HOME/skills/` (main) and `$HERMES_HOME/profiles/<name>/skills/` (per-profile) for SKILL.md dirs. Profile-custom = in profile but NOT in main skills set.
2. **Souls:** hash-verify each live `profiles/<name>/SOUL.md` against `soul-collection/` copy (md5 match = synced). Update backup if differs.
3. **Copy skills:** `shutil.copytree` main skills → `workflow/hermes-main-profile/`; profile skills → `workflow/<profile>/`. Preserve references/ scripts/ templates/ subdirs.
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
```
