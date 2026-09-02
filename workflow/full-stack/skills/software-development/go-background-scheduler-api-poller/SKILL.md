---
name: go-background-scheduler-api-poller
description: "Use when building a Go background API-poller scheduler."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [go, scheduler, background-goroutine, api-poller, oauth, external-integration, tdd]
    related_skills: [test-driven-development, github-pr-workflow, systematic-debugging]
---

# Go Background Scheduler — External API Poller

## Trigger

Use when implementing a Go background scheduler goroutine that periodically
polls an external API (YouTube Data API, EasyDonate REST API, etc.) with:
- OAuth 2.0 refresh-token exchange for access tokens
- Structured error classification (403 quota, 401 auth, empty response)
- Skip-cycle or alert-operator behavior on specific API errors
- Integration with an existing service layer for data persistence

This pattern recurs across multiple schedulers in spec-driven projects
(e.g., the Deerngo Bot SAD defines three: YouTube poller 15 min, EasyDonate
sync 5 min, name matcher 2 min). Build the first one right and the rest follow
the same shape.

## Architecture

```
cmd/server/main.go          → wires scheduler with config + DB + service
internal/youtube/client.go   → external API client (OAuth + endpoint)
internal/scheduler/poller.go → ticker goroutine, error classification
internal/repository/token.go → OAuth token CRUD on oauth_tokens table
internal/service/*.go         → existing business logic (reused, not duplicated)
```

### Key design rules

1. **The scheduler does NOT contain business logic.** It calls the existing
   service layer (`SubscriberService.Register()`) — same code path as the HTTP
   handler. No parallel validation, no separate upsert SQL.

2. **The API client is a separate package** (`internal/youtube/` or
   `internal/easydonate/`). It handles: OAuth token exchange, HTTP request
   construction, response parsing, and error classification. It knows nothing
   about the database or service layer.

3. **The scheduler orchestrates**: load token → call client → classify errors
   → call service for each result. The `PollOnce(ctx)` method is the
   unit-testable entry point. `Start(ctx)` wraps it in a ticker goroutine.

4. **OAuth tokens live in the database** (`oauth_tokens` table), not in
   environment variables. The scheduler loads the refresh token at startup from
   a `TokenRepository`. A separate CLI (`cmd/oauth-init`) performs the one-time
   consent flow and seeds the token.

## TDD approach — vertical tracer bullets

Do NOT write all tests first, then all implementation. Build one behavior slice
at a time:

### Slice 1: API client happy path (mock HTTP server)

```go
// RED: Write test against httptest.Server that returns 200 + subscriber JSON
func TestFetchSubscribersReturnsSubscribersOnSuccess(t *testing.T) { ... }

// GREEN: Implement FetchSubscribers with:
//   exchangeRefreshToken(ctx) → access token
//   GET /subscriptions with Bearer header
//   parse JSON response → []Subscriber
```

### Slice 2: Empty response

```go
func TestFetchSubscribersReturnsEmptyOnEmptyResponse(t *testing.T) { ... }
```

### Slice 3: Error classification (403/401)

```go
func TestFetchSubscribersReturnsQuotaExceededOn403(t *testing.T) { ... }
func TestFetchSubscribersReturnsUnauthorizedOn401(t *testing.T) { ... }
```

### Slice 4: Scheduler poll cycle (mock fetcher + mock registrar)

```go
func TestPollOnceCreatesSubscribersFromAPI(t *testing.T) { ... }
func TestPollOnceHandlesEmptyResponse(t *testing.T) { ... }
func TestPollOnceQuotaExceededSetsSkipFlag(t *testing.T) { ... }
func TestPollOnceUnauthorizedAlertsOperator(t *testing.T) { ... }
```

### Slice 5: Token repository (PostgreSQL integration)

```go
func TestPostgresTokenRepositoryUpsertAndLoad(t *testing.T) { ... }
```

## Error classification pattern

Export typed error checkers so the scheduler can branch without knowing
HTTP details:

```go
// In the API client package:
func IsQuotaExceeded(err error) bool {
    var ae *apiError
    return errors.As(err, &ae) && ae.Code == 403 && ae.Reason == "quotaExceeded"
}

func IsUnauthorized(err error) bool {
    var ae *apiError
    return errors.As(err, &ae) && ae.Code == 401
}

// Exported constructor for test use (avoids needing HTTP in unit tests):
func NewAPIError(statusCode int, reason, message string) error {
    return &apiError{Code: statusCode, Reason: reason, Message: message}
}
```

The scheduler branches on these:

```go
if youtube.IsQuotaExceeded(err) {
    p.logger.Error("quota exceeded, skipping next cycle", "error", err)
    p.skipNext = true
    return nil  // handled, not an error
}
if youtube.IsUnauthorized(err) {
    p.logger.Error("unauthorized — operator must re-authenticate",
        "error", err, "action", "manual_reauth_required")
    return nil  // handled
}
return err  // unexpected — propagate
```

## Skip-cycle pattern

For quota errors, use a `skipNext bool` field on the poller. `PollOnce` checks
it at the top:

```go
if p.skipNext {
    p.logger.Info("skipping poll cycle due to previous quota error")
    p.skipNext = false
    return nil
}
```

This is testable without waiting for a real timer — call `PollOnce` three times
and verify the second call is skipped.

## Configurable interval

The poll interval must be configurable for tests via env var, with a production
default:

```go
// config.go
pollMinutes, err := strconv.Atoi(getEnv("YOUTUBE_POLL_INTERVAL_MINUTES", "15"))
if err != nil || pollMinutes <= 0 {
    pollMinutes = 15
}
cfg.YouTubePollInterval = time.Duration(pollMinutes) * time.Minute
```

Never hardcode `15 * time.Minute` in the scheduler — the constructor should
apply the default if the config value is zero.

## OAuth one-time consent CLI

Build a separate `cmd/oauth-init` binary that reads the Google credentials
JSON (gitignored, not in code) and stores a refresh token in `oauth_tokens`
via `TokenRepository.UpsertToken`. Two flows exist — pick based on WHERE the
authorizing user sits:

**Flow A — operator is local (owns the account):** start a local HTTP
listener (e.g., `127.0.0.1:18090/callback`), print the consent URL, receive
the code via redirect, exchange.

**Flow B — authorizer is a REMOTE person (channel owner ≠ developer):** the
localhost callback FAILS for them — Google redirects to
`http://localhost:18090/callback?code=...` on THEIR machine, no server is
listening, the page won't load. That's expected: they copy the FULL URL from
the browser address bar and send it back; you paste it into the CLI, which
extracts `?code=...`, exchanges it, and stores the token. No public callback
endpoint needed. (This was the deciding factor in the Deerngo project: the
YouTube channel owner and the developer are different people.)

The main server binary loads the token at startup — if missing, it logs a
warning with a hint to run the CLI, but the HTTP API still works.

### Google Cloud Console setup

If the OAuth client is a **Desktop/installed app** (`"installed"` type in the
credentials JSON), **no redirect URI registration is needed.** Google accepts
loopback redirects (`http://localhost:<port>` / `http://127.0.0.1:<port>`)
with ANY port for installed apps. Only Web-app clients require the redirect
URI to be registered. Use `prompt=consent` and `access_type=offline` to
guarantee a refresh token is returned. If the owner previously granted
access, they must revoke the app at https://myaccount.google.com/permissions
first, or Google may not issue a refresh_token.

**Check the OAuth consent screen app status:** if the app is in "Testing"
mode, Google issues refresh tokens that **expire after 7 days** — the poller
breaks weekly. Publish the app ("In production") before running the consent
flow (personal projects with a single test user need no verification).

## Mock HTTP server pattern for API client tests

Use `httptest.NewServer` to simulate the external API and token endpoint
without network calls:

```go
func mockTokenServer() *httptest.Server {
    return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"access_token": "test-token"})
    }))
}

func mockYouTubeAPI(t *testing.T, statusCode int, body string) *httptest.Server {
    return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Assert Authorization header and query params
        w.WriteHeader(statusCode)
        w.Write([]byte(body))
    }))
}
```

Inject the test server URLs via `ClientConfig.TokenURL` and `ClientConfig.APIBaseURL`.

