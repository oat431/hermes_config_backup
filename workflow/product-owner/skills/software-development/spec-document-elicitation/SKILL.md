---
name: spec-document-elicitation
description: "Elicit requirements from stakeholders via structured 'grill me' interviews and populate spec documents from templates. Covers the full 01_requirement phase."
tags: [requirements, elicitation, product-owner, ba, interview, templates, specification, babok]
---

# Spec Document Elicitation

Elicit requirements from a stakeholder (the user) through structured Q&A and populate standardized specification documents from templates. The "grill me" pattern: sequential `clarify()` calls with curated multiple-choice options, each answer feeding the next question and the document being written.

## Trigger Conditions

Load this skill when:
- A user asks to "grill me," "interview me," or "ask me questions" to set up project specifications
- A user references the `project_spec` repository (`F:\projects\project_spec`) and wants foundation documents populated
- A user wants Business Objectives, User Stories, Acceptance Criteria, or Stakeholder Analysis written from scratch
- A user says "I'm ready, ask me" in the context of a new project/spec

## Repository Structure

```
F:\projects\project_spec\
├── README.md                          # Platform overview & service catalog
├── template\                          # Blank templates (the source of truth)
│   └── 01_requirement\
│       ├── 011_business_objective.md  # SMART goals, KPIs, risk matrix
│       ├── 012_user_stories.md        # As-a-I-want-so-that, epics, story maps
│       ├── 013_acceptance_criteria.md # Given-When-Then BDD format
│       ├── 014_stakeholder_analysis.md # Influence/interest matrix
│       └── 015_definition_of_done.md  # DoD criteria
│   └── 02_design\ ... 07_pm\         # Later phases
└── spec\                              # Populated specs (one dir per project)
    └── <project_name>\
        └── 01_requirement\            # Where documents get written
```

**Reference example**: `spec/tiny_mchwa/` — a completed spec to study for format and depth.

## Elicitation Workflow

