# Career-Path Overlay Note Pattern

Pattern for creating career-progression notes that layer professional application knowledge on top of existing Body of Knowledge (SWEBOK, PMBOK, BABOK, etc.) foundation notes. Proven 2026-08-05 across **8 of 9 Senior SWE capability areas** (60+ files, ~600 KB total).

## When to Use

- User wants career-path or role-specific notes that build on existing BOK content
- Creating "what does a senior/staff/principal engineer do differently" type content
- Building promotion-readiness or capability-development knowledge bases
- The vault already has deep technical BOK notes and the new content should cross-reference them, not duplicate them

## Core Principle: Overlay, Not Duplicate

Career-path notes answer: **"What does someone at this level DO with the foundational knowledge?"**

They do NOT re-teach the foundations. Every topic note links back to the relevant SWEBOK/BOK note via wikilinks and explains the senior-level application.

## Folder Structure

```text
career-path/
├── 00_Career_Path_Overview.md          ← master map of all roles
├── 01_Software_Engineer/
│   └── 00_overview.md
├── 02_Senior_Software_Engineer/
│   ├── 00_overview.md                  ← capability area table + links
│   ├── 01_Technical_Ownership/         ← 7 files, 56.6 KB
│   │   ├── 00_overview.md              ← progress tracker
│   │   └── 01-06 topic notes
│   ├── 02_Problem_Framing_and_Requirements/   ← 9 files, 91.2 KB
│   ├── 03_Architecture_and_Design_Judgment/   ← 8 files, 81.8 KB
│   ├── 04_Delivery_and_Execution/             ← 8 files, 78 KB
│   ├── 05_Quality_Reliability_Security/       ← 8 files, 76.5 KB
│   ├── 06_Communication_and_Influence/        ← 8 files, 110 KB
│   ├── 07_Mentoring_and_Team_Leadership/      ← 8 files, 96.6 KB
│   ├── 08_Engineering_Economics_and_Trade_Offs/ ← 7 files, 98.6 KB
│   └── 09_Promotion_Evidence_and_Capstone/    ← in progress
```

Three levels:
1. **Master overview** (`00_Career_Path_Overview.md`): all roles, family groupings, relationship diagram
2. **Role overview** (`02_Senior_Software_Engineer/00_overview.md`): capability areas table, progression signals, evidence to build, nearby paths
3. **Capability area** (`01_Technical_Ownership/`): progress-tracker overview + 6-7 topic notes

## Proven Topic Lists Per Capability Area

### 01_Technical_Ownership (6 topics)
System_Ownership, Lifecycle_Ownership, Technical_Decision_Making, Code_Quality_Standards, Production_Ownership, Ownership_Evidence

### 02_Problem_Framing_and_Requirements (8 topics)
Problem_Definition, Stakeholder_Analysis, Requirements_Elicitation, Requirements_Documentation, Acceptance_Criteria, Scope_Management, Requirements_Traceability, Problem_Framing_Evidence

### 03_Architecture_and_Design_Judgment (7 topics)
Architectural_Thinking, Design_Patterns_Selection, Trade_Off_Analysis, System_Design_Review, Evolutionary_Architecture, Architecture_Documentation, Architecture_Evidence

### 04_Delivery_and_Execution (7 topics)
Estimation_and_Forecasting, Dependency_Management, Delivery_Metrics, Technical_Debt_Strategy, Release_Management, Incremental_Delivery, Risk_Management

### 05_Quality_Reliability_Security (7 topics)
Testing_Strategy, SRE_Principles, Observability, Incident_Response, Security_Practices, Production_Readiness, Chaos_Engineering

### 06_Communication_and_Influence (7 topics)
Technical_Writing, Stakeholder_Communication, Influence_Without_Authority, Facilitation, Documentation_Strategy, Cross_Team_Collaboration, Conflict_Resolution

### 07_Mentoring_and_Team_Leadership (7 topics)
Technical_Mentoring, Code_Reviews_as_Teaching, Pair_Programming, Effective_Feedback, Coaching_and_Development, Psychological_Safety, Leading_Without_Authority

### 08_Engineering_Economics_and_Trade_Offs (6 topics)
Cost_Benefit_Analysis, Build_vs_Buy_Decisions, Technical_Debt_ROI, Total_Cost_of_Ownership, Business_Case_Development, Trade_Off_Evaluation

### 09_Promotion_Evidence_and_Capstone (6 topics, in progress)
Promotion_Packets, Evidence_Collection, Impact_Quantification, Self_Assessment, Career_Ladders, Capstone_Project

## Per-Capability-Area Execution Loop (9 Steps)

Each capability area follows this exact sequence:

