---
name: project-launch-checklist
description: Build, review, and audit vault checklists — two-tier launch checklists (generic + framework-specific) and master+technique-split domain checklists (security, QA, AI). Includes tier scoping matrices, audit workflow, and OWASP gap-pattern reference.
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
- **IDOR/BOLA** (security): object-level authorization — OWASP API #1, commonly missing
- **XXE** (security): XML parser DTD/external entity disabling
- **Immutable backups** (security/data): WORM/object-lock for ransomware resilience

## Pattern 3: Master Overview + Technique Deep-Dive Split

Beyond the two-tier launch pattern above, the vault has a **third checklist pattern** for cross-cutting domain checklists (security, QA, AI). This is NOT a launch checklist — it's a system-wide domain reference.

```
domain-checklist/
├── {domain}.md                   ← Master: all sections in one file, tier matrix, sanity check
├── technique-a.md                ← Deep dive on one technique/tool
├── technique-b.md                ← Deep dive on another
└── ...
```

### When to use this pattern

- **Domain is cross-cutting** (security, QA, AI) — applies to all stacks, not one framework
- **Multiple techniques/tools** within the domain (SAST, DAST, pentest for security; go-test, playwright, k6 for QA)
- **Each technique warrants its own deep dive** (tool setup, CI config, triage process, anti-patterns)
- Existing sibling checklist folders already use this pattern (check `qa-checklist/`, `ai-checklist/`)

### Master file structure

```
# {Domain} Checklist
> Complements [[Release]], [[Other Launch]]...
> Last updated: YYYY-MM-DD
---
## 1. Section Name
> **Deep dive:** [[technique-file]] — what it covers in one line.
- [ ] **Item** — one-line description → [[vault-note]]
## 2. ...
---
## Quick Sanity Check Before Launch
- [ ] top ~15 items verifiable quickly
---
## Project Tier Scoping Matrix
> Pick your tier, focus on ✅/🟡 sections, skip ❌
### Tier Descriptions (table)
### Which Tier Am I? (mermaid flowchart)
### Checklist Applicability by Tier (table: section × tier)
---
## Sources
- Technique deep dives list with one-line descriptions
```

### Technique file structure

```
# {Technique} Checklist
> What it is, what it complements → [[master]]
> Last updated: YYYY-MM-DD
---
## 1. What & Why (core concept, what it's good/bad at)
## 2. Tool Selection (table by stack/language)
## 3-N. Setup & Config (install, scan, CI integration with code examples)
## N+1. Triage & Tuning (false positives, quality gates, baselines)
## N+2. Anti-Patterns to Avoid
---
## Quick Sanity Check
## Sources (master link, vault notes, tools, standards)
```

### PITFALL: Defaulting to one-file when the pattern is multi-file

Before writing a domain checklist, **always check sibling checklist folders first** (`ls checklist/*/`). If `qa-checklist/` has `qa.md` + `go-test.md` + `playwright.md`, the established pattern is master + technique split. Don't cram everything into one monolithic file — the user will redirect you to match the existing pattern.

## Tier Scoping Matrix (Proportionality Pattern)

Every domain master checklist should include a tier scoping matrix so the comprehensive checklist remains proportionate. The user's philosophy: **the checklist should be complete; the tier matrix makes it proportionate.** Never simplify the checklist itself — instead, add a matrix that tells the reader what to skip.

### Required components

1. **Tier descriptions table** — 7 tiers from POC to Mission-Critical, with team size / users / lifespan
2. **"Which Tier Am I?" flowchart** — Mermaid decision tree narrowing to the right tier
3. **Applicability matrix** — section × tier table with ✅ (required) / 🟡 (recommended) / ❌ (skip)

### Legend

`✅ Required · 🟡 Recommended / partial · ❌ Skip`

## Domain Checklist Audit Workflow

When auditing or updating an existing domain checklist:

1. **Read the checklist** — full read, understand structure and existing sections
2. **Check sibling folders** — `ls checklist/*/` to see how other domain checklists are structured (master+technique split? tier matrix?)
3. **Verify fresh references via searxng MCP** — for fast-moving domains (OWASP, AI security), pull the current version of frameworks/standards before gap analysis. Don't rely on cached knowledge for taxonomies that change yearly
4. **Gap analysis** — compare checklist coverage against: OWASP Top 10 variants, sibling checklist patterns, vault note coverage
5. **Write updates** — patch the master file with new items, section headers, and `→ [[technique]]` deep-dive links
6. **Split into technique files** — if the domain has multiple tools/techniques, create standalone deep-dive files matching the sibling pattern
7. **Verify all wikilinks resolve** — run a shell loop checking every `[[wikilink]]` target exists in the vault. Broken links are a known user pain point
8. **Update Sources section** — list all technique files as companion references with one-line descriptions

## Reference Files

- [`references/owasp-security-references.md`](references/owasp-security-references.md) — OWASP API Top 10 (2023) + LLM Top 10 (2025) snapshot with gap patterns found during security checklist audit. Verify currency via searxng before relying on it.

## Framework Picks (Ponytail Default)

When user asks "what framework for X?" without experience:
- Go → Fiber v3 (simpler than stdlib, lighter than Echo, Axum for Rust fans)
- Rust → Axum (tokio-native, no macros, great docs. NOT Actix/Rocket/Warp for beginners)
- Node → NestJS (opinionated, DI, TypeScript-first, Express/Fastify)
- Frontend state → TanStack Query for server state, signals/stores for client state. No Redux.
