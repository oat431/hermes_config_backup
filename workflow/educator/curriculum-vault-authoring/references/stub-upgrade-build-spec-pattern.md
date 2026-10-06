# Stub-Upgrade Build-Spec Pattern (BOK Vault Continuation)

Use when a BOK vault has content-rich "stub" notes that fail the vault's own quality gate (e.g., a spec like `CLAUDE.md` requiring `source: "Textbook, Ch N"` frontmatter). The stubs have real prose, tables, and code but lack the spec-mandated fields. This pattern upgrades N stubs to deep notes in parallel without losing the stubs' good content.

## When to Use

- A vault built by another AI agent (Claude, Codex) has a foreign spec file (`CLAUDE.md`, `AGENTS.md`) at its root defining the deep-note quality gate
- Stub notes exist on disk but the roadmap/tracker says "0 deep notes" — the spec's gate defines what counts, not file count
- 10+ stubs need the same set of deltas applied uniformly

## Procedure

1. **Read the foreign spec file first** (before any notes). It defines: the note model (reference vs lesson), the quality gate (frontmatter fields, required sections, word-count floor), the textbook mapping, and the formatting rules. Obey it; do not impose the SOUL's lesson format.
2. **Read the roadmap/tracker and trust its status field.** A roadmap row saying "0 deep notes" can be accurate even when N note files exist on disk. Do not "fix" the count by reclassifying stubs as done.
3. **Diagnose stubs against the spec's quality gate.** Read 2-3 stubs and 1 gold-standard deep note from the same vault (the pilot KA). List the specific deltas between stub and spec (missing frontmatter fields, wrong H1 format, missing sections). These become the upgrade work items.
4. **Reconcile the working tree.** Run `git diff HEAD` (not just `git status`) to distinguish real content changes from line-ending normalization noise — on Windows, `git status` can flag files as modified when only CRLF/LF differs. If the diff is empty, the tree is clean.
5. **Write a build spec** to the scratch directory. The spec must contain:
   - The exact upgrade deltas (numbered, with before/after examples)
   - Hard formatting rules (colons not em-dashes in prose, LaTeX single backslash, Mermaid not ASCII, no exercises/quizzes)
   - A textbook mapping table (file → source frontmatter value) derived from the spec's §7
   - The workflow (read each stub, overwrite in place, one write_file per note immediately)
   - The QA gate (what to check after all notes are written)
   - Assignment of specific notes to each child subagent
6. **Dispatch parallel subagents** sized per the Subagent Sizing section below. Each child reads the build spec first, then reads and overwrites its assigned stubs. Group CS Core tier notes first (they need more depth).
7. **Write the KA overview yourself** while subagents run. It does not depend on the deep-note contents. Match the gold-standard KA overview structure from the pilot KA (frontmatter, Source+Texts lines, What Is This, Knowledge Units table, Topic Map Mermaid, Reading Paths, My Notes, Related Knowledge Areas, Coverage Map, Gaps to Fill).
8. **QA gate after batch completion** (run programmatically in `execute_code`):
   - All N files present
   - All deltas applied (title: frontmatter, source: frontmatter with named textbook not BOK, H1 renumbered to `# NN · Title`, Source blockquote with "approximate" line, Key Takeaways section, Related section)
   - No CJK / Devanagari / Vietnamese script slips
   - No self-correction traces ("... no: X", "(corrected", "PLACEHOLDER")
   - No double-backslash LaTeX
   - Mermaid syntax clean (closed fences, valid diagram type, no trailing-pipe on timeline lines)
   - Em-dash calibration (see below)
   - Word counts within the spec's floor (e.g., 1,000-4,000; CS Core toward upper end, non-core toward lower)
9. **Update the roadmap/tracker**: flip the KA row from "0 deep notes / 0%" to "N deep notes / ~100%", update the phase tracker, update the port-map row if applicable, update the last-analyzed date.
10. **Commit** with a conventional-commit message listing the KA, note count, and tier coverage.
11. **On user review, flip 🟨 → ✅.** When the user says "reviewed" or "good work", apply the status flip in three places: (a) the roadmap KA row, (b) the KA overview's Knowledge Units table (all rows for that KA), and (c) the KA overview's Coverage Map table. Use `patch` with `replace_all=true` for tier-based flips (e.g., replace all `| CS Core | 🟨 |` with `| CS Core | ✅ |`), then handle any remaining individual 🟨 cells. Verify with `grep -c '🟨'` returning 0 before committing. The flip is two commits: one for the upgrade, one for the review.

## Em-Dash Calibration (QA Gate Pitfall)

The em-dash QA grep is the most common false-positive source. The user's colons-over-em-dashes preference applies to **prose sentences in body text**, not to these structural contexts:
- Frontmatter `source:` lines (citations use em-dashes: `Sebesta 12e — Ch 12`)
- Blockquote citation lines (`> **Source:** Text — Ch N`)
- Code comments (`// Reverse — O(n) time`)
- `## Related` link descriptions (`[[link]] — how it connects`)

**Calibration baseline:** the user's approved AL (Algorithmic Foundations) pilot averages ~14.5 em-dash lines per note (669 total across 46 notes), mostly in code comments and Related link descriptions. The user did not flag these. A blanket `grep -c '—'` that counts all em-dashes will flag every note as a violation. Instead, exclude frontmatter, blockquote citations, code blocks, and Related sections from the grep before counting.

