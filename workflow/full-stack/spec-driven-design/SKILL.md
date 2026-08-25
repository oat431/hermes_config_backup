---
name: spec-driven-design
description: Generate design-phase documents (ADR, API Spec, DB Schema, ERD, SAD, Arch Overview) from completed requirements-phase specs. Used when the PO persona has finished 01_requirement docs and the Dev/SA persona needs to produce 02_design documents for handoff to other personas.
---

# Spec-Driven Design Document Generation

## Trigger

User has completed the requirements phase (01_requirement docs exist for their services/platform) and asks the Dev/SA persona to produce design-phase documents (02_design). They may say "fill up these templates," "do the designing part," or "create the design docs."

## Workflow

### Phase 0: Pre-Design Discovery (MANDATORY — before reading requirements)

> ⚠️ **This is the most important phase.** Skipping it produces beautiful architecture docs that don't match reality. The PO's requirement docs were written in a vacuum — your job is to reconcile the ideal with the real.

1. **Ask about existing infrastructure BEFORE reading requirement docs.** The user already has stuff running. Ask:
   - "What infrastructure is already set up? Reverse proxy? Database? Cache? DNS? Container orchestration?"
   - "Is this greenfield or are you adding to an existing environment?"
   - "Do you have infrastructure documentation or a server inventory I should read?"

2. **Load and read ALL infrastructure docs the user references.** If they point you at a server setup checklist, a subdomain plan, or a home lab inventory — READ IT FIRST. These docs will contradict or constrain your design.

3. **Run the grill-me protocol** (see below). Before producing any document, extract these architectural decisions:
   - **Domain scheme**: What domains/subdomains? Path-based or subdomain routing?
   - **Edge proxy**: What sits at the edge? Cloudflare? Nginx? Traefik? Nothing?
   - **TLS strategy**: Where is TLS terminated? Self-signed or real certs?
   - **Port assignments**: Are ports standardized? Any conflicts with existing services?
   - **Infrastructure sharing**: Use existing shared DB/cache or dedicated containers?
   - **Service identity**: For off-the-shelf services (Keycloak, Eureka) — are they deployed AS-IS or with a wrapper?
   - **Observability timing**: Phase 1 (alongside) or Phase 2 (after foundation stable)?

4. **Reconcile with requirements.** After reading infra docs + grill-me answers, compare against the PO's requirement docs. Flag conflicts before designing. Example: PO docs may describe Gateway on :80/:443, but Nginx already owns those ports.

5. **VERIFY deployment topology physically (if SSH access available).** After the grill session, before writing ANY document, SSH into the target infrastructure and run verification commands. This catches assumptions that grill questions miss. See `references/infrastructure-verification.md` for the exact commands. At minimum, verify:
   - Which machine runs what (Docker containers, systemd services)
   - Docker network topology (`docker network inspect`)
   - Port bindings and conflicts
   - Whether databases already exist (`psql -l`)
   - How the tunnel/proxy is configured (systemd vs Docker vs manual)

### Phase 1: Context Gathering (parallel reads)

1. **Read the project README** — understand the service catalog, tech stack, and overall platform vision
2. **Read ALL requirement docs in parallel** for every service that needs design docs:
   - `011_business_objective.md`
   - `012_user_stories.md`
   - `013_acceptance_criteria.md`
   - `014_stakeholder_analysis.md` (if present)
3. **Read ALL design templates** in parallel from the `template/02_design/` directory — these define the expected format, frontmatter, and section structure
4. **Find a reference implementation** — look for a sibling service that already has completed 02_design docs (e.g., `tiny_mchwa`). Read ALL of them in parallel to understand expected depth, tone, and formatting conventions

### Phase 2: Scoping

Before writing a single doc, determine what each service actually needs:

