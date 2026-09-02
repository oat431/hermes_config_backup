# Template Fix Patterns

> Ready-to-paste content blocks for common ISO/IEEE compliance fixes. Each block includes the mermaid diagrams and tables developed during the July 2026 fix session. Copy, adapt placeholders, and insert via `patch`.

---

## Fix 1: SCMP — Configuration Control Board (CCB)

**Standard:** IEEE 828-2012 Annex A
**Insert after:** Configuration Control section (before Status Accounting)

```markdown
## N. Configuration Control Board (CCB)

> Per IEEE 828-2012, a CCB must be defined with clear membership and authority for approving changes to baselined configuration items.

| Field | Detail |
|-------|--------|
| **CCB Name** | [Project Configuration Control Board] |
| **Charter** | Reviews and approves/disapproves all change requests affecting baselined CIs |
| **Quorum** | [Chair + Tech Lead + QA Lead] |
| **Meeting Frequency** | [Weekly / On-demand for urgent changes] |

| Role | Name | Authority |
|------|------|-----------|
| [CCB Chair] | [PM / Delivery Manager] | [Final approval authority] |
| [Technical Lead] | [Name] | [Technical impact assessment] |
| [QA Lead] | [Name] | [Quality impact assessment] |
| [Architect] | [Name] | [Architecture impact assessment] |
| [Security Officer] | [Name] | [Security impact assessment (if applicable)] |

| Decision Type | Authority | Turnaround |
|---------------|----------|------------|
| [Emergency hotfix] | [Tech Lead + CCB Chair] | [< 2 hours] |
| [Standard CR] | [Full CCB] | [Within 1 week] |
| [Major architectural change] | [CCB + Sponsor] | [Within 2 weeks] |
```

---

## Fix 2: SCMP — Baseline Definitions

**Standard:** IEEE 828-2012
**Insert after:** CCB section

```markdown
## N. Baseline Definitions

> Per IEEE 828-2012, baselines must be defined with their establishment points in the lifecycle.

| Baseline | Established When | Contents | Approval Required |
|----------|-----------------|----------|-------------------|
| [Requirements Baseline] | [SRS approved] | [SRS, NFR Catalog, RTM] | [Business Owner, BA Lead] |
| [Architecture Baseline] | [SAD approved] | [SAD, ADRs, Architecture Views] | [Architect, Tech Lead] |
| [Design Baseline] | [HLD/LLD approved] | [HLD, LLD, API Specs, ERD] | [Tech Lead, Architect] |
| [Code Baseline (Development)] | [End of sprint] | [Source code, unit tests] | [Tech Lead] |
| [Product Baseline] | [Release approved] | [All CIs: code, tests, docs, configs] | [CCB] |
| [Operational Baseline] | [Deployment to prod] | [Deployed artifacts, IaC, runbooks] | [DevOps Lead] |

\```mermaid
flowchart LR
    RB[Requirements<br>Baseline] --> AB[Architecture<br>Baseline]
    AB --> DB[Design<br>Baseline]
    DB --> CB[Code<br>Baseline]
    CB --> PB[Product<br>Baseline]
    PB --> OB[Operational<br>Baseline]
\```
```

---

## Fix 3: SCMP — Release Management and Delivery

**Standard:** IEEE 828-2012 (5th required CM process)
**Insert after:** Configuration Audits section

```markdown
## N. Release Management and Delivery

### N.1 Release Packaging

| Release Type | Trigger | Contents | Approval |
|--------------|---------|----------|----------|
| [Major (X.0.0)] | [Significant new features / breaking changes] | [Full system + migration scripts] | [CCB + Sponsor] |
| [Minor (0.X.0)] | [New features, backward-compatible] | [Updated system + release notes] | [CCB] |
| [Patch (0.0.X)] | [Bug fixes only] | [Patched system + changelog] | [Tech Lead] |
| [Hotfix] | [Critical production issue] | [Targeted fix + rollback plan] | [Tech Lead + CCB Chair] |

### N.2 Release Process

\```mermaid
flowchart TD
    REL[Release Candidate<br>Ready] --> QA[QA Sign-off]
    QA --> CCB[CCB Approval]
    CCB --> PKG[Package Release Artifacts]
    PKG --> TAG[Tag in VCS +<br>Create Version Description Document]
    TAG --> DEPLOY[Deploy to Staging]
    DEPLOY --> SMOKE[Smoke Test]
    SMOKE --> PROD[Deploy to Production]
    PROD --> ARCHIVE[Archive Release Artifacts]
    ARCHIVE --> NOTIFY[Notify Stakeholders]
\```

### N.3 Delivery Artifacts

| Artifact | Description | Storage |
|----------|-------------|---------|
| [Version Description Document] | [[Version-Description-Document]] | [Repository] |
| [Release Notes] | [[Release-Notes]] | [Repository] |
| [Container Image] | [Docker image with tag] | [Container Registry] |
```

