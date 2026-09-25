---
name: educational-content-authoring
description: "Scan existing Obsidian vaults for content gaps against a learning goal, then create structured educational notes following consistent templates. For building study guides, course notes, and skill-building knowledge bases."
tags: [education, obsidian, content-authoring, notes, ielts, toefl, language-learning, study-guides, swebok, babok, pmbok, gap-analysis, reading-list, frameworks, thai-curriculum, math-sci, ipst]
---

# Educational Content Authoring

Scan existing Obsidian note collections for content gaps against a learning goal (exam prep, skill development, curriculum coverage), then create structured educational notes that fill those gaps.

## Bulk Note Creation Workflow (for 20+ notes per subject)

When building out a complete subject vault (e.g., 23 Physics notes, 20 Chemistry notes, 20 Biology notes), use parallel subagent delegation to speed up the process:

### Parallel Delegation Strategy
- **Split by topic range**: Divide notes into 2-3 logical groups (e.g., "topics 01-10" and "topics 11-20")
- **Use 3 parallel subagents** for subjects with 20+ notes — proven to work well without overwhelming the system
- **Each subagent gets**:
  - Specific topic range and file paths
  - Full context: BOK overview, curriculum codes, style guidelines, cross-linking requirements
  - Template/example note for reference
- **Monitor progress** via live transcript files in delegation cache

### Quality Verification After Creation
- **Count files created**: Use `find` or `ls | wc -l` to verify all expected files exist
- **Spot-check 2-3 notes**: Read beginning, middle, and end sections to verify:
  - Correct language style (English narrative with Thai in parentheses)
  - Proper YAML frontmatter with course codes
  - All 5 required sections present
  - LaTeX math renders correctly
  - Cross-links to related notes work
- **File size check**: Each note should be 6-12 KB; files <3 KB likely incomplete, >15 KB may need splitting

## Systematic Enrichment Pass (Post-Creation)

After initial note creation, run a second pass to add mermaid diagrams where they add value:

### Identify Candidates for Diagrams
- **Classification trees** (`flowchart TD`): taxonomies, types, categories
- **Process flows** (`flowchart LR`): sequential processes, cycles
- **Decision trees**: problem-solving workflows
- **Color-coded patterns**: use `style` directive with fill colors (blue `#e1f5ff`, orange `#fff4e1`, green `#e8ffe1`, pink `#ffe1f4`)

### Parallel Delegation for Enrichment
- **Group by subject**: Physics+Chemistry, Biology, EarthScience+ComputerScience
- **Each subagent reads existing notes**, finds best insertion point in Section 3 (Key Concepts), patches in diagram
- **Verify diagram syntax**: Ensure no parentheses in labels, use `flowchart` not `graph`, no numbered dots like `"1."`

## ASCII to Mermaid Conversion (Quality Gate)

Any problem type that says "draw a flowchart," "trace an algorithm," or shows ASCII art with arrows (`↓`, `→`) should be converted to actual mermaid diagrams:

- **Search for ASCII patterns**: `grep -rn "↓\|→.*→\|START\|END.*↓"` across subject folders
- **Replace with mermaid**: Use proper flowchart syntax with decision diamonds, labeled branches
- **Verify rendering**: Check patched files render correctly in Obsidian

This is a quality gate — text-based flowcharts in problem solutions are incomplete without actual diagrams.

## Linked Files

- **`templates/book-checklist.md`** — Template for framework gap analysis book checklists with priority tiers and status tracking.
- **`templates/swebok-overview.md`** — Template for SWEBOK Knowledge Area overview files (vault scaffolding).
- **`templates/bok-overview.md`** — Template for Body of Knowledge top-level overview files (domain-agnostic: emoji table, mermaid diagram, reading paths).
- **`templates/bok-subject-overview.md`** — Template for individual subject/discipline overview files within a BOK.
- **`references/swebok-v4-books.md`** — SWEBOK v4 canonical book references (47 books across 18 KAs, with priority tiers and already-covered flags).
- **`references/session-pitfalls-2026-07-16.md`** — Lessons from SWEBOK vault restructuring: empty folder handling, cross-linking overviews, index file updates, multi-profile workflow.
- **`references/song-line-alignment-validator.md`** — Python script and patterns for validating English-Thai line alignment in song translation notes. Run after creating/editing any song note.
- **`references/bok-pattern-examples.md`** — Concrete examples of the BOK overview pattern from swe-knowledge (SWEBOK, PMBOK, CyBOK, DMBOK, etc.) showing the table structure, mermaid diagrams, and cross-linking conventions.
- **`references/mermaid-conversion-pattern.md`** — Patterns for converting ASCII diagrams to Mermaid in Obsidian notes. Includes type selection guide, style conventions, and conversion examples.
- **`templates/song-translation-note.md`** — Template for bilingual song translation notes (English lyrics + Thai translation + grammar analysis).
- **`templates/musical-overview.md`** — Template for musical/show overview files: story summary, Mermaid timeline, complete song list, studied-song cross-reference table.
- **`references/thai-math-sci-curriculum.md`** — Thai high school science-math curriculum (สายวิทย์-คณิต ม.4-ม.6) with IPST course codes, topic lists, and AP/IB/A-Level cross-reference. Used for BOK structure creation targeting Thai students.
- **`references/thai-fundamental-math-curriculum.md`** — Thai Fundamental Mathematics curriculum (ป.1-ม.3): 20 concept areas, spiral model, grade bands, course codes (ค111-ค213). Used for BOK topic note filling for foundation math.
- **`references/swe-process-gap-analysis.md`** — Session reference: small project checklist vs SWE theory gap analysis. Includes gap findings, key theory quotes, template sync pattern, and checklist update pattern.
- **`references/swebok-ch01-05-gap-analysis-2026-07.md`** — Session reference: SWEBOK v4 Ch01-05 gap analysis against the `software-engineering-note` vault. Per-chapter coverage tables, specific gaps, and priority-ranked gap list for gap-filling work.
- **`references/swebok-ch11-15-gap-analysis.md`** — Session reference: SWEBOK v4 Chapters 11-15 multi-chapter gap analysis. Includes per-chapter coverage findings, top priority gaps (Formal Methods, Prototyping, Domain-Specific Security, SIPAC), source-book bias observation, and the multi-chapter batch workflow pattern.
- **`references/swebok-ch06-10-gap-analysis.md`** — Session reference: SWEBOK v4 Chapters 06-10 multi-chapter gap analysis. Includes per-chapter coverage findings, top priority gaps (Ch.09 formal PM at ~20% coverage, Ch.10 process assessment, Ch.07 ISO 14764), source-book bias observation, subdirectory discovery note, and cross-comparison to ch11-15 session.
- **`references/swebok-full-gap-analysis-workflow.md`** — Complete end-to-end workflow for full SWEBOK gap analysis + gap filling. Two-phase approach (analyze then fill), parallel subagent dispatch pattern, Coverage Map section template, source-book bias table across all 15 KAs, priority ranking criteria.
- **`references/swebok-ch18-engineering-foundations-gap-analysis.md`** — Session reference: SWEBOK v4 Ch18 Engineering Foundations gap analysis against the `engineering-foundation-note` vault. Two-part vault structure (Physics & Math + SWE Process), Pfleeger textbook coverage pattern, 4 missing topics identified (engineering process, design, abstraction, modeling/simulation), overview update pattern for foundation vaults (table + mermaid + reading paths + coverage map).
- **`references/swebok-ch16-computing-foundations-gap-analysis.md`** — Session reference: SWEBOK v4 Ch16 Computing Foundations gap analysis against the `computing-foundation-note` vault. 9 topics, only 1 missing (Basic Concepts of a System). Vault is extremely comprehensive with 100+ files across 10 subdirectories.

- **`references/thai-fundamental-math-curriculum.md`** — Thai Fundamental Mathematics curriculum (ป.1-ม.3): 20 concept areas, spiral model, grade bands, course codes (ค111-ค213). Used for BOK topic note filling for foundation math.
- **`references/thai-fundamental-science-curriculum.md`** — Thai Fundamental Science curriculum (ป.1-ม.3): 22 concept areas across 4 domains (Process Skills, Life Science, Chemistry, Physics, Earth & Space), spiral model, grade bands, course codes (ว111-ว213), key formulas table, cross-domain connections. Used for BOK topic note filling for foundation science.
- `references/thai-technology-curriculum-research.md` — Source-grounded research notes for Thai Computing Science / Technology blueprints: official IPST links, ว 4.2 grade-band progression, Career & Technology naming caveat, topic-to-indicator mapping, international supplements, and direct-URL recovery workflow.
- `references/thai-arts-curriculum.md` — Thai Arts curriculum (ศิลปะ): 3 strands, standards ศ 1.1-ศ 3.2, the 19 concept areas with Thai names and vault file naming, course codes, condensed terminology (ทัศนธาตุ, instrument families, dance vocabulary, folk dances, Khon/Lakhon/puppetry), legacy-encoded PDF decoding tip, and the BOK expansion pattern.

## When to Use

- User has an existing Obsidian vault of study/educational notes and wants to expand it
- User asks "is this enough for X?" — perform a gap analysis, then fill gaps
- User wants to build a new educational note series from scratch
- User wants to add exam-prep, skill-building, or curriculum-aligned content to existing notes
- User wants to compare their vault against a **reference framework** (SWEBOK, BABOK, PMBOK, CyBOK, etc.) and identify what's missing
- User wants book/resource recommendations to fill knowledge gaps (output is a checklist, not notes)
- User has SWEBOK/BABOK/PMBOK-numbered folders and needs overview/index files for each (vault scaffolding)
- User says "create overview for each one" or "write [topic]_overview.md for all of them"
- User wants a **musical/show overview** with story context for song lesson notes — see Musical/Show Overview Creation variant
- User says "create overview for each of them about story and song" or "what's the story behind [musical]"
- User wants to **create a Body of Knowledge structure** for a new domain (academic curriculum, professional discipline, knowledge area) — see BOK Structure Creation variant
- User says "fill the gap for [subject]" or "create the topic notes behind the wikilinks in the overview" — see BOK Topic Note Filling variant
- User has a **project checklist** and wants it validated against theory notes — see Checklist-to-Theory Gap Analysis variant

## Workflow Variant: Checklist-to-Theory Gap Analysis (Document Templates)

When the user has a **project checklist** (e.g., "what documents do I need for a small project?") and wants it validated against a **reference theory** (SWE process notes, BOK chapters, standards docs), then wants missing templates created/copied to a working directory.

### When to Use