| Service Type | ADR | API Spec | DB Schema | ERD | SAD | Arch Overview |
|-------------|:---:|:---:|:---:|:---:|:---:|:---:|
| **Platform umbrella** | ✅ | — | — | — | ✅ | ✅ |
| **Stateful service (has DB)** | ✅ | ✅ | ✅ | ✅ | — | — |
| **Stateless service (no DB)** | ✅ | ✅ | — | — | — | — |
| **Off-the-shelf (managed DB)** | ✅ | ✅ | ✅ (provisioning, not schema) | ✅ (logical model) | — | — |

### Phase 3: Document Production

Produce documents in priority order. Batch writes to minimize round-trips:

1. **Platform-level first** (unblocks service-level docs that reference platform ADRs):
   - SAD (025): Full architecture — component design, data flow, deployment topology, quality attributes, security model, ADR summary
   - ADR (021): 5-10 platform-level decisions with context/consequences/alternatives
   - Architecture Overview (029): One-page "map" — simplified diagrams, port map, startup sequence

2. **Service-level per service**, parallel where possible:
   - ADR (021): 3-6 service-specific decisions that don't duplicate platform ADRs — implementation details, trade-offs unique to this service
   - API Spec (022): Full endpoint catalog with request/response schemas, error codes, auth requirements
   - DB Schema (023): DDL, indexes, triggers, migration strategy — OR for off-the-shelf services, provisioning script and connection config
   - ERD (024): Mermaid diagram + entity definitions + relationship rules

### Document Quality Standards

- **Frontmatter**: Match the reference implementation's frontmatter style. Include `parent_platform` for service-level docs
- **Diagrams**: Use Mermaid (`flowchart`, `sequenceDiagram`, `erDiagram`). Every architecture doc needs at least one diagram
- **Cross-references**: Link to related docs using Obsidian wiki-link syntax (`[[path/doc]]`)
- **ADR format**: Status → Date → Context → Decision → Consequences (±/∓) → Alternatives Considered (with "Why Not")
- **Version everything**: Set version to `0.1`, status to `Draft`, author to `Dev / SA Persona`
- **Don't repeat**: Service ADRs should NOT re-litigate platform ADRs. Link to them instead.

## Document Handoff Matrix

| Document | Primary Consumer | What They Need From It |
|----------|:---:|---|
| ADR (021) | PO, DevOps, Future Self | Why decisions were made; trade-offs accepted |
| API Spec (022) | QA, DevOps | Contract for testing and deployment |
| DB Schema (023) | DevOps, QA | Schema for environment setup and test data |
| ERD (024) | Dev, PO | Visual data model for understanding relationships |
| SAD (025) | Dev, DevOps | Primary architectural reference for implementation |
| Arch Overview (029) | All roles, Portfolio Reviewer | Entry point — the "map" |

## The Grill-Me Protocol

> Structured Q&A technique to extract architectural decisions from the project owner BEFORE writing design docs. Use `/grill-me` or proactively ask these questions.

### When to Grill

Grill BEFORE writing any document. The answers change everything — domain names, port assignments, TLS strategy, deployment topology. A single wrong assumption (e.g., "Gate sits on :80/:443") invalidates every doc that references it.

### Core Grill Questions (ask in rounds of 2-4)

> ⚠️ **Adapt to project complexity.** Not every project is an enterprise platform with Nginx, Keycloak, and subdomain routing. For simple projects (single service, local deploy, existing tunnel), skip irrelevant rounds and focus on what actually constrains the design. Use the **Project Complexity Heuristic** below to decide which rounds to ask.

#### Project Complexity Heuristic

| Signal | Complexity | Grill Approach |
|--------|-----------|----------------|
| Single service, single DB, local deploy | **Simple** | Ask Rounds 1+2 only (infrastructure + design decisions). Skip gateway/TLS/multi-service questions. |
| Multiple services, shared infra, homelab | **Medium** | Ask Rounds 1-3. Skip enterprise edge cases. |
| Multi-team, cloud, API gateway, microservices | **Complex** | Ask all 4 rounds. |

