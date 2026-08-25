---
name: github-pr-follow-up-review
description: "Use for GitHub PR re-reviews after fixes."
version: "1.0.0"
author: "Hermes Agent"
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [github, pull-request, qa, re-review, verification, integration-testing]
    related_skills: [github-code-review, requesting-code-review]
---

# GitHub PR Follow-up Review

A follow-up review is a fresh quality gate, not a confirmation of the author's summary or the previous review. Use this skill after a developer pushes fixes to an open PR, especially when an earlier review had findings, a premature approval, or contradictory evidence.

## When to use

- The user asks to re-review a PR after fixes.
- A PR head commit changed after QA findings.
- A previous approval is challenged by new test output or an independent reviewer.
- The PR description claims verification but the repository has no corresponding CI checks.
- The change includes middleware, routing, database integration tests, or test-gate changes.

## Review principles

1. **Current head wins.** Fetch/read the current PR head and compare it with the base; do not rely on the PR body, old comments, or a previous verdict.
2. **Acceptance criteria are the oracle.** Cross-reference the current implementation against the user story, ACs, API specification, database schema, and security standards.
3. **Verify claims with live evidence.** Run tests, inspect output, and exercise boundary behavior. Never report a claimed check as passed unless the tool output proves it.
4. **Independent evidence beats confidence.** Use a fresh review pass or subagent for difficult changes, but adjudicate its claims against the code and a focused reproduction before posting.
5. **Correct the record explicitly.** If later evidence overturns an earlier approval, post a correction that says the old verdict is superseded and explains why.

## Workflow

### 1. Capture the current PR state

Use `gh` or the GitHub API to collect:

- PR number, title, author, base branch/SHA, head branch/SHA, state, mergeability.
- Changed-file list and diff from the base.
- Existing reviews/comments and status checks.
- Whether the authenticated account is the PR author; GitHub will reject a formal approve/request-changes review from the PR author.

Confirm the local worktree is clean before relying on local code. Never let temporary probes or generated files become part of the review state.

### 2. Re-read the governing contract

Read the exact sections needed for the changed story:

- User story and acceptance criteria.
- API response/error and middleware requirements.
- Database schema, constraints, triggers, and migration behavior.
- Security coding standards and the project test plan.
- Development workflow/CI requirements.

Separate code defects from requirements gaps. Use the documented severity and merge-gate rules.

### 3. Inspect the fix diff and surrounding code

Review both:

```text
git diff <base>...<head>
git diff <old-reviewed-head>..<new-head>
```

The second diff shows what the developer attempted to fix; the first verifies the complete PR still satisfies the feature contract. Read the full surrounding functions, route registration, test setup, and build targets—not only changed lines.

### 4. Verify middleware and route tiers

Fiber route grouping has a subtle scope rule:

- Middleware passed to `app.Group("/api/v1", middleware)` is prefix middleware and matches descendants such as `/api/v1/webhooks`.
- Adding a child group with a higher limit does not bypass an inherited parent limiter. A 100/minute parent plus a 200/minute child still rejects at 100.
- If tiers differ, make the route groups non-overlapping or attach middleware at explicit route scope. If all endpoints must be limited, include root and health routes or document an explicit exemption.

Always use a fresh app/process for in-memory limiter probes. Verify exact boundaries:

| Route tier | Requests allowed | First rejected |
|---|---:|---:|
| Standard | 100 | 101 |
| Webhook | 200 | 201 |

Check the status, `RATE_LIMITED` JSON envelope, `Retry-After`, and rate-limit headers where required. Do not infer correct scope from the source layout alone.

### 5. Verify integration-test gates and isolation

A separate Make target is not automatically a mandatory gate.

- Run the normal target with `DEERNGO_TEST_DATABASE_URL` unset. If `go test ./...` passes with `t.Skip`, the default path is false-green for database behavior.
- Run the integration target without the DSN and confirm it fails non-zero.
- Inspect `.github/workflows/` and Makefile dependencies to confirm CI/`make all` actually invokes the mandatory integration gate.
- Run the integration target with an isolated test database and record real results.

Database test isolation:

- Package-level Go tests can run concurrently.
- Tests that `TRUNCATE` a shared database and reuse fixed handles are unsafe under `go test -p=2`.
- Reproduce deliberately with repeated package-parallel runs, for example `go test -p=2 -count=20 -failfast ./internal/repository ./internal/server`.
- Fix the class of problem with isolated databases/schemas, unique per-test fixtures, or explicit serialization. A sequential happy path does not make a destructive shared database CI-safe.

### 6. Verify response contracts and error paths

For API create/update behavior, assert all contract fields, not only status and one field:

- `data.id` is present and valid.
- Every required input and returned field is present and normalized as specified.
- `created_at` and `updated_at` are present and sensible.
- New/upsert status codes are correct.
- Validation details and top-level messages exactly match the API specification.
- Internal failures are logged with safe context while clients receive a generic error.

Add boundary tests for empty input, maximum lengths, invalid timestamps, duplicate/upsert semantics, and any new rate-limit tier.

### 7. Run and classify verification

Run the project’s real commands, usually:

```bash
go test -count=1 ./...
go test -count=1 -race ./...
go vet ./...
go build -trimpath -o bin/<binary> ./cmd/server
gofmt -d .
go mod tidy -diff
git diff --check
```

Run the mandatory database target separately with an isolated DSN. Record unavailable tools honestly; do not fabricate linter or vulnerability-scan results.

On Windows with `core.autocrlf`, `go mod tidy -diff` and formatting tools may report line-ending-only noise. Verify normalized content in a disposable copy rather than rewriting the review worktree merely to make a read-only check quiet.

### 8. Publish the verdict

Use this decision rule:

- **Approve** only when no critical/high/merge-blocking findings remain and the relevant evidence is real.
- **Request changes** when a contract, security, data-integrity, test-gate, or deterministic integration problem remains.
- **Comment** for genuinely non-blocking observations only.

If the authenticated user owns the PR, post a detailed comment and inline comments instead of claiming a formal blocking review was submitted. Include the exact head SHA, findings, commands run, and any limitations.

## Common failure patterns

### Parent limiter masks a child tier

Symptom: source contains both `rateLimit(100)` on `/api/v1` and `rateLimit(200)` on `/api/v1/webhooks`, but the webhook returns `429` at request 101.

Root cause: prefix middleware inheritance.

Fix: remove overlap; attach standard limiting only to non-webhook routes or use explicit route middleware.

### Green default suite with skipped integration tests

Symptom: `go test ./...` exits 0 while output contains `--- SKIP` for PostgreSQL tests.

Root cause: required DSN is absent and tests call `t.Skip`; the new fail-fast target is not part of the normal/CI path.

Fix: wire the integration target into CI/`all`, or make the required integration command the documented gate and ensure CI invokes it.

### Parallel package interference

Symptom: first insert reports upsert/update instead of create, fixed fixture is missing, or display name comes from another test.

Root cause: multiple packages truncate and mutate the same database with fixed identifiers.

Fix: isolate fixtures or serialize the package tests.

### Premature approval

Symptom: a review says “approved” and later evidence finds a remaining defect.

Fix: post a correction immediately, state that the earlier verdict is superseded, and give the developer one authoritative current verdict.

### Literal `\n` in GitHub comments

Symptom: posted review comments show `\n` as visible text instead of line breaks.

Root cause: `gh pr comment --body '...\n...'` or `gh api -f body='...'` does not interpret `\n` as newlines.

Fix: use `execute_code` with `json.dumps({"body": multiline_string})` piped to `gh api --method POST/PATCH --input -`. See `references/pr-follow-up-verification-pitfalls.md` for the full pattern.

## Handoff format

```markdown
## QA Follow-up Review

**Head:** <sha>
**Verdict:** Approved ✅ / Changes Requested 🔴 / Comment 💬

### Blocking findings
- **path:line** — evidence, requirement, and required fix.

### Non-blocking observations
- **path:line** — evidence and recommendation.

### Verification
- `command` — result

### Limitations
- Missing checks/tools or environment constraints, stated plainly.
```

## References

- `references/pr-follow-up-verification-pitfalls.md` — reusable Fiber boundary probes, integration-gate checks, isolation reproductions, and correction guidance.

## Related skills

- `github-code-review` — initial GitHub PR review and comment mechanics.
- `requesting-code-review` — pre-commit verification for the implementer’s own changes.
