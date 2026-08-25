# Third-Party Integration Credential Verification

## Credential taxonomy

Separate these contracts before requesting client credentials:

1. **Backend → provider API credential:** API key or OAuth access/refresh token used for polling/outbound calls.
2. **OAuth client identity:** client ID/secret identifies the application; the client ID alone is not an authorization URL.
3. **Provider → backend webhook:** public callback URL configured in the provider dashboard.
4. **Webhook authenticity credential:** HMAC/signing secret or signature header only when confirmed by current provider docs/dashboard.

Never treat an assumed webhook secret, HMAC header, payload shape, or retry policy as confirmed. Verify the vendor contract first, then update API spec, ACs, security docs, implementation issues, and client setup notes.

## YouTube Data API / OAuth

- Subscriber-feed access requires OAuth authorization by the channel owner/manager; a normal API key is insufficient.
- YouTube Data API does not support service-account access for this linked-channel scenario.
- The owner must authorize through a complete authorization URL, not by opening the OAuth client ID. The URL must use the registered redirect URI, requested scope, random `state`, `access_type=offline`, and `prompt=consent` when a new refresh token is needed.
- With a Desktop OAuth client, `localhost` redirects to the machine where the owner opens the URL. If the helper runs on the developer's computer and the owner authorizes on a different computer, the callback will not reach the helper and can produce a 404/connection failure. Use a helper on the same machine, a controlled remote session, or a reachable HTTPS callback.
- Use the read-only YouTube scope: `https://www.googleapis.com/auth/youtube.readonly`.
- Store the refresh token and client secret securely; never put them in chat, issues, source code, or logs.
- `YOUTUBE_CHANNEL_ID` is a non-secret stable identifier and can be recorded in normal configuration. Confirm it from YouTube Studio.
- Google documents that `subscriptions.list` recent-subscriber results may be limited. Private subscriptions may not be visible. Describe the result as best-available 24/7 capture, not unconditional 100% coverage.
- An External OAuth app left in Testing can issue refresh tokens that expire after 7 days for non-basic scopes; always-on deployments need appropriate publishing/production configuration.

## EasyDonate

Current official developer documentation distinguishes:

- **Personal API key:** opaque key beginning with `ezdn_v1_`, used as `Authorization: Bearer <token>` for the owner's own API account. Donation-list endpoints require the appropriate donation-read scope (the current quickstart names `read:donations`). Keep the key server-side only.
- **OAuth access token:** short-lived JWT for apps acting on behalf of other EasyDonate users; usually unnecessary for this single creator account.
- **Webhook:** a provider-to-backend callback configured in EasyDonate. The webhook guide shows donation payloads with fields such as `referenceNo`, `channelName`, `donatorName`, `donateMessage`, `amount`, and `time`.

Do not assume EasyDonate supports the project's previously drafted `EASYDONATE_WEBHOOK_SECRET` or `X-EasyDonate-Signature` HMAC contract until the dashboard or current provider documentation confirms it. Also do not assume the drafted field names (`id`, `donor_name`, `created_at`) match the real webhook payload. Confirm the live payload/security behavior before implementing verification.

The required client inputs are therefore separate:

- API key with donation-read scope for fallback polling.
- EasyDonate account/page identifier (for example the `deerngo0` page).
- Public webhook URL later, after backend deployment.
- Webhook signing secret only if EasyDonate actually provides/configures one.

## OAuth/404 troubleshooting

1. Determine whether the error occurs before or after consent.
2. If before consent, verify the full authorization URL and client ID/project.
3. If after consent, inspect the redirect URI (without sharing authorization codes). A callback to an unserved localhost or unregistered URI commonly causes 404.
4. Confirm the owner's exact Google account is an allowed test user and the YouTube API is enabled in the same Cloud project.
5. Never ask the user to paste client secrets, refresh tokens, authorization codes, or API keys into chat.

## Official sources used for Deerngo

- YouTube `subscriptions.list`: https://developers.google.com/youtube/v3/docs/subscriptions/list
- YouTube authentication: https://developers.google.com/youtube/v3/guides/authentication
- YouTube OAuth server-side apps: https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps
- Google OAuth client management: https://support.google.com/cloud/answer/6158849
- Google OAuth consent/branding: https://support.google.com/cloud/answer/10311615
- EasyDonate developer platform: https://docs.easydonate.app/developer
- EasyDonate authentication: https://docs.easydonate.app/developer/authentication
- EasyDonate quickstart: https://docs.easydonate.app/developer/quickstart
- EasyDonate webhook guide: https://docs.easydonate.app/guide/donate/developer
