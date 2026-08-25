# SWEBOK v4 Chapters 06-10 Gap Analysis (Session Reference)

> **Session:** 2026-07-21
> **Task:** Multi-chapter SWEBOK gap analysis for chapters 06-10
> **Vault:** `F:\obsidian_note\swe-knowledge\software-engineering-note\`
> **Reference:** `F:\obsidian_note\swe-knowledge\body-of-knowledge\SWEBOK\`
> **Report saved to:** `C:\Users\Admin\swebok_gap_analysis_06-10.md`

## Workflow Notes

This session followed the multi-chapter batch pattern established in the ch11-15 session. 5 chapters analyzed via:
1. Batch-read all 5 SWEBOK reference files (1 turn)
2. Batch-read all 5 vault overview files + `ls` each folder for inventory (1 turn)
3. Batch-read 2-3 representative note files per chapter across 2 turns (including subdirectory notes: `Fundamental/` for ch06, `Version Control/` for ch08)
4. Compile full report with per-chapter sections + cross-chapter summary table + priority recommendations

**Subdirectory discovery:** Chapter 06 had a `Fundamental/` subfolder with CI/CD and Docker notes; Chapter 08 had a `Version Control/` subfolder with 3 Git notes. These subdirectories contributed materially to coverage and must not be skipped during inventory. Use `ls -la` per folder and check for subdirectories explicitly.

## Per-Chapter Coverage Findings

### Chapter 06 — Software Engineering Operations (~65% coverage)

**Source-book bias:** DevOps Handbook (Kim, Humble, Debois, Willis) — excellent on DevOps culture, Three Ways, CI/CD, DevSecOps; thinner on traditional operations planning and governance.

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Fundamentals | ✅ | Three Ways, operations engineer role, CI/CD fundamentals |
| Operations Planning | ⚠️ | SLAs/capacity mentioned; no DR/failover/environment parity/supplier mgmt |
| Operations Delivery | ✅ | Deployment strategies, CI/CD, change management well covered; problem management missing |
| Operations Control | ⚠️ | Telemetry/incident management covered; service desks/service reporting/KPIs missing |
| Practical Considerations | ⚠️ | Automation/risk touched; ISO/IEC 29110 for VSEs completely missing |
| Operations Tools | ✅ | Containers, CI/CD toolchains, monitoring well covered; orchestrators mentioned |

**Top gaps:** Capacity management (dedicated), Backup/DR/failover, Service reporting & KPIs, Service desks, Problem management (distinct from incident mgmt), ISO/IEC 29110, Environment parity.

### Chapter 07 — Software Maintenance (~40% coverage)

**Source-book bias:** Feathers' *Working Effectively with Legacy Code* — deep on program comprehension, dependency breaking, testing legacy code; misses processes, org aspects, tools, reverse engineering.

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Maintenance Fundamentals | ⚠️ | Overview references Lehman's Laws/six categories; no dedicated file; Feathers covers 4 change types (not the 6 SWEBOK categories) |
| Key Issues | ⚠️ | Limited understanding is core theme; impact analysis via effect sketches; staffing/outsourcing/technical debt measurement/SLA-SLO all missing |
| Maintenance Processes | ❌ | No coverage of ISO/IEC/IEEE 14764 processes, four-level planning, MR/PR workflows, help-desk operations |
| Maintenance Techniques | ✅ | Program comprehension extensive; 24-technique dependency-breaking catalog; but reverse engineering and software visualization NOT covered |
| Maintenance Tools | ❌ | No dedicated coverage of static/dynamic analyzers, program slicers, cross-referencers, reverse engineering tools, maturity models |

**Top gaps:** ISO/IEC/IEEE 14764 processes, Lehman's Laws (dedicated file), six maintenance categories (dedicated file mapping to SWEBOK), staffing/organizational decisions, outsourcing/offshoring, technical debt measurement, reverse engineering, software visualization, maintenance tool ecosystem, maintenance maturity models.

### Chapter 08 — Software Configuration Management (~55% coverage)

**Source-book bias:** Berczuk & Appleton's *SCM Patterns* + practical Git — strong on patterns, branching, release management; misses formal governance (audits, status accounting, CCB).

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Management of SCM Process | ⚠️ | Role of SCM, balancing stability/progress covered; no SCMP, vendor/subcontractor control, interface control |
| Configuration Identification | ✅ | CIs, codelines, versions, labels, branches, workspace well covered |
| Change Control | ⚠️ | Codeline policy covers some; no CCB, no formal CR workflows, no deviations/waivers |
| Status Accounting (SCSA) | ❌ | No coverage |
| Configuration Auditing | ❌ | No FCA, PCA, or in-process audits |
| Release Management & Delivery | ✅ | Release Lines, Release-Prep, Task Branch, Daily Build well covered; SBOM and VDD missing |
| SCM Tools | ✅ | Git extensively covered (3 files); CMDB, integrated workbenches, SBOM tools, cryptographic hashing not covered |

**Top gaps:** SCM Plan (SCMP), vendor/subcontractor control, interface control, CCB, CR workflows, deviations vs. waivers, SCSA, FCA, PCA, SBOM, VDD, CMDB, cryptographic hashing for integrity.

### Chapter 09 — Software Engineering Management

**Source-book bias:** Peopleware (DeMarco & Lister) — excellent on human factors, team dynamics, office environment, organizational culture; but these are NOT the core SWEBOK management topics.

#### Initial Coverage (pre-fill): ~20%

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Initiation and Scope Definition | ❌ | No coverage |
| Software Project Planning | ❌ | Overview mentions SDLC/WBS/estimation; no dedicated files |
| Software Project Enactment | ❌ | Overview references Dev/Sec/Ops, acquisition; no dedicated files |
| Review and Evaluation | ⚠️ | Team performance via teamicide/competition; no earned value, no variance analysis, no stakeholder satisfaction |
| Closure | ❌ | Organizational learning touched; no project closure processes |
| Software Engineering Measurement | ❌ | Overview mentions ISO 15939/GQM/RACI; no dedicated files |
| Management Tools | ❌ | No coverage |

#### Gap-Fill Results (2026-07-21): Coverage improved to ~55-60%

Three notes created to address the largest gaps:

| New File | Size | SWEBOK Sections Covered | Key Topics |
|---|---|---|---|
| `06_Project_Initiation_and_Scope.md` | 15.9 KB | KA 9.1 | Project charter, context diagrams, MBSE, feasibility analysis (technical/economic/operational/schedule), requirements determination & negotiation, MoSCoW, scope baseline, scope change control, stakeholder power/interest grid |
| `07_Estimation_and_Planning.md` | 21.5 KB | KA 9.2 | SDLC model selection for planning, deliverables determination, Cone of Uncertainty, COCOMO II (3 stages, scale factors, cost drivers), Function Point Analysis, story points, Planning Poker, Wide Band Delphi, analogy estimation, resource allocation, WBS, scheduling (CPM/PERT/Gantt with cross-links to engineering-foundation-note) |
| `08_Risk_Management_and_Control.md` | 26.6 KB | KA 9.3-9.5 | Risk identification (Boehm's top 10), risk register, probability-impact matrix, risk response strategies, risk monitoring/burndown, software acquisition (build/buy/COTS/SaaS/open source), Earned Value Management (PV/EV/AC, CPI/SPI, EAC with worked example), variance analysis, status reporting, review types, project closure, archiving, retrospectives, lessons learned |

**Remaining gaps after fill:** ISO/IEC/IEEE 15939 measurement process, GQM (Goal-Question-Metric), RACI matrix, management tools, measurement databases. These could be addressed in a future `09_Measurement_and_Process_Improvement.md`.

**Cross-vault content reused:** The `07_Estimation_and_Planning.md` note cross-links to `[[11_Project_Planning_and_Management]]` in `engineering-foundation-note/02 SWE Process/` for detailed WBS, CPM, PERT, and Gantt chart coverage — avoiding content duplication.

### Chapter 10 — Software Engineering Process (~30% coverage)

**Source-book bias:** Multiple methodology sources (Clean Agile, Lean Software Development, methodology overviews) — good on life cycle models; missing entire process infrastructure/assessment side.

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Process Fundamentals | ❌ | No process definition, no four process categories |
| Life Cycle Categories & Terminology | ❌ | Four process categories not covered |
| Rationale for Life Cycles | ❌ | Not covered |
| Process Models vs. Life Cycle Models | ❌ | Distinction not covered |
| Development Life Cycle Paradigms | ✅ | Predictive/iterative/incremental/evolutionary covered via methodology comparisons |
| Specific Life Cycle Models | ⚠️ | Waterfall ✅, V-Model ✅, Agile ✅; Spiral ❌, RUP/UP ❌, rapid prototyping ❌ |
| Management of Life Cycle Processes | ❌ | Six generic stages and three management levels not covered |
| Software Engineering Process Management | ❌ | Three-level process management not covered |
| Life Cycle Adaptation & Practical Considerations | ⚠️ | Methodology selection touched; no formal tailoring process |
| Process Infrastructure, Tools, and Methods | ❌ | No BPMN, IDEF0, Petri nets, UML activity diagrams |
| Process Monitoring & Product Relationship | ❌ | Not covered |
| Process Assessment and Improvement | ❌ | Kaizen in Lean note; no PDCA, no CMMI, no SPICE/ISO 33000 |

**Top gaps:** Process fundamentals, four process categories, process model vs. SLCM, spiral model, RUP/UP/OpenUP, rapid prototyping, six generic life cycle stages, three management levels, process tailoring, process definition notations (BPMN/IDEF0/Petri nets), PDCA, CMMI, SPICE/ISO 33000, GQM for process improvement, process/product monitoring. The overview's own "What's Missing" section self-identifies the major gaps.

## Cross-Chapter Summary

| Chapter | Initial Coverage | Post-Fill | Key Strengths | Remaining Gaps |
|---|---|---|---|---|
| 06 — Operations | ~65% | ~65% | DevOps Handbook, CI/CD, Docker, DevSecOps | Capacity mgmt, DR, service desks, ISO 29110 |
| 07 — Maintenance | ~40% | ~40% | Feathers legacy code, dependency-breaking catalog | ISO 14764, staffing, reverse engineering, tools |
| 08 — SCM | ~55% | ~55% | SCM patterns, practical Git, release mgmt | SCSA, FCA/PCA, CCB, SBOM, CMDB |
| 09 — Management | ~20% | **~55-60%** | Peopleware + formal PM (estimation, risk, EVM, closure) | ISO 15939, GQM, RACI, mgmt tools |
| 10 — Process | ~30% | ~30% | Methodology models (Waterfall/V-Model/Agile/Lean) | Process fundamentals, CMMI, SPICE, BPMN, spiral/RUP |

## Top Priority Gaps (cross-chapter, ranked by gap severity)

1. **Ch.09 — Entire formal project management KA set** — **[PARTIALLY FILLED 2026-07-21]**. Three notes created (06-08), covering KA 9.1-9.5 core topics. Remaining: ISO/IEC/IEEE 15939, GQM, RACI, management tools.
2. **Ch.10 — Process assessment & improvement** (PDCA, CMMI, SPICE/ISO 33000). Entire process infrastructure side missing.
3. **Ch.07 — ISO/IEC/IEEE 14764 maintenance processes** + maintenance tools ecosystem. Two full KAs missing.
4. **Ch.08 — SCM governance** (SCSA, FCA/PCA, CCB/CR workflows, SBOM). Formal/governance side of SCM absent.
5. **Ch.06 — Traditional operations planning** (capacity, DR/backup/failover, service reporting, service desks). DevOps content strong; ops governance thin.

## Key Observations

1. **Source-book bias is the dominant coverage pattern.** Each vault chapter leans on one source book that covers SOME SWEBOK topics deeply but leaves others entirely untouched. The gap is always "what the source book doesn't cover."

2. **Chapter 09 had the largest gap of any chapter analyzed (ch06-15 range).** The vault was entirely Peopleware (human factors/culture) and missed all formal project management. The gap-fill session addressed this by creating 3 notes with ~64 KB of formal PM content.

3. **Governance/formal-process topics are systematically missing across all chapters.** Ch.06 misses service reporting/desks; Ch.07 misses ISO 14764; Ch.08 misses SCSA/FCA/PCA/CCB; Ch.09 misses ISO 15939; Ch.10 misses CMMI/SPICE. The vault favors practitioner/craft books over standards/process-framework books.

4. **Subdirectories matter for coverage.** Ch.06's `Fundamental/` (CI/CD, Docker) and Ch.08's `Version Control/` (3 Git files) contributed materially to their chapters' coverage scores. Always check subdirectories during inventory.

5. **Overviews with "What's Missing" sections are reliable but should be verified.** Ch.10's overview correctly self-identified its gaps; the independent analysis confirmed them.

6. **Cross-vault content avoids duplication.** When filling gaps, check adjacent vaults (e.g., `engineering-foundation-note`) for existing coverage. The estimation note cross-links to the engineering-foundation WBS/CPM/PERT note rather than duplicating content.

7. **Gap-fill notes should be substantially larger than overview files.** The three new notes range from 15.9 to 26.6 KB (383-581 lines), reflecting the depth needed for formal PM topics. Overview files at ~8 KB cannot provide this depth.

## Comparison to Ch.11-15 Session

The ch06-10 range has notably lower average coverage (~42%) than ch11-15 (~69%). The weakest chapter in ch11-15 was Ch.11 at ~55%; the weakest in ch06-10 was Ch.09 at ~20%. This suggests the earlier SWEBOK chapters (operations, maintenance, management, process) have received less vault-building attention than the later chapters (quality, security, professional practice, economics).