---

## Fix 4: SCMP — SCM Schedule, Resources, Plan Maintenance

**Standard:** IEEE 828-2012 Annex A §4-6
**Insert before:** Related Documents

```markdown
## N. SCM Schedule

| Milestone | CM Activity | Deliverable |
|-----------|-------------|-------------|
| [Project Start] | [Establish CM process, tools, repository] | [SCMP approved] |
| [Requirements Approved] | [Establish Requirements Baseline] | [Baseline record] |
| [Architecture Approved] | [Establish Architecture Baseline] | [Baseline record] |
| [End of Sprint] | [Code baseline, CI/CD status report] | [Sprint CM report] |
| [Pre-Release] | [FCA + PCA audits] | [Audit reports] |
| [Release] | [Product baseline, VDD, release notes] | [Release package] |
| [Post-Deployment] | [Operational baseline, archival] | [Archive confirmation] |

## N+1. SCM Resources

| Resource Type | Detail |
|---------------|--------|
| [CM Tool] | [Git + GitHub / GitLab / Bitbucket] |
| [CI/CD Tool] | [GitHub Actions / GitLab CI / Jenkins] |
| [Artifact Repository] | [Container registry / Nexus / Artifactory] |
| [CM Personnel] | [Configuration Manager: [Name]] |
| [Training] | [Git workflow training for all new team members] |

## N+2. SCM Plan Maintenance

| Field | Detail |
|-------|--------|
| [Plan Owner] | [Configuration Manager] |
| [Review Frequency] | [Per release or major process change] |
| [Change Process] | [Changes to this SCMP follow the same CR/CCB process as other CIs] |
| [Version History] | See YAML frontmatter `version` and `last_updated` fields |
```

---

## Fix 5: V&V Plan — Integrity Level Assignment

**Standard:** IEEE 1012-2017
**Insert after:** Purpose section

```markdown
## N. Software/System Integrity Level

> Per IEEE 1012-2017, the integrity level (1-4) determines which V&V tasks are mandatory and the rigor required.

| Integrity Level | Description | Failure Consequence | Typical Application |
|----------------|-------------|---------------------|---------------------|
| **Level 1: Catastrophic** | Loss of life, total system loss | [Could result in death or total system failure] | [Aviation, medical, nuclear] |
| **Level 2: Critical** | Severe injury, major system damage | [Could result in severe injury or major loss] | [Banking, industrial control, automotive] |
| **Level 3: Marginal** | Minor injury, minor degradation | [Could result in minor injury or marginal loss] | [Enterprise software, e-commerce] |
| **Level 4: Negligible** | No injury, no system damage | [No significant impact] | [Internal tools, prototypes] |

**Project Integrity Level Assignment:**

| Field | Value |
|-------|-------|
| **Assigned Integrity Level** | [Level 3: Marginal] |
| **Rationale** | [Enterprise application: no safety risk, but financial impact from downtime] |
| **Implications for V&V** | [Standard V&V tasks required per IEEE 1012 § for Level 3] |
| **V&V Independence Required** | [Technical independence required for Level 2-4] |
```

---

## Fix 6: V&V Plan — Independence Statement

**Standard:** IEEE 1012-2017
**Insert after:** Integrity Level section

```markdown
## N. V&V Independence

> Per IEEE 1012-2017, V&V must have appropriate independence based on the integrity level.

| Independence Type | Required? | Description | Implementation |
|-----------------|-----------|-------------|----------------|
| **Technical Independence** | [Yes/No] | [V&V team has separate technical skills] | [QA team reports independently] |
| **Managerial Independence** | [Yes/No] | [V&V reports to different management chain] | [QA reports to Quality Director] |
| **Financial Independence** | [Yes/No] | [V&V budget is separate from development] | [Separate QA budget line] |

> For Integrity Level 1 (Catastrophic), all three independence types are required.
```

---

## Fix 7: V&V Plan — Anomaly Resolution

**Standard:** IEEE 1012-2017 §5.1
**Insert before:** V&V Schedule

