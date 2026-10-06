# Obsidian/Markdown Template-Set Audit Reference

Use this reference when the audited set lives in an Obsidian vault or a Markdown repository and presents itself as an “essential documents” or “template” collection.

## Reusable audit probes

1. **Inventory the exact scope.** Count all Markdown files in the target folder, then read the overview, each profile, and the authoritative source/index notes. Record line counts, table-entry counts, priority counts, and checklist counts.
2. **Separate catalog from template.** A checklist of document names/descriptions is an inventory, not a reusable template. Look for canonical fields such as ID, purpose, owner, inputs, outputs, status, approver, review cadence, retention, and tailoring conditions.
3. **Resolve two link classes independently.** Obsidian wikilinks may resolve by basename even when literal backtick paths are stale. Resolve `[[...]]` targets against the vault, and separately test every embedded absolute/relative path for existence.
4. **Check profile arithmetic and parity.** Compare overview claims such as “~30 documents” with actual rows. Compare every Quick-Start item with the rows marked Must Have; do not assume abbreviations are equivalent without reporting the naming mismatch.
5. **Build an applicability matrix.** For every priority item, distinguish core practice, artifact form (document, record, code, configuration, dashboard, or tool-managed item), and applicability (universal, common, conditional, domain-specific, or not applicable).
6. **Canonicalize cross-cutting artifacts.** Treat repeated Risk Register, Threat Model, RTM, Data Dictionary, ADR, Runbook, Change Request, and V&V entries as a relationship problem: exact duplicate, parent/subset, lifecycle variant, cross-cutting view, or process versus record.
7. **Audit provenance and standards separately.** Confirm that the cited source note supports the artifact claim, that the reference column’s type matches its heading, and that edition/status is recorded. A column titled “ISO/IEEE Reference” should not silently contain NIST, GDPR, OWASP, MITRE, FIPS, OpenAPI, SPDX, or tool/taxonomy references.
8. **Verify read-only scope.** Before and after an audit, inspect repository status if available. Report pre-existing working-tree changes separately from files changed by the audit.

## Observed evidence pattern from a practical audit

In one vault audit (checked 2026-08), all 113 wikilinks in the target folder resolved, but seven embedded source paths pointed to a nonexistent legacy root. The profile claims were materially lower than the actual inventory: approximately 37, 125, and 215 listed artifacts versus overview claims of about 30, 110, and 150+. The small profile’s 22 red items matched its 22-item quick checklist; medium and large profiles had red/checklist parity and naming omissions. This is a useful pattern: logical navigation can be healthy while provenance paths, profile arithmetic, and checklist completeness remain unreliable.

## Standards-verification examples

Re-check edition/status at the time of the audit rather than trusting copied labels. In the same audit, ISO search results identified ISO/IEC/IEEE 12207:2017 and a newer 2026 entry while profiles cited 12207:2015; ISO/IEC 40500 was explicitly WCAG 2.0 while a profile claimed WCAG 2.1; ISO/IEC 19501 was a legacy UML reference; and IEEE 1012 citations required edition revalidation. Record these as “needs verification” or “mismatch” with official links, not as unsupported absolute claims.

## Report framing

Use an AMBER verdict when the set is useful as a selection guide but not yet trustworthy as an authoritative template baseline. Separate:

- lifecycle and knowledge coverage;
- artifact/catalog structure;
- tailoring and applicability logic;
- profile arithmetic and Quick-Start parity;
- link/path health;
- source and standards governance;
- small-project minimum viability.

Do not edit the vault during an audit unless explicitly authorized; report the exact files and pre-existing status instead.

## Re-audit: verify prior "FIXED" claims mechanically

When the folder contains an earlier audit/review doc claiming fixes were applied ("✅ ALL DONE"), treat each claim as a hypothesis and test it with a script before building on it:

1. Extract every claimed fix into a concrete, greppable assertion (section heading added, citation edition pinned, path replaced).
2. Run one batch script over the whole corpus that checks all assertions at once — e.g. search for the bare citation pattern `ISO(?:/IEC)? 27001(?!:2022)` to find edition-pin rollout gaps, or grep for the stale root path to confirm a path migration.
3. Report claims in three states: **confirmed fixed**, **claimed fixed but incomplete** (with exact file list and occurrence counts), and **open**.
4. Also recompute any index/checklist totals independently (parsed rows vs on-disk files vs stated totals). Self-contradictory totals across a header, a summary table, and the disk are a regeneration candidate, not a patch candidate.

Observed pattern: a quick-model pass claimed "applied :2022 to all 11 files" while 22 occurrences across 16 template files remained bare; stale source paths flagged Must-Fix in an earlier audit were still present in all 7 checklists a month later. Partial-fix claims are the norm, not the exception.

