---
name: knowledge-vault-scaffolding
description: Scaffold vault folders + tracker overviews from a BOK.
tags: [obsidian, vault, body-of-knowledge, scaffolding, overview, tracker, cs2023, markdown-parsing]
---

# Knowledge Vault Scaffolding

> Generate the notes-tree scaffold from a machine-readable `body-of-knowledge/` (BOK): one folder per knowledge area (KA), a `00_overview.md` tracker per KA listing sub-topics as future numbered notes, group-level index files, and README wiring. This is the **inverse** of `knowledge-vault-audit` / `obsidian-vault-audit` — those check coverage of an existing tree; this builds the tree from the baseline (e.g. CS2023, SWEBOK).

## When to Use

- User finished a BOK (one .md file per KA, frontmatter + Knowledge Units section) and asks to "create a folder for each group/KA with an overview tracking sub-topics".
- Extending an existing vault with a new specialist area whose BOK is complete.
- Reference pattern to mirror: `swe-knowledge/software-engineering-note/NN_Area/Area Overview.md` (Files table → numbered notes).

## Workflow

### 1. Survey before writing
Map the vault (`find`/`ls` the BOK dir and group dirs), read ONE BOK file end-to-end, and read the exemplar overview file the user pointed at. Do not parse-and-generate blind — the bullet formats vary and the overview shape is user-defined.

### 2. Clarify the tracker design FIRST (one `clarify` call, 3 questions)
Pin these before generating anything — they change every file:
- **Sub-topic tracking format** — this user's confirmed choice: a markdown table per KA: `| File | Knowledge Unit | KU Code | Focus | Status |` where File is a wikilink `[[NN_Name]]` to a future numbered note, Focus is a one-sentence extract from the BOK, Status starts ⬜ with legend line `⬜ not started · 🟨 draft · ✅ done`.
- **Granularity** — use the formal baseline units (CS2023 Knowledge Unit codes like `AI-Search`, `DM-Relational`), not ad-hoc clusters or the finest sub-bullets.
- **Group-level indexes** — yes: `<group>/00_Overview.md` with a table linking each KA overview (Knowledge Area | Abbr | #KUs | Purpose) plus folder list.

### 3. Parse the BOK programmatically, dump to JSON, verify counts per file
Extract per KA: title, abbr `(XX)` from H1, `source:` frontmatter, purpose blockquote, Knowledge Units (code/name/desc), Essential Concepts, Related KAs. Cache the parse to a scratch JSON in `$LOCALAPPDATA/Temp` (native tools can't read `/tmp`), regenerate from it — never re-parse on every fix pass. Print units-per-file with codes and flag empty/no-code/dup parses immediately; a count of 0 on a file that visibly has bullets means the parser is wrong, not the file.

**BOK bullet formats actually encountered in one vault (all must parse):**
- `- **Name (AI-Search):** desc` — code inside bold, colon-terminated
- `- **GIT-Fundamentals: Fundamental Concepts** — desc` — code-first inside bold, em-dash
- `- **PDC-Programs** — desc` — bold is ONLY the code; give it a human name via an explicit override map of bare codes
- `- **NC-Fundamentals — Fundamentals** (CS Core)` with content in nested `  - ` sub-bullets — pull focus from the first sub-bullet, render tier as trailing `*(CS Core)*`

### 4. Generate, then run an independent audit script
Write all overview + index files from the JSON with `newline="\n"` (see pitfalls), then re-read every generated file with a SEPARATE check: row count == parsed unit count, 5 cells per row, wikilink cell matches `^\[\[\d\d_`, code cell matches `` `[A-Z]{2,4}-[A-Za-z0-9-]+` ``, status == ⬜, focus ≥ 15 chars and not tier-only, group-index links resolve to real files. Clean up scratch files from the vault dir; append group-index links to the vault README.

## Pitfalls — parsing (each cost real time here)

- **When a regex returns 0 matches against a literal that `repr()` proves is present, stop tuning the regex — switch to plain string ops** (`line.startswith("- **")`, `line.find("**")`, slice on `":**"`). The string-op parser worked on all 17 files; the regex mysteriously failed on some in the same interpreter. Diagnose once with hexdump/repr to confirm what's really on disk, then hand-roll.
- **Marker order varies**: format A ends bold with `:**` before the desc while other formats use `** —`; matching `\*\*:\*\*` when the text is `:**` yields silent zero-count. Extract the bold span FIRST (split on `**`), then parse name/code out of it.
- **Character-class em-dash ranges**: `[—-:]` is an invalid range (— is > -) and raises `bad character range`. Put the literal dash last or escape it.
- **f-strings are Python 3.11 here**: no backslash inside f-string expressions — precompute `chr(10).join(...)` into a variable.
- **CRLF bites rewrites**: files written by the generator ended up CRLF, so a later `content.index("| File ...\n|---...\n")` block-replace failed with substring-not-found. When patching generated tables, split on `\n`, locate rows by index, rejoin with `newline="\n"`.

## Pitfalls — verification (suspect the auditor first)

- **A prefix filter on numbered rows must cover double digits**: checking `line.startswith("| [[0")` reports 9/12 rows for any KA with ≥10 units and looks like 7 generator failures. Use regex `^\| \[\[\d\d_`. When an audit flags a SUBSET of files in a way that correlates with item count, audit the audit before regenerating anything — here all 7 "failures" were auditor bugs and the files were correct.
- **Fix the generated output only for real defects** (bare-code names, tier-marker-only focus cells, missing sub-bullet content); regenerate the whole table for a file rather than line-patching it.
- **Cross-check totals**: tracked rows across all overviews must equal the summed parsed unit count; report both numbers in the final answer.

## Output conventions (this user)

- KA folder = BOK filename minus numeric prefix, kebab-case: `01_Artificial_Intelligence.md` → `applications/artificial-intelligence/`.
- Tracker wikilinks are forward-looking (`[[01_Fundamental_Issues]]` with NO stub files until the user asks) — the table IS the backlog.
- Each overview: frontmatter tags → H1 `Title — Overview` → `> **Source:** [[../../body-of-knowledge/<group>/<bok>|...]]` backlink → `## What Is This?` (purpose, strip `(Source: ...)` tails) → sub-topics table → `## Key Ideas (from the BOK)` (top ~5 Essential Concepts) → `## Related Knowledge Areas` (carried from BOK). Unwrap wikilinks to plain text and strip `**`/backticks from extracted text before embedding in table cells — pipes break cells.
- Deliver one sample overview as a MEDIA: card and offer format tweaks; note upstream BOK format inconsistencies to the user as a QA observation (standardizing source formats makes future audits cheaper).

## Related Skills

- `knowledge-vault-audit` / `obsidian-vault-audit` — the check side of the same vault ecosystem; reuse their wikilink normalization and `broken_links.py` after scaffolding to prove every emitted link resolves.
- `obsidian` — raw note CRUD and basename-resolution semantics.
