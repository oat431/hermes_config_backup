# Checklist Library Architecture (2026-08-05)

Library root: `F:\obsidian_note\swe-knowledge\checklist\`

## Mental model

- **Domain families** — one general checklist + framework/engine variants:
  - `api-checklist/` — api.md + dotnet-api.md, fastapi.md, fiber-v3-api.md, nestjs-api.md, rust-axum-api.md, spring-boot-api.md
  - `web-checklist/` — web.md + react-js.md, vue-js.md, angular.md, svelte.md (+ react-js-v2.md — DO NOT TOUCH)
  - `batch-checklist/` — batch.md + go/nestjs/rust/spring-boot variants
  - `microservice-checklist/` — 11 files incl. spring-boot-* variants
  - `mobile-checklist/` — mobile.md + flutter.md, kotlin-android.md
  - `infra-checklist/` — infra.md, homelab-infra.md, aws-infra.md
  - `database-checklist/` — database.md + postgresql.md, mongodb.md, valkey-redis.md
- **Horizontal checklists** — span all domains, deep references:
  - `release-checklist/release.md` (process) + API Launch.md, Frontend Launch.md, Microservice Launch.md (readiness gates, moved from domain folders)
  - `security-checklist/security.md` (product safety)
  - `qa-checklist/qa.md` (quality strategy)
  - `ai-checklist/ai.md` (AI/LLM applications)
- **Index** — `Overview.md`: "The Checklists" table + "Where the Originals Live" table. Every new file gets a row in both, same session.

## The three-question triangle

- **Launch files** answer "is THIS service ready?" (per-domain quality gates)
- **Horizontals** (security/qa/ai/db) answer "is the SYSTEM secure / tested / AI-sane / data-sane?"
- **release.md** answers "how do we SHIP it?" (process)

## Duplication policy (gate + link)

Overlapping items appear once in detail (the owning checklist) and as 1-line gates elsewhere with `→ [[Owner]]` links. Known overlap map:

| Item | Gate in | Detail in |
|---|---|---|
| SBOM, artifact signing | release.md §1 | security.md §5 |
| SAST/SCA, secret scan | release.md §2 | security.md §9 |
| Secrets per env | release.md §3 | security.md §4 |
| Migrations (backup, expand-contract, downgrade) | release.md §4 | database.md §2/§3, postgresql.md §5 |
| Test gates in CI | release.md §2 | qa.md §6 |
| AI guardrails | security.md §12, api/web §AI | ai.md §6 |

## House style for new files

1. Header: `# <Name> Checklist` + `> ...companion to [[X]]` + `> Last updated: YYYY-MM-DD` (session date)
2. ~10-22 numbered sections with checkbox items, framework/engine-native tools named
3. `## Quick Sanity Check Before Launch` — ~10 concrete verifiable items
4. `## Project Tier Scoping Matrix` — usage legend, 7-tier table, Mermaid "Which Tier Am I?", Applicability table (every section × 7 tiers with ✅/🟡/❌)
5. `## Sources` — cross-links to checklists it complements + official docs

## Verification before reporting done

```bash
for f in <new files>; do grep -c "flowchart TD" "$f"; grep -c "Checklist Applicability by Tier" "$f"; done
```
Both should be ≥ 1 per file. Overview.md rows present for each new file.

## Engine companions (database family)

Created 2026-08-05 to match the homelab stack (PostgreSQL 18, Valkey 9, MongoDB 8, all in Docker on flowero@remote.panomete.com):
- `postgresql.md` — pg_stat_statements, vacuum/XID wraparound, PgBouncer, PITR (pg_dump vs pg_basebackup+WAL vs pgBackRest/barman), Patroni failover, RLS, pgvector
- `mongodb.md` — embed-vs-reference, ESR compound indexes, replica sets (3 members min), shard key discipline (immutable, high-cardinality), FLE, oplog window watch
- `valkey-redis.md` — eviction policies (allkeys-lru vs volatile-lru vs noeviction), key naming, cache-aside + stampede protection, Sentinel vs managed, ACLs, dangerous-command renaming
