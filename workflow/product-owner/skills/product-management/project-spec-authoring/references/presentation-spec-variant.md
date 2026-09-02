# Presentation Spec Variant — Post-Build Interview Defense

Worked example: ITOPPLUS AI Engineer take-home presentation (2026-09-01).

## When This Variant Applies

- User has **already completed the implementation** (take-home, challenge, portfolio project)
- User needs a **presentation package** for an interview defense — slide-by-slide script, talking points, evidence references, visual cues
- The template tree (`F:\projects\project_spec\template\`) is a **development spec** ("we're about to build") — force-fitting it produces 375-line SMART documents the user doesn't need
- User says "presentation," "interview presentation," "keynote," or "I plan to do the real PowerPoint based on the spec"

## How It Differs from the Standard Spec

| Aspect | Standard spec (development) | Presentation spec (post-build) |
|---|---|---|
| **Purpose** | Drive implementation | Drive a 10-15 min verbal presentation |
| **Content** | User stories, ACs, API spec, DDL, test plan, README | Slide-by-slide outline, talking points, evidence refs, visual cues, timing |
| **Template fit** | High — templates map to what you're about to build | Low (~40%) — templates are too heavy, too enterprise, wrong job |
| **Output** | 10 docs, 100-250 lines each, in numbered folders | 3-4 docs, flat in a `project_presentation/` folder |
| **Primary reader** | Developer (implementation reference) | Presenter (spoken script) |
| **Evidence** | Requirements traceability | Code references + test output + DECISION_LOG citations |

## The Doc Set (4 files)

| File | What it is | Slides |
|---|---|---|
| `000_presentation_outline.md` | Slide-by-slide script: 10 slides, timing, talking points, visual cues, evidence refs, "don't" list | Master script (all slides) |
| `001_architecture_deep_dive.md` | Mermaid flowchart + component-by-component walkthrough with code references and test evidence | Slide 4 (the big diagram) |
| `002_key_decisions_and_evidence.md` | The 3 big architecture decisions with spoken answers (90-120 sec each), code references, and test evidence | Slide 5 (the core argument) |
| `003_risks_and_next_steps.md` | Risks, mitigations, production hardening, "with another week," ITOPPLUS connection (company-specific bridge) | Slides 8-9 (honesty + ambition) |

## Workflow (the fork from the standard workflow)

### 1. Inventory all resources (same as standard)
- The completed project (source code, tests, DECISION_LOG)
- The interview prep materials (company overview, battle card, fit assessment, assignment defense)
- The template tree (to assess fit, not to force-use)

### 2. Review & frame — CRITICAL: assess template fit honestly
- Map presentation needs to nearest templates
- **Be honest about misalignment.** The template was designed for development specs. If the user needs a presentation, say so — don't silently produce a 375-line SMART document as a "presentation spec."
- Propose a purpose-built doc set with the verdict: "The template is ~40% useful as raw material, but 0% presentation-ready. Here's a custom doc set."
- Get user buy-in before writing.

### 3. Write the presentation package
- 3-4 files, flat directory, no numbered subfolders
- Every doc has: frontmatter, slide mapping, talking points, evidence references, "Related Documents" cross-refs
- Borrow from templates where they help (mermaid from 025, decision-table from 021, risk framing from 071) but don't force the template structure
- The `000` doc is the master script — every slide has a "Talking points" section (spoken script) and an "Evidence" section (what to show on screen)

### 4. The presentation needs these things a development spec doesn't
- **Slide-by-slide timing** — 10 slides, ~12 min total
- **Narrative arc** — problem → approach → architecture → decisions → demo → risks → company connection
- **Visual suggestions** — "use the mermaid diagram here," "show the terminal screenshot here"
- **The company connection** — every slide ties back to the interviewer's actual product (e.g., ITOPPLUS Chat Center)
- **"Don't" list** — presentation-specific pitfalls (don't oversell the POC, don't read the DECISION_LOG verbatim, don't get defensive about "why no vectors")

## The ITOPPLUS Worked Example

### Source pools
- Completed project: `F:\interview\ITOPPLUS\sahachan-ai-engineer-takehome-complete\` (Python chatbot, 30 SKUs, 23 tests, DECISION_LOG)
- Interview prep: `F:\obsidian_note\interview-preparation\ITOPPLUS\` (6 files: company overview, battle card, fit assessment, assignment defense, knowledge gaps, practice plan)
- Template tree: `F:\projects\project_spec\template\` (33 files — assessed at ~40% fit)

### Verdict delivered
"The template is ~40% useful as raw material, but 0% of it is presentation-ready without heavy adaptation. Don't force-fit the template. Create a purpose-built presentation spec instead."

### What was borrowed from templates
- Mermaid flowchart pattern from `025_software_architecture_document.md`
- Decision-table pattern from `021_architecture_decision_records.md`
- Risk framing from `071_risk_register.md`

### What was NOT used
- SMART/KPI frameworks from `011_business_objective.md` (too heavy for a 1-slide problem statement)
- INVEST/epic/sprint ceremony from `012_user_stories.md` (irrelevant for a presentation)
- Stakeholder matrix from `014_stakeholder_analysis.md` (wrong shape for Q&A prep)
- README template from `031_README_developer_guide.md` (not needed — code is already built)

### Output
4 files, 53.6 KB total, in `F:\obsidian_note\interview-preparation\ITOPPLUS\project_presentation\`

## Pitfalls Specific to This Variant

- **Don't force-fit the template.** If the user says "presentation" and you produce a 375-line `011_business_objective.md`, you've done the wrong job. Assess honestly, propose the variant, get buy-in.
- **Don't skip the company connection.** The presentation spec MUST include a slide that bridges the take-home to the interviewer's actual product. This is the slide that separates "I did the assignment" from "I want THIS job."
- **Don't write development artifacts.** No user stories, no API specs, no DDL. The code is already built. The spec feeds a PowerPoint, not an IDE.
- **The `000` doc is the master script.** It should be usable as a side-by-side reference while building slides in PowerPoint. Every slide has "Talking points" (spoken) and "Evidence" (on-screen).werPoint, not an IDE.\n- **The `000` doc is the master script.** It should be usable as a side-by-side reference while building slides in PowerPoint. Every slide has \"Talking points\" (spoken) and \"Evidence\" (on-screen).\n"}