---
name: knowledge-base-quality-audit
description: Use when auditing checklists against source BOKs.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [knowledge-base, documentation, audit, bok, traceability, consistency]
    related_skills: [obsidian, po-requirements-elicitation, spec-document-elicitation]
---

# Knowledge-Base Quality Audit

## Overview

Audit document checklists, project profiles, templates, and overview notes against the local source body-of-knowledge files and companion engineering notes. The output is a read-only, evidence-based review: omissions, questionable priorities, overlaps, contradictions, terminology errors, scope drift, stale links, and profile-selection problems.

Do not edit source or derived files during the audit. Treat the source files as the local authority for what the vault claims; do not silently repair contradictions in the source. Report source-note inconsistencies separately from derived-checklist defects.

For a condensed cross-disciplinary evidence pattern and reusable examples, see `references/cross-disciplinary-bok-audit-patterns.md`.

## When to Use

Use this skill when the user asks to:

- audit or review essential-document sets, templates, checklists, or project profiles;
- compare summaries or extracts against BABOK, PMBOK, SEBoK, CyBOK, DMBOK, SWEBOK, HCI, or another source BOK;
- identify omissions, misprioritized artifacts, duplicate records, conflicting terminology, or scope problems;
- verify that a derived knowledge-base note is faithful to its local source notes;
- perform a read-only documentation-quality or cross-disciplinary consistency review.

Do not use this skill for ordinary proofreading, requirements elicitation, backlog creation, or editing the audited documents unless the user separately authorizes a post-audit remediation.

## Audit Model

Separate four layers before judging coverage:

1. **Source authority** — the BOK overview, chapter files, engineering-note overviews, and explicitly named companion standards.
2. **Knowledge content** — concepts, principles, tasks, techniques, competencies, perspectives, lifecycle processes, and domain areas.
3. **Work products** — plans, specifications, models, registers, logs, reports, records, code, configurations, datasets, and evidence packages.
4. **Project tailoring** — which work products apply, their formality, owner, timing, and approval rigor for a given context.

A BOK task output is not automatically a standalone document. Classify each checklist entry as one or more of: plan, specification, model/view, register/log, report, decision/approval record, code/configuration, dataset/evidence, role/competency, or knowledge concept. Flag entries that are presented as documents but are actually concepts, outcomes, or embedded content.

## Read-Only Workflow

### 1. Establish scope and source-of-truth map

Record:

- the exact derived files under audit;
- each corresponding source BOK directory and companion-note directory;
- the claimed edition/version in each file;
- whether the user wants artifacts only or also conceptual coverage.

Resolve advertised source paths against the actual vault before relying on them. Stale link banners are findings, not reasons to stop. If a source file contradicts its own overview, preserve both references and label the contradiction as a source-note issue.

Completion criterion: every audited derived file has a named source file or an explicit “no formal BOK / practice-note source” designation.

### 2. Preserve the no-edit boundary

Use read-only file tools. If the workspace is a repository and the user requests no edits, capture the initial working-tree state when possible and check again at the end. Report pre-existing modifications separately; do not revert, stage, or normalize them.

Completion criterion: no write, patch, delete, rename, formatting, or auto-fix operation has been performed.

### 3. Inventory before deep reading

Extract:

- headings and section structure;
- table entries and priority labels;
- owner/role fields;
- source references and standards claims;
- profile triggers, methodology assumptions, and quick-start counts;
- duplicate names across sections and files.

Use a small deterministic count or comparison script when helpful, but do not use counts as proof of coverage until duplicates and embedded checklists are separated.

Completion criterion: a compact inventory exists for each derived file and each source overview, including counts with a stated counting method.

### 4. Read the source in dependency order

Prefer this order:

1. source overview and scope/structure;
2. lifecycle, process, or knowledge-area index;
3. chapters that define outputs, inputs, artifacts, or tailoring;
4. relevant companion engineering-note overviews and detailed chapters;
5. only then standards or external sources if the user asked for external validation.

