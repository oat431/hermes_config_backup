# Senior SWE Technical Ownership — Complete Worked Example

**Created:** Session 2026-08-05  
**Total files:** 7  
**Total size:** 56.6 KB  
**Location:** `F:\obsidian_note\swe-knowledge\career-path\02_Senior_Software_Engineer\01_Technical_Ownership\`

## File Structure

```text
01_Technical_Ownership/
├── 00_overview.md                    (5.0 KB) — Progress tracker + concept map
├── 01_System_Ownership.md            (6.3 KB) — Understanding your system boundary
├── 02_Lifecycle_Ownership.md         (7.3 KB) — Managing across the development lifecycle
├── 03_Technical_Debt_and_Maintainability.md (9.2 KB) — Strategic debt management
├── 04_Production_Responsibility.md   (8.9 KB) — Observability, incidents, reliability
├── 05_Decision_Ownership.md          (9.4 KB) — ADRs and decision-making process
└── 06_Ownership_Evidence.md         (10.6 KB) — Building promotion evidence
```

## Capability Area Overview (00_overview.md)

### Key Sections

1. **One-line definition:** "A senior engineer owns a system area end-to-end, from problem understanding through production operation, and is accountable for its health over time."

2. **Topic notes table:** All 6 topics marked ✅ Done with file links

3. **Concept map:** Mermaid flowchart showing topic dependencies:
   ```mermaid
   flowchart TD
       S["01 System Ownership"] --> L["02 Lifecycle Ownership"]
       L --> D["03 Technical Debt and Maintainability"]
       L --> P["04 Production Responsibility"]
       D --> J["05 Decision Ownership"]
       P --> J
       J --> E["06 Ownership Evidence"]
       D --> E
   ```

4. **Existing vault anchors table:**

| Senior topic | Existing foundation notes |
|---|---|
| System Ownership | [[software-engineering-note/07_Software_Maintenance/Software Maintenance Overview]] |
| Lifecycle Ownership | [[software-engineering-note/01_Software_Requirements/Software Requirements Overview]] |
| Technical Debt | [[software-engineering-note/07_Software_Maintenance/07_Maintenance_Fundamentals]] |
| Production Responsibility | [[software-engineering-note/06_Software_Engineering_Operations/08_Service_Operations_and_Support]] |
| Decision Ownership | [[software-engineering-note/02_Software_Architecture/09_Evaluation_and_Governance]] |
| Ownership Evidence | [[document-template/00_Essential Document/Essential Documents - Overview]] |

5. **Self-assessment checklist:** 8 yes/no questions including:
   - "I can name every external dependency my system relies on"
   - "I have written or updated an Architecture Decision Record in the last quarter"
   - "My team can operate my system without me being present"

## Topic Notes

### 01_System_Ownership.md

**One-line definition:** "Knowing the full surface area of a system you are accountable for, including what it does, what depends on it, and what could go wrong."

**Key frameworks:**
- Four surfaces table (inputs, outputs, dependencies, state)
- Ownership handoff checklist (7 items: system map, runbook, risk register, debt inventory, contact list, recent incidents, open work)

**Practical exercise:** Complete a system boundary checklist for your current primary system

### 02_Lifecycle_Ownership.md

**One-line definition:** "Following your system from the initial problem statement through requirements, design, implementation, testing, deployment, operation, and eventual retirement."

**Key frameworks:**
- Mid-level vs senior role comparison table across 7 lifecycle phases
- Operational readiness review checklist (8 checks: monitoring, alerting, runbooks, rollback, capacity, security, data, dependencies)

**Practical exercise:** Trace one feature from end-to-end across all 8 lifecycle questions

### 03_Technical_Debt_and_Maintainability.md

**One-line definition:** "Managing technical debt strategically rather than reactively, so the system remains maintainable and the team remains productive over time."

**Key frameworks:**
- Debt taxonomy table (4 types: prudent/deliberate, prudent/inadvertent, reckless/deliberate, reckless/inadvertent)
- Debt inventory template (columns: item, impact, effort, risk, priority)
- Business translation table (technical description → business translation)
- Debt budget percentages (10-15% healthy, 20-30% significant debt, 40%+ crisis)

**Practical exercise:** Create a technical debt inventory for your current system (5 steps)

### 04_Production_Responsibility.md

**One-line definition:** "Being accountable for a system's health after it ships, not just until it passes testing."

**Key frameworks:**
- Three pillars: observability, incident response, reliability engineering
- Observability stack diagram (metrics, logs, traces → alert, dashboard, investigate)
- Incident response roles table (commander, investigator, communicator, scribe)
- Production readiness checklist (4 sections: monitoring, resilience, operations, deployment)

**Practical exercise:** Evaluate your current system's production readiness (5 questions)

### 05_Decision_Ownership.md

**One-line definition:** "Making technical decisions deliberately, recording them so others can understand the reasoning, and standing behind the consequences."

**Key frameworks:**
- Decision types table (routine, consequential, strategic)
- ADR template (status, context, options considered, decision, consequences, follow-up actions)
- Decision anti-patterns table (6 patterns: accidental, resume-driven, consensus paralysis, authority override, avoidance, cargo culting)

**Practical exercise:** Write an ADR for a decision you made or are about to make (6 steps)

### 06_Ownership_Evidence.md

**One-line definition:** "Building a documented record of outcomes, decisions, and improvements that demonstrates senior-level technical ownership for promotion and career growth."

**Key frameworks:**
- Evidence portfolio (5 categories: outcomes, decisions, problem prevention, influence, artifacts)
- Weak vs strong evidence comparison table (task description → outcome evidence)
- Evidence log template (markdown structure for quarterly logging)
- Promotion case template (summary, technical ownership, problem prevention, influence, evidence artifacts)

**Practical exercise:** Start your evidence log today (4 steps)

## Overlay Strategy in Action

**Duplication avoidance:** Every topic note links to 3-5 existing SWEBOK notes for foundational knowledge. The overlay notes focus on "what's different at senior level" rather than re-teaching concepts.

**Example from 01_System_Ownership.md:**
- Links to: [[software-engineering-note/07_Software_Maintenance/07_Maintenance_Fundamentals]]
- Does NOT re-explain what maintenance is
- DOES explain how a senior engineer defines ownership boundaries and manages handoffs

**Example from 03_Technical_Debt_and_Maintainability.md:**
- Links to: [[software-engineering-note/15_Software_Engineering_Economics/Software Engineering Economics Overview]]
- Does NOT re-explain what technical debt is
- DOES explain how a senior engineer creates a debt inventory, negotiates a debt budget, and translates debt into business terms

## Verification Results

All files pass verification:
- Zero em-dashes (used colons throughout)
- Zero ASCII trees (used Mermaid diagrams)
- 7 Mermaid diagrams total (all using `flowchart` syntax)
- No parentheses in Mermaid labels
- No dots after numbers in Mermaid labels
- No bare ampersands in Mermaid labels

## User Feedback

User approved this capability area and immediately requested the next one (Problem Framing and Requirements), indicating the structure and approach were correct.