#### Round 1 — Infrastructure Reality (ALWAYS ask)
- What infrastructure is already running? Database? Cache? Reverse proxy? Tunnel?
- Is this greenfield code or adding to an existing codebase?
- Any infrastructure docs or server inventory I should read FIRST?

#### Round 2 — Design Decisions (ALWAYS ask)
- For each open decision in the PO's handoff (DEC-D01, DEC-D02, etc.), present the options and get the user's call
- Tech stack choices: language version, framework, ORM/DB library, CSS framework
- If the PO already made decisions (DEC-001, DEC-002, etc.), confirm them — don't re-litigate
- **Port allocation**: Read the user's port registry (e.g., `F:\obsidian_note\oralita_md\Quick Note\Home Lab App.md`) BEFORE assigning ports. Follow the existing ranges (e.g., 8000-9000 BE, 3000-4000 FE). Pick the next available, not arbitrary ports like 8080/3000. Register the new service in the port registry after the user confirms.

#### Round 3 — Service Architecture (Medium/Complex only)
- What's the domain scheme? Subdomain-based or path-based?
- Is there an existing reverse proxy (Nginx, Traefik, Cloudflare)? What ports does it own?
- Where is TLS terminated?
- For off-the-shelf services (Keycloak, Eureka) — deployed AS-IS or with a wrapper?
- Observability: Phase 1 or deferred?

#### Round 4 — Edge Cases (Complex only)
- Any developer/debug access needed to internal ports?
- Resource constraints (RAM, CPU) on the target host?
- Any services that should NOT go through the gateway?

### Grill Anti-Patterns

- ❌ Don't ask all questions at once. 2-4 per round, adapt based on answers.
- ❌ Don't skip a round because you think you know the answer. The PO's requirement docs and the user's real infrastructure are different things.
- ❌ Don't ask yes/no questions when a 4-option clarify prompt would expose the actual trade-off.
- ❌ Don't grill about infrastructure that doesn't apply to the project. Asking "What's your API gateway strategy?" for a single Go binary on a Windows PC wastes everyone's time.
- ❌ Don't re-litigate decisions the PO already made (DEC-001 → DEC-007). Confirm them, then focus on the open decisions (DEC-D01 → DEC-D05).
### Phase 4: Post-Grill Reconciliation — The affect-doc Pattern

> After the grill session, the PO's requirement docs are almost certainly inconsistent with the discovered reality. Before rewriting YOUR design docs, produce a cross-persona handoff document.

1. **Create `spec/meeting-minute/affect-doc.md`** — a meeting minutes document listing every PO-owned file that needs changes:
   - Document path and severity (🔴 Critical / 🟡 Moderate)
   - Exact line numbers with the problematic text
   - What specifically needs to change (old → new)
   - A summary table grouping by service

2. **Format the affect-doc as a checklist** — PO should be able to work through it systematically without guessing. Include a "Handoff Checklist" section with checkboxes.

3. **Let PO do their job.** Say: "Go talk to PO. I'll be here." Don't rewrite design docs until PO confirms requirements are updated.

### Phase 5: PO Revision → Design Rewrite

> After PO says "I updated the docs," verify BEFORE rewriting.

1. **Read the PO's meeting minutes first** (they'll produce something like `po-update-2026-07-22.md`). Check:
   - Which documents were updated?
   - What version did they bump to?
   - Any decisions they pushed back on?

2. **Spot-read the most changed files** — don't trust the meeting minutes summary. Verify:
   - Is the version tag actually bumped? (POs often update content but forget frontmatter)
   - Are there lingering wrong references in "Related Documents" sections?
   - Do the architecture diagrams match the new design?

3. **Fix minor PO oversights immediately** — if you find stale version tags or wrong cross-reference text, use parallel `patch` calls to fix them before starting the design rewrite. Don't send them back to PO for 3 lines.

4. **Then rewrite all design docs** — bump all versions to match PO's new version, update every domain/port/architecture reference, add revision history entries.

## Pitfalls

