# Senior SWE Problem Framing and Requirements — Complete Worked Example

**Created:** Session 2026-08-05  
**Total files:** 9  
**Total size:** 91.2 KB  
**Location:** `F:\obsidian_note\swe-knowledge\career-path\02_Senior_Software_Engineer\02_Problem_Framing_and_Requirements\`

## File Structure

```text
02_Problem_Framing_and_Requirements/
├── 00_overview.md                          (6.2 KB) — Progress tracker + concept map
├── 01_Problem_Statement_Definition.md      (9.1 KB) — Framing the problem before jumping to solutions
├── 02_Current_and_Future_State.md         (10.2 KB) — Understanding where we are and where we need to be
├── 03_Stakeholder_Management.md           (11.7 KB) — Knowing who cares and what they need
├── 04_User_and_Business_Outcomes.md       (10.2 KB) — Connecting requirements to measurable value
├── 05_Acceptance_Conditions.md            (10.4 KB) — Defining success before building
├── 06_Ambiguity_Reduction.md              (10.8 KB) — Making progress when requirements are unclear
├── 07_Prioritization.md                   (11.0 KB) — Deciding what matters most
└── 08_Requirements_Risk.md                (11.6 KB) — Identifying and mitigating requirement-related risks
```

## Capability Area Overview (00_overview.md)

### Key Sections

1. **One-line definition:** "A senior engineer defines the right problem before building a solution, reducing ambiguity through structured analysis rather than waiting for perfect clarity."

2. **Topic notes table:** All 8 topics marked ✅ Done with file links

3. **Concept map:** Mermaid flowchart showing topic dependencies:
   ```mermaid
   flowchart TD
       P["01 Problem Statement"] --> C["02 Current/Future State"]
       C --> S["03 Stakeholder Management"]
       S --> U["04 User/Business Outcomes"]
       U --> A["05 Acceptance Conditions"]
       P --> AMB["06 Ambiguity Reduction"]
       AMB --> A
       U --> PRI["07 Prioritization"]
       PRI --> R["08 Requirements Risk"]
       A --> R
   ```

4. **Existing vault anchors table:**

| Senior topic | Existing foundation notes |
|---|---|
| Problem Statement Definition | [[software-engineering-note/01_Software_Requirements/01_Requirements_Fundamentals]], [[body-of-knowledge/BABOK/04_Strategy_Analysis]] |
| Current and Future State | [[body-of-knowledge/BABOK/04_Strategy_Analysis]] (Analyze Current State, Define Future State) |
| Stakeholder Management | [[software-engineering-note/01_Software_Requirements/03_Requirements_Elicitation]], [[body-of-knowledge/BABOK/02_Elicitation_and_Collaboration]] |
| User and Business Outcomes | [[software-engineering-note/01_Software_Requirements/02_Business_and_User_Requirements]] |
| Acceptance Conditions | [[software-engineering-note/01_Software_Requirements/13_ATDD_BDD_and_Acceptance]] |
| Ambiguity Reduction | [[software-engineering-note/01_Software_Requirements/07_Quality_and_Prototyping]] |
| Prioritization | [[software-engineering-note/01_Software_Requirements/08_Prioritization_Validation_and_Reuse]] |
| Requirements Risk | [[software-engineering-note/01_Software_Requirements/11_Tools_Process_Improvement_and_Risk]] |

5. **Self-assessment checklist:** 8 yes/no questions including:
   - "I can write a problem statement that does not mention a solution"
   - "I have identified the current state and future state for my current project"
   - "I have facilitated a prioritization session with conflicting stakeholders"

## Topic Notes

### 01_Problem_Statement_Definition.md

**One-line definition:** "Writing a clear, solution-free description of the problem to be solved, so the team can evaluate multiple approaches before committing to one."

**Key frameworks:**
- Problem statement template (4 components: current state, impact, desired state, constraints)
- Four common failures table (solution-in-disguise, vague complaint, blame statement, symptom-not-cause)
- Five Whys technique with worked example

**Practical exercise:** Take a current project and rewrite its problem statement using the four-component template

### 02_Current_and_Future_State.md

**One-line definition:** "Understanding where the system, process, or organization is today and defining where it needs to be, so the team can design a path that closes the gap."

**Key frameworks:**
- Current state analysis table (5 dimensions: technical, process, people, data, business)
- Future state definition table (5 dimensions with measurable outcomes)
- Gap analysis template (columns: capability, current state, future state, gap, priority, effort, risk)
- Priority matrix (impact vs effort: quick wins, strategic bets, fill-ins, avoid)

**Practical exercise:** Document current state, define future state, and conduct a gap analysis for your current project

### 03_Stakeholder_Management.md

**One-line definition:** "Knowing who cares about the problem, what they each need, and how to align their interests so the team can build something that works for everyone."

**Key frameworks:**
- Stakeholder identification checklist (3 categories: direct, indirect, technical, external)
- Power-interest grid (4 quadrants: manage closely, keep satisfied, keep informed, monitor)
- Elicitation techniques table (interviews, workshops, observation, surveys, prototypes)
- Hidden stakeholder problem (4 common hidden stakeholders)

**Practical exercise:** Build a stakeholder map and elicitation plan for your current project

### 04_User_and_Business_Outcomes.md

**One-line definition:** "Connecting every requirement to a measurable user or business outcome, so the team knows why they are building each feature and how to verify it delivers value."

**Key frameworks:**
- Outcome hierarchy diagram (business outcomes → user outcomes → features)
- Outcome traceability matrix (feature, user outcome, business outcome, success metric)
- "So what?" test with worked example
- SMART criteria (specific, measurable, achievable, relevant, time-bound)

**Practical exercise:** Trace three features to business outcomes using the "so what?" test

### 05_Acceptance_Conditions.md

**One-line definition:** "Defining how success will be verified before implementation begins, so the team builds something that can be objectively validated."

**Key frameworks:**
- Three levels of acceptance table (business, user, technical)
- Acceptance condition template (business, user, technical sections with checkboxes)
- Characteristics of good acceptance conditions (testable, specific, measurable, complete, agreed)
- Given-When-Then format for user-facing acceptance criteria
- Team definition of done template (code quality, testing, documentation, operations, acceptance)

**Practical exercise:** Write acceptance conditions for a current feature using the three-level template

### 06_Ambiguity_Reduction.md

**One-line definition:** "Making progress when requirements are unclear by systematically reducing ambiguity through structured analysis, prototyping, and stakeholder engagement."

**Key frameworks:**
- Ambiguity types table (5 types: problem, solution, stakeholder, technical, scope)
- Ambiguity reduction process flowchart (7 steps: identify, classify, assess, proceed/reduce, validate, monitor)
- Useful vs blocking ambiguity decision criteria
- Reduction techniques table (problem decomposition, spike experiments, facilitated alignment, proof of concept, explicit boundaries)
- Assumption log template

**Practical exercise:** Classify and reduce the top 3 ambiguities in your current project

### 07_Prioritization.md

**One-line definition:** "Deciding what matters most when resources are limited, making explicit trade-offs between competing needs, and communicating the reasoning to stakeholders."

**Key frameworks:**
- Four prioritization frameworks (MoSCoW, WSJF, value-effort matrix, RICE scoring)
- Trade-off matrix template (decision, what we gain, what we give up, risk, mitigation)
- Iron triangle diagram (scope, time, cost, quality)
- Cost of delay calculation table
- Prioritization anti-patterns table (6 patterns: HiPPO, everything-is-priority-1, loudest voice, sunk cost, scope creep, analysis paralysis)

**Practical exercise:** Prioritize 10 requirements using a structured framework (MoSCoW, WSJF, or RICE)

### 08_Requirements_Risk.md

**One-line definition:** "Identifying, assessing, and mitigating risks that arise from requirements themselves: incomplete requirements, changing requirements, conflicting requirements, and requirements that cannot be met."

**Key frameworks:**
- Requirements risk taxonomy (7 categories: completeness, correctness, consistency, feasibility, volatility, ambiguity, dependency)
- Risk management process flowchart (5 steps: identify, assess, prioritize, mitigate, monitor)
- Probability-impact matrix (3x3 grid: low/medium/high)
- Five mitigation strategies table (avoid, mitigate, transfer, accept, contingency)
- Requirements risk register template (columns: ID, risk, category, probability, impact, risk level, mitigation, owner, status)

**Practical exercise:** Build a requirements risk register for your current project (5 steps)

## Overlay Strategy in Action

**Duplication avoidance:** Every topic note links to 3-5 existing SWEBOK/BABOK notes for foundational knowledge. The overlay notes focus on "what's different at senior level" rather than re-teaching concepts.

**Example from 01_Problem_Statement_Definition.md:**
- Links to: [[software-engineering-note/01_Software_Requirements/01_Requirements_Fundamentals]]
- Does NOT re-explain what requirements are or how to elicit them
- DOES explain how a senior engineer frames problems, avoids solution-in-disguise, and uses the Five Whys

**Example from 07_Prioritization.md:**
- Links to: [[software-engineering-note/01_Software_Requirements/08_Prioritization_Validation_and_Reuse]]
- Does NOT re-explain what prioritization is
- DOES explain how a senior engineer facilitates prioritization workshops, makes trade-offs explicit, and quantifies cost of delay

## Verification Results

All files pass verification:
- Zero em-dashes (used colons throughout)
- Zero ASCII trees (used Mermaid diagrams)
- 8 Mermaid diagrams total (all using `flowchart` syntax)
- No parentheses in Mermaid labels
- No dots after numbers in Mermaid labels
- No bare ampersands in Mermaid labels

## User Feedback

User approved this capability area and is proceeding to the next one (Architecture and Design Judgment), indicating the structure and approach are working well.

## Key Insights from This Build

1. **Problem framing is foundational:** This capability area is larger than Technical Ownership (9 files vs 7) because problem framing touches more dimensions (problem, state, stakeholders, outcomes, acceptance, ambiguity, prioritization, risk).

2. **Comparison tables are powerful:** Every topic note includes "mid-level approach vs senior approach" tables that make the overlay strategy concrete.

3. **Practical exercises drive adoption:** Every topic ends with a hands-on exercise the reader can do on their current project, making the knowledge immediately applicable.

4. **Frameworks over theory:** Each topic provides 2-4 structured frameworks (templates, checklists, matrices) rather than abstract advice.

5. **Cross-linking to BABOK:** This capability area links to both SWEBOK and BABOK notes, showing how senior engineers draw from multiple knowledge bodies.
