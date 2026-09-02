# Fiber v3 Migration Gotchas (v2 → v3, verified against v3.5.0)

API surface changed significantly between v2 and v3. Verified live during a stdlib→Fiber migration.

## Renamed / moved APIs

| v2 | v3 | Notes |
|----|----|-------|
| `c.BodyParser(&dst)` | `c.Bind().Body(&dst)` (v3.5+) or decode `c.Body()` yourself | Bind returns `*BindError`; `WithAutoHandling()` makes it return `*fiber.Error` 400 |
| `c.UserContext()` | `c.Context() context.Context` | Pass to services/DB calls |
| `requestid.HeaderXRequestID` | `fiber.HeaderXRequestID` | Const moved to the fiber package |
| `fiber.Config.DisableStartupMessage` | removed | No equivalent in v3.5 |
| `fiber.Config.JSONDecoder` | exists but prefer explicit decode | see strict-decode pattern below |

## Behavior & wiring pitfalls

- **No automatic 405.** A path registered under `GET` returns 404 (falls to catch-all) for other verbs unless you add explicit `app.All(path, methodNotAllowed)` for every method-specific path. Write a test for it — it will catch you.
- **BodyLimit → 413 path.** `Config.BodyLimit` sets fasthttp `MaxRequestBodySize` at server level; oversized bodies become `fasthttp.ErrBodyTooLarge` → `fiber.ErrRequestEntityTooLarge` → routed through `Config.ErrorHandler`. Map it to a contract code (`REQUEST_TOO_LARGE`), never `INTERNAL_ERROR`. Live curl of an oversized body may show connection-reset (server rejects mid-upload) — capture the envelope with a just-over-limit body or assert via unit test on the error handler.
- **Central ErrorHandler pattern:**
  ```go
  app := fiber.New(fiber.Config{ ErrorHandler: errorHandler, Immutable: true, BodyLimit: 1<<20, ... })
  // handlers return domain errors or *apiError; errorHandler renders the envelope:
  //   apiError -> its status/code; *fiber.Error -> switch on fe.Code (404/405/400/413); else map domain errors
  ```
- **Strict JSON decode** (unknown-field rejection, e.g. password smuggling on PUT):
  ```go
  dec := json.NewDecoder(bytes.NewReader(c.Body()))
  dec.DisallowUnknownFields()
  if err := dec.Decode(dst); err != nil { return badRequest("Malformed request body") }
  ```
  Do NOT rely on Fiber's default body binding — it does not reject unknown fields.
- **Dual-stack listener.** Fiber v3 defaults to `ListenerNetwork: tcp4`. In containers, `wget localhost:8080/healthz` (busybox) resolves to `::1` → connection refused → compose reports unhealthy while host probes pass. Fix: `app.Listen(":"+port, fiber.ListenConfig{ListenerNetwork: fiber.NetworkTCP})`.
- **In-process tests:** `app.Test(req, fiber.TestConfig{Timeout: 5*time.Second}) (*http.Response, error)` — no server needed; read body via `io.ReadAll`.
- **gRPC-style reflection:** `reflection.Register(grpcSrv)` so `grpcurl list` works without a local proto — zero-friction reviewer experience.
- **Middleware order** (requestid → slog logger → recover → routes) and `c.GetRespHeader(fiber.HeaderXRequestID)` inside the logger for `request_id`.
- **Graceful shutdown:** `app.ShutdownWithContext(ctx)`; fall back to `grpcSrv.Stop()` after a timeout in the gRPC half.