```markdown
## N. Anomaly Resolution and Reporting

\```mermaid
flowchart TD
    DETECT[V&V Anomaly<br>Detected] --> REPORT[Report via<br>Defect Report]
    REPORT --> CLASSIFY[Classify<br>Severity]
    CLASSIFY --> ASSIGN[Assign to<br>Developer]
    ASSIGN --> FIX[Implement<br>Fix]
    FIX --> REVERIFY[Re-verify<br>via V&V]
    REVERIFY --> CLOSE{Resolved?}
    CLOSE -->|Yes| CLOSED[Close<br>Anomaly]
    CLOSE -->|No| ASSIGN
    CLOSED --> TREND[Track in<br>Defect Metrics]
\```

| Anomaly Severity | Reporting Timeframe | Escalation |
|-----------------|--------------------|-----------|
| [Critical] | [Immediate] | [Tech Lead + PM] |
| [High] | [Within 4 hours] | [Tech Lead] |
| [Medium] | [Within 1 day] | [Developer Lead] |
| [Low] | [Within 3 days] | [Backlog] |
```

---

## Fix 8: Test Plan — Suspension and Resumption Criteria

**Standard:** ISO/IEC/IEEE 29119-3 §8
**Insert after:** Entry/Exit Criteria section

```markdown
### N.2 Suspension Criteria

> Per ISO/IEC/IEEE 29119-3, the test plan must define conditions under which testing is suspended.

| Condition | Trigger | Action |
|-----------|---------|--------|
| [Critical defect blocks testing] | [A Critical defect prevents further test execution] | [Suspend affected test phase immediately] |
| [Excessive critical defects] | [> 5 Critical defects found in a single test session] | [Suspend testing, escalate to PM + Tech Lead] |
| [Test environment unavailable] | [Environment down for > 4 hours] | [Suspend testing, notify stakeholders] |
| [Build instability] | [Build fails to deploy or crashes on startup] | [Suspend until stable build provided] |

### N.3 Resumption Requirements

> Per ISO/IEC/IEEE 29119-3, the test plan must define what must be true before testing resumes.

| Suspension Cause | Resumption Requirement |
|-----------------|----------------------|
| [Critical defect fixed] | [Fix verified, build redeployed, affected tests re-run] |
| [Excessive defects resolved] | [Root cause analysis completed, fixes verified by dev] |
| [Environment restored] | [Environment health check passed, data valid] |
| [Stable build provided] | [Smoke tests passed on new build] |
```

---

## Fix 9: Test Plan — Staffing and Training

**Standard:** ISO/IEC/IEEE 29119-3 §13
**Insert after:** Test Resources section

```markdown
## N. Staffing and Training Needs

### N.1 Test Team Composition

| Role | Count | Required Skills | Assigned |
|------|-------|----------------|----------|
| [QA Lead] | [1] | [Test strategy, planning, coordination, risk assessment] | [Name] |
| [QA Engineer — Automation] | [1] | [Jest, Playwright, CI/CD integration, scripting] | [Name] |
| [QA Engineer — Manual] | [1] | [Test case design, exploratory testing, defect reporting] | [Name] |
| [Business Analyst (UAT)] | [1] | [Business processes, acceptance criteria, stakeholder mgmt] | [Name] |

### N.2 Training Requirements

| Training | Who | When | Duration |
|----------|-----|------|----------|
| [Domain/Product training] | [All QA] | [Project kickoff] | [2 days] |
| [Automation tools training] | [QA Engineers] | [Before automation starts] | [3 days] |
| [Test management tool] | [All QA] | [Project kickoff] | [0.5 day] |
| [Security testing basics] | [QA Engineers] | [Before security testing] | [1 day] |
| [Accessibility testing (WCAG)] | [QA Engineers] | [Before a11y testing] | [1 day] |
```

---

## Fix 10: SQAP — SQA Independence

**Standard:** IEEE 730-2014
**Insert after:** Purpose section

```markdown
## N. SQA Independence

> Per IEEE 730-2014, the SQA function must be organizationally independent from development to ensure objective assessment.

| Independence Aspect | Implementation |
|--------------------|---------------|
| **Reporting Structure** | [QA Lead reports to: Quality Director / PM, not Dev Lead] |
| **Technical Independence** | [QA team has separate evaluation authority: QA can block release] |
| **Budget Independence** | [QA budget is a separate line item, not controlled by Dev] |
| **Conflict Resolution** | [If QA and Dev disagree: escalate to [CCB / Steering Committee]] |

> SQA independence means QA can report non-compliance without fear of reprisal. If QA reports to the development manager, independence is compromised.
```