## Scheduler stub pattern for poller tests

The scheduler test uses two mocks — no HTTP, no database:

```go
type mockFetcher struct {
    subscribers []youtube.Subscriber
    err         error
    callCount   int
}
func (m *mockFetcher) FetchSubscribers(_ context.Context) ([]youtube.Subscriber, error) {
    m.callCount++
    return m.subscribers, m.err
}

type mockRegistrar struct {
    registered []service.RegisterSubscriberInput
    // ... results slice for per-call return values
}
```

Inject `youtube.NewAPIError(403, "quotaExceeded", "...")` as the fetcher error
to test skip-cycle behavior without a live HTTP server.

## Wiring into main.go

The scheduler starts as a background goroutine with context cancellation:

```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

// Start poller only if credentials are configured.
startYouTubePoller(ctx, cfg, db, subscriberService, logger)

// HTTP server runs in main goroutine.
go func() { app.Listen(":" + cfg.Port) }()

// Graceful shutdown.
quit := make(chan os.Signal, 1)
signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
<-quit
cancel()
```

`startYouTubePoller` checks for missing credentials and logs a warning —
the HTTP API should still work even if the poller is disabled.

## Verification

```bash
make fmt
make test
make vet
make build
go test -race -count=1 ./...
go build -trimpath -o bin/oauth-init ./cmd/oauth-init
```

Integration tests for the token repository run via `make test-integration`
against an isolated PostgreSQL database. On a Windows host with PostgreSQL in
Docker, cross-compile the test binaries and run them inside the container —
see `references/windows-docker-postgres-integration-testing.md` for the full
recipe (cross-compile → `docker cp` → Unix-socket DSN) plus cross-package
isolation rules (unique UUID handles, `-p=1`) and the CI PostgreSQL-service
workflow.

## Live end-to-end verification (before shipping a poller)

Mock tests prove the code paths; a live run proves the integration. When real
credentials exist, run the actual poller against the real API + local DB:

1. Start the server with the real `.env` (background process, watch for the
   poll log): the poller fires an **immediate poll on startup**.
2. Confirm the log line: `youtube poll completed fetched=N created=N upserted=0`.
3. Query the DB to confirm rows exist with the expected `source` and real data.
4. **Restart the server** — the startup poll now exercises the UPSERT path:
   expect `fetched=N created=0 upserted=N` and the DB row count unchanged
   (proves AC "no duplicates" live, without waiting for the real interval).

This pattern catches contract bugs that mocks cannot: wrong query parameters,
response field mismatches, and auth flow breaks. In the Deerngo session it
caught that the spec's endpoint URL was wrong (see Pitfalls).

## Verifying secrets exist WITHOUT printing them

When the user says "the token is in the DB, check it", never print the secret.
Prove presence + liveness with masked checks:

```bash
# 1. Row exists, correct shape, value masked:
docker exec local-postgres psql -U postgres -d deerngo -Atc \
  "SELECT provider, youtube_channel_id, created_at, LENGTH(refresh_token), LEFT(refresh_token,3) FROM oauth_tokens"

# 2. Cross-check the channel ID matches .env (length/prefix only):
CH=$(grep '^YOUTUBE_CHANNEL_ID=' .env | cut -d= -f2); echo "${#CH} ${CH:0:4}"

# 3. LIVE token-exchange probe — values stay in shell vars, only statuses print:
REFRESH_TOKEN=$(docker exec ... psql -Atc "SELECT refresh_token FROM oauth_tokens LIMIT 1;")
ACCESS_TOKEN=$(curl -sS -X POST "$TOKEN_URI" \
  -d "client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET&refresh_token=$REFRESH_TOKEN&grant_type=refresh_token" \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['access_token'])")
curl -sS -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=$CHANNEL_ID"
```

Print only lengths, prefixes, and HTTP statuses. On git-bash/MSYS, use `curl`
for TLS calls — MSYS `python3` urllib frequently fails with
`SSL: CERTIFICATE_VERIFY_FAILED` (no CA bundle); curl ships with proper certs.

## Detecting "API returns a subset" limitations

