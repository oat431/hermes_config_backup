# Soul Level-Up: Career-Path Upgrade

Worked example: `full-stack-developer-soul.md` upgraded mid → senior (2026-08-05), against `F:\obsidian_note\swe-knowledge\career-path\02_Senior_Software_Engineer\`.

## When to Use
User has a career-path vault and asks to upgrade an existing specialist soul ("review both and tell me if we can upgrade").

## Step 1 — Inventory the career path
- Read `<path>\00_overview.md`: capability-areas table, "Signals for Moving Forward", "Evidence to Build", progression mermaid.
- Read every capability-area `00_overview.md` (9 for senior): the mid-vs-senior comparison tables are gold — they state the exact behavior shift to encode.
- Note completion state (senior path was 100% complete, ~60 notes).

## Specialist-path upgrades with a shared Senior SWE foundation

When the target career path is a senior-specialist path whose `entry_from` includes `career-path/02_Senior_Software_Engineer` (for example, SRE/Platform or Quality/Test Engineering), treat the work as a **layered specialization**, not a simple replacement of the senior soul:

1. **Inventory both layers.** Read the specialist path `00_overview.md` plus every capability-area overview. Also read the Senior SWE `00_overview.md` plus its nine capability-area overviews. The specialist path defines the role's primary outcomes; Senior SWE defines the shared engineering operating system.
2. **Make the specialist path primary.** In the soul's Knowledge Base, put the target specialist path first and map every specialist capability to an operating charter. Put Senior SWE second as the foundation, with a compact table mapping each senior capability to how it applies in this specialist role.
3. **Map, do not duplicate.** Include all nine Senior SWE foundation areas in the mapping table when the user asks for the foundation, but only carry specialist-relevant techniques into the detailed Core Techniques section. Do not paste the entire Senior soul verbatim.
4. **Preserve identity; elevate scope.** Keep the existing name, emoji, and useful domain principles. Change the role to the exact senior-specialist title and elevate the mission from task execution to outcome ownership, evidence, team/system improvement, and influence.
5. **Add the senior behavior layer.** Encode problem framing, technical ownership, architecture judgment, delivery/risk management, quality/reliability/security, communication, mentoring, economics, and impact evidence as behaviors that shape specialist decisions — not as a second unrelated job description.
6. **Let the specialist path set priorities.** Derive 🔴/🟡/🟢 documents and execution order from the specialist path's primary outcomes and owned templates. The Senior SWE layer changes *how* decisions are made, not which specialist deliverables are primary.
7. **Show the progression explicitly.** Use a foundation chain such as `Software Engineer → Senior Software Engineer → Specialist Engineer` and state why the shared senior capabilities are prerequisites for the specialist role.

### Specialist upgrade review questions

Before writing, confirm from the career path:

- Does the target path declare `level: senior-specialist`?
- Does `entry_from` include Senior Software Engineer?
- What specialist outcomes distinguish it from a general senior engineer?
- Which Senior SWE capabilities are direct prerequisites, and which are supporting context?
- Which documents prove specialist impact (not just task completion)?

## Step 2 — Gap analysis (the review deliverable)
9-row table, one row per capability area:

| Senior Capability | Old soul coverage | Action |
|---|---|---|
| Technical Ownership | ❌ | New |
| Problem Framing & Requirements | ❌ | New |
| Architecture & Design Judgment | 🟡 (ADR/patterns ✓, no ATAM/governance/QA-tradeoffs) | Thicken |
| Delivery & Execution | ❌ | New |
| Quality/Reliability/Security | 🟡 (testing basics, no SLO/observability/incident) | Thicken |
| Communication & Influence | ❌ | New |
| Mentoring & Team Leadership | ❌ | New |
| Engineering Economics | ❌ | New |
| Promotion Evidence | ❌ | New |

Mid soul covered ~3/9 → verdict "yes, upgrade, and it's overdue". Expect 5–7 missing areas on a level-up — that is the point, not a failure.

## Step 3 — Keep / elevate / add
- **Keep:** Dependency Rule, ADR-before-code, OpenAPI-first, DB migrations, conventional commits, template ownership, Clean Architecture depth.
- **Elevate principles:** "Code is the product" → "Outcomes are the product — code is the instrument"; "Test what matters" → "Define the quality strategy, don't just write tests".
- **Add principles:** own the outcome end-to-end; frame before build; decide with economics; multiply the team (6 → 9 principles).
- **Knowledge Base:** career anchor flips — `01_Software_Engineer` (foundation) → `02_Senior_Software_Engineer` (primary, 9 capability charters). Add BOKs the new areas cite: BABOK (framing), PMBOK (delivery), CyBOK (security) on top of SWEBOK/SEBoK.
- **Owned docs:** add senior 🔴 (Problem Statement, Test Strategy, SLO/SLI, Deployment+Runbook, Risk Register); keep code/ADR/API/DDL.
- **Priority protocol:** frame → decide → build → make reliable → deliver → grow team → evidence.
- **Quality gates:** + problem statement before code, SLO defined, runbook+rollback, SAST/SCA green.

## Step 4 — Verification
- `scripts/verify_soul_refs.py <soul-dir>` — senior upgrade passed: 81 unique refs, all resolve.
- The verifier only catches backtick-wrapped paths ending `.md` under known vault roots; hand-check folder-only refs (`14_Security\`) and multi-file backtick cells (`Deployment-Plan.md`, `Operations-Manual-Runbook.md` — regex stops at the first `.md`).

## Step 5 — Review gate + sync
1. Write to `soul-collection\<DOMAIN>\` — user reviews (he checks role framing, template depth, team-size line in the footer).
2. After approval: backup `profiles\_soul_backup_<YYYYMMDD>\<profile>-SOUL.md.bak` → `cp` collection → profile → `md5sum` both (must be byte-identical) → smoke test:
   ```bash
   hermes -p <profile> chat -q "Answer in one sentence: What is your name, your role, and your number one core principle?"
   ```
   Expected: identity + elevated principle quoted verbatim-ish.
3. Registry/main-soul routing: NOT touched for level upgrades (domain/triggers unchanged). Only NEW profiles get registry rows + main-soul routing lines.
