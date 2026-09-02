# Fiber v3 API surface & migration gotchas

Verified against fiber v3.5.0 (2026-08). Fiber v3 requires Go 1.22+.

## Breaking changes vs Fiber v2 (all burned turns to discover)
| v2 pattern | v3 reality |
|---|---|
| `c.BodyParser(&req)` | **REMOVED** → `c.Bind()` returns a `*fiber.Bind` struct with `.Body()`, `.JSON()`, `.Query()`, etc. For strict control, decode `c.Body()` yourself with your own `json.Decoder` |
| `c.QueryParser`, `c.ParamsParser`, `c.AllParams` | replaced by the `Bind` API |
| `c.UserContext()` | **REMOVED** → `c.Context()` returns `context.Context` (Ctx itself also implements context.Context) |
| `requestid.HeaderXRequestID` | constant moved → **`fiber.HeaderXRequestID`** |
| `fiber.Config.DisableStartupMessage` | **removed in v3** (no equivalent; use your own startup logs) |
| `fiber.Config.JSONDecoder` | still exists (`utils.JSONUnmarshal`) but the Bind API doesn't obviously honor it — prefer explicit decoding |

## Patterns that work
### Central error envelope via ErrorHandler
```go
app := fiber.New(fiber.Config{
    AppName:   "my-api",
    Immutable: true,             // checklist: freeze config after start
    BodyLimit: 1 << 20,
    ErrorHandler: errorHandler,  // every returned error lands here
})
```
- Handlers `return err`; `errorHandler(c fiber.Ctx, err error)` maps: your own `*apiError{status, code, message, details}` (full envelope with field details) → `*fiber.Error` (status+message only; map 404/405/400 to envelope codes) → domain sentinel errors.
- `fiber.Error` can't carry an error *code* or details — that's why you need your own apiError type for the `{"error":{"code","message","details"}}` contract.

### Strict body decoding (unknown-field rejection)
```go
func decodeJSON(c fiber.Ctx, dst any) error {
    dec := json.NewDecoder(bytes.NewReader(c.Body()))
    dec.DisallowUnknownFields()   // keeps password-smuggling out of updates
    if err := dec.Decode(dst); err != nil { return badRequest("Malformed request body") }
    return nil
}
```

### No automatic 405 — register it yourself
Fiber falls through to 404 on method mismatch. Per the fiber checklist, add explicit handlers:
```go
methodNotAllowed := func(c fiber.Ctx) error {
    return &apiError{status: fiber.StatusMethodNotAllowed, code: "METHOD_NOT_ALLOWED", ...}
}
app.All("/path", methodNotAllowed)   // one per path that has specific methods
// plus a catch-all 404 at the end:
app.Use(func(c fiber.Ctx) error { return &apiError{status: 404, code: "NOT_FOUND", ...} })
```

### Middleware chain order (user's checklist)
`requestid.New()` → custom slog logger → `recover.New()` → route groups.
- Custom slog middleware: `start := time.Now(); err := c.Next(); log.Info("http request", "method", c.Method(), "path", c.Path(), "status", c.Response().StatusCode(), "duration_ms", ..., "request_id", c.GetRespHeader(fiber.HeaderXRequestID))`
- JWT on groups: `users := v1.Group("/users"); users.Use(requireAuth(auth))`. Use a **custom** middleware calling your shared verifier (not `jwtware`) when REST and gRPC must share one auth path.

### Graceful shutdown & serving
```go
go func() { if err := app.Listen(":" + port); err != nil { serverErr <- err } }()
// on signal:
app.ShutdownWithContext(ctx)   // drain + close; ctx carries the timeout
```

### In-process tests
```go
resp, err := app.Test(httptest.NewRequest(method, path, body), fiber.TestConfig{Timeout: 5 * time.Second})
// resp is *http.Response; read with io.ReadAll(resp.Body); assert resp.StatusCode
```
`httptest.NewRequest` works — no real listener needed. Note: goroutine leak detector may flag recover middleware tests; `t.Cleanup(app.Shutdown)` helps.

## User's Fiber checklist
`F:\obsidian_note\swe-knowledge\checklist\api-checklist\fiber-v3-api.md` — includes a tier matrix (POC→Mission-Critical). For prototype/interview tier: ✅ error handler, immutable, body limit, groups, 405/404 handlers, slog, app.Test, graceful shutdown. ❌ OTel, Swagger, helmet, CORS, rate limiter, Viper, cache — skip and document as out of tier.
