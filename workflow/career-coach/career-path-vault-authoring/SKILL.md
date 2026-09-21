---
name: career-path-vault-authoring
description: Use when adding or editing career paths in swe-knowledge.
---

# Career Path Vault Authoring

How to extend `F:\obsidian_note\swe-knowledge\career-path\` — the career-path map and its capability-area notes — correctly on the first try.

## Vault layout

- Paths are numbered folders `NN_Title/`, each with a `00_overview.md`; filled paths add capability-area folders (`0N_Area/`), each holding `00_overview.md` + 6 numbered topic files.
- `00_Career_Path_Overview.md` is the map: family table, mermaid graph, exploration-directions bullets.
- Format exemplars — READ FIRST and mirror exactly:
  - Area overview: `09_Data_and_ML_Engineer/06_ML_Lifecycle_and_MLOps/00_overview.md`
  - Topic file: `09_Data_and_ML_Engineer/06_ML_Lifecycle_and_MLOps/01_Experiment_Tracking_and_Reproducibility.md`
- Full frontmatter schemas and section order: `references/career-path-note-formats.md`.
- AI source notes for cross-links: `computing-foundation-note/Artificial_Intelligence/` (files 01–13).

## Add a new path

1. Prove the gap first: read the nearest existing path's `00_overview.md` and write the boundary into the new path's "What This Path Is" — never create a path that duplicates an existing center of gravity (e.g., AI Engineer vs Data/ML Engineer: owns products built ON models vs the data/platform that trains them).
2. Ground external sources before citing: web-search that they exist. Emerging paths have no BOK — say so plainly and cite real references (OWASP LLM Top 10, practitioner books) instead of pretending BOK grounding.
3. Create `NN_Title/00_overview.md` with the same sections as an existing overview: positioning quote, What This Path Is, Primary Outcomes, Capability Areas table, progression mermaid, Signals for Moving Forward, Evidence to Build, Nearby Paths, Suggested Future Note Route, Sources, Related.
4. Wire the map (`00_Career_Path_Overview.md`): add to the specialization-directions bullet, add a family-table row, add a `SENIOR --> ...` mermaid branch.
5. Cross-link both ways from the nearest paths' "Nearby Paths" and "Related" sections.
6. Grep the vault for hard-coded path counts ("N paths") and update any found.
7. If capability-area folders do not exist yet, mark them "planned" in the overview table — never link to wikilink targets that do not exist.

## Deep-fill capability areas (parallel subagents)

- One subagent per capability area; each writes exactly 7 files (`00_overview.md` + 6 topics) inside its own folder. Instruct every agent: DO NOT edit any existing file.
- Give each agent: the two exemplar paths to read first, exact topic filenames, frontmatter values (kebab-case `capability_area` and `career_path`), hard scope boundaries versus sibling areas (who owns what — eval metrics vs security guardrails vs cost engineering overlap badly without them), and source-note paths.
- Voice: senior-level contrast ("A mid-level engineer X; a senior Y."), principle-level over tool-level (frameworks churn — tools appear only in comparison tables), English, dense tables + bold-led "In Practice" principles + numbered "Practical Exercise".
- After agents return: verify every file (count, line counts, frontmatter), spot-check that wikilinks resolve, then add the area wikilinks into the path overview's capability table yourself.

## Pitfalls

- Escape wikilink pipes inside tables: `[[path\|alias]]` — an unescaped `|` splits one cell into broken columns. Legacy rows in the map's family table are unescaped and render mangled; write NEW rows escaped and offer to fix old rows rather than silently rewriting.
- Never invent wikilink targets. Use vault-root-relative links (`[[career-path/18_Applied_AI_Engineer/00_overview|Applied AI Engineer]]`); bare `[[00_overview]]` only inside the same folder.
- Cite only externally verified URLs — a fabricated reference in a teaching vault is worse than none.
