# Designer Handoff Meeting Minute Template

> Use this template when creating a PO → Designer handoff meeting minute for a new project.
> Adapt sections based on project complexity.

---

## Meeting Minutes — PO → Designer Handoff: [Project Name] Phase [N]

> **Date:** [YYYY-MM-DD]
> **Type:** Requirements Handoff
> **From:** PO Persona
> **To:** Designer Persona
> **Status:** ✅ Phase [N] requirements complete. Ready for design.

---

## 1. Purpose

> Record completion of Phase [N] requirements and hand off to Designer for wireframes, architecture design, and UI/UX.

---

## 2. What PO Produced

### Spec Documents

| Document | Path | Status | Key Metrics |
|----------|------|--------|-------------|
| Business Objectives | `01_requirement/011_business_objective.md` | ✅ | [X] objectives, [Y] KPIs |
| User Stories | `01_requirement/012_user_stories.md` | ✅ | [X] stories, [Y] epics, [Z] points |
| Acceptance Criteria | `01_requirement/013_acceptance_criteria.md` | ✅ | [X] BDD criteria ([Y]🔴, [Z]🟡) |

---

## 3. Key Architecture Decisions

| Decision ID | Decision | Rationale | Impact |
|------------|---------|-----------|--------|
| DEC-001 | [Tech stack choice] | [Why] | [Scope] |
| DEC-002 | [Database choice] | [Why] | [Scope] |

---

## 4. Integration Points (What Designer Needs to Know)

| Service | Integration Type | Key Details |
|---------|-----------------|-------------|
| [Service A] | [REST/WebSocket/etc] | [Ports, auth, rate limits] |

---

## 5. Phase [N] Scope — What Designer Must Deliver

### 🔴 Must Have

| # | Document | Template Path | What It Covers |
|---|----------|--------------|----------------|
| 1 | Architecture Decision Records | `02_design/021_...` | [Content] |
| 2 | API Specification | `02_design/022_...` | [Content] |
| 3 | Database Schema (DDL) | `02_design/023_...` | [Content] |

### 🟡 Should Have

| # | Document | Template Path | What It Covers |
|---|----------|--------------|----------------|
| 4 | Wireframes | `02_design/026_...` | [Content] |
| 5 | Style Guide | `02_design/028_...` | [Content] |

---

## 6. Design Questions for Designer to Resolve

| # | Question | Context | Suggested Approach |
|---|----------|---------|-------------------|
| 1 | [Question] | [Why it matters] | [Hint] |

---

## 7. Technical Constraints (Designer Must Respect)

| Constraint | Detail |
|-----------|--------|
| [Deployment] | [Where it runs] |
| [Database] | [Which DB, version] |

---

## 8. Decisions Needed from Designer

| Decision ID | Question | Options |
|:-----------:|---------|---------|
| DEC-D01 | [Question] | [Option A / Option B] |

---

## 9. Action Items

| Action ID | Action | Owner | Priority | Depends On |
|-----------|--------|:-----:|:--------:|:----------:|
| D-001 | Review PO spec documents | Designer | 🔴 | — |
| D-002 | Make design decisions | Designer | 🔴 | D-001 |
| D-003 | Produce design documents | Designer | 🔴 | D-002 |
| D-004 | Handoff to Dev | Designer | 🔴 | D-003 |

---

## 10. Handoff Summary

### What Designer Gets
1. [List of deliverables]

### What Designer Needs to Produce
1. [List of expected documents]

### What Designer Needs to Decide
1. [List of decisions]
