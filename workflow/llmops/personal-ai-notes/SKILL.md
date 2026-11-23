---
name: personal-ai-notes
description: "Use when writing notes for Panomete's personal AI vault."
version: 1.0.0
author: LLMOps
license: MIT
metadata:
  hermes:
    triggers:
      - "write a note"
      - "note for me"
      - "personal/ai"
      - "add to the AI notes"
    related_skills: [note-plaintext-cleanup]
---

# Personal AI Notes (Panomete's vault)

Write notes into `F:\obsidian_note\oralita_md\personal\ai\` (git repo) matching the established house style. Used for the Applied-AI knowledge series (applied concepts, frameworks, tools, security).

## When to Use

- User asks for a note / write-up "for me" about AI/LLM topics
- Follow-up deep dives on the AI tooling landscape
- Retrofit existing notes: see skill `note-plaintext-cleanup` for the character cleanup procedure

## Series Numbering (`personal/ai` is now a numbered series)

The folder is a **numbered reading series**, modeled on `personal/meta-learning/`. Rules:

- Files are `NN_kebab-case.md`, in reading order: `00_overview.md`, then `01_` .. `NN_`.
- `00_overview.md` is the front door: frontmatter, "The chain" mermaid flowchart, a `# | Note | The question it answers` table, "Why this order", "How this series works", "Candidate notes (a menu, not a plan)", "Knowledge connections", "Key takeaways".
- Every note carries the tag **`ai-series`** so the series is searchable via `#ai-series`.
- There is **no conclusion note, by design** - the field churns, so the series ends at a moving edge. Say this out loud in the overview instead of writing a fake conclusion.
- New notes **append** as the next number, after `NN`; they never renumber existing files.
- Backstage notes (vault proposals, reading lists) go at the **end**, since they document the making of the knowledge base rather than the knowledge.

**To add a note:** pick the next number, write it, add the `ai-series` tag, then wire it into `00_overview.md` (chain diagram + notes table + connections) and cross-link the nearest sibling. Verify with a link-resolution check that every `[[target]]` stem exists.

**To reorder or renumber (rare, invasive):** use `git mv` (never plain `mv`) so `git log --follow` keeps history, then rewrite every wikilink target with an exact-match dict (`re.sub(r"\[\[([^\]\|#]+)", ...)`), including links from **outside** the folder - `personal/note/modern-ai-agents-with-hermes.md` references these notes, including one GitHub blob URL. Then re-run the link check.

## House Style (all mandatory)

- **Characters**: no em-dash, en-dash, arrows, box-drawing, math symbols. Use ` - `, `->`, `!=`. **KEEP emojis** (user likes them: ✅🟢🟡🔴⚠️🦙 and section markers). Plain ASCII + Thai + emoji.
- **Filenames**: lowercase-hyphen, include year when churn-prone (`ai-tools-landscape-2026.md`).
- **Frontmatter**: `title`, `date`, `author: LLMOps 🦙`, `tags`, `status: living`.
- **Opening blockquote**: `> **Your question:** ...` / `> **Short answer:** ...` / `> **Verification:** web-checked YYYY-MM-DD ...`.
- **Structure**: numbered sections, tables, TL;DR/verdict tables, honest status labels (✅ Standard / 🟢 Emerging / 🟡 Niche), "Skeptic's corner" for caveats, "Related notes", "Sources (web-verified YYYY-MM-DD)", footer `*Authored by LLMOps 🦙, DATE. ...*`.
- **No "Thai Speaker Traps" section** - user removed it from all notes in this folder (2026-09-30). Do not add it back. (Still used in the teaching vaults, just not personal/ai.)
- **Cross-links**: `[[lowercase-hyphen-name]]` wikilinks to sibling notes; cross-vault references as inline code paths (they don't resolve across vaults).
- **Commands**: explain what each does (user convention: explain every command).

## Workflow

1. Web-verify facts first (search + read primary sources); cite with verification date. Tooling/policy facts churn - never cite from memory alone. Note: the `web_extract` tool fails on a SearXNG-only backend ("search-only backend and cannot extract URL content") - read pages with the searxng MCP tool `mcp__searxng__web_url_read` instead, using `startChar`/`maxLength` to page through long articles and `section` to pull one heading.
2. Check the folder for existing notes to cross-link.
3. Write the note with write_file.
4. Patch a companion line into the closest sibling note (keeps the graph connected).
5. Verify: run a character scan (Python: flag non-ASCII outside Thai 0E00-0E7F, emoji ranges 1F000-1FAFF / 2600-27BF / 2B00-2BFF / 2300-23FF, FE0E/FE0F/200D; check wikilink targets exist). Fix any hits.
6. The folder is a git repo - mention that the user can review with `git diff` before committing.

## Pitfalls

- Em-dash sneaks back in via copied text - always run the scan after writing.
- Em-dashes also sneak in through TABLE CELLS: using "—" as an "absent/not applicable" marker is the easiest way to fail the scan. Use `no` (or an emoji already allowed) instead.
- After editing, validate markdown tables programmatically (cell count per row) - a stray pipe silently breaks the whole table in Obsidian.
- Thai text must stay intact (it is content).
- Do not strip emoji - that was a user correction (2026-09-21); emojis stay.
- Prefer `execute_code` scans WITHOUT subprocess calls (subprocess can trigger consent prompts); do git status via terminal tool instead.
