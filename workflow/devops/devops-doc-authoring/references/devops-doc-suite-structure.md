# 05_devops Document Suite — Structure Reference

The DevOps phase produces 4 documents. Each has a distinct audience and purpose.

## Document Map

```
05_devops/
├── 051_CICD_pipeline_configuration.md   ← Developer + DevOps
├── 052_deployment_plan.md               ← DevOps + PO
├── 053_release_notes.md                 ← Everyone (PO, QA, Dev, Users)
└── 054_operations_manual_runbook.md     ← DevOps (ops bible)
```

## 051 — CI/CD Pipeline Configuration

**Audience:** Developers (how code gets built/tested), DevOps (pipeline maintenance)

**Must include:**
- Pipeline overview diagram (flowchart)
- Full workflow YAML (`.github/workflows/`) — not pseudocode
- Pipeline stages table (stage, purpose, duration, failure action)
- Environment configuration (branch → environment mapping)
- Secrets management table (what, where, rotation)
- Docker Compose production file
- Nginx config (if public access needed)
- Rollback procedure (image tag based)

**Key tailoring:** Workflow YAML must match actual build toolchain (Go/Node/etc.),
use correct service containers for tests (PostgreSQL, Redis), and deploy to
actual infrastructure (not generic K8s).

## 052 — Deployment Plan

**Audience:** DevOps (how to deploy), PO (what happens during deploy)

**Must include:**
- Deployment overview (method, target, downtime, rollback strategy)
- Deployment paths diagram (automated + manual fallback)
- First-time bootstrap guide (initial setup commands)
- Pre-deployment checklist (table with checkboxes)
- Step-by-step deployment procedure (both automated and manual)
- Post-deployment verification checklist (with actual commands)
- Rollback plan (application + database)
- Database migration strategy (risk matrix per migration type)
- Environment variables inventory

**Key tailoring:** Every command must work on the actual target infrastructure.
Don't write `kubectl` for Docker Compose projects. Include the actual SSH
command, actual compose file path, actual health check URLs.

## 053 — Release Notes

**Audience:** Everyone — developers, PO, stakeholders, users

**Must include:**
- Release template (copy-paste format for each release)
- Conventional commit → release section mapping
- Planned features list (from user stories / objectives)
- Release history table
- How to generate release notes (git log + GitHub auto-generate)

**Key tailoring:** Map the project's actual commit scopes to release sections.
List actual planned features with their user story references.

## 054 — Operations Manual / Runbook

**Audience:** DevOps (the operations bible)

**Must include:**
- System overview table (component, container, port, location)
- Access & credentials reference
- Daily/weekly/monthly routine checks (with actual commands)
- Operational procedures (restart, logs, envvars, migrations, cleanup)
- Troubleshooting guide (symptom → cause → investigation → resolution)
- Incident response steps (detect → assess → mitigate → resolve → review)
- Backup & recovery procedures
- Quick reference card (one-page cheat sheet)

**Key tailoring:** Troubleshooting tables should address project-specific failure
modes (e.g., "donation points not updating" for a VRM system, not generic
"application error"). Database queries should target the project's actual tables.

## Cross-Reference Convention

All documents link to each other and to upstream docs using `[[document_name]]`:

```
051 → 052 (deployment procedures)
051 → 032 (build scripts)
052 → 051 (pipeline config)
052 → 053 (release details)
052 → 054 (operational procedures)
053 → 052 (how release was deployed)
053 → 034 (commit messages / changelog)
054 → 052 (deployment procedures)
054 → 022 (API specification)
054 → 023 (database schema)
```
