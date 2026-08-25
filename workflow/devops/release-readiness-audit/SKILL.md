---
name: release-readiness-audit
description: Audit release checklists for production readiness.
trigger: >
  Use when reviewing a release/deployment checklist, release process, or production-readiness gate.
category: devops
---

# Release Readiness Audit

Audit release and deployment checklists as operational control documents, not merely as prose. The goal is to determine whether the checklist can support a safe, traceable release decision at the stated project scale, while preserving the distinction between a release-process checklist and domain-specific readiness checklists.

## When to Use

- A user asks to audit, review, or assess a release/deployment checklist.
- A team wants to validate a production gate before adopting it.
- A checklist family has separate API, frontend, microservice, security, or infrastructure gates that need consistency review.
- A release process contains rollout, migration, rollback, observability, or supply-chain controls that need technical verification.

## Scope and Safety

1. Treat the requested file as the primary object of review.
2. Do not edit the file during an audit unless the user explicitly asks for remediation or a rewrite.
3. Inspect local sibling and linked checklists when available; they are part of the checklist's operating context.
4. Distinguish facts observed in the file from recommendations and from assumptions about the user's platform.
5. Report the exact file path and line references for findings. If line numbers change after an edit, regenerate them rather than reusing stale references.
6. End an audit with an explicit statement about whether the file was modified.

## Audit Workflow

### 1. Establish the document contract

Determine:

- Is this a release-process checklist, deployment checklist, application readiness checklist, or a mixture?
- What workloads does it claim to cover: HTTP services, workers, batch jobs, mobile clients, static frontends, infrastructure, or all of them?
- Who is the decision maker and who is expected to check the boxes?
- Does it define a minimum baseline, tiered controls, or both?
- Does it capture evidence, or only a yes/no decision?

If a document claims to be framework-agnostic, treat platform-specific commands and assumptions as findings unless they are clearly labeled examples.

### 2. Inventory structure and references

Record:

- File path, line count, headings, checkbox count, tables, diagrams, and last-updated metadata.
- Wikilinks and relative links; verify linked notes exist when the vault is accessible.
- Sibling/domain checklists and their overlap boundaries.
- Source references for standards or technical claims.

Do not infer that a wiki link is valid merely because it is syntactically well-formed. Check whether the target exists and whether its scope matches the link's stated purpose.

### 3. Read the operating context

Read linked/domain checklists before judging duplicated or delegated controls. At minimum, inspect applicable API, frontend, microservice, security, deployment, rollback, SLO/SLI, and incident-response documents. Compare:

- terminology and section names;
- whether one checklist owns a control or merely references it;
- conflicting requirements;
- duplicated checks that can drift;
- missing handoff points between checklists.

### 4. Audit the lifecycle controls

Evaluate each of these dimensions, even when the checklist does not use these exact headings:

1. **Release identity and traceability** — version, source commit, build/workflow ID, artifact digest, target environment, deployment record, rollback target.
2. **Build and supply chain** — locked inputs, controlled build, tests against the built artifact, SBOM, signatures, provenance, registry immutability, verification at deploy.
3. **Environment promotion** — staging-before-production, environment-specific configuration, secret separation, parity exceptions, build-once/promote-the-same-artifact.
4. **Data and migrations** — backups and restore evidence, migration ordering, compatibility with old/new application versions, locking and duration, backfill validation, forward-fix versus restore decision.
5. **Deployment strategy** — recreate, rolling, blue-green, canary, batch replacement, mobile/static promotion, or other workload-appropriate strategy.
6. **Release exposure** — feature flags, cohorts, internal users, percentage rollout, dark launch, activation and cleanup. Keep this separate from deployment topology.
7. **Pre-deploy gates** — owner, approver, runbook, probes, capacity, dependencies, maintenance window, change record, escalation path.
8. **Post-deploy verification** — smoke tests, version/digest verification, dashboards, logs, traces, business metrics, observation window, on-call handoff.
9. **Rollback and recovery** — explicit triggers, mechanism, time target, data consequences, practiced procedure, forward-fix decision, recovery objective.
10. **Communication and learning** — stakeholders, on-call, status page, release record, DORA metrics, incident/postmortem linkage, artifact/log retention.

### 5. Check technical correctness

Apply these rules while reviewing the text:

- A version tag is not sufficient artifact identity. Require the source commit, build ID, and immutable artifact/image digest.
- An annotated tag should be created deliberately and pushed specifically; `git push --tags` can push unrelated local tags and does not itself create an annotated tag.
- SemVer pre-release labels such as `-rc.1` identify precedence/version state; they are not a substitute for canary traffic, feature flags, or staged exposure.
- Lockfiles and digest-pinned base images improve determinism but do not alone prove byte-for-byte reproducibility. Separate pinned inputs, controlled builds, and reproducibility verification.
- Require build once, test the exact built artifact, and promote that artifact without rebuilding for production.
- SBOMs, signatures, and provenance must be associated with the exact artifact digest and verified before deployment.
- A down migration is not automatically a safe rollback. State whether the release uses an application rollback, forward fix, compatible schema, restore, or another recovery path.
- Expand-contract migrations must preserve compatibility during the overlap period and must include backfill, validation, lock/latency analysis, and removal timing.
- Deployment topology and release exposure are separate decisions. A feature flag can accompany a rolling, blue-green, or canary deployment.
- Startup, readiness, and liveness have different semantics. Dependency failure may make an instance unready, but should not automatically make a healthy process non-live and cause restart amplification.
- An SLO error budget is a decision signal, not a single rollback threshold. Require concrete error/latency/business-impact thresholds, burn-rate or budget-consumption logic, and a sustained duration.
- Prefer current DORA terminology: deployment frequency, change lead time, change fail percentage, and failed deployment recovery time. Define the measurement boundaries.
- HTTP/Kubernetes examples must not be normative in a checklist that claims to cover batch, mobile, static, or non-HTTP workloads.

### 6. Audit tiering and exceptions

A user count or internal/external classification is not a complete risk model. Check for independent overlays:

- exposure and blast radius;
- data sensitivity and privacy;
- business or safety criticality;
- RTO/RPO and recoverability;
- topology/statefulness;
- regulatory obligations;
- change type and reversibility.

The effective control level should be the highest applicable requirement across the overlays. POCs and internal tools still need a non-negotiable baseline: no secrets in source, no unsafe production access, basic access control, source/artifact traceability, and isolation or explicit approval.

For every skipped item, require either:

```markdown
- [ ] N/A — reason:
- [ ] Exception approved by:
- [ ] Review/expiry date:
```

### 7. Produce actionable findings

Use severity based on operational consequence:

- **Critical** — can cause unsafe production change, unrecoverable data loss, or false release approval.
- **High** — important traceability, rollback, migration, security, or observability gap.
- **Medium** — material ambiguity, maintainability issue, or missing evidence.
- **Low** — wording, consistency, formatting, or convenience improvement.

For each finding include:

1. severity;
2. exact line(s) or section;
3. the observed statement;
4. why it matters operationally;
5. a concrete recommendation;
6. whether the fix belongs in this checklist or a linked runbook/template.

Separate **must change before production use** from **recommended hardening**. Do not bury blockers in a long undifferentiated list.

### 8. Verify the audit result

Before finalizing:

- Recheck every cited line against the file.
- Confirm linked-file findings are based on the actual linked notes.
- Confirm recommendations do not contradict the user's documented infrastructure or workflow.
- State whether the file was changed.
- If the user requested only an audit, do not present proposed text as if it was applied.

## Evidence Record Pattern

A reusable release checklist should begin with or link to a release record containing:

- service/system;
- release/change ID;
- version;
- source commit SHA;
- CI build/workflow ID;
- artifact/image digest;
- target environment;
- selected tier and risk overlays;
- release owner, deployer, and approver;
- rollout/exposure strategy;
- rollback artifact and procedure;
- dashboard, runbook, change record, and communication channel;
- observation-window result and final sign-off.

Every checked gate should have an evidence link where practical: CI run, test report, scan, migration record, deployment ID, dashboard snapshot, approval, or incident/release ticket.

## Common Pitfalls

| Pitfall | Why it happens | Prevention |
|---|---|---|
| Auditing only the target file | The checklist delegates controls to sibling notes | Read linked/domain checklists and verify ownership boundaries |
| Treating every checkbox as equally important | Long lists obscure release blockers | Classify findings by operational severity and identify hard gates |
| Confusing version, tag, and artifact identity | Human-readable labels are convenient | Require commit, build ID, digest, and provenance |
| Treating `-rc` as a canary | Version semantics and rollout semantics are conflated | Separate version state from deployment and exposure controls |
| Recommending generic reproducible builds | Lockfiles are mistaken for proof | Distinguish pinned inputs, controlled build, and verification |
| Treating down migrations as universal rollback | Schema/data changes may be irreversible | Decide rollback, forward fix, restore, or compatibility path per migration |
| Using “SLO violated” as the only rollback rule | SLO windows are too coarse for release decisions | Define thresholds, burn rate, duration, and business impact |
| Putting dependency checks in liveness | Readiness and liveness are conflated | Define startup/readiness/liveness behavior separately |
| Making Kubernetes commands normative | The checklist claims broader workload coverage | Label platform examples or move them to runbooks |
| Letting POCs skip all controls | Lifecycle label hides exposure/data risk | Enforce a universal baseline and risk overlays |
| Using user count as the main tier determinant | Small systems can be highly critical | Add sensitivity, criticality, recovery, and blast-radius overlays |
| Giving an audit report without evidence boundaries | Recommendations sound like facts | Distinguish observed, inferred, recommended, and unverified items |

## Support Files

- `references/release-checklist-audit-pattern.md` — condensed audit evidence model, technical correction patterns, and representative findings from the first release-checklist audit.
