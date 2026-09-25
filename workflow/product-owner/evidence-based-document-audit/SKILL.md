---
name: evidence-based-document-audit
description: Use when auditing document sets against standards.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, document-audit, evidence, standards, swebok, traceability]
    related_skills: [privacy-regulatory-research, hermes-agent-skill-authoring]
---

# Evidence-Based Document-Set Audits

## Overview

Use this skill to audit a proposed “essential,” “required,” or “standard” document/artifact catalog against an authoritative body of knowledge, standards, and a local knowledge directory. The deliverable is an evidence-backed report, not a rewritten catalog: identify omissions, over/under-prioritized items, duplicates, and weak or incorrect attributions with file paths and line references.

The central distinction is **knowledge coverage versus mandated work products**. A body of knowledge normally describes concepts, processes, inputs, outputs, practices, and tools; it rarely mandates one universal set of standalone documents. Treat any “essential” label as a claim that must be tested against lifecycle context, system criticality, methodology, team scale, regulatory obligations, and whether the artifact can be represented in a tool rather than a separate file.

## When to Use

Use when the user asks to:

- audit an artifact/document inventory against SWEBOK, a standard, a framework, a policy, or a local knowledge base;
- find missing categories, incorrect priorities, duplicates, or unsupported citations;
- review a “required documents” checklist without editing it;
- produce a concise report with evidence and line-level references.

Do not use this for ordinary proofreading, a source summary, or requirements elicitation unless the user is explicitly auditing a catalog.

## Workflow

### 1. Establish the audit boundary

Record the exact target file, authoritative source files, local-note directory, and whether edits are prohibited. Treat the target as read-only. Identify whether “document” includes code, tests, configuration, records, dashboards, and tool-managed data; if the catalog mixes them, call that out rather than silently normalizing it.

Completion criterion: the report can name every audited root and the target’s line range or table-entry count.

### 2. Inventory the target structurally

Read the target with line numbers. Extract section headings, table rows, labels, priorities, descriptions, and source/standard columns. Count entries by priority. Normalize labels only for analysis; preserve the original wording and line references in the report.

Look for:

- rows that are activities, methods, tools, code, configurations, records, or reports rather than documents;
- conditional labels such as Agile, OOP, safety-critical, regulated, or production;
- repeated labels, parent/subset relationships, and cross-cutting rows that subsume phase-specific rows;
- claims that the catalog is “SWEBOK-derived” or “essential for virtually all projects.”

Completion criterion: every finding points to an exact target row or an explicitly documented absence in the relevant section.

### 3. Build a source-to-artifact map

Read the source overview first, then the relevant knowledge-area chapters and local detailed notes. Extract source concepts in four buckets:

1. **Processes and activities** — e.g., requirements validation, change control, incident management.
2. **Inputs and outputs** — e.g., baselines, test results, release packages, audit evidence.
3. **Techniques and models** — e.g., ATAM, UML, FMEA, QAW, TDD.
4. **Context qualifiers** — e.g., safety-critical, service operation, Agile, large system, formal CM.

Do not infer a required standalone document merely because a source mentions an artifact. Verify whether the source says it is an output, a recommended record, a tool-managed item, or only an example.

Completion criterion: each major lifecycle/knowledge area has at least one source citation and a comparison against the target.

### 4. Identify missing categories

Search for omissions in these common classes:

- concept and feasibility: vision/scope, business case, feasibility, proposal/contract;
- planning/control: scope baseline, estimate basis, cost/schedule baselines, status reports, decisions, measurement plan;
- requirements governance: requirements baseline, backlog/release allocation, issue/TBD register, review record, CCB charter;
- product delivery: user/install/training/support documentation, deployment package, build manifest, release-readiness evidence;
- testing and quality: test policy/strategy, environment record, execution/incident log, summary report, V&V report, quality gates, CAPA, assurance case;
- operations/support: operations plan, service reports, incident/postmortem, problem/known-error records, service desk, recovery rehearsal;
- maintenance/retirement: transition plan, data migration, archive, decommissioning;
- security: security plan, risk assessment/acceptance, incident response, posture and dependency-compliance reports;
- process and organizational improvement: process tailoring, measurement repository, retrospective/lessons-learned, improvement plan.

Use “missing as a named category” when an existing broader row may contain the content. Do not claim a concept is wholly absent if the source material or target contains it under another name.

### 5. Audit priorities using context, not intuition

Start from the target’s own priority definition. For each Must Have, ask:

- Is the underlying activity essential, or only the separate document name?
- Is it applicable to virtually all projects, or only to a system type/lifecycle/domain?
- Can it be represented by an SRS, backlog, repository, issue tracker, CI system, or dashboard?
- Does the source explicitly require it, or merely mention it as an example?

Flag **over-classification** when a conditional artifact is marked universal: formal architecture packages, ADRs/4+1 views, SBOMs, UAT sign-offs, SLAs, DR plans, FCA/PCA, QMS, formal V&V, and security reports are common examples. Flag **under-classification** when a source calls something a core activity/output but the catalog marks it Optional/Nice, such as requirements baselining, status accounting under formal CM, or recovery evidence for an in-scope production service.

Prefer a three-axis recommendation when possible:

- **Core practice:** generally expected activity;
- **Artifact form:** separate document, record, tool-managed item, or generated report;
- **Applicability:** universal, common, conditional, or domain-specific.

