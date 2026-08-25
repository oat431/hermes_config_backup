# Evidence Patterns from a Spec-Driven Go PR Review

Use these patterns when reviewing API changes that cross Fiber routing, service validation, sqlx persistence, and PostgreSQL integration tests.

## Contract evidence

A response contract can define both the top-level `error.message` and every `error.details[]` item. A test that checks only the HTTP status or the number of detail entries can miss a client-visible mismatch. For required fields, keep distinct cases for:

- missing/blank: field-specific required message;
- over-length: maximum-length message;
- malformed format: format message.

Exercise `{}` and each single-field omission live, then compare the complete JSON envelope with the specification.

For success responses, status-only tests are insufficient. Assert the documented envelope and every contractual field (especially generated identifiers, normalized values, timestamps, and upsert metadata) so a response-shape regression cannot pass unnoticed.

## Operational evidence

Route registration alone does not satisfy a rate-limit requirement. Inspect middleware wiring and run a boundary probe at `N` and `N+1` requests. Discard bodies during the probe and use a disposable/isolated database. Clean up only probe-created rows afterward.

Fiber group middleware is inherited by descendant routes. A broad `Group("/api/v1", limiter(100))` also wraps `/api/v1/webhooks`, so a later sibling webhook group with `limiter(200)` is not an isolated tier. Inspect group prefixes and probe each special tier in a fresh app/process—webhook requests should reach 200 before the 201st request returns the documented 429 envelope. Do not exhaust the default tier first, because cross-tier interference can hide the boundary defect.

A generic 500 response is only half of the error-handling requirement when the security standard also requires internal diagnostics. Trigger a repository failure or use a stub, verify the client receives no internal detail, and separately verify an internal log entry is produced without secrets.

## Integration-test evidence

`t.Skip` on a missing DSN makes the default suite green without proving database behavior. Run the opt-in tests with an isolated PostgreSQL DSN, and report the two states separately:

- default suite: passed, but integration skipped if the variable is absent;
- explicitly configured integration suite: passed or failed.

When multiple packages truncate the same database, run them in parallel and repeatedly (for example, `go test -p=2 -count=100 ./internal/repository ./internal/server`). A single configured pass—or a short repetition—can miss an interleaving. If failures such as an expected first insert returning 200 or a first upsert reporting `created=false` appear, the shared fixture is proven race-prone. Do not call the tests flaky solely because destructive setup exists; classify based on observed failures. The durable fix is isolation or serialization, not a fabricated failure.

## GitHub publication evidence

For a self-authored PR, a formal `REQUEST_CHANGES` API call returns HTTP 422. Submit a `COMMENT` review with the technical verdict clearly stated, include inline comments anchored to the head SHA, and read the returned review/comments back. Report `COMMENTED` rather than claiming a blocking review.

## Dependency evidence

Run `go mod tidy -diff` without modifying the worktree. If production code imports a module currently marked indirect, report the tidy diff as a cleanup suggestion and verify `git status` remains clean.
