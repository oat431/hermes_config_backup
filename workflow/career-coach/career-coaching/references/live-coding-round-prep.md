# Live Coding Round Prep — pair programming, debug-and-extend, take-home

Use when the round is **live coding / pair programming / "debug and extend our app"** rather than a panel Q&A. The deliverable is a prep pack **plus a rehearsal repo the candidate can actually run**. For panel prep see `interview-prep-vault.md`.

## 1. Read the invitation as a spec

The email is written by someone who knows exactly what is scored. Decode it line by line into a rubric:

| Their words | What it means |
|---|---|
| "how you work with code in a small X application" | Unfamiliar repo, readable in ~10 minutes |
| "with minimal dependencies" | **No framework.** Plain language + stdlib + maybe a test lib. Framework-shaped experience becomes a liability here |
| "debug existing functionality" | Planted defect(s). In a stateful domain: precision, concurrency, rounding, broken contract |
| "implement new features" | Additive work; they watch test discipline and edge-case thinking |
| "understand and extend existing code" | A design smell is seeded. Extend in the code's grain, do not rewrite the file |
| "we will also assess system design / trade-offs" | Design is scored *inside* the coding session — it needs moments, not a whiteboard |
| "feel free to ask questions, explain your thought process" | The scoring channel, named explicitly. Narration is graded |

## 2. Recon: search the exercise text

1. Take a distinctive phrase from the invitation and search it quoted, plus the domain word ("banking", "ledger", "booking"). Candidate reports on Glassdoor / Medium / regional dev forums reproduce the exercise wording nearly verbatim.
2. Extract from those reports: the **round order**, the **seeded-defect type** (e.g. "find the bug → it was a race condition"), the **take-home shape**, and what the review round does (often: *refactor one of your own classes live*).
3. Cross-check the company's own job posts — they name the real stack, which tells you which trade-off vocabulary is native (transactions + reconciliation for payments, not REST + caching).
4. Flag the inference in the artifact: name the company you believe it is and say which prep survives if you are wrong. Never present inferred intel as confirmed.

## 3. The prep pack (numbered files, same vault convention)

| File | Must contain |
|---|---|
| `00_..._Index` | 30-second verdict, file map, **battle card: moment → exact line to say**. The only thing read on the day |
| `01_..._Recon` | Decoded invitation, scoring rubric (dimension / earns a tick / loses a tick), what comes after this round, company lens |
| `02_..._Concern_Register` | Ranked risks: evidence, fix, hours. Verdict table. This answers "should I be worried?" |
| `03_..._Language_Refresher` | Only the idioms the round will use. **Every snippet compiled and run before it goes in the file** — say so in the frontmatter |
| `04_..._Domain_Playbook` | The domain's correctness tell (see §4), edge-case checklist, "what I'd add before production" list for the closing line |
| `05_..._Pairing_Protocol` | Verbatim scripts: opening, debugging out loud, asking for a nudge, disagreeing, when you don't know. The highest-value file in the pack |
| `06_..._Design_and_Tradeoffs` | 3 moments to zoom out mid-code, the 5-step design frame, trade-off sentence templates |
| `07_..._Drill_Plan` | T-3/T-2/T-1/day-of, drills with time boxes, "what ready looks like" checklist, questions to ask them |

## 4. Find the domain's correctness tell — and drill it

The interviewer is looking for one or two "has this person shipped in this domain" signals. Name them and make the candidate say them unprompted:

| Domain | The tell |
|---|---|
| Money / payments | `BigDecimal` + explicit scale + explicit `RoundingMode`; never `double`. Then idempotency keys, the double-entry invariant, audit-by-append |
| Inventory / orders | Concurrency on stock decrement, idempotent order creation, overselling |
| Identity / auth | Token lifetime, revocation, constant-time comparison, never logging secrets |
| Data pipelines | Idempotent re-runs, late data, exactly-once vs at-least-once |
| Healthcare / regulated | PHI at rest and in logs, audit trail, retention |

Shape for every one of them: *the naive choice*, *why it is wrong*, *the correct choice*, *the cost of the correct choice*. A candidate who names a cost unprompted reads senior.

## 5. The rehearsal repo — the differentiator

