---
name: career-path-overlay-authoring
description: "Use when building senior career paths over existing BOKs."
tags: [career-path, obsidian, body-of-knowledge, swebok, babok, overlay, senior-engineer, staff-engineer]
triggers:
  - "career path"
  - "senior engineer"
  - "staff engineer"
  - "career progression"
  - "overlay existing BOK"
  - "build career paths"
  - "what should a senior engineer do"
---

# Career Path Overlay Authoring

Build career progression paths that overlay existing Bodies of Knowledge (SWEBOK, BABOK, PMBOK, SEBoK, etc.) without duplicating them. Focus on what a senior/staff engineer **does differently** (judgment, accountability, decision-making) rather than re-teaching foundational knowledge.

## When to Use

- User wants to build a career path for a specific role (Senior SWE, Staff Engineer, Tech Lead, Engineering Manager)
- User wants to build a **specialist engineering path** that branches from Senior SWE (SRE, Security Engineer, Data/ML Engineer, Quality Engineer)
- User has existing BOK notes (SWEBOK, BABOK, etc.) and wants to layer career progression on top
- User asks "what should a senior engineer know?" or "how do I become a staff engineer?"
- User wants to avoid duplicating existing knowledge while building career-focused notes
- User needs to fill a large career path with 30+ files across multiple capability areas

## The Overlay Strategy

**Core principle:** Don't rewrite fundamentals. Explain "Senior-Level Application" and link to existing notes.

A mid-level engineer knows **what** to do. A senior engineer knows **when, why, and how to make trade-offs**. Overlay notes focus on:

- **Judgment:** How to evaluate options and make decisions
- **Accountability:** What you own end-to-end (system, lifecycle, outcomes)
- **Decision-making:** How to frame problems, reduce ambiguity, and communicate trade-offs
- **Influence:** How to multiply team effectiveness without being a bottleneck

## Folder Structure

```text
career-path/
├── 00_Career_Path_Overview.md          # Master overview of all paths
├── 01_Software_Engineer/
│   └── 00_overview.md
├── 02_Senior_Software_Engineer/
│   ├── 00_overview.md                  # Role overview + capability areas
│   ├── 01_Technical_Ownership/
│   │   ├── 00_overview.md              # Capability overview (progress tracker)
│   │   ├── 01_System_Ownership.md      # Topic note
│   │   ├── 02_Lifecycle_Ownership.md
│   │   └── ...
│   ├── 02_Problem_Framing_and_Requirements/
│   │   ├── 00_overview.md
│   │   ├── 01_Problem_Statement_Definition.md
│   │   └── ...
│   └── ...
└── 03_Staff_Engineer/
    └── ...
```

**Key conventions:**
- Each role gets a numbered folder (01_, 02_, 03_)
- Each role has a `00_overview.md` summarizing the role and linking to capability areas
- Each capability area is a subfolder with its own `00_overview.md` (progress tracker)
- Topic notes are numbered (01_, 02_, 03_) within each capability area

## Step 1 — Define the Role and Capability Areas

For each role, identify 6-9 core capability areas that distinguish it from the previous level:

| Role | Example capability areas |
|---|---|
| **Senior SWE** | Technical ownership, problem framing, architecture judgment, delivery, quality, influence, mentoring |
| **Staff Engineer** | Multi-system ownership, technical strategy, cross-team influence, organizational design |
| **Tech Lead** | Team coordination, technical roadmap, stakeholder management, hiring |
| **Engineering Manager** | People development, team health, organizational alignment, resource allocation |
| **SRE / Platform Engineer** | Service objectives, observability, incident response, delivery automation, capacity and resilience, developer platform |
| **Security Engineer** | Threat modeling, secure development lifecycle, security operations, compliance, vulnerability management |
| **Data / ML Engineer** | Data architecture, ML lifecycle, data quality, model serving, experiment tracking |
| **Quality / Test Engineer** | Test strategy, automation frameworks, performance testing, exploratory testing, quality metrics |

**How to identify capability areas:**
- What does this role own that the previous role did not?
- What decisions does this role make that the previous role did not?
- What is the scope of influence (system, team, organization)?

## Step 2 — Create the Capability Area Overview

Each capability area gets an `00_overview.md` that serves as a progress tracker:

```yaml
---
title: "Capability Area Name"
note_type: capability-area-overview
capability_area: technical-ownership
career_path: senior-software-engineer
source_frameworks:
  - "[[SWEBOK v4 - Overview]]"
  - "[[SEBoK v2 - Overview]]"
tags:
  - career-path
  - senior-engineer
  - capability-area
---
```

### Required Sections

