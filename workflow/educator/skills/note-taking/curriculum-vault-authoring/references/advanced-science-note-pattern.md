# Advanced Science Note Creation Pattern (ม.4-ม.6)

Reference for creating advanced science content notes for Thai วิทย์-คณิต high school (ม.4-ม.6). Proven on 23 Physics notes (ว301-ว303) + 20 Chemistry notes (ว311-ว313) + 20 Biology notes (ว321-ว323) + 10 Earth Science notes (ว341 elective) + 12 Computer Science notes (ว331-ว333) created 2026-07-30. Total: 85 advanced science notes. Full Science vault: 107 notes (22 Fundamental + 85 Advance).

## Folder Structure

**Current (subject-grouped, user preference 2026-07-30):**
```
Science/
├── Fundamental/                       (22 notes, ป.1-ม.3, course codes ว111-ว213)
│   ├── 01_Scientific_Method.md
│   └── ... 22_Technology_and_Engineering.md
└── Advance/                          (subject-grouped subfolders)
    ├── physic/                       (23 notes, ม.4-ม.6, ว301-ว303)
    │   ├── 01_Measurement_and_Scientific_Method.md
    │   └── ... 23_Astrophysics_and_Cosmology.md
    ├── Chemistry/                    (20 notes, ม.4-ม.6, ว311-ว313)
    │   ├── 01_Atomic_Structure.md
    │   └── ... 20_Industrial_and_Applied_Chemistry.md
    ├── Biology/                      (20 notes, ม.4-ม.6, ว321-ว323, created 2026-07-30)
    ├── Earth_Science/                (10 notes, ว341 elective, created 2026-07-30)
    └── Computer_Science/             (12 notes, ว331-ว333, created 2026-07-30)
```

**Note on folder naming:** the user typed `physic/` (single 's') for Physics. Don't auto-correct; respect the user's exact folder name. Future subject folders can use English names: `Chemistry`, `Biology`, `Earth Science`, `Computer Science` (multi-word subject names keep the space — Obsidian handles them fine).

**Fundamental stays flat** (integrated ป.1-ม.3 content covering all subjects in one strand). Only the Advance folder is subject-grouped, because the ม.4-ม.6 curriculum splits into Physics/Chem/Bio/etc. The user explicitly said "the fundamental can be there, in case student want to read up to ม3, so not restructuring" — don't reorganize fundamental.

**Mirrors the Mathematics structure:** `Mathematics/Fundamental/` (20 files) + `Mathematics/Advance/` (23 files) for the single-subject Math case. For multi-subject Science, Advance gets one extra level of nesting.

## 5-Section Note Template

Every advanced science note follows this exact structure:

```markdown
---
tags:
  - [subject]
  - advance
  - [topic-tag]
  - ipst
source: "IPST (สสวท.) [Subject] Curriculum B.E. 2551 (2008, revised 2560/2017)"
created: YYYY-MM-DD
course_codes: ["ว301"]  # or ว302, ว303, ว311, ว321, ว331
---

# [Topic Name] — [Thai Topic Name]

> *"[relevant quote]"* — [Attribution]

[1-2 paragraph overview]

---

## 1 | Course Coverage

### ม.4 (ว301)  # or ม.5/ม.6 with appropriate code

| Semester | Scope | Key Skills |
|---|---|---|
| **Semester 1** | [scope] | [skills] |
| **Semester 2** | [scope] | [skills] |

---

## 2 | Key Terminology

| Thai | English | Symbol/Notes |
|---|---|---|
| [Thai term] | [English] | [symbol] |

---

## 3 | Key Concepts

### 3.1 [Subtopic]
[Explanation with $$...$$ for display math, $...$ for inline]

---

## 4 | Common Problem Types

### Type 1: [Name]
> [Problem statement]

**Solution:** [Step-by-step with formulas]

---

## 5 | Cross-Links

- [[Fundamental/13_Forces_and_Motion]] — [connection]
- [[02_Kinematics]] — [next topic]
- [[01_Advance Mathematics (Sci-Math) - Overview|Mathematics]] — [math connection]
```