- **⚠️ THE GREENFIELD ASSUMPTION (most common and costly mistake)**: Never assume the platform is being built from scratch on an empty host. The user almost certainly has infrastructure already running — Nginx, Cloudflare Tunnel, PostgreSQL, Redis/Valkey, Docker Compose, monitoring tools. Your beautiful architecture doc that puts Gateway on :80/:443 is wrong if Nginx already owns those ports. ALWAYS run Phase 0 (Pre-Design Discovery) before producing ANY document. Ask: "What's already running?" Read their infrastructure docs. A single unchecked assumption cascades through every document.
- **Infrastructure docs trump requirement docs**: When the user's server inventory says PostgreSQL 18 on port 5432 and your ADR says PostgreSQL 15 in a dedicated container, the server inventory wins. Reconcile discrepancies before designing, not after.
- **Empty `search_files` on Windows paths**: When `search_files` returns 0 results for directories that clearly exist, use `find` in terminal instead: `find /f/projects/... -name '*.md' -type f`. This is a known quirk with some Windows path formats.
- **Spec files vs directories**: In Obsidian-based specs, `spec/flowero_guard` may look like a directory path in wiki-links but is a directory containing numbered docs. Always probe with `find` or `ls` before assuming file paths.
- **Over-producing DB/ERD docs**: Services like Eureka (in-memory) and API Gateways (stateless) don't need DB schemas or ERDs. Scope per service type (see table above).
- **Off-the-shelf service DDL**: For services like Keycloak that manage their own schema, write a *provisioning* doc (create DB, create user, connection config), not a table DDL. The logical ERD is still useful.
- **Template rigidity**: Templates under `template/02_design/` are *guides* — the reference implementation and service context should override template placeholders. Never leave `[Author Name]` or `[Project Name]` in the final docs.
- **Writing docs before grill-me**: Producing 11 design documents and THEN discovering the user has Nginx at the edge means rewriting 10 of them. Grill first, write second.
- **Trusting PO meeting minutes without spot-reading**: When PO says "I updated 12 docs to v0.2," spot-read the 3 most critical files. PO may have updated content but forgotten to bump the frontmatter version tag. Also check "Related Documents" sections — stale cross-reference text (e.g., "Gate routes auth traffic through Guard") survives updates because POs focus on the body, not the footer.
- **Skipping the affect-doc**: After a grill session reveals requirement inconsistencies, DON'T just note them mentally and start rewriting design docs. Produce a formal `affect-doc.md` with exact line numbers. This is the contract between personas. Without it, PO doesn't know what to change, and you lose traceability.
- **Leaving PO doc fixes for later**: If you find 3 small issues (wrong version tag, stale table entry, incorrect cross-reference) after PO's revision, fix them with parallel `patch` calls immediately. Don't send them back to PO for trivial fixes — it's faster to fix them yourself and note it in the design rewrite.
- **Over-grilling simple projects**: The grill-me protocol has 4 rounds designed for enterprise platforms. For simple projects (single service, local deploy, existing tunnel), Rounds 3-4 are irrelevant. Use the Project Complexity Heuristic to skip unnecessary rounds. Asking "What's your API gateway strategy?" for a single Go binary on a Windows PC wastes everyone's time and signals you didn't read the meeting minute.
- **Presenting design decisions as open-ended**: When the PO handoff has open decisions (DEC-D01 → DEC-D05), present them as multiple-choice options with clear trade-offs, not as open-ended "what do you want?" questions. Users make faster, better decisions when they can compare concrete options. Use the `clarify` tool with 3-4 options per batch.

- **⚠️ MID-DESIGN REQUIREMENT CHANGES**: During the design phase, the user may request changes to requirements (e.g., "exclude 0-point viewers from scoreboard"). When this happens: (1) update the affected design documents first (API Spec, DB Schema, etc.), (2) update the SOURCE acceptance criteria in `01_requirement/013_acceptance_criteria.md` to match, (3) document the change in the handoff meeting minute's "Design Changes That Affect Requirements" section. Don't just update the design docs and forget the ACs — they'll diverge and confuse QA.