- User asks "is this checklist enough to build X?"
- User has a profile checklist (small/medium/large) and wants gaps identified
- User wants to compare a checklist against theory notes in the vault
- User wants templates copied from a knowledge vault to a project template directory

### Phase 1: Read & Map

1. **Read the checklist** — understand what documents it requires and their priority tiers (🔴/🟡/🟢)
2. **Read the reference theory** — scan the relevant vault section (e.g., `02 SWE Process/`) for process phases, quality attributes, and recommended artifacts
3. **Map checklist items to theory** — for each checklist item, identify which theory section covers it
4. **Identify gaps** — theory recommends artifacts the checklist doesn't list
5. **Assess gap severity** — use the theory's own severity signals:
   - Cost of fixing later (e.g., requirements errors cost 200x after delivery)
   - Explicit warnings/quotes from theory sources
   - Industry standard practice (what most teams do)

### Phase 2: Report Gaps

Present a structured comparison:

```
## ✅ What the Checklist Gets Right
| Theory Area | Checklist Coverage | Verdict |

## ⚠️ Potential Gaps
| Gap | Theory Source | Risk Level | Recommendation |
```

**Key:** Be specific about WHY each gap matters — cite the theory (page numbers, quotes, models). Don't just say "missing X"; say "missing X because theory says Y (source, page Z)".

### Phase 3: Update the Checklist

1. **Add new items** to the appropriate section with correct priority tier
2. **Update the summary table** — recalculate counts per category and total
3. **Update the quick-start checklist** — renumber items, maintain sequential order
4. **Verify consistency** — total in summary must match quick-start item count

### Phase 4: Sync Templates

1. **Check existing templates** in the target directory — list what's already there
2. **Identify missing templates** — compare updated checklist against existing files
3. **Copy from source** — use `cp` for templates that exist in the knowledge vault
4. **Create new** — for gaps where no template exists, create a minimal but complete template
5. **Use consistent numbering** — follow the target directory's naming convention (e.g., `015_definition_of_done.md`)

### Pitfalls

- **Don't forget to update the summary table.** Adding items without updating counts makes the checklist inconsistent. Always recalculate 🔴/🟡/🟢 counts and total.
- **Don't forget to update the quick-start checklist.** If you add 🔴 items, they must appear in the quick-start with correct numbering.
- **Don't create overly detailed templates for small projects.** A small/startup template should be lean — one page, essential sections only. Save the heavy templates for the medium/large profiles.
- **Don't assume the source vault has a template for everything.** Some gaps (like "Definition of Done") may not have a template — create one based on the theory (Scrum Guide, Agile Practice Guide, etc.).
- **Don't use em-dashes (—) in templates.** Use colons (:) per user preference.
- **Preserve the user's existing template numbering.** If their directory uses `011_`, `012_`, continue that pattern. Don't introduce a new convention.
- **Check for duplicate templates before copying.** The target directory may already have the template under a different name or path.

---

## Workflow Variant: Reference Framework Gap Analysis

When the user wants to compare their vault against an **authoritative reference framework** (SWEBOK, BABOK, PMBOK, CyBOK, DMBOK, SEBoK, etc.) and produce a gap report + book checklist (not notes).

### Phase 1: Scan & Map

1. **Read the framework overview** — understand the KAs/chapters/domains it defines
2. **List all vault folders and .md files** — `execute_code` with `os.walk`, excluding `.git`/`.obsidian`
3. **Count .md files per folder** to gauge coverage density
4. **Check substantive depth** — read file sizes and line counts; flag files under ~30 lines as stubs
5. **Map each framework KA to vault content** — produce a three-tier classification:
   - ✅ **Well Covered** — dedicated folder with multiple substantive files
   - ⚠️ **Partially Covered** — some content exists but missing SWEBOK-specific depth/concepts
   - ❌ **Missing** — no learning notes (only the framework reference file itself, if any)

### Phase 2: Report Findings

Present a summary table to the user:

```
| Status | Count | KAs |
|--------|-------|-----|
| ✅ Well Covered | N | ... |
| ⚠️ Partially Covered | N | ... |
| ❌ Missing | N | ... |
```

For each ⚠️/❌ area, specify **what's missing** (concepts, not just topic names).

### Phase 3: Source Books

For each gap area, compile canonical book recommendations:

| Priority | Criteria |
|----------|----------|
| 🔴 Core (1-2) | The industry-standard reference. Most recognized, most cited. |
| 🟡 Supplementary | Adds depth, alternative perspective, or modern practices. |
| 🟢 Deep Dive | Specialized, academic, or reference-only. |

**Book selection criteria:**
- Prefer books widely recognized as canonical in the field
- Check if user already has notes from the book (mark ✅ in checklist)
- Include edition, year, page count for shopping/estimation
- Include a "Why" column explaining what the book covers that fills the gap

### Phase 4: Produce Checklist

Save the checklist as a markdown file in the user's specified folder. Use the **book checklist template** (see Templates section below). Include:
- Suggested vault folder path for where summarized notes should go
- Status checkboxes (⬜/✅)
- Priority tiers
- Top N quick-start list
- Wikilinks back to the framework overview

### Phase 5: Update Memory

After completing a framework gap analysis, save to memory:
- Which frameworks the user is tracking
- Which KAs are covered vs missing
- The user's book-to-notes workflow (find → summarize → place in vault)

---

## Workflow Variant: SWEBOK Overview File Creation

When the user has restructured (or is restructuring) their vault to follow SWEBOK numbering and needs **overview/index files** for each Knowledge Area folder. This is vault scaffolding — not note creation, not gap analysis.

### When to Use

- User has SWEBOK-numbered folders (e.g., `01_Software_Requirements/`, `02_Software_Architecture/`) that lack overview files
- User says "create overview for each one" or "write [topic]_overview.md for all of them"
- User has moved foundation chapters (16-18) to separate vaults and needs overviews there too
- User wants overviews based on the books from the gap analysis checklist

### Overview File Template

Each SWEBOK overview follows this structure (see `templates/swebok-overview.md` for the full template):

```yaml
---
tags:
  - overview
  - swebok
  - [topic-specific-tags]
---
# [KA Name] — Overview
> **Source:** [[SWEBOK v4 - Overview|SWEBOK v4]] Chapter XX — [KA Name]
> **Purpose:** [One-line description]
## What Is This?
[2-3 paragraphs]
## The N Topic Areas
### 1. [[Subtopic_Name]]
- Key concepts
- **Book:** *Title* — Author(s)
## Recommended Books (Priority Order)
| # | Book | Author(s) | Pages | Priority |
## Vault Coverage Map (optional — for folders with existing content)
| Topic | Status | File |
## Relationship to Other KAs
[Wikilinks to adjacent chapters]
## Related
- [[SWEBOK v4 - Overview]]
```

### Phase 1: Scan

1. List all folders in the target vault — `execute_code` with `os.walk`
2. Check which folders already have overview files (search for `*overview*` or `*content*`)
3. Read the SWEBOK overview file to get the full KA list and descriptions
4. Identify which folders need overviews — **empty folders need overviews most** (they serve as roadmaps)

### Phase 2: Check Existing Content

For folders WITH content:
- Read the existing overview to understand its style
- Note what subtopics are covered vs missing
- Include a "Vault Coverage Map" section showing ✅/❌ per SWEBOK topic

For EMPTY folders:
- The overview is a **roadmap** — list all SWEBOK topics with wikilinks to future files
- Include book recommendations per topic (pull from `references/swebok-v4-books.md`)
- These are the most valuable overviews (they define what needs to be built)

### Phase 3: Batch Create

- Use `delegate_task` for 8+ files — pass the full template, book lists, and SWEBOK topic breakdowns in context
- For fewer files, use individual `write_file` calls
- For foundation chapters moved to separate vaults, create overviews in the new vault locations with cross-links back to SWEBOK

### Phase 4: Verify

- Confirm all files were created
- Check wikilinks point to correct paths
- Ensure cross-links between KAs are consistent

### Pitfalls

- **Don't create overviews without reading the SWEBOK overview first.** It defines the canonical KA descriptions.
- **Don't skip empty folders.** Empty folders need overviews most — they're the roadmap for future work.
- **Don't forget foundation chapters.** When chapters 16-18 are moved to separate vaults, they still need overviews with SWEBOK cross-links.
- **Don't mix overview files with note creation.** The user may want overviews now and notes later (multi-profile workflow).
- **Don't use the same book list for every KA.** Pull from `references/swebok-v4-books.md` and filter to the relevant chapter.
- **Don't forget to wikilink between overviews.** Each KA's "Relationship to Other KAs" section should link to adjacent chapters.

---

## Workflow Variant: BOK Structure Creation (Domain-Agnostic)

When the user wants to create a **Body of Knowledge** structure for a new domain — an academic curriculum, professional discipline, or knowledge area — that doesn't map to an existing reference framework like SWEBOK/PMBOK.

### When to Use

