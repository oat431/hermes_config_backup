# Design-Only Proposal Packages & Interview-Prep Handoffs

Patterns from the SevenSolution challenge Task 2 (lottery search system, design-only, 2026-08).

## 1. Proposal package anatomy (no code deliverable)

When the challenge asks for a **design proposal only** ("recommend storage, algorithms, performance analysis — no implementation"), author a 3-file package in `.agents/proposal/`:

| File | Basis | Content |
|------|-------|---------|
| `000_proposal_index.md` | — | Deliverable→section mapping table, evaluation-criteria coverage table, headline TL;DR, status checklist |
| `01_solution_proposal.md` | 029 HLD (adapted) | Problem analysis, architecture (mermaid), data structures, storage choice + alternatives table, algorithm, concurrency strategy, performance numbers, failure modes, assumptions, open questions |
| `02_architecture_decision_records.md` | 021 ADR | One ADR per consequential decision (storage split, indexing, allocation, recovery, scaling) |

### Rules that made the lottery proposal land

- **Open with the domain insight.** The non-obvious data fact: "10M tickets over only 1M distinct 6-digit numbers ⇒ ~10 copies per number ⇒ allocate ticket *instances* (`number-serial`), never numbers." Put it in Problem Analysis — reviewers score "thought about the data" before anything else.
- **Map every challenge deliverable to a section** in the index (the challenge named 4: architecture/data structures/algorithms, storage justification, performance analysis, concurrency strategy — the doc has one section per deliverable, auditable in 30 seconds).
- **Pre-answer the rejected alternative.** The interviewer WILL ask "why not just PostgreSQL `SKIP LOCKED`?" — the alternatives table names it as the strong runner-up with its trade-offs (slower claims, contention, index gymnastics for interior wildcards) before the question is asked.
- **Quantify estimates** (≈2.5 GB RAM, p95 <50 ms, ≥100K allocations/s) — numbers beat adjectives.
- **The concurrency argument in one sentence:** "SPOP is atomic and Redis executes single-threaded, so two concurrent identical queries each pop a different member — duplicates are impossible by construction, no locks."
- **End with open questions** (batch vs single allocation, lease TTL, sold-vs-allocated semantics) — invites discussion instead of closing it.

## 2. README disclosure for AI-assisted interview submissions

Place **before the Features section**:

- Disclose: *"produced spec-first with AI assistance — AI personas (PO/dev/QA/security) under continuous human review"*.
- Frame as strength, never apology: *"every significant decision has a recorded rationale, so nothing here is 'AI wrote it and we can't explain it'"*.
- Link both task packages (`.agents/spec/` for code, `.agents/proposal/` for design) and the decision trail (handoff minutes MTG-H01 → MTG-P01).
- Sync the same section into `031_README_developer_guide.md` so spec and repo stay consistent.
- Candidate coaching line: the true framing is "AI accelerated a spec-driven, decision-documented process I directed" — never "the AI wrote it."

## 3. Cross-profile handoff note (to another Hermes persona profile)

When handing work to a DIFFERENT profile (e.g. a coach-career profile created for interview prep, in a separate vault like `F:\obsidian_note\interview-preparation\7_solution`):

- **Self-contained, like a cron prompt** — the receiving profile has zero conversation context. No "as we discussed".
- **Absolute paths everywhere** (repo, spec packages, prep vault).
- Proven anatomy:
  1. Situation (interview flow, submission status)
  2. Deliverables map (path table)
  3. Cheat sheets — facts the candidate must know cold (stack, architecture, key decisions, headline design, quotable numbers)
  4. Attack surface — the drill questions with expected defense angle per criterion
  5. Disclosure framing — the exact sentence to rehearse
  6. Current state (e.g. "dry-run Round 1 posed, answers pending") — so the coach resumes instead of restarting
  7. Open threads checklist
- State the recipient's style directive ("candidate wants grill-me Socratic pressure, not lectures").
- Same-project persona handoffs stay as meeting minutes (07_pm/072_MM convention, MTG/DEC/ACT ids); cross-profile notes carry the trail as prose + links instead of ids the other profile can't resolve.

## 4. Dry-run interview structure (PO plays interviewer)

- Rounds escalate by evaluation criterion: (1) opening walkthrough, (2) correctness under concurrency, (3) performance numbers, (4) trade-off pressure ("why pay the Redis tax?"), (5) edge cases.
- Score against the challenge's stated criteria (feasibility/performance/correctness/practicality/creativity).
- Ask 2–3 questions per round, answer-in-your-own-words rule, then critique with the follow-up a real interviewer would use.
- Push hardest on the *weakest* defense — for this challenge: "why two databases?", "prove no duplicates", "what if the reaper dies".
