---
name: go-fiber-api-server
description: "Use when building Go Fiber v3 HTTP APIs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [go, fiber, http-api, middleware, rate-limit, validation, qa]
    related_skills: [test-driven-development, go-background-scheduler-api-poller, github-pr-workflow]
---

# Go Fiber v3 API Server

## Trigger

Building or extending a Fiber v3 HTTP API (Fiber is fasthttp-based; route
groups + middleware). Covers the API-layer patterns that survive QA review:
rate-limit tiers, validation contract shapes, error logging, and integration
test gates.

## Critical pitfall: group middleware inherits to ALL sub-paths

`app.Group("/api/v1", rateLimit(100))` applies the middleware to EVERY route
under `/api/v1`, including `/api/v1/webhooks/*`. A later group
`app.Group("/api/v1/webhooks", rateLimit(200))` ADDS a second limiter — it
cannot remove the inherited 100/min one. Result: webhook requests hit 429 at
request 101, not 201. QA verified this with a live probe.

Fix: exclude the path from the outer limiter via `Config.Next`:

```go
standardAPI := app.Group("/api/v1", rateLimit(100, isWebhookPath))
// ... standard routes ...

webhookAPI := app.Group("/api/v1/webhooks", rateLimit(200))
webhookAPI.Post("/easydonate", handler.NotImplemented)

func isWebhookPath(c fiber.Ctx) bool {
    return strings.HasPrefix(c.Path(), "/api/v1/webhooks")
}

func rateLimit(max int, skip ...func(c fiber.Ctx) bool) fiber.Handler {
    cfg := limiter.Config{Max: max, Expiration: time.Minute, /* LimitReached: 429 JSON */ }
    if len(skip) > 0 {
        cfg.Next = skip[0]
    }
    return limiter.New(cfg)
}
```

Rate-limit tiers must be sibling groups with disjoint prefixes, or
path-excluded via `Next` — never nested groups with different limits.

## Rate-limit boundary tests

Test the exact contract: N requests pass, N+1 returns 429 with the documented
error code body (e.g., `RATE_LIMITED`):

```go
// standard: requests 1-100 → 201, request 101 → 429
// webhook:  requests 1-200 → 501 (scaffold), request 201 → 429
```

Each test builds its own `fiber.New()` app → fresh in-memory limiter state, so
the per-IP counter does not leak between tests.

## Validation contract: separate required vs length messages

QA rejects combined messages like "This field is required and must be 100
characters or less". The API spec expects field-specific messages:

- top-level: `youtube_handle is required`
- detail:    `This field is required`
- length:    `youtube_handle must be 100 characters or less` /
             `This field must be 100 characters or less`

Implement separate branches (required → length) plus a small mapping function
for the top-level message, and assert the EXACT response shape in tests —
not substring matches.

## Internal errors: log full, respond generic

Log the real error server-side with slog, return a generic `INTERNAL_ERROR`
to the client, and never include the error text or DSN in the response.
Inject a logger via varargs so tests can assert the log line without touching
stdout:

```go
var logs bytes.Buffer
logger := slog.New(slog.NewTextHandler(&logs, nil))
handler := NewSubscriberHandler(stub, logger)
// ... trigger error path ...
if !strings.Contains(logs.String(), "subscriber registration failed") { ... }
```

## Health endpoint exemption

Health/readiness (`/healthz`, `/`) are usually excluded from API rate limits
so container probes don't burn quota. Document the exemption in code comments
— QA accepts it when explicitly documented.

## Integration gate & CI

- Keep `t.Skip` guards in DB tests for dev machines, but make the Makefile
  integration target fail fast when `DEERNGO_TEST_DATABASE_URL` is missing.
- GitHub Actions: PostgreSQL service container + migration + `make test-integration`.
- Cross-package DB tests: unique UUID handles, no shared TRUNCATE, `-p=1`.
  Full recipe: see `go-background-scheduler-api-poller` →
  `references/windows-docker-postgres-integration-testing.md`.

## Verification

```bash
make fmt && make test && make vet && make build
go test -race -count=1 ./...
git diff --check
```

## Critical pitfall: Fiber listens on tcp4 only — docker healthchecks fail

Fiber v3's default `ListenerNetwork` is `NetworkTCP4` (IPv4). In-container
healthchecks that hit `localhost` (which busybox wget/alpine resolves to
`::1` first) get **connection refused**, so the compose healthcheck goes
`unhealthy` even though the app serves fine from the host (port forward is
IPv4). stdlib net/http listens dual-stack by default, so migrating an
existing net/http service to Fiber silently breaks this.

Fix at the Listen call site (NOT `fiber.Config` — v3 moved it):

```go
app.Listen(":8080", fiber.ListenConfig{ListenerNetwork: fiber.NetworkTCP})
```

Verify with `/proc/net/tcp6` inside the container: port must appear as an
`0A` (LISTEN) entry. Alternative fix: point the healthcheck at
`127.0.0.1` instead of `localhost`.

## Server timeouts & pool bounds

`fiber.Config` has `ReadTimeout`/`WriteTimeout`/`IdleTimeout` (defaults:
unlimited — set them). fasthttp starts WriteTimeout when request headers
are read, so it must cover handler work (bcrypt, DB round-trips); make it
larger than ReadTimeout. For Mongo, set `SetMaxPoolSize`/`SetMinPoolSize`/
`SetServerSelectionTimeout` on `options.Client()` — driver defaults are
max 100 / min 0 / 30s selection.

## Pitfalls

- Nested route groups with different rate limits — the outer limiter wins.
- Substring assertions on validation messages — QA checks exact shape.
- Logging error details to the client — never leak DSN/credentials.
- Forgetting the health exemption documentation — QA flags it as a finding.
- Fiber on tcp4 only — in-container `localhost` healthchecks refused (see above).
