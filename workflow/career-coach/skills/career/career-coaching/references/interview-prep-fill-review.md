# Interview Prep Fill-Review — Trap Detection Playbook

Screen every candidate [CONFIRM] fill against this list before it becomes a rehearsed interview answer. Real cases from the MISUMI Senior ReactJS prep (Aug 2026).

## Phrases that must never leave the vault

| Raw fill | Why it's fatal | Reframe |
|---|---|---|
| "I never understand / I don't know X" where X is JD-named (Redux, Cypress…) | Instant red flag on a required skill | Deliberate-choice framing: "I chose Y because…; I'd reach for X when…" PLUS mandate a 2–3h crash course on X before the interview — the script is a bluff until backed by study |
| "No conflict" (asked about conflict) | Dodges the question; implies zero navigation experience | "A difference of technical views we navigated respectfully" + the real arc: listened → proposed with reasoning → disagree-and-commit → delivery + relationship intact |
| "I guess they didn't want to…" (motive-guessing about colleagues) | Unprofessional, invites probing | State what the system/process did, never what people thought |
| "The architect decided, I don't know" | Reads as disengaged | Attach reasoned understanding: "It was the SA team's decision; my understanding is [reasoning], and I've since studied the trade-off space" |
| "I'm not sure" about past project decisions | Reads as disengaged | Clean close: "It was deprioritized to ship; I left that project before it was revisited" |
| Casual intimacy ("we eat lunch together") | Too informal for a panel, esp. Japanese | "The working relationship stayed strong" |
| Employer complaints ("outsource, no ownership, limited access") | Reads as blaming; Japanese panels weigh this heavily | Growth-pull framing: product ownership over project rotation, deep-own-one-product, new-industry breadth at the candidate's age |
| Volunteered sloppiness ("hardcoded timing checks") | Sounds careless when unforced | "Timing instrumentation" first; upgrade honestly to "today I'd use OpenTelemetry-style tracing" only if pressed |

## Principles, not anecdotes

When the dramatic version of a story never happened (caught someone gaming tests, prod meltdown, heroic fix), do NOT let the candidate fabricate it — probing collapses it. Reframe as a principle earned from real work: e.g., "Coverage numbers can lie — so my review checks test *quality*, not just coverage." Principles backed by real work survive probing; invented war stories don't.

## Spoken-version pattern

Candidates cannot speak raw bullet fills. Every approved fill gets a 🗣️ spoken version: 60–120 seconds, conclusion-first, quantified, rehearse-ready. This is the actual deliverable of the fill-review round.

## Evidence repos (GitHub showcase idea)

When the candidate proposes publishing proof-of-skill repos:
- Fresh code ONLY — never publish employer code (write new examples)
- Mention in the interview ONLY if the repo exists and builds by the day before — never promise vapor
- Time-box 2–3 hours; keep scope modest (one component + one hook + one util + clean README). An over-engineered showcase raises the bar for the technical questions it invites
- Learning artifacts (crash-course app) live in a separate repo — the commit history itself evidences the learning

## Facts that change the strategy

When a fill reveals a fact that materially changes fit (e.g., ~1 year React vs a 3+ year requirement), immediately:
1. Revise the fit verdict honestly in the vault (e.g., ~80% → ~60%) and say so bluntly to the candidate
2. Write an honest pivot script: name the honest number, then pivot to velocity/evidence proof ("I took three legacy modules from zero tests to 90% coverage under delivery pressure")
3. Explicitly forbid inflation in the vault — honesty framed as trust-building, not confession

## Attribution hygiene in fills

Candidate fills often blur ownership ("we built X"). Under probing, split-ownership stories collapse. Enforce per-artifact attribution tables in the fit assessment: who built it vs who reviewed/supervised it. Reviewing every line of a junior's work is its own strong story — don't let it get claimed as authorship.
