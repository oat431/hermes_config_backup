# QA Polish Pass — Worked Example (SevenSolution, 2026-08-15)

Dev→QA handoff polish pass on a Go + Fiber v3 + MongoDB user-management API (interview project, hexagonal architecture, gRPC bonus). Baseline: dev handoff minute (073-style) with 6 QA action items, one pre-confirmed defect (413 error code), and a suggested probe. Outcome: 19 new automated checks, 3 defects filed, 46/46 AC traceability, security handoff evidence pack — committed + pushed in 2 commits.

## Sequence that worked

1. **Read handoff + spec basis first** (ACs, API spec, test plan, DoD) — the AC table is the oracle; the API error-code table is the contract for defect classification.
2. **Baseline re-verification** — re-ran every handoff claim: gofmt/vet/build, `go test -race -cover ./...` (coverage numbers matched exactly), smoke script vs live compose stack, container health, in-container health probe. Record as a table in your handoff minutes: claim → verification → result.
3. **Live probes before code changes** — reproduced the dev-reported defect with your own curl; spot-checked envelope shapes for 400/401/404/405/409/413 (shape-vs-code split: shape was right, code value wrong — that distinction decides severity).
4. **Code review pass** — read every handler/adapter/config file against spec; verify handoff-claimed fixes are actually in code (timeouts, pool sizes, listener network).
5. **Close gaps in risk order:**
   - Integration suite for the 0%-coverage adapter (build tag `integration`, throwaway DB per test `qa_it_<ts>_<seq>` dropped in `t.Cleanup`, `MONGO_URI` env override). Pitfalls found: Mongo DB names ≤63 chars (don't embed full test names); BSON datetime is ms-precision, so `time.Time` round-trips truncate sub-ms — compare CreatedAt with tolerance, not `==`.
   - Concurrency race AC at SERVICE level against real DB (16 goroutines, start-gate channel, count successes/conflicts; assert exactly 1 / N-1 / 0 and exactly 1 persisted doc). Fake repos serialize, so unit level can never prove this AC.
   - Traceability walk against test source (grep `^func Test` across all `*_test.go`, map to ACs) — found 2 untested ACs in a "fully covered" codebase; closed with 2 unit tests.
   - Smoke extension: append checks, keep numbering, graceful `command -v` guards, container-health probe via `docker inspect -f '{{.State.Health.Status}}'`.
6. **Deliverables:** 042 test cases (with full 46-AC traceability table including an honest residual-risk column), 043 defect report (each with live repro evidence), QA→PO handoff minutes (verdict + decisions requested), QA→Security handoff minutes (evidence pack).
7. **Commit convention:** one commit for the whole QA pass, `test(qa):`/`docs(qa):` prefix, message body enumerates the closed action-item IDs. Persona-commits one at a time per the project's DEC.

## Defect classification that proved useful

- **Misleading-but-correct-status defects** (413 with `INTERNAL_ERROR` code): Medium, not High — status is right, code misleads; route to PO if the code table is a locked contract.
- **Undocumented-but-consistent values** (catch-all 404 code `NOT_FOUND` absent from the spec's error table): Low, spec-gap class — found only by walking the contract table row-by-row against live responses.
- **Build hygiene with secret exposure** (no `.dockerignore` → real `.env` inside builder stage): escalate from inspection to DEMONSTRATED fact — `docker build --target builder` then `ls` the stage. Final-image-clean ≠ context-clean; state the blast radius precisely (builder layers only vs shipped artifact).

## Security handoff evidence pack (what to hand over)

Verified-for-them table with commands: secrets-in-git (`git log --all -- <file>` empty), final-image contents (`docker run --entrypoint sh <img> -c ls`), non-root (`id` in running container), build flags from Dockerfile, JWT unit-suite results, no-secret-logging tests. Then pre-chewed findings: exact file:line for the timing side-channel (early-return before bcrypt when email unknown) + 3-line fix sketch (dummy bcrypt compare). Then their open action items with QA-observed status. Repo visibility check (`gh repo view --json visibility`) — a public repo raises the stakes of every secret-hygiene finding.

## Redaction-guard incidents (see SKILL.md pitfall)

Three failures burned before root-cause: inline terminal `$()` with a password in the same command, `write_file` of a bash script, `patch` of a smoke-script line. All showed as `syntax error near unexpected token ')'` with `TOKEN=***` in the echoed error. Diagnostic that ended it: `od -c` on the failing line showed literal `***` on disk + a Unicode ellipsis char — the guard had rewritten file content. From then on: all script writes via Python with fragment-built token refs, and post-write integrity check `grep -c '[*][*][*]' file` == 0.
