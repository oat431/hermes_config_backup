---
name: iso-standards-compliance-review
description: Audit software development document templates against the ISO/IEEE/IEC standards they claim to follow. Verify section structures, identify compliance gaps, and produce structured review reports as Obsidian notes.
tags: [iso, ieee, iec, standards, compliance, audit, document-template, swebok, pmbok, quality]
triggers:
  - "review templates against iso"
  - "check if templates follow ieee standard"
  - "audit document templates for compliance"
  - "verify iso standard alignment"
  - "are these templates iso compliant"
  - "standards review for document template"
---

# ISO Standards Compliance Review

Audit a collection of software development document templates (typically in Obsidian `.md` format) against the formal ISO/IEEE/IEC standards each template claims to follow. Produce a structured review report identifying compliance gaps and recommended fixes.

## When to Use

- User asks to verify whether document templates follow ISO/IEEE standards
- User is building a document template library and wants quality assurance
- User wants to check a specific template (e.g., SRS, SCMP, Test Plan) against its claimed standard
- User wants to know what sections a compliant template must include
- Periodic re-audit after adding new templates or after ISO standard revisions

## Prerequisites

- Target vault path confirmed (typically `swe-knowledge/document-template/`)
- The templates have YAML frontmatter with `standard_ref` fields naming the claimed standards
- The BOK source vault is accessible for cross-referencing (e.g., `body-of-knowledge/`, `software-engineering-note/`)

## Step 1: Map the Template Library

Before auditing individual templates, understand the full scope:

1. **List all template files** — use `search_files(target='files', pattern='*.md')` or `find` via terminal
2. **Read the master checklist** — look for a `TEMPLATE-CHECKLIST.md` or `Essential Documents - Overview.md` that maps templates to BOKs and standards
3. **Extract all unique `standard_ref` values** — grep across all templates to build a list of claimed standards:
   ```bash
   grep -rh "^  - " "<template_dir>/" | grep -iE "(ISO|IEEE|IEC)" | sort -u
   ```
4. **Count templates per category** — understand the distribution of work

## Step 2: Identify Priority Templates

Not all templates need deep review. Prioritize by:

| Priority | Criteria | Examples |
|---|---|---|
| 🔴 Critical | Templates that claim compliance with a **prescriptive** standard (one that defines required sections) | SRS (29148), SCMP (828), Test Plan (29119) |
| 🟡 Important | Templates that reference **process** standards (12207, 15288) — check process traceability, not section structure | Project Plan, Maintenance Plan |
| 🟢 Lower | Templates with only BOK references (no ISO standard) or non-prescriptive standards | Meeting Minutes, Wireframes |

Focus deep review on templates where the standard has an **informative annex with a recommended outline** (29148 Annex C, 828 Annex A, 29119-3 Annex). These have the clearest compliance criteria.

## Step 3: Research the Standards

For each priority standard, determine what a compliant document must contain. Load the reference file:

> **See `references/iso-ieee-required-sections.md`** for pre-researched outlines of 15 major standards including: 29148 (SRS), 828 (SCMP), 730 (SQAP), 1012 (V&V), 29119 (Testing), 42010 (Architecture), 12207, 15288, 31000, 25010, 21502, 27001, 14764, 20000-1, and 22301.

Key distinction when researching:
- **Prescriptive standards** (29148 Annex C, 828 Annex A, 29119-3) — define specific section outlines. Compare section-by-section.
- **Process standards** (12207, 15288) — define processes, not document structures. Check that the template's activities map to the standard's processes.
- **Meta-standards** (42010) — define concepts (stakeholders, concerns, viewpoints) but not a fixed outline. Check that the concepts are addressed, not that specific sections exist.

**Use `delegate_task`** to research standards in parallel while you read templates. Dispatch one subagent to compile the standard outlines while you read template files.

## Step 4: Audit Each Priority Template

For each priority template, create a compliance table:

```
| Standard Section | Template Coverage | Notes |
|---|---|---|
| Required Section A | ✅ Covered / ⚠️ Partial / ❌ Missing | Details |
```

