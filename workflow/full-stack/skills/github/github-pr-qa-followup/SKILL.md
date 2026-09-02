---
name: github-pr-qa-followup
description: "Use when QA reviews a GitHub PR and findings need fixes."
version: 1.0.0
author: "Dev Persona"
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [github, pull-request, qa, review, verification, go]
    related_skills: [github-code-review, github-pr-workflow, requesting-code-review, test-driven-development]
---

# GitHub PR QA Follow-Up

## Trigger

Use when a QA reviewer has inspected an open GitHub pull request and reports
correctness, API-contract, security, observability, or test-gate findings.
This skill covers the full loop: inspect → reproduce → fix → verify → push →
request re-review. It does not merge the PR automatically.

## Workflow

### 1. Read every GitHub review surface

Do not rely on browser extraction alone; PR pages may omit review details.
Use the repository explicitly:

```bash
gh pr view <PR> --repo <owner>/<repo> --json number,title,state,baseRefName,headRefName,mergeStateStatus,reviewDecision,statusCheckRollup,url,commits,files
gh api repos/<owner>/<repo>/pulls/<PR>/reviews --paginate
gh api repos/<owner>/<repo>/pulls/<PR>/comments --paginate
gh api repos/<owner>/<repo>/issues/<PR>/comments --paginate
```

Read the full PR diff and the referenced source/spec files before editing.
Classify each finding as blocking correctness/contract, blocking
security/operability, blocking test-integrity, or non-blocking suggestion.
A clean merge state or no GitHub checks is not QA approval.

### 2. Reproduce findings with tight tests

Before fixing, create or run a red-capable test at the boundary where the
problem appears. Examples from Go/Fiber APIs:

- Rate limit: 100 requests from one IP succeed; request 101 returns `429` and
  JSON `error.code == "RATE_LIMITED"`.
- Contract validation: empty request returns the exact top-level message and
  each exact `error.details[].field/message`; required and max-length messages
  must be distinct.
- Error observability: inject a repository failure, assert the client receives
  generic `INTERNAL_ERROR`, and capture an injected `*slog.Logger` to assert the
  internal error is logged without credentials.
- Database integration: run repository and HTTP tests against an isolated
  PostgreSQL database, not only mocks.

Do not replace a failed integration run with a claim that it passed.

### 3. Apply targeted fixes

Keep the PR scope narrow and preserve the existing architecture:

- Add Fiber limiter middleware at the live route group, not only to a helper.
  Configure the documented standard and webhook tiers separately. **Important:**
  if you use `app.Group("/api/v1", rateLimit(100))` and then
  `app.Group("/api/v1/webhooks", rateLimit(200))`, the 100/min limiter fires
  on webhook paths too because the group prefix matches. Use a `Next` function
  to skip nested paths or register groups under non-overlapping prefixes.
- Return generic internal errors to clients but log unexpected persistence
  failures with operation context through an injectable structured logger
  (`*slog.Logger`). Never log DSNs, secrets, refresh tokens, or raw sensitive
  payloads.
- Separate required-field and max-length validation. Map exact API contract
  messages; add tests for both top-level and field-level messages.
- Run `go mod tidy` when production imports were incorrectly classified as
  indirect dependencies.

### 4. Enforce integration-test coverage and isolation

It is acceptable for the default unit command to run without credentials, but
acceptance-critical PostgreSQL tests must have a mandatory command that fails
when its DSN is absent. A Make target is a simple pattern:

```make
.PHONY: test-integration

test-integration:
	@test -n "$(DEERNGO_TEST_DATABASE_URL)" || (echo "DEERNGO_TEST_DATABASE_URL is required" >&2; exit 1)
	DEERNGO_TEST_DATABASE_URL="$(DEERNGO_TEST_DATABASE_URL)" go test -p=1 -count=1 -v ./internal/repository ./internal/server
```

`t.Skip` may preserve developer convenience in the default suite, but it must
not be the only enforcement for required integration coverage.

Additionally, wire the gate into CI (e.g., `.github/workflows/ci.yml`) with a
PostgreSQL service container so every PR run exercises the integration path.
Without CI enforcement, a green `go test ./...` can still skip all database
verification.

