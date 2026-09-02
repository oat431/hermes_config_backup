# Security Docs from Spec — Worked Example (Deerngo Bot)

> Source: Deerngo Bot VRM project. No code repo existed — all security findings derived from spec docs (022 API Spec, 021 ADRs, 023 DB Schema, 029 Architecture Overview, 035 BE Coding Standards).

## Threat Model Derivation

### Attack surface mapped from architecture (029)

| Surface | Exposure | Source Document |
|---------|----------|-----------------|
| Webhook endpoint | Public (Cloudflare Tunnel) | 029 §6 Port Map + ADR-011 |
| Scoreboard page | Public (Cloudflare Tunnel) | 029 §6 + ADR-011 |
| Scoreboard API | Public (Next.js → Go via Docker) | 022 §4.3 |
| Subscriber API | LAN only (192.168.1.121:8008) | 022 §2 + ADR-004 |
| Points API | LAN only | 022 §2 |
| PostgreSQL | Docker network only | 029 §4 |

### Trust boundaries from architecture (029)

```
Internet → Cloudflare (TLS/DDoS) → Next.js (:3008) → Go (:8008) → PostgreSQL (:5432)
                                         ↑
LAN → streamer.bot (Windows PC) ────────┘
EasyDonate → Webhook (HMAC verified) → Go
```

Key insight: Only 2 entry points face the internet (webhook + scoreboard). Everything else is LAN/Docker-internal. This dramatically reduces the attack surface.

## OWASP Assessment from Spec

| OWASP | Spec Source | Finding |
|-------|-----------|---------|
| A01 Access Control | 022 §2 "Authentication: None for Phase 1" | Accepted — LAN-only design |
| A02 Crypto | ADR-012 (HMAC-SHA256) | Pass — but key rotation gap (DEF-S005) |
| A03 Injection | 035 §5.3 (sqlx named params) | Pass — parameterized queries in coding standards |
| A04 Insecure Design | 022 §5 (rate limiting defined) | Partial — no ACs for rate limiting (DEF-S004) |
| A05 Misconfiguration | 022 §6 (CORS mentioned but not configured) | Partial — CORS spec gap |
| A06 Components | 033 (dependency manifest) | Pending — govulncheck needed after code |
| A07 Auth Failures | 022 §2 "None for Phase 1" | Pass — by design |
| A08 Data Integrity | ADR-012 + 022 §4.4 (HMAC + idempotency) | Partial — replay attack risk |
| A09 Logging | 035 §9 (logging middleware) | Partial — no security audit logging |
| A10 SSRF | 022 §4.5-4.6 (fixed URLs for YouTube/EasyDonate) | Pass — no user-controlled URLs |

## Security Findings Derived

| ID | Finding | Severity | How Found |
|----|---------|:--------:|-----------|
| SEC-001 | No auth on internal endpoints | 🟡 | 022 §2 "Authentication: None" |
| SEC-002 | Webhook replay vulnerability | 🟡 | ADR-012 mentions "timestamp check for replay protection" but not implemented |
| SEC-003 | HMAC secret in env var | 🟢 | ADR-012 "secret stored as environment variable" |
| SEC-004 | No security headers | 🟢 | 035 middleware section has no security headers |
| SEC-005 | No CORS configuration | 🟡 | 022 §6 mentions CORS but no config defined |
| SEC-006 | No request size limit | 🟢 | 022 §4.4 webhook has no body size limit |
| SEC-007 | SQL injection protected | ✅ | 035 §5.3 sqlx named params |
| SEC-008 | Public scoreboard data | 🟢 | 022 §4.3 exposes YouTube handles publicly |

## Security Coding Standards Derivation

Source: 035 BE Coding Standards (Go/Fiber/sqlx) + ADRs.

| Topic | Derived From | Rule Added |
|-------|-------------|------------|
| HMAC verification | ADR-012 + 035 §5.1 | `hmac.Equal` constant-time comparison |
| SQL injection | 035 §5.3 | Named params only, no `fmt.Sprintf` |
| Error handling | 035 §5.4 | Generic client messages, internal logging |
| Rate limiting | 022 §5 | Fiber limiter middleware config |
| CORS | 022 §6 | Explicit origins, restricted methods |
| Security headers | Not in 035 | Added: X-Content-Type-Options, X-Frame-Options, CSP |
| Secret management | ADR-012 + 035 §9 | Env vars only, startup validation, no logging |
| Input validation | 022 §4.1 validation rules | Handler-layer validation pattern |
| PR checklist | All above | 10-point security review checklist |