### 6. Detect duplicates by relationship, not just exact text

Classify overlaps as:

- **Exact duplicate:** same concept and scope under two headings;
- **Parent/subset:** e.g., test suite contains test cases; SAST is a security subset of static analysis;
- **Lifecycle variant:** same artifact at requirements, design, implementation, or maintenance scope;
- **Format/content duplicate:** ADR and design rationale, release notes and VDD, API contract and API reference docs;
- **Process versus record:** incident-management process versus incident record/postmortem;
- **Cross-cutting view:** one end-to-end RTM versus phase-specific traceability views.

Recommend a single canonical category with scope/type fields instead of deleting useful distinctions.

### 7. Verify source and standard attributions

For each citation, check four things:

1. **Scope:** does the standard govern this artifact or only a neighboring process?
2. **Edition/status:** is the cited edition current, withdrawn, superseded, or unspecified?
3. **Type:** is it an international standard, IEEE standard, framework, specification, taxonomy, regulation, tool, or book?
4. **Local support:** does the cited source file actually mention or support the attribution?

Common errors include using a quality model as a report template, an ISMS standard as a SAST/security-architecture standard, an architecture-description standard as an ADR-format standard, an open-source compliance standard as an SBOM standard, or a generic UML citation without a version. Separate columns for `Source/KA`, `Artifact standard`, `Framework/taxonomy`, and `External practice` are preferable.

Completion criterion: every “incorrect” attribution is supported either by the authoritative standard’s stated scope or by a clear mismatch between the target citation and the local source text.

### 8. Write the report, not a replacement catalog

Use this compact structure:

1. **Scope and headline finding** — roots audited, entry count, major pattern.
2. **Missing categories** — grouped by lifecycle/knowledge area, with source and target references.
3. **Priority errors** — over-classified, under-classified, and context-dependent items.
4. **Duplicates/overlaps** — original rows plus recommended relationship.
5. **Source/standard corrections** — precise citation issues and evidence.
6. **Files changed** — explicitly say none when the audit was read-only.
7. **Tooling issue** — mention only if it materially affected the method; describe the workaround, not a permanent refusal.

Keep conclusions proportional to evidence. Use “not named,” “overlaps,” “weakly supported,” or “conditional” where absolute claims would overstate the comparison.

## Common Pitfalls

1. **Treating SWEBOK as a mandatory document template.** SWEBOK is a body-of-knowledge map; distinguish generally accepted practice from project-specific work-product choices.
2. **Counting a separate file as the essential thing.** The essential thing may be traceability, change control, testing evidence, or operational knowledge, represented in a tool or combined document.
3. **Using absence as proof without checking aliases.** Search for synonyms such as vision/scope versus BRD, status report versus dashboard, postmortem versus RCA, and deployment package versus release artifact.
4. **Calling every overlap a duplicate.** Preserve useful lifecycle or scope distinctions; report parent/subset and process/record relationships.
5. **Applying a standard outside its scope.** Verify whether it defines a process, a data format, a quality model, an ISMS, a review framework, or an artifact template.
6. **Ignoring conditional rows.** Reclassify by applicability instead of forcing one universal priority.
7. **Citing a local summary as if it were the primary standard.** Identify whether the note is a paraphrase, a book-derived practice, or the actual authoritative publication.
8. **Replacing the requested audit with edits.** The user asked for evidence; do not modify the catalog unless explicitly requested.
9. **Overstating current-edition facts.** Include the edition/year and status when the claim depends on currency.

## Obsidian/Markdown Template-Set Audits

When the target is an Obsidian vault or Markdown repository, apply the additional probes below:

- Treat the folder name `document_template` as a claim to test: distinguish a document catalog/checklist from actual reusable templates with metadata and lifecycle fields.
- Resolve Obsidian wikilinks and literal backtick paths separately; a healthy wikilink graph does not prove that embedded filesystem paths are current.
- Compare profile counts and Quick-Start checklists against the priority-marked rows. Report both true omissions and abbreviation/naming mismatches.
- Build an applicability matrix that separates core practice, artifact form, and context (universal, common, conditional, domain-specific, or not applicable).
- Reconcile overview/index counts and scope claims across the source corpus before treating extracted labels as authoritative.
- Check repository status before/after a read-only audit so pre-existing working-tree changes are not attributed to the audit.

See `references/obsidian-template-audit.md` for a reusable probe sequence, evidence patterns, and standards-verification examples.

## Verification Checklist

- [ ] Target file, source roots, and read-only scope are stated.
- [ ] Target entries are counted and priority totals are grounded in inspection.
- [ ] Every major finding has a target path/line and a source path/line where possible.
- [ ] Missing categories distinguish absent names from absent concepts.
- [ ] Priority findings distinguish core practice from standalone artifact and applicability.
- [ ] Duplicate findings identify exact, parent/subset, lifecycle, or process/record relationships.
- [ ] Standard attributions are checked for scope, edition/status, and type.
- [ ] External authoritative links are included only for disputed/current standard facts.
- [ ] No files were edited or created unless the user explicitly authorized it.
- [ ] The final report is concise enough to scan but specific enough to reproduce.

## Supporting References

- See `references/swebok-artifact-audit.md` for a condensed source map, artifact-category checklist, and standard-attribution traps from a completed SWEBOK audit.
