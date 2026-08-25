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
