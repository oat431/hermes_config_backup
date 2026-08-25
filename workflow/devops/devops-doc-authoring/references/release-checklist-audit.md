# Release / Deployment Checklist Audit Reference

Use this reference when reviewing a reusable release checklist or deciding whether it is ready for full-scale production use.

## 1. Assess two dimensions separately

A checklist can have excellent lifecycle coverage while still being an incomplete release gate.

- **Lifecycle coverage:** versioning, build, promotion, migration, rollout, verification, rollback, communication, review.
- **Gate maturity:** evidence, artifact identity, approvals, risk decisions, health thresholds, recovery mechanics, observation, handoff, audit retention.

Recommended verdict vocabulary:

- **Strong full-lifecycle baseline:** covers the process, usable as a master checklist.
- **Production-ready gate with conditions:** sufficient for the stated environment after evidence and risk controls are recorded.
- **Not sufficient as a standalone gate:** important controls are delegated to linked documents or not defined.
- **Not sufficient for regulated/mission-critical use:** requires formal approvals, evidence retention, recovery exercises, and stronger assurance.

Do not equate “small/internal/POC” with “safe.” Exposure, data sensitivity, production credentials, business criticality, RTO/RPO, regulation, topology, and blast radius can raise the required control level.

## 2. Full-scale checklist control areas

### Release identity and evidence

Require a release record containing:

- service/system
- version or release ID
- source commit SHA
- CI workflow/build ID
- artifact/image digest
- target environment
- risk tier and overlays
- release owner, approver, and deployer
- rollback target
- change record, dashboard, runbook, and communication channel

For every checked gate, record evidence such as a CI run, test report, deployment ID, migration report, approval, dashboard snapshot, or incident/release ticket.

### Artifact integrity and promotion

Require:

- build once in CI
- exact artifact tested in staging is promoted to production
- no production rebuild
- immutable digest recorded
- SBOM associated with the exact artifact
- signature and provenance verified before deployment
- build metadata and release evidence retained

A tag is a human-friendly label; the immutable digest and source commit are the operational identity.

### Rollout and exposure

Separate two decisions:

- **Deployment strategy:** recreate, rolling, blue-green, canary, batch/job replacement, static artifact promotion.
- **Release exposure:** immediate, feature flag off, internal cohort, percentage rollout, tenant cohort, dark launch.

For progressive rollout, define stage sizes, observation periods, health signals, promotion criteria, abort criteria, pause/rollback behavior, and the responsible decision-maker.

### Health model

Distinguish startup, readiness, and liveness. Readiness may include dependency availability and should control traffic eligibility. Liveness should generally establish that the process is alive and able to make progress; dependency failures should not automatically cause restart storms.

### Rollback and recovery

Define concrete thresholds before deployment:

- error-rate threshold and duration
- latency threshold and duration
- business-transaction failure threshold
- queue lag/resource/database thresholds where applicable
- SLO burn-rate threshold
- hard safety/security signals

Use error budgets as decision context, not as the only rollback trigger. Explicitly choose whether recovery means artifact rollback, traffic switch, feature disablement, forward fix, database restore, or no rollback because a change is irreversible.

A deployment rollback does not undo already-written data, external side effects, or irreversible schema changes.

### Database and stateful changes

Require:

- compatibility with both previous and new application versions where rollback is expected
- migration dry run on representative data
- lock duration and runtime assessment
- bounded backfill and resource monitoring
- post-migration data validation
- explicit down-migration, restore, forward-fix, or no-rollback decision
- approval for irreversible changes

### Risk overlays

Use tier as a baseline, then apply overlays for:

- internet exposure
- personal, confidential, or regulated data
- production credential access
- business criticality and blast radius
- RTO/RPO and backup/restore obligations
- distributed-system complexity
- database/schema changes
- security-sensitive changes

No tier should skip the universal baseline: secret protection, source/artifact traceability, access control, basic validation, production isolation, monitoring, named owner, and a recovery decision.

For non-applicable controls, record `N/A — reason`, and for exceptions record approver and expiry/review date.

### Emergency releases

A full-scale checklist needs a controlled emergency/hotfix path. Define who may authorize it, which checks can be shortened, which baseline controls are never skipped, and the required retrospective review and evidence capture.

### Closeout

Require:

- deployed version/digest verified from the running system
- smoke tests and business-critical flows completed
- observation window completed
- dashboards, logs, traces, and alerts reviewed
- no abort threshold breached
- on-call handoff completed
- temporary flags/configuration/elevated access removed or tracked
- release evidence archived
- delivery metrics recorded
- follow-up actions assigned

## 3. Platform-neutrality check

If a document claims to cover APIs, frontends, batch jobs, workers, mobile backends, or infrastructure, do not make Kubernetes or HTTP traffic assumptions mandatory. Use platform-neutral gates and link to platform-specific deployment plans/runbooks.

Workload-specific additions may be needed:

- batch: idempotency, checkpointing, duplicate execution, output validation
- workers/consumers: queue lag, dead-letter behavior, drain behavior, compatibility
- mobile: API backward compatibility, store rollout, supported versions, kill switch
- static frontend: cache invalidation, CDN/origin propagation, manifest rollback
- infrastructure: plan review, drift, state backup, blast-radius simulation

## 4. Research anchors

- Google SRE recommends staged, supervised rollouts; when unexpected behavior appears, roll back first and diagnose afterward to minimize recovery time. See `https://sre.google/sre-book/service-best-practices/`.
- Google SRE release engineering emphasizes automated, hermetic/reliable delivery and archiving the changes included in a release with build artifacts. See `https://sre.google/sre-book/release-engineering/`.
- SLSA verification includes checking trusted builder identity, provenance signature, and expected build parameters; generating provenance without inspecting it is insufficient. See `https://slsa.dev/spec/v1.0/verifying-artifacts` and `https://slsa.dev/spec/v1.1/provenance`.
- NIST SP 800-218 SSDF recommends preserving software releases and integrity/provenance information for later vulnerability analysis. See `https://csrc.nist.gov/pubs/sp/800/218/final`.
- DORA’s current delivery metrics include change lead time, deployment frequency, failed deployment recovery time, change fail rate, and deployment rework rate. See `https://dora.dev/guides/dora-metrics/`.
- Microsoft safe-deployment guidance emphasizes small, incremental, quality-gated releases, progressive exposure, health models, rollback plans, and emergency protocols. See `https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments`.

## 5. Audit reporting pattern

Report:

1. scope and files inspected
2. overall verdict using the vocabulary above
3. strengths
4. high-priority findings with line references
5. technical corrections
6. missing controls
7. tier/risk-scope issues
8. recommended changes before production use
9. whether the file was modified

When the user asks whether to create a separate “low-risk” checklist, prefer improving the canonical full-lifecycle checklist with risk overlays unless the workflows are genuinely different.
