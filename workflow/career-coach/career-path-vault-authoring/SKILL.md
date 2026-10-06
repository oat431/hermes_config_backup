---
name: career-path-vault-authoring
description: Use when adding or editing career paths in swe-knowledge.
---

# Career Path Vault Authoring

How to extend `F:\obsidian_note\swe-knowledge\career-path\` — the career-path map and its capability-area notes — correctly on the first try.

## Vault layout

- Paths are numbered folders `NN_Title/`, each with a `00_overview.md`; filled paths add capability-area folders (`0N_Area/`), each holding `00_overview.md` + 6–7 numbered topic files (7 is the current standard: 7 areas × 8 files + path overview = 57 files per path).
- `00_Career_Path_Overview.md` is the map: family table, mermaid graph, exploration-directions bullets.
- Format exemplars — READ FIRST and mirror exactly:
  - Area overview: `09_Data_and_ML_Engineer/06_ML_Lifecycle_and_MLOps/00_overview.md`
  - Topic file: `09_Data_and_ML_Engineer/06_ML_Lifecycle_and_MLOps/01_Experiment_Tracking_and_Reproducibility.md`
- Full frontmatter schemas and section order: `references/career-path-note-formats.md`.
- AI source notes for cross-links: `computing-foundation-note/Artificial_Intelligence/` (files 01–13).

## Add a new path

0. Decide only after evidence, and build only after the user green-lights. Admission test: real hiring demand (search postings and pay data for the role, not just blog enthusiasm), a capability model genuinely distinct from the nearest existing paths, and enough substance for a full path (~57 files). Roles adjacent to an existing path are usually absorbed as area notes instead (e.g. a developer-experience variant living inside the platform path); pure org-chart roles (director, VP) are skipped. When the title barely exists in the user's local market, say so plainly — the path is a capability compass and interview language, not a local job-board play — and still recommend on global evidence. Present "full path" vs "a few notes inside an existing path" and let the user choose.

1. Prove the gap first: read the nearest existing path's `00_overview.md` and write the boundary into the new path's "What This Path Is" — never create a path that duplicates an existing center of gravity (e.g., AI Engineer vs Data/ML Engineer: owns products built ON models vs the data/platform that trains them).
2. Ground external sources before citing: web-search that they exist. Emerging paths have no BOK — say so plainly and cite real references (OWASP LLM Top 10, practitioner books) instead of pretending BOK grounding.
3. Create `NN_Title/00_overview.md` by cloning the newest completed path's root overview (formats evolve; the latest exemplar carries the current frontmatter keys such as `note_type`, `career_family`, `level`, `entry_from`, `next_paths`, `source_frameworks`) and keeping the same section order: positioning quote, What This Path Is, Primary Outcomes, Capability Areas table, progression mermaid, Signals for Moving Forward, Evidence to Build, Nearby Paths, Suggested Future Note Route, Sources, Related.
4. Wire the map (`00_Career_Path_Overview.md`): add to the specialization-directions bullet, add a family-table row, add a mermaid branch (quoted labels, `-->` only). While editing, audit the WHOLE family table and graph for completeness — earlier additions can leave an existing path with no row or no branch — and for unescaped wikilink pipes. When more than a couple of rows need repair, rebuild the entire table block in one edit (one row per path, columns `| Family | Path | Main question | Overview |`, every alias `\|`-escaped) instead of patching row-by-row, and report every repair.
5. Cross-link both ways from the nearest paths' "Nearby Paths" and "Related" sections.
6. Grep the vault for hard-coded path counts ("N paths") and update any found.
7. If capability-area folders do not exist yet, mark them "planned" in the overview table — never link to wikilink targets that do not exist.

## Deep-fill capability areas (contract-first, parallel subagents)

Full-path standard shape: 7 capability areas × (1 area overview + 7 topic notes) + 1 path overview = 57 files.

1. **Write every area `00_overview.md` yourself first** — these are contracts, not delegation output. Each locks: frontmatter (`role`, `capability_area`, ISO `created`/`updated`, kebab tags), a "Topics in This Capability Area" table naming every topic's EXACT filename + core skill, one mermaid, a role-vs-previous-level "What Changes" table, a `## Practical Applications` checklist, pitfalls, success indicators. Writers create topic notes only — never overviews. Topic-table wikilinks must byte-match the filenames you give the writers (comma/article variants break resolution; verify after the fill).
2. **Patch the path-level `00_overview.md`**: replace the capability table's external vault anchors with links to the new area overviews (`[[0N_Area/00_overview]]`).
3. **Delegate topic notes in 3 waves (14 + 14 + 21 files)**, one subagent per 1–3 areas (max 3 concurrent). Each brief self-contained: the style contract (frontmatter schema, `> **Core skill:**` one-liner, ONE mermaid with double-quoted labels and `-->` only, `## Practical Applications` checklist and/or fenced template, 3-column pitfalls table with 4–7 rows, 4–6 success bullets, Related Topics, 6–13 KB, no emoji); exact topic filenames; an ALLOWED WIKILINK whitelist of real targets (the specific Senior/TL/Staff/EM/Architect notes that exist — writers must not invent links); "DO NOT edit any file outside your assigned folders"; exemplar paths to read first; instruct writers to lock each note's `> **Core skill:**` line to the contract's topic-table row, forbid invented statistics or case studies, and keep governance, legal, and regulated content principle-based (no fabricated rates or legal specifics). Before dispatch, run the resolver over the whitelist itself — every target must resolve against the vault on disk; 0 broken is the gate, because a whitelist of invented or stale targets is exactly how broken links enter a fresh path.
4. **Dispatching is a tool call, not an announcement.** A turn that says "dispatching now" must contain the `delegate_task` call — otherwise the user comes back to "I only see the overviews". If the user reports that state: the contracts and path patches are already done, so dispatch immediately.
5. **Voice:** role-comparison tables ("Tech Lead vs Engineering Manager"), leadership/team/organizational angle — the personal-skill angle defers to the Senior path via links (Senior owns the craft, the new path owns the scope). Principle-level over tool-level; English; dense tables.
6. **Verify after the waves return** with the bundled checker (`obsidian-vault-builder` → `scripts/verify_vault_fill.py`): per-area counts, wikilinks under Obsidian semantics (case-insensitive, suffix match), mermaid arrows, frontmatter, size floors (overviews ≥4 KB, topic notes ≥5 KB — never apply the note floor to overviews). Subagent self-reports are not verification. Also re-check neighboring completed paths' counts and spot byte-sizes: writers occasionally touch files outside their assignment — verify any claimed revert instead of trusting it. A sweep taken between contract-writing and wave completion shows exactly `areas × topics` unresolved links (the fresh contracts' topic tables pointing at notes the writers have not created yet) — match the count exactly instead of treating it as damage; it should reach 0 once the waves return.

## Pitfalls

- Escape wikilink pipes inside tables: `[[path\|alias]]` — an unescaped `|` splits one cell into broken columns. Legacy rows in the map's family table are unescaped and render mangled; repair them as one reported whole-table rebuild (see "Add a new path" step 4) — never silent row-by-row edits.
- Never invent wikilink targets. Use vault-root-relative links (`[[career-path/18_Applied_AI_Engineer/00_overview|Applied AI Engineer]]`); bare `[[00_overview]]` only inside the same folder.
- Cite only externally verified URLs — a fabricated reference in a teaching vault is worse than none.
