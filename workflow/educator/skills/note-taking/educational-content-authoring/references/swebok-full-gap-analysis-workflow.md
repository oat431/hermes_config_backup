# Full SWEBOK Gap Analysis + Gap Filling Workflow

> Session: 2026-07-21 | Target: software-engineering-note vault (15 KAs)

## Workflow Overview

Two-phase approach: analyze first, then fill.

### Phase 1: Gap Analysis (parallel)

1. **Dispatch 3 subagents** (5 chapters each: 01-05, 06-10, 11-15)
   - Each reads SWEBOK reference .md + vault overview + 2-3 representative notes
   - Returns: per-chapter coverage table (✅/⚠️/❌), specific gaps, coverage % estimate
   - Duration: ~4-5 minutes for all 3

2. **Compile results** into summary table:
   ```
   | # | Chapter | Coverage | Status |
   | 01 | Requirements | ~80% | ⚠️ Partial gaps |
   | 09 | SE Management | ~20% | 🔴 Major gaps |
   ```

3. **Update main index file** (e.g., `Software Engineering Note Content.md`):
   - Fix stale statuses (e.g., "🔴 Missing notes" → actual coverage %)
   - Add mermaid quadrant chart (coverage vs priority)
   - Add priority action list with 🔴/🟡/🟢 rankings

4. **Append Coverage Map to each overview file**:
   - Anchor on last unique line of each file (via `tail -5`)
   - Use `execute_code` with `patch` to batch-update all 15 files
   - Each gets: SWEBOK topic table + gaps table with priorities

### Phase 2: Gap Filling (multi-wave parallel)

1. **Check cross-vault sources** before creating new content
   - `engineering-foundation-note/02 SWE Process/` has PM, evaluation, measurement content
   - `computing-foundation-note/` has algorithms, OS, networks, HCI content
   - Wikilink to existing content instead of duplicating

2. **Sort gaps by priority** — 🔴 Critical first, then 🟡 Medium, then 🟢 Low

3. **Dispatch waves of 3 subagents** — each wave handles 3 KAs:
   - Each subagent creates 2-3 files covering highest-priority gaps
   - Pass: file paths, SWEBOK topic list, vault conventions, cross-vault refs
   - Each file: 15-25KB, YAML frontmatter, tables, mermaid, wikilinks

4. **Update overview files between waves** — don't wait for all waves:
   - Change ❌ → ⚠️/✅ for filled gaps
   - Update coverage percentages
   - Add wikilinks to new files
   - Update main index

## Coverage Classification

| Status | Criteria |
|--------|----------|
| ✅ Well Covered | Dedicated file(s) with substantive content (15-45KB), multiple concepts |
| ⚠️ Partially Covered | Some content exists but missing depth or subtopics; or thin files (4-8KB) |
| ❌ Missing | No file covering this topic |

## Priority Ranking

| Priority | Coverage | Action |
|----------|----------|--------|
| 🔴 Critical | <30% | Fill immediately — KA is essentially empty |
| 🟡 Medium | 30-65% | Fill next round — significant gaps exist |
| 🟢 Low | 65-85% | Fill when convenient — minor gaps |

## Source-Book Bias Pattern

Each vault chapter typically leans on one source book. This creates predictable blind spots:

| KA | Source Book | Blind Spots |
|----|-----------|-------------|
| 01 Requirements | Wiegers | Formal methods (Z/VDM), ATDD/BDD as spec |
| 02 Architecture | Bass (SAiP) | ADLs, architecture frameworks |
| 03 Design | SWEBOK ref | Depth crisis — files are 4-6KB (thin) |
| 04 Construction | McConnell (CC) | Modern tech: AI/LLM, cloud IDEs, low-code |
| 05 Testing | Jorgensen | Testing tools, domain-specific testing |
| 06 Operations | DevOps Handbook | Traditional ops: capacity, DR, service desks |
| 07 Maintenance | Feathers | ISO 14764, Lehman's Laws, processes |
| 08 SCM | Berczuk | Formal governance: SCSA, FCA/PCA, CCB |
| 09 Management | Peopleware | ALL formal PM (initiation, estimation, WBS, risk) |
| 10 Process | Methodology refs | Process fundamentals, CMMI, SPICE, PDCA |
| 11 Models/Methods | Gomaa (COMET) | Formal methods, prototyping, design-by-contract |
| 12 Quality | Galin | Dependability, safety-critical |
| 13 Security | Anderson | Domain-specific (cloud/IoT/ML), CVE/CWE |
| 14 Professional | Clean Coder etc | Professional societies, employment contracts |
| 15 Economics | McConnell (Est) | SIPAC/intangible assets |

