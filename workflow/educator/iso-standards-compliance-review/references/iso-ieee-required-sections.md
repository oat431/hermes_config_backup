# ISO/IEEE Required Sections Reference

> Pre-researched outlines for 15 major ISO/IEEE/IEC standards. Compiled July 2026.
> **Confidence note:** Version years reflect training knowledge (through early 2025). Standard content/structure is stable for well-established standards. Always verify against current published standard for formal compliance audits.

---

## Priority Standards (Prescriptive: define required sections)

### 1. ISO/IEC/IEEE 29148:2018 — Requirements Engineering (SRS)

**Type:** Process + practice standard with informative SRS outline (Annex C)
**Supersedes:** IEEE 830-1998

#### SRS Outline (Annex C — informative but de facto industry baseline):

```
1. Introduction
   1.1 Purpose
   1.2 Scope / Document scope
   1.3 Definitions, acronyms and abbreviations
   1.4 References
   1.5 Overview of the SRS
2. Overall Description
   2.1 Product perspective
   2.2 Product functions
   2.3 User characteristics
   2.4 Constraints
   2.5 Assumptions and dependencies
   2.6 Apportioning of requirements
3. Specific Requirements
   3.1 External interfaces (user, hardware, software, communications)
   3.2 Functions (functional requirements)
   3.3 Performance requirements
   3.4 Design constraints
   3.5 Software system attributes (quality attributes)
   3.6 Other requirements
4. Verification & Acceptance Criteria
Annexes: Analysis models, Issues list, Traceability matrix
```

**Compliance notes:**
- Each requirement should have: unique ID, description, rationale, source, priority, and **acceptance criteria** (normative requirement for well-formed requirements)
- Requirements must be: traceable, verifiable, feasible, necessary, unambiguous, complete
- Annex C is *informative* but represents the accepted industry baseline

---

### 2. IEEE 828-2012 — Configuration Management Plan (SCMP)

**Type:** Process standard with SCMP content outline (Annex A)

#### SCMP Outline (Annex A):

```
1. Introduction (Purpose, Scope, Terms, References)
2. SCM Management / Organization
   2.1 Organization
   2.2 SCM responsibilities
   2.3 Authorities (who approves changes)
   2.4 Policies and directives
   2.5 SCM procedures
3. SCM Activities (5 required CM processes)
   3.1 Configuration identification (CIs, baselines, naming)
   3.2 Configuration control (change request process, CCB)
   3.3 Configuration status accounting (reporting)
   3.4 Configuration audits and reviews (FCA, PCA)
   3.5 Release management and delivery
4. SCM Schedules
5. SCM Resources (Tools, Personnel, Training, Facilities)
6. SCM Plan Maintenance
```

**Compliance notes:**
- The **five CM processes** (Identification, Change Control, Status Accounting, Audits, Release Management) are the structural backbone
- A **Configuration Control Board (CCB)** with defined membership and authority must be described
- **Baselines** must be defined with their points of establishment

---

### 3. IEEE 730-2014 — Software Quality Assurance (SQAP)

**Type:** Process standard (no rigid document outline in 2014 version)

#### SQAP Content (derived from process requirements):

```
1. Purpose
2. Reference documents
3. Management / Organization
   - SQA organizational structure
   - SQA tasks and responsibilities
   - Independence of SQA function (CRITICAL)
4. Documentation
5. Standards, Practices, Conventions, and Metrics
6. Reviews and Audits
7. Test
8. Problem Reporting and Corrective Action
9. Tools, Techniques, and Methodologies
10. Code / Media Control
11. Supplier Control
12. Records Collection, Maintenance, and Retention
13. Training
14. Risk Management
15. SQA Plan Maintenance
```

**Compliance notes:**
- IEEE 730-2014 is **more process-oriented** than the 2002 version
- **Independence of SQA** is a core requirement (organizational independence from development)
- Must address both **process assurance** and **product assurance**
- Must include **noncompliance/deviation reporting** escalation

---

### 4. ISO/IEC/IEEE 29119-3:2013 — Software Testing Documentation

**Type:** Test documentation standard with test plan outline (Annex)
**Supersedes:** IEEE 829-2008

#### Test Plan Outline (16 sections):