1. **Research via SearXNG** (2 parallel queries): one for the capability area's core practices, one for adjacent/advanced topics. Space queries to avoid 429 rate limits.
2. **Inspect existing vault notes**: `ls` the relevant BOK folder (SWEBOK/PMBOK/CyBOK) to find existing notes that the new content should cross-link to rather than duplicate.
3. **Scaffold folder**: `mkdir -p career-path/02_Senior_Software_Engineer/NN_Area_Name/`
4. **Write overview**: `00_overview.md` with YAML frontmatter (source_frameworks, topics, prerequisite links to BOKs), capability-area Mermaid diagram, topic table, success indicators
5. **Batch-write topic files**: 6-7 numbered files (`01_Topic_Name.md` through `07_Topic_Name.md`). Each includes: YAML frontmatter, core-skill blockquote, "Why This Matters" section, 1-2 Mermaid diagrams, practical tables, templates, anti-patterns, success indicators, cross-links to BOK notes and sibling capability areas
6. **Verify**: `ls -la && wc -l *.md && grep -c '—' *.md && grep -c 'mermaid' *.md` — zero em-dashes, 9+ Mermaid diagrams per area expected
7. **Update parent overview**: Patch `02_Senior_Software_Engineer/00_overview.md` capability-area table to link to the new `NN_Area_Name/00_overview.md`
8. **Git commit**: `git add -A && git commit -m "Add NN_Area_Name capability area for Senior SWE"` with multi-line message listing files, diagrams, and cross-links
9. **Report to user**: file count, total KB, Mermaid count, brief topic summary, "next area" preview

## 00_overview.md (Capability Area Progress Tracker)

Contains:
- YAML frontmatter with `capability_area`, `career_path`, `source_frameworks`
- Core idea statement (one paragraph)
- Topic notes table: #, Topic, Focus, Status (✅/❌), File
- Completion percentage
- Mermaid flowchart showing how topics connect
- Reading order guidance
- Existing vault anchors table (maps senior topics to foundation notes)
- Self-assessment checklist
- Related links

## Topic Note Template

```yaml
---
title: "Topic Name"
note_type: capability-topic
capability_area: technical-ownership
career_path: senior-software-engineer
prerequisite:
  - "[[previous_topic]]"
tags:
  - career-path
  - senior-engineer
  - technical-ownership
---
```

### Required Sections (in order)

1. **Title + one-line definition** (blockquote): `> **Core skill:** ...` (changed from "One-line definition" to match actual pattern)
2. **Why This Matters**: 2-3 paragraphs explaining the level distinction
3. **Comparison tables**: Mid-level vs Senior mindset/behavior/responsibility
4. **Core content sections** (3-5): The actual knowledge, with tables, Mermaid diagrams, and structured frameworks
5. **Practical Applications**: Concrete action the reader can take today (checklist, template, analysis)
6. **Knowledge Connections**: Wikilinks to related career-path topics AND existing BOK notes
7. **Summary**: 2-3 sentence synthesis (replaced "Key Takeaways" to match actual pattern)

### Content Patterns That Work

- **Comparison tables** (mid-level vs senior): the most valuable section for career development
- **Anti-pattern tables**: common mistakes with "what to do instead" column
- **Checklists**: production readiness, system ownership, evidence building
- **ADR template**: concrete document template the reader can copy
- **Evidence translation tables**: technical description → business translation
- **Mermaid flowcharts**: decision processes, lifecycle phases, system boundaries
- **Self-assessment checklists**: "can you do X?" format for gauging readiness

### What NOT to Include

- Re-teaching foundational concepts (link to the BOK note instead)
- Quizzes or assessments (per SOUL.md: no assessment, no pressure)
- Generic career advice without technical specificity
- Content that duplicates existing SWEBOK/PMBOK/BABOK notes

## File Size Reference (8 Areas Complete)

| Area | Files | Total KB | Mermaid | Avg KB/File |
|------|-------|----------|---------|-------------|
| 01_Technical_Ownership | 7 | 56.6 | ~12 | 8.1 |
| 02_Problem_Framing | 9 | 91.2 | ~18 | 10.1 |
| 03_Architecture_Judgment | 8 | 81.8 | ~14 | 10.2 |
| 04_Delivery_Execution | 8 | 78.0 | ~16 | 9.8 |
| 05_Quality_Reliability_Security | 8 | 76.5 | 12 | 9.6 |
| 06_Communication_Influence | 8 | 110.0 | 15 | 13.8 |
| 07_Mentoring_Team_Leadership | 8 | 96.6 | 9 | 12.1 |
| 08_Engineering_Economics | 7 | 98.6 | 9 | 14.1 |

**Target:** 8-14 KB per topic file, 9-18 Mermaid diagrams per area, zero em-dashes.

## BOK Anchoring Table Pattern

