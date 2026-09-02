---
name: devops-doc-authoring
description: >
  Produce DevOps document suites (CI/CD, deployment plan, release notes, runbook)
  from project specs and templates. Reads upstream docs (architecture, API spec,
  build scripts, dependency manifests, test plan) to extract deployment-relevant
  details, then tailors templates to the project's actual infrastructure.
trigger: >
  User asks to create/fill DevOps docs (05_devops folder), deployment documentation,
  CI/CD config, runbook, or release notes for a project that already has spec docs
  (01–04 phases). Also triggers when user says "fill the devops template" or
  "create the operations docs."
---

# DevOps Document Authoring

Produce a complete `05_devops/` document suite by reading upstream project specs
and tailoring standard templates to the project's actual architecture.

## When to Use

- User has a project with existing spec docs (01_requirement, 02_design, 03_construction, 04_testing)
- User wants the DevOps phase documents created
- User asks to audit, assess, or improve an existing release/deployment checklist or DevOps document
- User asks whether a release checklist is ready for production, enterprise, or full-scale use
- Templates exist at a known template path

## Prerequisites

Before writing any document, read ALL of these upstream sources:

| Source Folder | Key Files to Read | What to Extract |
|--------------|-------------------|-----------------|
| `01_requirement/` | `011_business_objective.md` | Project name, ID, tech stack, stakeholders, KPIs |
| `02_design/` | `025_software_architecture_document.md` | Architecture style, deployment topology, ports, network, security model |
| `02_design/` | `029_architecture_overview.md` | Component map, port map, tech stack summary |
| `02_design/` | `022_API_specification.md` | Endpoints, rate limits, auth, CORS |
| `02_design/` | `023_database_schema_DDL.md` | Tables, extensions, triggers, migrations |
| `03_construction/` | `031_BE_README.md` + `031_FE_README.md` | Build commands, Docker setup, project structure |
| `03_construction/` | `032_BE_build_scripts.md` + `032_FE_build_scripts.md` | Makefile targets, Dockerfile stages, npm scripts |
| `03_construction/` | `033_BE_dependency_manifest.md` + `033_FE_dependency_manifest.md` | Key dependencies, versions, licenses |
| `03_construction/` | `034_SHARED_commit_messages_changelog.md` | Commit convention, scopes, changelog format |
| `04_testing/` | `041_test_plan.md` | Test levels, tools, environments, entry/exit criteria |

## Workflow

### Existing DevOps / Release Checklist Audit

When auditing an existing release or deployment checklist, distinguish two questions:

1. **Lifecycle coverage:** Does it cover versioning, build, promotion, migration, rollout, verification, rollback, communication, and review?
2. **Release-gate maturity:** Does it require evidence, artifact identity, approvals, risk decisions, health thresholds, recovery choices, and an auditable closeout?

Do not label a checklist merely as a “low-risk checklist” because it lacks mature gate mechanics. State clearly whether it is a strong full-lifecycle baseline, a sufficient standalone production gate, or suitable for regulated/mission-critical use. If it already covers the lifecycle, recommend improving the canonical checklist with risk overlays and evidence rather than creating a separate low-risk checklist.

Audit workflow:

1. Read the target checklist and all linked/domain checklists.
2. Inspect internal links and sibling notes for naming and ownership consistency.
3. Audit artifact identity: release/version, commit SHA, build ID, artifact digest, SBOM, signature, provenance, and build-once/promote-same-artifact.
4. Audit operational controls: deployment strategy, exposure strategy, health model, promotion/abort criteria, observation window, rollback/forward-fix, and handoff.
5. Audit stateful changes: schema compatibility, migration locking/backfill, data validation, and explicit restore/forward-fix decisions.
6. Audit risk scoping: do not let user count or “POC/internal” labels override internet exposure, sensitive data, production credentials, business criticality, RTO/RPO, regulation, or blast radius.
7. Check for platform assumptions in documents claiming to be framework-agnostic; move commands into platform-specific runbooks.
8. Use current authoritative sources when the user asks for a full-scale or best-practice assessment; prefer Google SRE, DORA, SLSA, NIST SSDF, and platform safe-deployment guidance.
9. Report findings with line references and severity. Do not modify the user’s file during an audit unless explicitly asked.