## IPST Physics Topic Distribution (Verified)

Verified via SearXNG search → smartmathpro.com article (2025-02-13). Source: IPST textbooks vol 1-6, หลักสูตรแกนกลาง 2560.

### ม.4 (ว301) — Classical Mechanics & Thermodynamics

| Semester | Topics (IPST chapter names) |
|---|---|
| **Semester 1** | ธรรมชาติและพัฒนาการทางฟิสิกส์ (Nature of Physics), การเคลื่อนที่แนวตรง (Linear Motion), แรงและกฎการเคลื่อนที่ (Forces & Laws of Motion) |
| **Semester 2** | สมดุลกล (Mechanical Equilibrium), งานและพลังงาน (Work & Energy), โมเมนตัมและการชน (Momentum & Collisions), การเคลื่อนที่แนวโค้ง (Curvilinear Motion) |

### ม.5 (ว302) — Waves, Sound, Electricity & Magnetism, Optics

| Semester | Topics |
|---|---|
| **Semester 1** | การเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย (SHM), คลื่น (Waves), แสงเชิงคลื่น (Wave Optics), แสงเชิงรังสี (Ray Optics) |
| **Semester 2** | เสียง (Sound), ไฟฟ้าสถิต (Electrostatics), ไฟฟ้ากระแส (Electric Current) |

### ม.6 (ว303) — Magnetism, Heat, Fluids, EM Waves, Modern Physics

| Semester | Topics |
|---|---|
| **Semester 1** | แม่เหล็กและไฟฟ้า (Magnetism & Electricity), ความร้อนและแก๊ส (Heat & Gases), ของแข็งและของไหล (Solids & Fluids) |
| **Semester 2** | คลื่นแม่เหล็กไฟฟ้า (EM Waves), ฟิสิกส์อะตอม (Atomic Physics), ฟิสิกส์นิวเคลียร์และฟิสิกส์อนุภาค (Nuclear & Particle Physics) |

### Notes on Coverage

- Our 23-topic BOK is a **superset** of the standard IPST ~20-chapter curriculum
- We include Special Relativity (18) and Astrophysics (23) as extension topics
- IPST splits some chapters differently: e.g., "Equilibrium" is a separate chapter in IPST but we fold it into Dynamics; "Solids & Fluids" is separate in IPST but we fold it into Thermo/Waves
- The IPST curriculum is confirmed via smartmathpro.com (2025-02-13), cross-referenced with the Physics Facebook page (facebook.com/physics.ipst)

## IPST Chemistry Topic Distribution (Verified)

Verified via 20 Chemistry notes created 2026-07-30 (ว311-ว313). Topic boundaries match `02_Chemistry - Overview.md` wikilinks and IPST curriculum structure.

### ม.4 (ว311) — Foundations & Physical Chemistry

| Semester | Topics (IPST chapter names) |
|---|---|
| **Semester 1** | อะตอมและสมบัติของธาตุ, พันธะเคมี (Atomic Structure, Periodic Table, Chemical Bonding, Intermolecular Forces — topics 01-04) |
| **Semester 2** | ปริมาณสารสัมพันธ์, สารละลาย, แก๊ส (Stoichiometry, Solutions, Gases — topics 05-07) |

### ม.5 (ว312) — Reactions & Equilibrium

| Semester | Theme | Topics (IPST chapter names) |
|---|---|---|
| **Semester 1** | **Equilibrium trilogy** (all on equilibrium constants and Le Chatelier) | กรดและเบส (Acids & Bases — 08), สมดุลเคมี (Chemical Equilibrium — 09), สมดุลไอออน (Ionic Equilibrium — 10) |
| **Semester 2** | **Energy / rate / electron trilogy** | อุณหเคมี (Thermochemistry — 11), จลนพลศาสตร์เคมี (Reaction Kinetics — 12), เคมีไฟฟ้า (Electrochemistry — 13) |

### ม.6 (ว313) — Organic & Applied Chemistry

