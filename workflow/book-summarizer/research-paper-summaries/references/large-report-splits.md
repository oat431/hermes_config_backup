# Large Reports → Numbered Sets

Pattern for splitting a big technical report into a numbered set of study notes in a
subfolder of `daily-paper/`. Confirmed with the user on a 59-page open-model technical
report whose results and appendices were roughly half the page count.

## Decision rule

- Up to ~25–30 pages → one file (the skill default).
- Large report (60+ pages, or results/appendices ≈ half the page count) → numbered set.
- In between → ask; show the split table and let the user pick.

## The split the user prefers for technical reports

Content files (methods and story) + one tests file + an overview:

| File | Role |
|---|---|
| `00_Overview.md` | MOC: lineup table, headline numbers, file map, reading paths (fast orientation, practitioner path, evaluation-first, source order) |
| `01_..` / `02_..` / `03_..` | Content in the report's own order: method and story sections; each may state headline numbers but points to the tests file for full evaluation detail |
| `04_Evaluation.md` | THE tests file: all formal evaluation material consolidated — main-body benchmark tables, appendix benchmark breakdowns, human evaluation (win rates + a few representative cases, not the full output gallery), qualitative case studies |

- One writer for the whole set (voice consistency); no delegation for a 4–6 file set.
- Not split into files: Related Work / survey sections and the reference list; cover them at one line or skip, and record the decision in the manifest, not in the notes.
- Sample-output galleries (multi-page response comparisons) condense to: the evaluation structure, the win/loss pattern, and representative cases with page cites.

## Cross-linking

- The set is one folder in the vault, so wikilinks resolve inside it: `[[01_Pretraining]]`; cross-folder navigation uses a path form (`[[qwen-technical-report/00_Overview]]`).
- The overview links every file; each content file links the overview and its siblings; keep a `Related` line in the tests file pointing back.
- When a companion paper's summary lands elsewhere in the vault, link both directions and keep the manifests in sync (see the sibling-linking pitfall in SKILL.md).

## Verification for sets

- Run the checker once per file against that file's extract slice.
- Pass `--allow-links` with the set's canonical stems so hallucinated links fail the gate.
- Promote all files in one operation; hash every staged/vault pair; update each manifest row.