For the reusable audit checklist and research notes, see `references/release-checklist-audit.md`.

### Microservice Checklist Suite Audit

When auditing a microservice checklist folder, exclude implementation-specific overlays (for example, `spring-boot/`) unless the user explicitly includes them. Treat the root notes as a coordinated suite rather than seven unrelated documents.

Audit workflow:

1. Inventory every root note, line count, checklist count, and excluded subfolder; report the exact scope.
2. Read every in-scope note before judging completeness. Inspect all Obsidian wikilinks and relative Markdown links against the actual vault paths; broken links are release-safety defects because they hide the detailed control.
3. Establish canonical ownership: the system/infrastructure checklist should own architecture-level decisions, while gateway, authentication, load balancing, data/messaging, observability, and resilience notes own their detailed gates. Flag duplicated rules that can drift.
4. Reconcile cross-note trust boundaries and guarantees, especially gateway JWT validation versus service-level authorization, JWKS discovery, health-check semantics, retry ownership, fallback safety, and delivery guarantees.
5. Separate platform-neutral outcomes from platform overlays. Docker Compose, Kubernetes, VM/systemd, service mesh, and managed-cloud controls must be conditional or linked overlays, not universal requirements in a framework-agnostic checklist.
6. Replace absolute rules and arbitrary defaults with a decision field: selected option, rationale, evidence, owner, N/A reason, exception approver, and review/expiry date. Examples such as timeout values, replica counts, service-count thresholds, SLOs, and resource sizes are starting points, not universal policy.
7. Audit security claims against current authoritative guidance: issuer metadata and `jwks_uri`, algorithm allowlists, PKCE, token lifecycle/revocation, password policy, trusted proxy headers, and defense-in-depth authorization.
8. Audit messaging claims for delivery semantics, idempotency, outbox/replay behavior, saga compensation, broker HA/security/retention, and the distinction between at-least-once, effectively-once, and true exactly-once boundaries.
9. Audit observability for metric cardinality, correlation-context availability, telemetry privacy/retention, alert ownership, and collector failure—not only the presence of logs, metrics, and traces.
10. Audit resilience for retry amplification, deadline propagation, circuit-breaker applicability, safe versus unsafe fallbacks, backpressure, load shedding, and measurable failure scenarios.
11. Produce a folder-level verdict plus file-level P1/P2/P3 findings, with line references, concrete corrections, cross-file contradictions, missing controls, and a clear statement that no files were modified unless explicitly requested.
12. If editing is explicitly approved, apply coordinated changes only to in-scope root notes, then verify frontmatter/version, zero unresolved links, no stale relative Markdown links, no leftover contradictory patterns, and unchanged hashes/sizes for excluded folders.

For the reusable microservice-suite audit matrix and research anchors, see `references/microservice-checklist-audit.md`.

### Step 1: Context Gathering (Read-Heavy)

Read ALL upstream documents listed above. Do NOT write any DevOps doc until you've
read the full project context. This is the most important step — skipping it
produces generic, templated docs instead of tailored ones.

### Step 2: Extract Deployment-Relevant Facts

From the upstream docs, build a mental model of:

- **Components** — what runs where (containers, ports, networks)
- **Build toolchain** — Go/Node/etc., Makefile/npm, Dockerfile stages
- **Infrastructure** — Docker/K8s/serverless, managed services, shared networks
- **External integrations** — APIs, webhooks, OAuth tokens, third-party services
- **Security model** — auth mechanisms, secrets management, TLS
- **Database** — version, extensions, migration tool, backup strategy
- **Public access** — tunnels, load balancers, CDN, DNS

### Step 3: Read Templates

