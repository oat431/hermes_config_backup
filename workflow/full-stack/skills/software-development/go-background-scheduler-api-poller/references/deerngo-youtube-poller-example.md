# Deerngo Bot YouTube Poller — Worked Example

Concrete implementation reference from Sprint 1 Issue #3 (US-003).
This is a real working implementation, not pseudocode.

## Project context

- **Module**: `oat431/deerngo-bot`
- **Stack**: Go 1.25, Fiber v3, sqlx, pgx, PostgreSQL 18
- **Spec**: API Specification §4.6 defines the polling scheduler
- **DB**: `oauth_tokens` table stores refresh tokens by (provider, channel_id)
- **Scope**: 7 acceptance criteria (AC-003a through AC-003g)

## File layout

```
cmd/oauth-init/main.go               One-time OAuth consent CLI
internal/config/config.go            Added YouTubeClientID, YouTubeClientSecret, YouTubePollInterval
internal/repository/token.go         OAuthToken struct, GetRefreshToken, UpsertToken
internal/repository/token_integration_test.go   PostgreSQL integration test
internal/youtube/client.go           Client struct, FetchSubscribers, exchangeRefreshToken, error types
internal/youtube/client_test.go      4 mock HTTP tests (success, empty, 403, 401)
internal/scheduler/poller.go         Poller struct, PollOnce, Start, skipNext flag
internal/scheduler/poller_test.go    5 mock tests (happy, empty, quota skip, 401 alert, upsert)
cmd/server/main.go                   Wires poller with graceful shutdown
```

## YouTube Data API endpoint (CORRECTED — verified live)

```
GET https://www.googleapis.com/youtube/v3/subscriptions
  ?part=snippet
  &mySubscribers=true        ← NOT channelId=
  &maxResults=50
  &pageToken=...             ← paginate (cap at 10 pages to protect quota)

Authorization: Bearer {access_token}
```

> ⚠️ **Spec correction:** the original API spec §4.6 documented
> `channelId={channel_id}&order=date`. Live testing proved both wrong:
> `channelId=` returns the channels the owner FOLLOWS (not subscribers), and
> `order=date` is invalid for subscriptions.list (400). Full details in
> `youtube-subscriptions-api.md`.

After the subscriptions call, a second **channels.list enrichment** call
(batched 50 IDs) fetches display name + @handle, because the subscriptions
response only returns subscriber channel IDs:

```
GET https://www.googleapis.com/youtube/v3/channels?part=snippet&id=UC1,UC2,...
```

- `snippet.title` → display_name
- `snippet.customUrl` → @handle (strip `@`); fall back to channel ID if empty

The access token is obtained by POSTing to
`https://oauth2.googleapis.com/token` with:
- client_id, client_secret, refresh_token, grant_type=refresh_token

## OAuth consent CLI (cmd/oauth-init)

The tool (manual copy-paste flow — the authorizer is the channel owner on a
different machine, so a local callback server never runs):
1. Reads `deerngo-oauth-api.json` (gitignored — contains client_id/secret)
2. Builds auth URL with `scope=youtube.readonly`, `access_type=offline`,
   `prompt=consent`
3. Prints the URL and prompts the operator to paste back the FULL redirect URL
   (the owner authorizes in their browser; Google redirects to
   `http://localhost:18090/callback?code=...` on THEIR machine; the page
   won't load — that's expected and fine)
4. Extracts the code: `parsed.Query().Get("code")` from the pasted URL
5. Exchanges the code for a refresh token
6. Calls `tokenRepo.UpsertToken(ctx, "youtube", channelID, refreshToken)`

### Google Cloud Console — Desktop app client

The credentials file is type `"installed"` (Desktop app), so **no redirect URI
registration is needed** — Google accepts loopback redirects
(`http://localhost:<port>`) with any port for installed apps. The
`redirect_uri` in the consent URL and the code-exchange POST must still match
exactly (`http://localhost:18090/callback`).

