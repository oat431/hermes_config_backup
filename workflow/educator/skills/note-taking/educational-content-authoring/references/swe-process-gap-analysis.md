# SWE Process Gap Analysis Reference

## Session: 2026-07-21 — Small Project Checklist vs SWE Theory

### Context
User had a `Profile-Small-Startup-Checklist.md` (17 🔴 Must Have docs) and wanted to know if it was enough to build a small project (1–5 devs, Agile/Lean, weeks to months).

### Theory Source
`F:\obsidian_note\swe-knowledge\engineering-foundation-note\02 SWE Process\` — 16 files covering:
- 10_SE_Fundamentals_and_Process (lifecycle, process models)
- 12_Requirements_Engineering (SRS, elicitation, validation)
- 13_Software_Architecture (styles, views, quality attributes)
- 11_Project_Planning_and_Management (WBS, estimation, risk)
- 16_Testing_Strategies (unit, integration, system, acceptance)
- 17_Delivery_and_Maintenance (training, documentation, types of maintenance)

### Gaps Identified

| Gap | Theory Source | Risk | Resolution |
|-----|--------------|------|------------|
| No Architecture Overview (HLD) | Ch 13: SAD communicates system-level design decisions | 🟡 Medium | Added as 🔴 — use High-Level-Design.md template |
| No Definition of Done | Scrum Guide / Agile Practice Guide | 🟡 Low-Medium | Added as 🔴 — created new template |
| No formal SRS | Ch 12: SRS for technical audience | 🟡 Low | User Stories + Acceptance Criteria sufficient for small |
| No User Documentation | Ch 10: Training, audience-specific docs | 🟡 Low | Add before public launch |
| No Risk Management | Ch 3: Risk Register + Risk Exposure | 🟡 Low | Risk Register already 🟡 in checklist |

### Key Theory Quotes

- **Fred Brooks (1987):** "The hardest single part of building a software system is deciding precisely what to build."
- **Boehm & Papaccio (1988):** Requirements fix cost ratio: $1 → $5 → $10 → $20 → $200 (req → design → code → test → post-delivery)
- **Standish Group:** Incomplete requirements (13.1%) and lack of user involvement (12.4%) are top project failure causes
- **Lehman:** Maintenance consumes 60–80% of total software cost over lifetime

### Template Sync Pattern

Source: `F:\obsidian_note\swe-knowledge\document-template\`
Target: `F:\projects\project_spec\template\`

Target structure (numbered subdirectories):
```
01_requirement\   (011_ through 015_)
02_design\        (021_ through 029_)
03_construction\  (031_ through 036_)
04_testing\       (041_ through 045_)
05_devops\        (051_ through 054_)
06_security\      (061_ through 062_)
07_pm\            (071_ through 072_)
```

Final count: 19 🔴 + 14 🟡 = 33 total documents, 33 templates in target directory.

### Checklist Update Pattern

When adding items to a priority-based checklist:
1. Add the item to the correct section table
2. Update the summary table (recalculate per-category and total counts)
3. Update the quick-start checklist (renumber, maintain sequential order)
4. Verify: summary total = quick-start item count