- User says "create body of knowledge for X" (e.g., "math-sci student", "data engineering", "game dev")
- User wants to organize a new knowledge domain into a structured vault
- No authoritative reference framework exists (or user doesn't need to map to one)
- The output is a **top-level overview + subject folder structure** with overview files per subject

### Context: Purpose Matters

The BOK's purpose shapes the content. Always clarify:

| Purpose | Style | Content Focus |
|---|---|---|
| **Exam prep** | Concise, formula-heavy, problem-solving | Key formulas, common question types, shortcuts |
| **Parent-child communication** | Accessible, grade-band tables, "what your child learns" | Progressive concepts, Thai terminology, real-world examples |
| **Professional reference** | Detailed, source-cited, standards-based | Depth, cross-references, best practices |
| **Self-study** | Tutorial-like, step-by-step, worked examples | Building understanding incrementally |

**Thai curriculum BOKs** are typically for parent-child communication — parents tracking what their child learns at school. Content should be organized by grade band (ป.1-3, ป.4-6, ม.1-3, ม.4-6) with clear progression.

### File Naming Convention

Use `01_Name_-_Overview.md` pattern with underscores and `_-_` separator before "Overview":
```
01_Buddhist_Principles.md
02_Democracy_and_Government.md
01_Economics_Fundamentals.md
```

Each subject folder gets independent numbering (01, 02, 03...) — NOT globally sequential.

### Grouping Pattern

Group topic notes into subject folders matching the BOK structure:
```
Social Studies/
├── 01 Religion/
│   ├── 00_overview.md              ← Progress tracker + concept area table
│   ├── 01_Buddhist_Principles.md
│   └── 02_Buddhist_Ceremonies.md
├── 02 Civics/
│   ├── 00_overview.md
│   ├── 01_Democracy.md
│   └── 02_Thai_Culture.md
```

### Phase 1: Scope the Domain

Ask clarifying questions (use `clarify` tool):
1. **Level** — High school? Undergraduate? Professional? Self-study?
2. **Scope** — Core subjects only? Or broader including electives/applied fields?
3. **Goal** — Personal reference? Curriculum map? Study guide?

If the user says "use grill-me", use `clarify` with multiple-choice options to narrow scope efficiently.

### Phase 2: Research the Domain

Use `delegate_task` to research what topics the domain covers:
- List all major subject areas (typically 4-8)
- List 10-20 topics per subject area
- Identify how topics are organized (by year, by difficulty, by category)
- Note prerequisites and cross-subject dependencies
- Look for official curriculum codes, standards, or organizing body references

**Key:** Research before creating. Don't guess topic lists — use web search to verify.

**Two-pass pattern:** When research is slow (2+ minutes), create initial overviews from your knowledge FIRST, then update them when research returns. This gives the user something to review immediately while ensuring accuracy later. Use `delegate_task` for research in the background while you create files.

### Phase 3: Create Folder Structure

```python
from hermes_tools import terminal
# Create body-of-knowledge directory and subject subdirectories
terminal('mkdir -p "VAULT_PATH/body-of-knowledge"')
for subject in subjects:
    terminal(f'mkdir -p "VAULT_PATH/body-of-knowledge/{subject}"')
```

### Phase 4: Create Top-Level Overview

Use the **BOK overview template** (see `templates/bok-overview.md`). Key elements:
- YAML frontmatter with tags
- Summary table of all areas (emoji + name + topic count + focus)
- Brief description of each area with `[[wikilinks]]` to subject overviews
- Mermaid diagram showing inter-subject relationships
- Reading paths for different tracks/goals
- Cross-link to other BOKs in the same vault (if any)

### Phase 5: Create Subject Overviews

Use the **BOK subject overview template** (see `templates/bok-subject-overview.md`). Each file includes:
- YAML frontmatter with tags
- "What Is This?" section
- Full topic breakdown with `[[wikilinks]]` to future topic files
- Topic distribution table (by year/semester/category)
- Prerequisites
- Mermaid diagram showing topic dependencies within the subject
- Cross-links to related subjects
- Reading paths for different goals

### Phase 6: Verify & Report

- Confirm all files created
- Count total topics across all subjects
- Report to user with the full structure tree

### Pitfalls

- **Don't skip the research phase.** Topic lists from memory may be incomplete or inaccurate for specific curricula. Use web search or delegate to a subagent.
- **Don't create topic files without user approval.** The overview defines the roadmap; the user decides when to fill it in.
- **Don't use SWEBOK-specific conventions for non-SWEBOK domains.** The BOK templates are domain-agnostic (no "Knowledge Area" jargon, no SWEBOK chapter numbers).
- **Don't forget to ask about level.** A high school curriculum and a graduate program cover the same subject (e.g., Physics) at very different depths.
- **Don't skip the mermaid diagram.** It's the most valuable part — shows how topics connect at a glance.
- **Don't forget reading paths.** Different students have different goals (e.g., "Medicine track" vs "Engineering track").
- **Don't cram all subjects into one file.** One overview per subject, plus a top-level index.
- **Always include the top-level `Body of Knowledge - Overview.md`** as the entry point, even if the user didn't ask for it.

---

## Workflow Variant: Career Capability BOK and Cross-Framework Professional Roadmap

Use this variant when a user has a substantial technical vault and asks what Body of Knowledge to build next for promotion, senior growth, technical leadership, project management, product management, or broader professional capability.

### Core Principle

Build a **career-capability overlay**, not another duplicate technical BOK. Existing frameworks answer different questions:

- **SWEBOK:** how to engineer software
- **PMBOK:** how to manage project work
- **SEBoK:** how to engineer whole systems
- **BABOK:** how to understand needs and define change
- **CyBOK:** how to manage cyber risk
- **DMBOK:** how to manage data as an organizational asset

The overlay answers: **how does a senior technical professional connect technical work to value, lead people, make decisions, and deliver outcomes across these disciplines?** Link back to the source BOKs instead of copying their content.

- **`references/career-capability-bok-pattern.md`** — Session reference: career-capability overlay, domain map, role pathways, source mapping, and applied capstone pattern.
- **`references/career-path-folder-layout.md`** — Proven layout for a root career-path map plus one numbered role folder per path, each containing `00_overview.md`, with explicit folder-aware wikilinks and verification checks.

### Phase 1: Inventory Before Recommending a New BOK

1. Scan the existing BOK root, target technical-note root, foundations, checklists, and document_template library.
2. Count files and inspect representative file sizes. Do not rely on stale overview claims.
3. Read the top-level BOK index, the target technical-note index, and the relevant framework overviews.
4. Search for adjacent coverage such as leadership, product management, enterprise architecture, service management, procurement, finance, organizational change, and technical program management.
5. Inspect existing artifact templates because they reveal practical capability that may not appear in learning notes.

### Phase 2: Reconcile Three Different Statuses

Always separate these dimensions in the report:

| Status | Meaning |
|---|---|
| **Topic coverage** | The concept exists somewhere in the vault |
| **Source-book status** | The canonical or recommended source has been summarized |
| **Applied evidence** | The learner used the concept to produce an artifact or achieve a real result |

A topic can be covered without summarizing its canonical book. A book can be summarized without creating practical capability. Do not treat either as proof of applied competence.

### Phase 3: Identify the Actual Career Target

Distinguish the meanings of PM before deep prioritization:

- **Project Manager:** scope, schedule, cost, risk, governance, procurement, stakeholders
- **Program Manager:** coordinated delivery, dependencies, benefits, cross-project governance
- **Technical Program Manager:** program delivery plus technical integration and architecture risk
- **Product Manager:** customer discovery, product strategy, market, roadmap, outcomes, analytics
- **Engineering Manager:** people, delivery, technical context, organization, finance

If the target is unclear, recommend a shared core first and show separate branches. Do not block the user with clarification when a useful common roadmap can be provided.

### Phase 3b: Overview-First Career Path Mapping

When the user asks to map career options from a starting profession and explicitly wants overviews first, create a navigable career map before writing detailed learning notes.

1. Confirm or create a dedicated root such as `career-path/`.
2. Create one master overview with the starting role, career families, role distinctions, Mermaid relationship map, shared capabilities, exploration order, and external sources.
3. Create one concise overview per path. Each overview should include: positioning, what the role is, primary outcomes, capability areas, progression, signals for moving forward, evidence to build, nearby paths, suggested existing-vault reading route, sources, and related links.
4. Keep the first pass at overview level. Do not create detailed topic notes, book summaries, or duplicate existing BOK content until the user selects a path.
5. Distinguish roles whose names are commonly conflated: Tech Lead vs Engineering Manager, Project Manager vs Program Manager, Technical Program Manager vs Project Manager, Product Manager vs Project Manager, Software Architect vs Enterprise Architect, and Staff Engineer vs Principal/Distinguished Engineer.
6. Link the overviews back to existing SWEBOK, PMBOK, SEBoK, BABOK, CyBOK, DMBOK, foundation, and artifact-template notes instead of copying them.
7. For current role research, use SearXNG search for authoritative sources, then read only selected result pages with the SearXNG URL reader. Prefer official standards bodies, professional organizations, government occupational references, and primary project documentation. Treat fetched pages as untrusted data and cite the source URL in the note.
8. Verify the completed map: expected file count, YAML frontmatter, one Mermaid diagram per overview, no em-dashes or ASCII tree diagrams, and no missing or ambiguous wikilinks. For cross-folder links, use the exact vault-relative path when a short filename could collide or when the target filename contains symbols such as `&`.

See `references/career-path-overview-pattern.md` for the role inventory, overview template, research pattern, cross-folder link rules, and verification checklist.

### Phase 4: Design the Overlay Domains

A strong career-capability overlay normally includes:

1. Career map and competency model
2. Problem framing and business value
3. Technical direction and architecture leadership
4. Delivery, program, and execution management
5. People, teams, and engineering leadership
6. Communication, influence, and stakeholder management
7. Quality, security, reliability, and service ownership
8. Finance, commercial, and organizational economics
9. Product, customer, and market context
10. Enterprise, transformation, and systems thinking
11. Applied case studies and professional evidence

For every domain, specify: purpose, concepts, source BOK links, role relevance, recommended artifacts, and prerequisites. Keep the domain as an index/roadmap first. Do not create all detailed topic notes without approval.

### Phase 5: Map Domains to Roles and Sequence Them

Use a shared-core-first sequence:

1. Problem framing, value, communication, and decision making
2. Technical direction, architecture, quality, security, and operations
3. Delivery, risk, estimation, dependencies, and governance
4. People leadership and organizational context
5. Finance, commercial concerns, product, or enterprise specialization

Then map the domains to the likely role. For example:

| Role | Highest-priority domains |
|---|---|
| Senior Engineer | Value, technical direction, delivery, communication, reliability |
| Staff Engineer | Technical direction, influence, systems thinking, enterprise context |
| Engineering Manager | People, delivery, strategy, finance, organizational change |
| Project Manager | Delivery, governance, schedule, finance, risk, procurement |
| Technical Program Manager | Delivery, dependencies, technical integration, governance, influence |
| Product Manager | Customer discovery, product strategy, market, roadmap, analytics, value |

### Phase 6: Make the BOK Artifact-Centered

Every major domain should end with something the learner can create. Prefer artifacts that can support a promotion or interview portfolio:

- Problem statement and current/future-state description
- Stakeholder map and communication plan
- Business case and value hypothesis
- Architecture Decision Record
- Trade-study report
- Risk and assumption register
- Dependency map and delivery roadmap
- Quality, security, and operational-readiness plan
- Incident review and improvement plan
- Product discovery report or product strategy
- Benefits-realization review
- Retrospective with evidence

Use existing `document_template` files when they exist. Do not create duplicate templates merely because the new BOK has a new name.

### Phase 7: Create a Cross-BOK Capstone

Recommend one integrated capstone instead of disconnected exercises. A suitable capstone includes:

1. Problem and stakeholder context
2. Business objective and expected value
3. Current-state and future-state models
4. System context and architecture options
5. Decision records and trade-offs
6. Scope, roadmap, dependencies, risks, and assumptions
7. Quality, security, reliability, and operational readiness
8. Communication and governance plan
9. Delivery evidence
10. Benefits review and retrospective

This converts a reference library into evidence of senior-level judgment.

### Phase 8: Build the Book Checklist Conservatively

Before recommending books:

1. Search the vault for existing summaries and mark them as already covered.
2. Use one primary source per capability before adding supplementary books.
3. Separate framework references from practical books and deep dives.
4. Explain the exact gap each book fills.
5. Keep the first reading path small. A 47-book list is not a learning plan.
6. Keep book status separate from topic coverage and applied evidence.

### Quality Gates

Before finalizing a career-capability BOK recommendation:

- [ ] Existing technical coverage was scanned rather than assumed
- [ ] Duplicate content is redirected to existing BOKs with wikilinks
- [ ] Project Manager, Program Manager, Technical Program Manager, Product Manager, and Engineering Manager are distinguished
- [ ] A shared core and role-specific branches are shown
- [ ] Each domain has a practical artifact
- [ ] Existing templates are reused where possible
- [ ] A cross-BOK capstone is included
- [ ] Topic coverage, book status, and applied evidence are not conflated
- [ ] The reading list is prioritized and checked against existing summaries

### Pitfalls

- Do not respond to a mature SWE vault by recommending another generic software engineering BOK.
- Do not treat a high coverage percentage as career readiness. Senior capability requires decisions, influence, and evidence.
- Do not use PM as an unqualified label when the distinction changes the roadmap.
- Do not produce a large book list before reconciling what the vault already contains.
- Do not duplicate SWEBOK, PMBOK, SEBoK, BABOK, CyBOK, or DMBOK content. Build the connective layer.
- Do not make the new BOK purely theoretical. Attach each domain to an artifact and an applied case.

---

## Workflow: Note Creation

### Phase 1: Scan & Assess

1. **List all files** — On C:\ drives: `search_files(target='files', pattern='*.md')` under the vault/section. On F:\ drives: use `terminal` with `find "<vault>" -name "*.md" -type f | sort` instead (`search_files` silently returns 0 on F:\ — see BOK Chapter Gap Analysis Phase 3 pitfall).
2. **Read the index/content file** — understand the structure, section organization, and what's covered
3. **Read 4-5 representative files** — assess depth, format, and quality
4. **Identify the learning goal** — ask the user if unclear (exam prep? skill building? reference?)
5. **Gap analysis** — compare current coverage against the learning goal:
   - What topics are well-covered?
   - What critical topics are missing?
   - What topics are present but shallow?
6. **Present findings to user** — honest assessment with specific recommendations
7. **Get approval** before creating new content

### Phase 2: Plan New Content

1. **Design the section structure** — group related topics into logical sections
2. **Number files sequentially** — continue from the existing numbering scheme
3. **Plan each file** — one concept per file (Miller's Law)
4. **Create section folders** — match existing folder naming pattern

### Phase 3: Create Notes

Use the **educational note template** (see below). Create files in batches using `write_file`.

### Phase 4: Update the Index

Update the main content/index file to include all new sections with:
- Section heading
- Wikilinks to each new file with one-line descriptions
- Updated teaching routes (if applicable)
- Updated sources list

## Educational Note Template

Every educational note follows this structure:

```yaml
---
tags:
- [topic-tag]
- [skill-tag]
- [context-tag, e.g., ielts, toefl, academic]
---
```

```markdown
# [Title]

[1-2 sentence introduction — what this topic is and why it matters]

---

## [Core Content Section]

[Explanation with tables, examples, comparisons]

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| data     | data     | data     |

---

## [Additional Sections as Needed]

[More detail, progressive complexity]

---

## ⚠️ Thai Speaker Traps  ← (or relevant L1-interference section)

| Trap | Problem | Fix |
|------|---------|-----|
| ...  | ...     | ... |

---

## Sources

- [Author, Title, Edition, Publisher, Year]
```

### Template Principles

- **YAML frontmatter** — tags for discoverability (topic, skill, context)
- **Tables over paragraphs** — scannable, compare-at-a-glance
- **Examples with ❌/✅** — show wrong vs. right
- **L1-interference section** — if targeting a specific L1 audience, include common mistakes from structural differences
- **Wikilinks** — connect to related notes with `[[Note Name]]`
- **Sources** — cite authoritative references
- **One concept per file** — don't cram related topics together
- **Self-contained** — each file should be useful on its own

## Batching Strategy

When creating 10+ files, use `execute_code` with a Python script:

```python
import os
from hermes_tools import write_file

base = r"F:\projects\orlita_md\English Skill"
files = {
    "09 Vocabulary Building\\28 Academic Word List.md": content_28,
    "09 Vocabulary Building\\29 Word Families.md": content_29,
    # ...
}
for rel_path, content in files.items():
    full_path = os.path.join(base, rel_path)
    write_file(full_path, content)
```

For fewer files, individual `write_file` calls work fine.

## Workflow Variant: Song-Based English Learning

When the user wants to translate English songs to Thai and create learning materials from lyrics — connecting songs to the English Skill curriculum (grammar, vocabulary, collocations, figurative language).

### When to Use

- User has English songs in their vault and wants Thai translations
- User wants to use songs as English teaching materials
- User asks "is this song good for learning English?"

### Note Structure

Songs follow a **dual-section format** — readable first, analytical second:

```markdown
---
song: [Song Title]
source: [Musical / Movie / Artist]
character: [If from a musical]
lesson_type: concept
topic: English Through Songs
audience_level: [beginner | intermediate | advanced]
grammar_focus: [list of grammar points]
prerequisites: [wikilinks to English Skill sections]
related: [wikilinks]
tags: [english, song, ...]
---

# [Song Title]
> from [Source] — sung by [Character/Artist]

## Learning Objectives
[What the learner will gain from studying this song]

## Lyric + Thai Translation

### [Section Name - English]
> [Full English lyrics in blockquote, preserving verse structure]

### [Section Name - Thai]
> [Full Thai translation in blockquote, matching verse structure]

## Lyric + Thai Translation — Detail

### [Section Name — ความหมาย]
| # | English | Thai | หมายเหตุ |
|---|---------|-----|----------|
| 1 | English line | Thai translation | Grammar/vocab note |

## Grammar Points
[Extracted grammar with Thai Speaker Traps]

## Vocabulary Highlights
[Key words + collocations tables]

## Knowledge Connections
[Wikilinks to English Skill sections]

## Key Takeaways
[Numbered lessons from the song]
```

### Phase 1: Evaluate Song Suitability

Before translating, assess the song for English learning value:
- **Grammar richness** — Does it contain multiple tense patterns, conditionals, modals?
- **Vocabulary value** — Does it teach useful everyday words or academic vocabulary?
- **Figurative language** — Metaphors, idioms, personification (high value for Thai speakers)
- **Length** — Short songs (< 20 lines) may be too light; long ensemble numbers (100+ lines) may need trimming
- **Register variety** — Multiple characters = multiple registers (formal, slang, poetic) = higher value

Present the assessment as a table with priority ranking before creating notes.

### Phase 2: Search for Existing Translations

Before translating yourself, **search for existing Thai translations** online. Thai music translation sites (e.g., aelitaxtranslate.com) often have high-quality, natural-sounding translations that are better than AI-generated ones.

1. Search `[song title] แปลเพลง` or `[song title] thai translation`
2. Check known Thai translation sites:
   - **aelitaxtranslate.com** — reliable for musical/theater songs and mainstream pop. Scrapeable with curl.
   - **oldsonghome.com** — has translations for classic/musical songs (cr: movie subtitles). Scrapeable with curl.
   - **bloggang.com** — Thai blog platform with user translations. **Uses TIS-620 encoding** — pipe through `iconv -f tis-620 -t utf-8` when scraping.
   - **Smule** — has karaoke translations but **blocks automated scraping** (requires JS). User must copy-paste text manually from Smule pages.
3. If found: use the existing translation and add an **APA-style reference** (see References section below)
4. If not found: translate yourself, but keep the language natural and colloquial — not stiff textbook Thai

**Encoding notes for scraping:**
- **bloggang.com** uses **TIS-620 encoding** (not UTF-8). When curling, pipe through `iconv -f tis-620 -t utf-8`:
  ```bash
  curl -s -L -A "Mozilla/5.0" "URL" | iconv -f tis-620 -t utf-8 2>/dev/null | sed 's/<[^>]*>//g'
  ```
- **Smule** blocks automated scraping (requires JavaScript). Ask the user to copy-paste the text manually.

> ⚠️ **Pitfall:** AI-generated Thai translations tend to sound stiff and unnatural ("มีช่วงเวลาหนึ่งที่ผู้คนใจดี" vs natural "เคยมีช่วงเวลา ที่ผู้คนนั้นแสนจะโอบอ้อมอารี"). Always prefer existing human translations when available.

### Phase 3: Create the Note

1. Read the existing song file (if any) to preserve any existing content/structure
2. Determine if user wants **bilingual** (English + Thai) or **English-only** notes:
   - **Bilingual:** Write the **Lyric + Thai Translation** section — full lyrics, English verse → Thai verse underneath (blockquotes). Include Thai column in Detail table.
   - **English-only:** Write just **Lyric** section — English lyrics in blockquotes only, no Thai. Detail table has English + grammar notes only (no Thai column). User will translate themselves. Skip all Thai-related validation (CJK check, line alignment).
3. Write the **Detail** section — line-by-line table with grammar notes
4. Extract grammar points, map to English Skill curriculum sections
5. Build vocabulary and collocations tables
6. Add wikilinks to relevant English Skill notes

### Phase 4: Quality Checks

- **No Chinese characters in Thai text** — AI models sometimes produce Chinese (e.g., 殘酷/残酷 instead of โหดร้าย) when generating Thai. This happens even mid-sentence in otherwise correct Thai. After writing ANY Thai text, run this check programmatically:
  ```python
  # Check for CJK characters (Chinese/Japanese) in Thai text
  import re
  cjk = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', thai_text)
  if cjk:
      print(f"FOUND CJK: {''.join(cjk)} — replace with Thai equivalents")
  ```
  Thai text should contain only Thai script (U+0E00-U+0E7F), Latin characters, Arabic numerals, and standard punctuation.
- **No em-dashes (—)** — Use colons (:) instead. The user finds em-dashes unnatural in their notes. This applies to ALL content: headings, table separators, inline explanations, everything. Use `patch(replace_all=True)` to bulk-replace if em-dashes slip through.
- **Thai translation accuracy** — Don't just translate literally; capture the emotional meaning and figurative sense
- **Blockquote formatting** — Use `>` for both English and Thai verses, no tables in the readable section
- **Detail table completeness** — Every line should have English, Thai, and a note explaining the grammar/vocabulary point
- **Source attribution** — When using an existing translation, add an APA-style `## References` section at the top of the note (after the title). Format:
  ```
  Author. (Year, Month Day). *Title in original language*. Site Name. Retrieved Month Day, Year, from URL
  ```
  Example: `Beer. (2013, January 27). *แปลเพลง Les Miserables - I Dreamed a Dream*. AelitaX Translate. Retrieved July 20, 2026, from https://...`
  If no author is known, use the site name. If no date, use `(n.d.)`.
- **Cross-vault links (English Skill references)** — When the song note lives in a vault separate from the English Skill vault (e.g., song in `oralita_md/musical/`, English Skill in `general-knowledge/English Skill/`), use **embedded markdown links** `[name](URL)` pointing to the public GitHub repo instead of Obsidian `[[wikilinks]]`. Wikilinks only work within the same vault. Example: `[05.5 Past Simple](https://github.com/oat431/general-knowledge/tree/main/English%20Skill/02%20Tenses%20%26%20Time/05%2012%20English%20Tense/05.5%20Past%20Simple.md)`
- **Same-vault links (song lesson ↔ overview)** — When linking from the musical overview to a song lesson file **in the same folder**, use short-format wikilinks matching the actual file name: `[[05_I_Dreamed_a_Dream]]`. Do NOT use the full human title with spaces. The `00_overview.md` file and `##_Song_Name.md` files are siblings in the same folder, so short wikilinks resolve correctly in Obsidian.
- **Line alignment validation** — After writing the Lyric + Thai Translation section, validate that English and Thai blockquote groups have matching line counts. Mismatches mean the Thai is on the wrong English line. Run this check:
  ```python
  # Parse blockquote pairs and compare line counts
  # Flag any pair where len(en_lines) != len(th_lines)
  # Common causes:
  #   - Thai translator combined 2 English lines into 1 Thai line (split or annotate)
  #   - Missing Thai line for an English line (add it)
  #   - Extra Thai line (duplicate or misaligned — fix it)
  ```
  Exception: When the source translation naturally combines lines (e.g., 8 EN lines → 5 TH lines), this is acceptable in the blockquote section IF the Detail table provides per-line alignment. Note the discrepancy with a comment.
- **Post-write validation checklist** — After creating/updating a song note, always run:
  1. CJK character check (no Chinese/Japanese in Thai text)
  2. Em-dash check (no — anywhere, use : instead)
  3. Line alignment check (EN/TH line counts match per blockquote group)
  4. Duplicate check (no repeated Thai lines unless the English also repeats)

---

## Workflow Variant: Musical/Show Overview Creation

When the user has organized song lesson notes into folders by **musical/show title** and wants an overview file for each: story summary, complete song list, and context for each studied song.

### When to Use

- User says "create overview for each of them about story and song"
- User has song lesson notes organized by musical (e.g., `musical/Les Misérables/`, `musical/Anastasia/`)
- User wants context for where each studied song sits in the full story

### Phase 1: Scan Existing Structure

1. `find "F:/path/musical" -type f -name "*.md"` — list all song notes
2. `find "F:/path/musical" -type d` — identify which musical folders exist
3. Check if overview files already exist (`*overview*` or `*readme*`)

### Phase 2: Research Each Musical (Wikipedia API)

Use the Wikipedia API for story summaries and complete track/song listings. This is more reliable than scraping fan wikis.

**Story summary (plain text):**
```bash
curl -s "https://en.wikipedia.org/w/api.php?action=query&titles=PAGE_TITLE&prop=extracts&exintro=true&explaintext=true&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(list(d['query']['pages'].values())[0].get('extract','')[:3000])"
```

**Complete song list (from wikitext — preserves track tables):**
```bash
curl -s "https://en.wikipedia.org/w/api.php?action=parse&page=PAGE_TITLE&prop=wikitext&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); w=d['parse']['wikitext']['*']; idx=w.find('Musical numbers'); print(w[idx:idx+5000] if idx>0 else 'NOT FOUND')"
```

**Finding the correct Wikipedia page title** when unsure:
```bash
curl -s "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=SEARCH+TERMS&format=json" | python3 -c "import sys,json; [print(r['title']) for r in json.load(sys.stdin)['query']['search'][:5]]"
```

> ⚠️ **Pitfall:** The `extracts` API sometimes returns empty for newer/niche works (e.g., EPIC: The Musical returned empty on the intro extract but had full content on the full extract). If the intro extract is empty, use `explaintext=true` without `exintro=true` to get the full article text, then locate the Plot section with string search.

> ⚠️ **Pitfall:** For the soundtrack/track listing, the `extracts` API strips table data. Use `action=parse&prop=wikitext` instead — it returns raw wikitext including `{{Track listing}}` templates which are easy to parse for song titles.

### Phase 3: Create Overview File

Use the **musical overview template** (`templates/musical-overview.md`). The overview file is always named `00_overview.md` and lives inside the musical's folder.

**Folder + file naming convention (as of 2026-07):**
```
musical/
├── [Musical Name]/
│   ├── 00_overview.md                         ← overview file
│   ├── 01_Song_Title.md                       ← song lessons, numbered
│   ├── 02_Another_Song_Title.md
│   └── ...
```
The overview cross-references songs using short-format wikilinks matching the file name: `[[05_I_Dreamed_a_Dream]]`, NOT the full human title.

Each overview includes:

1. **About the Musical** table (source, composers, premiere, format, awards)
2. **Story Summary** — 2-3 paragraphs + Mermaid timeline showing chronological flow
3. **Complete Song List** — full table with song number, title, character(s). Mark studied songs with ⭐
4. **English Learning Themes** (new) — table of grammar/vocab/register/idiom value the musical offers as a whole. NOT per-song analysis (that goes in song notes), but the musical's overall learning value
5. **Songs Studied in This Vault** — table linking each studied song to its lesson file + one-sentence context of when it occurs in the story
6. **Sources** — APA format

**"Is it a musical?" edge case:** Some works blur the line (e.g., *La La Land* is a live-action film, not a stage musical). When the user adds one, include a `> **Note:**` callout in the About section explaining why it qualifies as a musical for learning purposes (e.g., "songs advance the story, follows musical structure, draws from classic Hollywood musical tradition").

### Phase 4: Quality Checks

- **No em-dashes** — use colons throughout
- **Wikilinks** — link to song lesson files in the same folder: `[[Song Title - Musical]]`
- **Mermaid timeline** — shows key story events chronologically; helps learners understand when each song occurs
- **Song list completeness** — include ALL songs from the musical, not just studied ones; this makes the overview a useful reference

### Pitfalls

- **Don't guess song lists from memory.** Use Wikipedia or the official soundtrack listing. Musical song lists are long (Les Mis has 40+ songs) and easy to get wrong.
- **Don't skip the Mermaid timeline.** It's the most valuable part for learners — shows where each song fits in the story.
- **Don't forget the ⭐ Songs Studied section.** This is what connects the overview to the lesson notes. Include a one-sentence "context in story" for each.
- **Mark studied songs with ⭐ in the complete list AND in the Songs Studied table.** Dual visibility.

---

## Workflow Variant: BOK Topic Note Filling

When the user has created BOK overviews (via `curriculum-vault-authoring`) with `[[wikilinks]]` to topic files, and now wants to fill in the **individual topic notes** behind those links.

### When to Use

- User says "fill the gap for [subject]" or "create the topic notes for [overview]"
- User has a BOK overview with ~20 topic wikilinks and wants each one fleshed out
- Notes go in a **separate vault location** from the overviews (e.g., overviews in `body-of-knowledge/Fundamental Mathematics/`, detailed notes in `Mathematics/`)
- Content needs to be detailed enough for study/reference — not stubs

### Progress Tracker Pattern

When handing off work to other educator agents, include a **Progress Tracker** section in each `00_overview.md` file:

```markdown
## Progress Tracker

| # | Concept Area | Status | Files Created | Notes |
|---|---|---|---|---|
| 01 | Topic Name | ✅ Done | `01_Topic_Name.md` | |
| 02 | Another Topic | ❌ Pending | — | Brief note on what's needed |

**Completion: X/Y (Z%)**
```

This allows other agents to:
1. See exactly what's done and what's pending
2. Pick up work without re-scanning the vault
3. Track progress across sessions

### Phase 0: Confirm Style

Before creating, confirm the note format with the user:

| Style | When to Use | Features |
|---|---|---|
| **English Skill** | Language learning, beginner content | Tables, Thai translations, ❌/✅ examples, concise (~4-8 KB) |
| **swe-knowledge** | Math-sci, technical, professional | Source-cited, hierarchical headings, detailed (15-30 KB), Thai terminology only where needed |
| **Mix** | Depth + readability | Tables + detailed sections, selective Thai terminology |

**Default for math-sci curriculum: swe-knowledge style** (source-cited, professional). The user explicitly chose this over English Skill style for fundamental mathematics.

### Phase 1: Research Content

For 10+ topics, use **parallel subagents** for research:

1. Split topics into 2 batches (e.g., 01-10 and 11-20)
2. Dispatch both via `delegate_task` with `tasks` array (parallel)
3. Each subagent researches: grade-band progression, definitions, formulas, examples, Thai terminology

**Prompt template per subagent:**
```markdown
Research Thai IPST [Subject] curriculum for concept areas [NN-NN]. For each:
1. Concepts at each grade band (ป.1-3, ป.4-6, ม.1-ม.3)
2. Key definitions, formulas, properties
3. Thai mathematical terminology
4. Common problem types and examples
5. How concepts connect (prerequisites, next topics)
```

### Phase 2: Create Topic Notes

Create each note using `write_file`. **swe-knowledge style template:**

```yaml
---
title: "[Topic Name]"
tags: [subject-tag, concept-area, ipst, thai-curriculum]
source: "IPST (สสวท.) [Subject], หลักสูตรแกนกลาง 2551 (ปรับปรุง 2560)"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [Title]

[Overview paragraph with Thai terminology]

## 1 | [Section]

[Content with tables, formulas, examples]

## Sources

- IPST textbook citation
```

Body structure:
1. Overview with Thai term (e.g., "**Numbers and Numeration (จำนวนนับและระบบจำนวน)**")
2. Grade-band sections (ป.1-3 → ป.4-6 → ม.1-3) with progressive depth
3. Key formulas/properties in tables
4. Worked examples
5. `[[wikilinks]]` to related concepts, prerequisites, and next topics

### Phase 3: Verify

- Confirm all files created: use `terminal` with `find "<dest>" -name "*.md" -type f | wc -l` instead of `search_files` (on F:\ drives, `search_files(target='files')` silently returns 0 results — see BOK Chapter Gap Analysis Phase 3 pitfall)
- Verify each file has non-empty content (no stubs)
- Report created count to user

### Pitfalls

- **Don't create stubs.** Wait for research to complete before writing.
- **Don't skip Thai terminology.** Include Thai terms parenthetically: "**Fractions (เศษส่วน)**".
- **Notes go in a different path than overviews.** Confirm destination with user.
- **Don't use English Skill format for math-sci.** swe-knowledge style is appropriate.
- **Research BEFORE creating.** Topic content must be curriculum-accurate.
- **Use parallel subagents for 10+ topics.** Serial research takes too long.
- **CRITICAL — LaTeX in Obsidian:** Use SINGLE backslashes for ALL LaTeX commands (`\frac`, `\times`, `\div`, `\text`, `\boxed`, `\sqrt`, `\begin{aligned}`, `\end{aligned}`, `\propto`, `\Rightarrow`, `\pm`). NEVER use double backslashes — `\\frac` renders as broken text "f ac a b..." in Obsidian. The ONLY place double backslashes are correct is as line breaks inside `{aligned}`, `{array}`, or `{cases}` environments. **After writing files, run this exact sed command ONCE:** `sed -i 's/\\\\frac/\\frac/g; s/\\\\times/\\times/g; s/\\\\text/\\text/g; s/\\\\boxed/\\boxed/g; s/\\\\sqrt/\\sqrt/g; s/\\\\begin/\\begin/g; s/\\\\end/\\end/g; s/\\\\propto/\\propto/g; s/\\\\Rightarrow/\\Rightarrow/g; s/\\\\pm/\\pm/g; s/\\\\div/\\div/g; s/\\\\%/\\%/g' *.md`. Then verify with `grep -c '\\\\\\\\' *.md | grep -v ':0$'`. **⚠️ Never run sed twice** — it corrupts already-correct content. If the first pass leaves issues, fix remaining files individually with `patch` tool. **Prefer plain-text alternatives** for complex LaTeX: `a/b` instead of `\frac{a}{b}`, `(x₁+x₂)/2` instead of `\frac{x₁+x₂}{2}`, `√[...]` instead of `\sqrt{...}`, `P(A) = n(A)/n(S)` instead of `P(A) = \frac{n(A)}{n(S)}`. Avoid `\left`, `\right`, `\middle` — they're fragile in Obsidian MathJax.
- **CRITICAL — Mermaid over ASCII:** Use Mermaid diagrams for ALL visual structures in Obsidian notes. The user explicitly prefers Mermaid over ASCII art. Obsidian renders Mermaid natively. Key Mermaid types for math education:
  - `flowchart TD` — factor trees, number sets, concept maps, Venn diagrams (with subgraphs)
  - `flowchart LR` — number lines, probability scales, process flows
  - `quadrantChart` — coordinate plane quadrants (x/y axis labels, quadrant labels)
  - `erDiagram` — set relationships, entity mapping
  Avoid: `graph` (legacy), ASCII box-drawing, hand-drawn slash/pipes. After creating notes, verify no ASCII diagrams remain with `grep -E '\\\\──|↦|/  \\\\\\|\\\\/' file.md`.
- **Post-write verification:** After writing all topic files, run: (1) `grep -c '\\\\\\\\' *.md` to check for broken LaTeX, (2) `grep -l '\\─\\|↔\\|↤' *.md` to find ASCII diagrams. Fix any matches immediately.

---

## Workflow Variant: BOK Chapter Gap Analysis (Single or Multi-Chapter)

When the user wants to compare **one or more BOK chapters/KAs** against existing vault section(s) — not the whole framework. This is lighter-weight than the full Reference Framework Gap Analysis: no book checklists, no BOK structure creation, just gap identification and a structured report.

### When to Use

- User says "read [BOK chapter] and review [vault folder]" — compare one KA against one vault section
- User says "perform gap analysis for chapters X-Y" — compare multiple KAs in one session (multi-chapter batch)
- User wants to verify coverage of a specific domain (e.g., "does my computing-foundation-note cover SWEBOK Chapter 16?")
- The vault already has substantial content; the task is verification, not creation

### Phase 1: Read Both Sides

1. **Read the BOK chapter** — extract all knowledge areas, specific topics, and technical terms mentioned
2. **List all vault files** — `search_files(target='files')` for complete inventory; if the vault is on a non-C: drive and `search_files` fails, use `ls -la` via `terminal` instead (see Phase 3 pitfall)
3. **Read overview files** — understand the vault's self-assessed coverage
4. **Depth-sample representative files** — don't read whole large files. Use two fast signals:
   - **File size as depth proxy** — run `ls -la` per folder; files <8 KB are likely thin, 20-45 KB+ are substantive. Flag thin files for closer readings.
   - **`read_file(limit=80)`** on 4-6 representative files — the first 80 lines reveal structure, source, and whether the content has real depth or is a stub.

#### Multi-Chapter Batch Pattern

When analyzing multiple KAs in one session (e.g., "chapters 11-15"), use **parallel batched reads** rather than serial per-chapter loops:

1. **Batch the SWEBOK reference + vault overview reads** — issue `read_file` calls for all chapter reference files AND all vault overview files in a single assistant turn (independent reads, no dependencies). For 5 chapters this is ~10 reads in one round-trip instead of 10 sequential turns.
2. **Then batch 2-3 representative note files per chapter** — read the first 60-80 lines of each to verify depth. Use `limit=60` to keep context manageable; the opening + table of contents is usually enough to judge coverage.
3. **Use a todo list** (`todo` tool) to track per-chapter progress — one item per chapter + a final "compile report" item. Mark each chapter completed as you finish reading its files.
4. **Detect cross-coverage** — when a topic is ⚠️ Partial in one chapter but likely covered in another chapter's notes (e.g., Agile methods listed in Ch.11 but deeply covered in Ch.10 Process notes), note it explicitly. This prevents over-reporting gaps.
5. **Observe source-book bias** — each vault chapter typically leans on one source book (Gomaa for Ch.11, Galin for Ch.12, Anderson for Ch.13, McConnell for Ch.15). This creates predictable blind spots where the source book doesn't align with BOK's full scope. Call this out in the report's observations section.

### Phase 2: Map & Classify

For each BOK topic, classify coverage:

| Status | Criteria |
|--------|----------|
| ✅ Well Covered | Dedicated file(s) with substantive content, multiple concepts explained |
| ⚠️ Partially Covered | Some content exists but missing depth, missing subtopics, or only mentioned in passing |
| ❌ Missing | No file covering this topic |

### Phase 3: Search for Specific Terms

Use `search_files(pattern='keyword', target='content')` to find mentions of BOK-specific terms that might be covered in unexpected files. For example, "Flynn's Taxonomy" might be in Computer Organization even if the BOK lists it under a different section.

**If the vault is on a non-C: drive (e.g., F:\) and `search_files` returns "IO error... path specified"**, fall back to `grep` via `terminal`. This happens consistently on F:\ drives; don't retry `search_files` with different path formats — switch to `grep` immediately:

```bash
cd "F:/obsidian_note/swe-knowledge/vault-folder" && \
grep -l -i -E "keyword1|keyword2|keyword3" 01_Chapter_Folder/*.md
```

Use MSYS forward-slash paths (not `F:\`) — `cd "F:/path"` works in the git-bash terminal.

**Batch keyword checks**: When checking coverage across multiple chapters, batch all grep checks into one `terminal` call with `echo` separators. This avoids 5+ round-trips:

```bash
cd "F:/obsidian_note/swe-knowledge/vault" && \
echo "=== Ch01 formal methods ===" && grep -l -i -E "formal|theorem" 01_Folder/*.md && \
echo "=== Ch02 ADLs ===" && grep -l -i -E "ADL|ArchiMate" 02_Folder/*.md && \
echo "=== Ch03 DSLs ===" && grep -l -i -E "DSL|aspect" 03_Folder/*.md
```

This pattern produced a single readable output block covering 5 chapters in one round-trip.

### Phase 4: Report with Severity

Present gaps with severity levels:

| Severity | Criteria |
|----------|----------|
| 🟡 Medium | Important for SE practice, commonly tested in exams, or frequently needed in industry |
| 🟢 Low | Nice-to-have, specialized, or covered indirectly through related topics |

For each gap, provide:
- What the BOK says (with section reference)
- What the vault already has (specific files)
- What's missing (specific concepts, not just topic names)
- Recommended file path for new content

#### Multi-Chapter Report Format

When analyzing multiple KAs, structure the report as **one section per chapter** plus a **summary table** at the end:

1. **Per-chapter sections** — for each chapter: SWEBOK topic list → coverage status table (✅/⚠️/❌ with vault file references) → specific gaps found → coverage estimate percentage
2. **Summary table** — all chapters in one table: chapter name, total topics, ✅ count, ⚠️ count, ❌ count, estimated coverage %
3. **Top Priority Gaps** — consolidated list of all ❌ Missing items across all chapters, ranked by impact
4. **Key Observations** — cross-coverage patterns, source-book bias, strongest/weakest chapters

The per-chapter coverage estimate percentage helps the user see at a glance which areas need the most work. In practice, coverage ranges from ~55% (heavily biased toward one source book) to ~80% (well-rounded notes).

### Phase 5: Check for "Already Covered Elsewhere"

Some BOK topics span multiple chapters. Before declaring a gap:
- Check if the topic is covered in a different vault section (e.g., distributed systems might be in OS or Networks)
- Check if the topic is covered in a related BOK (e.g., SEBoK might cover what SWEBOK doesn't)
- Use the vault's overview files to see if the user already noted the coverage

### Phase 5b: Update Overview Files with Coverage Maps

After completing the gap analysis, append a **SWEBOK Coverage Map** section to each KA's overview file. This makes the gap analysis persistent and self-service — the user can check coverage anytime without re-running the analysis.

**Anchoring for patch:** Read the last 5 lines of each overview file (`tail -5` via terminal), then use the last unique line as the anchor for `patch`. The patch replaces that line with itself + the new section.

**Coverage Map section format** (append to bottom of each overview file):

```markdown
---

## SWEBOK v4 Coverage Map

> **Source:** [[SWEBOK v4 - Overview|SWEBOK v4]] Chapter XX | **Last analyzed:** YYYY-MM-DD | **Coverage:** ~NN%

| # | SWEBOK Topic | Status | Vault File(s) | Notes |
|---|---|---|---|---|
| 1 | Topic Name | ✅ | `01_File.md` (NN KB) | Brief note |
| 2 | Topic Name | ⚠️ | Overview only | What's thin |
| 3 | Topic Name | ❌ | — | What's missing |

### Gaps to Fill

| Priority | Gap | SWEBOK Topic | What's Missing |
|----------|-----|-------------|----------------|
| 🔴 High | Gap Name | Topic | Specific concepts missing |
| 🟡 Medium | Gap Name | Topic | Specific concepts missing |
| 🟢 Low | Gap Name | Topic | Specific concepts missing |
```

**Batch updating:** Use `execute_code` to apply patches to all overview files at once. For 15 files, this takes ~12 seconds vs 15 individual `patch` calls.

**Also update the main index file** (e.g., `Software Engineering Note Content.md`):
- Replace stale status indicators (e.g., "🔴 Missing notes" for folders that actually have 11 files)
- Add coverage percentages per KA
- Add a priority action list
- Add a mermaid quadrant chart showing coverage vs priority

### Phase 6: Fill Gaps (Multi-Wave Parallel Batch Create)

After the user approves the gap report, fill the gaps using a **multi-wave parallel batching strategy**:

1. **Check cross-vault content first** — Before creating new files, check if related vaults already cover the gap topics. For example, `engineering-foundation-note/02 SWE Process/` may have files on project planning, maintenance, or evaluation that cover SWEBOK KA 09/10/07 gaps. If found, reference them with `[[wikilinks]]` instead of duplicating content.

2. **Sort gaps by priority** — 🔴 Critical first (lowest coverage, highest impact), then 🟡 Medium, then 🟢 Low. Within each tier, prioritize KAs with the lowest coverage %.

3. **Batch into waves of 3 subagents** — Each subagent handles one KA and creates 2-3 files. Three subagents run in parallel per wave. For 7+ KAs, use multiple waves:
   - **Wave 1:** The 3 most critical KAs (lowest coverage, highest impact)
   - **Wave 2:** The next 3 KAs
   - **Wave 3:** Remaining KAs

4. **Pass each subagent a structured prompt** including:
   - Exact file names and SWEBOK topic coverage for each file
   - The vault path and existing file inventory
   - Cross-references to existing notes (wikilink format)
   - Format requirements: YAML frontmatter with `tags: [software-engineering, swebok, kaXX, topic-tag]` and `source: "SWEBOK vX Chapter XX"`, 15-25KB per file, tables, mermaid diagrams, colons not em-dashes, English only
   - Instruction to use `write_file` and confirm success by reading back the first 20 lines

5. **Update overview files incrementally per wave** — Don't wait for all waves. After each wave completes:
   - Patch each KA's overview file: change coverage %, update status table rows from ❌/⚠️ to ✅
   - Patch the main index file: update coverage % and status column for completed KAs
   - Use `patch` tool with targeted old_string/new_string pairs (batch via `execute_code` for speed)

6. **Update the main index summary** — After all waves complete, update the summary section:
   - Recalculate overall coverage percentage
   - Update the priority action list
   - Update the mermaid quadrant chart positions

7. **Report to user** — Summarize what was created, what coverage improved, and what gaps remain.

#### Subagent Prompt Template

```
CREATE THESE N FILES:

1. **filename.md**
Cover: [SWEBOK topics]. SWEBOK KA X.Y.
Source: SWEBOK vX ChXX.

FORMAT:
```yaml
---
tags: [software-engineering, swebok, kaXX, topic-specific-tag]
source: "SWEBOK vX Chapter XX"
---
```

Body 15-25KB. Tables, mermaid diagrams, wikilinks to existing notes. Colons not em-dashes. English only.
For each file use write_file. Confirm success.
```

### Pitfalls

- **Don't declare gaps without searching for specific terms.** A topic might be covered in an unexpected file.
- **Don't confuse "mentioned" with "covered."** A one-line mention in an overview is not coverage.
- **Don't recommend creating files without checking if the vault already has them under different names.**
- **Don't skip reading the overview files.** They often contain "What's Missing" sections that answer the question directly.
- **Don't apply the full Reference Framework workflow to a single-chapter analysis.** This variant is lighter — no book checklists, no BOK structure creation, just gap identification and recommendations.
- **Don't forget to update the overview's progress tracking.** After filling each gap, update the status column and coverage percentage. An overview that says "Pending" when the file already exists erodes trust.
- **Don't wait for all research to complete before creating notes.** Create each note as its research subagent returns. User gets incremental progress instead of waiting for everything.
- **Don't create notes without YAML frontmatter.** Every Obsidian note needs tags and source references for discoverability.
- **When `execute_code`'s `read_file` returns empty content for a file, fall back to `terminal cp`.** This can happen with large files or files created by subagents. The `cp` command reliably copies the content.
- **When `search_files` fails on non-C: drives, switch to `grep`/`find` via `terminal` immediately.** This vault lives on `F:\` and `search_files` consistently fails for any `F:\` path — both `F:\` and `F:/` formats fail. The failure mode differs by target type: `target='content'` returns "IO error... path specified", while `target='files'` returns `{"total_count": 0}` silently with NO error message (more dangerous — looks like the folder is empty when it isn't). Don't retry `search_files` with different path formats; switch to `grep -l -i -E "pattern" folder/*.md` for content search or `find "F:/path" -name "*.md" -type f | sort` for file listing via `terminal` with MSYS forward-slash paths (`cd "F:/path"`). This is a persistent environment quirk, not a transient error.
- **Use file size as a fast depth proxy before reading.** Run `ls -la` per folder early. Files under ~8 KB in a vault where substantive notes run 20-45 KB are likely thin/stub files — flag them for closer reading rather than assuming coverage from filename alone. A chapter with all 4-6 KB files has a depth crisis even if every KA is nominally "covered" by a file.
- **Batch grep checks across chapters into one `terminal` call.** When verifying coverage of 5+ keyword sets across 5+ chapters, don't issue 5+ separate searches. Chain them with `echo "=== Section ===" && grep ...` in one `terminal` command. This turns 5 round-trips into 1 and produces a single scannable output block.
- **For multi-chapter batches, don't read entire note files.** Use `read_file` with `limit=60` to read just the opening + first sections. The full file is rarely needed to judge coverage depth — the overview, TOC, and first 60 lines tell you whether a topic is ✅ (substantive, multiple sections) vs ⚠️ (mentioned in passing) vs ❌ (absent). Reading 6 full 30KB files per chapter across 5 chapters would blow context budget.
- **Don't conflate cross-coverage with coverage.** When a topic appears ⚠️ in Chapter X but is deeply covered in Chapter Y's notes, mark it as ⚠️ with a note "likely cross-covered by Ch.Y" rather than ❌ Missing. The user needs to know the content exists somewhere in the vault, even if not in the "right" folder.
- **Don't trust stale status indicators in index files.** Index files (like `Software Engineering Note Content.md`) may show "🔴 Missing notes" for folders that actually have 11 substantive files. Always verify by listing the actual directory contents before trusting status columns. Update the index as part of the gap analysis.
- **Don't create content without checking cross-vault sources first.** The user's vault may have related content in adjacent vaults (e.g., `engineering-foundation-note/02 SWE Process/` covers PM topics, evaluation, measurement). Before creating new files, check for existing content that can be wikilinked instead of duplicated. This respects the user's existing work and avoids redundancy.
- **`hermes_tools.read_file` may fail on non-C: drives.** When using `execute_code`, `hermes_tools.read_file` with F:\\ paths sometimes returns empty/1-line content. Fall back to `terminal` commands (`tail`, `head`, `cat`) or use the top-level `read_file` tool directly instead.

- **When updating mermaid diagrams in overview files, add BOTH nodes AND edges.** When adding new files to an overview's mermaid diagram, you need two patches: (1) add new node definitions inside the subgraph, (2) add new edge connections after the existing edges. Forgetting the edges means the new nodes float disconnected. Use separate `patch` calls for nodes and edges since they're in different parts of the diagram.

---

## Thai Curriculum Notes: Language Style (CRITICAL)

For Thai curriculum notes (IPST math-sci, ป.1-ม.6), the user's preferred style is **English narrative with Thai in `(...)` parentheses** for technical terms — NOT Thai narrative. This was a confirmed style preference on 2026-07-30 after the user reviewed 23 Physics notes and asked to convert 20 Chemistry notes from Thai narrative to English narrative to match.

**The pattern:**
- **Primary language**: English (prose, explanations, headers)
- **Technical terms**: Thai in `(...)` parens, e.g. "electrons (อิเล็กตรอน)", "nucleus (นิวเคลียส)", "polymers (พอลิเมอร์)"
- **Terminology tables**: Keep format `| Thai | English | Symbol/Notes |` — these tables were already correct in both Physics and Chemistry
- **Course coverage tables**: Scope and Key Skills columns in English (with Thai only where natural)
- **Formulas / LaTeX / `\ce{}`**: Unchanged
- **Wikilinks**: Unchanged

**Why this style:** Parents (Thai speakers) can use the English as the main study text and reference Thai terms for clarity. The Physics notes set the precedent; Chemistry notes were retroactively converted to match.

**When writing new advanced science notes (Physics, Chemistry, Biology, Earth Science, Computer Science), ALWAYS use English narrative with Thai in parens from the start.** Don't write Thai narrative first then convert — that's wasted work. The default style is **English-first**. Proven subjects: Physics (23 notes), Chemistry (20 notes), Biology (20 notes) — all created 2026-07-30.

**When converting existing notes from Thai narrative to English narrative:**
- Dispatch 3 parallel subagents (each handling ~7 files) for batches of 20+ files
- Each subagent needs explicit "before/after" examples to avoid drifting back to Thai
- Specify which sections to convert (prose) vs leave alone (tables, formula, wikilinks)
- Verify after: spot-check first prose line of each note to confirm English-first

## Folder Structure Pattern: Subject Folders (Social Studies Style)

When the user says "i update the [subject] structure like social study" or wants to reorganize a flat content folder into subject subfolders, follow this pattern:

**Social Studies gold standard:**
```
Social Studies/
├── 01 Religion/
│   ├── 00_overview.md         ← progress tracker + concept area table
│   ├── 01_Buddhist_Principles.md
│   └── ...
├── 02 Civics/
│   ├── 00_overview.md
│   └── ...
```

**Applied to Science (2026-07-30 target structure):**
```
Science/
├── Fundamental/                ← integrated ป.1-ม.3, kept flat (one path through)
│   ├── 01_Scientific_Method.md
│   └── 22_Technology.md
└── Advance/                    ← ม.4-ม.6 split by subject
    ├── physic/                 ← ว301-ว303 (23 notes)
    │   ├── 01_Measurement.md
    │   └── 23_Astrophysics.md
    ├── Chemistry/              ← ว311-ว313 (20 notes)
    │   ├── 01_Atomic_Structure.md
    │   └── 20_Industrial_Chemistry.md
    ├── Biology/                ← ว321-ว323 (20 notes)
    ├── Earth Science/          ← (future, ~10 notes)
    └── Computer Science/       ← (future, ~10 notes)
```

**Key rules:**
- **Fundamental level stays flat** — integrated science curriculum, students read it as one path
- **Advance level splits by subject** — each subject gets its own folder matching the BOK structure
- **BOK overviews use short wikilinks** (e.g., `[[01_Measurement_and_Scientific_Method]]`) — Obsidian resolves by filename regardless of path, so no path prefix needed
- **Folder name = subject name** (lowercase like `physic/` or capitalized like `Chemistry/` — match the BOK; user used `physic` and `Chemistry` in 2026-07-30)
- **Numbered prefixes continue within each subject folder** (01, 02, 03...) — independent numbering per subject

## BOK Overview Link Strategy

When BOK overviews reference topic notes that have moved into subject subfolders, the **short wikilink format** `[[01_Topic_Name]]` works in Obsidian. The user prefers this over long paths like `[[Advance/physic/01_Measurement_and_Scientific_Method]]` because:
- Cleaner to read
- Resilient to folder moves (Obsidian resolves by filename)
- Less editing when restructuring

**Don't bulk-update BOK links to include full paths.** If BOK already has short links, leave them. If converting to short links from full paths, use Python regex: `re.sub(rf'\\[\\[{num}_([A-Za-z_]+)(\\|[^]]*)?\\]\\]', lambda m: f'[[{num}_{m.group(1)}{m.group(2) or ""}]]', content)` to strip the path prefix.

**BOK links must resolve to real content filenames.** If the BOK uses bare English names (e.g. `[[Drawing]]`) but the content folder uses numbered prefixes (`01_Drawing.md`), those links break in Obsidian. When expanding/filling a BOK, convert its table rows to filename-style short links (`[[01_Drawing]]`). Verified in the Arts BOK expansion (2026-08-04): 15 name-style links → 19 filename-style links, with continuous row numbering (01-19) across domains in the BOK while content folders keep independent per-folder numbering.

**If the BOK header says "~N concept areas" but lists fewer, expand the tables to the stated N before filling.** The Arts BOK stated ~19 but listed 15; the user approved expansion to exactly 19 (+Thai Traditional Art, +Art History, +Music Composition, +Khon/Lakhon/Puppetry) before the topic notes were filled.

## Parallel Subagent Dispatch for Bulk Note Creation

For batches of 20+ notes (e.g., 23 Physics topics, 20 Chemistry topics, 21 Biology topics), use **parallel subagent dispatch** with `delegate_task(tasks=[...])`:

**Sizing rule:** Each subagent handles 6-8 notes. For 20 notes → 3 subagents (7+7+6). For 23 notes → 3 subagents (8+8+7). For 30+ notes → consider 4 subagents to keep each subagent's context manageable.

**Each subagent prompt must include:**
- Exact file paths (full paths, not relative)
- The exact format template with YAML frontmatter spec
- Per-topic content guide (1-2 sentences per topic)
- Style preference (English narrative with Thai in parens, for Thai curriculum)
- Course codes (e.g., ว311 for Chem S1, ว312 for Chem S2)
- Cross-link format (relative paths from subfolder)

**Two-pass pattern for bulk conversion (e.g., Thai narrative → English):**
- Dispatch 3 parallel subagents simultaneously
- Each one reads assigned files, rewrites, writes back
- After all complete: verify a sample (first line of each note) to confirm format consistency
- Spot-check 2-3 notes deeply for any subagent that drifted

**Pitfall with parallel subagents:** They sometimes skip files or report "no changes needed" if the file already partially matches. Always verify file count after — `find <dir> -name "*.md" | wc -l` should match expected.

### Pitfalls

- **Don't create content without scanning first.** Always understand what exists before adding.
- **Don't skip the gap analysis.** Present findings and get approval before creating 18 files.
- **Don't forget to update the index.** The main content file must reflect all new sections.
- **Don't mix topics in one file.** One concept per file. Use wikilinks to connect.
- **Don't copy-paste the same template mindlessly.** Adapt sections to the topic (not every note needs a "Thai Speaker Traps" — use the relevant L1-interference section for the audience).
- **Don't use paragraphs where tables work better.** Tables are scannable; paragraphs are not.
- **Don't forget wikilinks.** The power of Obsidian is interconnection. Link related notes.
- **Don't number files arbitrarily.** Continue the existing numbering scheme. If existing notes go 01-27, new notes start at 28.
- **Match existing folder naming conventions.** If folders use "01 Foundation" pattern, new folders follow the same pattern (e.g., "09 Vocabulary Building").
- **Don't create notes when user wants a checklist.** Some users use a multi-profile workflow — educator produces analysis/checklists, another profile produces the actual notes. Ask before creating content.
- **Don't skip line alignment validation.** After writing English-Thai blockquote pairs, always verify line counts match. A 7-line English verse with an 8-line Thai verse means something is misaligned. The user's Thai-speaking friends will notice immediately.
- **Don't assume AI-generated Thai is correct.** Always prefer existing human translations. AI Thai tends to be stiff, may contain Chinese characters (残酷 instead of โหดร้าย), and misses idiomatic register (ข้า/เจ้า for epic settings, ฉัน/คุณ for modern settings).
- **Don't use em-dashes (—) in notes.** The user finds them unnatural. Use colons (:) everywhere — headings, table separators, inline explanations. This applies to ALL content, not just song notes. **Exception:** bilingual H1 titles use an em-dash separator (`# Buddhist Principles — หลักธรรมทางพระพุทธศาสนา`, `# Arts — ศิลปะ`) — this matches the vault's established BOK/Social Studies convention; keep em-dashes out of every other line.
- **Don't recommend books user already has notes for.** Check the vault for existing book summaries before adding to the checklist. Mark already-done books with ✅.
- **Save research output as reference files.** When `delegate_task` produces a comprehensive research document (curriculum maps, international comparisons, domain surveys), save it alongside the vault or in the skill's `references/` directory. These are valuable for cross-referencing and future sessions.
- **Use the two-pass pattern for slow research.** When research takes 2+ minutes, create initial overviews from your knowledge first, then update when research returns. User gets something to review immediately while accuracy is ensured later.
- **Don't add checklist items without updating counts.** When adding items to a priority-based checklist, always update the summary table (recalculate per-category and total) and the quick-start list (renumber). Inconsistent counts erode trust in the checklist.
- **Don't write Thai curriculum notes in Thai narrative — use English narrative with Thai in `(...)` parens.** This is the user's confirmed style preference (2026-07-30). Writing Thai narrative first then converting wastes work. Default to English-first for all Thai curriculum note creation.
- **Don't add long paths to BOK wikilinks.** Obsidian resolves by filename. Short links like `[[01_Topic_Name]]` work fine across folder moves. Avoid `[[Advance/physic/01_Topic_Name]]` unless the user explicitly asks for explicit paths.
- **Don't dispatch 1 subagent per file for bulk creation.** Always batch 6-8 notes per subagent and dispatch 3+ in parallel. Single-file subagents waste delegation overhead and context budget.
- **Don't trust subagent self-reports on completeness.** After parallel subagent dispatch, verify file count and spot-check content. Subagents sometimes report "no changes needed" when files actually needed updating.
- **Prefer Mermaid over ASCII diagrams in Obsidian notes.** The user explicitly asked to convert ASCII diagrams to Mermaid. Obsidian renders Mermaid natively (no plugins needed), producing interactive, visually clean diagrams. ASCII diagrams should only be used when Mermaid can't represent the structure (e.g., very specific character alignment, mathematical notation). When creating new notes, always use Mermaid. When encountering existing ASCII diagrams, offer to convert them. Mermaid types to use: `flowchart TD/LR` for process flows, `erDiagram` for database schemas, `stateDiagram-v2` for state transitions, `graph` for architectures, `quadrantChart` for coordinate planes (x-axis/y-axis with `-->` for direction, `quadrant-1` through `quadrant-4` with hyphens), `gitGraph` for linear progressions (number lines, timelines — use `commit id: "label" type: HIGHLIGHT` for key points). **quadrantChart syntax:** `x-axis "left label" --> "right label"`, `y-axis "bottom label" --> "top label"`, `quadrant-1 "label"`. The y-axis direction matters: "bottom" --> "top" means positive is up (standard Cartesian).
- **Don't wait for all waves to complete before updating overviews.** After each wave of subagents finishes, immediately update the overview files and main index for those KAs. This gives the user incremental progress visibility and prevents the overview from becoming stale. Use `execute_code` to batch all patches for one wave in a single call.
- **Don't ask "do you need anything else?" when the task is clear.** The user prefers action over clarification questions. If the task direction is obvious (e.g., "check the material and update the overview"), proceed without asking for confirmation. The user will redirect if needed. Save questions for genuinely ambiguous choices (which KA to prioritize, which format to use).
- **Don't assume filling only critical gaps is enough.** The user wants comprehensive coverage. When they say "let do it" or "sure thing" to gap-filling, they mean ALL gaps — not just critical ones. Dispatch waves for medium and minor gaps without asking for separate approval. The user's enthusiasm signals "keep going until everything is covered."
- **The main index file has 4 separate sections that all need individual patching.** When updating the main index (e.g., `Software Engineering Note Content.md`), there are 4 distinct areas: (1) the main KA table at the top (coverage % and status column), (2) the mermaid quadrant chart (coordinate values), (3) the priority action list (rows with coverage and gap descriptions), and (4) the overall summary paragraph at the bottom. Updating 3 of 4 and missing the main table is a common oversight — the user will notice stale percentages in the table even if the priority list is correct. Always patch all 4 sections.
- **Subagents may update overview files themselves.** When a subagent's prompt includes the overview file path, it may independently update the overview (adding new files to the file list, updating coverage maps). This causes "BLOCKED: already_read 3 times" errors when you try to patch the same file afterward. Either: (a) re-read the overview before patching, or (b) instruct subagents NOT to modify overview files — handle all overview updates yourself after the wave completes.
- **Subagents may create ASCII diagrams despite Mermaid instructions.** After each wave of subagents completes, spot-check 2-3 new files for ASCII art (box drawing characters, caret-and-pipe arrows, slash-branch trees). Use `grep` to find them quickly. Convert to Mermaid immediately — the user will catch them if you don't.
