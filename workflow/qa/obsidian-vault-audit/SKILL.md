---
name: obsidian-vault-audit
description: Audit an Obsidian vault vs a BOK baseline; fix broken links.
difficulty: senior
created: 2026-08-20
tags: [obsidian, vault, audit, traceability, wikilink, backlink, gap-analysis, knowledge-base]
---

# Obsidian Vault Audit & Backlink Repair

> Audit a knowledge vault against its own `body-of-knowledge/` baseline (coverage/traceability), then repair broken wikilinks and naming drift. QA-flavored, Obsidian-mechanics-heavy.

## When to Use

- User asks to "audit" a knowledge vault, "check coverage" against a body-of-knowledge baseline, or "fix the taxonomy / backlinks / broken links".
- User wants a coverage report (baseline concept areas → content notes → hit/miss) for a vault like `general-knowledge` or `swe-knowledge`.
- User wants broken wikilinks repaired after a vault reorg.

## Core Concept: two audit axes

1. **Baseline coverage** — does each concept area in `body-of-knowledge/` have a corresponding content note? Build a traceability matrix (baseline item → content file → hit/miss).
2. **Link-graph health** — do all `[[wikilinks]]` resolve? Split failures into **taxonomy drift** (note exists under a different name) vs **genuine gap** (note missing). Only drift is repairable; gaps get *flagged*, never fabricated.

## Workflow

### 1. Map structure
```bash
find <vault> -name '*.md' -not -path '*/.git*' -not -path '*/.obsidian*' | sort
```
Exclude `.git/` and `.obsidian/`. Note the baseline dir (usually `body-of-knowledge/`) vs content dirs.

### 2. Extract & resolve wikilinks
Run `scripts/broken_links.py` (see below) — it already encodes the correct parsing + resolution rules. It reports broken links by top folder and, with `--collisions`, the dangerous normalized-name collision groups.

### 3. Classify findings
| Class | Meaning | Action |
|---|---|---|
| 🔴 Gap | target note does not exist | flag as missing content, do NOT create on a coverage-only pass |
| 🟡 Drift | note exists under a different name | remap link (below) |
| 🟢 Strong | covered + filename-matched | leave alone |

### 4. Repair drift (only if user asked to fix)
- Remap each broken link's target to the correct note, **preserving the original name as an alias** so reading-paths stay valid: `[[Correct_Note|Old_Name]]`.
- Rename drifted **folders** with `git mv` (keeps history), not `mv`.
- Fix stale **prose** paths (e.g. `Vault: `Physics\``) in overview files.
- Re-scan and confirm remaining broken links are all genuine gaps.

### 5. Report
Write `Audit/knowledge_audit_YYYYMMDD_topic.md` with: inventory, coverage matrix, findings register (severity-ranked), note-quality spot-checks, and a "Remediation Applied" section if you fixed anything.

## Pitfalls (learned the hard way — read before ANY bulk edit)

1. **Escaped pipe in markdown tables.** Obsidian renders `[[note\|alias]]` inside tables with an escaped pipe. A naive `\[\[(.*?)\]\]` parse reads the target as `note\` and mis-flags it broken. ALWAYS unescape `\|` → `|` before splitting target/alias.

2. **Obsidian resolves by BASENAME, not path.** `[[../../Arts/Arts - Overview]]` and `[[Fundamental/01_Scientific_Method]]` are valid if a note with that basename exists *anywhere* in the vault. A broken-link check must compare the **basename (case-insensitive)**, never the full path. (The `obsidian` skill documents this too.)

3. **Normalization-collision corruption (the big one).** If you auto-remap by stripping number prefixes and normalizing `_`/`-`/space, distinct notes collide: `17_Probability`↔`19_Probability`, `04_Human_Body_Systems`↔`13_Human_Body_Systems`, `09_Sound`↔`17_Sound`. An unguarded pass will silently *flip valid links* and corrupt files you never meant to touch. **Guard:** only rewrite a link when its target basename does NOT exist in the vault; never rewrite a valid link. Run the `--collisions` report FIRST and build an explicit file-scoped or target-scoped map for every collision group.

4. **Use git as the safety net.** On a git-tracked vault, always verify with `git diff` after a bulk edit, and know you can `git reset --hard HEAD` (destroys uncommitted changes — get user approval) to revert a bad pass cleanly before re-applying correctly.

5. **BOK overviews often enumerate a finer taxonomy than content actually holds.** The overview may list 18 concept areas while content has 8 consolidated notes. That's not "18 missing notes" — remap the fine-grained links to their consolidated parent note and note the consolidation in the report rather than fabricating 10 files.

## Support Files

- `scripts/broken_links.py` — re-runnable vault wikilink scanner (broken-link report + `--collisions`). Run before and after any repair.
- `references/naming-drift-playbook.md` — concrete drift patterns observed (space↔underscore, number-prefix drift, fine-grained→consolidated remaps) that recur across vaults.

## Related Skills

- `checklist-audit` — audits a single checklist/reference document against vault KBS (sibling class; document-level, not vault-level). Note overlap: both produce severity-ranked findings tables; a future curator may want to unify under one "audit" umbrella.
- `obsidian` — filesystem-first note CRUD (bundled; documents basename-resolution semantics).
