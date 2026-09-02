---
name: go-backend-api
description: "Use when building Go backend APIs: hexagonal, Mongo, JWT."
version: "1.0"
author: "PO"
license: "internal"
metadata:
  hermes:
    tags: [golang, hexagonal, mongodb, jwt, grpc, docker, clean-code, backend]
    related_skills: [spec-document-elicitation, requesting-code-review]
---

# Go Backend API Development

## When to Use

- Building or scaffolding a Go HTTP/gRPC service, especially with MongoDB, JWT auth, Docker.
- Refactoring or auditing Go code for cleanliness (user's Clean Code Simplify notes).
- Adding a gRPC bonus server, dockerizing, or setting up a verification pipeline (tests → smoke → grpcurl → shutdown check) for a Go service.

## Trigger

User asks to build, scaffold, refactor, or audit a Go backend service (REST/gRPC) — interview coding challenges, microservices, anything involving MongoDB + JWT + Docker.

## Architecture (the user's preferred pattern)

Hexagonal, stdlib-first, minimal deps:

```
cmd/api/main.go          # composition root: config, wiring, servers, worker, shutdown
internal/
  domain/                # pure entity + validation + sentinel errors (stdlib ONLY)
  application/           # use cases + ports (interfaces); no framework imports
  infrastructure/
    mongodb/             # official-driver adapter behind UserRepository port
    auth/                # bcrypt + JWT (HS256) adapters
    httpapi/             # REST: ServeMux (Go 1.22+ method+path patterns), handlers, middleware
    grpcapi/             # gRPC server + unary auth interceptor (same application core)
    config/              # env vars, fail-fast validation at startup
    logger/              # slog JSON
  worker/                # background goroutines (ctx-cancelled)
testutil/                # hand-written fakes (NO mock library) — repository + hasher
scripts/smoke.sh         # end-to-end verification against running stack
```

Dependency-ordered build (each step compiles before the next):
1. domain → 2. application ports + services → 3. adapters → 4. main + worker → 5. tests → 6. Docker/compose/smoke/README → 7. gRPC last if it's a bonus item.

## User conventions (do not re-negotiate)

- **Module name must match repo name** — the user WILL ask for a rename if it doesn't. Include proto `go_package` and Makefile `--go_opt=module=` in the rename.
- **Docs-first spec**: spec docs live in `.agents/spec/` using templates from `F:\projects\project_spec\template` (numbered: 011 business objectives, 012 user stories, 013 acceptance criteria, 015 DoD, 022 API spec, 023 DB schema, 025 architecture, 031 README guide, 041 test plan). Self-contained per-service folders.
- **Comments policy**: one-line docs on exported symbols + rationale comments ONLY (security, race conditions, design decisions). Remove section markers (`// ---- x ----`), restatements, verbose prose. User asked to trim comments — do it preemptively.
- **Clean-code audit**: user keeps checklists at `F:\obsidian_note\swe-knowledge\computing-foundation-note\Clean Code Simplify` (naming/functions, smells/refactoring, comments). When asked "is the code clean?", audit against THOSE notes (see references/clean-code-audit.md).
- **Commit discipline**: conventional messages (`feat:` / `refactor:` / `style:` / `docs:`), refactoring in its own commit, never mixed with features.
- **Evidence over claims**: never report done without real tool output — tests, smoke results, grpcurl output, docker logs, exit codes. Rebuild the container after ANY code change so the running stack matches the repo.

## Pitfalls (each cost real debugging time)

1. **mongo-driver v2 breaking changes** — there is NO `bson/primitive` package in v2: `ObjectID`/`ObjectIDFromHex`/`NilObjectID` live in `bson` directly; `mongo.Connect(opts...)` takes NO context (v1 did); `Ping`/`Disconnect` still take ctx. Verify signatures with `go doc` before writing main. Details: references/mongo-driver-v2-gotchas.md
2. **gRPC reflection is not optional** — grpcurl fails with "server does not support the reflection API" unless `reflection.Register(grpcSrv)` is called. It's a reviewer-experience win, always add it. Setup + bufconn tests: references/grpc-bonus-setup.md
3. **Go test import cycle** — an internal test (`package application`) importing `testutil` that imports `application` = cycle. Fix: external test package `package application_test` and qualify all references.
4. **Validation rules belong in the domain layer** — if the adapter validates (e.g. ObjectID parse), fakes bypass it and tests diverge from production behavior (404 vs 400). Domain gets `IsValidID` etc.; adapters keep their own checks only as defense.
5. **protoc output paths** — `paths=source_relative` produces `gen/proto/...` (ugly); use `--go_out=. --go_opt=module=<module-path>` for clean `gen/userservice/v1/`. `rm -rf gen` first.
6. **Windows/git-bash specifics** — Docker Desktop daemon must be running before compose (CLI alone errors on the npipe); Makefile env loading for local runs: `set -a && . ./.env && set +a && go run ./cmd/api`; `sed -i` works fine for mass renames.
7. **4-param functions** — the user's clean-code notes cap params at 3. Extract parameter objects (e.g. `UpdateUserInput{Name, Email *string}`) and move policy fields to their owner (JWT TTL belongs in the token manager, not call sites).

## Verification ladder (run all before claiming done)

1. `gofmt -l -w . && go vet ./... && go build ./...`
2. `go test -race -cover ./...` — all green; core packages ≥80% (domain/application/http/grpc/worker); mongo adapter legitimately 0% (integration-only, documented)
3. `docker compose up -d --build` → poll `/healthz` → `bash scripts/smoke.sh` (expect all pass)
4. gRPC: `grpcurl -plaintext localhost:50051 list` + authenticated call + missing-token → `Unauthenticated`
5. `docker logs`: request lines (method/path/status/duration) + worker ticks (`total_users`)
6. Graceful shutdown: `docker stop` → logs show "shutdown signal received" → worker stopped → "shutdown complete" → exit code 0
7. Commit; keep the stack running (restart if the shutdown test stopped it)

## References

- `references/mongo-driver-v2-gotchas.md` — v1→v2 API diff and error signatures
- `references/grpc-bonus-setup.md` — protoc install, proto generation, reflection, bufconn tests, grpcurl verification
- `references/clean-code-audit.md` — the user's checklist distilled + Go-specific smells and fixes
