# Backend API Checklist Review — 2026-08-05

## Context
Reviewed `F:\obsidian_note\swe-knowledge\checklist\api-checklist\api.md` — a 200-line, 17-section backend project checklist. Last updated 2026-06-11.

## Assessment Framework Used
Rated gaps in three tiers:
- 🔴 **Critical** — Must-add, reflects 2026 production requirements
- 🟡 **High-Value** — Significant improvement, covers common patterns
- 🟢 **Minor** — Nice-to-have, polish items

## Gaps Identified and Filled

### 🔴 Critical (new sections added)
| Area | Items Added | Section |
|---|---|---|
| AI/LLM Integration | 9 items (prompt injection, output validation, token costs, model fallback, streaming, hallucination guardrails, content safety, LLM observability, data sent to external models) | §18 |
| Data Privacy & Compliance | 11 items (PII inventory, log masking, erasure, access, consent, retention, audit trail, DPAs, breach notification, encryption, minimization) | §19 |

### 🔴 Critical (items added to existing sections)
| Area | Section | Detail |
|---|---|---|
| Supply chain security | §7 | SBOM, Sigstore/cosign, SLSA, lockfile integrity |
| Zero Trust / workload identity | §7 | mTLS, SPIFFE/SPIRE, service-to-service auth |

### 🟡 High-Value Additions
| Area | Section | Detail |
|---|---|---|
| Connect Protocol | §4 | Modern grpc-gateway replacement |
| API deprecation | §4 | RFC 8594 headers, sunset dates |
| WebSocket/SSE | §4 | Auth, heartbeat, backpressure, reconnection |
| Cost observability | §8 | Per-tenant cost, anomaly alerts, LLM budgets |
| Outbox pattern | §11 | Exactly-once publishing from transactional context |
| Mutation testing | §13 | Verify tests catch bugs (≥80% mutation score) |
| Feature flag hygiene | §17 | Ownership, expiry, quarterly audits |

### 🟢 Minor
- GraphQL depth/complexity (already partially covered in §7)
- eBPF observability (noted but not added — too emerging)

## Cross-Reference Fixes
- Section 10 → 11 (Message Queues) in §14 Async Processing
- Section 13 → 14 (Performance) in §17 Graceful Shutdown

## Technique: Batching via execute_code
The most efficient approach was wrapping multiple `patch()` calls in a single `execute_code` script. This turned ~10 round-trips into 2-3 script executions. Pattern:

```python
from hermes_tools import patch

file_path = r"F:\path\to\file.md"

# All related patches in one script
patch(file_path, old1, new1)
patch(file_path, old2, new2)
patch(file_path, old3, new3)

print("Done.")
```

## Quick Sanity Check — 5 New Gates Added
- SBOM generated and attached to build artifact
- No PII in logs (verified by searching log output)
- LLM inputs sanitized, outputs validated against schema
- Right-to-erasure pipeline tested end-to-end
- Data retention policy enforced (old records actually purged)

## Result
200 → 250 lines, 17 → 19 sections. All changes applied, cross-references verified.
