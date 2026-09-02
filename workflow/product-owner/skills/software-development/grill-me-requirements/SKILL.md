---
name: grill-me-requirements
description: Structured stakeholder interview for requirements elicitation. Use clarify() with choice-driven questioning to produce Business Objectives → User Stories → Acceptance Criteria → Stakeholder Analysis, guided by the project_spec template structure.
---

# Grill-Me Requirements Elicitation

> Structured PO/stakeholder interview pattern. Drive a session from vague vision → complete `01_requirement` documents using sequential `clarify()` calls with multiple-choice options.

## When to Use

- User says "grill me," "ask me questions," or "help me define requirements"
- User has a project vision but no written requirements
- User references `F:\projects\project_spec\template\` or similar template directories
- Starting a new project spec under `spec/<project>/`

## Workflow

### Phase 0: Load Templates

1. Read any existing README or overview docs the user provides
2. Read the template files from the template directory (usually `01_requirement/`):
   - `011_business_objective.md`
   - `012_user_stories.md`
   - `013_acceptance_criteria.md`
   - `014_stakeholder_analysis.md`
3. If possible, read an existing completed spec as a reference example (e.g., `spec/tiny_mchwa/`)

### Phase 1: Grill for Business Objectives (Round 1 — Big Picture)

Ask ONE question at a time using `clarify()` with 4 multiple-choice options. Never ask more than one question per turn — let the user's answer shape the next question.

Question order (adapt based on answers):
1. **Why** — what problem does this solve? (4 options covering different motivations)
2. **Who** — who are the users? Solo? Friends? Public? Portfolio-only?
3. **When** — timeline? Hard deadline or hobby pace?
4. **How (infra)** — deployment? Docker? K8s? Bare metal?
5. **How (tech)** — language preferences? Open to recommendation?
6. **What (scope)** — MVP boundaries? Foundation-only or include business services?

After 5-7 questions, produce `011_business_objective.md`. Include:
- Executive summary
- Strategic alignment (strategy map, traceability, balanced scorecard)
- 3-5 SMART objectives with detailed cards
- KPI framework (register, dashboard mockup, leading/lagging)
- Baseline & target measurements
- Dependency diagram (Mermaid flowchart)
- Risk matrix + heat map
- Objective tracking + review cadence

### Phase 2: Grill for User Stories (Round 2 — Drill Down)

Now drill into each service/component identified in the objectives. Questions per service:
1. **Architecture clarity** — what exactly does this service DO vs its dependencies?
2. **Technology specifics** — which library/framework? Why?
3. **Traffic/routing** — how does data flow through this service?

Write the user stories document. Each story MUST have:
- As a/I want/So that format
- 3-5 acceptance criteria (plain text, will expand in Phase 3)
- Story points estimate
- Priority (🔴/🟡/🟢)
- Sprint/milestone assignment
- Trace to objective ID

Group stories into epics. Include a story map (milestones × epics table).

### Phase 3: Write Acceptance Criteria (BDD Format)

For every story, write GWT (Given/When/Then) acceptance criteria. Each table row:
- AC ID (e.g., `AC-G001a`)
- Scenario name
- Given / When / Then columns
- Priority column

Include a summary table: story → AC count → 🔴 vs 🟡 counts.

### Phase 4: Stakeholder Analysis

Identify stakeholders including AI personas (Dev, QA, Designer, DevOps). Write:
- Influence/interest matrix with Mermaid quadrantChart
- Concerns + fears + success criteria per stakeholder
- Communication plan
- Requirements influence mapping

### Phase 5: Umbrella vs Deep-Dive Decision

After Phase 2, ASK the user whether to:
- Keep everything under one platform-level doc, OR
- Split into per-service self-contained directories with an umbrella

If splitting: each service gets its own `spec/<service>/01_requirement/` with all 3 docs. The platform-level doc becomes an umbrella with a consolidated story map and links.

## Pitfalls

- **Don't ask open-ended questions without choices.** Users who say "grill me" want guided options, not blank prompts. Every `clarify()` call should have 4 choices.
- **Don't grunt work the user.** One question per turn. Let their answer steer the next question.
- **Don't assume tech decisions.** Ask about language, framework, deployment even if you think you know.
- **Don't forget AI personas in stakeholder analysis.** The platform is built for AI agents to consume the specs — they're first-class stakeholders.

## Diagram Preferences

- **Architecture diagrams**: `flowchart TB` or `flowchart LR` with subgraphs, solid arrows for data flow, dashed for cross-cutting concerns
- **Project structure**: `treeView-beta` with `├──` / `└──` tree lines and `→` annotations
- **Stakeholder maps**: `quadrantChart`
- **Dependencies**: `flowchart` with color-coded nodes
- Never use ASCII art — always Mermaid. Never use `mindmap` for project structure — use `treeView-beta`.

## Output Structure

```
spec/<project>/
├── README.md                           ← Architecture overview, service map, Mermaid diagrams
└── 01_requirement/
    ├── 011_business_objective.md       ← SMART objectives, KPIs, risk matrix
    ├── 012_user_stories.md             ← User stories (umbrella or consolidated)
    ├── 013_acceptance_criteria.md      ← BDD GWT criteria
    └── 014_stakeholder_analysis.md     ← Influence/interest, AI personas

# If split into per-service:
spec/<service>/
└── 01_requirement/
    ├── 011_business_objective.md
    ├── 012_user_stories.md
    └── 013_acceptance_criteria.md
```

## Templates Reference

Base templates live at `F:\projects\project_spec\template\01_requirement\`. Completed example: `spec/tiny_mchwa/`.
