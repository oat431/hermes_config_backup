---
name: go-backend-service
description: Use when building or extending a Go backend service.
---

# Go Backend Service (hexagonal, MongoDB, JWT, gRPC)

Covers REST + gRPC Go services with MongoDB persistence and JWT auth, built hexagonal, tested with fakes, shipped via Docker — including the user's spec-first delivery loop and the mongo-driver v2 / gRPC / Windows pitfalls.

## When to use
- Building a Go service from scratch (interview challenge, Panomete business service, Deerngo-style backend)
- Adding REST/gRPC endpoints, Mongo persistence, or JWT auth to an existing Go service
- Build/test failures in a Go + MongoDB + gRPC stack

## Delivery loop (user convention: spec first)
1. Write the spec package first into the repo itself: `<repo>/.agents/spec/` with numbered subfolders mirroring `F:\projects\project_spec\template\` (01_requirement, 02_design, 03_construction, 04_testing). Keep interview specs lean — 9-10 docs, no enterprise ceremony.
2. Resolve genuine forks with the `clarify` tool before writing docs (e.g. bonus scope). One question per fork.
3. Implement in dependency order: scaffold → domain → application → adapters → main → tests → docker verify. Commit per phase with scoped messages.
4. Module path: use `github.com/<owner>/<repo-name>`; renaming later is one `sed` pass + proto regen (user does rename to match repo — see Pitfalls).

## Architecture (hexagonal)
```
cmd/api/main.go          # composition root: config → mongo → services → servers → worker → shutdown
internal/
  domain/                # entities, validation rules, sentinel errors — STDLIB ONLY, no bson tags
  application/           # use cases + ports (interfaces). No framework imports.
  infrastructure/
    mongodb/             # adapter implements application.UserRepository
    auth/                # bcrypt hasher + HS256 JWT manager
    httpapi/             # REST adapter: router, handlers, middleware, error envelope
    grpcapi/             # gRPC adapter: server + JWT metadata interceptor (same core as REST)
    config/              # env vars, fail-fast validation at startup
    logger/              # slog JSON handler
  worker/                # background jobs (ticker loops, ctx cancellation)
testutil/                # hand-written fakes (no mock library)
proto/ + gen/            # protobuf definitions + generated code (committed)
```
Dependency rule: domain → nothing; application → domain + ports; infrastructure → application/domain; main wires everything.

## Hard-won pitfalls

1. **mongo-driver v2 API broke from v1** — `bson/primitive` is GONE: `ObjectID`, `ObjectIDFromHex`, `NilObjectID` live in `bson` directly. `mongo.Connect(opts...)` takes NO ctx. After `go get`, run `go mod tidy` or go.sum is missing transitive entries (snappy, scram, x/sync). Full map in `references/mongo-driver-v2-api.md`.
2. **Import cycle with test doubles** — `testutil` imports `application` (for port interfaces), so application tests must be EXTERNAL: `package application_test` + qualify exported names. Internal tests (`package application`) importing testutil = `import cycle not allowed in test`.
3. **Validation rules live in domain, not adapters** — ObjectID shape check as regex `^[0-9a-fA-F]{24}$` in domain; otherwise fake-repo tests and the Mongo adapter diverge (404 vs 400). Same for email/name rules via `domain.ValidateEmail`/`ValidateName` reused by create AND update paths.
4. **grpcurl needs reflection** — `reflection.Register(grpcSrv)` or grpcurl cannot discover the service. Reviewers use grpcurl first.
5. **protoc on Windows without choco/scoop** — curl the win64 release zip into a gitignored `tools/protoc/`; install the Go plugins with `go install`. Use `--go_out=. --go_opt=module=<modpath>` (NOT `paths=source_relative`, which dumps output under `gen/proto/...`). Full recipe in `references/golang-grpc-setup-windows.md`.
6. **JWT details reviewers check** — pin alg via `jwt.WithValidMethods([]string{"HS256"})`; identical 401 body for wrong email AND wrong password (no user enumeration); password hash never in responses; `JWT_SECRET` ≥32 bytes enforced at startup (fail-fast).
7. **Go 1.22+ stdlib routing** — `mux.HandleFunc("POST /api/v1/users/{id}", ...)` + `r.PathValue("id")`; ServeMux auto-405s wrong methods. Zero web-framework deps reads as idiomatic.
8. **Email uniqueness race** — lowercase-normalize at the service boundary (create + login); pre-check FindByEmail for a friendly 409 AND unique index as the race-proof backstop (`mongo.IsDuplicateKeyError` → domain error).
9. **Terminal guard flags `docker compose up`** as a server start → run it with `background=true` + process wait; verify readiness with a separate health-poll loop. `docker stop` for shutdown tests is fine.
10. **git-bash + make** — `make run` must load .env itself: `set -a && . ./.env && set +a && go run ./cmd/api` (single line). Long curl `&&` chains hit transient exit-23 pipe failures → run steps as separate commands.

## Verification checklist (real tool output required, never prose-only)
- `go test -race -cover ./...` all green; core packages ≥80% (Mongo adapter 0% is acceptable and documented as integration-only)
- `docker compose up --build` → healthcheck 200 on both API ports
- `bash scripts/smoke.sh` → full REST matrix passes
- grpcurl: `list` (reflection), authed RPC returns data, no-token → `Unauthenticated`
- Container logs: middleware lines (method/path/status/duration_ms) + worker `total_users` ticks
- Graceful shutdown: `docker stop` → logs end with `shutdown complete`, exit code 0

## Support files
- `references/mongo-driver-v2-api.md` — v1→v2 breaking-change map + working snippets
- `references/golang-grpc-setup-windows.md` — protoc install, codegen modes, reflection, bufconn test pattern
