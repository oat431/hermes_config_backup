# Fiber v3 Rate-Limit Patterns for Tiers

## The prefix-inheritance trap

When you need different rate-limit tiers on the same prefix hierarchy
(e.g., 100/min for `/api/v1/*` but 200/min for `/api/v1/webhooks/*`),
Fiber's `app.Group(prefix, middleware)` inherits middleware to all nested
paths. The second group's middleware cannot remove the first's.

### Wrong — webhook is capped at 100/min

```go
// This applies rateLimit(100) to ALL /api/v1/* paths, including webhooks.
standardAPI := app.Group("/api/v1", rateLimit(100))
standardAPI.Post("/subscribers", handler.Create)
standardAPI.Get("/points/:handle", handler.Points)

// This group ALSO inherits the 100/min limiter from above.
// The 200/min limiter below fires AFTER the 100/min one has already run.
webhookAPI := app.Group("/api/v1/webhooks", rateLimit(200))
webhookAPI.Post("/easydonate", handler.Webhook)
// Result: /api/v1/webhooks/easydonate returns 429 at request 101, not 201.
```

### Correct — use Next() to skip nested paths

```go
// isWebhookPath lets the standard limiter skip webhook routes.
func isWebhookPath(c fiber.Ctx) bool {
	return strings.HasPrefix(c.Path(), "/api/v1/webhooks")
}

// Standard tier: 100/min, but skips webhook paths.
standardAPI := app.Group("/api/v1", rateLimit(100, isWebhookPath))
standardAPI.Post("/subscribers", handler.Create)

// Webhook tier: 200/min — only limiter that fires for these paths.
webhookAPI := app.Group("/api/v1/webhooks", rateLimit(200))
webhookAPI.Post("/easydonate", handler.Webhook)
```

### Correct — non-overlapping prefixes (alternative)

```go
standardAPI := app.Group("/api/v1/subscribers", rateLimit(100))
standardAPI.Post("/", handler.Create)

// No inheritance because the prefix doesn't contain the other group's prefix.
webhookAPI := app.Group("/api/v1/webhooks", rateLimit(200))
webhookAPI.Post("/easydonate", handler.Webhook)
```

## Configurable limiter factory

```go
func rateLimit(max int, skip ...func(c fiber.Ctx) bool) fiber.Handler {
	cfg := limiter.Config{
		Max:        max,
		Expiration: time.Minute,
		LimitReached: func(c fiber.Ctx) error {
			return c.Status(fiber.StatusTooManyRequests).JSON(fiber.Map{
				"error": fiber.Map{
					"code":    "RATE_LIMITED",
					"message": "Too many requests",
				},
			})
		},
	}
	if len(skip) > 0 {
		cfg.Next = skip[0]
	}
	return limiter.New(cfg)
}
```

## Boundary tests

Always test the exact tier boundary through the real Fiber route, not the
middleware factory alone:

```go
func TestWebhookRateLimitAllows200RequestsThen429(t *testing.T) {
	app := server.New(config.Config{})

	// Requests 1-200: must succeed (webhook tier = 200/min).
	for i := 1; i <= 200; i++ {
		req := httptest.NewRequest("POST", "/api/v1/webhooks/easydonate", strings.NewReader(`{}`))
		resp, err := app.Test(req)
		// assert 501 (NotImplemented) or 200, NOT 429
	}

	// Request 201: must be rate-limited.
	req := httptest.NewRequest("POST", "/api/v1/webhooks/easydonate", strings.NewReader(`{}`))
	resp, _ := app.Test(req)
	// assert 429 + RATE_LIMITED
}
```

Without a boundary test, the prefix-inheritance trap is invisible — the route
"works" until the 101st request returns 429 instead of the 201st.

## Health/readiness exemption

`/healthz` and `/` are intentionally exempt from rate limiting so container
probes don't burn API quota. Document the exemption explicitly in code comments
and cite Security Standard §7.1 if applicable.