- **⚠️ DON'T PERSIST RUNTIME-GENERATED DATA**: When designing database schemas, question every column: "Is this value generated at runtime from other stored data?" If yes, don't persist it. Example: OAuth access tokens are generated from refresh tokens on each request — storing them in the DB is unnecessary. The user will often catch this ("just keep the refresh token here"), but be proactive. Strip columns that are: (a) short-lived and regenerable, (b) derived from other columns, (c) only needed during a single request lifecycle. The simplified schema is easier to maintain and avoids stale data bugs.

- **⚠️ VERSION BUMPS NEED VERIFICATION**: When a user says "I'll use version 3 instead of version 2" for a framework, check for breaking changes BEFORE updating the docs. Don't just sed-replace `v2` → `v3`. Fetch the migration guide or changelog (curl the docs, check GitHub releases). In the deerngo-bot session, the user wanted Fiber v3 — a quick check confirmed `fiber.Ctx` still works (backward compatible), so no core logic changes were needed. But if the API had breaking changes, the SAD's Go project structure, handler signatures, and middleware setup would all need rewriting. Always verify, then update.

- **⚠️ `patch` TOOL ON WINDOWS — BACKSLASH PATHS REQUIRED**: The `patch` tool's `path` parameter requires Windows backslash paths (`r"F:\projects\..."`) on Windows hosts. Forward slashes (`F:/projects/...`) work for `search_files`, `terminal`, and `read_file`, but `patch` silently fails to find the file with forward slashes. Use raw string literals to avoid escaping issues. If `patch` returns "Could not find a match" when you know the string exists, check the path format first.

- **⚠️ ARBITRARY PORT ASSIGNMENT**: Never assign ports like 8080, 3000, 5000 without checking the user's port registry first. Homelab users have strict port allocation schemes (e.g., 8000-9000 for backend, 3000-4000 for frontend, 7000-8000 for self-hosted). Assigning 8080 when 8008 is the next available breaks their naming convention and port map. Read the registry (commonly at `F:\obsidian_note\oralita_md\Quick Note\Home Lab App.md` or similar), pick the next available port in the correct range, and offer to register the new service in the registry after user confirms.

- **⚠️ SED REPLACEMENT MISSES TABLE-FORMATTED PORTS**: When bulk-replacing ports across design docs (e.g., `sed -i 's/:8080/:8008/g' *.md`), the pattern `:8080` only matches ports with a colon prefix. Ports in markdown tables often appear as bare numbers (e.g., `| 8080 | Go Backend |` in a port map table). After any sed-based port replacement, run `grep -rn "OLD_PORT" *.md` to catch remaining references in table cells, prose, and headers. Better yet, use the `patch` tool for targeted replacements — it handles context better and won't silently miss table-formatted values.

- **⚠️ CONSTRUCTION DOC NAMING: DOCTYPE ID, NOT RUNNING NUMBER**: When splitting 03_construction docs by repo type (BE/FE/SHARED), the doc number is the **doctype ID**, not a sequential counter. Both BE and FE variants share the same number. Wrong: `031_BE_README.md`, `032_FE_README.md`, `033_BE_build_scripts.md`. Right: `031_BE_README.md`, `031_FE_README.md`, `032_BE_build_scripts.md`, `032_FE_build_scripts.md`. The user will correct this immediately — it's a strong convention. Only `03_construction` gets the repo-type prefix. `01_requirement` and `02_design` stay unsplit (they're shared across repos).

- **⚠️ ASKING IS NOT VERIFYING — SSH and check before writing**: Grill questions extract *intent*, not *reality*. The user saying "PostgreSQL exists, Cloudflare Tunnel running, greenfield code" does NOT tell you WHERE the Go backend should run, WHICH machine has Docker, or HOW containers are networked. After the grill session, if the user provides SSH access or infrastructure docs, **USE THEM** before writing any document. Run `docker ps`, `docker network inspect`, check port bindings, verify which machine runs what. In one session, asking "where does the backend deploy?" got a vague answer — only `docker ps` on the homelab revealed Docker containers on `db-network`, `cloudflared` as systemd (not Docker), and the `deerngo` database already existing. **Rewriting 4 documents after the user corrected deployment topology is a 30-minute waste.** See `references/infrastructure-verification.md` for the exact commands.

