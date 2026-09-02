# Social Studies Progress Tracker Pattern

After creating topic notes for Social Studies, group them into 5 strand folders and create `00_overview.md` progress trackers in each.

## Folder Structure

```
Social Studies/
├── 01 Religion/
│   ├── 00_overview.md              ← Progress tracker
│   ├── 01_Buddhist_Principles.md
│   └── 02_Buddhist_Ceremonies_and_Meditation.md
├── 02 Civics/
│   ├── 00_overview.md
│   ├── 01_Democracy_and_Government.md
│   └── ...
├── 03 Economics/
│   ├── 00_overview.md
│   └── ...
├── 04 History/
│   ├── 00_overview.md
│   └── ...
└── 05 Geography/
    ├── 00_overview.md
    └── ...
```

## 00_overview.md Template

```markdown
---
tags: [overview, social-studies, <strand-tag>, primary, lower-secondary, upper-secondary, ipst]
source: "OBEC Basic Education Core Curriculum B.E. 2551 (2008), revised 2560 (2017)"
created: YYYY-MM-DD
strand: "สาระที่ X: <strand name>"
---

# <Strand Name> — <Thai Name>

> **Strand:** สาระที่ X | **Concept Areas:** ~N | **Duration:** 12 years (ป.1–ม.6)
> **Focus:** <key topics>

## Overview
<1-2 paragraph description>

## Concept Areas

| # | Concept Area | Thai | ป.1–3 | ป.4–6 | ม.1–3 | ม.4–6 |
|---|---|---|---|---|---|---|
| 01 | [[Topic]] | ไทย | ... | ... | ... | ... |
...

## Progress Tracker

| # | Concept Area | Status | Files Created | Notes |
|---|---|---|---|---|
| 01 | Topic | ✅ Done | `01_File.md` | |
| 02 | Topic | ❌ Pending | — | What's needed |

**Completion: X/Y (Z%)**

## Related
- [[Social Studies - Overview|← Back to Social Studies]]
- [[other strand/00_overview|Other Strand]]
```

## Key Points

- Each folder has independent 01, 02, 03 numbering
- Old overview files from research agents should be removed to avoid conflicts
- Progress trackers enable continuation by other educator agents
- Full ป.1-ม.6 range in concept area tables (4 grade band columns)

## Continuing From a Progress Tracker

When picking up work from another agent's progress tracker:

1. **Read all existing files** — understand format, depth, style before creating new ones
2. **Verify cross-links** — previous agents often planned filenames that differ from actual files. Check every `[[wikilink]]` against real filenames.
3. **Scan for encoding errors** — `grep -P '[\x{4e00}-\x{9fff}]' *.md` to find Chinese characters in Thai text
4. **Match format exactly** — same YAML frontmatter keys, section numbering, table style
5. **Update tracker after each file** — mark ✅ Done with real filename, recalculate percentage

### Cross-Link Repair Pattern

When existing files have broken cross-links (planned name ≠ actual name):

```bash
# List actual files
ls *.md

# Find broken links
grep -n '\[\[' *.md | grep -v 'Overview'
```

Then use `patch` to fix each broken link to match the actual filename. Example:
- `[[02_Rights_and_Duties|Rights & Duties]]` → `[[04_Rights_Duties_and_Laws|Rights, Duties, and Laws]]`

### Mermaid for Hierarchical Content

Social Studies topic notes benefit from Mermaid diagrams for:
- Government structure (three branches with sub-bodies)
- Institutional hierarchies (ministries → departments)
- Court system hierarchy
- Concept interdependence (family → school → economy → government)

Use `flowchart TD` with labeled nodes. Avoid `()` in labels — use `&#40;`/`&#41;` or `[]` brackets instead.
