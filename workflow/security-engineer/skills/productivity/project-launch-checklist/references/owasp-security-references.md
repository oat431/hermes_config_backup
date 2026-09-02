# OWASP Security Reference Snapshot

> Captured 2026-08-07 via searxng MCP for security checklist audit.
> Verify currency before relying on these — OWASP lists update yearly.

## OWASP API Security Top 10 (2023)

The most recent API-specific list. Key risk: **API1:2023 Broken Object Level Authorization (BOLA/IDOR)** is #1 — the most common API vulnerability. Every object access must check ownership.

Full list:
1. API1:2023 — Broken Object Level Authorization (BOLA)
2. API2:2023 — Broken Authentication
3. API3:2023 — Broken Object Property Level Authorization (mass assignment, data exposure)
4. API4:2023 — Unrestricted Resource Consumption
5. API5:2023 — Broken Function Level Authorization (BFLA)
6. API6:2023 — Unrestricted Access to Sensitive Business Flows
7. API7:2023 — Server Side Request Forgery (SSRF)
8. API8:2023 — Security Misconfiguration
9. API9:2023 — Improper Inventory Management
10. API10:2023 — Unsafe Consumption of APIs

Source: https://owasp.org/API-Security/editions/2023/en/0x11-t10/

## OWASP Top 10 for LLM Applications (2025)

Supersedes the 2023 v1.1 list. Three categories are NEW in 2025: LLM07, LLM08, LLM10.

Full list:
1. LLM01 — Prompt Injection (direct + indirect via retrieved content)
2. LLM02 — Sensitive Information Disclosure
3. LLM03 — Supply Chain Vulnerabilities (models, datasets, MCP servers)
4. LLM04 — Data and Model Poisoning
5. LLM05 — Improper Output Handling (treat output as untrusted input)
6. LLM06 — Excessive Agency (per-agent identity, tool allowlists, human approval)
7. LLM07 — System Prompt Leakage **(NEW in 2025)**
8. LLM08 — Vector and Embedding Weaknesses **(NEW in 2025)**
9. LLM09 — Misinformation (absorbs former "Overreliance")
10. LLM10 — Unbounded Consumption **(NEW in 2025, expanded from "Model DoS")**

Removed from v1.1: "Insecure Plugin Design" and "Model Theft" — distributed across LLM03 and LLM06.

### Architecture-weighted prioritization

| Pattern | Highest-priority risks |
|---|---|
| Chat-only | LLM01, LLM02, LLM09 |
| RAG | + LLM08, LLM03 (embedding models) |
| Agentic (tool-calling) | + LLM06, LLM10, LLM05 |

Source: https://owasp.org/www-project-top-10-for-large-language-model-applications/

## Key gap patterns found in security checklists

During the 2026-08-07 audit of `security-checklist/security.md`, these were the most commonly missing items:

1. **IDOR/BOLA** — object-level authorization (OWASP API #1)
2. **XXE** — XML external entity prevention
3. **Path traversal / Zip Slip** — archive extraction sanitization
4. **Open redirect** — redirect/next/returnTo parameter validation
5. **OAuth2/OIDC flow correctness** — PKCE, redirect allowlist, state/nonce
6. **Dependency confusion** — internal package name squatting
7. **Immutable backups** — WORM/object-lock for ransomware
8. **Log integrity** — tamper-evident audit logs (append-only/WORM)
9. **Excessive Agency** (LLM06) — per-agent identity, not shared service accounts
10. **System Prompt Leakage** (LLM07) — no secrets in system prompts
11. **Vector/Embedding isolation** (LLM08) — namespace-level tenant isolation
12. **Unbounded Consumption** (LLM10) — token rate limits, cost quotas
