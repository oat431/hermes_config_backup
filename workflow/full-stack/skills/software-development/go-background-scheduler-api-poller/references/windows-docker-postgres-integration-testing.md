# Windows → Docker PostgreSQL Integration Testing

Context: Go tests that need a real PostgreSQL run on a Windows host where the
database lives in a Docker container (e.g., `local-postgres`). The host binary
cannot reach the container's Unix socket, and the DSN password may be an
unknown secret you must never print.

## The pattern: cross-compile → docker cp → run inside the container

1. Build Linux test binaries from Windows:

```bash
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go test -c -o bin/deerngo-repository.test ./internal/repository
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go test -c -o bin/deerngo-server.test ./internal/server
```

2. Copy into the postgres container (same network namespace → socket reachable):

```bash
docker cp bin/deerngo-repository.test local-postgres:/tmp/deerngo-repository.test
docker exec local-postgres chmod +x /tmp/deerngo-repository.test
```

3. Run with a Unix-socket DSN — no password needed (local socket trust):

```bash
docker exec -e DEERNGO_TEST_DATABASE_URL='postgres:///deerngo_test?host=/var/run/postgresql&user=postgres&sslmode=disable' \
  local-postgres /tmp/deerngo-repository.test -test.v
```

4. Clean up: `docker exec local-postgres rm -f /tmp/...` and `rm -f bin/...`.

Why not `go test` on the host? The DSN would need the container's
POSTGRES_PASSWORD (a secret), and the Windows binary cannot use the Linux
socket path. Running inside the container avoids both.

## Integration test isolation (cross-package parallelism)

When two test packages (e.g., `repository_test` and `server_test`) both touch
the same table:

- NEVER `TRUNCATE` a shared table from both packages — `go test -p=N` runs
  packages in parallel and interleaved TRUNCATE + fixed fixtures (e.g.,
  `viewer1`) produce false failures: first upsert returns `created=false`,
  HTTP 200 instead of 201, missing rows. QA reproduced this with
  `go test -p=2 -count=100`.
- Use unique per-test handles and drop TRUNCATE entirely:

```go
func uniqueHandle(t *testing.T) string {
    t.Helper()
    return "repo_" + uuid.New().String()[:8]   // or "server_" + ...
}
```

- In the Makefile integration target, add `-p=1` to force serial packages:

```make
test-integration:
	@test -n "$(DEERNGO_TEST_DATABASE_URL)" || (echo "DEERNGO_TEST_DATABASE_URL is required" >&2; exit 1)
	DEERNGO_TEST_DATABASE_URL="$(DEERNGO_TEST_DATABASE_URL)" go test -p=1 -count=1 -v ./internal/repository ./internal/server
```

- Keep the `t.Skip` guard for dev machines, but gate the CI path: the Makefile
  target fails fast when the DSN is missing, and the GitHub Actions workflow
  supplies a PostgreSQL service so `make test-integration` always runs in CI.
  A green CI run must never be able to skip DB verification silently.

## CI workflow (PostgreSQL service container)

```yaml
services:
  postgres:
    image: postgres:18
    env:
      POSTGRES_DB: deerngo_test
      POSTGRES_PASSWORD: test
    ports: ["5432:5432"]
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
# steps: gofmt check → go vet → apply migration
#        (psql "$DATABASE_URL" -v ON_ERROR_STOP=1 < migrations/001_*.up.sql)
#        → go test -race → make test-integration → go build
```

## Windows line-ending gotchas

`go mod tidy -diff` on Windows may report EVERY go.sum line changed — that is
CRLF↔LF normalization, not a real content diff. `git add` then
`git diff --cached` shows the true delta. Don't chase it as a dependency
change.

`gofmt -w` (e.g., `make fmt`) rewrites every .go file with LF endings, so
`git status` shows a dozen files as modified — but `git diff` is EMPTY. That
means it's pure line-ending noise, not real changes. Fix:

```bash
git restore .        # safe when git diff shows no content changes
```

Check `git diff --numstat`/`git diff <file>` first to confirm emptiness
before restoring — never blindly restore when real changes are uncommitted.

## MSYS2/git-bash HTTPS quirks

- **Python `urllib` fails SSL** in MSYS2 (`SSL: CERTIFICATE_VERIFY_FAILED` —
  the MSYS2 Python lacks a CA cert bundle). Use **curl** for HTTPS calls from
  the terminal instead (git-bash curl has proper certs).
- **`/tmp` does not map for Go tooling** — `go run /tmp/foo.go` fails with
  `GetFileAttributesEx /tmp/...: file not found`. Use a repo-local temp dir
  (e.g., `./tmp-...`) or drive-letter paths for anything Go reads/writes.
  Docker's `/tmp` (inside a container) works fine — only the MSYS `/tmp` is
  problematic for Go.
