---
name: go-hexagonal-api
description: Use when building Go backend APIs, spec-first hexagonal.
version: "1.0"
author: "product-owner profile (PO)"
license: "internal"
metadata:
  hermes:
    tags: [go, golang, fiber, hexagonal, mongodb, jwt, grpc, api, spec-first]
    related_skills: [po-requirements-elicitation, test-driven-development]
---

# Go Hexagonal API (spec-first)

## When to Use
- A Go service needs a spec-first build (REST via Fiber v3, gRPC, MongoDB, JWT)
- Refactoring or migrating an existing Go HTTP adapter (e.g., stdlib → Fiber)
- Interview/portfolio Go API work where reviewer friction and bonus items matter

## Triggers
- Building or refactoring a Go backend API (REST, gRPC, or both)
- Interview-challenge services, Panomete business services, Deerngo-style bots
- Any "create the spec first, then implement" request for a Go service

## User's standing rules (start here — these prevent corrections)
1. **Spec first.** Write the spec package in `<repo>/.agents/spec/` from templates at `F:\projects\project_spec\template\` BEFORE writing code. Grill the user on open decisions (scope, bonus items, framework) — never silently pick. See `references/spec-package-layout.md`.
2. **Fiber v3 for REST**, not stdlib `net/http`. Framework choice must be an explicit **ADR in the architecture doc** — the user rejected a silent stdlib default ("you skip the project decision and goes straight to the mux"). gRPC stays native grpc-go.
3. **Module path = repo name** (`github.com/<user>/<repo>`); rename everywhere (go.mod, imports, proto go_package, Makefile `--go_opt=module=`) and regenerate protobuf when it changes.
4. **Clean-code authority = the user's vault notes.** Audit against them before claiming done:
   - `F:\obsidian_note\swe-knowledge\computing-foundation-note\Clean Code Simplify\` — functions <20 lines, 0–3 params (parameter objects for 4+), no boolean params, rule of three for duplication, no dead/speculative code, DRY.
   - `F:\obsidian_note\swe-knowledge\checklist\api-checklist\fiber-v3-api.md` — Fiber checklist with tier matrix; apply per tier (prototype: skip OTel/Swagger/helmet/rate-limit/Viper).
5. **Comment policy:** one-line doc per exported symbol (golint) + why-rationale comments (security, races, design decisions). NO section markers (`// ---- x ----`), no restatements of code, no dead code. Tests keep intent comments.
6. TTL is signing policy → lives in the JWT manager, not passed per call. One verifier shared by REST middleware and gRPC interceptor.

## Workflow (proven sequence)
1. Spec package: `000 index` (assumptions table A1..An) → `011 business objectives` (evaluation criteria → objectives) → `025 architecture` (package tree + ADRs) → `022 API spec` + `023 DB schema` → `012/013 stories/ACs` → `041 test plan` → `015 DoD` → `031 README guide`.
2. Environment audit with batched parallel terminal calls: `go version`, docker daemon (`docker info`), protoc/grpcurl, port conflicts.
3. Implement in dependency order: domain (stdlib-only) → application (ports + services) → infrastructure adapters (mongo, auth, httpapi, grpcapi) → worker → main. Compile only when a layer is complete; `go get` early and check real API signatures with `go doc`.
4. Tests alongside: hand-written fakes in `testutil/` (no mock lib — challenge-safe), **external** test packages (`package foo_test`).
5. Gates: `gofmt -l -w . && go vet ./... && go test -race -cover ./...`
6. Container rebuild + live smoke script + grpcurl + graceful-shutdown check (must exit 0).
7. Sync spec docs to the shipped code (assumptions, ADRs, status checkboxes, README copy at repo root).

## Pitfalls (each cost real debugging time)
- **Internal test packages can't import testutil** when testutil imports the package under test → import cycle. Fix: `package foo_test` (external).
- **mongo-driver v2 breaking changes** — see `references/mongo-driver-v2.md`.
- **Fiber v3 breaking changes** — see `references/fiber-v3-api.md` (BodyParser/UserContext gone, no auto-405, etc.).
- **ID/format validation lives in the domain**, not the persistence adapter — a fake repo bypasses adapter checks and turns 400s into 404s.
- **grpcurl fails without gRPC reflection** registered on the server ("does not support the reflection API"). One `reflection.Register(srv)` line; grpcurl then discovers descriptors.
- **protoc on Windows** without choco/scoop: curl the release zip (`protoc-<ver>-win64.zip`) into a gitignored `tools/`; use `--go_opt=module=<module>` for clean `gen/` output (with `paths=source_relative` you get `gen/proto/...`).
- **make run must load .env**: `set -a && . ./.env && set +a && go run ./cmd/api` — GNU make on Windows runs sh and each recipe line is a separate shell, so chain with `&&` on one line.
- **Duplicate email**: friendly pre-check for 409 + unique index as the race-proof backstop (do both).
- **JWT**: pin HS256 via `WithValidMethods`; identical 401 body for wrong-email and wrong-password (no enumeration); `JWT_SECRET` ≥32 bytes fail-fast at startup; hash never in responses.
- **Graceful shutdown order**: signal → stop accepting → drain (Fiber `ShutdownWithContext` / gRPC `GracefulStop` with timeout fallback) → cancel worker ctx → disconnect DB → exit 0.

## Verification gates (before claiming done)
- gofmt/vet/build clean; `go test -race` all green; core coverage ≥80% (Mongo adapter excluded — documented honest "mock where appropriate" story)
- `docker compose up --build` → healthz 200 → smoke script all pass → grpcurl Create/Get + missing-token `Unauthenticated`
- Logs show `method/path/status/duration_ms` + `request_id`; worker logs `total_users` each interval
- `docker stop` → "shutdown complete", exit code 0

## References
- `references/spec-package-layout.md` — template numbering + doc map for a Go API
- `references/fiber-v3-api.md` — Fiber v3.5 API surface and migration gotchas
- `references/mongo-driver-v2.md` — driver v2 breaking changes and patterns
- `templates/smoke.sh` — REST smoke-script starter (curl + grep, no jq dependency)
