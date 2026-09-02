# Deerngo Bot — Design Session Example

> **Date:** 2026-07-29
> **Project Type:** Single service (Go monolith), simple infrastructure
> **Complexity:** Simple — homelab Docker deploy, existing Cloudflare Tunnel, shared PostgreSQL

## Session Summary

PO persona produced requirements (011_business_objective, 012_user_stories, 013_acceptance_criteria) and handed off to SA/Designer persona via meeting minute (MM01). SA ran grill-me protocol, resolved 5 open design decisions, produced 6 design documents, then had to correct deployment topology and port assignments after user clarification — requiring rewrites of 4 documents.

## ⚠️ Mid-Session Corrections (Key Learnings — 4 corrections)

### 1. Deployment Topology (Critical)

**What happened:** The PO meeting minute said "Local Windows deployment" and the user initially confirmed "PostgreSQL exists, Cloudflare Tunnel running, greenfield code." SA assumed Go backend + Next.js would run on the Windows PC alongside streamer.bot. After all 6 documents were written, the user corrected: "actually about deployment api, routine, frontend is running at my homelab server, only streamer.bot is running on local window pc."

**Impact:** 4 documents needed rewriting (ADR-004, ADR-011, API Spec base URLs, SAD deployment diagram, Architecture Overview). The correction cascaded through:
- Deployment topology diagram (Windows PC → Homelab Docker)
- Network communication (localhost → LAN 192.168.1.121:8008)
- Docker Compose configuration (new — wasn't needed for bare Windows)
- Cloudflare Tunnel origin (Windows → homelab systemd)
- API base URL (localhost:8008 → 192.168.1.121:8008 for streamer.bot)

**Lesson:** After grill Round 1, SSH into the homelab and run `docker ps`, `docker network inspect`, `psql -l` BEFORE writing documents. "PostgreSQL exists, Cloudflare Tunnel running" doesn't tell you WHERE Go/Next.js should deploy. See `references/infrastructure-verification.md` for the exact commands.

**What was discovered via SSH:**
- Homelab: Ubuntu 26.04, Docker 29.6.2, Docker Compose v5.3.1
- PostgreSQL 18: Docker container `local-postgres` on `db-network` (172.20.0.3)
- `deerngo` database already existed in PostgreSQL
- Cloudflare Tunnel: systemd service `cloudflared.service` (not Docker)
- Homelab LAN IP: 192.168.1.121
- All infra containers on `db-network` Docker network

### 2. Port Assignment (User Preference)

**What happened:** SA assigned default ports `:8080` (Go) and `:3000` (Next.js). User has a strict port registry at `F:\obsidian_note\oralita_md\Quick Note\Home Lab App.md` with ranges: 8000-9000 (BE), 3000-4000 (FE), 7000-8000 (self-hosted).

**User correction:** "i really want a custom port — so you can check available port here: Home Lab App.md"

**Resolution:** Next available: **8008** (BE) and **3008** (FE). Updated all 4 affected docs (21 occurrences). Registered in Home Lab App doc with 🚧 status.

**Lesson:** ALWAYS read the port registry before assigning ANY port. Never use arbitrary defaults (8080, 3000, 5000).

### 3. Domain Naming

**What happened:** SA assumed `scoreboard.panomete.com`. User wanted `deerngo-viewer-score.panomete.com` (verbose but project-specific).

**Lesson:** Don't assume domain naming preferences. Use the project name as prefix when the user has multiple projects under one domain.

### 4. Framework Version Bump

**What happened:** SA wrote "Fiber v2" in all docs. User said "i think latest version of fiber is version 3 — i will use version 3 for this project, will it affect any core logic?"

**Resolution:** Checked Fiber v3 docs — confirmed `fiber.Ctx` handler pattern is backward compatible. Updated all 4 affected docs via `sed -i`. No core logic changes needed.

**Lesson:** When a user suggests a version bump, check for breaking changes BEFORE updating docs. Don't just sed-replace — verify the API is compatible. If breaking, the SAD's project structure, handler signatures, and middleware setup all need rewriting.

## Grill-Me Session (3 rounds)

### Round 1 — Infrastructure Reality
**Questions asked:** Existing database? Reverse proxy? Greenfield code?
**Answers:** PostgreSQL 18 exists (shared homelab), Cloudflare Tunnel already running, greenfield code.
**Key insight:** No infra docs to read — simple setup. Skipped "read infrastructure docs" step.

### Round 2 — Design Decisions (DEC-D01 → DEC-D05)
**Questions asked:** Presented all 5 open decisions as a 4-option multiple-choice.
**Answers:** sqlx + Fiber + Tailwind/DaisyUI + Cloudflare Tunnel + HMAC-SHA256.
**Key insight:** User picked `sqlx` (not `sqlc` or GORM) and `DaisyUI` (not shadcn/ui) — non-default choices that wouldn't have been guessed. Always present options, don't assume.

### Round 3 — Technical Details
**Questions asked:** Go version? Node version? Fuzzy matching approach? OAuth token storage?
**Answers:** "Just assume latest stable — design it."
**Key insight:** For simple projects, users often don't care about minor version details. Don't over-grill.

## Decisions Made

| ID | Decision | Options Presented | Chosen |
|----|----------|-------------------|--------|
| DEC-D01 | Go database layer | GORM / sqlc / raw sql / **sqlx** | sqlx |
| DEC-D02 | Go web framework | Gin / Echo / Chi / stdlib / **Fiber** | Fiber |
| DEC-D03 | Scoreboard UI | shadcn/ui / Material UI / plain CSS / **DaisyUI** | DaisyUI |
| DEC-D04 | Public access | Cloudflare Tunnel / ngrok / Tailscale | Cloudflare Tunnel |
| DEC-D05 | Webhook verification | HMAC-SHA256 / shared secret / IP whitelist | HMAC-SHA256 |

## Documents Produced (6 total)

| # | Document | Template | Key Content |
|---|----------|----------|-------------|
| 1 | ADR (021) | 021_architecture_decision_records.md | 12 ADRs (7 from PO + 5 design decisions) |
| 2 | API Spec (022) | 022_API_specification.md | 4 REST endpoints + 1 webhook + 3 internal schedulers |
| 3 | DB Schema (023) | 023_database_schema_DDL.md | 4 tables, pg_trgm indexes, auto-sync trigger |
| 4 | ERD (024) | 024_ERD.md | Mermaid ERD + entity definitions + data flow |
| 5 | SAD (025) | 025_software_architecture_document.md | Modular monolith, Go project structure, deployment topology |
| 6 | Arch Overview (029) | 029_architecture_overview.md | One-page "map" with sequence diagrams |

## Scoping Decisions

This was a **stateful single service** (has DB), so all 6 documents were produced:
- ADR ✅ (12 decisions to formalize)
- API Spec ✅ (4 endpoints + webhook)
- DB Schema ✅ (4 tables)
- ERD ✅ (4 entities)
- SAD ✅ (full architecture for single service)
- Arch Overview ✅ (stakeholder-friendly map)

🟡 Should Have docs (Wireframes, Style Guide) were NOT produced — Tailwind/DaisyUI provides defaults, and wireframes need separate UI/UX work.

## Grill-Me Adaptation Notes

The standard grill-me protocol assumes enterprise platform complexity (Nginx, Keycloak, subdomain routing, TLS strategy). For this simple project:
- **Skipped:** Domain scheme, edge proxy details, TLS strategy, port conflicts, service identity, observability timing
- **Focused on:** Infrastructure existence (DB, tunnel), design decisions (5 open items), tech versions
- **Result:** 3 rounds instead of 4, ~10 minutes instead of 30+

## Tech Stack (Resolved)

| Layer | Technology | Version | Location |
|-------|-----------|---------|----------|
| Backend | Go + Fiber v3 + sqlx | 1.24+ | Homelab (Docker, `db-network`) |
| Frontend | Next.js + Tailwind + DaisyUI | 22 LTS / 4+ / 5+ | Homelab (Docker, `db-network`) |
| Database | PostgreSQL 18 (shared homelab) | 18 | Homelab (Docker, `db-network`) |
| Fuzzy Matching | pg_trgm extension | built-in | PostgreSQL |
| Public Access | Cloudflare Tunnel | systemd service | Homelab |
| Webhook Auth | HMAC-SHA256 | — | Go backend |
| Automation | streamer.bot | latest | **Windows PC** (LAN → 192.168.1.121:8008) |

## Corrected Deployment Topology

```
Windows PC                          Homelab Server (Ubuntu 26.04, Docker)
+------------------+                +-------------------------------------+
|  streamer.bot    |                |  Docker Network: db-network         |
|  :7474, :8681    |--- LAN ------->|  +------------+  +---------------+ |
|                  |  192.168.1.121  |  | Go Backend |  | Next.js       | |
|  ":deer: point"  |    :8008       |  | :8008      |  | :3008         | |
|  ":deer: donate" |                |  +------+-----+  +------+--------+ |
+------------------+                |         |               |           |
                                    |  +------v-----+        |           |
                                    |  | PostgreSQL 18|       |           |
                                    |  | :5432        |       |           |
                                    |  +--------------+       |           |
                                    |                         |           |
                                    |  cloudflared (systemd) <-+          |
                                    +---------------------+---------------+
                                                          |
                                                          v
                                         deerngo-viewer-score.panomete.com
```

## Port Registry Entry

```markdown
| Deerngo Bot | deerngo | Deerngo Bot | 8008 | 3008 | 🚧 |
```

Registered in `F:\obsidian_note\oralita_md\Quick Note\Home Lab App.md` under "Personal Project : 8000-9000 (BE) | 3000-4000 (FE)".
