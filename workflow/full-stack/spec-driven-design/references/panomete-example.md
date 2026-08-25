# Worked Example: Panomete Platform

> Full lifecycle across three sessions. **Session 1** produced the initial 11-document design phase (contained errors). **Session 2** (grill-me) discovered existing infrastructure that invalidated the design. **Session 3** completed the PO revision + design rewrite cycle — producing 11 corrected v0.2 documents.

## Session 1: Initial Design (Pre-Grill — contained errors)

Assuming greenfield: Gate on :80/:443, `panomete.local` domain, dedicated guard-db PostgreSQL 15, self-signed TLS, in-memory rate limiting.

**Output: 11 files at v0.1 — 10 of 11 were wrong.**

## Session 2: Grill-Me — Discovery of REAL Architecture

### What was discovered (by asking, not assuming):

| Assumption (Wrong) | Reality | Source |
|---|---|---|
| Greenfield Docker Compose | Existing homelab with Nginx, Cloudflare Tunnel, PostgreSQL 18, Valkey 9, Portainer, AdGuard, Tailscale, UFW, Fail2ban | `Home Lab App.md` server inventory |
| `panomete.local` domain | `*.panomete.com` with subdomain routing via Nginx | User's subdomain plan |
| Gate on :80/:443 (edge) | Nginx is the edge. Gate on port 8000 behind Nginx. | Existing Nginx reverse proxy |
| Path-based routing through Gate | Hybrid: foundation = subdomains (auth, discovery), business APIs = paths through Gate | User confirmed |
| Dedicated guard-db PostgreSQL 15 | Shared existing PostgreSQL 18 — just add a `keycloak` database | Already running |
| In-memory rate limiting | Valkey 9 already running — use it for rate limiting | Infrastructure inventory |
| Self-signed TLS at Gate | Cloudflare Tunnel handles external TLS. Plain HTTP internally. | Already configured |
| Guard = Spring Boot wrapper? | Guard IS Keycloak. No wrapper. Gate validates JWT locally via JWKS. | Confirmed in grill |

### The affect-doc Pattern (Post-Grill)

After Session 2, Dev/SA produced `spec/meeting-minute/affect-doc.md` — a 150-line meeting minutes document listing:

- 13 PO-owned files requiring changes (12 🔴 Critical, 1 🟡 Moderate)
- Exact line numbers with old text → new text for each
- 9 design decisions codified (D1-D9)
- A handoff checklist for PO

**This is the cross-persona contract.** Without it, PO doesn't know what to change.

## Session 3: PO Revision → Design Rewrite

### PO's Update
PO produced `spec/meeting-minute/po-update-2026-07-22.md` documenting 12 files updated to v0.2.

### Dev Verification (spot-reading before rewriting)
Dev spot-read 4 critical files and found 3 issues:
1. Guard + Discover story docs: version still `0.1` in frontmatter (content was updated, tags forgotten)
2. Guard `Related Documents`: still said "Gate routes auth traffic through Guard" (stale)
3. Discover summary table: still said "Dashboard via Gateway" (should be "Dashboard via Nginx")

**Applied 6 parallel `patch` calls to fix all 3 issues** before starting the design rewrite.

### Full Design Rewrite — 11 docs, all v0.2

| Document | Key Changes |
|----------|------------|
| **Platform SAD (025)** | Rewrote architecture diagram: Cloudflare → Nginx → services. Added request flow sequence diagram. Updated deployment topology to reflect shared infrastructure. |
| **Platform ADR (021)** | Removed ADR on TLS (Cloudflare handles it). Added ADR-005 (shared PG18), ADR-006 (Nginx edge), ADR-008 (Valkey rate limiting), ADR-009 (hybrid routing). |
| **Platform Arch Overview (029)** | Simplified: key rules, port map, one sequence diagram. |
| **Guard ADR (021)** | Added ADR-G006 (shared PG18), ADR-G007 (Guard IS Keycloak). Removed wrapper-service language. |
| **Guard API Spec (022)** | Domain: `auth.panomete.com`. Port: 8001. Note: Gate validates JWT locally, no calls to Guard. |
| **Guard DB Schema (023)** | Rewrote for shared PostgreSQL 18 (not dedicated container). `jdbc:postgresql://host.docker.internal:5432/keycloak`. |
| **Guard ERD (024)** | Simplified to logical realm model only. |
| **Discover ADR (021)** | Added ADR-D003 (dashboard via Nginx), ADR-D005 (dual ports 8999/3999). |
| **Discover API Spec (022)** | Ports: 8999 (BE), 3999 (FE). Dashboard at `discovery.panomete.com` via Nginx. |
| **Gate ADR (021)** | Superseded ADR-W005 (Valkey, not in-memory). Added ADR-W006 (internal-only behind Nginx), ADR-W007 (no TLS). |
| **Gate API Spec (022)** | Removed `/auth/**` and `/eureka/**` routes. Added Valkey config. Removed TLS section. Added note: "Foundation services routed by Nginx, not Gate." |

### Final Consistency Check

All docs show `version: "0.2"`. Requirements (PO, 12 docs) and Design (Dev/SA, 11 docs) aligned. Architecture matches production infrastructure.

## Grill-Me Session Structure (what worked)

```
Round 1: Guard identity — "Is Guard Keycloak itself or a wrapper?"
Round 2: Domain & TLS — user pointed to Home Lab App.md (critical infra doc)
Round 3: Nginx vs Gate — user was unsure, presented 4-option trade-off table
Round 4: Shared vs dedicated infrastructure
Round 5: Rapid fire (routing, TLS, observability — 1 question at a time)
Round 2 (post-PO): Version tag consistency, stale text, lingering errors
```

## Key Lessons

1. **Phase 0 (Pre-Design Discovery) is mandatory.** Without it, 10 of 11 docs were wrong.
2. **The affect-doc is the persona handoff contract.** Don't skip it.
3. **Spot-read PO's work before trusting it.** Version tags and cross-references are the first things to check.
4. **Fix minor PO oversights yourself.** Don't waste a round-trip for 3 lines.
5. **Version consistency across all docs matters.** PO v0.2 → Design v0.2. Mismatched versions create confusion for the next persona.