Read the full template file (`read_file`), then compare each section against the standard's required/recommended content.

### Common Compliance Gaps to Check

These patterns appeared across the user's 357-template library and are likely to recur:

1. **Missing acceptance criteria in SRS** — 29148:2018 requires well-formed requirements with acceptance criteria per requirement
2. **Missing CCB in SCMP** — IEEE 828 requires a Configuration Control Board with defined membership and authority
3. **Missing suspension/resumption in Test Plan** — 29119-3 requires explicit criteria for halting and resuming testing
4. **Missing integrity levels in V&V Plan** — IEEE 1012 requires identifying the system integrity level (1-4)
5. **Missing SQA independence in SQAP** — IEEE 730 requires SQA to be organizationally independent from development
6. **Incorrect standard designation** — e.g., ISO/IEC 20000-1 cited as ISO/IEC/IEEE 20000-1 (IEEE was never a co-author)
7. **Outdated ISO 27001 version** — templates may reference the 2013 structure (14 domains, 114 controls) instead of 2022 (4 themes, 93 controls)
8. **42010 "compliance" with 4+1 views** — 42010 does not mandate the 4+1 model; it requires stakeholder→concern→viewpoint→view mapping
9. **Superseded standards** — IEEE 830 (SRS) superseded by 29148; IEEE 829 (test docs) consolidated into 29119-3

## Step 5: Check Cross-Template Consistency

Beyond individual template compliance, verify:

- **Standard reference granularity** — templates should cite both the BOK context AND the formal standard. Flag templates with only BOK references.
- **Version specificity** — ISO references should include the year (`:2018`, `:2022`). Flag bare `ISO/IEC 27001` without version.
- **Standard name accuracy** — verify the standard's official designation (e.g., `ISO/IEC` vs `ISO/IEC/IEEE`)
- **YAML frontmatter consistency** — `tags` should include the standard ID (e.g., `iso-29148`), `standard_ref` should list both BOK and ISO

## Step 6: Write the Review Report

Create the review as an Obsidian note in the template directory. Use this structure:

```yaml
---
tags: [review, iso-compliance, standards-audit, document-template, quality-gate]
created: YYYY-MM-DD
reviewed_scope: "description of what was audited"
standards_checked: "comma-separated list"
---
```

### Report Sections

1. **Executive Summary** — total templates, compliance breakdown (strong/moderate/gaps), critical issues count
2. **Compliance Assessment by Priority Standard** — one subsection per major standard, each with a compliance table
3. **Critical Issues Found** — numbered list of must-fix items with severity
4. **Consistency Issues** — cross-template patterns (naming, versioning, granularity)
5. **Standards Reference Accuracy Audit** — table of verified-correct and needs-correction
6. **Recommendations Summary** — priority-ranked fix list (P1: critical, P2: gaps, P3: consistency, P4: long-term)
7. **Template Quality Scoring** — per-template scorecard (structure / content / overall)

## Step 7: Apply Fixes (Post-Review Repair)

After the review identifies compliance gaps, the user may ask you to fix them. This is a distinct phase from the audit.

### Fix Workflow

1. **Read the full template** — use `read_file` on the target template to understand the current section structure and numbering
2. **Insert missing sections** — use `patch` (mode=replace) to replace the section boundary where new content goes. Anchor on a stable existing heading or the Related Documents block
3. **Renumber subsequent sections** — inserting sections shifts numbering. Grep for `^## ` to list all headings, then patch each shifted number. **This is the most common gotcha** — forgetting to renumber creates duplicate or out-of-order sections
4. **Update YAML frontmatter** — add the standard version to `standard_ref` (e.g., `IEEE 828-2012`) and the standard ID to `tags` (e.g., `ieee-1012`)
5. **Update the template footer** — change the `> **Template Standard:**` line to reference the specific standard version and annex
6. **Verify with grep** — run verification commands to confirm fixes landed (see `references/template-fix-patterns.md` for the verification script)

### Fix Patterns by Gap Type