## Creating NEW Notes (vs Upgrading Stubs)

When the KA has NO existing stub files (all ⬜ not started), the same build-spec-then-dispatch pattern works, but the children CREATE files instead of overwriting. The build spec's "What NOT to Do" section changes from "do not create new files" to "do not overwrite existing files — these are NEW notes." The QA gate, em-dash calibration, status flip, and commit flow are identical.

## Subagent Sizing

- 20-22 notes → 4 subagents (6+5+5+6 or similar)
- 10-15 notes → 2 subagents (5+5 or 6+5)
- 5-9 notes → 2 subagents (3+2, 5+3, or 5+4) — parallelism still helps because each note is 1,500-4,000 words of dense content; 1 subagent serializes the writes and stalls the parent
- Group CS Core tier notes together in the first subagent(s) — they need more depth (2,500-4,000 words). Non-core notes go in later subagents (1,000-2,500 words).
- For a KA with tiered word-count targets (e.g., one 20h unit at 3,000-4,000 words and four smaller units at 1,500-2,500), put the big note alone or with one sibling in the first subagent, and the rest in the second.

## Cross-Vault Bridge Notes (When a Sibling Vault Holds the Deep Content)

When a KA in the target vault has a corresponding sibling vault that already holds deep SWEBOK/professional-BOK content (e.g., cs-knowledge's SE KA vs swe-knowledge's 410 SWEBOK notes), do NOT duplicate the sibling's depth. Instead, write **CS2023-framed bridge notes** that:

1. **Cover the CS2023 KU topics at overview level** — the concepts, not exhaustive depth. The foreign spec's textbook mapping (e.g., Sommerville 10e Ch N) is still the `source:` frontmatter.
2. **Include a `## SWEBOK Cross-Reference` section** in each note — a table mapping CS2023 topics to the sibling vault's folders, with folder paths and note counts:
   ```markdown
   ## SWEBOK Cross-Reference
   
   This KU maps to SWEBOK v4 knowledge areas in the sibling vault
   [`swe-knowledge`](https://github.com/oat431/swe-knowledge):
   
   | SWEBOK Area | swe-knowledge Folder | Notes | Relevance |
   |---|---|---|---|
   | [Area] | `software-engineering-note/[NN]_[Area]/` | N | [how it connects] |
   ```
3. **Link the sibling vault's GitHub URL in `## Related`** — each note's Related section ends with the repo link, and the KA overview's header block carries it prominently.
4. **The KA overview notes the relationship explicitly** — add a `### Relationship to swe-knowledge` subsection under `## What Is This?` explaining that these are bridge notes, not duplicates.

This pattern keeps the two vaults connected without duplication. The sibling vault is the canonical home for SWEBOK-depth; the target vault is the canonical home for CS2023-framed coverage. Use the same build-spec-then-dispatch-subagents workflow — the only difference is the build spec instructs children to include the SWEBOK Cross-Reference section and the GitHub link rather than writing full-depth content.

**When to use this vs full-depth notes:** use bridge notes when a sibling vault already covers the domain at depth AND the user explicitly says "just cover the note from the overview is okay" or similar. When the user wants full depth in the target vault, write standard deep notes from the named textbooks.

## What NOT to Do

- Do NOT create new files — only overwrite existing stubs at their current paths.
- Do NOT use "CS2023 BOK" or the coverage-map source as the `source:` frontmatter — use the named textbook from the spec's mapping.
- Do NOT leave self-correction traces or placeholder text.
- Do NOT impose the SOUL's lesson format (audience_level, hands-on-project, learning objectives) — the foreign spec's note model is the authority.
- Do NOT reclassify stubs as done (✅) — they go to 🟨 (drafted); only the user flips 🟨 → ✅.
- Do NOT commit phantom changes from line-ending normalization — verify with `git diff HEAD` first.

## Pitfalls

- **`write_file` refuses to overwrite a file read via `terminal`/`cat` but not via `read_file`.** The `write_file` tool tracks whether THIS task has seen the file's full content through its own `read_file` call. Reading via `terminal` (`cat`, `head`, `tail`) or seeing it in a prior tool's output does NOT satisfy the guard — the call returns `stale_write_blocked: true` and the file is untouched. Before overwriting an existing file, call `read_file` on it (every page if it needs offset/limit), then retry `write_file`. For targeted edits, use `patch` instead.
- **`grep -c` exits 1 when count is 0, breaking `&&` chains.** A `grep -c '🟨' file.md && git commit ...` command never reaches `git commit` when there are zero matches — grep exits 1 (no matches) and the `&&` chain stops. Either use `grep -c '🟨' file.md; git commit ...` (semicolon, not `&&`) or run the grep and commit as separate `terminal` calls. This surfaces as a tool-loop warning after 3 consecutive failures if you keep retrying the chained form.
- **Status-flip via `patch` with `replace_all=true` is the efficient path for KA overviews.** A KA overview has two tables with status cells (Knowledge Units table and Coverage Map), each with repeated tier-based status values like `| CS Core | 🟨 |`. Flipping all at once with `replace_all=true` on the tier string (`| CS Core | 🟨 |` → `| CS Core | ✅ |`) handles both tables in one call. Verify with `grep -c '🟨'` returning 0 (but see the grep-exit-code pitfall above — don't chain it with `&&`).