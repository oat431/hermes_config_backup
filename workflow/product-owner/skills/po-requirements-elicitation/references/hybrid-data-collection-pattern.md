# Hybrid Data Collection Pattern

## When to Use

When a feature depends on capturing events from a source that **isn't always available**:
- Desktop apps (streamer.bot, OBS plugins) — only running during sessions
- Browser extensions — only active when browser is open
- Mobile apps — only active when app is in foreground
- User-initiated processes — only running when user starts them

## The Pattern

```
Primary Source (always-on)     Secondary Source (when available)
─────────────────────────      ──────────────────────────────────
API polling (every N min)  +   Real-time push (webhooks/events)
Webhook from platform      +   Desktop app capture
Scheduled sync             +   User-triggered capture
```

**Both sources write to the same database with upsert logic (deduplicate by unique key).**

## Design Checklist

When proposing a hybrid approach, document ALL of these in the spec:

| Aspect | Question | Example |
|--------|----------|---------|
| **Primary source** | What's the always-on source? | YouTube Data API polling |
| **Secondary source** | What's the real-time source? | streamer.bot subscription event |
| **Polling interval** | How often does the primary poll? | Every 15 minutes |
| **Freshness SLA** | Max time before data appears? | 15 min (polling) or 5s (live) |
| **API quota** | Does polling fit within rate limits? | 96 calls/day vs 10,000 unit quota |
| **Deduplication** | What's the unique key? How is conflict resolved? | `youtube_handle`, preserve earliest timestamp |
| **Source tracking** | Which source captured the record? | `source` field: "youtube_api" or "streamer_bot" |
| **Fallback behavior** | What if primary source is down? | Log error, retry next cycle |
| **Conflict resolution** | What if both sources fire for same event? | Upsert — preserve earliest timestamp, do NOT overwrite |

## Real Example: Deerngo Bot Subscriber Capture

**Problem:** streamer.bot only runs during live streams. Subscribers who join at 3am are never captured.

**Solution:**
- **Primary:** Go backend polls `GET /youtube/v3/subscriptions` every 15 minutes (24/7)
- **Secondary:** streamer.bot fires `YouTube > General > New Subscriber` during live streams, POSTs to Go API
- **Database:** PostgreSQL with `youtube_handle` as unique key, `source` field to track origin
- **Upsert:** Both sources insert/update on `youtube_handle`. Earliest `subscribed_at` timestamp is preserved.
- **Quota:** 96 API calls/day (every 15 min) vs 10,000 unit/day quota = well within limits

```
YouTube Data API ──────poll every 15min──────┐
                                              ├──▶ PostgreSQL (upsert by handle)
streamer.bot ──────real-time during live─────┘
```

## AC Template for Hybrid Capture

```markdown
| AC-xxx | Real-time capture | [source B is running] | [event fires] | [record created with source="B", response time <Xs] | 🔴 |
| AC-xxx | Offline capture | [source B is offline] | [polling scheduler runs] | [record created/updated with source="A"] | 🔴 |
| AC-xxx | Upsert dedup | [record exists from source A] | [source B captures same event] | [record updated, no duplicate, earliest timestamp preserved] | 🔴 |
| AC-xxx | Both sources fire | [source B captures event, then polling also finds it] | [upsert runs from second source] | [record NOT overwritten, earliest timestamp preserved] | 🔴 |
| AC-xxx | Primary source error | [primary returns 403/401/timeout] | [scheduler detects error] | [error logged, next cycle skipped/alerted] | 🔴 |
| AC-xxx | Polling interval | [scheduler is running] | [interval has passed] | [new poll cycle starts automatically] | 🔴 |
| AC-xxx | No new data | [primary returns 0 records] | [scheduler processes response] | [no records created, completes without error] | 🟡 |
```

## Common Primary Sources

| Source | Always-On? | Freshness | Cost |
|--------|-----------|-----------|------|
| REST API polling | ✅ | Interval-dependent | Quota units per call |
| Webhook (push) | ✅ | Near real-time | None (push model) |
| Database replication | ✅ | Near real-time | None |
| Log file tailing | ✅ | Near real-time | None |
| PubSubHubbub/WebSub | ✅ | Real-time | None (but limited platform support) |

## Common Secondary Sources

| Source | Availability | Freshness | Notes |
|--------|-------------|-----------|-------|
| Desktop app callback | When app is running | Real-time | e.g., streamer.bot HTTP Request sub-action |
| Browser extension | When browser is open | Real-time | e.g., content script → backend |
| Mobile app push | When app is active | Real-time | e.g., Firebase → backend |
| WebSocket connection | When client is connected | Real-time | e.g., live dashboard updates |
| Plugin/add-on hook | When host app is running | Real-time | e.g., OBS plugin, VS Code extension |
