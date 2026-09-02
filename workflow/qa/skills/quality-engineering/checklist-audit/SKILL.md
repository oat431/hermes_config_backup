---
name: checklist-audit
description: Audit checklists against vault knowledge bases
difficulty: senior
created: 2026-08-06
tags: [checklist, audit, review, vault, knowledge-base, gap-analysis]
---

# Checklist Audit

> Systematic review of checklists, reference documents, and guides against authoritative vault knowledge bases to identify gaps, strengthen items, and ensure cross-reference consistency.

## When to Use

- User asks to "audit", "review", or "check" a checklist or reference document
- User wants to verify a document against their vault (SWEBOK, CyBOK, career paths, etc.)
- User wants to identify gaps, missing items, or outdated guidance in a structured document
- The document has sections, checklists, tier matrices, or sanity checks that need verification

## Audit Workflow

### 1. Read the Target Document

```bash
read_file(path="<target-checklist-path>")
```

Understand the document's structure, purpose, audience, and existing cross-references.

### 2. Gather Vault References in Parallel

Read all relevant knowledge base files that could inform the audit. Use `terminal` with `find` if directory structure is unclear:

```bash
find "F:/obsidian_note/swe-knowledge/career-path/<domain>" -name "*.md" -type f | sort
```

Batch reads in parallel for efficiency. Target:
- Career path overviews and capability notes for the domain
- Relevant Body of Knowledge chapters (SWEBOK, CyBOK, DMBOK, SEBoK)
- Any existing specialist notes that cover the same territory

### 3. Compile Structured Findings

Create a findings table:

| # | Finding | Source | Severity | Location |
|---|---------|--------|----------|----------|

Severity levels:
- 🔴 **Gap** — Critical missing item that violates authoritative source
- 🟡 **Improve** — Existing item needs strengthening or clarification
- 🟢 **Nice-to-have** — Optional enhancement
- ✅ **Already Strong** — Leave unchanged

### 4. Apply Patches Systematically

For each finding, use `patch` tool with `mode=replace`:

1. **Add new items** at appropriate section with clear rationale
2. **Strengthen existing items** — expand wording, add context
3. **Update section titles** if they no longer reflect content
4. **Maintain numbering** — keep sections sequential, no gaps

### 5. Update Tier Matrix

If the document has a tier applicability matrix:
- Add rows for new sections
- Update column entries to reflect new items
- Ensure row numbers match actual section numbers

### 6. Update Sanity Checks

Add items for each new critical section item. Keep concise (10-15 items max). Each sanity item should map to a section item.

### 7. Verify Cross-References

Check:
- Section numbering is sequential (no gaps)
- Internal references (§X) point to correct sections
- Tier matrix rows match actual sections
- External references ([[Release]], [[API Launch]]) still valid

### 8. Final Verification Read

```bash
read_file(path="<target-checklist-path>")
```

Confirm all patches applied correctly and document is internally consistent.

### 9. Compile Summary Report

Provide before/after metrics, changes summary (✅ added, 🟡 improved, 🟢 untouched), cross-reference verification results, and final verdict with risk reduction statement.

## Pitfalls

- **Don't add redundancy** — if an item is already covered, strengthen the existing item, don't duplicate
- **Don't over-audit** — if a section is already strong, leave it alone
- **Don't break cross-references** — when adding items or renumbering, verify §X references still work
- **Don't inflate sanity checks** — focused subset (10-15 items), not a parallel list
- **Don't ignore tier matrices** — if the document has one, you MUST update it
- **Don't invent authoritative sources** — only cite vault files you actually read
- **Patch text must match exactly** — re-read sections before patching to avoid whitespace/mismatch errors

## Examples

### QA Checklist Audit (2026-08-06)

**Target:** `checklist/qa-checklist/qa.md`
**Vault refs:** 18 files from `career-path/10_Quality_and_Test_Engineering/` + SWEBOK Testing chapter
**Key gaps closed:** Systematic test design, exploratory testing, shift-left, test oracles, regression strategy, RCA
**Result:** 152 → 172 lines, added §7 Exploratory Testing, strengthened §1 with shift-left

### Security Checklist Audit (2026-08-06)

**Target:** `checklist/security-checklist/security.md`
**Vault refs:** Security Engineer overview, CyBOK Software Security, CyBOK Secure SDL, QA Security Testing note
**Key gaps closed:** CSRF, TOCTOU/race conditions, error leakage, IaC scanning, remediation SLAs, crypto API misuse, security champions, abuse cases, hallucination mitigation
**Result:** 203 → 222 lines, 11 → 17 sanity items, full OWASP Top 10 coverage verified

## Folder Expansion Workflow

After auditing a checklist, check if its folder follows the vault pattern: **general checklist + technology-specific companions**. If the folder has only the general checklist, recommend expansion.

### Identifying Expansion Candidates

1. List all checklist folders: `find "F:/obsidian_note/swe-knowledge/checklist" -type d`
2. Count files per folder — folders with 3+ files have the pattern (e.g., `api-checklist/` has `api.md` + `fastapi.md`, `spring-boot-api.md`, etc.)
3. Folders with only 1 file are expansion candidates

### Creating Technology-Specific Checklists

Use `delegate_task` with `tasks` array (max 3 per batch due to `max_concurrent_children=3` limit). Batch remaining tasks in subsequent dispatches.

Each technology checklist should include:
- Setup & installation (language-specific package managers, dependencies)
- Core concepts and lifecycle
- Common patterns with real code examples
- CI integration
- Quick sanity check (10-15 items)
- Tier applicability matrix (7 tiers matching vault convention)
- Cross-references back to the general checklist

### Delegation Pattern

```
Batch 1: delegate_task(tasks=[task1, task2, task3])  # max 3
Batch 2: delegate_task(tasks=[task4, task5, task6])  # next 3
...
Final items: write_file directly if subagents can't write
```

**Pitfall:** Subagents may report "cannot write files" in sandboxed environments. If so, use their detailed output as content and `write_file` directly.

### Recommended Checklist Set by Domain

| Domain | General | Technology-Specific Companions |
|--------|---------|-------------------------------|
| QA | `qa.md` | pytest, jest-vitest, junit, go-test, playwright, cypress, k6-performance, testcontainers, mutation-testing, accessibility-testing |
| API | `api.md` | Framework-specific (already populated) |
| Database | `database.md` | Engine-specific (already populated) |
| Web | `web.md` | Framework-specific (already populated) |

## Related Skills

- `dogfood` — Exploratory QA of live web apps (different: audits documents, not running systems)
- `spec-driven-code-review` — Code review against specs (different: audits checklists, not code)
- `requesting-code-review` — How to request reviews (different: performs audits, not requests them)