---

## Fix 11: SQAP — Supplier and Vendor Quality Control

**Standard:** IEEE 730-2014 §11
**Insert after:** Non-Compliance Process section

```markdown
## N. Supplier and Vendor Quality Control

> Per IEEE 730-2014, if external vendors or contractors deliver components, their work must be subject to SQA oversight.

| Supplier Type | SQA Activity | Acceptance Criteria |
|---------------|-------------|---------------------|
| [Contractor developers] | [Code review by internal team] | [Meets Coding Standards, passes static analysis] |
| [Third-party APIs] | [Integration testing + SLA review] | [Meets NFR performance targets, documented SLA] |
| [Open-source dependencies] | [License check + security scan] | [No GPL violations, no known CVEs] |
| [Outsourced testing] | [Review test results, verify coverage] | [Test plan approved, exit criteria met] |
| [Cloud provider] | [Review SLA + compliance certifications] | [ISO 27001 certified, uptime >= 99.9%] |
```

---

## Fix 12: SQAP — Quality Records Management

**Standard:** IEEE 730-2014 §12
**Insert after:** Supplier Control section

```markdown
## N. Quality Records Management

> Per IEEE 730-2014, quality records must be collected, maintained, and retained as evidence of SQA activities.

| Record Type | Storage | Retention | Access |
|-------------|---------|-----------|--------|
| [Review Records] | [Repository / Wiki] | [Project + 7 years] | [Team] |
| [Test Results] | [CI/CD system] | [Project + 7 years] | [QA + Dev] |
| [Defect Reports] | [Defect tracking system] | [Project + 7 years] | [QA + Dev] |
| [Audit Reports] | [Document repository] | [Permanent] | [QA Lead + Management] |
| [SQA Reports] | [Document repository] | [Project + 7 years] | [Management] |
| [Non-compliance Records] | [Document repository] | [Project + 7 years] | [QA Lead + Management] |
```

---

## Verification Script

After applying fixes, run this verification to confirm all changes landed:

```bash
echo "FIX VERIFICATION"
echo "1. SCMP CCB: $(grep -c 'Configuration Control Board' SCMP.md)"
echo "2. SCMP Sections: $(grep '^## ' SCMP.md | wc -l)"
echo "3. V&V Integrity: $(grep -c 'Integrity Level' VandV-Plan.md)"
echo "4. V&V Lifecycle Phases: $(grep -c 'Phase V&V' VandV-Plan.md)"
echo "5. 20000-1 Incorrect (should be 0): $(grep -rc 'ISO/IEC/IEEE 20000' . | grep -v ':0' | wc -l)"
echo "6. Test Plan Suspension: $(grep -c 'Suspension' Test-Plan.md)"
echo "7. Test Plan Staffing: $(grep -c 'Staffing' Test-Plan.md)"
echo "8. SQAP Independence: $(grep -c 'Independence' SQAP.md)"
echo "9. SQAP Supplier: $(grep -c 'Supplier' SQAP.md)"
```

---

## YAML Frontmatter Updates

When fixing templates, update the frontmatter to reflect the specific standard version:

### SCMP
```yaml
tags: [scmp, configuration-management, swebok, ieee-828]
standard_ref:
  - SWEBOK v4 — Configuration Management
  - IEEE 828-2012 — Configuration Management in Systems and Software Engineering (Annex A)
```

### V&V Plan
```yaml
tags: [verification, validation, v-and-v, swebok, ieee-1012]
standard_ref:
  - SWEBOK v4 — Quality Assurance
  - IEEE 1012-2017 — System, Software, and Hardware Verification and Validation
  - ISO/IEC/IEEE 12207 — Software Life Cycle Processes
```

### SQAP
```yaml
tags: [sqap, quality-assurance, swebok, ieee-730, iso-9001]
standard_ref:
  - SWEBOK v4 — Quality Assurance
  - IEEE 730-2014 — Software Quality Assurance Processes
  - ISO/IEC/IEEE 90003 — Quality Assurance
  - ISO 9001 — Quality Management
```

### Test Plan
```yaml
standard_ref:
  - SWEBOK v4 — Testing
  - ISO/IEC/IEEE 29119-3 — Software Testing Documentation (Annex: Test Plan content)
```