> **See `references/template-fix-patterns.md`** for ready-to-paste content blocks for each common gap: CCB section, Baseline definitions, Release Management, Integrity Level assignment, V&V lifecycle phase structure, Suspension/Resumption criteria, Staffing/Training, SQA Independence, Supplier Control, Records Management. Each block includes the exact mermaid diagrams and tables to insert.

### Batch Fixes (Global Find-Replace)

For issues that affect multiple files (e.g., incorrect standard designations like `ISO/IEC/IEEE 20000-1`), use `sed -i` via terminal:

```bash
sed -i "s/ISO\/IEC\/IEEE 20000-1/ISO\/IEC 20000-1/g" "<file>"
```

Then verify with:
```bash
grep -rc "ISO/IEC/IEEE 20000" "<dir>" | grep -v ":0"
```

### Updating the Review Document

After applying fixes, update the `ISO Standards Compliance Review.md` report:
- Add ✅ FIXED markers to resolved issues
- Update the Recommendations Summary to mark completed items
- Record what was changed in each fix entry

## Pitfalls

### Standards Knowledge
- **Annexes are informative, not normative** — 29148 Annex C (SRS outline) and 828 Annex A (SCMP outline) are *recommended* outlines, not mandatory. However, they represent the de facto industry baseline. A template that deviates should document why.
- **Process standards don't prescribe templates** — 12207, 15288, and 31000 define processes and guidelines, not document structures. Don't audit these for section compliance; check process traceability instead.
- **Standards get revised** — 25010:2011 → 25010:2023, 27001:2013 → 27001:2022, 15288:2015 → 15288:2023. Always check the current version. Add version years to all references.
- **Some standards are aging** — 14764:2006 is old; many organizations now reference 12207:2015's maintenance process instead. Note this in the review.

### Methodology
- **Don't audit all 357 templates equally** — prioritize the prescriptive-standard templates. Process-standard and BOK-only templates get lighter review.
- **Don't confuse "practical" with "compliant"** — a template can be excellent for working teams but not formally standard-compliant. Note both perspectives.
- **Clean up delegation artifacts** — if you use `delegate_task` for standards research, the subagent may write files to `C:\\Users\\Admin\\`. Clean these up after extracting the content.
- **The research output is a knowledge bank** — when a subagent compiles standard outlines, save that as a reference file in the skill directory so future sessions don't need to re-research.
- **Section renumbering after insertions** — when you insert new sections into a template, all subsequent `## N.` headings shift. This is the #1 gotcha in the fix phase. Always grep `^## ` after insertion and verify sequential numbering. The SQAP had duplicate `## 3` headings and the Test Plan skipped from 7 to 9 before we caught and fixed it.
- **Patch large template sections as one block** — when a template needs many new sections (e.g., SCMP needed 7 new sections), replace the entire region from the insertion point to the Related Documents block in a single `patch` call. Multiple small patches risk merge conflicts on adjacent content.

### Output Format
- **User prefers colons over em-dashes** in Obsidian notes. Use `:` not `—` in prose.
- **User prefers Mermaid diagrams** over ASCII in Obsidian notes.
- **Scoring tables and compliance matrices** render well in Obsidian — use them liberally.

## References

- See `references/iso-ieee-required-sections.md` for pre-researched outlines of 15 major ISO/IEEE/IEC standards: what sections each requires, current versions, and compliance notes. Saves re-researching in every session.
- See `references/common-compliance-gaps.md` for the 9 recurring gap patterns identified during the first audit of the 357-template library, with specific fix recommendations.
- See `references/template-fix-patterns.md` for ready-to-paste content blocks (mermaid diagrams, tables, section structures) for each common fix: CCB, Baselines, Release Management, Integrity Levels, V&V lifecycle phases, Suspension/Resumption, Staffing/Training, SQA Independence, Supplier Control, Records Management.

## Related Skills

- [[obsidian]] — Read, search, create notes in the Obsidian vault
- [[curriculum-vault-authoring]] — Create BOK vault structures (the source vaults these templates are derived from)
- [[obsidian-vault-restructuring]] — Reorganize vault files and fix frontmatter
