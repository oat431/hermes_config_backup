# Cross-Disciplinary BOK Audit Patterns

This reference records durable patterns from an audit of local BABOK, PMBOK, SEBoK, CyBOK, DMBOK, HCI/UX, SWEBOK, and project-profile notes. Use it as an evidence checklist, not as a universal artifact catalog.

## High-value source comparisons

| Audit question | Source evidence to look for | Typical derived-file defect |
|---|---|---|
| Is an output really a standalone document? | BABOK defines broad business-analysis information and task outputs; PMBOK defines artifacts as documents or other items. | A checklist calls an outcome, model, source code, or configuration a “document” without artifact type. |
| Are priorities tailored? | PMBOK tailoring says approaches/processes may be added, modified, removed, or blended; SE standards distinguish compliance, conformance, and tailoring. | Dozens of red items are followed by a note saying no project needs every item. |
| Is the lifecycle vocabulary correct? | PMBOK says Focus Areas are not phases; SEBoK separates Concept, Development, Production, Utilization, Support, and Retirement. | Focus Areas or architecture are presented as sequential lifecycle phases. |
| Are operational/retirement controls present? | SWEBOK Operations/Maintenance and SEBoK Realization/Maintenance cover monitoring, incidents, recovery, sustainment, transition, and disposal. | The profile stops at CI/CD, deployment, and release notes. |
| Is a domain control conditional? | CyBOK and DMBOK describe controls based on threat, data type, architecture, law, and technology. | HSM, DPIA, MDM, dimensional models, WAF, or safety artifacts are red for every project. |
| Is the profile title justified? | Profile triggers should distinguish scale, complexity, safety/mission criticality, regulatory exposure, and certification. | Team size or duration alone activates a safety-critical/V-model profile. |

## Representative evidence patterns

- **BABOK transition gap:** `body-of-knowledge/BABOK/00_Introduction_to_BABOK.md` distinguishes business, stakeholder, solution, and transition requirements. A derived checklist that has a change strategy but no transition-requirements entry may miss migration, training, and business-continuity obligations.
- **PMBOK Focus Area error:** `body-of-knowledge/PMBOK/03_Project_Life_Cycles.md` explicitly says the five Focus Areas are not phases. A file titled “essential documents by phase” should either rename the structure or explain the distinction.
- **SEBoK lifecycle error:** `body-of-knowledge/System Engineer BOK/05_Life_Cycles_and_Processes.md` defines six typical stages. Architecture belongs to system definition/design, not between concept and realization as a universal stage.
- **CyBOK conditionality:** `body-of-knowledge/CyBOK/02_Law_and_Regulation.md` makes DPIAs conditional on high-risk personal-data processing. A universal red DPIA entry is overclassified.
- **CyBOK accountability gap:** `body-of-knowledge/CyBOK/01_Risk_Management_and_Governance.md` calls for accepted risks and accountable owners. A risk register plus treatment plan is not necessarily sufficient evidence.
- **DMBOK support omission:** `body-of-knowledge/DMBOK/00_Introduction_to_DMBOK.md` adds ethics, Big Data/Data Science, maturity, organization/roles, and organizational change-management chapters beyond the 11 KAs. A checklist limited to 11 KAs should state that scope explicitly.
- **UX source-authority check:** The local HCI notes cite NNG/IDEO/Lean UX and design-system sources rather than a formal BOK. The derived UX checklist should be labeled as a practice guide and should not imply that every method is an industry-mandated deliverable.
- **SWEBOK production-readiness check:** `software-engineering-note/06_Software_Engineering_Operations/Software Engineering Operations Overview.md` emphasizes SLAs, capacity, continuity, deployment/rollback, incident management, telemetry, and service reporting. A profile containing only CI/CD and a deployment plan has a production-readiness gap.

## Overlap clusters to normalize

1. **Need → requirement → design → implementation → verification:** BRD/business objective, stakeholder needs, SyRS/SRS, user stories, acceptance criteria, architecture/design, RTM, tests.
2. **Uncertainty and control:** risk register, risk assessment, risk treatment, accepted-risk record, issue log, risk report, hazard log, threat model.
3. **Change and baseline:** requirements change assessment, change request, change log, ECR/MR/PR, CCB decision, configuration baseline, FCA/PCA.
4. **Architecture and rationale:** system architecture description, functional/logical/physical views, SAD, HLD/LLD, ADR, trade study, design rationale.
5. **Data semantics and movement:** business glossary, data dictionary, metadata repository, lineage, mapping specification, data contract, data-sharing agreement.
6. **Quality and evidence:** quality plan, SQAP/QMS, V&V plan, test plan, verification/validation reports, defect log, audit report, coverage report.
7. **Security lifecycle:** security policy/ISMS, security requirements, threat model, security architecture, SSDLC, SAST/SCA/DAST, pen test, vulnerability management, incident response.
8. **Service operations:** SLA, SLO/SLI, monitoring dashboard, operational KPI report, runbook, incident report, postmortem, problem-management record.

For each cluster, define one canonical system of record and allow discipline-specific views or evidence attachments rather than independent copies.

## Count-validation recipe

When a master overview claims profile totals:

1. Count visible quick-start checkboxes separately.
2. Count all priority-table rows separately.
3. Normalize names and count unique artifacts.
4. Exclude repeated quick-start tables from the unique total.
5. Report the method next to the number.

Never compare a stated “documents” total with an unqualified line count.

## Report shape

For each high-impact finding use:

> **Finding — impact.** Derived file/section/lines. Source file/section/lines. Classification: omission | priority | overlap | contradiction | scope | terminology. Disposition: add | downgrade | make conditional | merge | crosswalk | document source inconsistency.

Separate:

- defects in the derived checklist;
- contradictions inside the source notes;
- missing content from the local vault;
- external-standard questions that were not checked.
