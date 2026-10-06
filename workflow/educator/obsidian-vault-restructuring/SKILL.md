---
name: obsidian-vault-restructuring
description: "Reorganize Obsidian vaults — split combined notes into individual files, move into topic-based folders, update overview/index files, fix YAML frontmatter."
tags: [obsidian, vault, restructuring, file-management, organization]
---

# Obsidian Vault Restructuring

Reorganize Obsidian vaults by splitting combined notes into individual files, organizing into topic-based folders, and maintaining overview/index files.

## When to Use

- User has combined notes (e.g., multiple chapters in one file) and wants them split into individual files
- User wants notes organized into topic-based folders (e.g., `01_Data_Structures/`, `02_Algorithms/`)
- User wants to pick up reading at any specific topic without navigating a monolithic file
- Overview/index files need updating after restructuring
- User wants to move notes between vaults to align with a reference framework (SWEBOK, BABOK, etc.)

## Linked Files

- **`references/cross-vault-move-pitfalls.md`** — Pitfalls for moving files between vaults: shutil.move ordering, duplicate preservation, filename parsing, verification.

## Workflow

### 1. Scan Current Structure

```
search_files(target='files', path=vault_path, pattern='*.md')
```

Read all files to understand:
- Which files combine multiple topics/chapters
- Which files are standalone (single topic)
- What the overview/index file contains

### 2. Plan the Split

Identify **split points** — the `## Chapter N:` or `## Section Name` headers that delimit topics.

Create a mapping:
```
Combined File → [Individual Files]
02_Advanced_Data_Structures.md → 18_B-Trees.md, 19_Fibonacci_Heaps.md, ...
```

Assign each topic to a folder:
```
01_Data_Structures/
02_Algorithms/
```

### 3. Split Combined Files

Use `execute_code` with a comprehensive Python script. For each combined file:

1. **Read via `terminal("cat ...")`** — NOT `read_file` (see pitfalls)
2. **Normalize line endings** — `.replace("\r\n", "\n").replace("\r", "\n")`
3. **Split by chapter headers** — track preamble (frontmatter + intro) and per-chapter content
4. **Split exercises** — map each exercise to its specific chapter
5. **Split assignments** — map table rows to chapters by keyword matching
6. **Write individual files** — each with its own frontmatter, content, exercises, assignments

#### Splitting Logic

```python
def split_at_headers(content, headers):
    """Split by ## headers. Returns preamble and {header: section_content}."""
    lines = content.split("\n")
    sections = {}
    current_key = None
    current_lines = []
    preamble = []
    found = False
    for line in lines:
        matched = None
        for h in headers:
            if line.strip().startswith(h):
                matched = h
                break
        if matched:
            found = True
            if current_key:
                sections[current_key] = "\n".join(current_lines)
            current_key = matched
            current_lines = []  # Skip the header itself
        elif not found:
            preamble.append(line)
        else:
            current_lines.append(line)
    if current_key:
        sections[current_key] = "\n".join(current_lines)
    return "\n".join(preamble), sections
```

#### Exercise-to-Chapter Mapping

When exercises are at the end of a combined file, map them to chapters:
- By exercise topic/content matching chapter topics
- Or by position (Exercise 1→Chapter 1, etc.)
- Track the mapping explicitly before writing

#### Assignment Row Splitting

Split assignment table rows by keyword matching:
```python
ch18_rows = [r for r in rows if "B-Tree" in r]
ch19_rows = [r for r in rows if "Fibonacci" in r]
```
Uncategorized rows go to the most relevant chapter.

### 4. Move Standalone Files

For files that don't need splitting, just move to the right folder:
```bash
mv original.md destination_folder/new_name.md
```

### 5. Update Overview/Index File

The overview file needs:
- Updated file table with links to all individual files
- Updated Mermaid diagram (if present)
- Updated "When to Study What" guide
- Updated wikilinks

### 6. Delete Old Combined Files

After verifying the split files are correct:
```bash
rm old_combined_file.md
```

### 7. Clean Up

- Remove empty folders
- Verify final structure with `find ... | sort`
- Check sample file content (head + tail)

## Output Structure

```
vault/
├── Overview.md
├── 01_Category/
│   ├── 17_Topic_A.md
│   ├── 18_Topic_B.md
│   └── 19_Topic_C.md
└── 02_Category/
    ├── 23_Topic_D.md
    ├── 24_Topic_E.md
    └── 25_Topic_F.md
```

Each individual file has:
```markdown
---
title: "18 · Topic Name"
tags:
  - tag1
  - tag2
source: CLRS Chapter N
---

# 18 · Topic Name

> One-line summary quote

[Chapter content]

---

## Hands-On Exercises

[Exercises specific to this chapter]

---

## Assignments

| # | Problem | Difficulty | Key Technique |
|---|---------|:----------:|---------------|
[Problems specific to this chapter]
```

## Cross-Linking an Index and a Reference Tier

