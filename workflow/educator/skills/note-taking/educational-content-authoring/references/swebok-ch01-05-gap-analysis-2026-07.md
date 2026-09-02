# SWEBOK v4 Gap Analysis — Chapters 01-05 (2026-07-21)

> Session reference for the gap analysis performed against the `software-engineering-note` vault on `F:\obsidian_note\swe-knowledge\`. Future sessions can use this to prioritize gap-filling work without re-running the analysis.

## Vault Locations

- **SWEBOK reference files:** `F:\obsidian_note\swe-knowledge\body-of-knowledge\SWEBOK\01_Software_Requirements.md` … `05_Software_Testing.md`
- **Vault note folders:** `F:\obsidian_note\swe-knowledge\software-engineering-note\01_Software_Requirements\` … `05_Software_Testing\`
- **Full report saved to:** `C:\Users\Admin\swebok_gap_analysis_ch01_05.md`

## Coverage Summary

| Chapter | KAs | ✅ Well | ⚠️ Partial | ❌ Missing | Est. Coverage |
|---|---|---|---|---|---|
| 01 — Software Requirements | 8 | 6 | 2 | 0 | ~80% |
| 02 — Software Architecture | 7 | 5 | 2 | 0 | ~85% |
| 03 — Software Design | 6 | 1 | 5 | 0 | ~55% |
| 04 — Software Construction | 5 | 2 | 3 | 0 | ~65% |
| 05 — Software Testing | 8 | 3 | 4 | 1 | ~60% |

## Per-Chapter Gap Detail

### Ch01 Software Requirements (~80%) — Source: Wiegers & Beatty, 11 files
**Well covered:** Fundamentals, Elicitation, Specification, Validation, Management, Tools
**Gaps:**
- Formal methods specification (Z, VDM, theorem provers, model checkers) — only brief mentions in `05_Documenting`, `06_Modeling`; no dedicated treatment
- ATDD/BDD as specification (Given/When/Then) — only in `07_Quality_and_Prototyping`; not elevated as core specification technique
- Perfect Technology Filter & QoS economics (perfection/fail point) — only in `07`; not standalone
- Requirements Analysis as distinct KA — no dedicated file; content scattered across fundamentals/prioritization

### Ch02 Software Architecture (~85%) — Source: SAiP (Bass/Clements/Kazman), 11 files + Microservice subfolder
**Well covered:** Fundamentals, Views/Viewpoints, Patterns, Design Process, Evaluation
**Gaps:**
- ADLs (Architecture Description Languages) — mentioned in 5 files but no dedicated file; ArchiMate, AUTOSAR, UAF, RM-ODP likely brief
- Architecture Frameworks — only in overview
- Architecture as Significant Decisions (standalone) — technical debt and rationale scattered in `07`, `09`; not a dedicated KA-level treatment

### Ch03 Software Design (~55%) — Source: SWEBOK v4 + subfolders (Design Pattern, Clean Architecture, HCI)
**Weakest chapter — depth crisis.** Main files are 4-6 KB each (total ~33 KB) vs 20-45 KB per file in Ch01/Ch02.
**Well covered:** Design Strategies and Methods (`05`, 5.8 KB)
**Gaps (all due to thin files, not missing KAs):**
- Design Fundamentals (`01`, 6 KB) — needs 3-5× expansion
- Design Processes (`02`, 4.6 KB) — thin
- Design Qualities (`03`, 5.5 KB) — 8 quality topics present but brief
- Recording Software Designs (`04`, 5.5 KB) — MBD, DSLs, design rationale thin
- Design Quality Analysis (`06`, 6 KB) — reviews, metrics, static analysis thin
- Design Rationale — only in overview; no dedicated section
- MBD (Model-Based Design) — mentioned but brief
- DSLs — only in `05` and overview
- Variability & Feature Models — mentioned but brief
- Aspect-Oriented Design — only in `05`; brief
- Note: Subfolders (Design Pattern/5 subdirs, Clean Architecture/9 subdirs, HCI/8 files) partially compensate but follow their own book structures, not SWEBOK KA organization

### Ch04 Software Construction (~65%) — Source: Code Complete (McConnell), 11 files + API subfolder
**Well covered:** Construction Fundamentals, Practical Considerations (coding practices)
**Gaps:**
- AI-Assisted Programming (LLMs) — only in overview; Code Complete (2004) predates
- Cloud-Based IDEs & Low-Code/Zero-Code — only in overview
- Dependency Management / Supply Chain — brief in `09` and overview; no dedicated treatment
- Executable Models (MDA, PIM/PSM) — not found
- Middleware / ESB — not found
- Heterogeneous Systems (Hardware/Software Co-design) — not found
- Continuous Integration as construction concern — brief in `09`/overview only

### Ch05 Software Testing (~60%) — Source: Jorgensen, 8 files + QA subfolder
**Well covered:** Testing Fundamentals, Test Levels, Test Techniques
**Gaps:**
- Testing Tools (catalog) — ENTIRE KA MISSING; no dedicated file; SWEBOK catalogs 15+ tool categories
- Test Process (3-layer model: organizational → management → dynamic) — only 1 grep hit; not deeply covered
- Test-Related Measures (consolidated) — scattered across 7 files; no consolidated treatment of reliability growth models, fault density, KPIs, mutation score
- AI/ML/DL System Testing — metamorphic testing only in overview; no substantive coverage
- Domain-Specific Testing (automotive, IoT, healthcare, mobile, avionics, finance, embedded) — not found
- Blockchain & Cloud Testing — not found
- Testing Standards (ISO 29119, IEEE 1012, TMMi, CMMI, SPICE, ODC) — only in overview

## Top Priority Gaps (for gap-filling work)

1. **Ch03 depth crisis** — All 6 main files need 3-5× expansion to match Ch01/Ch02 depth
2. **Ch05 Testing Tools** — Entire KA missing (no dedicated file)
3. **Ch04 Modern Construction Technologies** — AI/LLM, cloud IDEs, low-code, MDA, middleware all missing (Code Complete predates)
4. **Ch05 Test Process & Measures** — 3-layer process model and consolidated measures not covered
5. **Ch01 Formal Methods** — Z, VDM, theorem provers, model checking not substantively covered
6. **Ch05 Domain-Specific & Emerging Tech Testing** — AI/ML, blockchain, cloud, automotive, IoT, healthcare all missing
7. **Ch02 ADLs & Frameworks** — No dedicated file; AUTOSAR, UAF, RM-ODP only briefly mentioned

## Method Notes

- `search_files` tool failed on F:\ drive (IO error); used `grep -l -i -E` via `terminal` with MSYS paths instead
- Depth-sampled by reading first 80 lines (`read_file(limit=80)`) + using `ls -la` file sizes as depth proxy
- Batched 5 grep checks per `terminal` call with `echo` separators
