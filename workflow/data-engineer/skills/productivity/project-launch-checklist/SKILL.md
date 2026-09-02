---
name: project-launch-checklist
description: Build and review two-tier production launch checklists — generic + framework-specific. Simplify verbose reference manuals into tickable checklists (ponytail pattern).
---

# Project Launch Checklist — Two-Tier System

Build production-ready launch checklists for any tech stack. Pattern: generic tick-first checklists + framework-specific companions + reference manuals.

## The Two-Tier Pattern

Three file types per domain, living in the same folder:

```
domain-checklist/
├── {Domain} Launch.md           ← Generic. Tick FIRST. ~40-50 items, framework-agnostic.
├── framework-vX-api.md          ← Framework companion. Tick AFTER generic. ~70-85 items.
├── framework-reference.md       ← Reference manual. Deep dives, tutorials. Not ticked.
└── (repeat for each framework)
```

### Tier 1: Generic Launch Checklist

- 6-8 sections, 5-7 one-line items each
- Target: ~45 items total
- Every item: `- [ ] Description → [[vault-note]]` — links to knowledge vault, no explanations embedded
- Zero code examples. Zero version trivia. Zero tutorials.
- Sections: Security → API/State → Database/Data → Resilience/Performance → Observability → Testing → Deployment → (+ Routing for frontend)
- References framework companions: "For {framework} specifics, see [[framework-vX]]"
- References dependent checklists: "Assumes [[Related Launch]] is already done"

### Tier 2: Framework Companion

- "Tick [[{Domain} Launch]] first" in the header
- Framework-specific only: setup, routing, DI, middleware, ORM, testing tools
- ~70-85 items. Still tickable. Still no tutorials.
- Sections mirror generic but with framework details:
  Project Setup → App Structure → Middleware/Routing → Auth → Config/Secrets → DB/State → Testing → Observability → Build/Deploy → Quick Sanity Check
- Quick Sanity Check at the end: 8-10 items verifiable in 2 minutes

### Tier 3: Reference Manuals (Keep Separately)

- Can be long (100-250 lines), detailed, with code examples
- Version-specific (Spring Boot 4.x, Fiber v3, React 19+, Angular 17+)
- Contains tutorials, migration guides, option comparisons
- NOT ticked before launch — consulted when a launch checklist item fails
- Named without "Launch" suffix: `spring-boot-api.md`, `react-js.md`

## Ponytail Filter

When reviewing existing verbose checklists:
1. Strip tutorials, code examples, and version-specific trivia
2. Keep only tick boxes (`- [ ]`) with one-line descriptions
3. Link to vault notes (`→ [[vault-note]]`) instead of embedding explanations
4. Target ~40-50 items per file
5. Keep original as deep reference; create `-v2.md` or rename to `{Domain} Launch.md`

If a checklist item needs > 1 line of explanation, it belongs in the reference manual, not the launch checklist.

## Cross-Referencing Rules

- Generic → Framework: "For {framework} details, see [[framework-vX-api]]"
- Framework → Generic: "Tick [[{Domain} Launch]] first"
- Generic ↔ Vaults: Every item links `→ [[vault-note]]` for deep knowledge

## Common Missing Sections

When reviewing checklists, always check for these commonly missing sections:
- **Routing** (frontend): file-based routing, dynamic routes, navigation guards, 404
- **Form validation**: Zod/schema + server-side re-validation (client UX, server security)
- **OpenAPI/Swagger** (backend): auto-generated docs, annotations
- **Secrets management**: never in source code, Vault/K8s/env vars
- **Graceful shutdown**: drain connections, close DB on SIGTERM

## Auditing Existing Checklists (Domain Specialist Review)

When a user asks to "audit" or "review" an existing checklist for production readiness:

### 1. Read ALL files in the checklist folder first
Checklists are usually a collection: a general file + engine/topic-specific companions. Read every file in the folder before auditing — cross-file consistency matters (shared tier matrix format, shared wikilink targets, consistent section depth).

### 2. Check for mandatory cross-cutting sections
Every production-grade checklist (database, AI, infrastructure) should have these cross-cutting sections. If missing, flag as 🔴 critical:
- **Privacy & Data Protection** — PII inventory, right to erasure, retention, anonymization, data subject requests
- **Data Quality** — validation rules, profiling, drift monitoring, integrity checks
- **Maintenance & Operations** — routine maintenance, vacuum/compaction, statistics freshness, deadlock detection

These are the three sections most commonly missing from checklists written by application engineers — they think about "does it work" not "is the data correct/safe/maintainable over time."

### 3. Engine-specific gap analysis
Each engine has unique operational concerns that a general checklist can't cover. When auditing an engine-specific checklist, verify the engine's signature features are present (not just general DB principles). See `references/database-checklist-audit-domains.md` for the full per-engine gap list (PostgreSQL, MongoDB, Valkey, Elasticsearch, ClickHouse, SQLite, Cassandra, plus AI/LLM-specific sections).

### 4. Tier matrix synchronization
When you add or expand sections in a checklist:
- The **tier scoping matrix table** must grow correspondingly — one row per section
- The **Quick Sanity Check** must add launch-critical items from new sections
- Re-verify: does every section in the checklist body have a row in the tier matrix?

### 5. Honest scope warnings in tier matrices
Add explicit warnings when a technology doesn't fit certain tiers:
- SQLite: "⚠️ Typically not SQLite territory at Tier 5+ — consider migrating to PostgreSQL"
- Cassandra: "⚠️ Overkill below Tier 4 — choose when you need >10K writes/sec or multi-DC active-active"
This prevents the "golden hammer" problem where engineers scale a technology past its design intent.

### 6. Section renumbering
When adding sections to the middle of a checklist, renumber ALL subsequent sections and update ALL internal cross-references (e.g., "see §4"). A full `write_file` rewrite is cleaner than multiple fragile `patch` calls when renumbering changes most of the file.

### 7. Update cross-references in companion files
When a general checklist gains new engine companions (e.g., database.md now references elasticsearch.md), update the general file's header to list all companions. Keep wikilinks consistent across the collection.

### 8. "Last updated" date
Bump the date in the header blockquote on every file you modify.

## Framework Picks (Ponytail Default)

When user asks "what framework for X?" without experience:
- Go → Fiber v3 (simpler than stdlib, lighter than Echo, Axum for Rust fans)
- Rust → Axum (tokio-native, no macros, great docs. NOT Actix/Rocket/Warp for beginners)
- Node → NestJS (opinionated, DI, TypeScript-first, Express/Fastify)
- Frontend state → TanStack Query for server state, signals/stores for client state. No Redux.
