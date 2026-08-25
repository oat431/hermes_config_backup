# Essential-Document Catalog Audit — Reusable Evidence Notes

Use this reference with the `Auditing Essential-Document Catalogs` section in the parent skill.

## Audit stance

An Essential Documents folder is not automatically a set of templates. It may contain a mixture of:

- information products;
- lifecycle plans and baselines;
- registers, logs, and records;
- review/approval evidence;
- models and diagrams;
- generated reports and tool outputs;
- techniques or methods;
- organization-level, regulatory, or safety evidence.

The audit must distinguish those classes before proposing additions.

## Evidence pattern from the 2026-08-03 audit

The audited folder contained 11 Markdown files, a SWEBOK checklist with 145 table rows, and Small/Medium/Large profile presets. It had broad lifecycle coverage, but the highest-value findings were governance and classification gaps rather than missing diagram types:

1. Universal versus conditional priority semantics were mixed.
2. Tailoring/documentation strategy was not a first-class artifact.
3. Vision/scope/success criteria was implicit rather than explicit.
4. Software engineering management and measurement were weaker than the completed notes: estimate basis, metrics plan, performance/status reporting, process monitoring, acquisition/supplier management, and lessons learned.
5. Lifecycle/process definition was represented mainly by methodology labels.
6. Requirements/design approval, verification, validation, acceptance, and quality-gate evidence were fragmented.
7. Operational readiness, post-deployment validation, service/problem management, and retirement were underrepresented in the main software checklist.
8. Cross-BOK aliases and shared artifacts were duplicated without a canonical source-of-truth rule.
9. Hard-coded source paths were stale even though local wikilinks resolved.
10. Profile counts and priority checklists were not fully synchronized.

## Recommended catalog row schema

Every catalog row should answer:

| Field | Question |
|---|---|
| Canonical name | What is the authoritative artifact called? |
| Aliases | What do other BOKs/teams call it? |
| Class | Artifact, plan, baseline, register/log, report, record, model, generated output, technique, or evidence? |
| Purpose | What decision, risk, or handoff does it support? |
| Owner/consumers | Who owns and uses it? |
| Lifecycle point | When is it created, updated, approved, superseded, or archived? |
| Applicability trigger | What condition makes it required? |
| Minimum form | What is the lightest acceptable representation? |
| Formal form | What is required for regulated/high-risk contexts? |
| Inputs/outputs | What does it consume and produce? |
| Traceability | Which objective, requirement, design, test, release, or incident does it link to? |
| Approval/evidence | Who approves it and what proves completion? |
| Source BOK/standard | Which source supports it? |
| Source of truth | Where does the authoritative copy live? |

## Control-loop completeness checklist

Audit these before spending time on optional artifacts:

- Vision, scope, and success criteria
- Tailoring/documentation strategy
- Lifecycle/process definition
- Requirements baseline and change control
- Architecture/design baseline and decision rationale
- Estimate basis and uncertainty
- Measurement/metrics plan and performance reporting
- Risk register and response tracking
- Verification/validation/acceptance strategy
- Quality gate/readiness decision with exceptions
- Operational readiness and post-deployment validation
- Maintenance/problem management and technical debt
- Retirement/decommissioning and data handling

## Profile audit dimensions

Do not treat team size as the only profile axis. Evaluate at least:

- team size and distribution;
- lifecycle/methodology;
- product/system criticality;
- regulatory and contractual obligations;
- data sensitivity and privacy;
- operational exposure and service commitments;
- integration/distributed-system complexity;
- product maturity: prototype, MVP, production, legacy;
- expected staff turnover and supplier dependence.

A five-person safety-critical project may require more evidence than a fifty-person internal prototype.

## Source-path verification

For local Obsidian vault work:

1. Resolve the actual vault root before reading files.
2. Search the target folder and source folders using concrete Windows paths.
3. Check literal `F:\...`/`C:\...` references separately from wikilinks.
4. Prefer vault-relative links or a central source registry over hard-coded machine paths.
5. Report stale paths as correctness findings, not merely formatting issues.

## Recommended audit report structure

1. Frontmatter: status, version, audit date.
2. Scope and evidence sources.
3. Executive verdict.
4. Inventory snapshot.
5. Findings table with IDs, priority, evidence, and impact.
6. Detailed findings with exact file/line references.
7. BOK-by-BOK assessment.
8. Recommended artifact families.
9. Priority reclassification guidance.
10. Future rewrite structure and phased order.
11. Quality gate for the rewrite.
12. Handoff and revision history.

## Do not overcorrect

- Do not add one file per BOK output.
- Do not call every BOK topic a project deliverable.
- Do not downgrade all red rows simply to reduce the count; add applicability triggers instead.
- Do not make organization-level ISMS/QMS/SOA/SIEM, enterprise data, MBSE, formal assurance, or safety artifacts universal without a project trigger.
- Do not replace a read-only audit with a template rewrite unless the user explicitly changes scope.

## Session-specific tool note

On Windows, some file-search helpers may translate `F:` to an unavailable `/f` mount. Prefer concrete Windows paths with `read_file`/`terminal` when that occurs, and treat the workaround as a path-resolution detail rather than a permanent tool limitation.