1. **One-line definition** — What does this capability mean at senior level?
2. **Why it matters** — How does this distinguish senior from mid-level?
3. **Topic notes table** — List all topics with status (✅ Done, 🚧 In Progress, ⏳ Planned)
4. **Concept map** — Mermaid diagram showing how topics connect
5. **Existing vault anchors** — Table linking each topic to existing BOK notes (no duplication)
6. **Self-assessment checklist** — 8-10 yes/no questions to gauge current level
7. **Related** — Links to adjacent capability areas and next-level roles

## Step 3 — Create Topic Notes

Each topic note follows this template:

```yaml
---
title: "Topic Name"
note_type: capability-topic
capability_area: technical-ownership
career_path: senior-software-engineer
prerequisite:
  - "[[01_Previous_Topic]]"
tags:
  - career-path
  - senior-engineer
  - topic-name
---
```

### Required Sections

1. **One-line definition** — What is this topic in one sentence?
2. **Why this is a senior skill** — What does a senior do differently than a mid-level?
3. **Core frameworks** — 2-4 structured approaches (tables, decision matrices, checklists)
4. **In practice** — How to apply this in real projects (workshops, reviews, exercises)
5. **Practical exercise** — Hands-on activity to build this skill
6. **Knowledge connections** — Wikilinks to existing BOK notes and adjacent topics
7. **Key takeaways** — 5-6 bullet points summarizing the most important ideas

### Content Principles

- **Focus on judgment, not knowledge:** Don't re-teach requirements engineering. Explain how a senior engineer frames problems, reduces ambiguity, and makes trade-offs.
- **Use comparison tables:** Show "mid-level approach" vs "senior approach" side-by-side
- **Include decision frameworks:** Give structured approaches for common decisions (prioritization, trade-offs, risk assessment)
- **Add practical exercises:** Every topic should have a hands-on activity the reader can do on their current project
- **Link to existing vault:** Every topic should link to 3-5 existing notes that provide the foundational knowledge

## Step 4 — Avoid Duplication

**The duplication test:** If your note explains **what** something is (e.g., "what is a requirement?"), you're duplicating. If your note explains **how a senior engineer approaches it** (e.g., "how to frame a problem before jumping to solutions"), you're overlaying.

### Duplication Anti-Patterns

| Anti-pattern | What it looks like | What to do instead |
|---|---|---|
| **Rewriting fundamentals** | "A requirement is a property that a product must have..." | Link to [[SWEBOK Requirements]] and explain how a senior validates requirements |
| **Re-teaching techniques** | "Requirements elicitation techniques include interviews, workshops..." | Link to [[SWEBOK Elicitation]] and explain how a senior chooses techniques for ambiguous problems |
| **Defining concepts** | "Technical debt is the cost of choosing an easy solution now..." | Link to [[SWEBOK Maintenance]] and explain how a senior manages debt strategically |

### Overlay Patterns

| Pattern | Example |
|---|---|
| **Senior judgment** | "A mid-level engineer implements requirements. A senior engineer questions whether the requirements solve the right problem." |
| **Decision framework** | "Use the Five Whys to find the root cause behind the stated problem" |
| **Trade-off analysis** | "When prioritizing, make explicit what you are choosing NOT to do" |
| **Practical exercise** | "Take your current project and apply the problem statement template" |

## Scope-Safe Execution in Concurrent Windows Vaults

When a role path is being filled in parallel, treat the user's file list as a hard scope boundary:

1. Resolve and confirm the native vault path before writing. Use a read-only filesystem probe when an indexer cannot enumerate a Windows drive, then use concrete absolute paths for all writes.
2. Record a scoped baseline with `git status --short -- <role-path>` before creating files. Preserve pre-existing modifications and report them separately.
3. Use `write_file` for each requested Markdown file. It creates parent directories safely. Parallelize only independent writes, and never delete or rewrite sibling capability folders that belong to another workstream.
4. For an exact request such as two capability areas with six topics each, verify the owned directories against an explicit expected filename set. Do not treat concurrently created sibling folders as failures in this workstream.
5. Run a post-write structural sweep over the owned files: frontmatter fields, required headings, exercises, comparison tables, Mermaid blocks, forbidden syntax, and requested foundation links. Validate wikilinks against the concrete vault paths and distinguish intentionally future links from broken links.
6. Report absolute files created, verification results, pre-existing changes, and concurrent changes separately. Do not commit unless explicitly requested.

## Verification Sweep

After creating all files, verify:

```bash
# Check for em-dashes (should be zero: use colons per user preference)
grep -c '—' *.md

# Check for ASCII trees (should be zero: use Mermaid per user preference)
grep -c '[├└│─]' *.md

# Check for deprecated Mermaid graph syntax
grep -rn "^graph " . --include="*.md"

# Verify all wikilinks resolve
grep -o '\[\[.*\]\]' *.md | sort -u
```