Read all template files from the template directory (e.g., `template/05_devops/`).
Understand the template structure, section order, and placeholder format.

### Step 4: Author Each Document

Produce all 4 DevOps documents, tailoring every section to the project's reality:

| # | Document | Template | Key Tailoring Points |
|---|----------|----------|---------------------|
| 051 | CI/CD Pipeline Configuration | `051_CICD_pipeline_configuration.md` | Workflow YAML matching actual build toolchain, correct service containers for tests, proper image registry, deploy steps matching actual infrastructure |
| 052 | Deployment Plan | `052_deployment_plan.md` | Actual deploy commands for the target infra, first-time bootstrap guide, rollback procedure using image tags, database migration strategy |
| 053 | Release Notes | `053_release_notes.md` | Planned features from user stories, conventional commit → section mapping matching the project's commit convention, release history table |
| 054 | Operations Manual / Runbook | `054_operations_manual_runbook.md` | Actual container names, ports, log commands, troubleshooting tables for the project's specific failure modes, database queries, quick reference card |

### Step 5: Verify

After writing, verify the folder structure:
```
05_devops/
├── 051_CICD_pipeline_configuration.md
├── 052_deployment_plan.md
├── 053_release_notes.md
└── 054_operations_manual_runbook.md
```

## Critical Rules

1. **Never generic.** Every command, port, container name, and URL must match the
   project's actual architecture. If the project uses Docker Compose on a homelab,
   don't write Kubernetes commands.

2. **Read before write.** The upstream docs (01–04) are the source of truth. If a
   detail isn't in the upstream docs, note it as TBD — don't invent it.

3. **Frontmatter must match convention.** Use the same YAML frontmatter structure
   as all other project docs (document_type, version, status, author, created,
   last_updated, project_name, project_id, classification, tags, standard_ref,
   parent_project).

4. **Cross-reference.** Every DevOps doc should link to relevant upstream docs
   and to sibling DevOps docs via `[[document_name]]` syntax.

5. **Pragmatic over aspirational.** For small projects (1 dev, homelab), don't
   write Kubernetes manifests or multi-environment promotion pipelines. Match
   the scale.

6. **Infrastructure = code.** Include actual Docker Compose, Nginx config,
   GitHub Actions YAML — not pseudocode or placeholders.

7. **Rollback always.** Every deployment doc must include a rollback procedure.
   Every CI/CD doc must preserve previous image tags.

## Pitfalls

| Pitfall | Why It Happens | Prevention |
|---------|---------------|------------|
| Generic CI/CD YAML that doesn't match build toolchain | Didn't read `032_build_scripts.md` | Always read build scripts first |
| Wrong ports or container names | Assumed defaults instead of reading architecture doc | Extract from `029_architecture_overview.md` port map |
| Missing `db-network` or shared infrastructure | Didn't check existing homelab setup | Read architecture deployment section carefully |
| Kubernetes commands for Docker Compose project | Template assumed K8s | Read architecture, then tailor — never blindly copy template |
| Secrets in committed YAML | Copied from template without redacting | Use `${{ secrets.* }}` in CI, `${VAR}` in Compose |
| No healthcheck in Docker Compose | Omitted for brevity | Always include healthcheck — it gates deploy verification |
| Runbook troubleshooting too generic | Didn't think about project-specific failure modes | Read API spec + architecture to identify actual failure scenarios |

## Output Convention

All documents go in `05_devops/` folder at the same level as the project's
other spec folders (01_requirement, 02_design, etc.). File naming follows
the `05N_document_name.md` pattern from the template directory.

## Support Files

- `references/homelab-ghcr-cicd-pattern.md` — Reusable CI/CD YAML patterns for
  homelab + GHCR + Docker Compose deployments (GitHub Actions workflow, Compose
  production file, Nginx proxy, rollback commands)
- `references/devops-doc-suite-structure.md` — What each of the 4 DevOps documents
  must include, who reads it, and how they cross-reference each other
