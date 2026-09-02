# External Project Workflow: Deerngo Bot Case Study

> **Project:** Deerngo Bot — Viewer Relationship Management (VRM)
> **Type:** External project (not part of Panomete platform)
> **Date:** 2026-07-29 → 2026-07-30

---

## Workflow Summary

### Session 1: PO → Requirements (2026-07-29)
1. Stakeholder described the project (YouTube live streaming bot)
2. PO delegated research on unfamiliar tech (streamer.bot, EasyDonate) in background
3. PO grilled stakeholder (10 questions via `clarify()`)
4. PO wrote 3 spec documents:
   - `011_business_objective.md` — 4 SMART objectives
   - `012_user_stories.md` — 10 stories, 34 points
   - `013_acceptance_criteria.md` — 46 BDD criteria
5. PO updated overview document (`external_overview/Deer Ngo Bot.md`)

### Session 1 (continued): Architecture Change
1. Stakeholder raised concern: "subscribers who subscribe outside live streaming time"
2. PO proposed hybrid approach (YouTube API polling + streamer.bot)
3. PO updated all 3 spec documents + overview
4. New story added: US-003 (YouTube API Polling Scheduler)
5. Updated counts: 10→11 stories, 34→41 points, 46→53 ACs

### Session 1 (continued): PO → Designer Handoff
1. PO created meeting minute: `MM01_po-to-designer_20260729.md`
2. Included: what PO produced, architecture decisions, integration points, what designer must deliver

### Session 2: Designer → Multi-Persona Handoff (2026-07-29)
1. Designer produced 6 design documents (021→029)
2. Designer made 5 decisions (DEC-D01→DEC-D05)
3. Designer changed deployment topology (local Windows → homelab Docker)
4. Designer added AC-031c for 0-point exclusion
5. PO reviewed MM02, confirmed decisions with stakeholder
6. PO fixed AC summary table inconsistency (designer added AC but forgot to update counts)

### Session 3: QA → PO Spec Gap Review (2026-07-30)
1. QA produced test plan, test cases (59), defect report (6 spec gaps)
2. QA identified 3 blocking PO decisions (DEF-S001, DEF-S004, DEF-S005)
3. PO grilled stakeholder on each decision
4. PO updated meeting minute decision table
5. PO updated AC document (AC-001f rewritten, summary counts fixed)
6. PO updated overview document counts

### Session 4: Implementation Plan (2026-07-30)
1. PO reviewed QA test cases (59 total, 3 new for rate limiting/HMAC)
2. PO created implementation plan: `external_plan/phase1-deerngo-bot-mvp.md`
3. Included: 3 sprints, 28 tasks, ~66h, repo/branch strategy, DevOps tasks

### Session 5: Document Review & Cleanup (2026-07-30)
1. PO reviewed new devops (051→054) and security (061→062) documents
2. PO found conflict: coverage report (045) had stale AC counts (31🔴/23🟡 → 32🔴/22🟡)
3. PO fixed coverage report: US-001 row (4🔴/2🟡 → 5🔴/1🟡), total counts
4. PO moved meeting minutes from `external_spec/meeting_minute/` to `external_spec/deerngo_bot/07_pm/`
5. Final structure: 37 documents across 7 categories

---

## Key Decisions Made

| ID | Decision | Choice | Rationale |
|----|----------|--------|-----------|
| DEC-001 | Backend language | Go | Lightweight, stakeholder comfortable |
| DEC-002 | Database | PostgreSQL 18 | Existing homelab |
| DEC-003 | Frontend | React/Next.js | Nice UI for scoreboard |
| DEC-004 | Deployment | Homelab Docker | Changed from local Windows PC |
| DEC-005 | Subscriber capture | Hybrid (API polling + streamer.bot) | 24/7 coverage |
| DEC-006 | Name matching | Fuzzy (pg_trgm) | Flexible matching |
| DEC-007 | Webhook verification | HMAC-SHA256 | Standard, secure |
| DEF-S001 | display_name | Required (no fallback) | API spec strict |
| DEF-S004 | Rate limiting | Add ACs in Phase 1 | QA to write test cases |
| DEF-S005 | HMAC key rotation | Document now | Security ops readiness |

---

## Document Counts (Final)

| Metric | Value |
|--------|-------|
| User Stories | 11 |
| Story Points | 41 |
| Acceptance Criteria | 54 (32🔴, 22🟡) |
| Test Cases | 59 |
| Design Documents | 8 (021→029) |
| Construction Documents | 11 (BE + FE) |
| DevOps Documents | 4 (051→054) |
| Security Documents | 2 (061→062) |
| Testing Documents | 5 (041→045) |
| Meeting Minutes | 4 (MM01→MM04) |
| Spec Gaps Found | 6 (3 resolved, 3 dev-facing) |
| **Total Documents** | **37** |

---

## Lessons Learned

1. **Hybrid data collection pattern** — When a runtime component (streamer.bot) isn't always online, propose a hybrid approach: always-on polling + real-time push when available
2. **Designer changes require PO confirmation** — Deployment topology changed from local Windows to homelab Docker. PO must confirm with stakeholder before updating specs.
3. **AC count consistency across ALL documents** — When anyone adds/changes ACs, verify counts in FOUR places: (1) AC summary table, (2) traceability table, (3) coverage report (045), (4) overview document. The coverage report is the most commonly missed one.
4. **Update existing meeting minutes** — When PO makes decisions on QA meeting minute, update the existing file. Do not create a new one.
5. **Overview document is the source of truth** — Update it after every significant spec change. Stakeholders read it first.
6. **Meeting minutes belong inside the project folder** — `external_spec/<project>/07_pm/`, NOT in a separate `meeting_minute/` folder. Keeps the project self-contained.
7. **Confirm repo count/names before writing implementation plans** — User may say "3 repos" then correct to "2 repos". Always use `clarify()` to confirm before writing.
8. **Coverage report gets stale fast** — The QA coverage report (045) has per-user-story AC counts that break when ACs change priority. Add it to the consistency checklist.