- **⚠️ DEPLOYMENT TOPOLOGY IS THE #1 THING TO VERIFY PHYSICALLY**: Of all infrastructure facts, *which component runs on which machine* has the highest impact on design docs (affects ADRs, SAD deployment diagram, API base URLs, Docker Compose, network communication tables). If the PO's docs say "local Windows PC" but the user says "homelab server", don't pick one — SSH in and check. The topology affects 4+ documents and every rewrite cascades. In the deerngo-bot session, the PO meeting minute said "Local Windows deployment" but the actual setup was: Go + Next.js + PostgreSQL on homelab (Docker `db-network`), streamer.bot on Windows PC, Cloudflare Tunnel as systemd on homelab. This single correction required rewriting ADR-004, ADR-011, API Spec base URLs, SAD deployment diagram, and Architecture Overview.

### Phase 6: Multi-Persona Handoff Meeting Minutes

> After all design docs are produced, create a formal meeting minute (MM02) that hands off to Dev, UX/UI, and PO simultaneously. This is the designer's final deliverable.

1. **Produce `meeting_minute/MM02_designer-to-dev-uxpo_YYYYMMDD.md`** with these sections:
   - **What Designer Produced** — table of all design docs with status
   - **Design Decisions Resolved** — summary of grill-me outcomes
   - **Infrastructure Discovery** — actual deployment topology (from SSH verification)
   - **Design Changes That Affect Requirements** — any mid-design requirement changes, deployment corrections, or schema simplifications that the PO needs to review
   - **Handoff to Dev** — 🔴 implementation task list + which docs they receive
   - **Handoff to UX/UI** — 🟡 wireframe/style guide tasks + design constraints they must respect
   - **Handoff to PO** — 🟡 review tasks (confirm design decisions, confirm requirement changes)
   - **Action Items** — numbered checklist per persona with priorities and dependencies
   - **Sprint Plan** — confirmed sprint allocation
   - **Cross-references** — link to all related documents (requirements, design, previous MM)

2. **Include a "Requirements Reconciliation" table** in the PO handoff section — list every PO-owned file that was modified during design (e.g., AC-031 updated for 0-point exclusion). The PO needs to know what changed without diffing files.

3. **The meeting minute is the contract between personas.** Without it, Dev doesn't know what to implement, UX/UI doesn't know the constraints, and PO doesn't know their requirements were modified.

## Implementation Follow-Through

> After design docs are accepted, the implementation phase (code, tests, Dockerfile, build verification) follows. Load the appropriate implementation reference for the project's tech stack:

- **For Panomete platform services** (Spring Boot 4.1 / Java 25 / Spring Cloud 2025.1): Load `references/spring-boot-4.1-implementation.md` — Build config, TestRestTemplate gotcha, Eureka dual-port Docker pattern, test patterns, known cosmetic errors, Windows JAVA_HOME workaround, multi-stage Dockerfile template.
- **For other projects**: No platform-specific reference exists yet. If you complete an implementation for a new tech stack, save it as a reference file (e.g., `references/go-fiber-implementation.md`) for future sessions.

## Example Walkthroughs

See `references/` for complete session examples:
- **`references/panomete-example.md`** — Multi-service platform (Gate, Guard, Discover) with enterprise infrastructure (Nginx, Keycloak, Eureka, subdomain routing)
- **`references/deerngo-bot-example.md`** — Single-service project (Go + Fiber + sqlx) with simple infrastructure (local Windows, Cloudflare Tunnel, shared PostgreSQL)
- **`references/deerngo-bot-example-cont.md`** — Continuation: mid-design requirement changes, schema simplification, multi-persona handoff (MM02), 6 total corrections
