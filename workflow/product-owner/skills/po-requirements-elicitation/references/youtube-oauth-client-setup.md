# YouTube Data API OAuth — Client Setup Reference

Use this reference when a project needs an always-on backend to read private YouTube channel data, especially subscriber activity.

## Core distinction

A Google Cloud project and an enabled YouTube Data API are not authorization to read channel data. A normal API key identifies a project but is not sufficient for an authenticated channel-owner feed. Use OAuth 2.0 with the channel owner/manager's consent.

For a server-side Deerngo-style integration:

- Google Cloud project
- YouTube Data API v3 enabled
- OAuth consent/branding configured
- OAuth client ID and client secret
- Channel-owner consent using the Google account that owns/manages the channel
- Refresh token stored securely for long-lived backend operation
- Stable `YOUTUBE_CHANNEL_ID` (normally begins with `UC`)

Use the least-privilege read-only scope where sufficient:

```text
https://www.googleapis.com/auth/youtube.readonly
```

YouTube Data API does not support using a service account as a substitute for channel-owner OAuth authorization.

## Client-friendly handoff pattern

The client should not be asked to write code or paste secrets into chat. Dev owns the bootstrap flow:

1. Dev creates the OAuth client and provides a local authorization URL/command.
2. Client signs in with the channel-owner Google account and approves the exact requested scope.
3. Dev exchanges the authorization code and stores the refresh token in an approved secret store/token table.
4. Client provides the non-secret channel ID through the agreed channel.
5. Dev verifies token refresh and the authorized channel before implementing the scheduler.

Never put the client secret, refresh token, downloaded client-secret JSON, database password, or webhook secret in Git, issue bodies, ordinary chat, screenshots, or an unprotected note vault.

## YouTube subscriber feed caveats

For recent subscribers, the YouTube `subscriptions.list` method uses an authorized request such as `myRecentSubscribers=true`. Check the official reference at execution time because API behavior and quotas can change.

Document these constraints explicitly:

- Method quota cost is currently documented as 1 unit per call.
- `maxResults` is limited; the recent-subscriber result may itself be limited.
- Some subscription activity may not be visible due to viewer privacy or YouTube API rules.
- Therefore, do not promise absolute capture until a controlled test validates the channel's behavior.
- A hybrid design can combine always-on polling with a live-time integration, but it does not override provider visibility limits.

## OAuth lifecycle warning

A refresh token can be revoked, invalidated, or become unusable after client deletion or account changes. A Google OAuth app configured as External and left in Testing may issue refresh tokens that expire after a short testing period (Google currently documents a 7-day behavior for non-basic scopes in this situation). For an always-on service, Dev/PO must review the current publishing/production requirements before go-live.

The implementation must:

- refresh access tokens at runtime;
- handle `401` by alerting for reauthorization without logging secrets;
- avoid tight retry loops on `403 quotaExceeded`;
- make the polling interval configurable for tests;
- keep the production interval and quota assumptions documented.

## Credential readiness checklist

- [ ] API project selected and recorded
- [ ] YouTube Data API v3 enabled
- [ ] Consent screen configured with support/developer contact
- [ ] Correct channel owner added as a test user when required
- [ ] OAuth client type and redirect URI match the Dev bootstrap flow
- [ ] Consent completed for the intended channel account
- [ ] Refresh token stored securely and tested
- [ ] `YOUTUBE_CHANNEL_ID` verified independently of `@handle`
- [ ] `.env.example` lists required variable names without values
- [ ] Logs and errors redact tokens and secrets
- [ ] Scheduler tests cover success, empty response, `401`, and quota errors

## Official references

- https://developers.google.com/youtube/v3/docs/subscriptions/list
- https://developers.google.com/youtube/v3/guides/authentication
- https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps
- https://support.google.com/cloud/answer/6158849
- https://support.google.com/cloud/answer/10311615

Always re-check these sources before giving current Google-console instructions.
