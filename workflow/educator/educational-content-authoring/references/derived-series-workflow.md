# Derived Note Series from an Existing Vault (cheat sheets, playbooks, digests)

Workflow for condensing an existing note collection into a NEW derived series (e.g. a `Cheat_Sheet/` folder distilling `Fundamental/` + `Advance/` notes into merged rulebooks chained zero-to-practical).

## Steps

1. **Inventory + sample**: `search_files` for *.md in the source tree; read 2-3 representative notes (one per subfolder) to learn frontmatter shape, Thai/English mix, section conventions.
2. **Scope interview (grill-me frontier rounds)**: one `clarify` call bundling the independent decisions, each with a recommendation first:
   - Which topics count as in-scope (where does the series stop)?
   - One note per source topic vs merged rulebooks (users often prefer merged: ~5-6 thematic rulebooks)?
   - Content density: rules-only vs rules + short examples?
   - Language: English primary with native terms for rule names?
   - Structure: new subfolder, numbered files, index with mermaid progression map, prev|next chain footer?
3. **Parent writes the index first** (`00_Index.md`): mermaid chain diagram, table of rulebooks with coverage + level, how-to-use, chain-navigation stub. This locks the file names the subagents must link.
4. **Dispatch one subagent per output note**, each brief containing the SAME shared format spec verbatim:
   - Explicit absolute paths of ALL source notes to read (children cannot discover them).
   - Exact output path for `write_file`.
   - Frontmatter shape with `sources:` wikilinks to every source note.
   - Per-rule structure: the rule, one SHORT worked example, one-line *When to use:* hint. Exclude grade bands, long glossaries, essays, multi-step word problems.
   - Native-language copy rule: copy Thai strings character-exact from sources, never generate from memory.
   - Exact chain-navigation footer (`⬅ [[prev]] · ➡ [[next]]`).
   - LaTeX (single backslash, `$$...$$` own lines), mermaid conventions (quoted labels, `&#40;`/`&#41;`), colons-not-em-dashes, target line range.
   - An `output_schema` requiring output_path, line_count, sections, artifact_check.

## Parent QA gate (never trust child "all checks pass" self-reports)

Children routinely ship broken wikilinks, em-dash violations, and source-inherited artifacts while claiming PASS. Run one mechanical `execute_code` pass over the whole output folder:

- **Encoding artifacts by codepoint, not by eye**: the Thai artifact ความ (คว + SARA AA U+0E32 + MO MA) is visually near-identical to correct ความ (SARA AM U+0E33). Detect via unicodedata/codepoint comparison; fix with literal replace. If found in output, grep the SOURCE corpus too: children copy faithfully, so the artifact often originates in the user's existing notes. Fix the derived files, then report the source contamination to the user before touching sources.
- **Fabricated-native-text check**: extract every Thai run (`[\u0E00-\u0E7F]{2,}`) from each output and require it to appear in the concatenated source corpus. Unmatched tokens are either invented terms, composite header phrases (benign), or artifacts (fix).
- **Format**: no `\\\\[a-zA-Z]` double-backslash LaTeX, balanced `$$` count, balanced code fences, frontmatter starts `---`, em-dash count outside H1/tagline (convert ` — ` -> `: ` per user style).
- **Wikilink resolution**: every frontmatter `sources` link and in-body wikilink must resolve to a real file on disk. Common child failure: dropping the subfolder prefix (`[[12_Geometry_Shapes]]` instead of `[[Fundamental/12_Geometry_Shapes]]`). Auto-fix by building a basename -> subfolder map from the source tree and rewriting frontmatter with a regex.
- **Chain integrity**: each file's Chain Navigation footer contains exactly the expected `[[prev]]` and `[[next]]`; the index links every member; dead in-body links (e.g. `[[Mathematics]]` when no MOC note exists) get converted to plain text.

## Lessons

- Give children the file list; do not make them glob. Children told to "find the source notes" pick wrong or partial sets.
- Lock chain-link file names in the index BEFORE dispatching so every child's footer uses exact names.
- A child's programmatic self-check is still a self-report: it validates what the child thought to check, not the parent's gate criteria. Re-run everything centrally.