Vaults often hold two kinds of `00-` notes: a **map/index** (short, opinionated, wired to guides — "which guide do I open?") and a **reference/theory** note (long, exhaustive — "the full model"). They are not duplicates; they serve different jobs.

- **Name folders by function, not difficulty.** "fundamental vs advance" invites endless reclassification and breaks wikilinks every time a note moves. Prefer the stable axis: **guides/how-to** vs **theory/reference** — a note either shows how to do something or explains the underlying model, which never needs re-litigating.
- **Wire both ways.** The index links *up* to the reference ("for the full model, see [[X-Reference]]"); the reference links *back down* to each matching guide with a `**Related guide:** [[guide]]` line under the relevant section. A reference tier with no link back from the guides is dead weight.
- **Disambiguate duplicate titles.** When both tiers share a name (e.g. `00-Writing-Types.md` in each folder), rename the reference to `00-Writing-Types-Reference.md` (retitle H1 + frontmatter too) so the two stop reading as the same note.

## Tiered Hub-and-Spoke Structure

When a large reference note will expand into many topics, prefer a **tiered hub-and-spoke** layout over a flat dump:

```
vault/
├── 00-Reference.md            ← master hub (links down into each tier)
├── tier-1-<topic>/
│   ├── overview.md            ← hub: table of leaves + up/down/sibling links
│   ├── Leaf-A.md
│   └── Leaf-B.md
├── tier-2-<topic>/
│   └── overview.md
└── tier-3-<topic>/
    └── overview.md
```

- **Each `overview.md` is a hub**, not a leaf: a table listing its leaves as `[[wikilinks]]`, cross-references to related fundamental guides, and a `## Status` line stating whether leaves are written or pending.
- **Use unresolved `[[...]]` links as the roadmap.** The hub's table names leaves that don't exist yet; they resolve one at a time as each note lands, and `## Status` records progress. This makes the hub the plan of record — no separate TODO list needed.
- **Master hub descends via path-qualified links** — `[[tier-1-modes/overview|Tier 1 · Modes]]` — so a reader can walk from the single reference into any tier.
- **Leaves follow one consistent template** so the set reads as a set: purpose → when-to-use → characteristics → a Mermaid structure → key techniques → examples → pitfalls → quality criterion → related links → sources.

## Pitfalls

- **Preserve line endings on in-place edits, not just on read.** When renaming + cross-linking an existing file in place (rather than rewriting it), detect the original EOL (`if '\r\n' in text`) and write back with the SAME EOL. Mixing EOLs turns the whole file into a diff and can break Obsidian rendering.
- **Escape `[[` in search patterns.** `search_files` content patterns are regex; a literal `[[Note]]` needs escaping (`\\[\\[`) or it throws an "unclosed character class" error. Match on a distinct substring (the note title) instead of the full wikilink when possible.
- **`read_file` dedup after modification.** If you read a file with `read_file`, then modify it, subsequent `read_file` calls return a dedup response. Use `terminal("cat '<path>'")` instead. Check `result.keys()` — if `content_returned` instead of `content`, you got deduped.
- **Windows line endings.** Always normalize: `.replace("\r\n", "\n").replace("\r", "\n")`. MSYS `cat` may produce `\r\n`. Without normalization, header matching silently fails.
- **YAML frontmatter indentation.** Tags must be indented under `tags:`:
  ```yaml
  tags:
    - tag1
    - tag2
  ```
  NOT `tags:\n- tag1\n  - tag2` (first tag missing indentation).
- **Duplicate section headers.** When writing split files, don't include the original `## Chapter N:` header if you're adding a new `# N · Title` header. Remove the old one from extracted content.
- **Duplicate `---` separators.** After splitting, check for `\n---\n\n---\n` patterns and collapse to single `---`.
- **Exercise-to-chapter mismatch.** Track which exercise belongs to which chapter BEFORE writing. Don't append all exercises to all files.
- **Assignment row completeness.** Verify all assignment table rows are accounted for after splitting. Use keyword matching, then assign uncategorized rows to the most relevant chapter.
- **Empty folders.** Clean up any empty directories left after moving files.
- **Duplicate note names across folders break wikilinks.** Obsidian resolves `[[...]]` by note *name*, not path. Multiple `overview.md` files (one per tier) make a bare `[[overview]]` ambiguous — Obsidian prompts the user to disambiguate. Fix by either (a) giving each hub a distinct name (`modes-overview.md`, `domains-overview.md`), or (b) using path-qualified links `[[tier-1-modes/overview|Label]]` for every cross-tier reference. Folder renames are free since links are name-based.

## Quality Checklist

Before declaring done:
- [ ] All individual files have proper YAML frontmatter
- [ ] No duplicate `---` separators
- [ ] No duplicate section headers
- [ ] Each file has its own exercises and assignments
- [ ] Overview file links to all individual files
- [ ] Old combined files deleted
- [ ] No empty folders
- [ ] Sample file verified (head + tail check)