| Semester | Topics (IPST chapter names) |
|---|---|
| **Semester 1** | เคมีอินทรีย์เบื้องต้น, ปฏิกิริยาเคมีอินทรีย์, สารอินทรีย์ที่มีหมู่ฟังก์ชัน (Organic Fundamentals, Organic Reactions, Functional Groups — topics 14-16) |
| **Semester 2** | พอลิเมอร์, ชีวเคมี, การวิเคราะห์เชิงคุณภาพ, เคมีอุตสาหกรรม (Polymers, Biochemistry, Qual Analysis, Industrial Chemistry — topics 17-20) |

### Pedagogy Pattern (ว312)

The ว312 split follows a deliberate theme grouping:

- **Semester 1 (08-10)** — all three topics use the **same mathematical machinery** (equilibrium constant, ICE table, Le Chatelier). Students learn the abstract framework once and apply it to three different chemical contexts (proton transfer, gas-phase reactions, ionic dissolution).
- **Semester 2 (11-13)** — three independent frameworks: thermodynamics (ΔH, ΔG), kinetics (rate law, Arrhenius), electrochemistry (E°, Nernst, Faraday).

### Chemistry LaTeX Conventions

- **Chemical formulas** as `\ce{species}` inside `$...$` or `$$...$$` (mhchem extension; standard in Obsidian since v0.9). Example: `$\ce{CH3COOH}$`, `$\ce{CaF2(s) <=> Ca^2+(aq) + 2F-(aq)}$`
- **Reactions** with arrows: `$\ce{2H2 + O2 -> 2H2O}$` or `$\ce{2H2 + O2 ->[\Delta] 2H2O}$` for heated
- **Tables of strong acids/bases, standard reduction potentials, solubility products** are standard pedagogical inclusions
- For organic: `$\ce{-OH}$` (alcohol), `$\ce{C=C}$` (alkene), `$\ce{C#C}$` (alkyne), `$\ce{-COOH}$` (carboxylic acid), `$\ce{-COOR}$` (ester), `$\ce{-NH2}$` (amine), `$\ce{-CONH2}$` (amide)

## Language Style: English Narrative with Thai in Parens (CRITICAL)

All advanced science notes (Physics, Chemistry, Biology, Earth Science, Computer Science) use **English narrative with Thai technical terms in `(...)` parentheses**. This is the user's confirmed style preference (2026-07-30).

**The pattern:**
- **Primary language**: English (prose, explanations, headers, problem statements, solutions)
- **Technical terms**: Thai in `(...)` parens, e.g. "electrons (อิเล็กตรอน)", "nucleus (นิวเคลียส)", "polymers (พอลิเมอร์)"
- **Terminology tables**: Keep format `| Thai | English | Symbol/Notes |` — these tables are the same in all subjects
- **Course coverage tables**: Scope and Key Skills columns in English (with Thai only where natural)
- **Formulas / LaTeX / `\\ce{}`**: Unchanged
- **Wikilinks**: Unchanged

**Why this style:** Parents (Thai speakers) can use the English as the main study text and reference Thai terms for clarity. The Physics notes set the precedent; Chemistry notes were retroactively converted to match; Biology notes were created in this style from the start.

**When creating new notes:** ALWAYS use English narrative from the start. Don't write Thai narrative first then convert — that wastes a full subagent pass.

**When converting existing Thai notes to English:**
1. Dispatch 3 parallel subagents (each handling ~7 files) for batches of 20+ files
2. Each subagent needs explicit "before/after" examples to avoid drifting back to Thai
3. Specify which sections to convert (prose) vs leave alone (tables, formula, wikilinks)
4. Verify after: spot-check first prose line of each note to confirm English-first
5. Some subagents may report "no changes needed" if notes were already partially in English — verify independently

## IPST Biology Topic Distribution

Created 2026-07-30, 20 notes in `Science/Advance/Biology/`.

### ม.4 (ว321) — Molecular & Cell Biology

| Semester | Topics |
|---|---|
| **Semester 1** | Cell Biology (01), Cell Membrane & Transport (02), Biomolecules (03) |
| **Semester 2** | Cell Energy (04), Cell Division (05), Molecular Biology (06), Genetics (07) |