For a multi-folder capability-area build, use the reusable validation workflow in `references/overlay-validation-workflow.md`. It adds exact-manifest checks, YAML/frontmatter validation, context-aware wikilink resolution, Mermaid safety checks, placeholder detection, and scoped working-tree verification.

## Vault-Safe Batch Authoring and Validation

When creating 6 or more notes, treat the requested folder set as an explicit manifest:

1. Discover the confirmed vault or repository root and inspect the existing role overview and target folders before writing.
2. Write only the manifest paths. Prefer full-content `write_file` calls; batching calls through `execute_code` is acceptable when each file is still written through the file tool.
3. Validate the exact expected file set after writing. Do not infer success from a broad role-folder listing because sibling capability areas may contain unrelated work.
4. Resolve links in context: vault-root paths such as `career-path/...` from the vault root, role-relative paths such as `03_.../...` from the role folder, and bare topic links from the current capability folder. For a reliable checker, strip aliases and heading or block fragments, test candidates relative to the source folder, role folder, and vault root, then compare against concrete `.md` files. Do not mark a short sibling-folder link missing merely because a checker appended it to the wrong directory. Report genuinely ambiguous bare links separately from missing links.
5. Check every topic for the overlay headings, comparison or decision tables, a practical exercise, knowledge links, and an Obsidian-safe `flowchart` diagram.
6. Check only the requested scope with `git status --untracked-files=all -- <target folders>`. Report unrelated pre-existing working-tree entries without modifying them.
7. For parallel builds, wait for all child workstreams before the final manifest and integration sweep. The orchestrator should own root-overview integration and the final commit so child work cannot be committed or counted prematurely.
8. If committing is explicitly requested, stage by exact path such as `git add -- <role-path>`, verify the commit summary contains only that path, and run a post-commit status check to confirm unrelated changes remain untouched.
9. Report absolute paths, file counts, verification results, the commit identifier when applicable, and any unrelated pre-existing working-tree entries.

This preserves the overlay strategy while making large fills reproducible and safe to review. The validated Security Engineer build pattern and manifest are recorded in `references/security-engineer-overlay-build.md`.

### Mermaid Rules (from user preferences)

- **Always use `flowchart`, never `graph`** — Obsidian's renderer rejects `graph`
- **No parentheses in node labels** — Use `&#40;` and `&#41;` instead
- **No dots after numbers** — Use `"1 Assessment"` not `"1. Assessment"`
- **No bare ampersands** — Use `and` instead of `&`

## Specialist Engineering Paths

Specialist paths (SRE, Security, Data/ML, Quality) branch from Senior SWE and require different capability framing than the IC progression.

### How specialist paths differ from IC progression

| Aspect | IC Progression (Senior → Staff → Principal) | Specialist Path (Senior SWE → SRE/Security/etc.) |
|---|---|---|
| **Focus** | Increasing scope of influence (system → team → org) | Deep domain expertise in a specific discipline |
| **Capability areas** | Broader ownership, strategy, influence | Technical depth in specialist domain |
| **Prerequisites** | Previous IC level | Senior SWE (foundational engineering judgment) |
| **Career trajectory** | Staff → Principal → Distinguished | Senior Specialist → Principal Specialist → Fellow |

### Specialist path capability areas

Specialist paths typically have 5-7 capability areas focused on **domain mastery** rather than **scope expansion**:

| Specialist Path | Capability Areas |
|---|---|
| **SRE / Platform Engineer** | Service level objectives, observability, incident response, delivery automation, capacity planning, platform engineering, reliability patterns |
| **Security Engineer** | Threat modeling, secure SDLC, security testing, incident response, compliance, vulnerability management, security architecture |
| **Data / ML Engineer** | Data architecture, ML lifecycle, data quality, model serving, experiment tracking, MLOps, data governance |
| **Quality / Test Engineer** | Test strategy, test design, automation, quality engineering, specialized testing, measurement |

### Framing specialist capability areas

When defining specialist capability areas, focus on:
- **What does a senior specialist do that a senior generalist doesn't?**
- **What domain-specific judgment is required?**
- **What specialized tools, frameworks, or methodologies must be mastered?**

Example for SRE:
- ❌ "System ownership" (this is Senior SWE territory)
- ✅ "Service level objective design and error budget management" (SRE-specific judgment)

## Execution Strategy for Large Fills

When filling a complete career path with 30+ files across 6+ capability areas:

### Parallel batch execution pattern

**Recommended approach:** Use `delegate_task` with 3 parallel subagents, each handling 2 capability areas.