**Test isolation:** when multiple test packages share the same database, use
unique UUID-based keys per test instead of `TRUNCATE` + fixed fixtures (e.g.,
`viewer1`). Serialize packages with `-p=1` in the integration Make target as
defense-in-depth against cross-package interference.

### 5. Verify in layers

Run all relevant checks after the fix:

```bash
make fmt
make test
make vet
make build
go test -race ./...
go mod tidy -diff
git diff --check
```

Then run the mandatory integration gate against an isolated database. When the
host is Windows and PostgreSQL is in Docker, a Unix-socket DSN from the host
will not work. Use a verified TCP DSN with credentials, or compile the test
binary for Linux and run it inside the PostgreSQL container:

```bash
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go test -c -o bin/deerngo-repository.test ./internal/repository
docker cp bin/deerngo-repository.test local-postgres:/tmp/deerngo-repository.test
docker exec local-postgres chmod +x /tmp/deerngo-repository.test
docker exec -e DEERNGO_TEST_DATABASE_URL='postgres:///deerngo_test?host=/var/run/postgresql&user=postgres&sslmode=disable' local-postgres /tmp/deerngo-repository.test -test.run TestPostgresSubscriberRepositoryUpsertPreservesEarliestTimestamp -test.v
```

Use the equivalent compiled test for the HTTP integration package. Clean up
copied binaries after the run. Keep the exact pass/fail output.

### 6. Commit, push, and document

Use a focused follow-up commit, for example:

```text
fix(subscribers): address QA review findings
```

Push the existing feature branch, then update both the PR and its linked issue
with the follow-up commit SHA, findings addressed, exact verification results,
and infrastructure-specific test details.

Re-check remote state:

```bash
git status --short --branch
git ls-remote --heads origin <feature-branch>
gh pr view <PR> --repo <owner>/<repo> --json headRefOid,baseRefName,state,mergeStateStatus,reviewDecision,url
```

### 7. Stop for fresh QA review

Do not merge after self-fixing. Ask QA to re-review the new head commit. If
QA used the same account as the PR author, GitHub may record only a `COMMENTED`
review because self-approval/request-changes is restricted; report that fact
and treat unresolved findings as blocking until QA explicitly rechecks them.

## Pitfalls

- **Only checking `gh pr view`** — review details may live in separate REST
  endpoints; fetch reviews, inline comments, and issue comments too.
- **Testing only the helper** — middleware may be registered incorrectly; test
  through the actual Fiber route group.
- **Fiber group prefix-middleware inheritance** — `app.Group("/api/v1", mw)`
  applies `mw` to ALL paths under `/api/v1/`, including a later
  `app.Group("/api/v1/webhooks", mw2)`. The first middleware fires on every
  request to the nested path regardless of the second group. Use a `Next`
  function to skip nested paths, or register groups under non-overlapping
  prefixes. See `references/fiber-rate-limit-patterns.md`.
- **Combining validation messages** — required and length violations are
  different contract cases; assert exact messages.
- **Using `t.Skip` as the integration gate** — it creates false green results;
  add a failing-on-missing-DSN command and wire it into CI.
- **Fixed test fixtures across packages** — when two test packages share a
  database and both `TRUNCATE` the same table or use the same fixed key (e.g.,
  `viewer1`), concurrent execution (`go test -p=N`) causes false failures. Use
  unique UUID-based handles per test and remove `TRUNCATE`; serialize packages
  with `-p=1` as defense-in-depth.
- **Logging client-safe errors only** — operational diagnosis requires the
  internal error to be logged, but secrets must remain excluded.
- **Calling a host Unix socket from Windows** — run inside the DB container or
  use TCP; preserve real evidence.
- **`go.sum` CRLF/LF false diff on Windows** — `go mod tidy -diff` may report
  go.sum changes that are purely line-ending normalization, not content
  changes. Stage the file (`git add go.sum`) and re-check; if the diff
  disappears, it was line-ending noise.
- **Merging after a local pass** — wait for fresh QA review and account for
  absent GitHub checks or self-review restrictions.

## Reference

See `references/qa-follow-up-checklist.md` for a compact reusable checklist
and command sequence.

See `references/fiber-rate-limit-patterns.md` for Fiber v3 multi-tier rate
limiting (prefix-inheritance trap, `Next()` skip pattern, factory, and
boundary test templates).