### ม.5 (ว322) — Evolution, Diversity & Organismal Biology

| Semester | Topics |
|---|---|
| **Semester 1** | Evolution (08), Diversity of Life (09), Microbiology (10) |
| **Semester 2** | Plant Biology (11), Animal Biology (12), Human Body Systems (13) |

### ม.6 (ว323) — Ecology, Immunity & Biotechnology

| Semester | Topics |
|---|---|
| **Semester 1** | Immune System (14), Human Reproduction & Development (15), Ecology (16) |
| **Semester 2** | Environmental Science (17), Biotechnology (18), Behavioral Biology (19), Bioethics (20) |

### Biology Note Characteristics

- Course codes: ว321 (ม.4), ว322 (ม.5), ว323 (ม.6)
- Key biology-specific conventions: use `\\ce{}` for biochemical equations (e.g., `$\\ce{C6H12O6 + 6O2 -> 6CO2 + 6H2O + 36ATP}$`)
- Include Punnett squares as tables for genetics notes
- Include diagrams descriptions for cell structure, organ systems (Mermaid where possible)
- Hardy-Weinberg equation: $$p^2 + 2pq + q^2 = 1$$ with conditions table
- Central Dogma: DNA → RNA → Protein (replication, transcription, translation)
- Note: Some notes (09, 14, 08, 12, 10) came out shorter (105-115 lines) than the 150-line target. Consider enriching these in a future pass.

## IPST Earth Science Topic Distribution (ว341, Elective)

Created 2026-07-30, 10 notes in `Science/Advance/Earth_Science/` (note: underscore in folder name, not space — the agent chose `Earth_Science/` and the user accepted it).

Earth Science is a **1.5-credit elective** (ว341), typically taken in ม.4 or ม.5. It is NOT a required subject in the วิทย์-คณิต track, but many students take it.

### Folder Structure

```
Advance/Earth_Science/
├── 01_Minerals_and_Rocks.md          (160 lines)
├── 02_Plate_Tectonics.md             (143 lines)
├── 03_Earthquakes_and_Volcanoes.md   (164 lines)
├── 04_Weathering_and_Erosion.md      (175 lines)
├── 05_Earth_History.md              (186 lines)
├── 06_Weather_and_Climate.md         (175 lines)
├── 07_Oceanography.md               (191 lines)
├── 08_Water_Cycle_and_Hydrology.md   (212 lines)
├── 09_Solar_System_and_Astronomy.md  (206 lines)
└── 10_Climate_Change_and_Environment.md (205 lines)
```

### Topic Groupings

| Category | Topics | Description |
|---|---|---|
| **Geosphere** | 01-05 | Minerals/rocks, plate tectonics, earthquakes/volcanoes, weathering/erosion, geological history |
| **Atmosphere & Hydrosphere** | 06-08 | Weather/climate, oceanography, water cycle/hydrology |
| **Astronomy & Environment** | 09-10 | Solar system/astronomy, climate change/environment |

### Earth Science Note Characteristics