## Example-contamination scan recipe

For template libraries consumed by AI personas (spec-driven workflows), fake example data can be inherited as real project data. Score every file mechanically instead of spot-reading:

- Signals (regex counts per file): concrete dates (`20YY-MM`), currency (`$N`), percentages, domain ID patterns (`US-`, `AC-`, `RSK-`, `NFR-`, `FR-`, `E-` + 2-3 digits), and named-example entities (Acme, Contoso, "Customer Portal", etc.).
- Weighted score, e.g. `dates + money + 2×IDs + 3×named + min(pct,10)`; tier as HIGH (≥15) / MEDIUM (6–14) / LOW (<6). Tune thresholds to the corpus; report the formula so tiers are reproducible.
- Cross-check internal consistency of the worst files: a filled-in example whose summary tables (totals, counts, referenced item IDs) contradict its own body is worse than no example at all.
- Deliver the full per-file table as a dated companion doc in the vault (e.g. `Example-Contamination-Scan-<date>.md`), referenced from the plan doc, so per-file remediation decisions have a worklist.
- Remediation options to grill the owner on: fence one internally-consistent example as a callout, strip to pure `[placeholders]` (safest for AI generation), or decide per-file from the scan tiers.

Also check house diagram conventions in the same sweep (e.g. forbidden `mindmap` Mermaid, hardcoded gantt dates) — these are one-pass regex findings that belong in the same correctness phase.

## Restructure-plan deliverable shape

When the user picks "full restructure" over fix-in-place, produce two vault artifacts and no template edits:

1. **Plan doc** (`<Folder>/Template Restructure Plan - <date>.md`): verified current-state inventory table, open-defect register (RC-nn IDs with file-level evidence), target state, explicit **decisions required** table (D-nn, owner, options, recommendation, which phase each blocks), phased execution with a Mermaid `flowchart LR` dependency diagram (color-coded by priority), Definition of Done checklist, and risks.
2. **Companion data doc**: the machine-generated scan/inventory tables the plan references.

Key framing that worked: answer the "should we purge?" question with scan evidence (e.g. "57% of files are already clean — hybrid upgrade beats blind purge; archive-don't-delete"), and separate scriptable phases (citations, paths, diagrams, frontmatter) from phases blocked on an owner decision, so work can proceed while the vision question is unresolved.

## Scripted remediation sweeps (executing fixes)

When the owner approves a fix phase, execute each defect class as ONE Python batch over the corpus, then re-scan with the same regex until the count is zero — report per-defect before/after counts as the verification evidence, never "applied successfully" alone.

1. **Exclude historical audit/review docs from every sweep.** They are evidence records; their stale citations and old paths must survive verbatim or the audit trail lies.
2. **Citation edition-pin sweep:** regex like `ISO(?:/IEC)?[ /]27001(?!\s*:\s*2022)(?![-\d])` → canonical `ISO/IEC 27001:2022`. The negative lookahead for `-\d` prevents corrupting range citations.
3. **Gantt date placeholder-ization:** do NOT substitute `[YYYY-MM-DD]` inside Mermaid gantt blocks — it breaks rendering. Instead re-base every date to a fixed placeholder epoch (min date in block → `2000-01-01`, all others keep their relative offsets) and inject a `%%` comment after `dateFormat` explaining the convention. The diagram still renders and relative schedule shape survives.
4. **mindmap → flowchart conversion:** parse indentation into a stack; `root((Label))` becomes `R(("Label"))`, each node becomes `nX["Label"]` plus a `parent --> nX` edge to the nearest shallower-indent node. Verify the converted hierarchy by spot-reading one output, not just the mindmap-count rescan.
5. **CRLF diff noise:** on Windows vaults, `git diff --stat` shows thousands of changed lines from line-ending normalization. Confirm the real edit surface with `git diff --ignore-all-space` and per-file diff greps before reporting scope.
6. **Update the plan doc in place after execution:** add a decision-review subsection, flip each defect-register row to ✅ with the verified fix evidence (counts, method), bump version/revision history, and mark superseded steps (e.g. "do not patch index X — regenerate in later phase").
7. **A purge-and-rebuild decision (D1=b style) merges the patch phases into the rebuild:** don't strip contamination in-place on files slated for regeneration — the scan tiers become the rebuild priority worklist instead.
8. **Verify owner decision text against its cited source before recording it.** Owners paraphrase; if a decision names a source file (e.g. a tier model defined in a checklist), read that file and record the verified facts (exact tier names/count), noting any mismatch with the decision wording rather than silently copying either version.

