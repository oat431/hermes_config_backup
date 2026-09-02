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

## Pitfalls

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