- Course code: ว341 (elective, NOT ว331-ว333 — the BOK overview header says ว341)
- Earth Science covers topics from ALL science disciplines: geology (geosphere), meteorology (atmosphere), oceanography (hydrosphere), astronomy (space), environmental science (climate)
- Notes are 143-212 lines, slightly shorter than Physics/Chemistry (because ว341 is a single elective, not 3 years)
- Cross-links reference Fundamental notes (19_Rocks_Minerals_Soil, 20_Weather_and_Climate, 21_Solar_System_and_Astronomy) and Biology (16_Ecology)
- No semester split table in BOK overview (it's a 1-year elective, not a 3-year progression)

### 2-Subagent Pattern for Small Batches (10 files)

When creating exactly 10 notes, use **2 parallel subagents** (not 3):
- **Subagent 1:** Topics 01-05 (Geosphere)
- **Subagent 2:** Topics 06-10 (Atmosphere/Hydrosphere/Astronomy/Environment)

This completed all 10 Earth Science notes in ~4 minutes. Using 3 subagents for 10 files wastes a subagent on only 3-4 topics; 2 subagents with 5 topics each is the sweet spot.

### Folder Naming Convention

When the agent creates a folder for a multi-word subject, it may use underscores (`Earth_Science/`) instead of spaces (`Earth Science/`). The user accepted `Earth_Science/`. For consistency with other subject folders (`physic/`, `Chemistry/`, `Biology/` — all single-word), prefer single-word names where possible. For multi-word, underscores are fine — Obsidian handles them identically to spaces.

## IPST Computer Science Topic Distribution (ว331-ว333)

Created 2026-07-30, 12 notes in `Science/Advance/Computer_Science/`. Course codes: ว331 (ม.4), ว332 (ม.5), ว333 (ม.6). Note: วิทยาการคำนวณ (Computer Science) was introduced as a formal subject in the 2017 curriculum revision (หลักสูตร 2560).

### ม.4 (ว331) — Foundations & Programming

| Semester | Topics |
|---|---|
| **Semester 1** | Computational Thinking (01), Data Representation (02), Boolean Logic (03) |
| **Semester 2** | Programming Fundamentals (04) |

### ม.5 (ว332) — Data & Algorithms

| Semester | Topics |
|---|---|
| **Semester 1** | Functions and Modularity (05), Algorithms (06) |
| **Semester 2** | Data Structures (07), Object-Oriented Programming (08) |

### ม.6 (ว333) — Systems & Modern Computing

| Semester | Topics |
|---|---|
| **Semester 1** | Computer Systems and Networks (09), Databases (10) |
| **Semester 2** | Artificial Intelligence (11), Digital Citizenship (12) |

### Computer Science Note Characteristics

- Unlike other sciences, CS notes include **Python code blocks** (```` ```python ````) in Section 4 (Problem Types) instead of LaTeX formulas
- Big-O notation uses `$O(n^2)$` inline math format
- Logic gates (AND/OR/NOT/XOR/NAND/NOR) presented as truth tables
- AI note covers ML/DL hierarchy, neural networks, generative AI — modern topics reflecting the 2560 curriculum update
- Notes are 162-281 lines (some of the longer notes due to code examples)
- 2-subagent pattern used: Subagent 1 (topics 01-06), Subagent 2 (topics 07-12)

## SearXNG Verification Pattern

Use SearXNG MCP to verify IPST curriculum before creating notes:

1. Search: `mcp__searxng__searxng_web_search` with query like `"IPST สสวท หลักสูตรฟิสิกส์ มัธยมปลาย ว301 ว302 ว303"`
2. Look for smartmathpro.com articles — they summarize IPST curriculum by subject/year
3. Use `mcp__searxng__web_url_read` to fetch the full article
4. Cross-reference topic distribution against BOK overview
5. Note any discrepancies (our BOK may be a superset or may reorganize topics differently)

**Pitfall:** SearXNG returns mixed results with spam. Filter for `.com` educational sites (smartmathpro.com), `.ac.th` domains, and Facebook pages of official IPST subject pages. The user is aware of rate-limits; space out calls (2-3 then stop, then fall back to model knowledge).

## Parallel Subagent Batching for Note Creation

For creating 20+ notes, dispatch 3 parallel subagents via `delegate_task`:

- **Subagent 1:** Topics 01-08 (e.g., ม.4 Semester 1-2 mechanics)
- **Subagent 2:** Topics 09-17 (e.g., ม.5 electricity/optics)
- **Subagent 3:** Topics 18-23 (e.g., ม.6 modern physics)

Each subagent gets:
- Exact file paths to create
- The 5-section template (above)
- Topic content guide with key formulas and Thai terminology
- Rules: single-backslash LaTeX, $$...$$ for display math, 150-200 lines per note

Result: 23 notes created in ~3 minutes (vs ~15+ minutes serial).

### 2-Subagent Pattern (10 files)

For 10-note batches (e.g., Earth Science), use 2 parallel subagents:
- **Subagent 1:** Topics 01-05
- **Subagent 2:** Topics 06-10

Proven: 10 Earth Science notes created in ~4 minutes. Don't use 3 subagents for 10 files — the third subagent gets only 3-4 topics, wasting overhead.

### Small-Batch Pattern (5-10 files)

When creating 6-10 files (below the delegation threshold but above manual-effort threshold), **do NOT delegate** — subagent overhead exceeds savings, and you lose guaranteed style consistency. Instead:

1. **Batch parallel `write_file` calls in one assistant turn** — the runtime executes independent file writes concurrently, and you avoid re-sending context for each round-trip. Practical cap: ~5 files per turn keeps tool results manageable.
2. **For 6 files:** do the first file solo to validate the template renders, then batch the remaining 5 in parallel. Proven for Chemistry ม.5 (ว312) topics 08-13 (2026-07-30).
3. **Skip subagents for style consistency** — when each note must follow the exact same template with shared conventions (e.g., same LaTeX style, same terminology table structure), a single author produces more uniform output than 3 subagents.
4. **Front-load research in the same turn as file creation** — read the overview file and a representative sibling template, then write all files in the same assistant turn.

Pattern: 6 notes in ~12 seconds (vs ~3 minutes via delegation; vs ~2 minutes via serial write_file).

## Wikilink Path Prefix Update Pattern (and the User's Revert)

After moving notes into `Fundamental/` and `Advance/` subfolders, you can update BOK overview wikilinks to add path prefixes (`[[Fundamental/01_Topic]]`, `[[Advance/01_Topic]]`). **But the user explicitly reverted this.** The user prefers short wikilinks (`[[01_Measurement_and_Scientific_Method]]`) in the BOK overview files because:

1. Obsidian resolves wikilinks by filename regardless of path
2. Long paths add visual noise without functional benefit
3. The folder structure is already clear from the BOK overview's own prose

**Strategy when doing Phase 3 BOK overview updates:**

- **Default to short wikilinks** (`[[01_Topic]]`) — that's what the user actually wants
- Only add path prefixes if the user explicitly asks for them or if short links would be ambiguous (e.g., a topic with the same number in different folders)
- If you DO add path prefixes, follow the patterns below and verify with `grep -c 'Advance/'`

### When path prefixes ARE needed (rare)

- When the same numbered topic exists in multiple subfolders (e.g., both `Advance/physic/01_...` and `Advance/Chemistry/01_...` exist — though numbers don't usually collide in this vault)
- When the user explicitly asks for "fully qualified links" or "show the folder in the link"

### Batch patching with execute_code

```python
import re

def patch_wikilinks(filepath, prefix, max_topic):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for i in range(1, max_topic + 1):
        num = f"{i:02d}"
        pattern = rf'\[\[{num}_([A-Za-z_]+)(\|.*?)?\]\]'
        content = re.sub(pattern, lambda m: f'[[{prefix}{num}_{m.group(1)}{m.group(2) or ""}]]', content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_wikilinks("path/to/00_Fundamental Science - Overview.md", "Fundamental/", 22)
patch_wikilinks("path/to/01_Physics - Overview.md", "Advance/", 23)
```

### Pitfall: hermes_tools.write_file dedup

`hermes_tools.write_file` (inside execute_code) may refuse to write, returning `"status": "unchanged"` with `content_returned: false` if it thinks the file hasn't changed. This happens when the file was read earlier in the conversation and the tool's dedup cache thinks the content is the same.

**Symptom:** `execute_code` script exits 0, but `grep` shows the original short links unchanged.

**Fix:** Use direct Python `open()/read()/write()` file I/O in execute_code instead of `hermes_tools.write_file` for batch patching operations. This bypasses the dedup cache entirely.

### Verification

After patching, verify links were actually updated:
```bash
grep -c 'Fundamental/' "path/00_Fundamental Science - Overview.md"  # should be 22
grep -c 'Advance/' "path/01_Physics - Overview.md"                   # should be 23
```

## Mermaid Diagram Enrichment Pass (Post-Creation)

After creating all advanced science notes, add mermaid diagrams to notes where visual classification trees, process flows, or cycles add educational value. Not every note needs one — target ~50-60% of notes.

### What to Add

**High-value diagram types by subject:**

| Subject | Best Diagram Candidates | Diagram Type |
|---|---|---|
| Physics | Force classification, energy transformations, collision types, heat transfer, classical vs relativistic | `flowchart TD` classification trees |
| Chemistry | Atomic models timeline, element categories, bond types, acid-base theories, Le Chatelier responses, hydrocarbon taxonomy, cell types | `flowchart TD` classification trees |
| Biology | Cell types, biomolecules, energy flow (photosynthesis↔respiration), cell cycle, central dogma, inheritance patterns, taxonomy tree, ecosystem energy flow | `flowchart TD` trees + `flowchart LR` process flows |
| Earth Science | Rock cycle, plate boundaries, seismic waves, atmospheric layers, water cycle, stellar evolution, carbon cycle | `flowchart TD` cycles + classification |
| Computer Science | CT pillars, logic gate classification, algorithm types, data structure taxonomy, OSI layers, AI hierarchy | `flowchart TD` classification trees |

### Workflow (Proven 2026-07-30: 43 diagrams added to 40 notes in ~5 min)

1. **Scan for existing diagrams:** `find <vault>/Advance -name "*.md" -exec grep -l '```mermaid' {} \;` — skip notes that already have one
2. **Dispatch 3 parallel subagents** by subject grouping:
   - Subagent 1: Physics + Chemistry (~15 notes)
   - Subagent 2: Biology (~10 notes)
   - Subagent 3: Earth Science + Computer Science (~13 notes)
3. **Each subagent:** READ each file → find Section 3 (Key Concepts) insertion point → `patch` in a mermaid block
4. **Mermaid rules (CRITICAL for Obsidian):**
   - Use `flowchart TD` or `flowchart LR` (NOT `graph`)
   - NO `()` in labels → use `&#40;`/`&#41;` or square brackets
   - NO `"1."` numbered dots → use `"1 "` 
   - NO `&` → use `and`
5. **Keep diagrams concise:** 8-15 nodes max — clarify, don't overwhelm
6. **Verify after:** `find <vault>/Advance -name "*.md" -exec grep -l '```mermaid' {} \; | wc -l` — count should match expected

### Diagram Placement Convention

Insert diagrams at the **start of Section 3 (Key Concepts)**, before the first `### 3.1` subsection. This gives readers a visual overview before diving into details. The diagram acts as a "map" for the concepts that follow.

### Example Patch

```
old_string: "## 3 | Key Concepts\n\n### 3.1"
new_string: "## 3 | Key Concepts\n\n```mermaid\nflowchart TD\n    A[\"Chemical Bonds\"] --> B[\"Ionic\"]\n    A --> C[\"Covalent\"]\n    ...\n```\n\n### 3.1"
```

### Pitfall: Don't force diagrams where they don't help

Notes that are purely procedural (e.g., stoichiometry calculations, programming exercises) may not benefit from classification trees. Skip them rather than adding forced visuals. The target is ~50-60% coverage, not 100%.

## User Restructuring Mid-Project (Common Pattern)

The user often reorganizes the vault structure between sessions. Common patterns observed:

- **Flat → Fundamental/Advance split:** When expanding from ป.1-ม.3 to ม.4-ม.6, user asks to split into subfolders. Create subfolders, `mv` existing files in one batch, create new advanced files in the new subfolder.
- **Advance/ → Advance/subject/ split:** When adding a second subject (Chem after Physics), user creates `Advance/Chemistry/` for new content. Don't move existing Physics files — let user reorganize manually.
- **Rename convention:** User may use slightly non-standard names (e.g., `physic/` for `physics/`). **Respect the user's exact choice** — don't auto-correct to "more standard" spellings.
- **Move BOK wikilinks to short form:** After user adds subject folders, they may revert the `Advance/01_Topic` wikilinks in BOK overviews back to `01_Topic` short form. Don't re-add the path prefixes after this.
- **Restructure without explicit instruction:** The user may reorganize files between sessions (e.g., via Obsidian UI) without telling you. Always `find` the actual file list before assuming structure.
