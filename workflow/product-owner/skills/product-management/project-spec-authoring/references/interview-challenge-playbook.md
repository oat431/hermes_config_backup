# Interview Challenge Playbook — Worked Example

Worked example from the SevenSolution backend challenge (2026-08). Pattern reference for future written-source spec packages on assessment/interview tasks.

## The Source

7-Solutions backend challenge: Task 1 = Go + MongoDB + JWT user management API (code), Task 2 = lottery search system (design proposal only). Fetched via:

```bash
curl -sL https://raw.githubusercontent.com/7-solutions/backend-challenge/main/README.md
```

(`web_extract` failed with "SearXNG is a search-only backend" — curl on the raw URL was the fix.)

## Review Shape That Worked

1. Verdict up front: "Yes — we can spec this."
2. Requirement → interpretation table (7 challenge bullets → 7 rows).
3. Evaluation criteria framed as "the real acceptance gate".
4. **Bonus synergy analysis** — the decisive move:
   - "Go interfaces for Mongo" → directly enables the *required* "mock Mongo in tests" criterion (one stone, two criteria)
   - "Hexagonal architecture" → the structure that makes interfaces + clean tests look effortless
   - "Docker compose" → reviewer types `docker compose up`, instant credibility
   - "gRPC" → the only heavyweight, so sequence it LAST
5. Proposed doc set table (doc → template → why), then ONE clarify fork.

## The One Clarify Fork

Bonus scope, presets:
- Full send — all 6 (recommended)
- All except gRPC
- Foundation trio — Docker + interfaces + hexagonal
- Minimal

gRPC-or-not was the only question that touched 5+ docs (stories, ACs, API spec, architecture, test plan). Everything else became assumptions.

## Doc Set Delivered (10 files)

| File | Content highlights |
|------|--------------------|
| `000_spec_index.md` | Doc map, reading order, **12 baseline assumptions (A1–A12)**, status checklist |
| `01_requirement/011_business_objective.md` | Eval criteria → 5 objectives (OBJ-01..05), KPI gates as binary checklists, risk table (gRPC-scope-creep first) |
| `01_requirement/012_user_stories.md` | 11 INVEST stories, 4 epics, points, sequencing E-01→E-04 |
| `01_requirement/013_acceptance_criteria.md` | 46 GWT ACs, FR-001..FR-011, AC IDs → TC IDs |
| `01_requirement/015_definition_of_done.md` | Submission DoD: 7 functional + 7 quality gates incl. all 6 bonuses |
| `02_design/022_API_specification.md` | REST contract + gRPC proto block + error envelope + curl/grpcurl samples |
| `02_design/023_database_schema_DDL.md` | Mongo: `users` collection, `ux_users_email` unique index (programmatic creation), repo ops table |
| `02_design/025_software_architecture_document.md` | Hexagonal, full package tree, component table, 7 ADRs, mermaid flowchart |
| `03_construction/031_README_developer_guide.md` | Deliverable README (fenced `## README (repo)` copy-verbatim section) + JWT guide + samples + assumptions |
| `04_testing/041_test_plan.md` | Hand-written fake repo (no mock lib), ≥80% coverage, TC-001..015 ↔ AC trace, compose smoke script |

## Assumption Set That Was Baked In (A1–A12, condensed)

- Go 1.22+ stdlib router, zero HTTP frameworks (idiomatic, reviewer-friendly)
- Official mongo-driver, golang-jwt/v5 (HS256, secret ≥32B fail-fast), bcrypt cost 10
- `log/slog` structured logging (middleware + worker share it)
- Register (public) and Create User (JWT) both exist, sharing one `CreateUser` use case — challenge lists both bullets
- No role model / no ownership checks (noted as production hardening) — challenge specifies none
- `PUT` = partial update of name/email only; password immutable there
- List = all users, no pagination, `count` meta
- gRPC separate port, JWT metadata interceptor on both RPCs
- Unique email index created programmatically at startup (idempotent)

## Patterns Worth Reusing

- **Sequence guard:** stories/epics put bonus work last; risk register lists "gRPC scope creep" with mitigation "required scope green first" — the bonus can never block submission.
- **Shared-core framing:** REST and gRPC adapters over ONE application layer is the strongest "senior" signal; it also halves implementation.
- **Deliverable as spec artifact:** the repo README is written in 031 before code exists, so "documentation of assumptions" (a stated deliverable) can't be forgotten.
- **ID traceability:** Objective → Story → AC ID (001a…) → TC ID (TC-001…) → DoD rows, all cross-referenced in "Related Documents" footers.
- **Lean sizing:** each doc 100–250 lines, no approvals ceremony, risk register folded into 011 (skipped 071/072), stakeholder analysis skipped (014) — the reviewer never sees the spec; it only needs to drive a great implementation.

## What Comes Next (known follow-ups)

- Task 2 (lottery design proposal) spec: design-doc-only package — likely 025-adjacent doc + performance analysis; user said "after Task 1 ships".
- Implementation reading order given to user: 011 → 025 → 022/023 → 013 → 041.
