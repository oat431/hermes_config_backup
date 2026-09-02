# Provider-Limited Membership Pivot — Decision Matrix

Use this reference as a compact worksheet during a requirements grill when an external audience/subscriber API is incomplete.

## Evidence Gate

| Question | Evidence to capture | Decision consequence |
|----------|---------------------|----------------------|
| What count does the provider expose? | Live response/pageInfo + authoritative count if available | Replace absolute completeness claims |
| Is the list historical or recent/current? | Timestamp window, pagination/cap | Decide whether backfill is possible |
| Are private users hidden? | Provider docs/settings/test response | Treat provider list as incomplete observation |
| Is identity stable? | User ID/handle semantics | Select trusted identity key |
| Is display data needed? | Fields exposed and product need | Minimize storage/public fields |

## Grill Sequence

1. Trusted event identity: actual platform user ID/handle or user-entered value?
2. Runtime availability: what happens when the event source is offline?
3. Cutover: starting balance and actual transaction timestamp?
4. Matching: normalized exact, controlled mapping, or fuzzy? For points, default to exact.
5. Handle change: alias/history or inactive old + new zero-point record/manual correction?
6. Public identity: handle, nickname, or no public display?
7. Visibility: explicit opt-in, public-by-default notice, hide/private command, removal?
8. Retention: keep provider observations/transactions privately or remove from MVP?
9. Provider contract: exact payload, idempotency key, auth/signature, retry, rate limits?

## Safe MVP Defaults

```text
trusted event identity
new member starts at 0
transaction_time >= registered_at
trim + strip one leading @ + lowercase
exact matching only
no automatic historical credit
inactive old member + active new zero-point member on handle change
manual DB correction in transaction + backup + audit note
public response allowlist only
no raw display/donor fields publicly
```

## Cross-Document Ripple Map

```text
meeting minute / ADR
  -> business objectives and KPIs
  -> user stories and ACs
  -> API / DDL / ERD / SAD
  -> QA cases / regression / coverage
  -> security / risk / runbook / deployment
  -> overview / wireframes / FE types / release notes
  -> GitHub issues / milestones
```

## Verification Targets

```text
active story IDs = approved story count
active unique AC IDs = summary total
traceability AC IDs = active AC IDs
active test IDs = active AC IDs (unless a documented split exists)
duplicate test IDs = 0
```

Classify old references as `active`, `historical`, `superseded`, or `stale`; do not delete useful evidence blindly.

## GitHub Body/Batch Pattern

For complex issue bodies:

```bash
# write markdown to a temporary file
# then use:
gh issue edit <N> --body-file /path/to/body.md
gh issue create --body-file /path/to/body.md
```

After a batch:

```bash
gh issue view <N> --json number,title,state,body,labels,milestone,url
gh issue list --state all --json number,title,state,url
```

A successful command batch is not sufficient evidence: verify every issue remotely and fix partial failures before reporting completion.