### Phase 1: Discovery (read, don't ask)
1. Read `F:\projects\project_spec\README.md` — understand the project context
2. Read all relevant templates from `F:\projects\project_spec\template\01_requirement\`
3. Read an existing completed spec (e.g., `spec/tiny_mchwa/`) as a reference
4. Scan the project's spec directory to see what already exists

### Phase 1.5: Structure Decision (multi-service projects only)

**When the project has multiple discrete services** (e.g., a platform with foundation services + business microservices), ask the structure question BEFORE writing any document beyond the platform-level Business Objectives:

> "Should each service get its own deep-dive documents, with the platform serving as an umbrella? Or should all stories live in one monolithic platform doc?"

**The recommended pattern (and the one to lead with):**

```
spec/
├── <platform>/                     ← UMBRELLA: platform-level docs only
│   ├── README.md                   ← Architecture overview, service map, quick links
│   └── 01_requirement/
│       ├── 011_business_objective.md   ← Cross-cutting objectives (all services)
│       ├── 012_user_stories.md         ← Consolidated story map + links to service docs
│       └── 014_stakeholder_analysis.md ← All personas (human + AI)
│
├── <service-a>/                    ← DEEP DIVE: self-contained, AI-persona-ready
│   └── 01_requirement/
│       ├── 011_business_objective.md   ← Service-specific objectives (subset of platform)
│       ├── 012_user_stories.md         ← That service's stories only
│       └── 013_acceptance_criteria.md  ← BDD criteria for that service's stories
│
├── <service-b>/                    ← Same structure, fully independent
│   └── 01_requirement/
│       └── ...
```

**Why this pattern:**
- Each service spec is self-contained — an AI persona can pick up one directory and build without reading the whole platform
- The platform umbrella provides cross-service traceability (story → objective, service → dependency) without duplicating content
- Story points, epics, and milestones are consolidated at the platform level; details live in service docs
- `012_user_stories.md` at the platform level is a **thin umbrella** — story map + cross-service dependencies + links. Not a copy of service-level stories.

**When NOT to split:**
- Single-service projects (e.g., one microservice with no platform layer)
- The platform document is the only document needed (no deep dives)
- Tiny projects where splitting adds more overhead than value

### Phase 2: Grilling (structured Q&A)
Use `clarify()` with multiple-choice options. Sequencing matters — start broad, then narrow:

**Round 1 — The Big Picture:**
- Primary motivation (why build this?)
- Users and scale (self only, friends, public-ready)
- Timeline and delivery preferences (docs first? code first?)

**Round 2 — Scope & Architecture:**
- MVP scope (what's the minimum viable set?)
- Technology preferences or constraints
- Deployment environment (Docker Compose, Kubernetes, bare metal)

**Round 3 — Drilling into specifics:**
- For each component/service in scope, ask targeted questions
- Use prior answers to constrain subsequent choices
- Each answer should narrow options for the next question

**Rules for grill questions:**
- ALWAYS provide 3-4 curated choices via `clarify(choices=[...])` — never open-ended unless no good options exist
- Design choices that progressively narrow scope
- Each choice must force a real decision between distinct paths
- After 4-5 rounds of questions, you should have enough to write a document
- If the user picks "Other," honor it and adapt

### Phase 3: Document Population
For each document, follow the template structure precisely:

1. Copy the template's frontmatter — replace placeholders with real values
2. Fill every section — empty sections with placeholder text are unacceptable
3. Use real data from the interview — never fabricate metrics, names, or numbers
4. Mark unknowns honestly — use "TBD" rather than guessing
5. Trace stories to objectives — each user story must map to a business objective
6. Include "Related Documents" cross-references at the bottom

### Document Order (dependencies)

**For the platform umbrella:**
1. `011_business_objective.md` — defines the WHY (objectives, KPIs, success criteria) for all services
2. `012_user_stories.md` — consolidated story map + inter-service traceability + links (thin umbrella, NOT a copy)
3. `014_stakeholder_analysis.md` — defines WHO CARES (influence, concerns, engagement)

**For each service deep-dive:**
1. `011_business_objective.md` — service-specific objectives (subset of platform objectives)
2. `012_user_stories.md` — that service's stories only, self-contained for an AI persona
3. `013_acceptance_criteria.md` — BDD criteria for that service's stories (Given-When-Then)

**Rule:** The platform umbrella's `012_user_stories.md` links to service-level story docs. It does NOT duplicate them. Each service doc is the source of truth for its own stories.

### Phase 4: Present & Continue
After each document:
- Summarize what was written (2-3 lines)
- Show key metrics (e.g., "5 objectives," "18 stories across 4 epics")
- Ask "Review or continue?" — don't assume all documents in one session

## Diagram Preferences

- **Architecture / data flow diagrams**: `flowchart TB` or `flowchart LR` with `subgraph` blocks, solid arrows (`-->`) for data flow, dashed (`-.->`) for cross-cutting concerns (auth validation, metrics scraping, service registration). Color-code nodes by layer (edge, foundation, gateway, observability, business).
- **Project / directory structure**: `treeView-beta` with `├──` / `└──` tree lines and `→` annotations for descriptions. NEVER use `mindmap` for project structure — the user explicitly corrected this. NEVER use ASCII art boxes.
- **Dependency graphs**: `flowchart` with color-coded priority nodes (🔴 red fill for must-have, 🟡 orange for should-have, 🟢 green for nice-to-have).
- **Stakeholder maps**: `quadrantChart` with labeled quadrants.
- **Execution order / sprint plans**: `flowchart LR` with colored initiative nodes and dependency arrows.
- Always wrap Mermaid in ```mermaid fences. Mermaid renders natively in Obsidian and GitHub.

## Design Review Feedback Loop

> Requirements documents are NOT static. After PO writes `01_requirement`, the Design/Dev persona reviews them against real architecture constraints and produces a **meeting minute** (placed in `spec/meeting-minute/`) listing decisions and affected documents. The PO must then update ALL affected docs and produce a **response meeting minute** confirming the changes.

### The feedback loop pattern:

```
PO writes 01_requirement docs
  → Design/Dev persona reviews against real infra
  → Design/Dev produces meeting minute (affect-doc.md) with:
     - Decisions made (D1, D2, ... Dn)
     - Documents requiring changes (severity: 🔴 Critical / 🟡 Moderate)
     - Specific line-level changes needed
  → PO reads the meeting minute
  → PO grills user on any unclear decisions
  → PO updates ALL listed documents (bump version to 0.2)
  → PO writes a response meeting minute confirming:
     - What changed in each document
     - Updated story/point/AC counts
     - Architecture rules (the new ground truth)
  → PO hands back to Design persona
```

### Key rules for the feedback loop:
- **Read the meeting minute completely** before touching any document. Understand the full scope of changes.
- **Grill the user on ambiguous decisions** — some design decisions need PO clarification (e.g., "does Gate see auth traffic at all?" or "is Valkey for rate limiting or something else?").
- **Update docs in order of severity** — 🔴 Critical docs first (they block development).
- **Don't forget the README** — both platform-level and root-level READMEs need updating when architecture changes. This is easy to miss.
- **Bump document versions** — changed docs go from `0.1` → `0.2` with a revision history entry.
- **Produce a response meeting minute** — this is the contract that tells the next persona what changed and that requirements are now aligned.

## Post-Requirements Deliverables

After `01_requirement` is complete and services are being built/deployed, the PO persona also produces:

### Phase Plans (`plan/` directory)
When the DevOps/Dev persona proposes a new phase (e.g., "Phase 2: add CI/CD, observability, alerting"), the PO:
1. Reads the DevOps proposal meeting minute
2. Grills the user on decisions (scope, notification channel, deploy strategy, retention policy)
3. Writes a structured Phase Plan with: initiatives, PO decisions, execution order (Mermaid), action items, Definition of Done, and transition criteria

### Construction Overview (`03_construction/031_README_developer_guide.md`)
A platform-level document that ties together each service's `03_construction/` folder. Contains:
- Service inventory (treeView-beta diagrams)
- Monorepo structure
- Development workflow (local dev + CI/CD deploy flow)
- Build profiles per tech stack
- Shared resources table
- Coding standards summary

### Meeting Minutes (`spec/meeting-minute/`)
Every cross-persona handoff produces a meeting minute. These are the **contracts** between personas:
- Format: YAML frontmatter + structured sections (decisions, documents affected, action items)
- Named: `<topic>_<date>.md` (e.g., `po-update-2026-07-22.md`)
- Include severity tags (🔴/🟡) on affected documents
- Include a handoff checklist at the end

## Pitfalls

- **DON'T write all documents before the user has seen any.** Write one, present it, get implicit or explicit go-ahead, then write the next.
- **DON'T ask the same question twice.** Track what's been answered. Each round builds on prior answers.
- **DON'T use open-ended `clarify()` when you can provide choices.** The user chose "grill me" mode — they want to pick from options.
- **DON'T fill template fields with placeholder text.** If you lack data, ask another question or mark it `TBD`.
- **DON'T skip sections assuming they're irrelevant for a small project.** A portfolio project needs full documents. Every section signals rigor.
- **When the user changes a fundamental assumption mid-session** (e.g., "Guard IS the Keycloak instance itself"), note that earlier documents may need updating. Flag it explicitly.
- **DON'T write monolithic `012_user_stories.md` with all services' stories in one file for multi-service platforms.** This forces every persona to read everything. Ask the structure question (Phase 1.5) BEFORE populating story documents. If the user wants service-level docs, split the stories and make the platform `012` a thin umbrella.
- **DON'T restructure mid-session without asking.** If the user suggests a structural change, pause and confirm the pattern before applying it everywhere. "Are all three foundation services getting independent docs? What about business services?"
- **DON'T forget the READMEs when architecture changes.** When applying design review changes, both the platform-level README (`spec/<platform>/README.md`) AND the root-level README (`project_spec/README.md`) must be updated with new architecture diagrams, service statuses, ports, domains, and phase tracking. These are high-visibility documents — stale information here undermines trust in the rest of the spec.
- **DON'T replace entire table rows when adding rows.** Use targeted `patch` operations with enough context to be unique. Replacing a row's content when you meant to insert a new row silently deletes data.