**Check the app status:** "Testing" mode → refresh tokens expire after 7 days.
Publish the app ("In production") before the consent flow, or the poller will
break weekly.

### Pitfall: no refresh_token in response

If the owner previously authorized without `prompt=consent`, Google may not
return a `refresh_token`. Ask them to revoke the app at
https://myaccount.google.com/permissions and re-run the flow.

## Config additions

```go
// internal/config/config.go
type Config struct {
    // ... existing fields ...
    YouTubeClientID         string
    YouTubeClientSecret     string
    YouTubePollInterval     time.Duration
}

// In Load():
YouTubeClientID:     os.Getenv("YOUTUBE_CLIENT_ID"),
YouTubeClientSecret: os.Getenv("YOUTUBE_CLIENT_SECRET"),

pollMinutes, err := strconv.Atoi(getEnv("YOUTUBE_POLL_INTERVAL_MINUTES", "15"))
if err != nil || pollMinutes <= 0 {
    pollMinutes = 15
}
cfg.YouTubePollInterval = time.Duration(pollMinutes) * time.Minute
```

## .env.example additions

```
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_POLL_INTERVAL_MINUTES=15
```

## main.go wiring pattern

```go
func main() {
    cfg := config.Load()
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
    slog.SetDefault(logger)

    db, err := database.Open(context.Background(), cfg.DatabaseURL)
    // ...

    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    startYouTubePoller(ctx, cfg, db, subscriberService, logger)

    go func() {
        if err := app.Listen(":" + cfg.Port); err != nil {
            log.Fatalf("server stopped: %v", err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    cancel()
}
```

`startYouTubePoller` gracefully degrades — if credentials or token are
missing, it logs a warning and returns. The HTTP API still works.

## Test count

- 5 YouTube client mock tests (httptest.Server — success + enrichment,
  handle fallback, empty, 403, 401)
- 5 scheduler mock tests (mockFetcher + mockRegistrar)
- 1 token repository PostgreSQL integration test
- 3 config tests (defaults, env, invalid interval)

Total: 14 new tests. All pass with `-race`.

## Live verification evidence (real API + local DB)

Running the actual server with the stored refresh token:

```
First poll:  "youtube poll completed" fetched=172 created=172 upserted=0
Restart:     "youtube poll completed" fetched=172 created=0  upserted=172
```

DB count stayed 172 after the second poll — no duplicates (AC-003c live).
Real rows: `ggwpไฟแคน` (GGWP ไฟแค้น), `jibpumkaew` (Jib Pumkaew), `baofai12`
(BAOFAI CHANNEL), all `source=youtube_api` with correct signup timestamps.

## Lessons from this implementation

1. **Live-verify spec URLs before building on them.** The spec's
   `channelId=&order=date` example was wrong on both counts; the correct
   `mySubscribers=true` + channels enrichment flow was only discovered by
   probing the real API with a fresh access token. Build the client
   interface so the endpoint details live in ONE place (the client) — when
   the spec is wrong, only the client changes, not the scheduler.

2. **Exported error helpers are essential** — `youtube.NewAPIError()` was
   added specifically so scheduler tests could construct typed errors without
   a live HTTP server. Without it, the skip-cycle test cannot be written
   cleanly.

3. **PollOnce is the testable surface** — do NOT try to test `Start(ctx)`
   with real timers. The `skipNext` flag pattern exists specifically so
   skip-cycle behavior can be tested by calling `PollOnce` three times in
   sequence.

4. **Graceful credential absence** — the server starts and serves HTTP even
   without YouTube credentials. The poller logs a warning. This lets you
   develop and test the HTTP layer independently of the external API.

5. **Token repository interface vs concrete type** — the scheduler's
   `TokenProvider` interface and the repository's `TokenRepository` interface
   overlap. The scheduler defines its own minimal interface to stay
   testable. Do not import the concrete repository into the scheduler
   package — that couples them unnecessarily.
