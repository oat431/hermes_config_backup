# Software Project Classification Frameworks

Research findings (2026-08): No single framework classifies software projects by required engineering practices across the spectrum from side projects to mission-critical. Multiple formal standards exist, each covering one dimension.

## Formal Criticality Classifications (prescribe practices per level)

### DO-178C (Avionics) — Development Assurance Levels
| Level | Failure Consequence | Rigor |
|-------|-------------------|-------|
| A | Catastrophic (may cause deaths) | Maximum — full MC/DC coverage, independent verification |
| B | Hazardous (large negative impact) | High |
| C | Major (significantly reduces safety margin) | Medium |
| D | Minor (slightly reduces safety margin) | Low |
| E | No effect | None required |

Key insight: "The software level establishes the rigor necessary to demonstrate compliance." Each level has a specific number of objectives, some requiring independence (different person writes vs. verifies).

### IEC 61508 (Generic Safety Systems) — Safety Integrity Levels (SIL)
- SIL 1–4, derived from risk assessment
- Prescribes: formal/semi-formal specification, modular testable design, documented code reviews, multi-layer testing, specific test coverage
- EN 50716 (railway) lists 32 documents required across the lifecycle

### ISO 26262 (Automotive) — ASIL A–D
- Derived from Hazard and Risk Assessment (HARA) at vehicle level
- Each ASIL mandates specific development and verification methods

### NASA Software Classification
- Class A (critical), B, C based on mission impact
- Different process requirements per class

## Maturity/Readiness Frameworks (about development stage, not project type)

### Technology Readiness Levels (TRL 1–9, NASA)
- TRL 1: Basic principles observed
- TRL 2: Potential application validated  
- TRL 3: Proof-of-concept demonstrated
- TRL 4: Component validated in lab
- TRL 5: Component validated in relevant environment
- TRL 6: System validated in relevant environment
- TRL 7: System demonstrated in operational environment
- TRL 8: System complete and qualified
- TRL 9: System proven in operational environment

Criticism: "concreteness and sophistication gradually diminished as usage spread outside space programs"

### CMMI (Process Maturity, Levels 1–5)
- Level 1: Initial (ad hoc, chaotic)
- Level 2: Managed (project-level planning, tracking)
- Level 3: Defined (organization-wide standards)
- Level 4: Quantitatively Managed (statistical process control)
- Level 5: Optimizing (continuous improvement)

## Practice Selection Decision Factors

From the research, teams implicitly combine multiple dimensions:

| Dimension | Framework | Example Levels |
|-----------|-----------|---------------|
| Failure consequence | DO-178C, IEC 61508 | Catastrophic → No effect |
| Technology maturity | TRL | Research → Production-proven |
| Organizational maturity | CMMI | Ad hoc → Optimizing |
| Team/scale | Agile scaling | Single team → Enterprise |
| Regulatory domain | Domain standards | Regulated → Unregulated |

## Proposed Practical Categories (not from any single source)

A synthesis that maps to how teams actually decide practices:

1. **Proof of concept / Spike** — TRL 1-3, throwaway, minimal process
2. **Prototype / MVP** — TRL 3-5, learning-focused, lightweight process
3. **Internal tool** — Low criticality, small team, pragmatic practices
4. **Small SaaS** — Production, paying users, standard engineering practices
5. **Medium SaaS** — Multiple teams, scaling concerns, formalized processes
6. **Large / Enterprise** — CMMI 3+ territory, governance, compliance
7. **Regulated / Mission-critical** — DO-178C / SIL territory, maximum rigor

These 7 categories are NOT from any existing framework — they're a practical synthesis of how engineering teams right-size their practices. No formal standard uses exactly these boundaries.