When the user suspects the poller missed subscribers, compare two live calls:

```bash
# Public truth: channels.list statistics
GET /channels?part=statistics&id=<channel>  → subscriberCount=1310
# What the poller can see: subscriptions pageInfo
GET /subscriptions?part=snippet&mySubscribers=true&maxResults=1 → totalResults=172
```

If `totalResults` << `subscriberCount`, the endpoint only exposes recent
subscribers (ongoing capture works, historical backfill is impossible). This
is a platform limitation, not a code bug — report it via meeting minute, don't
try to "fix" the client.

## Pitfalls

- **API spec example URLs may be factually wrong — verify live.** The Deerngo
  API spec said `GET /subscriptions?channelId=X&order=date`. Live testing
  proved: `channelId=` returns the channels the owner FOLLOWS (not its
  subscribers), and `order=date` is not a valid enum for subscriptions.list
  (400 INVALID_ARGUMENT). The correct call is `mySubscribers=true`. When real
  credentials exist, empirically probe the endpoint (curl with a fresh access
  token) BEFORE trusting spec query params. See
  `references/youtube-subscriptions-api.md`.
- **List endpoints may return IDs only — budget a second enrichment call.**
  `subscriptions?mySubscribers=true` returns only subscriber channel IDs +
  timestamps (`subscriberSnippet` is empty). Display name + @handle require a
  second batched call (`GET /channels?part=snippet&id=<comma-separated>`, 50
  per call, 1 quota unit each). Account for the extra call in quota math, and
  fall back to the ID as the handle when a channel has no customUrl.
- **Parallel business logic in the scheduler** — the scheduler must call the
  same service method as the HTTP handler. Do not duplicate validation,
  normalization, or upsert SQL in the scheduler.
- **Hardcoded poll interval** — always make it configurable; tests need fast
  intervals and the production default (15 min) is too slow for CI.
- **Unexported error types** — if `apiError` is unexported, tests in other
  packages cannot construct it. Export `NewAPIError()` as a test helper.
- **Missing skip-cycle reset** — after skipping one cycle, `skipNext` must be
  reset to `false` so the third cycle runs normally.
- **Token in env vars** — the spec says `oauth_tokens` table. Use the database.
  The env var is only for the CLI's `DATABASE_URL`.
- **OAuth credentials in Git** — the credentials JSON must be in `.gitignore`.
  Never read it into source files or commit it.
- **No graceful shutdown** — the ticker goroutine must respect `ctx.Done()`
  or it leaks on process exit.
- **Testing with real timers** — `PollOnce(ctx)` is the testable entry point.
  Do not test `Start(ctx)` with real `time.Ticker` waits.
- **Subscriber lists are subsets** — `mySubscribers=true` returns only the
  most recent ~N subscribers (Deerngo: 172 of 1,310 public), not the full
  list. Ongoing capture works; historical backfill is impossible. Detect via
  `channels.list statistics.subscriberCount` vs `pageInfo.totalResults`.
- **Platform limitation affecting acceptance criteria → meeting minute, not
  chat.** When a live finding invalidates what an AC implies (e.g., "capture
  all subscribers" is impossible), notify PO/QA via a meeting minute in the
  project's `07_pm/` directory following the local MM format (finding →
  evidence → impact on affected ACs → options → action items), and keep Dev
  work unblocked with a fix branch. User explicitly requested this
  ("create meeting minute to notice the PO/QA instant").
- **gofmt on Windows marks every file modified** — `make fmt` (gofmt -w)
  rewrites files with LF; git status shows all .go files as `M` while
  `git diff` is EMPTY (CRLF/LF artifact). Verify the diff is empty, then
  `git restore .` — never commit the line-ending noise.
- **`git restore` can silently delete uncommitted work** — cleaning the
  gofmt noise with a broad `git restore cmd internal` also reverted an
  UNCOMMITTED new test file in the working tree (it was only flagged as
  `M` by the same CRLF artifact, so it looked like noise). Rules: (1)
  commit all intended changes BEFORE restoring line-ending noise; (2) if
  you must restore before committing, restore only the specific noise
  files, and `grep -c` your new symbol afterward to confirm it survived.
