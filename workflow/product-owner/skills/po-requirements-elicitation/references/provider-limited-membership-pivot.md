# Provider-Limited Audience Data → Explicit Member Program

Use this reference when a provider API returns only a partial, capped, privacy-filtered, or otherwise incomplete audience list, while the product needs reliable identity, points, or relationship management.

## Trigger

Typical signals:

- The provider's public count is larger than the API result.
- The API only exposes recent/current/visible users.
- Historical backfill is impossible or not guaranteed.
- Provider display names or handles may identify real people.
- The product needs explicit participation rather than passive observation.

## Evidence-First Review

1. Test the provider request against the real authorized account, not only mocks.
2. Verify the request parameters against current official documentation.
3. Record returned count, public/known count, pagination behavior, visibility restrictions, and enrichment calls.
4. Capture a sanitized evidence sample; never store or paste tokens, private payloads, or unnecessary personal data.
5. Rewrite acceptance criteria to match what the provider can actually guarantee.

### Deerngo example

The live YouTube verification found that:

- `subscriptions.list` with `mySubscribers=true` returned 172 records while the channel statistics showed 1,310 subscribers.
- `channelId` in the tested request returned channels followed by the owner, not the owner's subscribers.
- `order=date` was invalid for that request.
- Subscriber channel IDs and timestamps came from `subscriptions.list`; display titles and handles required batched `channels.list` enrichment.
- The corrected poller and tests were merged after live verification.

Do not claim "all subscribers" when the API only provides a partial/recent/visible subset. Use language such as "available subscribers returned by the provider" or "new subscribers going forward," and document private/limited visibility.

## Domain Separation

Do not make an incomplete provider observation table the product's membership source. Separate:

```text
source observations = provider data, incomplete and provider-controlled
members            = people who explicitly join the product
transactions       = donations/payment events
benefits/points    = calculations for eligible members
```

A YouTube observation should not automatically create a member, award points, or appear on the public scoreboard.

## Explicit Registration Pattern

For a live-chat member program:

1. Receive the actual chat author's stable provider identity from the trusted event integration (for streamer.bot, verify the real `userId`/channel ID field).
2. Ignore any handle typed by the viewer; otherwise a viewer could claim another person's identity.
3. On `:deer: register`, create a member with zero points and `registered_at=now`.
4. Make repeated registration idempotent for the same active handle.
5. Define what happens when identity/handle changes before implementation; do not silently merge points.
6. If registration depends on a desktop component, document that the command cannot be detected while that component is offline.

## Donation Cutover and Matching

For a clean MVP cutover:

- Donations before `member.registered_at` are stored for reconciliation but do not earn points.
- A donation earns points only when `donation_time >= member.registered_at`.
- Normalize both the donor name and handle by trimming whitespace, stripping one leading `@`, and lowercasing.
- Use normalized exact matching for automatic points when false positives are costly; fuzzy matching is not a substitute for identity proof.
- Do not automatically backfill historical donations unless the stakeholder approves a controlled process.
- Keep unmatched donor events private and define a retention period.

## Simple Handle-Change MVP

A separate alias table is technically possible, but it adds identity and collision policy. If the stakeholder wants a simpler first release:

- Use `member_id` as the row primary key.
- Keep only the current normalized handle unique among active members.
- On a changed-handle re-registration, mark the old member inactive and create a new active member with zero points.
- Keep the old row and its points private for manual correction/transfer by the owner or back-office worker.
- Hide inactive members from point queries, automatic matching, and the public scoreboard.
- Do not automatically transfer or merge points.
- If a new active registration reuses an old inactive handle, allow it but keep the records and points separate.
- Record the manual correction procedure even before building an admin console; use a transaction and a backup/audit note.

## Public Visibility and Thai PDPA Caution

Treat YouTube handles, display names, channel IDs, donor names, donation events, and member points as potentially personal data when they can identify or be linked to a natural person. Normalizing a handle does not anonymize it.

Before public display, document:

- purpose and legal basis;
- what is collected from YouTube/streamer.bot and EasyDonate;
- whether membership and public display are separate choices;
- the public fields (never expose raw donor names or provider display names by default);
- retention and deletion rules;
- correction, opt-out, hide, and removal paths;
- channel-owner controller vs developer/host processor responsibilities;
- cloud/subprocessor and cross-border handling where relevant.

For a conservative product, make public visibility a separate explicit opt-in. If the stakeholder chooses public-by-default, show a clear notice at registration and provide an easy `public/private` or removal mechanism. A public bot reply is itself public; exact points may need to be rounded/banded for private members.

This is product/privacy guidance, not legal advice; refer the channel owner to Thai PDPC or counsel for a final determination.

## Vendor Contract Verification

For every third-party integration, distinguish:

1. backend outbound API credential (API key/OAuth token);
2. OAuth client identity (client ID/secret);
3. provider-to-backend webhook URL;
4. webhook authenticity mechanism (signature/secret/header), only if the provider explicitly supports it.

For EasyDonate specifically:

- Current developer documentation describes a personal API key used as a Bearer token and donation-read scopes for API calls.
- A webhook URL is a separate configuration from the API key.
- Current public documentation shows donation webhook fields such as `referenceNo`, `channelName`, `donatorName`, `donateMessage`, `amount`, and `time`.
- Do not assume `EASYDONATE_WEBHOOK_SECRET`, `X-EasyDonate-Signature`, HMAC, or the draft field names `id`, `donor_name`, and `created_at` until the dashboard/provider contract confirms them.
- If no signing mechanism exists, use an unpredictable endpoint path, strict payload validation, idempotency on `referenceNo`, rate/body limits, and API polling reconciliation; mark the weaker authenticity as a security risk.

## Ripple-Update Checklist

After approving the pivot, update all affected artifacts together:

- existing meeting minute decision/status/action items;
- business objectives and KPI definitions;
- user stories and acceptance criteria/counts;
- API endpoint contracts and provider payload mapping;
- DDL/ERD and migration plan;
- QA test cases, regression suite, and coverage report;
- security report and risk register;
- architecture/overview and implementation plan;
- GitHub issue titles/bodies, milestones, and stale issues.

Do not create a parallel specification just because a meeting minute raised a change. Finish the grill, update the existing decision record, then make the minimum coherent cross-document revision.
