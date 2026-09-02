# Pre-Code Spec Gap Patterns — Worked Example (Deerngo Bot)

> Source: Deerngo Bot VRM project, QA review of spec docs (013 ACs, 022 API Spec, 023 DB Schema) before any code was written. 6 spec gaps found across 3 document pairs.

## Document pairs reviewed

| Pair | Documents | Gaps Found |
|------|-----------|:----------:|
| AC ↔ API Spec | `013_acceptance_criteria.md` × `022_API_specification.md` | 2 |
| AC/API ↔ DB Schema | `022_API_specification.md` × `023_database_schema_DDL.md` | 2 |
| API Spec ↔ operational docs | `022_API_specification.md` × ADR-012 | 2 |

## Gaps found

### DEF-S001: Fallback vs Required contradiction (AC ↔ API Spec)

**AC-001f** states: *"A subscriber event arrives with youtube_handle but no display_name... The record is created with display_name = youtube_handle (fallback)."*

**API Spec §4.1** defines `display_name` as **Required** with validation: `"Required, string, 1–255 chars"` → returns `VALIDATION_ERROR` if missing.

**Contradiction:** If API rejects empty `display_name`, AC-001f cannot pass. If API allows it, the validation rule is wrong.

**Resolution options:**
- A: Make `display_name` optional in API spec. Backend implements fallback.
- B: Keep `display_name` required. Remove or rewrite AC-001f.

**Pattern:** This is the most common spec gap — one author writes permissive behavior (fallback), another writes strict validation. Happens when ACs and API specs are written by different personas at different times.

---

### DEF-S003: Trigger idempotency risk (DB Schema ↔ AC)

**DB Schema §5.2** defines `sync_viewer_points()` trigger: fires `AFTER UPDATE ON donations WHEN (OLD.match_status IS DISTINCT FROM NEW.match_status)`, adds `NEW.amount_thb` to `total_points`.

**Risk:** If a donation transitions `pending → matched → manual_review → matched`, the trigger fires twice on `→ matched`, double-counting the amount.

**The `IS DISTINCT FROM` guard prevents re-fire on same status, but doesn't prevent re-entry from a different starting status.**

**Resolution:** Add explicit guard: `IF OLD.match_status != 'matched' AND NEW.match_status = 'matched' THEN ...`

**Pattern:** DB triggers that accumulate values (SUM, COUNT) are inherently risky if the triggering condition can be satisfied multiple times. Always check: "can this transition happen more than once?"

---

### DEF-S004: Defined behavior with no test coverage (API Spec ↔ ACs)

**API Spec §5** defines rate limiting: "100 requests/minute per IP (Fiber middleware)" and webhook tier at "200 requests/minute."

**ACs (013):** No acceptance criterion covers rate limiting behavior. No test case verifies 429 response.

**Resolution options:**
- A: Add AC + test case for rate limit behavior (recommended)
- B: Explicitly defer to Phase 2

**Pattern:** API specs often define infrastructure behavior (rate limiting, CORS, pagination limits) that ACs skip because they focus on business logic. QA should flag these gaps.

---

### DEF-S005: Security operations gap (API Spec ↔ operational docs)

**API Spec §4.4** defines HMAC-SHA256 webhook verification with `secret_key` from environment variable.

**Gap:** No documentation for:
1. Initial key generation/sharing with EasyDonate
2. Key rotation procedure (security incident response)
3. Whether EasyDonate supports multiple active keys during rotation

**Resolution:** Document key rotation procedure. Consider vault-based secret management.

**Pattern:** Security mechanisms defined in API specs rarely include operational runbooks. The spec says "use HMAC" but doesn't say "here's how to rotate the key when it's compromised."

---

### DEF-S006: External system retry behavior unclear (API Spec)

**API Spec §4.4** defines webhook error response: `401` for invalid HMAC signature.

**Gap:** Some webhook systems retry on 4xx errors. If EasyDonate retries on 401, returning 401 for invalid signatures causes repeated failed attempts. Better to return `200` with `{"skipped": true}`.

**Resolution:** Verify EasyDonate's webhook retry policy. If they retry on 4xx, change error response to 200-with-error-body.

**Pattern:** Webhook error responses must account for the sender's retry behavior. Always check: "does this external system retry on my error codes?"

---

## Technique summary

The cross-reference pairs that yield the most gaps:

1. **AC ↔ API Spec** — permissive vs strict field handling
2. **API Spec ↔ DB Schema** — trigger idempotency, constraint coverage
3. **API Spec ↔ ACs** — infrastructure behavior with no test coverage
4. **Security mechanisms ↔ operational docs** — missing runbooks
5. **Error responses ↔ external system behavior** — retry policy mismatches