```python
# Example structure for SRE path (6 areas × 6 files = 36 files)
delegate_task(tasks=[
    {
        "goal": "Build capability areas 01-02 for SRE path",
        "context": "Create 01_Service_Level_Objectives and 02_Observability with overview + 5 topics each..."
    },
    {
        "goal": "Build capability areas 03-04 for SRE path",
        "context": "Create 03_Incident_Response and 04_Delivery_Automation with overview + 5 topics each..."
    },
    {
        "goal": "Build capability areas 05-06 for SRE path",
        "context": "Create 05_Capacity_Planning and 06_Platform_Engineering with overview + 5 topics each..."
    }
])
```

**Why this works:**
- Each subagent has focused scope (2 areas, ~12 files)
- Parallel execution saves time (3× faster than sequential)
- Context remains manageable per subagent
- Results consolidate cleanly

### Sequential execution pattern

**Use when:** User wants to review each capability area before proceeding, or when areas have dependencies.

**Structure:**
1. Build one capability area completely (overview + 5-7 topics)
2. User reviews and provides feedback
3. Adjust approach if needed
4. Proceed to next area

### File count estimation

For a complete career path:

| Component | Files per area | Total areas | Total files |
|---|---|---|---|
| Capability area overview | 1 | 6 | 6 |
| Topic files | 5-7 | 6 | 30-42 |
| **Total** | **6-8** | **6** | **36-48** |

**Time estimate with parallel execution:** ~15-20 minutes for 36 files using 3 subagents.

## Worked Examples

See `references/` directory for complete capability areas:

- `references/senior-swe-technical-ownership-example.md` — Technical Ownership (7 files, 56.6 KB)
- `references/senior-swe-problem-framing-example.md` — Problem Framing and Requirements (9 files, 91.2 KB)
- `references/quality-test-engineering-example.md` — Quality and Test Engineering specialist path (44 files, 483 KB, 6 capability areas)
- `references/data-ml-engineer-areas-05-07-manifest.md` — Data/ML Engineer areas 05-07 (21 files, 3 capability areas: Security, MLOps, Production Engineering)
- `references/full-specialist-path-build-workflow.md` — Proven 3-batch parallel workflow for filling a complete 7-area specialist path (50 files) in ~15 minutes, validated on Security Engineer and Data/ML Engineer paths

## Content Density Management

When batch-generating 6+ files with a line-count floor (typically 100-180 lines), initial content generation consistently produces files 3-10 lines below the floor. Plan for a mandatory expansion pass.

### The line-count shortfall pattern

Initial generation of a topic note with all required sections (definition, why senior, frameworks, in practice, exercise, connections, takeaways) typically produces 80-100 lines. Overview files are even shorter (75-85 lines) because they have fewer framework tables.

### Expansion strategy: "Common Pitfalls" section

The most natural way to add 5-8 lines of high-value content is a **Common Pitfalls** section placed before Key Takeaways. Each pitfall is a 1-2 line bullet describing a mistake mid-level engineers make, which reinforces the senior-judgment focus of the overlay. This section:
- Adds genuine value (anti-patterns are senior-level knowledge)
- Fits naturally before Key Takeaways
- Scales predictably: 4-5 pitfalls = 6-8 lines with header

### Batch execution order for density management

1. Generate all files in one `execute_code` pass
2. Run verification script checking line counts
3. Identify files below the floor
4. Expand only short files with targeted patches (add Pitfalls section if missing, expand existing section if present)
5. Re-verify to confirm all files pass

For overview files specifically, add "Common Anti-Patterns" table and "Maturity Signals" section to reach the floor.

## Pitfalls

- **Don't skip the "Existing vault anchors" table.** This is what makes the overlay strategy work. Without it, readers don't know where to find the foundational knowledge.
- **Don't write topic notes as standalone tutorials.** Every topic should assume the reader has (or will read) the foundational notes. Focus on "what's different at senior level."
- **Don't forget the practical exercises.** Career paths are built by doing, not just reading. Every topic needs a hands-on activity.
- **Don't use em-dashes.** Use colons (:) per user preference.
- **Don't use ASCII trees.** Use Mermaid diagrams per user preference.
- **🚨 NEVER use `graph TD/LR/BT` in Mermaid diagrams.** Obsidian's current Mermaid renderer rejects or misrenders `graph`. Always use `flowchart TD/LR/BT`.
- **Plan for the expansion pass.** Do not try to hit 100 lines in initial generation by padding. Generate naturally, then expand systematically with Common Pitfalls or Anti-Patterns sections.

## Related

- [[educational-content-authoring]] — Scanning vaults for content gaps (different workflow)
- [[career-guidance-authoring]] — Building career guidance for Thai students (different audience)
- [[obsidian-note-authoring]] — Synthesizing source material into notes (general technique)
