---
name: po-requirements-elicitation
description: Product Owner requirements workshop — grill stakeholders, populate BABOK/PMBOK templates, process design review feedback, resolve QA spec gap findings, create implementation plans, and manage GitHub backlog.
triggers:
  - User asks to /grill-me or /grill-me-docs to elicit requirements
  - User provides meeting minutes that require document revisions
  - User asks to set up foundational product documentation from templates
  - User asks to audit an Essential Documents or BOK-based template catalog
  - User wants to run a requirements workshop for a new project
  - User says requirements are complete and wants to hand off to designer
  - User asks to review a designer's meeting minute or design handoff
  - User provides a QA meeting minute with spec gaps (DEF-SXXX findings) needing PO decisions
  - User asks to review a QA spec gap report or defect report
  - User asks for an implementation plan or sprint plan with tasks and estimates
  - User asks to create GitHub issues, milestones, or labels for a repo
---

# PO Requirements Elicitation

## Overview

This skill governs the Product Owner workflow for eliciting requirements from a stakeholder (the user) and producing structured documentation using the BABOK/PMBOK-aligned templates at `F:\projects\project_spec\template\`. It also covers processing design review meeting minutes and applying architectural changes across affected documents.

## Five-Phase Workflow

### Phase 1: Requirements Elicitation (Grill Session)

1. **Load context.** Read the project README and any existing specs. Understand what already exists.
2. **Read the templates.** Load the target template files from the template directory so you know exactly what fields need to be populated.
3. **Grill one question at a time.** Use the `clarify` tool. Each question should:
   - Be directly traceable to a field in the template you are about to populate
   - Offer 3-4 specific choices (never open-ended unless the field genuinely has no reasonable options)
   - Build on previous answers — drill deeper, do not jump topics
4. **Write the document.** Once enough answers are gathered, produce the document immediately. Do not wait until all questions are asked — write incrementally.
5. **Repeat.** Move through the template documents in priority order: Business Objectives → User Stories → Acceptance Criteria → Stakeholder Analysis.

### Phase 2: Design Review Processing

When the user hands you meeting minutes (e.g., from a design persona review):

1. **Read the meeting minutes first.** Understand every decision and which documents are affected.
2. **Verify assumptions with clarifying questions.** Before editing, ask the user about anything ambiguous in the minutes. The minutes may be wrong or incomplete.
3. **Apply changes systematically.** Work document by document, starting with the highest-severity items (Critical). Use `patch` for targeted fixes, `write_file` for major rewrites.
4. **Update cross-document references.** When ports, domains, or architecture changes occur, every document that references them must be updated — not just the document flagged in the minutes.
5. **Present before/after summary.** Show what changed: new ports, removed stories, updated AC counts.
6. **Write a handoff meeting minute.** Create a new meeting minute in `spec/meeting-minute/` summarizing what the PO changed, so the next persona (designer/dev) knows the requirements are updated. Include: decisions applied, documents changed (with version bumps), key architecture rules, and handoff checklist.

### Phase 3: Phase Planning (from DevOps/Infra Proposals)

When the user hands you a DevOps/infra proposal (e.g., "Phase 2 planning" meeting minutes with initiatives and decision IDs):

1. **Read the proposal meeting minutes.** Understand every initiative, its priority, dependencies, and effort estimate. Note all "Decisions Needed from PO" items (usually tagged DEC-XXX).
2. **Review existing service docs.** Read the `05_devops/` and `03_construction/` folders of affected services to understand current state. Check for inconsistencies between what the proposal assumes and what the docs say (e.g., proposal assumes auto-deploy but docs show manual approval needed).
3. **Grill on decisions.** Use `clarify()` to resolve each DEC-XXX. Unlike requirements elicitation (which asks "what are we building?"), phase planning grilling asks:
   - **Scope** — which initiatives are in/out of this phase?
   - **Priority** — what order? What's must-have vs nice-to-have?
   - **Tooling choices** — notification channel? Deploy trigger (auto vs manual)? Retention policy?
   - **Sequencing rationale** — does the user agree with the proposed dependency order?
4. **Write the phase plan.** Produce a plan document in `plan/phaseN-<name>.md`. Include:
   - Phase objective (1-2 sentences)
   - Scope table (initiative, name, priority, depends on)
   - PO decisions table (DEC-XXX → choice → rationale)
   - Execution order with Mermaid flowchart dependency diagram
   - Sprint allocation (which initiatives in which sprint)
   - Initiative details (deliverables, ports/domains, configs)
   - Action items table (ID, action, owner, priority, depends on)
   - Definition of Done checklist
   - Transition criteria to next phase
5. **Flag doc inconsistencies.** If existing service docs contradict the approved decisions (e.g., CI/CD docs show auto-deploy but PO chose manual), create action items for the relevant persona to update them.
6. **Write construction overview if needed.** If the platform doesn't yet have a platform-level `03_construction/031_README_developer_guide.md`, create one. It should tie together per-service construction docs with: monorepo structure, dev workflow, build profiles, tech stack summary, shared resources, and coding standards. Use `treeView-beta` Mermaid for service inventories.

### Phase 4: QA Gap Review Processing

When QA hands you a meeting minute with spec gaps (DEF-S001 style findings):

1. **Read the QA meeting minute.** Understand each spec gap: what the AC says vs what the API Spec says, and where the contradiction is.
2. **Grill on each blocking decision.** Use `clarify()` for each DEF-SXXX that needs PO input. Offer clear options (A vs B) with the impact of each choice on the spec documents.
3. **Update the meeting minute decision table.** Fill in the PO Decision column with the chosen option, date, and notes. Update the status field from "Awaiting PO response" to "PO decisions complete".
4. **Apply decisions to spec documents.** For each decision:
   - DEF-SXXX → Which document changes → What specifically changes (AC rewritten, new ACs added, validation rule changed)
   - Update the AC summary table counts (🔴/🟡 split must match actual ACs)
   - Update the traceability table (every AC must have a TC entry)
   - Update the overview document counts
5. **Verify document consistency.** After all changes, run the consistency checklist (see below).
6. **Do NOT create a new meeting minute.** Update the existing QA meeting minute with PO decisions. The QA will update it further when they finalize test cases.

## Document Consistency Checklist

When making ANY change to spec documents, verify ALL of these:

| # | Check | Where to Look |
|---|-------|---------------|
| 1 | AC count in summary table matches actual ACs listed | `013_acceptance_criteria.md` §4 Summary |
| 2 | 🔴/🟡 split in summary matches actual priorities | `013_acceptance_criteria.md` §4 Summary |
| 3 | Every AC has a traceability entry (TC-XXX) | `013_acceptance_criteria.md` §5 Traceability |
| 4 | Test case numbers don't conflict (no duplicate TC-XXX) | `013_acceptance_criteria.md` §5 Traceability |
| 5 | Overview document counts match spec counts | `external_overview/<project>.md` or `overview/` |
| 6 | User story AC count matches actual ACs in AC doc | Compare `012_user_stories.md` ACs vs `013_acceptance_criteria.md` |
| 7 | Meeting minute status reflects actual state | `07_pm/MM*.md` status field |
| 8 | Coverage report (045) has correct AC counts | `04_testing/045_coverage_report.md` — AC counts by user story and total |
| 9 | Coverage report has correct 🔴/🟡 split per user story | `04_testing/045_coverage_report.md` — US-001 row especially |

**Common failure pattern:** Adding a new AC (e.g., AC-031c) but forgetting to update the summary table count, traceability entry, and overview document. Always update ALL four locations atomically.

## Meeting Minute Decision Updates

When PO makes decisions on a QA or designer meeting minute:

1. **Update in-place** — do NOT create a new meeting minute. Edit the existing file.
2. **Fill the decision table** — PO Decision column, Date column, Notes column.
3. **Update the status field** — from "Awaiting PO response" to "PO decisions complete" (or similar).
4. **Update action items** — mark PO actions as done, unblock dependent QA/Dev actions.

## Document Structure Convention

**Umbrella + Service-Level Pattern (user preference):**

```
spec/
├── <platform>/              ← UMBRELLA: cross-cutting concerns only
│   ├── README.md            ← Architecture overview, service map
│   └── 01_requirement/
│       ├── 011_business_objective.md  ← Platform-level objectives
│       ├── 012_user_stories.md        ← Thin consolidation + links
│       └── 014_stakeholder_analysis.md
│
├── <service-a>/             ← DEEP DIVE: self-contained
│   └── 01_requirement/
│       ├── 011_business_objective.md  ← Service-specific
│       ├── 012_user_stories.md
│       └── 013_acceptance_criteria.md
│
├── <service-b>/
│   └── 01_requirement/
│       ...
```

**Rules:**
- Each service folder is self-contained — a developer picking it up needs zero external context
- The platform umbrella links to service docs, never duplicates them
- Business objectives at the platform level trace to strategy; service-level ones trace to platform objectives
- User stories use the standard template format: As a…I want…so that… with ACs, story points, priority, and objective mapping

## Mermaid Diagram Conventions

**For architecture diagrams:** `flowchart TB` with `subgraph` for logical layers. Solid arrows for data flow, dashed for cross-cutting concerns, dotted for registrations. Color-code: red=gateway, blue=auth, green=discovery, dark=business services. Use brand colors for infra layers (Cloudflare orange, Nginx green).

**For project structures:** `treeView-beta` (NOT `mindmap`). Use unicode tree characters (`├──`, `└──`, `│`) with `→` annotations for metadata (story points, AC counts, status, ports, domains). Never use `mindmap` — the user explicitly corrected this.

**For phase plan dependency diagrams:** `flowchart LR` with color-coded initiative nodes (red=must, orange=should, green=nice). Use solid arrows for hard dependencies, dotted (`.->`) for independent/soft dependencies.

**For service inventories in construction docs:** `treeView-beta` showing each service with its `03_construction/` file list and completion status (✅/⬜).

## External Projects Convention

When the user asks to spec a project that is **not part of the Panomete platform** (standalone tools, bots, external services):

- **Spec location:** `F:\projects\project_spec\external_spec\<project-name>\` — NOT under `spec/`
- **Same templates:** Use the same `F:\projects\project_spec\template\` templates as Panomete projects
- **Same document structure:** `01_requirement/`, `02_design/`, etc. inside the project folder
- **Independence:** External project specs are fully self-contained — they do NOT link to or reference Panomete umbrella docs
- **Meeting minutes:** `F:\projects\project_spec\external_spec\<project-name>\07_pm\` — INSIDE the project folder, NOT in a separate meeting_minute folder
- **Overview docs:** If an overview is needed, place it in `F:\projects\project_spec\external_overview\`
- **Implementation plans:** `F:\projects\project_spec\external_plan\` — NOT under `plan/`

## Parallel Research for Unfamiliar Tech

When the stakeholder mentions tools, APIs, or platforms you're unfamiliar with (e.g., streamer.bot, EasyDonate, a third-party API):

1. **Delegate research in the background** using `delegate_task` as soon as the tech is identified — do NOT wait until the grill session ends
2. **Continue the grill session** in parallel — the research and the questions are independent workstreams
3. **Integrate findings** when the research returns — use them to inform follow-up questions and validate assumptions in the spec documents
4. **What to research:** Overview/capabilities, API/webhook support, integration patterns, rate limits, authentication, and how the tech connects to the user's architecture

This saves a full round-trip and ensures the spec is grounded in real technical constraints, not assumptions.

## Question Strategy

- Start with the biggest, most consequential question: **Why are we building this?** Everything flows from purpose.
- Then scope: **Who uses it? When does it need to be done? What is the MVP?**
- Then technical constraints: **Language? Deployment? Existing infrastructure?**
- **Availability check:** For any feature that depends on a runtime component (desktop app, browser extension, external process), ask: "What happens when this component is offline?" If data/events will be missed, propose the hybrid pattern (see `references/hybrid-data-collection-pattern.md`).
- Each answer informs the next question. Never ask random or unrelated questions.
- If the user says "what do you think" — give your honest assessment with pros/cons, then let them decide.

### Phase 5: Implementation Plan Creation

When requirements, design, and QA are complete and the user asks for an implementation plan:

1. **Read all spec documents.** Understand the full scope: user stories, ACs, API spec, DB schema, architecture decisions.
2. **Ask about repos.** Use `clarify()` to confirm: How many repos? What goes in each? What are the names?
3. **Define branch strategy.** Propose a Gitflow-style approach:
   - `main` — production-ready
   - `develop` — integration branch
   - `feat/sprint-{N}-{description}` — feature branches per sprint
4. **Break down sprints into tasks.** Each user story → concrete implementation tasks with estimates, owner, and dependencies.
5. **Include DevOps tasks.** Docker Compose, tunnel config, database setup, monitoring.
6. **Write the plan.** Produce in `external_plan/` (external projects) or `plan/` (platform projects). Include:
   - Phase objective
   - Scope table (epics, stories, points, priority)
   - Sprint breakdown (tasks, owners, estimates, dependencies)
   - Repository & branch strategy (repos, branch naming, PR workflow, commit convention)
   - DevOps tasks
   - Dependency diagram (Mermaid flowchart)
   - Risk register
   - Definition of Done checklist
   - Transition criteria to next phase
7. **Offer GitHub issues/milestones.** When repos are ready, offer to create:
   - Milestones (one per sprint)
   - Issues (one per user story, with labels, story points, ACs in body)
   - Labels (epic, priority 🔴🟡🟢, sprint)

### Plan Revision After a Scope Pivot

When an approved requirements change replaces a feature or changes the product model, revise the existing phase plan in place unless the work is genuinely a new phase. Do not leave the old plan as the apparent source of truth and do not create a duplicate plan merely because the scope changed.

1. Read the current requirements, acceptance criteria, API/DDL/architecture contracts, QA baseline, risk register, existing phase plan, and current GitHub backlog before editing.
2. Recompute story count, story points, active AC count, priority split, and test-case coverage from the source documents; do not hand-copy stale totals.
3. Update the plan's scope table, out-of-scope list, decision table, dependency flow, sprint tasks, repositories, branch strategy, DevOps tasks, release gates, Definition of Done, transition criteria, and document references together.
4. Label historical work explicitly as superseded/retained for evidence. Do not leave old endpoints, tables, providers, schedulers, or matching algorithms described as active implementation requirements.
5. Add a plan index/README when the external plan directory lacks one. The index should identify the active plan, baseline totals, and superseded planning assumptions.
6. Link release gates to actual issue URLs and identify which gates block production. A specification can be complete while implementation, provider verification, privacy approval, and real test execution remain pending.
7. Re-read the rewritten plan and run a scripted consistency check before reporting completion: version/date, active totals, endpoint names, current dependencies, release gates, DoD, and Phase 2 transition criteria.

## GitHub Issues & Milestones (PO Backlog Management)

When the user has a GitHub repo ready and wants to create issues:

1. **Confirm repo URL.** Ask for `owner/repo` or full URL.
2. **Create milestones first.** One per sprint: "Sprint 1 — Foundation + Subscribers", "Sprint 2 — Points Engine", "Sprint 3 — Scoreboard".
3. **Create labels.** Epic labels (e-01-register, e-02-bot, etc.), priority labels (🔴 must-have, 🟡 should-have, 🟢 could-have), sprint labels (sprint-1, sprint-2, sprint-3).
4. **Create issues.** One per user story. Each issue body includes:
   - Story format: "As a…I want…so that…"
   - Acceptance criteria (from 013)
   - Story points
   - Link to business objective
   - Sprint assignment
5. **Use `gh` CLI.** `gh issue create`, `gh label create`, `gh milestone create`.

## Multi-Repository Backlog Creation

When approved user stories are ready to be created as GitHub issues across multiple repositories, use an explicit ownership map before touching GitHub:

### Rich Markdown and Partial-Batch Safety

For issue bodies containing multiline Markdown, emoji, backticks, Unicode, tables, or shell-sensitive characters, write the body to a temporary file and use `gh issue edit/create --body-file`; do not rely on inline `--body` quoting. Execute metadata updates in small batches, inspect exit codes individually, and re-read every affected issue afterward because a batch can partially succeed. Correct failed issues before reporting completion. Preserve stable story IDs and verify title, body, labels, milestone, state, and cross-repository dependency URLs remotely.

1. **Inspect first.** Read the requirements, acceptance criteria, phase plan, and each repository README. Query each repo's existing issues, labels, milestones, default branch, and root layout. Do not assume the repositories are empty or that the local plan still matches the scaffold.
2. **Map stories to repositories.** Put backend/API/database/scheduler/streamer.bot integration stories in the backend repo; put public UI/page stories in the frontend repo. A story belongs in one repo only. For cross-repo work, create the provider/API issue first and add its actual URL to the consumer issue.
3. **Scope milestones to ownership.** Create sprint milestones only in repositories that contain work for that sprint. It is valid for the frontend repo to have only Sprint 3 while the backend repo has Sprints 1–3.
4. **Create metadata idempotently.** Preserve GitHub's default labels. Create only missing custom labels for story type, epic, priority, sprint, repository area, and integrations. On rerun, detect existing milestones/issues by exact stable story ID in the title instead of creating duplicates.
5. **Make issue bodies implementation-ready.** Each story issue includes the `As a / I want / So that` statement, story ID, objective, epic, priority, points, sprint, every AC as a checkbox, implementation notes, source-document paths, and cross-repo dependency links where applicable. Keep DevOps/security tasks separate unless they are explicitly approved as user stories.
6. **Verify remote side effects.** Read GitHub back after creation and verify issue count, story-ID mapping, labels, milestone assignment, cross-repository URLs, and duplicate absence. Report issue URLs/numbers and milestone totals, not only a success claim.

The reusable checklist and Deerngo repo-split example are in `references/requirements-to-github-backlog.md`.

## Third-Party Integration Credential Verification

When a project depends on a vendor API, OAuth account, or webhook, separate the integration into four distinct contracts before asking the stakeholder for credentials:

1. **Backend → provider API credential** — usually an API key or OAuth access/refresh token used for polling or outbound API calls.
2. **OAuth client identity** — client ID/secret identifies the application; a client ID alone is never an authorization link.
3. **Provider → backend webhook** — a public callback URL configured in the provider dashboard.
4. **Webhook authenticity credential** — HMAC/signing secret or signature header, but only if the current provider documentation/dashboard explicitly confirms it.

### Required verification sequence

1. Read the provider's current official documentation and inspect the provider dashboard. Confirm the exact auth header, scope names, endpoint, payload field names, signature scheme, retry behavior, and rate limit.
2. Do not turn an assumed payload or HMAC header into an API specification. Mark it as an open integration decision until verified against a real provider sample or official contract.
3. For OAuth, generate a complete authorization URL containing the registered redirect URI, requested scope, random `state`, `access_type=offline`, and (when a new refresh token is required) `prompt=consent`. Sending an OAuth client ID by itself cannot authorize a user.
4. If using a Desktop OAuth client with a localhost callback, remember that `localhost` belongs to the machine where the stakeholder opens the URL. A remote client will not redirect back to the developer's computer. Use a running helper on the same machine, a controlled remote session, or a reachable HTTPS callback owned by the application.
5. Treat the resource owner and the developer/operator as different actors. The owner must authorize their own channel/account; the developer's backend may consume the resulting token only with explicit consent. Never request refresh tokens, API keys, client secrets, or webhook secrets through ordinary chat or GitHub issues.
6. Separate non-secret identifiers from secrets in client-facing notes. Channel IDs and provider/page IDs are normally non-secret; refresh tokens, API keys, client secrets, and signing secrets are sensitive.
7. Do not promise complete event capture when a provider limits results or hides private data. Document visibility limits, pagination/recent-item limits, polling freshness, and the fallback path.
8. When vendor research changes the assumed contract, update the affected API spec, acceptance criteria, security assessment, implementation issue, and client setup note before implementation proceeds.

### Deerngo integration facts to preserve

- YouTube subscriber polling requires the Deer_NGO channel owner's OAuth consent; a normal API key is not sufficient, and YouTube Data API does not support service-account access for this scenario.
- Use the authorized recent-subscriber operation and verify the provider's current parameters. The API may limit recent-subscriber results and private subscriptions may not be visible, so describe the design as best-available 24/7 capture rather than an unconditional 100% guarantee.
- EasyDonate's current developer documentation distinguishes a personal API key (used as a Bearer token for the account API, with the donation-read scope) from a webhook URL. Do not assume that an `EASYDONATE_WEBHOOK_SECRET`, `X-EasyDonate-Signature`, or a particular JSON field naming scheme exists until the provider confirms it.

## Member-Led VRM Changes and Privacy-Safe Identity

When a provider's API exposes only a partial, capped, or privacy-filtered audience list, do not force that external list to be the product's membership source. Reframe the domain explicitly:

1. **Observation/source data** — what YouTube or another provider exposes; incomplete, provider-controlled, and not necessarily consented for public display.
2. **Explicit members** — viewers who intentionally opt into the product through a trusted event, such as a chat command whose author identity comes from streamer.bot.
3. **Transactions** — donations/payment events, retained separately from identity and membership.
4. **Benefits/points** — calculated only from explicit membership and approved eligibility rules.

For a member-registration change request, grill one decision at a time in this order: trusted identity source, registration availability, starting balance/cutover, donor-to-member matching rule, public display identity, retention/opt-out, and whether old source data is retained for audit. Do not let a viewer type an arbitrary handle to self-claim another account; prefer the platform identity supplied in the event metadata.

Default safe MVP pattern for Deerngo-style VRM:

- `:deer: register` uses the actual chat author's YouTube identity from streamer.bot; ignore a handle typed in the message.
- A new member starts at zero points.
- A donation earns points only when `donation_time >= member.registered_at`.
- Normalize both values by trimming whitespace, removing a leading `@`, and lowercasing; use normalized exact matching rather than fuzzy matching for point attribution.
- Do not automatically credit historical donations unless the stakeholder explicitly approves a controlled backfill.
- A public scoreboard should not expose raw provider display names by default; use a normalized handle or an explicit public nickname/consent flow.
- Treat handles, display names, and donor names as potentially personal data. Apply minimization, purpose limitation, explicit participation/visibility rules, an opt-out/removal process, and a privacy notice; do not present this as legal advice.

When this change is approved, update the existing requirements, acceptance criteria, API/DDL/ERD, implementation plan, QA cases, risk/security documents, overview, and GitHub issues/milestones. Do not create a new parallel spec just because a meeting minute raised the change; first finish the grill and record the decision in the existing meeting-minute workflow.

## Support Files

- **`references/panomete-infra.md`** — Infrastructure snapshot (ports, domains, tech stack, deployment status, design decisions). Update when infra changes.
- **`references/hybrid-data-collection-pattern.md`** — Pattern for capturing events from sources that aren't always available (primary polling + secondary real-time push). Includes design checklist, AC template, and the Deerngo Bot example.
- **`references/deerngo-bot-case-study.md`** — Full case study of the Deerngo Bot external project workflow: requirements → design → QA → implementation plan. Shows the complete 5-phase workflow in action with real decisions, document counts, and lessons learned.
- **`references/third-party-integrations.md`** — Credential taxonomy, OAuth callback troubleshooting, YouTube authorization constraints, EasyDonate API/webhook verification notes, and the official source URLs used for Deerngo.
- **`templates/phase-plan.md`** — Scaffold for sprint-based implementation plans with repo/branch strategy, task breakdown, and DevOps tasks. Copy and fill when creating a plan for Dev after design and QA are complete.
- **`templates/designer-handoff-meeting-minute.md`** — Scaffold for PO → Designer handoff meeting minutes. Copy and fill when requirements are complete and design phase begins.
- **`references/youtube-oauth-client-setup.md`** — Client-friendly OAuth setup checklist, secret-handling rules, YouTube subscriber-feed caveats, and official references for always-on YouTube integrations.
- **`references/provider-limited-membership-pivot.md`** — Evidence-first workflow for replacing incomplete provider audience capture with explicit member registration, cutover-based points, handle-change handling, privacy safeguards, and vendor-contract verification.


## Auditing Essential-Document Catalogs

When auditing a document-template or Essential Documents library against multiple BOKs and a completed knowledge vault, treat the task as a **catalog-and-tailoring audit**, not as a hunt for more filenames.

1. **Inventory before judging.** Read every file in the target folder, count source rows/profile rows, inspect headings, and verify both internal wikilinks and literal source paths. Use the actual local vault path as the source of truth; do not trust stale paths written in old banners.
2. **Build a cross-source map.** Compare the catalog with the BOK overview/chapter outputs and the user's completed notes. Track each candidate as one of: artifact, plan, baseline, register/log, report, review/approval record, model/diagram, generated/tool output, technique, or organizational/regulatory evidence.
3. **Separate omission from classification.** For every apparent gap ask: Is this genuinely absent, represented under an alias, a section of another artifact, a generated output, or only conditionally applicable? Do not recommend adding every BOK output as a standalone file.
4. **Audit applicability semantics.** A priority flag is insufficient. Each row should distinguish universal minimum, conditional trigger, profile preset, evidence/record, technique/model, and optional enhancement. Organization-level artifacts such as ISMS, SoA, QMS, SIEM rules, enterprise data models, MBSE models, FCA/PCA, and safety cases must not silently become universal software-project requirements.
5. **Check the control loop, not only delivery artifacts.** Confirm explicit coverage for: vision/scope/success criteria; project tailoring/documentation strategy; lifecycle/process definition; requirements/design baselines and approvals; estimation basis; measurement/metrics; risk and performance control; verification/validation/acceptance; quality gates; operational readiness/post-deployment validation; maintenance; retirement/decommissioning.
6. **Normalize shared artifacts across BOKs.** RTM, risk register, change request/log, design/review record, data dictionary, release notes/VDD, SRS/SyRS, and lessons learned often appear in multiple disciplines. Define one canonical source of truth plus linked discipline views rather than duplicating independent documents.
7. **Recompute profile numbers.** Quick-start counts and priority checklists must be derived from the profile's actual rows. Also test the profile dimensions independently: team size, lifecycle, criticality, regulatory/contractual exposure, data sensitivity, operational exposure, distribution, and product maturity.
8. **Produce a read-only audit first.** Save a dated audit report with verdict, evidence, prioritized findings, recommended artifact families, reclassification guidance, rewrite order, and a future quality gate. Do not rewrite the template in the audit session unless explicitly requested.

The reusable audit method and evidence notes are in `references/essential-document-catalog-audit.md`.

## Pitfalls

- **Monolithic specs.** Do not put all stories in the platform-level document. Split into service-level docs and make the platform doc an umbrella.
- **ASCII art diagrams.** User prefers Mermaid everywhere. `treeView-beta` for trees, `flowchart` for architecture. Never `mindmap` for file trees.
- **Assuming architecture.** Always ask about existing infrastructure before documenting deployment. The user may already have Nginx, databases, tunnels running.
- **Waiting too long to write.** Write documents as soon as you have enough for a section. Do not accumulate all answers before producing output.
- **Missing cross-document updates.** When a design review changes ports/domains, check ALL documents — not just the ones flagged in the minutes.
- **Missing handoff meeting minutes.** After applying design review changes OR writing a phase plan, always produce a meeting minute in `spec/meeting-minute/` so the next persona knows what changed. This is the contract between personas.
- **Blindly trusting proposal docs.** When processing a DevOps/infra proposal, cross-check the proposed approach against existing service docs (especially `05_devops/051_CICD_pipeline_configuration.md`). The proposal may assume auto-deploy while existing docs show a different model. Flag inconsistencies as action items.
- **Forgetting the plan/ directory.** Phase plans go in `F:\projects\project_spec\plan\`, NOT in `spec/`. The `plan/` directory is for milestone/phase-level planning documents that span multiple services.
- **Phase plan without Definition of Done.** Every phase plan MUST have a checklist-based DoD and transition criteria to the next phase. Without these, "done" is ambiguous.
- **Availability gap in data capture.** When a feature depends on a runtime component that isn't always running (desktop app, browser extension, mobile app, streamer.bot, OBS plugin), ALWAYS ask: "What happens when this component is offline? Are there subscribers/events/data points that will be missed?" If the answer is yes, propose a hybrid approach: primary source (always-on polling/webhook) + secondary source (real-time push when component is active). Upsert logic handles duplicates. Example: YouTube subscriber capture — streamer.bot only runs during live streams, so YouTube Data API polling (every 15 min) is the primary source for 24/7 coverage.
- **Hybrid data collection without explicit trade-offs.** When proposing a hybrid approach (e.g., API polling + real-time push), always document the trade-offs in the spec: polling interval vs freshness, API quota costs, deduplication/upsert logic, and what happens when both sources fire for the same event. Do not leave these implicit.
- **Designer handoff AC inconsistency.** When reviewing designer meeting minutes that claim ACs were updated, ALWAYS verify: (1) the AC summary table count matches the actual number of ACs listed, (2) the traceability table has an entry for every AC, (3) test case (TC-XXX) numbering doesn't conflict with existing entries. Designers frequently add new ACs but forget to update the summary counts or traceability entries. Fix immediately — do not assume the designer checked.
- **Multi-persona handoff meeting minutes.** When a designer hands off to multiple personas simultaneously (e.g., Dev + UX/UI + PO), the meeting minute should have SEPARATE sections for each persona with: what they receive, what they need to produce, and their specific action items. Do not merge all personas into one section.
- **QA gap review without document consistency.** When PO makes decisions on QA spec gaps, the meeting minute is NOT the only thing to update. Each decision ripples into: AC document (rewrite/add ACs), summary table (counts), traceability (TC entries), overview document (counts), AND coverage report (045). The coverage report has per-user-story AC counts that break when ACs change priority (🟡→🔴). Use the expanded Document Consistency Checklist (9 items). Failing to update all locations is the #1 source of downstream confusion.
- **Meeting minutes in wrong location.** Meeting minutes for external projects go INSIDE the project folder at `external_spec/<project>/07_pm/`, NOT in a separate `external_spec/meeting_minute/` folder. Each project owns its own meeting minutes. This keeps the project self-contained.
- **Creating new meeting minutes for PO decisions.** When QA hands you a meeting minute with pending decisions, UPDATE THE EXISTING FILE. Do not create a new meeting minute. The QA meeting minute is the living document — PO fills in the decision table, QA updates test cases later. Creating duplicates fragments the record.
- **Deployment topology changes from designer.** When the designer's meeting minute changes the deployment topology (e.g., "Go backend on homelab Docker, not local Windows PC"), this is a MAJOR change that affects: (1) the overview document architecture diagram, (2) the business objectives (deployment section), (3) any ACs that reference localhost vs LAN calls. Always ask the stakeholder to CONFIRM the topology change before updating specs. Do not assume the designer got it right — the stakeholder may have changed their mind without telling you, or the designer may have misunderstood.
- **Forgetting to update the overview document.** After ANY significant spec change (new stories, topology change, AC rewrites, count changes), update the overview document (`external_overview/<project>.md` or `overview/`). The overview is the single-page summary stakeholders read — if it's stale, they lose trust in the docs. Update: counts, architecture diagram, integration table, sprint plan.
- **Implementation plans without repo/branch strategy.** When creating an implementation plan for Dev, ALWAYS include: (1) repository names and what goes in each, (2) branch strategy (main/develop/feature branches), (3) branch naming convention, (4) PR workflow (squash merge to develop), (5) commit message convention. Devs need this before they start — asking later wastes a sprint.
- **Assuming repo count.** When the user mentions repos, ALWAYS use `clarify()` to confirm the exact count and names before writing the implementation plan. Users may say "3 repos" then correct to "2 repos" — writing first wastes effort.
