# Issue-driven Go + PostgreSQL PR recipe

Use this reference after a repository bootstrap when implementing a PO-created backend issue on Windows with Go, Docker PostgreSQL, and a `develop`-targeted PR.

## 1. Sync and branch

From the repository root:

```bash
git status --short --branch
git remote -v
git fetch origin
git checkout develop
git pull --ff-only origin develop
git checkout -b feat/issue-<N>-<short-name>
```

If Git reports a Windows dubious-ownership error for a trusted project path, add the exact repository path as a safe directory (or use the narrowly scoped `-c safe.directory=...` form) before continuing. Do not disable repository safety globally with a broad wildcard unless the user explicitly accepts that risk.

## 2. Verify the database without exposing secrets

Inspect service state and readiness without printing password values:

```bash
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}'
docker exec local-postgres pg_isready -U postgres
docker exec local-postgres psql -U postgres -Atc "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;"
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' local-postgres \
  | grep -E '^POSTGRES_(USER|PASSWORD|DB)=' \
  | sed 's/=.*/=<redacted>/'
```

Create an isolated test database only if it does not exist. Apply the repository migration to the isolated database, not to production data. Prefer a local Unix-socket connection from a test binary running in the PostgreSQL container when host password authentication is unavailable or intentionally not configured:

```text
postgres:///deerngo_test?host=/var/run/postgresql&user=postgres&sslmode=disable
```

If a host DSN fails with password authentication, do not weaken PostgreSQL auth or print credentials. Use the container-local socket route or the project’s configured local credential mechanism.

## 3. Implement as a vertical slice

For a registration endpoint, keep the layers explicit:

```text
Fiber handler → service validation/normalization → sqlx repository → PostgreSQL migration
```

Write tests around the contract first and use small in-memory stubs for handler/service tests. Add a real PostgreSQL integration test for the repository and HTTP route when the local database is available.

Important contract details to preserve:

- Validate all required fields and return `VALIDATION_ERROR` with field-level details.
- Parse timestamps as RFC3339/ISO 8601.
- Validate the API input source (`streamer_bot`) while allowing the service contract to support the future `youtube_api` scheduler.
- Normalize handles for storage (trim, lowercase, remove one leading `@`) but return the public representation expected by the API.
- Use `INSERT ... ON CONFLICT` with `LEAST(existing.subscribed_at, excluded.subscribed_at)` so the earliest timestamp survives.
- Return `201` for a created row and `200` with explicit upsert metadata for an existing row.
- Return a generic `INTERNAL_ERROR`; never expose SQL, credentials, or connection details.

## 4. Verification matrix

Run all of these before commit/PR:

```bash
make fmt
make test
make vet
make build
go test -race ./...
git diff --check
docker compose config
```

Then run the real database tests. If the test package must run inside the PostgreSQL container to use peer/socket authentication, compile a Linux test binary, copy it into the container, execute it with the socket DSN, and remove the temporary binary afterward. Record the test names and PASS output in the issue and PR.

Also perform an HTTP smoke test against the running app when practical. A smoke test must assert the actual status/body (for example, `201` on first registration and `200` on a duplicate), not merely that the process starts.

## 5. PR and issue evidence

Use a Conventional Commit with the issue reference, push the issue-traceable branch, and create the PR against `develop`:

```bash
git push -u origin feat/issue-<N>-<short-name>
gh issue comment <N> --repo owner/repo --body-file evidence.md
gh pr create --repo owner/repo --base develop --head feat/issue-<N>-<short-name> ...
```

Verify the PR URL, base/head branches, remote commit, and issue comment through `gh` after creation. If `gh pr checks` reports that no checks exist, state exactly that; local verification is not GitHub CI. Stop at the PR unless merge/deploy is explicitly authorized.
