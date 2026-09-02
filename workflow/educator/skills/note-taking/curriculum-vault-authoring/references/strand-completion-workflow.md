# Strand Completion Workflow: Phase 1 + Phase 2

When a strand is partially complete (e.g., 3/14 files done covering ม.1-3 only) and the user asks to "proceed the pending and also update the 01-03 by adding the ม.4-ม.6 content", use this two-phase workflow.

## Phase 1: Create All Pending Files

1. Read the `00_overview.md` to identify which files are pending (❌ Pending)
2. Read 2-3 existing files to match format, depth, and style exactly
3. Batch-create all pending files using `write_file` — 3-4 per response
4. Match the existing format precisely:
   - YAML frontmatter with strand, course_codes, tags (include `upper-secondary`)
   - Grade band table (ป.1–3, ป.4–6, ม.1–3, **ม.4–6**)
   - Numbered sections (## 1 | Grade Band, ## 2 | Topic, etc.)
   - Thai-English terminology tables
   - Real-world examples section
   - Cross-links section

## Phase 2: Update Existing Files with ม.4-6 Content

For each file that exists but lacks upper secondary content:

### Step A: Patch YAML tags
Add `upper-secondary` to the tags array.

### Step B: Patch grade band table
Add a new row:
```markdown
| **ม.4–6** | Advanced [topic], critical analysis, [specialized content] |
```

### Step C: Insert new section before cross-links
Three `patch` calls per file (tags, grade band, new section), or combine into fewer calls where the context is contiguous.

### Section template:
```markdown
## N | Upper Secondary (ม.4-6): [Topic Title]

### [Subsection 1]

| Concept | Thai | Description |
|---|---|---|
| **Term** | คำศัพท์ | Description |

### [Subsection 2]
...
```

### Step D: Renumber cross-links section
If the new section pushes cross-links from section 9 to section 10, update the heading number.

### Step E: Fix cross-link target numbers
Some existing cross-links reference old file numbers (e.g., `[[04_Personal_Finance]]` when the file is actually `02_Personal_Finance`). Verify and fix.

## Phase 3: Update Overview Tracker

After all files are created/updated:

```markdown
| 01 | Topic | ✅ Done | `01_File.md` | Updated with ม.4-6 |
| 02 | Topic | ✅ Done | `02_File.md` | Updated with ม.4-6 |
...
| NN | Topic | ✅ Done | `NN_File.md` | Created YYYY-MM-DD |

**Completion: N/N (100%)**
```

## Quality Checks After Completion

1. **File size check** — scan `bytes_written` from write_file results. Any file < 4KB when siblings are 7-12KB is likely truncated. Rewrite truncated files fully.
2. **YAML corruption check** — scan frontmatter for Latin garbage in Thai strings: `grep -rn 'strand:' *.md`
3. **Cross-link verification** — check that every `[[Wikilink]]` in cross-links sections matches an actual file in the folder.
4. **Grade band completeness** — every file should have all 4 grade bands (ป.1–3, ป.4–6, ม.1–3, ม.4–6) in its table.

## Proven Strand Sizes (reference)

| Strand | Files | Total Size | Avg/File | Notes |
|---|---|---|---|---|
| **02 Civics** | 13 + overview | ~95KB | ~7.3KB | First strand completed |
| **03 Economics** | 14 + overview | ~120KB | ~8.6KB | Phase 1+2 workflow |
| **04 History** | 15 + overview | ~150KB | ~10KB | Richest strand, Mermaid-heavy |
| **05 Geography** | 14 + overview | ~140KB | ~10KB | Completed with SearXNG-assisted research |
| **01 Religion** | 2 + overview | ~12KB | ~6KB | Partial, needs expansion |

History and Geography strands tend to be the largest (~10KB/file) due to: detailed period/region tables, multiple Mermaid diagrams (flowcharts for timelines/processes), source criticism sections, and ม.4-6 analytical content (historiography, GIS, policy analysis).

## SearXNG MCP Usage During Strand Completion

When SearXNG MCP is available, use it strategically — NOT for every file:

1. **Fire 2-3 initial searches** for the most uncertain/specialized topics (e.g., Ban Chiang archaeology, Sukhothai inscription details)
2. **Use `web_url_read`** to extract detailed content from promising search results (Wikipedia articles are most reliable)
3. **Complete remaining files from model knowledge** — the model's training knowledge of Thai geography, history, economics is accurate and sufficient for BOK notes
4. **Watch for rate limits** — if 429 errors appear, STOP searching and switch to knowledge-based production

**Search quality note:** SearXNG returns mixed relevance. Commercial sites (Best Buy, hotels) sometimes rank above educational content. Filter for `.org`, `.ac.th`, Wikipedia, and known educational domains in results.

## Content Depth by Grade Band

| Grade | Content Depth | Example (History) |
|---|---|---|
| **ป.1–3** | Stories, simple concepts | "Stories of King Ramkhamhaeng" |
| **ป.4–6** | Key facts, overview | "Sukhothai as first Thai kingdom, key achievements" |
| **ม.1–3** | Detailed analysis | "Political structure, culture, religion, trade" |
| **ม.4–6** | Critical/analytical | "Source criticism of Ramkhamhaeng inscription, comparative with Ayutthaya" |

The ม.4-6 sections should introduce:
- Historiographical debate (multiple perspectives, source criticism)
- Comparative analysis (comparing periods, systems, figures)
- Critical thinking (questioning narratives, evaluating evidence)
- Advanced terminology (academic Thai terms)
- Real-world connections (modern relevance, current events)