In the capability area overview, include a table that maps each senior topic to its foundation:

```markdown
| Senior topic | Existing foundation notes |
|---|---|
| System Ownership | [[software-engineering-note/07_Software_Maintenance/Software Maintenance Overview]] |
| Lifecycle Ownership | [[software-engineering-note/01_Software_Requirements/Software Requirements Overview]] |
```

### BOK Anchoring by Capability Area

| Capability Area | Primary BOK Anchors |
|---|---|
| Technical Ownership | SWEBOK: Software Construction, Configuration Management |
| Problem Framing | SWEBOK: Requirements Engineering; BABOK: Requirements Analysis |
| Architecture Judgment | SWEBOK: Software Design; SEBoK: System Architecture |
| Delivery Execution | PMBOK: Project Integration, Schedule, Risk; SWEBOK: Management |
| Quality Reliability Security | SWEBOK: Quality, Testing, Maintenance; CyBOK: Security |
| Communication Influence | SWEBOK: Professional Practice; PMBOK: Communications |
| Mentoring Leadership | SWEBOK: Professional Practice (Group Dynamics) |
| Engineering Economics | SWEBOK: Economics; PMBOK: Cost Management |
| Promotion Evidence | All BOKs (synthesis) |

## Quality Gates (per area)

Before committing each capability area:
- [ ] Zero em-dashes (`grep -c '—' *.md` returns 0 for all files)
- [ ] 9+ Mermaid diagrams using `flowchart` (not `graph`)
- [ ] YAML frontmatter complete on every file
- [ ] Cross-links to at least 2 existing BOK notes (no duplication)
- [ ] Cross-links to at least 2 sibling capability areas
- [ ] Parent `02_Senior_Software_Engineer/00_overview.md` updated with link
- [ ] Git commit with multi-line message listing all files and key features

## Pitfalls

### Structural
- **Don't duplicate BOK content.** Cross-link via `[[body-of-knowledge/SWEBOK/...]]` wikilinks. The overlay notes focus on SENIOR-LEVEL APPLICATION (judgment, trade-offs, decision-making), not foundational knowledge.
- **Don't use em-dashes.** Replace with colons (`:`). Always run `grep -c '—' *.md` before committing; if any file shows non-zero, run `sed -i 's/—/:/g' *.md`.
- **Don't use ASCII diagrams.** Use Mermaid `flowchart` (not `graph`), avoid `()` in labels (use `&#40;`/`&#41;`), avoid `"1."` dot-numbers (use `"1 "`), avoid `&` (use `and`).
- **Folder naming:** Use numbered prefixes (`01_`, `02_`, ...) with underscores (not hyphens) for ordering. Topic files inside each folder also use numbered prefixes.

### Workflow
- **Batch topic file creation.** Use multiple `write_file` calls in one response (3-4 files per batch). Don't create one at a time — wastes round trips.
- **Update parent overview AFTER verification, BEFORE commit.** This ensures the commit includes the parent link.
- **Commit per capability area, not per file.** One commit per area with a descriptive multi-line message listing files, diagram counts, and cross-links.
- **Space out SearXNG queries** to avoid 429 rate limits. Two parallel queries at session start is fine; don't fire 5 rapid consecutive queries.

### Content
- **Each topic file needs 3+ practical artifacts:** templates, checklists, decision frameworks, anti-pattern tables. Theory alone doesn't match the "senior-level application" goal.
- **Include "Evidence" sections** where the capability area feeds into promotion packets (especially areas 01, 03, 08).
- **Senior-level focus check:** Every topic file should answer "what does a senior engineer do DIFFERENTLY than a mid-level engineer?" If the answer is "the same thing but more of it," rewrite.

## Naming Convention

- Folders: `NN_Capability_Area_Name/` (numbered, underscored)
- Topic files: `NN_Topic_Name.md` (numbered, underscored, sequential within folder)
- Overview: always `00_overview.md`
- Career-path folders: `NN_Role_Name/` (numbered, underscored)

## Next Steps After All 9 Areas Complete

1. Update `02_Senior_Software_Engineer/00_overview.md` with a "Typical Progression" section showing how capabilities build on each other
2. Add cross-links from Senior SWE to adjacent career paths (Staff Engineer, Engineering Manager) that share capabilities
3. Consider a `00_capstone_checklist.md` in the Senior SWE folder that aggregates all 9 capability areas into a single promotion-readiness checklist

## Relationship to Other Patterns

- This pattern is for **software engineering career paths** overlaying SWEBOK/PMBOK/BABOK
- The Thai curriculum patterns (Steps 3-9d in the main skill) are for **academic curricula** overlaying IPST/OBEC
- Both use progress trackers (00_overview.md), but career-path trackers use ✅/❌ while curriculum trackers use grade-band columns
