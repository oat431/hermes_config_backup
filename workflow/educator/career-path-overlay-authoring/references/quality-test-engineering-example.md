# Quality and Test Engineering: Specialist Path Worked Example

**Built:** 2026-08-05  
**Location:** `F:\obsidian_note\swe-knowledge\career-path\10_Quality_and_Test_Engineering\`  
**Stats:** 44 files, 483 KB, 35 Mermaid diagrams, 0 em-dashes

## Overview

This is a complete specialist career path built as an overlay on existing BOKs (SWEBOK Software Testing, Software Quality). It demonstrates how to structure a specialist path that branches from Senior SWE and focuses on domain mastery rather than scope expansion.

## Capability Areas

| # | Area | Files | Focus |
|---|------|-------|-------|
| 1 | Test Strategy | 7 | Risk-based testing, test planning, estimation, release decisions, stakeholder communication |
| 2 | Test Design | 8 | Equivalence partitioning, BVA, decision tables, state transitions, use cases, exploratory testing |
| 3 | Automation | 7 | Strategy, framework design, maintainable tests, CI/CD integration, flaky test management, ROI analysis |
| 4 | Quality Engineering | 7 | Defect prevention, code reviews, static analysis, continuous improvement, metrics, quality culture |
| 5 | Specialized Testing | 7 | Performance, security, reliability, accessibility, API, mobile testing |
| 6 | Measurement | 7 | Defect metrics, coverage metrics, process metrics, quality reporting, data analysis, measurement pitfalls |

## Key Design Decisions

### 1. Separation of concerns

- **Test Strategy** = planning and decision-making (what to test, when, why)
- **Test Design** = techniques for creating effective tests (how to test)
- **Automation** = implementation and maintenance of automated tests
- **Quality Engineering** = preventing defects through process and practices
- **Specialized Testing** = domain-specific testing (performance, security, etc.)
- **Measurement** = using metrics to drive improvement (without gaming)

### 2. Specialist vs. generalist framing

**Generalist (Senior SWE):** "A senior engineer writes tests for their code."  
**Specialist (Quality Engineer):** "A specialist designs test strategy for the organization, builds automation frameworks, and uses metrics to drive quality improvement."

### 3. Practical depth over theory

Each topic includes:
- Real code examples (Python, JavaScript, YAML)
- Tool recommendations (pytest, Jest, SonarQube, etc.)
- Checklists and decision frameworks
- Common pitfalls and anti-patterns

## Topic Breakdown

### 01_Test_Strategy (7 files)
- Risk-Based Testing
- Test Levels and Scope
- Test Planning
- Test Estimation
- Release Strategy
- Stakeholder Communication

### 02_Test_Design (8 files)
- Equivalence Partitioning
- Boundary Value Analysis
- Decision Table Testing
- State Transition Testing
- Use Case Testing
- Exploratory Testing
- Test Design Strategy

### 03_Automation (7 files)
- Automation Strategy
- Test Framework Design
- Maintainable Tests
- CI/CD Integration
- Flaky Test Management
- ROI Analysis

### 04_Quality_Engineering (7 files)
- Defect Prevention
- Code Reviews
- Static Analysis
- Continuous Improvement
- Quality Metrics
- Quality Culture

### 05_Specialized_Testing (7 files)
- Performance Testing
- Security Testing
- Reliability Testing
- Accessibility Testing
- API Testing
- Mobile Testing

### 06_Measurement (7 files)
- Defect Metrics
- Coverage Metrics
- Process Metrics
- Quality Reporting
- Data Analysis
- Measurement Pitfalls

## Lessons Learned

### What worked well

1. **Clear separation between strategy and design:** Test Strategy focuses on decisions, Test Design focuses on techniques. No overlap.

2. **Measurement as its own area:** Quality measurement is complex enough (Goodhart's Law, gaming, pitfalls) to warrant dedicated coverage. The "Measurement Pitfalls" topic is critical for preventing metric abuse.

3. **Specialized Testing as a catch-all:** Performance, security, accessibility, API, mobile testing each got their own file. This keeps them discoverable without creating separate capability areas.

4. **Code examples throughout:** Every topic includes practical code snippets (pytest, Jest, Appium, etc.) that readers can adapt immediately.

5. **Anti-patterns explicitly called out:** Measurement Pitfalls, Automation ROI myths, Coverage obsession, etc. These prevent common mistakes.

### What to watch for

1. **Automation is not just "write tests":** The Automation area covers strategy, framework design, maintenance, CI/CD integration, flaky tests, and ROI. It's a full engineering discipline.

2. **Quality Engineering ≠ Testing:** Quality Engineering focuses on prevention (code reviews, static analysis, culture) while Testing focuses on detection. Both are needed.

3. **Metrics are dangerous:** The Measurement area spends significant time on pitfalls (Goodhart's Law, gaming, vanity metrics). This is intentional: misused metrics cause more harm than no metrics.

4. **Specialized Testing depth:** Each specialized area (performance, security, etc.) could be its own career path. These files provide foundations, not mastery.

## Vault Connections

The path links to:
- `software-engineering-note/05_Software_Testing/` (12+ testing topics)
- `software-engineering-note/12_Software_Quality/` (quality management)
- `software-engineering-note/06_Software_Engineering_Operations/` (CI/CD, deployment)
- `software-engineering-note/10_Software_Engineering_Management/` (project metrics)

## Execution Notes

**Built sequentially:** Each capability area was built completely before moving to the next. This allowed for consistent structure and cross-referencing.

**Verification after each area:**
- em-dash check (should be 0)
- Mermaid diagram count
- File count and size
- Wikilink validation

**Total build time:** ~45 minutes for 44 files across 6 areas.

## Use This Example When

- Building a specialist engineering path (SRE, Security, Data/ML, Quality)
- Structuring a career path with 6+ capability areas
- Creating technical depth in a specific domain
- Avoiding duplication with existing BOK notes
- Including practical code examples and tool recommendations