For BOKs, compare the derived set against both the named work products and the source’s lifecycle/tailoring guidance. For SWEBOK or engineering notes, inspect requirements, architecture, quality, security, operations, maintenance, configuration management, engineering management, and HCI as applicable.

Completion criterion: every major derived section has at least one source section that supports, limits, or contradicts it.

### 5. Run the five comparison passes

#### A. High-impact omissions
Look for missing controls or work products that affect:

- requirements traceability, verification, validation, and approval;
- transition, migration, training, operations, maintenance, retirement, or benefits realization;
- security governance, accepted-risk accountability, privacy/legal obligations, incident response, and recovery;
- data governance, lineage, metadata, quality, retention, and change management;
- safety, reliability, availability, maintainability, resilience, human-systems integration, and certification evidence;
- architecture decisions, interfaces, configuration baselines, technical reviews, and operational feedback;
- user research, accessibility, usability evidence, and design-to-implementation handoff.

Distinguish “missing from this extract” from “missing from the local source vault.”

#### B. Questionable priorities
For every “Must Have,” ask:

1. Is it universal, or only applicable to a technology/domain/lifecycle/regulatory condition?
2. Does the source call it mandatory, or merely describe it as an output/technique?
3. Can it be embedded in another artifact instead of being a separate file?
4. Does the profile’s stated risk/criticality justify the label?
5. Is the same artifact red in one profile and yellow/absent in another without a rationale?

Use severity language such as “overclassified,” “underclassified,” or “conditionally essential,” not blanket claims that a document is wrong.

#### C. Overlaps and ownership ambiguity
Cluster synonymous or related entries:

- BRD/business requirements/stakeholder needs/SyRS/SRS/user stories;
- risk register/risk assessment/risk treatment/risk report;
- change request/change assessment/change log/MR-PR/ECR;
- system architecture/SAD/HLD/LLD/architecture views/ADR/trade study;
- business glossary/data dictionary/metadata repository/lineage/mapping;
- quality plan/SQAP/QMS/V&V plan/test plan;
- security plan/ISMS/SSDLC/security requirements/threat model;
- SLA/SLO/SLI/operational KPI/monitoring dashboard.

For each cluster, identify the intended level (enterprise, project, system, software, data, security, or evidence) and whether one canonical record should own the others.

#### D. Internal contradictions
Check:

- phase versus process/focus-area terminology;
- lifecycle stage names versus source lifecycle stages;
- “document-only” claims versus code/configuration/model entries;
- “all projects” legends versus tailoring notes;
- profile trigger conditions versus profile title and methodology;
- source counts, checklist counts, and stated document totals;
- duplicated headings or repeated artifacts;
- source-version claims versus chapter structure;
- standard references that are not supported by the local source note.

Report the two conflicting references together; do not silently choose one.

#### E. Scope and terminology
Flag:

- a formal BOK being conflated with an internal practice guide;
- a BOK knowledge area being presented as a document phase;
- task outputs being called files without artifact type or system-of-record semantics;
- “must,” “required,” “compliance,” “conformance,” “certification,” and “recommended” being used interchangeably;
- “architecture,” “design,” “requirements,” “validation,” “acceptance,” “verification,” “quality,” and “security” being used at different abstraction levels without definitions.

### 6. Record evidence at line/section level

Each material finding should contain:

- **Finding:** one precise claim;
- **Impact:** why it matters;
- **Derived reference:** exact file and line/section;
- **Source reference:** exact file and line/section;
- **Classification:** omission, priority, overlap, contradiction, scope, or terminology;
- **Confidence:** high when directly supported by local source text; medium when an interpretation is required;
- **Suggested disposition:** clarify, downgrade, make conditional, merge, add a crosswalk, or leave as a documented source-note inconsistency.

Prefer several strong findings over a long catalog of trivial differences. Rank high-impact safety, security, privacy, legal, operational, traceability, and profile-selection issues first.

### 7. Validate the final report

Before responding:

- verify every cited path and line range was actually read;
- verify count claims state whether they include duplicates or quick-start tables;
- separate source-note defects from derived-file defects;
- state whether any files were written or modified;
- disclose pre-existing dirty-worktree state if it was observed;
- do not claim external standards compliance unless external standards were actually checked.

## Cross-Disciplinary Heuristics

- **BABOK:** Check BACCM, the four requirements classifications including transition requirements, elicitation/confirmation/communication, requirements lifecycle, solution evaluation prerequisites, and the distinction between requirements and designs.
- **PMBOK:** Check value delivery and benefits, seven performance domains, five Focus Areas (not phases), process outputs, procurement as conditional, risk opportunities, resources, status/performance information, and continuous tailoring.
- **SEBoK:** Check actual system lifecycle stages, system-of-interest/context/enabling systems, technical management, decision management, system definition, realization, operations, maintenance, retirement, specialty engineering, human systems integration, and MBSE claims.
- **CyBOK:** Check all 21 knowledge-area mappings, especially law/regulation, human factors, privacy, accepted-risk ownership, secure lifecycle, operations, forensics, identity, distributed systems, and conditional infrastructure controls.
- **DMBOK:** Check the 11 KAs plus supporting chapters on ethics, data science, maturity, organization, and change management; look for scope/roadmap artifacts, data lifecycle coverage, and duplicated glossary/lineage/model artifacts.
- **UX/HCI:** First establish source authority. Then check research planning/evidence, IA/navigation, user flows, design systems, accessibility requirements and testing, usability metrics, analytics validity, and handoff/design QA. Do not assume every project needs every research method or UI artifact.
- **SWEBOK/software-engineering-note:** Check requirements, architecture, design, testing, security, quality, operations, maintenance, configuration management, engineering management, economics, professional practice, and HCI. In profiles, verify that production readiness includes rollback, monitoring, incident/problem management, recovery, and traceability—not only build and deployment files.

## Common Pitfalls

1. **Treating a BOK as a prescriptive document template.** BOKs describe knowledge, tasks, processes, and outputs; apply tailoring before making a file mandatory.
2. **Calling every output a document.** Preserve the difference between a model, register, report, code artifact, configuration, evidence package, and outcome.
3. **Using lifecycle labels casually.** PMBOK Focus Areas are not phases; SEBoK architecture is not a lifecycle stage; HCI research/design/testing loops are iterative.
4. **Accepting red labels without applicability conditions.** HSMs, DPIAs, MDM, dimensional models, safety cases, SLAs, and procurement packages are context-dependent.
5. **Ignoring operational and retirement evidence.** A checklist that stops at deployment is incomplete; include monitoring, incidents, maintenance, migration, disposal, and benefits/outcome review when applicable.
6. **Leaving overlapping artifacts unowned.** Add a canonical artifact and domain-specific views or evidence records instead of duplicating uncontrolled registers.
7. **Trusting stale source banners.** Resolve paths and verify that the advertised edition and source files exist before treating a link as authoritative.
8. **Mixing source contradictions into derived findings.** Report the source-note contradiction separately and do not “fix” it while auditing.
9. **Reporting counts without a counting method.** Deduplicate names and exclude repeated quick-start checklists when comparing profile totals.
10. **Editing during a no-edit audit.** Do not repair links, priorities, or terminology in place; return findings only unless a separate remediation request is made.

## Verification Checklist

- [ ] Every derived file has a mapped source overview/chapter.
- [ ] Source paths and claimed versions were checked.
- [ ] Artifact types were classified.
- [ ] Omissions were checked across lifecycle, safety/security/privacy, operations, maintenance, retirement, and user validation.
- [ ] Priority labels were tested against source tailoring guidance and profile conditions.
- [ ] Duplicate/overlapping artifacts have been identified with abstraction level and ownership notes.
- [ ] Internal contradictions and source-note contradictions are separated.
- [ ] Counts, if reported, include a stated deduplication method.
- [ ] Every high-impact finding has derived and source references.
- [ ] No file was written or modified during the audit.
- [ ] Any pre-existing working-tree changes are disclosed without altering them.
