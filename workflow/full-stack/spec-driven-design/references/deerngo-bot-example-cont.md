# Deerngo Bot — Design Session Example (Continued)

> **Continuation of:** `deerngo-bot-example.md`
> **Date:** 2026-07-29 (continued through 2026-07-30)
> **Focus:** Mid-design requirement changes, schema simplification, multi-persona handoff, construction docs

## Mid-Design Requirement Change: 0-Point Viewer Exclusion

**What happened:** After all 6 design docs were produced, the user requested: "for scoreboard, let add another condition, if point is still at 0, just don't fetch to scoreboard."

**How it was handled:**
1. Updated API Spec (022) — added note on scoreboard endpoint: "Only viewers with `total_points > 0` are included"
2. Updated Acceptance Criteria (013) — modified AC-031a, AC-031b, added new AC-031c
3. Documented in MM02 under "Design Changes That Affect Requirements"

**Key insight:** `:deer: point` still returns `total_points: 0` — only the scoreboard filters. Different endpoints, different purposes.

## Schema Simplification: OAuth Tokens Table

**What happened:** User said "just keep the refresh token here" — stripped table to provider, youtube_channel_id, refresh_token only.

**Principle:** Don't persist values that are short-lived, derived, or single-request-scoped.

## Session Corrections (Total: 7)

| # | Correction | Impact | Docs Rewritten |
|---|-----------|--------|:--------------:|
| 1 | Deployment topology (homelab Docker, not Windows PC) | High | 5 |
| 2 | Port assignment (8008/3008, not 8080/3000) | Medium | 4 |
| 3 | Domain (deerngo-viewer-score.panomete.com) | Low | 4 |
| 4 | Fiber v2 → v3 | Low | 4 |
| 5 | 0-point viewer exclusion | Low | 2 |
| 6 | OAuth table simplification | Low | 3 |
| 7 | Construction doc naming (doctype ID, not running number) | Low | 7 |

---

## Construction Docs Phase (2026-07-30)

### Repo-Type Naming Convention

User wanted construction docs tagged by repo type: `<doc_no>_<repo_type>_<doc_name>.md`

**Final layout:** (doctype_id is the same for BE/FE variants)

| File | Repo | Content |
|------|------|---------|
| `031_BE_README.md` | BE | Go backend README |
| `031_FE_README.md` | FE | Next.js frontend README |
| `032_BE_build_scripts.md` | BE | Makefile + Dockerfile |
| `032_FE_build_scripts.md` | FE | package.json scripts + Dockerfile |
| `033_BE_dependency_manifest.md` | BE | go.mod (6 deps) |
| `033_FE_dependency_manifest.md` | FE | package.json (8 deps) |
| `034_SHARED_commit_messages_changelog.md` | Both | Conventional Commits |
| `035_BE_coding_standards.md` | BE | Go coding patterns, Fiber/sqlx conventions |
| `035_FE_coding_standards.md` | FE | Next.js/TypeScript/DaisyUI conventions |
| `036_BE_code_review_records.md` | BE | Go review checklist (20 items) |
| `036_FE_code_review_records.md` | FE | Next.js review checklist (24 items) |

**Naming rule:** Doc number = doctype ID (031=README, 032=Build Scripts, 033=Dep Manifest, 034=Commits, 035=Coding Standards, 036=Code Review). Both BE and FE variants share the same number. User corrected initial mistake of using running numbers (031, 032, 033... → 031, 031, 032, 032...).

**Rules:** Only `03_construction` gets prefix. `01_requirement` and `02_design` stay unsplit. SHARED docs go into both repos at split time.

### SA → QA Handoff (MM03)

`MM03_sa-to-qa_20260730.md` — QA receives ACs, API Spec, Build Scripts, README. Next: QA produces Test Plan (041) + Test Cases (042) → Dev.

### Complete Document Set

| Phase | Count |
|-------|:-----:|
| 01 Requirement | 3 |
| 02 Design | 8 |
| 03 Construction | 11 |
| Meeting Minutes | 3 |
| **Total** | **25** |
