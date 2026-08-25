# Spec-Driven PR Review Reference

## Compact requirement matrix

| Area | Evidence to inspect | Typical requirement source |
|---|---|---|
| Scope | Base/head SHAs, changed files, worktree status | PR metadata + Git |
| API wiring | Route registration, dependency injection, middleware | Architecture/API spec |
| Request contract | Required fields, type/length/time parsing, normalization | Acceptance criteria/API spec |
| Response contract | Status, `data`/`meta`/`error` envelopes, exact messages | Acceptance criteria/API spec |
| Persistence | Unique key, atomic upsert, update fields, timestamp rule, returned row | DB schema/API spec |
| Security | Parameterized SQL, redaction, internal logging, rate limiting, headers/CORS | Security standard |
| Verification | Unit, integration, boundary, concurrency, security tests; skip behavior | Test plan/test cases |
| Operations | Build/lint/vet, module hygiene, migrations, CI checks, deployment assumptions | Construction/DevOps docs |

## Go review commands (read-only)

```bash
git status --short --branch
git diff --stat <base-sha>..<head-sha>
git diff --check <base-sha>..<head-sha>
go test -count=1 ./...
go test -race -count=1 ./...
go vet ./...
go build -trimpath ./cmd/server
gofmt -d cmd internal
go mod tidy -diff
gh pr view <number> --json baseRefOid,headRefOid,baseRefName,headRefName
gh pr checks <number>
```

Use `-count=1` so a cached pass does not substitute for fresh execution. `go mod tidy -diff` reports module drift without writing `go.mod` or `go.sum`. Never replace `gofmt -d` with `gofmt -w` in a read-only review.

## Common API/DB traps

- **Rate-limit illusion:** registering a route under `/api/v1` does not apply a limiter. Confirm `app.Use`/group middleware and the required 429 envelope.
- **Logging illusion:** returning a generic 500 protects the client but does not satisfy an internal logging requirement. Check that the original error reaches a logger with safe context.
- **Validation illusion:** checking only the number of field errors misses exact top-level and detail messages. Test each missing field separately as well as `{}`.
- **Normalization illusion:** unit-testing normalization with a stub does not prove two canonical forms collide in the real database. Add a DB-backed `@`, case, and whitespace duplicate test.
- **Upsert illusion:** a sequential duplicate test does not exercise concurrent uniqueness contention. Inspect the single-statement `ON CONFLICT` path and add a concurrent test when integrity is critical.
- **Integration race:** two Go packages can run in parallel under `go test ./...`. If both truncate the same test DSN, their setup can invalidate each other's IDs and status assertions. Serialize them or isolate schemas/databases.
- **Opt-in test illusion:** a test that calls `t.Skip` when a DSN is absent is not evidence of integration correctness. Report the skip and whether CI supplies the DSN.
- **Module drift:** a production import listed as `// indirect` is a `go mod tidy -diff` finding even if compilation succeeds.

## Finding evidence convention

Prefer a single changed line as the anchor and put cross-file evidence in the text:

```json
{
  "severity": "high",
  "path": "internal/server/server.go",
  "line": 19,
  "title": "Required operational control is absent",
  "evidence": "The app is constructed without the middleware that the route contract requires; the route is registered at line 26.",
  "requirement": "API specification §5 requires the control and its documented failure response."
}
```

Do not claim an issue from a mere absence unless the requirement explicitly demands it and the relevant construction point is clear. For a skipped or unavailable check, say so in `verification` rather than converting uncertainty into a finding.

## JSON-only output checklist

- No Markdown or prose outside the JSON object.
- Preserve the user's exact top-level keys and enum values.
- Escape quotes/newlines correctly.
- Use repository-relative paths and integer line numbers.
- Mention passed commands, skipped integration checks, missing GitHub checks, and clean worktree state in the verification string.