## Key Metrics (Sessions 2026-07-21)

- **Analysis phase:** 3 parallel subagents (5 chapters each), ~4-5 min
- **Gap filling wave 1 (Critical):** 3 subagents (Ch07, Ch09, Ch10), 9 files, ~6 min
- **Gap filling wave 2 (Medium):** 3 subagents (Ch11, Ch04, Ch06), 8 files, ~4 min
- **Gap filling wave 3 (Medium):** 3 subagents (Ch08, Ch05, Ch13), 9 files, ~8 min
- **Gap filling wave 4 (Minor):** 3 subagents (Ch01, Ch02, Ch09, Ch12, Ch14, Ch15), 10 files, ~9 min
- **Gap filling wave 5 (Push to 90%):** 2 subagents (Ch03, Ch04, Ch05, Ch07, Ch08, Ch11), 8 files, ~4 min
- **Total files created:** 50 new notes across all 15 KAs
- **Total overview files updated:** 15 Coverage Maps + 1 main index (updated after each wave)
- **Overall coverage improvement:** ~58% → ~90%

### Wave 5 (Push to 90%) Pattern

After waves 1-4 fill critical/medium/minor gaps, a final wave pushes remaining KAs from 75-85% to 88-95%. This wave targets the specific subtopics that are still thin:

```
Wave 5: Ch03 Design (2 files: design thinking, design issues)
        Ch04 Construction (2 files: middleware, embedded)
        Ch05 Testing (1 file: test process/measures)
        Ch07 Maintenance (1 file: staffing/org models)
        Ch08 SCM (1 file: vendor/interface control)
        Ch11 Models & Methods (1 file: syntax/semantics/model analysis)
```

Wave 5 is triggered when the user says "let cover them, why not" or "nice to fill the gap, let do it" after seeing remaining Minor gaps. Don't ask for confirmation — the user's intent is clear.

### Main Index 4-Section Patching

The main index file (e.g., `Software Engineering Note Content.md`) has 4 distinct sections that ALL need updating after gap filling:

1. **Main KA table** (top) — coverage % and status column per KA
2. **Mermaid quadrant chart** — coordinate values per KA
3. **Priority action list** — rows with coverage %, gap descriptions
4. **Overall summary paragraph** (bottom) — strongest/weakest KAs, total coverage %

Common mistake: updating the priority list and mermaid chart but forgetting the main table. The user will catch stale percentages. Always patch all 4 sections.

### Wave 4 (Minor Gaps) Pattern

After filling critical and medium gaps, a final wave handles the 🟢 Low priority gaps across remaining KAs. This wave typically bundles multiple KAs per subagent (2-4 files each) since the gaps are smaller. Example:

```
Wave 4: Ch01 (2 files), Ch02 (1 file), Ch09 (1 file), Ch12 (2 files), Ch14 (3 files), Ch15 (1 file)
```

The user may want to fill even minor gaps ("i love the to fill everything up"). Dispatch wave 4 without asking for confirmation if the user's enthusiasm is clear.

## Multi-Wave Batching Pattern

When filling gaps for 7+ KAs, use multiple waves of 3 subagents each:

```
Wave 1 (Critical):  Ch09 SE Mgmt, Ch10 SE Process, Ch07 Maintenance     → 9 files
Wave 2 (Medium):    Ch11 Models, Ch04 Construction, Ch06 Operations      → 8 files
Wave 3 (Medium):    Ch08 SCM, Ch05 Testing, Ch13 Security                → 9 files
Wave 4 (Remaining): Ch03 Design                                          → 3 files
```

Between waves: update overview files + main index for completed KAs. This gives the user incremental progress visibility.

## Subagent Prompt Template

```
CREATE THESE N FILES:

1. **filename.md**
Cover: [SWEBOK topics]. SWEBOK KA X.Y.
Source: SWEBOK vX ChXX.

FORMAT:
```yaml
---
tags: [software-engineering, swebok, kaXX, topic-specific-tag]
source: "SWEBOK vX Chapter XX"
---
```

Body 15-25KB. Tables, mermaid diagrams, wikilinks to existing notes.
Colons not em-dashes. English only.
For each file use write_file. Confirm success.
```
