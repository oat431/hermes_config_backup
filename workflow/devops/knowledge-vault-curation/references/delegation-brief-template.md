# Subagent Brief Template — Batch Note Authoring

One subagent per 2–4 notes in the SAME folder (shared samples/style). Every brief must contain:

1. **Role line**: "You are writing study notes in an Obsidian vault for a senior DevOps engineer's knowledge base." Note if the folder follows a textbook (e.g. Computer Organization follows Hennessy & Patterson) — that changes the register from cheatsheet to academic-deep.
2. **Sample files** (2 per brief, absolute paths, MUST be read first): pick the best-styled existing notes in the target folder.
3. **Style rules** (copy from SKILL.md "Writing new notes" section verbatim, plus folder-specific frontmatter tag list and line-count range observed in samples).
4. **Per note**: exact output path + a detailed content outline — sections to cover and the must-include facts/commands/comparisons (spelled out, not "cover TLS well"). The outline is where the parent's domain knowledge goes; the child executes style + prose.
5. **Cross-links**: list the existing sibling note names the child should wikilink to.
6. **Verification step**: "After writing, verify each file by reading back its first 5 lines. Report paths + line counts."
7. **Anti-hallucination**: "`## Sources` with real RFCs/books/man-pages only — never invent citations. Factually accurate as of the current year."

Parent-side follow-up after results land:
- Re-run the per-folder `wc -l`/`wc -w` inventory to confirm counts match reports.
- Spot-read 1–2 notes per child fully (children self-report success; trust but verify).
- Update folder Overview notes + master `Computing Foundation Overview.md` coverage table yourself — don't delegate index edits (multiple children would conflict on the same file).
