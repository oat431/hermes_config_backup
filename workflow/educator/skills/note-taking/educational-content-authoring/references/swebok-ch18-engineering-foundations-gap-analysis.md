# SWEBOK v4 Ch18 — Engineering Foundations Gap Analysis

> **Session:** 2026-07-21
> **Vault:** `F:\obsidian_note\swe-knowledge\engineering-foundation-note`
> **Reference:** `F:\obsidian_note\swe-knowledge\body-of-knowledge\SWEBOK\18_Engineering_Foundations.md`

## Vault Structure

Two-part structure:
- `01 Physics and Math/` — 9 files (Moaveni textbook: dimensions, force, thermal, electrical, energy, materials, drawings, math/stats)
- `02 SWE Process/` — 16 files (Pfleeger textbook + SWEBOK supplementary: 10-25)

## Coverage Findings

| # | SWEBOK Topic | Status | Vault File |
|---|-------------|--------|-----------|
| 1 | The Engineering Process | ❌ → ✅ | `26_The_Engineering_Process.md` (17 KB) |
| 2 | Engineering Design | ❌ → ✅ | `27_Engineering_Design.md` (16 KB) |
| 3 | Abstraction and Encapsulation | ⚠️ → ✅ | `28_Abstraction_and_Encapsulation.md` (15 KB) |
| 4 | Empirical Methods | ✅ | `22_Empirical_Methods.md` |
| 5 | Statistical Analysis | ✅ | `24_Statistical_Inference.md` |
| 6 | Modeling, Simulation, Prototyping | ❌ → ✅ | `29_Modeling_Simulation_and_Prototyping.md` (18 KB) |
| 7 | Measurement | ✅ | `21_Measurement_Theory.md` |
| 8 | Standards | ✅ | `25_Engineering_Standards_and_Process.md` |
| 9 | Root Cause Analysis | ✅ | `20_Root_Cause_Analysis.md` |
| 10 | Industry 4.0 & CSE | ✅ | `23_Industry_4_and_Continuous_SE.md` |

**Coverage: 65% → 90%** after adding 4 files.

## Key Observations

1. **Pfleeger textbook covers topics 4-5, 7-10** via chapters 12-14 + supplementary files (20-25). The textbook naturally covers the "process" side of engineering foundations.

2. **Topics 1-3 and 6 were missing** — these are the "design thinking" side of engineering foundations (engineering process, design, abstraction, modeling). The Pfleeger textbook doesn't cover these as standalone topics.

3. **Cross-vault reference pattern:** `engineering-foundation-note/02 SWE Process/11_Project_Planning_and_Management.md` (22 KB) covers WBS, CPM, PERT — referenced from `software-engineering-note/09_Software_Engineering_Management/07_Estimation_and_Planning.md` via wikilink. Cross-vault references work within the same Obsidian vault.

4. **Overview update pattern for foundation vaults:** Unlike the software-engineering-note KA overviews (which have SWEBOK Coverage Maps), the engineering-foundation-note overview needed updates to: (a) file table, (b) mermaid diagram, (c) reading paths, (d) new SWEBOK Coverage Map section. The mermaid diagram update requires adding new nodes AND new edges — don't forget the edges.

## Overview Update Commands Used

```python
# 1. Add new files to table
patch(overview, last_table_row, last_table_row + new_rows)

# 2. Add new nodes to mermaid subgraph
patch(overview, "STAND[\"Engineering Standards\"]\n    end",
      "STAND[\"Engineering Standards\"]\n        EPROC[\"Engineering Process\"]\n        ...")

# 3. Add new edges to mermaid
patch(overview, "STAND --> PROC\n```",
      "STAND --> PROC\n    EPROC --> DES\n    ...")

# 4. Update reading path
patch(overview, old_path, new_path_including_new_files)

# 5. Add SWEBOK Coverage Map section
patch(overview, last_related_link, last_related_link + coverage_map_section)
```