```
1.  Test plan identifier
2.  Introduction (Purpose, Scope, References)
3.  Test items
4.  Features to be tested
5.  Features not to be tested (with rationale)
6.  Approach / Test strategy
7.  Item pass/fail criteria
8.  Suspension criteria and resumption requirements
9.  Test deliverables
10. Testing tasks
11. Environmental needs
12. Responsibilities
13. Staffing and training needs
14. Schedule
15. Risks and contingencies
16. Approvals
```

**Compliance notes:**
- Test plan is part of a documentation set: also includes Test Design Spec, Test Case Spec, Test Procedure Spec, Test Item Transmittal Report, Test Log, Test Incident Report, Test Summary Report
- **Entry/exit criteria** and **suspension/resumption criteria** are mandatory
- Must define the relationship between test strategy and test levels

---

### 5. IEEE 1012-2017 — V&V (Verification and Validation)

**Type:** Process standard with V&V plan outline (Annex — informative)

#### V&V Plan Content:

```
1. Purpose / Scope
2. V&V Overview
   2.1 Organization (team structure, independence)
   2.2 Master schedule
   2.3 Software integrity level (1-4, determines V&V rigor)
   2.4 Resources
   2.5 Responsibilities
   2.6 Tools, techniques, methodologies
3. V&V Processes
   3.1 Management of V&V
   3.2 Acquisition of V&V
   3.3 Supply of V&V
4. V&V Reporting Requirements
5. V&V Administrative Requirements
   5.1 Anomaly resolution and reporting
   5.2 Task iteration policy
   5.3 Control of V&V process
   5.4 Control of V&V documentation
6. V&V Documentation Requirements
7. V&V Activity Plans (by lifecycle phase)
   For each: Concept, Requirements, Design, Implementation, Test,
   Installation/Checkout, Operation, Maintenance
8. Standards, regulations, and practices
9. Metrics
10. Risk
11. Glossary
```

**Compliance notes:**
- **Software/Hardware/System Integrity Level** (1-4) determines which V&V tasks are mandatory
- V&V must be organized by **lifecycle phase** (8 phases)
- **Independence** of V&V required (technical, managerial, and/or financial)
- V&V **task reports** and **anomaly reports** are required deliverables

---

## Process Standards (Non-prescriptive: check traceability, not sections)

### 6. ISO/IEC/IEEE 42010:2022 — Architecture Description

**Type:** Meta-standard (defines concepts, NOT a document outline)

**Required concepts (not sections):**
- Identification of stakeholders and their concerns
- Architecture viewpoints (each with: stakeholders, concerns, model kinds)
- Architecture views (concrete instantiations of viewpoints)
- Architecture models
- Correspondences (relationships between views)
- Correspondence rules
- Architecture rationale
- Architecture framework reference (if used)

**Note:** The 4+1 View Model (Kruchten) aligns *spiritually* but is NOT mandated by 42010.

---

### 7. ISO/IEC/IEEE 12207:2015 — Software Life Cycle Processes

**Type:** Process standard (no document template)

**Process categories:**
- Agreement: Acquisition, Supply
- Organizational Project-Enablement: Life Cycle Model Mgmt, Infrastructure, Portfolio, HR, Quality Mgmt
- Project: Planning, Assessment & Control, Decision Mgmt, Risk Mgmt, Configuration Mgmt, Measurement, QA
- Technical: Business/Mission Analysis, Stakeholder Needs, System Requirements, System Architecture, Design Definition, System Analysis, Implementation, Integration, Verification, Transition, Validation, Operation, Maintenance, Disposal

**Use for:** Process traceability (map document activities to 12207 processes)

---

### 8. ISO/IEC/IEEE 15288:2023 — System Life Cycle Processes

**Type:** Process standard (system counterpart to 12207)

Same process categories as 12207 but for **systems** (broader than software). Templates reference 15288 for system-level process coverage. Same audit approach as 12207.

---

### 9. ISO 31000:2018 — Risk Management

**Type:** Guidelines (not certifiable)

**Risk management process:**
```
3.1 Communication and consultation
3.2 Scope, context and criteria
3.3 Risk assessment (identification → analysis → evaluation)
3.4 Risk treatment
3.5 Monitoring and review
3.6 Recording and reporting
```

