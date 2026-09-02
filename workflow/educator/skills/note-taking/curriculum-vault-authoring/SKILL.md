---
name: curriculum-vault-authoring
description: Map educational curricula into Obsidian Body of Knowledge vault structures — overview files, topic breakdowns, cross-links, and reading paths.
tags: [obsidian, curriculum, education, body-of-knowledge, vault-structure]
triggers:
  - "create body of knowledge for"
  - "map curriculum to obsidian"
  - "build knowledge area overview"
  - "curriculum structure for vault"
  - "bok overview"
---

# Curriculum-to-Vault Authoring

Create Obsidian vault structures that map educational curricula into organized Body of Knowledge (BOK) hierarchies. Used when building knowledge reference vaults from scratch — not for filling gaps in existing vaults (use `educational-content-authoring` for that).

## When to Use

- User wants to create a new BOK structure in an Obsidian vault
- Mapping a curriculum (Thai, international, or custom) into topic-organized notes
- Building overview/index files for a knowledge domain
- Organizing subjects by concept area, course code, or grade level

## Prerequisites

- Target vault path confirmed
- Scope clarified: level (primary/secondary/university), subjects, depth
- Format reference if user has an existing vault pattern

## Step 1 — Clarify Scope

Ask the user:
1. **Level** — Primary, secondary, university, or mixed?
2. **Subjects** — Which subjects to include?
3. **Source** — Official curriculum (IPST, AP, IB, A-Level) or custom?
- **Goal** — Personal reference, curriculum map, teaching resource, or **parent-child communication tool** (parents tracking what their child learns at school to support learning at home)? The purpose shapes the overview style: exam-focused (formulas, test weights) vs parent-focused (\"What Your Child Learns\" tables, home activity suggestions).

## Step 2 — Research the Curriculum

Use web search or delegation to find:
- Official course codes (e.g., Thai ค301, ว301)
- Topic distribution by year/semester
- Governing body standards (e.g., สสวท./IPST for math-science, สพฐ./OBEC for Thai language and other subjects)
- International equivalents if needed

### Career & Technology / Home Economics and Agriculture research pattern

For Career & Technology requests (การงานอาชีพ), especially Home Economics and Agriculture, treat the national curriculum as a **standards umbrella**, not as a guaranteed chapter list. The requested applied topics may be school-level units or useful concept clusters rather than headings that appear verbatim in the national document.

1. **Anchor the research in the exact document version.** Start with the OBEC curriculum index and the official Career & Technology indicator document. Record whether the source is the legacy 2551 guide, a 2560 revision, or a school curriculum derived from it. Do not silently mix old `การงานอาชีพและเทคโนโลยี` strand names with post-2560 subject arrangements.
2. **Separate three claims in the note:** (a) `National-standard alignment`, (b) `Suggested school-unit progression`, and (c) `Extension / practical knowledge`. This prevents an inferred sequence such as “cooking in ป.3” from being presented as an official nationwide placement.
3. **Map applied topics to broad outcomes:** work process (กระบวนการทำงาน), management (ทักษะการจัดการ), problem solving (การแก้ปัญหา), collaboration (การทำงานร่วมกัน), safe tool/material use (การใช้วัสดุ อุปกรณ์ และเครื่องมืออย่างปลอดภัย), resource and environmental responsibility (การใช้พลังงาน ทรัพยากร และสิ่งแวดล้อม), and career orientation (การอาชีพ). Verify any `ง 1.1` / `ง 2.1` indicator number against the cited document and grade before quoting it.
4. **Use the four requested bands as a spiral progression:** ป.1–3 = self-help, recognition, routines, and supervised tools; ป.4–6 = repeatable procedures, measurement, planning, hygiene, and teamwork; ม.1–3 = analysis, troubleshooting, resource management, and career awareness; ม.4–6 = specialization, quality control, costing, sustainability, entrepreneurship, and evidence-based decisions. This is a blueprinting model, not a claim that every school allocates every topic identically.
5. **Cross-link rather than overclaim.** Nutrition connects to Health (สุขศึกษา), child development connects to Health and family/life skills, cultivation and animal husbandry connect to Science, soil/water to Earth/environment, and food processing to health, chemistry, and entrepreneurship. Keep the Career & Technology alignment explicit while labeling the cross-curricular support.
6. **Source hierarchy:** use OBEC/MOE for standards; Thai government technical agencies for practice (กรมวิชาการเกษตร, กรมพัฒนาที่ดิน, กรมปศุสัตว์, อย./กองอาหาร, กรมอนามัย); WHO/UNICEF/FAO for internationally recognized health, child-development, food-safety, and agriculture guidance; universities only as secondary explanatory sources. Put the direct URL beside each topic rather than a generic homepage alone.
7. **Research efficiently and stop on evidence.** Batch a small number of high-value searches, select the authoritative result, and record its URL and what it supports. If a PDF is difficult to extract, use the official landing page, indexed metadata, or a second official HTML/PDF representation; do not keep repeating the same query or infer exact wording from a corrupted extraction. Never let search-tool throttling turn into a loop.

See `references/thai-career-technology-curriculum.md` for the nine-topic Home Economics/Agriculture mapping, grade-band blueprint, terminology bank, and source directory. See `references/thai-career-technology-curriculum-research.md` for the broader curriculum-status distinction, technology-strand transition, workshop-safety hierarchy, and career/technical source workflow.

**Pitfall:** Don't assume topic distribution — always verify against official curriculum docs. Thai curriculum uses "ค" prefix for math, "ว" prefix for science, "ท" for Thai language, with 1xx=primary, 2xx=lower secondary, 3xx=upper secondary. Math-science is governed by IPST (สสวท.); Thai language is governed by OBEC (สพฐ.).

**Pitfall — source access and evidence:** Do not infer that a curriculum source is unavailable from a poor search result or one failed fetch. Open the official landing page, inspect its linked document titles and direct URLs, and use an alternate official HTML/PDF representation when needed. For Thai Career & Technology, use the OBEC hub and Order 921/2561 before relying on training knowledge or Wikipedia. Wikipedia is a contextual fallback, not primary evidence for curriculum status. Do not repeat identical failed searches; change the source or retrieval method and record what the source actually supports.

## Step 3 — Choose Organization Strategy

This is the most important structural decision:

### Linear Progression (year-based)
Use when each year covers **different topics**:
```
Physics/
├── Physics - Overview.md
├── ม4/ (Mechanics, Waves, Thermo)
├── ม5/ (E&M, Optics)
├── ม6/ (Modern Physics)
```
**Best for:** Upper secondary specialized subjects (ม.4-ม.6), university courses

### Spiral Progression (concept-area-based)
Use when **same concepts** appear at every level, just deeper:
```
Fundamental Mathematics/
├── Fundamental Mathematics - Overview.md
├── 01_Numbers_and_Numeration.md  (covers ป.1-ม.3 progression)
├── 02_Fractions.md               (covers ป.1-ม.3 progression)
```
**Best for:** Primary/lower secondary (ป.1-ม.3), integrated subjects. Note: Thai language and Social Studies both use spiral progression across all 12 years (ป.1-ม.6).

**Pitfall:** Don't split spiral-curriculum subjects by grade band — you'll get 60 files with repeated content instead of 20 clean concept-area files. Use progression tables within each file to show grade-band depth.

## Step 4 — Create Directory Structure

```bash
mkdir -p "<vault>/body-of-knowledge/<Subject>"
```

One folder per subject area. Each folder gets an overview file. Topic files go inside the same folder.

## Step 5 — Write Overview Files

Each overview file follows this template:

```yaml
---
tags: [overview, <subject>, <level>, <curriculum-source>]
---
```

### Required Sections

1. **Header block** — Subject name, course codes, topic count, duration, source, leads-to links
2. **What Is This?** — 2-3 paragraph explanation
3. **Topic/Concept Area Breakdown** — Numbered list with `[[wikilinks]]`, grouped by category
4. **Progression Table** — Shows how topics distribute across years/levels
5. **Prerequisites** — What's needed before each level
6. **Mermaid Diagram** — Shows how topics connect (use `flowchart TD`)
7. **Cross-links** — Connections to related subjects with `[[wikilinks]]`
8. **Reading Paths** — Different routes through the material
9. **Related** — Back-link to parent overview, forward links to child subjects

### Format Patterns

- YAML frontmatter with tags array
- `> **bold key:**` for header metadata blocks
- Tables for progression/comparison
- `[[Topic Name|→ Full Overview]]` for overview links
- `[[Topic Name]]` for topic wikilinks
- Mermaid `flowchart TD` for relationship diagrams
- Emoji prefixes for visual category grouping (🔢 Math, ⚛️ Physics, etc.)

## Step 6 — Write Top-Level Index

The `Body of Knowledge - Overview.md` is the master index:

1. Summary table of all subject areas (name, course codes, topic count, focus)
2. One section per subject with brief description and link to full overview
3. Mermaid diagram showing how ALL subjects interconnect
4. Reading paths for different tracks (engineering, medicine, etc.)
5. Curriculum notes (governing body, course code system, textbook sources)
6. Related links to other vault sections (e.g., English Skill)

## Step 7 — Create Book Checklist

After the BOK structure is complete, create a `checklist/` folder with book recommendations:

```
checklist/
├── Book Checklist - Overview.md      ← master index + publisher guide
├── <Subject> - Books.md              ← one per subject
```

Each subject file uses priority tiers:
- 🔴 **Essential** — Must-have (IPST textbooks + primary reference)
- 🟡 **Recommended** — Very useful supplement (Thai study books, exam prep)
- 🟢 **Optional** — Deeper exploration (international textbooks)

Sections per file:
1. **IPST Textbooks** — Official curriculum books (free PDFs at ipst.ac.th)
2. **Thai Study Books** — สรุปเข้ม (MIS), ตะลุยโจทย์ (iQBook), พ.ก.ศึกษาศาสตร์ (แบบเรียนเร็ว)
3. **International Textbooks** — Standard references (Giancoli → Halliday for physics, Zumdahl/Chang for chemistry, Campbell for biology, Stewart for calculus)
4. **Exam Prep** — O-NET, A-Level, PAT, กสพท.
5. **Famous Tutors** — Popular tutoring materials (ครูพี่ยม, ครูพี่วิเวียน, ครูพี่ลูกกอล์ฟ, OnDemand)

**Research method:** Use `delegate_task` with 2 subagents running in parallel — one for comprehensive book research across all subjects, one for cross-referencing Thai publishers and exam-prep specific books. Each returns in 1-3 minutes while you create files. The research output should also be saved to `references/thai-book-recommendations.md` for future sessions. Include both Thai-language books and English international textbooks with their Thai translations where available (e.g., Campbell → ชีววิทยา แคมป์เบลล์).

**Pitfall:** Don't skip IPST textbooks — they're the PRIMARY reference and free. Always list them as 🔴 Essential. International textbooks come as 🟡/🟢 for deeper exploration. Don't forget to mention that Campbell is non-negotiable for กสพท. preparation.

## Step 8 — Verify and Report

- Check all files created: use `terminal` with `find "<vault>/body-of-knowledge" -name "*.md" -type f | sort` instead of `search_files` (see pitfall below)
- Check checklist created: same `find` pattern under `<vault>/checklist`
- Report total topic count and structure to user
- Offer to dive deeper into any specific subject

> **⚠️ Pitfall — `search_files` silently returns 0 on F:\ drives for `target='files'`:** When the vault is on a non-C: drive (F:\), `search_files(target='files', pattern='*.md', path='F:\\...')` returns `{"total_count": 0}` with NO error message — a silent failure, not an exception. This affects BOTH `target='files'` (file listing) and `target='content'` (grep). Always use `terminal` with `find "<F:/path>" -name "*.md" -type f | sort` for file listing, and `grep` for content search. Do NOT retry `search_files` with different path formats — it fails silently every time on F:\ drives.

## Step 9 — BOK Enrichment Pass (Sub-Overview Creation)

After the initial overview files are created, the user may ask to **enrich** a subject to match the depth of another (e.g., "review and add gaps, make it like Social Studies"). This happens when a BOK has only flat topic lists without deeper category breakdowns.

### When to Enrich

- User explicitly compares depth across BOK subjects (e.g., "Math is thin vs Social Studies")
- A BOK has only 2 thin files while another has 6+ files with sub-overviews
- User has reorganized vault and consolidated subjects

### Enrichment Pattern

1. **Identify categories** — Group existing flat topic lists into 5-10 logical categories
2. **Create sub-folders** — `mkdir -p` for each category under the subject folder
3. **Write sub-overviews** — Each gets: YAML frontmatter, overview paragraph, topic table with grade bands, learning progression (Mermaid), key formulas/theorems, Thai terminology, common misconceptions, exam relevance, cross-links
4. **Update main overviews** — Add a category table at the top linking to each sub-overview
5. **Maintain wikilinks** — Sub-overviews link back to main overview and across to related categories

**Result example:** Mathematics: 2 files (20KB) → 12 files (92KB)

### Sub-Overview Template

See `references/thai-math-strand-overview-pattern.md` for the complete proven template used across 10 Mathematics strand sub-overview files. The template includes:
- YAML frontmatter with strand-specific tags
- Per-sub-strand: grade band table, key formulas, Thai terminology (Thai/romanized/English), common misconceptions, real-life connections (Thai context)
- Cross-reference progression summary table
- Exam relevance with approximate weights
- IPST textbook references per level
- Mermaid diagrams (quadrantChart for coordinate planes, flowchart for hierarchies)

### Pitfall

**Don't duplicate topic detail between overview and sub-overview.** The main overview delegates to sub-overviews via a category table. Put deep content (formulas, misconceptions, grade-band details) in the sub-overview. The main overview retains the topic list, progression table, mermaid diagram, and reading paths.

**Use `delegate_task`** to research enrichment content while you create directory structure — the research takes 2-5 minutes and returns comprehensive strand/topic breakdowns that match the enriched format.

- **After enrichment, regroup by parent subject.** Once all sub-overviews are created, the user may want them moved under parent folders (e.g., Physics/, Chemistry/, Biology/) rather than flat-numbered. Use `mv` to relocate sub-folders, then `rmdir` to clean up empty old directories. This makes the structure cleaner:

### Pitfall — SearXNG MCP Rate Limiting (429)

When using the SearXNG MCP (`mcp__searxng__searxng_web_search`) for curriculum research, the server may rate-limit after ~3 rapid consecutive calls, returning `429: Rate limit exceeded`. This is a transient throttle, NOT a permanent failure.

**Strategy:**
1. Fire 2-3 initial searches for the most uncertain topics, then STOP.
2. Complete remaining files from model knowledge — the model's training knowledge of Thai history, economics, civics, geography is accurate and sufficient for BOK notes.
3. Do NOT retry the same failing MCP call repeatedly — the tool loop warning fires after 3 consecutive failures.
4. If a single `web_url_read` works, use it; don't cascade into more searches.
5. **If the user says the rate limit is fixed** (infra team adjusted settings), test with one search. If it works, use it strategically for the 2-3 most specialized topics, then proceed from model knowledge.

**Search quality:** SearXNG returns mixed relevance — commercial sites (Best Buy, hotels, gaming PCs) sometimes outrank educational content. Filter results for Wikipedia, `.org`, `.ac.th`, and known educational domains. Wikipedia articles load reliably via `web_url_read` and are the best source for historical/geographic detail.

**Curriculum verification pattern (proven for IPST Physics 2026-07-30):** When verifying Thai curriculum topic distribution before creating advanced notes, search for `"[subject] ม.ปลาย หลักสูตร สสวท เรียนอะไรบ้าง"` (e.g., `"ฟิสิกส์ ม.ปลาย หลักสูตร สสวท เรียนอะไรบ้าง"`). The site smartmathpro.com publishes per-subject IPST curriculum summaries with chapter names in Thai, topic distribution by semester, and source attribution to IPST textbooks. Fetch the full article via `mcp__searxng__web_url_read` and cross-reference against the BOK overview. Note: our BOK overviews may be a superset of the standard IPST curriculum (e.g., we include Special Relativity and Astrophysics as extension topics beyond the standard ~20 chapters).

**When SearXNG is unavailable entirely (403/connection error):** Fall back fully to the two-pass pattern (produce from knowledge, verify against Wikipedia which loads reliably).

**Failure mode 2 — subprocess death (seen 2026-08-28, distinct from 429):** every `mcp__searxng__searxng_web_search` call fails fast with `TimeoutError: MCP stdio subprocess for 'searxng' has exited`. No call succeeds, not even spaced out — this is a dead server, not a throttle. Do not keep retrying the MCP (loop warning fires at 3 failures). Fallback that works: the built-in `web_search` tool (SearXNG-backed) — run 1–2 verification searches for the most load-bearing facts (e.g., English มาตรฐาน codes อ1.1–อ4.2, course code อ21101), then build the rest from model knowledge. Never block note creation on search tooling when the curriculum structure is already known.

### Pitfall — File Truncation in `write_file`

When batch-creating multiple large files (8KB+), occasionally a `write_file` call returns success but the file is truncated (e.g., 2,385 bytes instead of the expected ~11KB). The tool reports `bytes_written` in its result.

**Strategy:**
- After batch writes, scan the `bytes_written` values. Any file significantly smaller than siblings (e.g., < 4KB when siblings are 7-12KB) is likely truncated.
- For truncated files, rewrite with `write_file` using the full content.
- Do NOT patch truncated files piecemeal — rewrite the whole file.

**Observed variants (2026-08-28, glm model):** truncation is not the only failure shape.
- **Silent path typo = junk root.** A single-char path typo (`obsidian_note` → `obsian_note`) made `write_file` create the full directory tree in a NEW junk root with `dirs_created: true` and `verified: true`. The corrupt file hid there while the real vault stayed clean. After any batch, `ls` the vault root for unexpected directories; delete junk roots explicitly (user-approved `rm -rf`).
- **Garbage tail at full length.** One file arrived at expected size (7,005 bytes) with the last sections replaced by duplicated/garbled fragments (repeated headings, `. Use the...` fragments). Size checks alone do not catch this — tail-check the final 10–15 lines of a sample of files, or grep for repeated heading strings.

### Pitfall — Thai Text Corruption in YAML Frontmatter and Body Text

AI models occasionally produce Latin-script garbage mid-Thai-string in YAML frontmatter values (e.g., `ปร. Walshาสตร์` instead of `ประวัติศาสตร์`). This happens with longer Thai strings in `strand:` and `source:` fields.

With the **glm-5.2 model** (zai provider), the corruption extends beyond YAML into **body text and wikilink display text** — and scales with strand size. Small strands (10 files) see ~4 sporadic instances; large strands (23+ files) can produce **20+ distinct corruption strings** across most files. Observed corruption types: `พ.ศ. ไ2๕51` in frontmatter, `การพูดแสดงคว Thai: มีอักษรผิด` inside a wikilink, Latin-mid-Thai insertions (`ควam` for `ความ`, `กlอน` for `กลอน`, `วrอง` for `วรรค`), and single-character word swaps (`พูก` for `พูด`, `สงบสุข` for `สงบใจ`).

**Strategy — small strands (≤15 files):**
- After batch file creation, scan for corruption: `grep -rn '[ไ-ฮ][A-Za-z]' *.md` catches Latin-script characters adjacent to Thai script.
- After batch file creation, scan YAML frontmatter for non-Thai, non-ASCII garbage: `grep -rn 'strand:' *.md | grep -v 'ประวัติ\|เศรษฐ\|หน้าที่\|ศาสนา\|ภูมิ'`
- Fix with `patch` — the corrupted string is always unique in the file.

**Strategy — large strands (15+ files) — batch sed cleanup:**
When corruption is too widespread for individual patches, run a batch `sed` cleanup via `execute_code`:
```python
from hermes_tools import terminal
fixes = [("ควam", "ความ"), ("กlอน", "กลอน"), ("วrอง", "วรรค"), ...]  # discovered via grep first
for old, new in fixes:
    cmd = f'find "{base}" -name "*.md" -exec sed -i \'s/{old}/{new}/g\' {{}} \\;'
    terminal(cmd)
```
Run `grep -rn '[ไ-ฮ][A-Za-z]' *.md` FIRST to discover all patterns, build the fixes list, apply sed, then verify with a final grep.

```
Before (flat):                    After (grouped):
Science/                          Science/
├── 05 Mechanics/                 ├── Physics/
├── 06 Thermodynamics/            │   ├── 05 Mechanics/
├── 07 Electricity/               │   ├── 06 Thermodynamics/
├── 09 Chemical Foundations/      │   └── ...
└── ...                           ├── Chemistry/
                                  │   ├── 09 Chemical Foundations/
                                  │   └── ...
                                  └── ...
```

The user will explicitly ask for this: "group them following by Physics Chem Bio Earth Com for me like create Physic folder and under it might have 05 Mechanics". Execute the move in one batch, then rmdir old empty folders.

## Step 9b — Progress Tracker Overviews (00_overview.md)

After grouping topic notes into strand folders, create a `00_overview.md` in each strand folder. This serves as a **continuation guide** for other educator agents.

### 00_overview.md Template

Each file contains:
1. **YAML frontmatter** with strand tag and `ipst` source
2. **Overview paragraph** explaining the strand
3. **Concept area table** — ALL concept areas in the strand, with grade band columns (ป.1–3, ป.4–6, ม.1–3, ม.4–6)
4. **Progress tracker table** — Each concept area marked ✅ Done (with filename) or ❌ Pending
5. **Completion percentage** — e.g., "Completion: 4/13 (31%)"
6. **Cross-links** to other strand overviews

### Progress Tracker Table Format

```markdown
| # | Concept Area | Status | Files Created | Notes |
|---|---|---|---|---|
| 01 | Topic Name | ✅ Done | `01_Topic_Name.md` | |
| 02 | Another Topic | ❌ Pending | — | Brief note on what's needed |
```

### Pitfall
- **Don't create 00_overview.md before topic notes exist.** Create topic notes first, then the overview tracks what's done vs pending.
- **Numbering convention varies by subject — CONFIRM the existing content root's convention before creating any file.** Two proven layouts in this vault: per-folder numbering restarting at 01 (Social Studies, Student Development, Health-PE) vs CONTINUOUS numbering across the whole subject (English Curriculum: strands hold 01–06, 07–12, 13–18, 19–24; Career & Technology: 01–22 across 5 strand folders). Derive it from the closest sibling content root, or ask. Creating files before the scheme is locked caused a 3-file rename + 7-link repair on 2026-08-28.

## Step 9c — Continuing Work From Other Agents

When a progress tracker shows ❌ Pending items, another educator agent can pick up the work. Before creating new files:

1. **Read ALL existing files first** — understand the format, style, and depth the previous agent used
2. **Check cross-links in existing files** — previous agents often planned filenames that don't match what was actually created (e.g., `02_Rights_and_Duties` in a link vs `04_Rights_Duties_and_Laws` as the actual file). Fix broken links before proceeding.
3. **Watch for encoding errors** — AI models sometimes produce Chinese characters (e.g., 男性 instead of ชาย) mid-sentence in Thai text. Scan existing files for CJK: `grep -P '[\x{4e00}-\x{9fff}]' *.md`
4. **Match the format exactly** — YAML frontmatter structure, section numbering style, table column count, terminology table placement
5. **Update the progress tracker** — mark items ✅ Done with actual filenames, recalculate completion percentage

**Pitfall — Cross-link filenames diverge from actual files.** When one agent plans the overview with placeholder wikilinks and another agent creates the actual files, the filenames often differ (planned `02_Rights_and_Duties` vs actual `04_Rights_Duties_and_Laws`). Always verify cross-links match real filenames after continuing work. Use `find` via `terminal` (NOT `search_files` — see Step 8 pitfall) to get the actual file list, then patch broken links.

**Tip — `read_file` returns `similar_files` on path mismatch.** When `read_file` can't find the exact path (e.g., you guessed `Fundamental Mathematics - Overview.md` but the actual file is `00_Fundamental Mathematics - Overview.md`), the tool returns a `similar_files` array with the correct path. This is the fastest way to discover the actual filename when you know the approximate name but not the exact prefix/numbering. Use it before falling back to `find` or `ls`.

## Step 9d — Completing a Strand from Partial Coverage

When a strand is partially complete (e.g., 3/14 files done) and the user asks to "proceed the pending and also update existing with ม.4-6", use this **two-phase completion workflow**:

### Phase 1: Create All Pending Files

1. **Read the overview** to identify which files are pending (❌ Pending in tracker)
2. **Read 2-3 existing files** to match format, depth, and style exactly
3. **Batch-create all pending files** using `write_file` — create files in parallel batches of 3-4
4. **Match existing format:**
   - YAML frontmatter with strand/course_codes/tags
   - Grade band table (ป.1–3, ป.4–6, ม.1–3, ม.4–6)
   - Numbered sections (## 1 | Grade Band, ## 2 | Topic, etc.)
   - Thai-English terminology tables
   - Real-world examples section
   - Cross-links section

### Phase 2: Update Existing Files

For files that exist but are missing upper secondary (ม.4-6) content:

1. **Patch the grade band table** — add a new row for ม.4–6 with appropriate content summary
2. **Add new section before cross-links** — insert "## N | Upper Secondary (ม.4-6): [Topic]" with advanced content
3. **Update YAML tags** — add `upper-secondary` if not present
4. **Renumber cross-links section** if needed (e.g., section 9 → section 10)

### Example Patch Pattern

```markdown
## 9 | Upper Secondary (ม.4-6): Advanced Economics

### Microeconomic Analysis

| Concept | Thai | Description |
|---|---|---|
| **Elasticity** | ความยืดหยุ่น | Responsiveness to price changes |
| **Marginal utility** | อรรถประโยชน์ส่วนเพิ่ม | Additional satisfaction from one more unit |
```

### Pitfalls

- **Don't skip Phase 2.** Creating new files without updating existing ones leaves inconsistent depth across the strand.
- **Read existing files FIRST.** The format (section numbering, table structure, terminology style) varies by strand. Match it exactly.
- **Batch efficiently.** Create pending files in batches of 3-4 using multiple `write_file` calls in one response. Don't create one at a time.
- **Update the overview tracker last.** After all files are created/updated, mark all items ✅ Done and recalculate to 100%.

## Step 9e — Learner Development Activities (กิจกรรมพัฒนาผู้เรียน)

The Thai Basic Education Core Curriculum has **8 academic learning areas**, plus a separate required curriculum component called **Learner Development Activities** (`กิจกรรมพัฒนาผู้เรียน`). Do not classify this as a ninth `กลุ่มสาระการเรียนรู้`, and do not omit it from a parent-child curriculum map.

### Three Forms

1. **Guidance and Counseling Activities** (`กิจกรรมแนะแนว`) — educational, career, personal, and social development; life skills, well-being, self-understanding, educational pathways, and career preparation.
2. **Student Activities** (`กิจกรรมนักเรียน`) — Scouts/Girl Guides (`ลูกเสือ-เนตรนารี`), Red Cross Youth (`ยุวกาชาด`), volunteer/student organizations, clubs, and student leadership. The school selects and schedules the available activity; Scouts are not a guaranteed standalone subject at every school.
3. **Social and Public Benefit Activities** (`กิจกรรมเพื่อสังคมและสาธารณประโยชน์`) — service learning and community/public-interest work. It may be integrated into student activities according to the school's structure.

### How to Model It in a BOK

Create a separate top-level `Learner Development Activities/` area beside the 8 learning areas, not inside Social Studies, Health, or Career. Use a parent overview plus three child overviews. For parent-child communication, describe what students actually participate in, the developmental purpose, and the fact that implementation varies by school.

Suggested progression:

| Level | Guidance | Student activities | Public benefit |
|---|---|---|---|
| **ป.1–3** | Self-awareness, school adjustment, social skills, career awareness | Cooperation, rules, simple Scout/club activities | Simple helping and school/community care |
| **ป.4–6** | Study habits, interests, basic career awareness | Scout skills, teamwork, responsibility, outdoor activities | Local service and environmental care |
| **ม.1–3** | Self-exploration, interests/aptitudes, upper-secondary or vocational pathways | Leadership, clubs, Scouts or alternative groups | Planned service projects |
| **ม.4–6** | Higher-education planning, career preparation, personal/social well-being | Clubs, leadership, school projects; Scout continuation is school-dependent | Community engagement and service learning |

### Verification Rules

- Use the official curriculum phrase **`กิจกรรมพัฒนาผู้เรียน`**, not “extra subjects” or “survival class.”
- Translate `ลูกเสือ` as **Scouts** and `เนตรนารี` as **Girl Guides**; describe practical survival skills as possible content, not the official identity of the component.
- Do not infer a national fixed hour allocation from one school's timetable. The national framework defines the activity types; school curricula determine the detailed timetable and delivery.
- Treat the number of guidance teachers as a school staffing arrangement, not a national curriculum requirement.
- Distinguish **national framework** from **school implementation** in the note: label school-specific examples as examples.

See `references/thai-learner-development-activities.md` for the official-source map, terminology, grade progression, and evidence boundaries.

### Proven Research and Placement Workflow

For this component, search the official OBEC curriculum hub and Guidance Development Group with SearXNG first, then read the selected official PDF or page with `mcp__searxng__web_url_read`. Use the search result only to locate the source: distinguish what the national document establishes from what a sample school's timetable demonstrates. If a query returns no results, vary the query rather than concluding that the activity is absent.

Place the BOK overview at `body-of-knowledge/Student Development Activities/`, separate from academic subject BOKs. Keep detailed implementation or future topic notes in the corresponding non-BOK content root if the user later requests them. Do not put Scout or Guidance notes inside Social Studies merely because both concern citizenship or development; use cross-links instead.

## Step 9f — Closing an Audit-Flagged Partial BOK Subject (Supplementary-Root Pattern)

When a vault audit flags a subject 🟡 Partial because only a *supplementary* root exists (e.g., `English Skill/` teaching-ordered notes) while the BOK's own curriculum strands have zero content notes, do NOT expand the supplementary root. Proven 2026-08-28 for English: created `English Curriculum/` (28 files) to close the finding "4-strand curriculum notes still absent".

1. **Read the audit finding and the BOK overview first.** The BOK's topic tables are the contract — build exactly one note per enumerated concept area (24 for English), not a list from memory.
2. **Keep the supplementary root untouched** as a sibling content root; create a NEW root named after the subject (`English Curriculum/`), one folder per strand.
3. **Cross-link bidirectionally into the supplementary notes** (curriculum note ↔ skill deep-dive by FILE name). The two systems interlink instead of duplicating.
4. **Decide the numbering scheme BEFORE the first write** — see the Step 9b numbering pitfall. Mirror the closest sibling content root.
5. **Topic note shape:** YAML with strand + มาตรฐาน codes (อ1.1–อ4.2 for English), grade-band table (ป.1–3 → ม.4–6), Mermaid progression, Thai-speaker difficulty section, Thai terminology, cross-links. English subject → English text.
6. **Write 00_overview.md trackers LAST**, then wire the BOK overview: a "Curriculum Content Notes" wikilink table under each strand section + strand-overview links in Related. NEVER reference content as inline-code paths — audits flag link-graph orphans (their finding N1); use path-qualified links for ambiguous basenames like `00_overview` (finding N2's own recommendation).
7. **QA gate before reporting closure:** file count vs BOK concept-area count, size scan (3.9–7.3 KB per note here), Thai-Latin + CJK artifact greps, and a full wikilink resolution check — see `scripts/verify_vault_links.py`.

**Pitfall — numbering drift mid-build:** creating files before locking the numbering plan forced a rename of 3 strand-3 files (19–21 → 13–18) and fixing 7 broken links on 2026-08-28. Lock the scheme first.

## Step 10 — What Comes Next (Topic Note Filling)

After the user approves the overview structure, they may ask to fill in the individual topic files behind each `[[wikilink]]`. This is handled by `educational-content-authoring` (see "BOK Topic Note Filling" workflow variant).

Key points for the handoff:
- **Topic notes go in a DIFFERENT vault path** than the BOK overviews. Example: overviews in `body-of-knowledge/Fundamental Mathematics/`, full notes in `Mathematics/`. **CRITICAL: The user corrected this explicitly** — do NOT put topic notes inside `body-of-knowledge/`. Topic notes go in the main content folder (e.g., `F:\obsidian_note\general-knowledge\Social Studies\`, NOT `F:\obsidian_note\general-knowledge\body-of-knowledge\Social Studies\`).
- **Group topic notes by subject/strand.** After creating topic notes, the user will ask to group them into subject folders matching the BOK strand structure. Example for Social Studies: `01 Religion/`, `02 Civics/`, `03 Economics/`, `04 History/`, `05 Geography/`. Move files with `mv` into subfolders, then `rmdir` empty old folders. The user explicitly requested this grouping.
- **For spiral curriculum (ป.1-ม.3):** Each topic file covers all 3 grade bands with a progression table — don't split by grade.
- **For linear curriculum (ม.4-ม.6):** Each topic file covers one year's content.
- Use `delegate_task` with parallel subagents to research topic batches (split into 2 batches of ~10 topics each).
- **Confirm style before creating:** The user may want swe-knowledge style (YAML frontmatter with `source:`, hierarchical sections, cited, professional) or English Skill style (concise, table-heavy, Thai terminology). Ask explicitly.
- **Always verify and fix after grouping.** Run `sed` to fix double-backslash LaTeX issues. Check Mermaid syntax. Replace ASCII diagrams with Mermaid. Then verify the final file count and structure.
- **User may expand scope from ป.1-ม.3 to ม.6.** Initially create topic notes for ป.1-ม.3 (fundamental level). The user will often later ask to expand overviews to include ม.4-ม.6. When this happens, update the concept area tables to add a ม.4–6 column and update progress trackers. Topic notes for ม.4-ม.6 can be created later — the overview just needs the grade band column.
- **User may request post-fix passes:** After file creation, the user often requests: (a) replacing ASCII diagrams with Mermaid, (b) fixing LaTeX rendering errors, (c) replacing specific diagrams with better Mermaid types (e.g., `gitGraph` for number lines, `quadrantChart` for quadrants). Budget time for this — it's part of the workflow, not a surprise.
- **User may reorganize folder structure mid-project.** A common pattern: start with flat topic files in one folder, then the user asks to split into subfolders by level (e.g., `Fundamental/` for ป.1–ม.3, `Advance/` for ม.4–ม.6). When this happens, create the subfolders, `mv` existing files in one batch, then create new files in the new subfolder. Wikilinks across subfolders resolve automatically in Obsidian (no path changes needed). Confirm the split structure with the user before moving — flat vs. by-grade-band is a user preference.
- **Batch-create new topic notes with `execute_code` + `hermes_tools.write_file`.** When creating 10+ files of consistent format, use `execute_code` with a Python script that builds the full file content as Python string variables (one per file) and calls `hermes_tools.write_file` for each. Proven: 23 files in ~12 runs (2 files per run), ~3 seconds per run. Each file follows the same 6-section template (YAML → coverage table → terminology → concepts → problems → cross-links). This is much more reliable than `delegate_task` for content you can produce from model knowledge — no research subagent needed, no context pollution from subagent transcripts.
**Subject-folder-per-topic pattern (user preference, proven 2026-07-30).** For multi-subject content vaults (Science with Physics/Chem/Bio/EarthSci/CS), the user prefers **one subfolder per subject** mirroring the Social Studies pattern (`01 Religion/`, `02 Civics/`). The folder name uses the subject English name (or close to it — the user once wrote `physic/` for `physics/`). Layout (COMPLETE as of 2026-07-30, 85 advanced notes):
```text
Science/Advance/
├── physic/            ← 23 notes, ม.4-ม.6 ว301-ว303
├── Chemistry/         ← 20 notes, ม.4-ม.6 ว311-ว313
├── Biology/           ← 20 notes, ม.4-ม.6 ว321-ว323
├── Earth_Science/     ← 10 notes, ว341 elective
└── Computer_Science/  ← 12 notes, ม.4-ม.6 ว331-ว333
```
  The BOK overviews continue to use **short wikilinks** (`[[01_Measurement_and_Scientific_Method]]`, NOT `[[Advance/physic/01_Measurement_and_Scientific_Method]]`) because Obsidian resolves wikilinks by filename. Long paths add visual noise without functional benefit. **Pitfall:** When patching BOK overview wikilinks in Phase 3, the first `execute_code` attempt's `hermes_tools.write_file` calls can silently fail due to the dedup cache (the file was read earlier in the session). Symptom: script exits 0, but `grep` shows the original short links unchanged. **Fix:** use direct Python `open()/read()/write()` in `execute_code` for batch wikilink patching — that bypasses the dedup cache. Always verify with `grep -c 'Fundamental/'` (or `Advance/`) afterward.
- **Fundamental/Advance split may NOT be subject-grouped.** When the user says "the fundamental can be there, in case student want to read up to ม3, so not restructuring" — keep fundamental as a single flat folder of integrated content (covering all subjects) for the integrated ป.1-ม.3 curriculum. Only the **Advance** folder needs subject grouping. The BOK `00_Fundamental Science - Overview.md` links to flat `[[Fundamental/01_Scientific_Method]]` and the user keeps this. Don't second-guess — when the user says "leave it," leave it.
- **For 20+ advanced science notes, use 3 parallel `delegate_task` subagents instead of `execute_code`.** When creating 20+ notes that require accurate physics/chemistry/biology content (not just template-filling from model knowledge of simple math), dispatch 3 parallel subagents via `delegate_task` with `tasks` array. Each subagent gets 6-8 topics, the 5-section template, and a topic content guide. Proven across ALL 5 subjects (2026-07-30): Physics (23 notes ว301-ว303, ~3 min), Chemistry (20 notes ว311-ว313), Biology (20 notes ว321-ว323), Earth Science (10 notes ว341, 2 subagents), Computer Science (12 notes ว331-ว333, 2 subagents). For 10-note batches use 2 subagents (5+5) not 3. See `references/advanced-science-note-pattern.md` for the complete template, all 5 subject topic distributions, subagent sizing rules, and the English-narrative-with-Thai-in-parens style guide.
- **Reorganize vault into Fundamental/Advance folders when expanding from ป.1-ม.3 to ม.4-ม.6.** When the user asks to expand a subject from fundamental (ป.1-ม.3) to advanced (ม.4-ม.6) coverage, split the flat folder into `Fundamental/` and `Advance/` subfolders (mirroring the Mathematics structure). Move existing notes with `mv` in one batch, then create new advanced notes in `Advance/`. After moving, update BOK overview wikilinks with path prefixes (`[[Fundamental/01_Topic]]`, `[[Advance/01_Topic]]`). Use `execute_code` with direct Python file I/O (not `hermes_tools.write_file`) for batch wikilink patching — the dedup cache can block writes to files read earlier in the session. See `references/advanced-science-note-pattern.md` for the batch patching script and verification pattern.

## Pitfalls

### Structural
- **Don't cram multiple subjects into one file** — one subject per folder, one overview per folder
- **Don't skip the mermaid diagram** — it's the most valuable part for showing relationships
- **Don't use vague folder names** — "Science" is bad, "Fundamental Science" or "Physics" is good
- **Don't forget course codes** — they're essential for curriculum alignment
- **Don't mix levels in one overview** — keep ป.1-ม.3 separate from ม.4-ม.6
- **Don't create topic files before the overview is approved** — overview first, then depth
- **Don't confuse spiral vs linear curriculum** — if each grade band revisits the SAME concepts (just deeper), use concept-area organization. If each year covers DIFFERENT topics, use year-based organization.
- **Choose the right language for each BOK.** Thai subject (ภาษาไทย) → write in Thai. English subject (ภาษาอังกฤษ) → write in English (even for Thai students — the user corrected this explicitly). Math-science → English with Thai terminology as needed. This is NOT optional — the user will ask you to rewrite if wrong.
## Step 11 — Non-Academic BOK Subjects (Arts, Health & PE, Career & Technology)

When the user's BOK covers ALL 8 Thai basic education learning areas, the remaining 3 (Arts, Health & PE, Career & Technology) need overview files too. These use the **same academic format** as other subjects — NOT a simplified parent-focused format.

### When to Use

- User has built BOKs for core subjects (Math, Science, Thai, English, Social Studies) and asks "what else?"
- User says the "out of scope" subjects should be included
- User wants comprehensive curriculum coverage

### Format — Same as Academic Subjects

**CRITICAL: The user explicitly rejected a "parent-focused" format with "What You Can Do at Home" columns.** They want the SAME format as Mathematics, Science, etc. — concept area tables, grade band progression, Thai terminology, cross-links, Mermaid diagrams. The PURPOSE may be parent-child communication, but the FORMAT must be academic.

Each overview file should have:

1. **YAML frontmatter** with tags, source, duration
2. **Overview paragraph** explaining the subject
3. **Domains/Strands summary table** — what the subject covers
4. **Concept area tables** — one per domain/strand, with grade band columns (ป.1–3, ป.4–6, ม.1–3, ม.4–6)
5. **Grade band progression table** — summary across all domains
6. **Key Thai terminology table** — Thai → English
7. **Mermaid diagram** — showing domain interconnections
8. **Cross-links** — to related subjects and back to master overview

### Covered Subjects

| Subject | Domains | Notes |
|---|---|---|
| **Arts (ศิลปะ)** | Visual Arts, Music, Performing Arts | 3 domains, ~15 concept areas |
| **Health & PE (สุขศึกษาและพลศึกษา)** | Health Education, Physical Education | 2 strands, ~14 concept areas |
| **Career & Technology (การงานอาชีพ)** | Home Economics, Agriculture, Crafts, Career, Technology | 5 strands, ~22 concept areas |

### Proven Career and Technology Filling Pattern

When filling the existing Career and Technology overview, preserve its actual wikilinked topic list and use a Social Studies-style content root outside `body-of-knowledge`. The proven layout is:

```text
work-careers-technology/
├── 01 Home Economics/
│   ├── 00_overview.md
│   └── 01-04 topic notes
├── 02 Agriculture/
│   ├── 00_overview.md
│   └── 05-09 topic notes
├── 03 Crafts and Industry/
│   ├── 00_overview.md
│   └── 10-13 topic notes
├── 04 Career Education/
│   ├── 00_overview.md
│   └── 14-17 topic notes
└── 05 Technology/
    ├── 00_overview.md
    └── 18-22 topic notes
```

For the current Thai Career and Technology overview, this produces 5 strand overviews and 22 topic notes. Do not invent additional topics merely because a parent overview says "~25" when only 22 concrete wikilinks exist. Preserve the existing numbering across strand folders, use `00_overview.md` progress trackers, and create the detailed notes in the separate `work-careers-technology` root rather than under `body-of-knowledge`.

Each strand overview should include: YAML frontmatter with OBEC source and strand, a concept-area table, four grade bands, a Mermaid progression diagram, a progress tracker, related links, and sources. Each topic note should include: English-first narrative with Thai terms in parentheses, grade-band breakdown, concept or process tables, safety/ethics where relevant, one hands-on project, Thai terminology, Mermaid flowchart, cross-links, and authoritative sources.

For source research, use the OBEC Basic Education Core Curriculum as the curriculum anchor. Use IPST Computing Science and technology pages for the Technology strand, then add authoritative sector sources where the topic needs current safety, health, labour, agriculture, or information-literacy guidance. A search result URL and source citation can be retained when full page extraction is unavailable; do not let a source-fetch issue block creation when the curriculum structure is already verified.

See `references/career-technology-topic-pattern.md` for the complete topic inventory, file layout, note template, source map, and verification checklist.

See `references/career-path-overlay-pattern.md` for the career-path overlay note pattern: creating senior-level application notes that layer on top of existing BOK foundations (SWEBOK, PMBOK, BABOK) without duplicating them. Proven for Senior SWE Technical Ownership (7 files, 56.6 KB). Includes folder structure, topic note template, BOK anchoring table, and proven file sizes.

### Pitfalls

- **Don't use parent-focused columns** ("What Your Child Learns", "What You Can Do at Home"). The user wants standard academic tables with concept areas and grade bands.
- **Career and Technology is a Social Studies-style exception to the integrated-subject rule.** Organize it into five strand folders with one `00_overview.md` and numbered topic notes per strand. Do not create an additional hierarchy beneath those strand folders unless the user explicitly requests it.
- **Don't split into sub-overviews.** Arts, Health, and Career are integrated subjects — one overview per subject is sufficient.
- **Don't skip concept area tables.** Even though these aren't exam-focused, they still need structured topic breakdowns.
- **Language:** Write in English with Thai terminology where needed. Only Thai language subject (ภาษาไทย) must be written in Thai.

- **Cross-links in sub-overviews** use relative wikilinks: `[[01_Physics - Overview|Physics]]` for main overviews, `[[05 Mechanics|Mechanics]]` for sub-categories. For cross-BOK links, use the full filename: `[[03_Biology - Overview|Biology]]`.

### Diagram Formatting (CRITICAL — user preference)
- **PREFER MERMAID OVER ASCII.** The user wants Mermaid diagrams in Obsidian notes, not ASCII box-drawing. Replace `├──`/`└──` trees, hand-drawn number lines, and box-drawing with proper Mermaid diagrams. Key patterns from this session:
  - **Factor trees** → `flowchart TD` with `A["84"] --> B["2"]` style arrows
  - **Number lines** → `gitGraph` with `commit id: "-3"` nodes (use `type: HIGHLIGHT` for zero/ellipsis, `"..."` for terminal ellipses)
  - **Real number hierarchy** → `flowchart TD` tree with subgraphs (ℕ→ℤ→ℚ→ℝ, irrationals as sibling)
  - **Quadrant diagrams** → `quadrantChart` with `quadrant-1` through `quadrant-4` (hyphenated numbers — NOT `quadrant I` or `quadrant "Q I"` — those produce syntax errors). Use `[nl]` in labels for newlines. **CRITICAL:** y-axis direction in Mermaid quadrantChart is `y-axis "bottom-label" --> "top-label"`. So for standard Cartesian (positive-y up): `y-axis "y (negative ↓)" --> "y (positive ↑)"`. The first quoted string goes at the bottom, second at the top. Also: `x-axis "left-label" --> "right-label"`. Failure to get y-axis direction right is the #1 user-reported bug.
  - **Venn diagrams** → `flowchart TD` with nested `subgraph` blocks and `-->` arrows to show overlap regions
  - **Probability scales** → `flowchart LR` with chained `-->` nodes
- **Check Mermaid syntax against official docs (mermaid.js.org).** For newer chart types (`quadrantChart`, `gitGraph`), verify syntax matches current spec. The user catches syntax errors.
- **ASCII is acceptable for simple alignments.** Use plain code blocks (` ``` `) for: column arithmetic, decimal addition alignments, and short text diagrams where Mermaid would be overkill.

### LaTeX / Math Formatting (CRITICAL — Obsidian rendering)
- **`write_file` behavior:** The `write_file` tool writes content literally. Single backslashes in source (`\frac`) → single backslashes in file → correct rendering. Double backslashes in source (`\\frac`) → literal `\\frac` on disk → broken rendering as "f ac a b". **Rule: always use single backslashes in LaTeX commands.** `\frac`, `\times`, `\div`, `\sqrt`, `\boxed`, `\mathbf`, `\text`, `\begin{aligned}`, `\end{aligned}`.
- **Formula-in-table pattern (user-preferred):** Use `$$...$$` inside table cells for display math formulas. This is the user's established format for Key Formulas sections: `| **Concept** | $$formula$$ |`. Example: `| **Mass-energy** | $$E = mc^2$$ |`. This avoids the fragility of inline math and produces clean, readable formula tables. The user applied this pattern to Modern Physics themselves and it works reliably.
- **Chemical formulas:** Use `$$\ce{CH4}$$` for chemical notation in Obsidian (MathJax mhchem extension — standard in Obsidian). For functional groups: `$$\ce{-OH}$$`, `$$\ce{C=C}$$`, `$$\ce{CH3COOH}$$`.
- **When LaTeX fails, simplify to plain text.** Prefer readability over fragile formatting. Fallbacks:
  - `a/b` instead of `\frac{a}{b}`
  - `(x₁+x₂)/2` instead of `\frac{x₁+x₂}{2}`
  - `m = (y₂−y₁)/(x₂−x₁)` instead of `m = \frac{y₂-y₁}{x₂-x₁}`
  - `√[(x₂−x₁)² + (y₂−y₁)²]` instead of `\sqrt{(x₂-x₁)^2+(y₂-y₁)^2}`
- **`\\` (double backslash) is ONLY correct** as LaTeX line breaks inside `{aligned}`, `{array}`, or `{cases}`. Everywhere else: single backslash.
- **Batch-fix sed:** Run ONCE on newly created files. Verify with `grep -c '\\\\\\\\' *.md | grep -v ':0$'` first. Only apply to files that actually contain `\\`. Fix remaining with `patch` — do NOT re-run sed iteratively (corrupts already-correct content).
- **⚠️ Greek letter corruption in `patch`:** When using `patch` to insert LaTeX with Greek letters (\rho, \lambda, \mu) via `execute_code`, line-wrapping in the patch body can insert newlines between the backslash and the letter (e.g., `\` on one line, `ho` on the next for \rho). This produces visible corruption. **Mitigation:** (1) Keep formula lines short (< 60 chars) in patch strings, (2) After any patch with Greek letters, read back the affected lines to verify, (3) Prefer `write_file` for formula-heavy sections where line-wrapping risk is high. If corruption occurs, re-patch with shorter lines or rewrite the section.
- **Avoid `\left`, `\right`, `\middle`** — fragile in Obsidian MathJax, use plain brackets instead.

### Workflow
- **Two-pass pattern:** When research is slow (2+ min), create initial overviews from your knowledge FIRST, then update when research returns. The user gets something to review immediately. For Thai curriculum, do not assume that search failure means the official source is unavailable: open the governing body's landing page, inspect its direct PDF/HTML links, and use direct retrieval when needed. For IPST Computing Science, start at `https://www.ipst.ac.th/cs`, which exposes the official course descriptions, teacher guide, textbooks, and grade resources. Use Wikipedia only as contextual fallback, never as primary evidence for curriculum status. If an extraction backend reports search-only, switch retrieval method rather than repeating the same search; record what the official source actually supports.
- **Book checklists come after overviews:** Don't skip the book checklist step — the user uses it to find books for future summarizing.
- **Use `delegate_task` for research:** Curriculum research (topic lists, course codes, grade bands) is reasoning-heavy and benefits from subagent isolation.
- **For topic-filling (Step 9):** Use 2 parallel subagents to research ~10 topics each. Write files in swe-knowledge style (detailed, source-cited) for math-sci content. Put topic files in the user's specified destination (e.g., `Mathematics/`, NOT inside `body-of-knowledge/`). Confirm format preference BEFORE writing — the user may want swe-knowledge style (YAML frontmatter with source, hierarchical, professional) or English Skill style (concise, table-heavy, Thai terminology).

## References

- Thai IPST curriculum: [ipst.ac.th](https://www.ipst.ac.th) (free textbooks)
- Thai course code system: ค=Math, ว=Science, ท=Thai Language, อ=English, ส=Social Studies; 1xx=primary, 2xx=lower secondary, 3xx=upper secondary
- See `references/thai-curriculum-structure.md` for detailed Thai curriculum cross-reference with AP/IB/A-Level
- See `references/thai-career-technology-curriculum-research.md` for the official-source-first workflow, the Order 921/2561 status correction, grade-band progression, applied-topic classification, safety source bank, and blueprint quality gates for Crafts and Industry and Career Education topics.
- See `references/thai-book-recommendations.md` for book recommendations, publishers, and exam prep details
- See `references/ipst-math-concepts-01-10.md` for pre-researched IPST Fundamental Math curriculum: grade-band breakdowns, Thai terminology tables, key formulas, worked examples, and cross-links for concepts 01-10 (Numbers through Algebraic Thinking). Saves re-researching the same 10 concept areas.
- See `references/ipst-math-concepts-11-20.md` for the companion reference covering concepts 11-20 (Basic Algebra through Mathematical Processes): includes all formula references (Pythagorean, distance/slope, volume/surface area, mean/SD), probability rules, set operations, Polya's problem-solving steps, and integration matrix showing how Mathematical Processes connects to every strand.
- See `references/latex-formatting-obsidian.md` for LaTeX formatting rules: single vs double backslash behavior, `write_file` literal writing, batch sed fix commands, fallback-to-plain-text patterns, and common LaTeX pitfalls in Obsidian MathJax.
- See `references/latex-formula-table-pattern.md` for the LaTeX formula-in-table pattern: using `$$...$$` inside table cells for Key Formulas sections, correct syntax examples for physics/chemistry/math, and common formula types with their LaTeX representations.

- See `references/mermaid-patterns-for-obsidian-math.md` for tested Mermaid diagram patterns: factor trees (flowchart), number lines (gitGraph), number hierarchies (flowchart tree), Venn diagrams (subgraphs), probability scales (flowchart LR), and quadrant charts (quadrantChart).
- See `references/thai-language-curriculum.md` for the Thai language BOK structure: 5 strands (การอ่าน, การเขียน, การฟังการดูและการพูด, หลักการใช้ภาษาไทย, วรรณคดีและวรรณกรรม), grade bands (ป.1-ม.6), key literature works by level, and Thai language components. Use this when building a Thai language curriculum BOK.
- See `references/thai-language-topic-note-pattern.md` for the fully-Thai topic note template (YAML, 6-section body, mermaid rules, batch creation via execute_code), strand-by-strand workflow for ~78 notes, content filter workaround, and completion tracker for all 5 strands. Use this when filling in ภาษาไทย topic notes.
- See `references/thai-language-session-progress.md` for the current completion status of the ภาษาไทย vault (2/5 strands done as of 2026-08-02), next session resume point, and session learnings (duplicate filename pitfall, SearXNG integration strategy).
- See `references/thai-social-studies-curriculum.md` for the Social Studies BOK structure: 5 strands (ศาสนาฯ, หน้าที่พลเมืองฯ, เศรษฐศาสตร์, ประวัติศาสตร์, ภูมิศาสตร์), course codes (ส11101–ส33102), grade bands (ป.1-ม.6), and spiral model across all 12 years. Use this when building a Social Studies curriculum BOK.
- See `references/thai-social-studies-topic-notes-pattern.md` for the Social Studies topic note creation pattern: 5 strands, YAML frontmatter with strand/course_codes, grade band tables, strand-specific content (Buddhist doctrine, government structure, economics, Thai history, geography), and example topic list
- See `references/thai-social-studies-progress-tracker-pattern.md` for the Social Studies progress tracker pattern: 00_overview.md template with completion tracking, folder structure with independent numbering, and continuation guide for other educator agents
- See `references/strand-completion-workflow.md` for the proven two-phase workflow when completing a partially-done strand (Phase 1: create pending files, Phase 2: add ม.4-6 to existing files, Phase 3: update tracker). Includes quality checks (truncation, YAML corruption, cross-link verification) and proven strand size reference table.
- See `references/advanced-science-note-pattern.md` for the advanced science note template (5-section format for ม.4-ม.6), IPST Physics topic distribution (verified via SearXNG → smartmathpro.com), parallel subagent batching pattern for 20+ notes, IPST Chemistry/Biology/Earth Science topic distributions, and wikilink path-prefix update script for Fundamental/Advance folder reorganization.
- See `references/thai-history-strand-reference.md` for the History strand (สาระที่ 4) curriculum: 15 concept areas, seven มหาราช kings, key historical dates (พ.ศ./CE), calendar conversion formula, Mermaid patterns for timelines/dynasties, and cross-strand connections.
- See `references/thai-geography-strand-reference.md` for the Geography strand (สาระที่ 5) curriculum: 14 concept areas, six regions of Thailand, key geographic features, three seasons, climate change impacts, Mermaid patterns for geographic processes, and cross-strand connections.
- See `references/thai-english-curriculum.md` for the English BOK structure: 4 strands, grade bands with hour allocations, language choice rule (English overviews must be in English — user correction from session), exam structure (O-NET, A-Level, TOEFL, IELTS, TOEIC, CU-TEP, TU-GET).
- See `references/vault-link-verification.md` for the post-creation QA gate: reusable wikilink resolution checker (execute_code, handles `[[note\|alias]]` table escapes and vault-root-relative path links), artifact grep set, false-positive notes, and the 2026-08-28 English Curriculum closure log (28 files, 249 links).
- See `references/thai-math-strand-overview-pattern.md` for the proven strand sub-overview template used across 10 Mathematics files: per-sub-strand structure with grade bands, Thai terminology, misconceptions, real-life connections, exam relevance, and IPST references. Copy this when creating strand-level sub-overviews for any subject.
- **Thai language domain — write overviews in Thai.** When the curriculum IS Thai language (ภาษาไทย), write all overviews and topic files in Thai. When the curriculum is math-sci for Thai students, write in English with Thai terminology as needed.
- **English language domain — write overviews in English.** When the curriculum IS English (ภาษาอังกฤษ), write all overviews in English — even when the user is Thai and the audience is Thai students. The user corrected this explicitly. Thai language overviews = Thai. English language overviews = English. Math-sci = English with Thai terminology as needed.
- **Cross-vault format adaptation (proven 2026-08-02).** When the user points to an existing vault format (e.g., `oralita_md/musical/`) and says "adapt to this subject," study the source format's structure — overview files, individual entry notes, detail tables, cross-references — then map each element to the target domain. The musical format (era overview + song note with lyric-translation-detail table) mapped cleanly to literature (era overview + work note with classical-passage-modern-Thai-detail table). This technique produces richer hierarchical structures than flat numbered files for content that has natural groupings (by era, by author, by artist). The user explicitly validated this approach: "i think it makesense to represent this way, what do you think."
