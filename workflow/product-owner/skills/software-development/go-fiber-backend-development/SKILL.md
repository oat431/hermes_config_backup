---
name: go-fiber-backend-development
description: Use when building Go backend APIs (Fiber v3, Mongo, gRPC).
---

# Go Backend Development (User Stack: Fiber v3)

## When to Use

Any Go backend service work for this user: new API services, stack migrations (e.g. stdlib→Fiber), Go interview-challenge deliverables, or reviewing Go code from the Dev/QA/Security personas.

## Stack Contract (user's chosen stack — do NOT second-guess)

| Concern | Choice (user-confirmed) | Note |
|---------|-------------------------|------|
| REST framework | **Fiber v3** (`github.com/gofiber/fiber/v3`) | User explicitly overrode a stdlib `net/http` choice — never default back to stdlib/ServeMux |
| Architecture | Hexagonal (ports & adapters): `domain/` (stdlib-only) → `application/` (use cases + ports) → `infrastructure/` (adapters) | Domain package must have zero external imports |
| Persistence | Official `go.mongodb.org/mongo-driver/v2` behind a repository port | See `references/mongo-driver-v2-gotchas.md` |
| Auth | `golang-jwt/v5` HS256, `golang.org/x/crypto/bcrypt` | Custom JWT middleware, NOT `jwtware` — so REST + gRPC share one verifier |
| gRPC (bonus) | grpc-go on separate port + `reflection.Register` | Unary interceptor reads `authorization` metadata |
| Logging | stdlib `log/slog` JSON handler | method/path/status/duration_ms + request_id |
| Testing | stdlib `testing` + hand-written fakes (no mock lib, no testify) | Challenge/test convention: standard package |
| Ops | Multi-stage Dockerfile, docker-compose (app+mongo), Makefile, `.env` gitignored | Non-root runtime user |

## Project Layout (hexagonal, module = repo name)

```
cmd/api/main.go            # composition root: wiring + graceful shutdown (helpers: connectMongo/ensureIndexes/serveFiber/serveGRPC/shutdown)
internal/
  domain/                  # entities, validation rules, sentinel errors (stdlib-only)
  application/             # use cases + port interfaces (UserRepository, TokenManager, PasswordHasher)
  infrastructure/
    mongodb/ user_repo.go  # + user_repo_integration_test.go (//go:build integration)
    auth/    bcrypt.go jwt.go
    httpapi/ app.go handlers.go middleware.go errors.go
    grpcapi/ server.go     # + interceptor
    config/  logger/
  worker/                  # background jobs (interval injectable for tests)
testutil/                  # fake repo + fake hasher (external test packages to avoid import cycles)
proto/ + gen/              # protoc output (module= flag, commit generated code)
```

## Verification Gate Ladder (run in order, all must pass before commit)

1. `gofmt -l .` empty, `go vet ./...`, `go build ./...`
2. `go test -race -count=1 ./...` — all packages green
3. `go test -tags integration -race ./internal/infrastructure/mongodb/` (compose Mongo up; per-test throwaway DB)
4. `bash scripts/smoke.sh` vs live compose stack (REST + gRPC + 404/405 + container-health checks)
5. `grpcurl -plaintext ...` happy path + missing-token `Unauthenticated`
6. `docker stop <api>` → logs show clean shutdown, exit code 0
7. `go run golang.org/x/vuln/cmd/govulncheck@latest ./...` — 0 reachable (bump `go.mod` go directive/toolchain to clear reachable stdlib vulns)

## Pitfalls (details in references/)

- **Fiber v3 renames** — `c.BodyParser`→`c.Bind()`, `c.UserContext()`→`c.Context()`, `requestid.HeaderXRequestID`→`fiber.HeaderXRequestID`, no `DisableStartupMessage`. Full map: `references/fiber-v3-gotchas.md`
- **Fiber has no auto-405** — add explicit `app.All(path, methodNotAllowed)` for every path with specific methods (test will catch it)
- **BodyLimit → 413** — server-level `MaxRequestBodySize`; route `*fiber.Error` 413 through central `ErrorHandler` and map to a contract code (e.g. `REQUEST_TOO_LARGE`), never `INTERNAL_ERROR`
- **In-container healthchecks** — Fiber defaults to `ListenerNetwork: tcp4`; busybox `wget localhost` resolves `::1` → unhealthy. Use `fiber.ListenConfig{ListenerNetwork: fiber.NetworkTCP}`
- **mongo-driver v2** — `bson/primitive` package removed; `ObjectID` lives in `bson` directly; `mongo.Connect(opts...)` takes no ctx. Full map: `references/mongo-driver-v2-gotchas.md`
- **JWT hardening** — `jwt.WithValidMethods([HS256])` + `jwt.WithIssuer(...)` + `jwt.WithExpirationRequired()`; login timing oracle → dummy bcrypt compare on unknown email (identical 401 body for both failure paths)
- **Duplicate-email race** — friendly pre-check (409) + unique index as race-proof backstop; ID-shape validation in the domain layer so every adapter behaves identically
- **Docker secrets** — `.dockerignore` must exclude `.env`/`.git`/`.agents`/`tools/` or the real JWT secret lands in builder-image layers
- **Strict JSON decoding** — decode `c.Body()` with `json.Decoder.DisallowUnknownFields()` (rejects `password` smuggling on PUT update)
- **Import cycles in tests** — `testutil` imports `application`, so application tests must be external (`package application_test`)
- **Mermaid in spec docs** — see `references/mermaid-pitfalls.md` (braces/arrows in node labels break rendering)

## Spec-First Workflow (this user)

Write the spec package BEFORE code, using templates at `F:\projects\project_spec\template\` (numbered convention: 01_requirement/011, 02_design/022…, 04_testing/041, 07_pm/072_MM). Self-contained spec folder per service (e.g. `.agents/spec/`, proposals in `.agents/proposal/`). Cross-persona handoffs are meeting-minutes docs with DEC/ACT ids; contract changes route back to PO (DEC-H03 pattern) — personas polish HOW, never change WHAT.