**Compliance notes:** A Risk Register/Plan should include: identification method, analysis approach (likelihood x impact), evaluation criteria, treatment options (mitigate, transfer, avoid, accept), and monitoring cadence.

---

### 10. ISO/IEC 25010:2023 — SQuaRE Quality Model

**Type:** Quality model (reference, not document/process standard)

**8 quality characteristics:**
1. Functional suitability (completeness, correctness, appropriateness)
2. Performance efficiency (time behavior, resource utilization, capacity)
3. Compatibility (co-existence, interoperability)
4. Usability (learnability, operability, user error protection, accessibility)
5. Reliability (maturity, availability, fault tolerance, recoverability)
6. Security (confidentiality, integrity, non-repudiation, accountability, authenticity)
7. Maintainability (modularity, reusability, analysability, modifiability, testability)
8. Portability (adaptability, installability, replaceability)

**Also defines:** Quality in use model (5 characteristics: effectiveness, efficiency, satisfaction, freedom from risk, context coverage)

**Note:** 25010:2023 may have updated sub-characteristics from the widely-used 2011 version. Verify if formal compliance needed.

---

### 11. ISO 21502:2020 — Project Management Guidance

**Type:** Guidance (not certifiable)

Covers 5 process groups (Initiating, Planning, Executing, M&C, Closing) and knowledge areas (Integration, Scope, Schedule, Cost, Resource, Risk, Quality, Communication, Procurement, Stakeholder). Aligned with PMBOK.

---

### 12. ISO/IEC 27001:2022 — Information Security Management

**Type:** Certifiable requirements standard

**10 clauses (4-10):** Context, Leadership, Planning, Support, Operation, Performance evaluation, Improvement

**Annex A (2022):** 93 controls in 4 themes:
- Organizational (37)
- People (8)
- Physical (14)
- Technological (34)

**RED FLAG:** Templates citing "14 domains, 114 controls" are based on the **outdated 2013 version**.

---

### 13. ISO/IEC/IEEE 14764:2006 — Software Maintenance

**Type:** Process standard

**6 maintenance activities:**
1. Process implementation (maintenance plan)
2. Problem and modification analysis
3. Modification implementation
4. Maintenance review/acceptance
5. Migration
6. Retirement

**4 maintenance types:** Corrective, Adaptive, Perfective, Preventive

**Note:** Aging standard. Many organizations reference 12207:2015's maintenance process instead.

---

### 14. ISO/IEC 20000-1:2018 — Service Management

**Type:** Certifiable SMS standard

**IMPORTANT:** Official designation is `ISO/IEC 20000-1` (NOT `ISO/IEC/IEEE 20000-1`). IEEE was never a co-author.

**Service management processes:** SLA management, incident management, problem management, change management, configuration management, release & deployment, continuity & availability, capacity management.

---

### 15. ISO 22301:2019 — Business Continuity Management

**Type:** Certifiable BCMS standard

A DR Plan is one component of a full BCMS. For full ISO 22301 compliance, also need: Business Impact Analysis (BIA), Business Continuity Plan (BCP), and continuity strategy.

---

## Quick Reference: Standard Type and Audit Approach

| Standard | Type | How to Audit |
|---|---|---|
| 29148 | Process + Annex outline | Section-by-section comparison with Annex C |
| 828 | Process + Annex outline | Section-by-section comparison with Annex A |
| 730 | Process (no rigid outline) | Check process requirements are addressed |
| 29119-3 | Documentation outline | Section-by-section comparison (16 sections) |
| 1012 | Process + Annex outline | Check integrity levels + lifecycle phases |
| 42010 | Meta-standard | Check stakeholder→concern→viewpoint→view mapping |
| 12207 | Process | Check process traceability |
| 15288 | Process | Check process traceability |
| 31000 | Guidelines | Check risk process steps |
| 25010 | Quality model | Check 8 characteristics are addressed |
| 21502 | Guidance | Check process groups + knowledge areas |
| 27001 | Requirements (certifiable) | Check 10 clauses + Annex A controls |
| 14764 | Process | Check 6 activities + 4 maintenance types |
| 20000-1 | Requirements (certifiable) | Check SMS processes |
| 22301 | Requirements (certifiable) | Check BCMS components |
