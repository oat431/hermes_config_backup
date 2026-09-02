# SWEBOK v4 Chapters 11-15 Gap Analysis (Session Reference)

> **Session:** 2026-07-21
> **Task:** Multi-chapter SWEBOK gap analysis for chapters 11-15
> **Vault:** `F:\obsidian_note\swe-knowledge\software-engineering-note\`
> **Reference:** `F:\obsidian_note\swe-knowledge\body-of-knowledge\SWEBOK\`

## Multi-Chapter Batch Workflow Pattern

This session established the pattern for analyzing 5 BOK chapters in one pass:

1. **List both directories first** (`ls` on SWEBOK ref folder + vault note folder) to confirm file inventory
2. **Batch-read all 10 files** (5 SWEBOK reference + 5 vault overview) in parallel `read_file` calls — single assistant turn
3. **Per-chapter: batch-read 2-3 representative note files** with `limit=60` to verify depth without blowing context
4. **Use `todo` tool** to track per-chapter progress (one item per chapter + final report item)
5. **Compile report** with per-chapter sections + summary table + top priority gaps + key observations

Key efficiency: 5 chapters analyzed in ~8 tool calls total (vs ~25+ if done serially with full file reads).

## Per-Chapter Coverage Findings

### Chapter 11 — Software Engineering Models and Methods (~55% coverage)

**Source-book bias:** Gomaa's *Software Modeling and Design* (COMET method) — heavily OO/UML focused.

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Modeling Principles | ✅ | COMET, UML, 4+1 view model |
| Properties/Expression of Models | ⚠️ | Overview only |
| Syntax/Semantics/Pragmatics | ⚠️ | Overview only |
| Preconditions/Postconditions/Invariants | ❌ | No dedicated file |
| Structural Modeling | ✅ | Class/component/deployment diagrams |
| Behavioral Modeling | ✅ | State machines, interaction diagrams |
| Analysis of Models | ⚠️ | Tangential coverage |
| Heuristic Methods | ✅ | OO design (UP/RUP/AOP/MDD in overview only) |
| Formal Methods | ❌ | Only overview mention; no Alloy/model checking |
| Prototyping Methods | ❌ | Only overview mention |
| Agile Methods | ⚠️ | Listed but shallow (likely cross-covered by Ch.10) |

### Chapter 12 — Software Quality (~75% coverage)

**Source-book bias:** Galin's *Software Quality Assurance* — comprehensive on SQA fundamentals, reviews, standards.

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Quality Fundamentals | ✅ | Error/defect/failure chain, McCall, ISO 9126 |
| Quality Management Process | ✅ | QMS, planning, CAPA |
| SQA Process (SQAP, V&V) | ✅ | Reviews, audits well covered; V&V techniques lighter |
| Quality Tools | ⚠️ | Standards covered; CI/CD/static analysis tools light |
| Metrics & Cost of Quality | ✅ | Process/product metrics, function points, CoSQ |
| Dependability / Safety-Critical | ⚠️ | Overview mentions FMEA/FTA; no dedicated note |

### Chapter 13 — Software Security (~60% coverage)

**Source-book bias:** Anderson's *Security Engineering* — strong on fundamentals, protocols, access control; weak on modern domain-specific security.

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Security Fundamentals | ✅ | CIA triad, policy/mechanism/assurance/incentive |
| Security Management & Organization | ⚠️ | SSE-CMM, ISO 27001 in overview only |
| Security Engineering & Processes | ✅ | Secure SDLC, DevSecOps, Common Criteria |
| Security Design | ✅ | Crypto, TLS, ACLs, MLS |
| Secure Construction (CERT) | ⚠️ | Mentioned but not dedicated |
| Security Testing | ⚠️ | Network attacks covered; SAST/DAST/fuzzing light |
| Vulnerability Management | ❌ | CVE/CWE/CAPEC/CVSS only in overview |
| Software Security Tools | ⚠️ | Source/binary analyzers mentioned |
| Domain-Specific (Cloud/IoT/ML) | ❌ | Only overview mentions |

### Chapter 14 — Software Engineering Professional Practice (~80% coverage)

**Source:** SWEBOK v4 Chapter 14 directly (no single source book; supplemented by Clean Coder/Craftsmanship/Agile, Pragmatic Programmer folders).

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Code of Ethics | ✅ | ACM/IEEE 8 principles + 3 case studies |
| Accreditation/Certification/Licensing | ✅ | Washington Accord, CSDP/CISSP/ISTQB/PMP |
| Professional Societies | ⚠️ | Mentioned but not deep |
| SE Standards | ⚠️ | Referenced but not enumerated |
| Economic Impact | ⚠️ | Overview only |
| Employment Contracts | ⚠️ | NDAs/IP lightly |
| Legal Issues (IP, privacy) | ✅ | Patents, copyrights, trade secrets, GDPR/CCPA |
| Documentation | ✅ | Document types covered |
| Trade-off Analysis | ⚠️ | Cross-covered by Ch.15 |
| Team Dynamics | ✅ | Tuckman, psychological safety, Project Aristotle |
| Individual Cognition | ✅ | Miller's Law, cognitive biases table |
| Problem Complexity | ✅ | Decomposition, pair programming |
| Stakeholder Interaction | ✅ | Covered |
| Uncertainty & Ambiguity | ✅ | Covered |
| Equity/Diversity/Inclusivity | ⚠️ | Mentioned but light |
| Reading/Writing/Presentation | ✅ | 3-pass method, document types, writing principles |

### Chapter 15 — Software Engineering Economics (~75% coverage)

**Source-book bias:** McConnell's *Software Estimation* — excellent on estimation (3 dedicated files, 70KB total); thinner on pure economics.

| SWEBOK Topic | Status | Notes |
|---|---|---|
| Economics Fundamentals | ✅ | Cash flow, time-value, PW/FW/IRR |
| Decision-Making Process | ✅ | 7-step, certainty/risk/uncertainty |
| For-Profit Decision-Making | ✅ | MARR, economic life, depreciation |
| Nonprofit Decision-Making | ✅ | Benefit-cost, cost-effectiveness |
| Present Economy | ✅ | Break-even analysis |
| Multiple-Attribute Decision-Making | ✅ | AHP, ATAM, additive weighting |
| Intangible Assets / SIPAC | ❌ | No coverage (7-step method, 11 asset taxonomy) |
| Estimation | ✅ | Excellent depth via McConnell (3 files) |
| Practical Considerations | ⚠️ | Multi-currency, systems thinking in overview |
| Related Concepts (TCO, SPLC) | ⚠️ | TCO mentioned; accounting/finance not deep |

## Top Priority Gaps (❌ Missing)

Ranked by impact on vault completeness:

1. **Ch.11 — Formal Methods** — specification languages, model checking, Alloy, program refinement. Largest gap in Ch.11.
2. **Ch.13 — Domain-Specific Security** — cloud, IoT, ML security (model poisoning, evasion attacks). Largest gap in Ch.13.
3. **Ch.15 — SIPAC / Intangible Assets** — 7-step characterization method, 11 Generic Intangible Assets taxonomy. Largest gap in Ch.15.
4. **Ch.11 — Prototyping Methods** — throwaway/evolutionary prototyping, executable specifications.
5. **Ch.13 — Vulnerability Management** — CVE/CWE/CAPEC/CVSS databases and scoring.
6. **Ch.11 — Preconditions/Postconditions/Invariants** — design-by-contract reasoning.

## Key Observations

1. **Source-book bias creates predictable blind spots.** Each vault chapter leans on one authoritative source, which aligns well with SOME SWEBOK topics but leaves others uncovered. Future note creation should target the gaps the source book doesn't cover.

2. **Cross-coverage is common.** Several ⚠️ topics (Agile in Ch.11, V&V in Ch.12, security testing in Ch.13, trade-off analysis in Ch.14) are likely partially covered in other chapters' notes. The vault's overview files' "Relationship to Other KAs" sections help identify these.

3. **Strongest coverage: Ch.14 (Professional Practice, ~80%)** — All three KAs have dedicated notes with good depth, case studies, and practical frameworks. No ❌ Missing items.

4. **Weakest coverage: Ch.11 (Models & Methods, ~55%)** — The vault is heavily biased toward Gomaa's COMET/OO approach, leaving formal methods, prototyping, and design-by-contract largely uncovered.

5. **Estimation is over-represented in Ch.15.** Three dedicated files (70KB) cover McConnell's estimation thoroughly, while SIPAC and intangible assets — a full SWEBOK KA — have zero coverage. Rebalancing needed.