Reading notes cannot train "read unfamiliar code and debug it". Build a small repo in the round's language, under the round's constraints, containing **the defects an interviewer would plant**.

Recipe:

1. **Zero dependencies.** Plain source tree, one `build.sh` (`javac --release <N>` / `go build` / `node`) and one `test.sh`. A hand-rolled assertion harness (`Checks.equal/isTrue/throwsIllegalArgument/probe`) beats fighting a test framework and mirrors "minimal dependencies" exactly.
2. **Two suites.** A *baseline* that must stay green (the candidate's regression net) and *probes* that fail — one per defect, each independently reporting so a single run shows the whole picture.
3. **Seed realistic defects, one per habit being tested.** For a stateful domain: lossy numeric type; `==` instead of `equals`; `equals` without `hashCode`; truncation instead of documented rounding; a missing domain guard (self-transfer / zero / negative); a lost update under concurrency; an unsynchronised collection.
4. **Make the failure message teach.** Print the raw offending value, not the formatted one — `stored value was 0.30000000000000001665…` is the lesson; `expected 0.30, actual 0.30` is a puzzle.
5. **Stage it.** Stage 1 debug (probes red to green), stage 2 extend (new feature + edge cases), stage 3 refactor under test (replace an `if/else` chain with a sealed/polymorphic type).
6. **`SOLUTIONS.md` holds the diffs *and the trade-off conversation*** each fix triggers — the fix is 30% of the score, the sentence said while fixing is the other 70%.

### Solvability check (never skip)

A practice repo that cannot be fixed destroys trust. Before delivering:

```bash
rm -rf "$TMPDIR/solution-check"; cp -r "<repo>" "$TMPDIR/solution-check"; cd "$TMPDIR/solution-check"
# apply every documented fix, then
bash test.sh   # must print all green
```

Delete the copy, then quote the real numbers in the README (baseline green, N probe failures across M areas, "verified solvable"). Apply fixes in the copy with **signature-anchored** replacements — overloaded methods share identical bodies and a body-level replace breaks the correct overload.

### Non-deterministic probes

Concurrency probes legitimately vary (8 failures, sometimes 9). Say so in the README — "that variability *is* the lesson: a race is not a deterministic failure" — instead of hard-coding a count that will look like your bug.

## 6. Pairing protocol — the part that decides close calls

The brief usually grants permission to ask questions and think aloud; encode it as scripts:

- **Opening (first 5 min):** restate the task and acceptance criteria; run the test suite to establish a baseline; state the plan and invite correction. Before typing anything.
- **Debug loop out loud:** reproduce → read the full error → *killable* hypothesis → cheapest test → narrow → root cause in one sentence → regression test → verify. Silence over ~20s reads as "lost".
- **Asking for help, like a senior:** "I've narrowed it to these two files — I'd like a nudge on which one, not the answer." Never "I'm stuck, help". Asking is explicitly invited and scores positively.
- **Disagreement template:** acknowledge → name the cost → propose → defer ("which problem are we optimising for?"). Never "that's wrong"; never instant capitulation.
- **Scope discipline:** when spotting the design smell, ask "fix it now, or keep this change additive and note it as follow-up?" — they are testing whether the candidate rewrites files they met twenty minutes ago.
- **Three honest exits for not knowing:** know-the-concept-not-the-API / outside-my-experience / not-the-answer-I'd-defend. Bluffing is the only unrecoverable move.

## 7. Pitfalls

- Do not let concern #1 be "technical ability" when the actual #1 is an uninstalled toolchain. Rank by *damage per hour of prep*, not by how impressive the fix sounds.
- Do not write a T-3/T-2/T-1 plan before knowing the date; ask for it, or label every step relative and flag the file as unanchored.
- Do not deliver prep without the drill that makes it automatic: recorded out-loud run, listen back, count silences. Knowledge without rehearsal collapses under observation.
- Do not gold-plate the take-home that follows. Overscoping is a documented rejection reason in this class of round; scope discipline is the signal.
- Cross-vault refs: from the interview-prep vault to swe-knowledge, use a plain code path, not a wikilink — each top-level folder is its own Obsidian vault.
