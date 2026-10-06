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

## Re-audit lesson: verify prior "fix" claims

When re-auditing a library that carries an earlier audit or review doc claiming fixes, treat every "✅ FIXED" claim as unverified. Machine-check each one (grep for the corrected string, count occurrences across ALL files, not the count the review doc asserted). A quick-model pass commonly claims "all N files fixed" while a fraction remains — cite counts from a fresh scan, never from the earlier report.

## Example-contamination scan method (spec-driven template libraries)

When AI personas consume templates, fully-worked fictional example data is contamination: personas can inherit fake IDs/totals as real. Scan every template with regex signals and score:

| Signal | Pattern sketch |
|---|---|
| Concrete IDs | `(US\|AC\|RSK\|DEF\|TC\|CR\|OBJ\|NFR\|FR\|E)-\d{2,}` |
| Money | `$\d[\d,]*[KMB]?` |
| Dates | `20xx-xx-xx` |
| Filled percentages | `\d{1,3}(\.\d+)?%` |
| Named examples | Acme, Customer Portal, persona/company names |

Score = dates + money + 2×IDs + 3×named + min(%,10); tiers HIGH ≥15 / MEDIUM 6–14 / LOW <6. Save the full per-file table as a dated scan doc beside the library — it becomes the rebuild worklist and the before/after evidence. Keep a scan-history table (baseline vs post-fix counts) in the doc.

Scanner limits: it cannot distinguish method content from fake data, so a file scoring HIGH purely on scoring-matrix weights, `$0` baseline semantics, or threshold prose is a documented policy exception, not a defect. Review remaining HIGH files by hand before declaring the band closed.

### Strip-vs-keep rules (D3 policy: strip to placeholders, no fenced examples)

Strip (filled example data): worked register rows, named example items, filled money/date/percent cells, false summary totals, fully-worked multi-item sections (reduce to ONE bracketed skeleton per section, `-[XX]`/`$[X]`/`[YYYY-MM-DD]` pattern placeholders).

Keep (method content): ID-format specifications (`Format: TC-NNN`), scoring-matrix criterion weights, probability/impact scale definitions, threshold rules in prose, formulas (NPV/ROI), `[e.g., ...]` guidance cells, frontmatter, citations, footers, wikilinks.

Mechanics: quote every Mermaid label containing brackets (`["FR-[XXX]"]`) — unquoted brackets break the parser; preserve per-file CRLF/LF; after bulk edits run a structural integrity sweep (frontmatter present, code fences balanced, 0 mindmaps) across the whole library.

## Standing rebuild decisions (document_template library, F:\obsidian_note\swe-knowledge)

Decided by the Founder 2026-09; recorded in `Template Restructure Plan - 2026-09-23.md` §3.1:

- **D1 = purge & rebuild** (option b): contaminated/schema work merges into the rebuild; strip-first keeps the library safe for AI consumption meanwhile; archive-don't-delete (`99_Archive/` + git).
- **D2 = 7-tier maturity model** replacing Small/Medium/Large: 🧪 POC → 🔧 Prototype → 🏠 Internal Tool → 🟢 Small Prod → 🔵 Medium Prod → 🟣 Production Grade → 🔴 Mission-Critical. Source of truth: `checklist/release-checklist/release.md`. Phase 4 maps each template to its minimum required tier and regenerates the master index from disk.
- **D3 = strip to placeholders everywhere**; examples generated on demand by agents, never shipped in templates.
- **D4 = alias-first overlap resolution** (`canonical_name`/`aliases`/`source_of_truth` frontmatter); merges deferred until tier mapping clarifies ownership.

Phase 1 (correctness sweeps: 27001:2022 citations, stale source paths, mindmap→flowchart, gantt dates→2000-01-01 placeholder epoch with offsets preserved) and Phase 2 (HIGH-band strip, 49 files) are complete and verified; Phase 3 (v2 frontmatter schema + rebuild) is next.

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

A five-person safety-critical project may require more evidence than a fifty-person internal prototype. The Founder's 7-tier model (see standing decisions above) is this vault's chosen maturity axis.

## Source-path verification

For local Obsidian vault work:

1. Resolve the actual vault root before reading files.
2. Search the target folder and source folders using concrete Windows paths.
3. Check literal `F:\...`/`C:\...` references separately from wikilinks.
4. Prefer vault-relative links or a central source registry over hard-coded machine paths.
5. Report stale paths as correctness findings, not merely formatting issues.
6. When repointing a stale banner path, verify the new target exists on disk before writing the replacement.

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
- Exclude historical audit/review docs and the restructure plan doc itself from bulk sweeps and contamination worklists — they are evidence records that quote the defects they track.

## Session-specific tool note

On Windows, some file-search helpers may translate `F:` to an unavailable `/f` mount. Prefer concrete Windows paths with `read_file`/`terminal` when that occurs, and treat the workaround as a path-resolution detail rather than a permanent tool limitation.
