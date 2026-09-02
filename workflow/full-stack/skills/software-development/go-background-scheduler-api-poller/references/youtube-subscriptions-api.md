# YouTube Data API — Subscriber Polling (verified live)

Empirically verified against the real YouTube Data API v3 (Deerngo session,
2026-08). **The commonly-documented URL is wrong; these are the working facts.**

## The endpoint that actually works

```
GET https://www.googleapis.com/youtube/v3/subscriptions
  ?part=snippet
  &mySubscribers=true        ← NOT channelId=
  &maxResults=50             ← max 50; paginate with nextPageToken
  &pageToken=...             ← for pages 2+

Authorization: Bearer {access_token}
```

### Why `channelId=` is wrong (verified live)

| Parameter | Live result | Verdict |
|---|---|---|
| `channelId=X` | Returns channels that X FOLLOWS (e.g., SEPHER SCHWARZ, SPYRUN, dayta for DeerNGO) | ❌ Not subscribers |
| `order=date` | `400 INVALID_ARGUMENT` — valid enum for subscriptions.list is `alphabetical`, `relevance`, `unread` | ❌ Invalid value |
| `mySubscribers=true` | Returns the actual subscribers (172 for DeerNGO) with `snippet.channelId` + `snippet.publishedAt` | ✅ Correct |

### Response shape

```json
{
  "nextPageToken": "CAEQAA",
  "pageInfo": { "totalResults": 172 },
  "items": [{
    "snippet": {
      "publishedAt": "2026-07-31T07:52:03.545051Z",
      "channelId": "UCYPiaNffQqhMnmlnrONvgww",
      "resourceId": { "channelId": "UCAXtrxOTFigvqviKyoSB6Fg" }
    }
  }]
}
```

Key field mapping:
- `snippet.channelId` → **subscriber's** channel ID (the one you want)
- `snippet.publishedAt` → subscription/signup timestamp (parse RFC3339)
- `snippet.resourceId.channelId` → **the owner's own** channel ID (not useful)
- `snippet.subscriberSnippet` → **empty `{}`** — do not rely on it

## Enrichment call (channels.list)

The subscriptions response has NO display name or @handle. Get them from
channels.list, batched 50 IDs per call (1 quota unit each):

```
GET https://www.googleapis.com/youtube/v3/channels?part=snippet&id=UC1,UC2,...
```

```json
{ "items": [{ "id": "UCsub1", "snippet": {
    "title": "Viewer One",
    "customUrl": "@viewer1"
}}]}
```

- `snippet.title` → display_name
- `snippet.customUrl` → @handle (strip the `@`); **fall back to channel ID**
  as the handle when customUrl is empty (some channels have none).

## Platform limitation — the API exposes only a SUBSET of subscribers

`mySubscribers=true` does NOT return the channel's full subscriber list. Live
verification (Deerngo, 2026-08): public `subscriberCount=1310` but
`mySubscribers` `totalResults=172`. The exposed set is the MOST RECENT
signups — ongoing capture works (new subscribers appear in the window), but
**historical backfill is impossible** via the Data API v3.

### Detect the gap (live check)

```bash
# Public truth:
GET /youtube/v3/channels?part=statistics&id={channel_id}
#   → statistics.subscriberCount (1310), statistics.hiddenSubscriberCount

# Exposed subset:
GET /youtube/v3/subscriptions?part=snippet&mySubscribers=true&maxResults=1
#   → pageInfo.totalResults (172)
```

If `totalResults << subscriberCount`, set expectations: the DB will grow by
new-signup capture only. This is an external platform constraint, not a code
bug — flag it to PO/QA rather than "fixing" it. The Deerngo MM06 meeting
minute documents the finding, its impact on AC-001b/AC-003, and PO options.

## Quota math

- subscriptions.list: 1 unit/call (paginated — 172 subscribers = 4 pages = 4 units)
- channels.list: 1 unit/call (batched 50 ids)
- ~5 units/poll × 96 polls/day ≈ 480 units/day — well under the 10,000/day default.

## OAuth for installed/desktop clients (the credentials file)

`deerngo-oauth-api.json` type `"installed"` means **Desktop app** OAuth client:

- **No redirect URI registration needed** in Google Cloud Console — loopback
  (`http://localhost:<port>`) with any port is accepted for installed apps.
- The auth URL must still pass `redirect_uri=http://localhost:18090/callback`
  (must match exactly between the consent URL and the code-exchange POST).
- Consent flow with a remote authorizer: they authorize, their browser
  redirects to localhost on THEIR machine (page fails to load — expected),
  they copy the FULL URL from the address bar, you paste it into the CLI.
- **App status matters:** "Testing" mode → refresh tokens expire after 7 days.
  Publish the app ("In production") before consent, or add the owner as a
  test user for temporary dev.

## Live verification recipe (proves the whole chain)

```bash
# 1. Exchange the stored refresh token for an access token (curl, not Python
#    urllib — MSYS2 Python lacks CA certs):
REFRESH_TOKEN=$(docker exec local-postgres psql -U postgres -d deerngo -Atc \
  "SELECT refresh_token FROM oauth_tokens WHERE provider='youtube' LIMIT 1;")
ACCESS_TOKEN=$(curl -sS -X POST https://oauth2.googleapis.com/token \
  -d "client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET&refresh_token=$REFRESH_TOKEN&grant_type=refresh_token" \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['access_token'])")

# 2. Probe the endpoint:
curl -sS -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&mySubscribers=true&maxResults=3"

# 3. Then run the actual server (immediate poll on startup) and watch logs:
#    "youtube poll completed fetched=172 created=172 upserted=0"
#    Restart → "fetched=172 created=0 upserted=172" proves no-duplicate upsert.
```

## Credentials handling rules

- `deerngo-oauth-api.json` and `.env` are gitignored; never print token values
  — verify presence with `LENGTH(refresh_token)` and `LEFT(refresh_token,3)`
  (Google refresh tokens start with `1//`).
- The DB token check: one row per (provider, youtube_channel_id); the token
  repo upserts on the unique constraint.
