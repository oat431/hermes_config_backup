---
name: knowledge-vault-audit
description: Audit a knowledge vault's coverage vs its BOK baseline.
difficulty: senior
created: 2026-08-20
tags: [audit, knowledge-vault, obsidian, body-of-knowledge, coverage, traceability, gap-analysis, wikilink]
---

# Knowledge Vault Audit

> Systematic coverage + traceability audit of an entire Obsidian knowledge vault against its own `body-of-knowledge/` baseline, plus an optional "general knowledge for a human" gap analysis.

## When to Use

- User asks to "audit", "review", or "check if X covers Y" a **knowledge vault** (a folder of many notes with a `body-of-knowledge/` or curriculum baseline).
- User asks "does my vault cover the body of knowledge / curriculum / baseline?"
- User wants a **gap matrix**: baseline concept areas → content files → hit/miss.
- User adds a second axis like "does it also cover *general knowledge for a human*" (beyond the declared baseline).

**Distinguish from `checklist-audit`:** that skill audits *a single checklist/reference document* against a vault KB. This skill audits *the vault itself* against its own declared baseline — a whole-folder coverage/traceability pass over hundreds of notes.

## The Feasibility Gate (do this FIRST)

When the user says "review the vault and tell me if you can really audit this", answer that honestly **before** committing to depth. A vault is genuinely auditable when:

1. **The baseline is machine-traceable** — its overviews enumerate concept areas as numbered tables with `[[wikilinks]]` to concrete note filenames (not prose).
2. **The vault asserts coverage it can falsify** — e.g. "Completion: 19/19 (100%) ✅" is a testable claim.
3. **The two axes separate cleanly** — baseline coverage is objective (curriculum→file mapping); "nice-to-have" is subjective and needs an auditor-defined reference frame.

If the baseline is prose-only (no wikilinks/filenames), say so and propose a different method (manual read) rather than faking traceability.

## Confirm Scope Before Committing (clarify)

The "nice-to-have general knowledge" axis has **no in-vault oracle**. Use `clarify` to pin depth + reference frame:

- **Option A (recommended default):** coverage/traceability audit — filename+topic mapping vs baseline, spot-check a few notes for quality, produce a gap matrix.
- **Option B:** deep audit — read *every* note, verify accuracy/completeness against baseline AND a self-defined general-knowledge reference.
- **Option C:** baseline only — skip the nice-to-have axis.

Also confirm the **audit log location + naming** (user convention: `Audit/knowledge_audit_YYYYMMDD_topic.md`).

## Workflow

### 1. Map the vault structure (cheap, high signal)

```bash
cd "<vault>" && find . -type d -not -path './.git*' -not -path './.obsidian*' | sort
# file counts per top-level folder:
find . -name '*.md' -not -path './.git*' -not -path './.obsidian*' | sed 's|^\./||' | cut -d'/' -f1 | sort | uniq -c
```

Build a **baseline → content** inventory table: each BOK component, its *claimed* concept-area count, its content folder, actual notes found, and a status (✅ exact / 🟡 partial / 🔴 empty). This table alone surfaces the biggest gaps.

### 2. Read the baseline overviews

Read the top `Body of Knowledge - Overview.md` plus each subject overview. They state totals ("~94 concept areas", "Completion 19/19") that you can later falsify.

### 3. Run the traceability script

```bash
python scripts/traceability_audit.py --root "<vault>" --baseline "body-of-knowledge"
```

This extracts every `[[wikilink]]` from baseline files and resolves each against actual content filenames with **normalization** (see below), producing: totals, per-subject missing counts, unique missing targets per subject, and content-file counts per top folder.

### 4. Verify with ground truth — do NOT trust link resolution alone

The script's "missing" list is a *hypothesis*, not a finding. Cross-check against actual filenames:

```bash
ls -1 "<vault>/Social Studies/01 Religion/"   # etc., per subject
```

Link resolution fails on **taxonomy drift** (baseline links to `[[01_Buddha_Biography]]` but the file was renamed to `01_Buddhist_Principles.md`) — coverage may be fine, just *untraceable*. Only `ls` of the real folders tells you whether content is actually missing vs merely renamed.

### 5. Spot-check note quality

Read 2–3 content notes across subjects. Check for: frontmatter (tags/source/course codes), grade-band breakdown, Thai/English terminology tables, worked examples, cross-links. **Separate content-quality from structural-traceability** in the final verdict — a vault can have excellent notes but broken links (or vice versa).

### 6. Run the "nice-to-have" axis (if in scope)

Probe with keyword counts against an auditor-defined reference frame:

```bash
for kw in philosophy "world literature" "current affairs" psychology logic; do
  echo "$kw: $(grep -rli "$kw" --include='*.md' . 2>/dev/null | grep -v '/.git/' | grep -v 'body-of-knowledge' | wc -l)"
done
```

Reference frame for "general knowledge for a human" (define explicitly, since there's no oracle): world history & geography, general science literacy, philosophy & critical thinking, world literature & arts, personal finance, media/information literacy, current affairs, psychology, civic/law literacy. **Flag that this frame is your judgment**, not a vault requirement.

### 7. Write the audit log

To `Audit/knowledge_audit_YYYYMMDD_topic.md`. Structure:
- Executive summary (two-axis verdicts + confidence)
- Inventory table (baseline → content mapping)
- Axis 1 findings (✅ / 🟡 / 🔴 per component, with evidence)
- Traceability & naming defects table
- Axis 2 findings (well-covered vs genuine gaps)
- Findings register (severity-ranked, each with evidence)
- Note-quality assessment
- Recommendations (priority-ordered)
- Verdict

## The Traceability Technique (core)

Wikilink→filename matching requires **normalization** or the gap count is wildly inflated:

- Strip a leading numeric prefix (`01_`, `13 `) from target basenames.
- Replace `_` and `-` with spaces, collapse whitespace, lowercase.
- Strip trailing `\` from `[[Name\]]` artifacts.
- Skip navigation links (contain "Overview" / "ภาพรวม", or end in `\`).

A naive match on raw link text produced 363 "unresolved"; normalization dropped the true count to 151; ground-truth `ls` showed most of those were renames, not missing content. **Always run all three layers (raw → normalized → ground-truth) before concluding anything is a gap.**

## Pitfalls

- **Don't report "missing" from link resolution alone** — taxonomy drift (baseline reorganized after content was renamed) produces false gaps. Confirm with `ls`.
- **Don't conflate "untraceable" with "missing"** — they need different fixes (rename/redirect vs author new content).
- **Beware stale `Vault:` path directives** in baseline overviews — they frequently point to non-existent folders (e.g. `Thai\` vs actual `ภาษาไทย\`). List them as traceability defects.
- **Distinguish content quality from structure** — excellent notes can sit behind broken cross-links; don't let broken links imply thin content.
- **The "nice-to-have" axis has no oracle** — state your reference frame as auditor judgment and let the user correct it.
- **Don't audit content you were told is out of scope** — `career/`, `checklist/` folders may sit outside the baseline; classify them, don't score them against it.
- **Feasibility first** — answer "can you really audit this?" before diving in; a prose-only baseline isn't machine-traceable.

## Related Skills

- `checklist-audit` — audits *a checklist/document* against a vault KB (narrower, different target). The two overlap on the findings-register + severity formatting; consolidation candidate.
- `obsidian` — reading/searching/editing notes in the vault (the raw file primitives this audit builds on).
