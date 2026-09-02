# Thai Mathematics Strand Overview Pattern

Proven template used across 10 strand sub-overview files (Fundamental Math ป.1-ม.3 + Advanced Math ม.4-ม.6). Copy this structure when creating strand/category-level overviews within a BOK subject.

## Template Structure

```yaml
---
tags: [overview, mathematics, <level>, <strand-tag>, ipst, thai-curriculum, <spiral|linear>]
---
```

```markdown
# <emoji> Strand N: <English Name> (<Thai Name>)

> **Subject Area:** <Full subject name> — <grade range>
> **Course Codes:** <code range>
> **Total Concept Areas:** N sub-strands | **Duration:** <years/grade bands>
> **Source:** IPST (สสวท.) <curriculum reference> — Strand <N>
> **Prerequisites:** [[prerequisite]]
> **Foundation for:** [[downstream]]

## What Is This?

[2-3 paragraphs: explain the strand, its importance, how content is organized, spiral/linear nature, IPST strand number, key themes]

## The N Sub-Strands

### 1. Sub-Strand Name (Thai Name)

**Grade Bands:**

| Band | Key Concepts |
|---|---|
| **Level 1** | Topic A, Topic B, ... |
| **Level 2** | Topic C, Topic D, ... |

**Key Formulas/Theorems:** (as needed)

| Concept | Formula | Application |
|---|---|---|

**Key Thai Terminology:**

| Thai | Romanized | English |
|------|-----------|---------|
| ... | ... | ... |

**Common Misconceptions:**
- Misconception 1
- Misconception 2

**Real-Life Connections:**
- Connection 1
- Connection 2

[Repeat for each sub-strand — typically 3-9 per file]

## Progression Summary Table

| Sub-Strand | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| ... | ... | ... | ... |

## Cross-Links to Other Strands

- [[Other Strand]] — How they connect

## Exam Relevance

| Exam | Relevance |
|---|---|
| **Exam 1** | ~X%: specific topics tested |
| **Exam 2** | ~Y%: specific topics tested |

## IPST Textbook References

| Level | Textbook |
|---|---|
| **Level 1** | Full textbook name |
| **Level 2** | Full textbook name |

## Related

- [[Parent Overview|← Back to Overview]]
- [[Previous Strand|← Previous Strand]]
- [[Next Strand|→ Next Strand]]
```

## Key Conventions

### Structural
- **One file per strand** — not one per concept area; group related concept areas under a strand
- **Grade band progression inside each sub-strand** — don't split by grade; show the progression within the sub-strand section
- **Progression summary table at bottom** — cross-reference table showing all sub-strands × grade bands at a glance
- **Cross-links section** — connects to every other strand overview + advanced/fundamental counterpart

### Content
- **Thai terminology table per sub-strand** — Thai, romanized, English in 3 columns
- **Common misconceptions per sub-strand** — bullet list of the most common student errors
- **Real-life connections per sub-strand** — concrete Thai-context examples (ไม่ใช่ examples นอกบริบท)
- **IPST textbook references per level** — full book names with publisher (สสวท.)
- **Exam relevance with approximate weight** — O-NET, A-Level, PAT1, กสพท.

### Diagrams
- **Mermaid over ASCII** — always
- **flowchart TD** for hierarchies (number systems, concept maps)
- **quadrantChart** for coordinate planes (use `quadrant-1` through `quadrant-4`, `[nl]` for line breaks)
- **flowchart LR** for probability scales and process flows

### Emoji Convention
| Emoji | Strand |
|---|---|
| 🔢 | Numbers and Operations |
| 📐 | Algebra and Patterns |
| 📏 | Geometry and Measurement |
| 📊 | Data, Statistics, and Probability |
| 🧠 | Mathematical Processes |
| 🏛️ | Foundations and Functions |
| ∫ | Calculus |
| 🔣 | Algebra and Geometry (Advanced) |
| 🎲 | Probability and Statistics (Advanced) |
| 🧩 | Discrete and Advanced Topics |

## IPST Strand Mapping for Mathematics

### Fundamental Mathematics (ป.1-ม.3) — 6 IPST Strands
| Strand | Thai Name | Grouped Into |
|---|---|---|
| สาระที่ 1 | จำนวนและการดำเนินการ | Strand 1: Numbers and Operations |
| สาระที่ 2 | การวัด | Strand 3: Geometry and Measurement (combined with 3) |
| สาระที่ 3 | เรขาคณิต | Strand 3: Geometry and Measurement |
| สาระที่ 4 | พีชคณิต | Strand 2: Algebra and Patterns |
| สาระที่ 5 | การวิเคราะห์ข้อมูลและความน่าจะเป็น | Strand 4: Data, Statistics, and Probability |
| สาระที่ 6 | ทักษะและกระบวนการทางคณิตศาสตร์ | Strand 5: Mathematical Processes |

### Advanced Mathematics (ม.4-ม.6) — Organize by Mathematical Domain
| Strand | Coverage |
|---|---|
| 6: Foundations and Functions | Sets, Logic, Real Numbers, Functions, Exp/Log, Trig, Sequences/Series |
| 7: Calculus | Limits, Differentiation, Integration, Differential Equations |
| 8: Algebra and Geometry | Complex Numbers, Matrices, Analytic Geometry, Vectors |
| 9: Probability and Statistics | Advanced Probability, Distributions, Descriptive/Inferential Stats |
| 10: Discrete and Advanced Topics | Discrete Math, Proof Techniques, Linear Programming |

## File Size Targets
- Fundamental Math sub-overviews: 14-27 KB (deeper because each sub-strand covers 3 grade bands)
- Advanced Math sub-overviews: 14-19 KB (more focused, each sub-strand covers ม.4-6 only)

## Pitfalls
- **Don't duplicate content between main overview and sub-overview.** The main overview gets a category table with links; sub-overviews carry the deep content.
- **Don't skip the progression summary table.** It's the single most useful reference — shows all sub-strands across all grade bands at a glance.
- **Don't skip the Thai terminology.** Every sub-strand needs its own terminology table. Thai students and teachers reference these files.
- **Don't forget real-life connections with Thai context.** Generic examples feel imported. Use Thai-context examples (baht/satang, ไร่/งาน/วา, Thai exam names).
- **Verify no double-backslash LaTeX.** Run `grep -c '\\\\\\\\' *.md` after writing all files. Should be 0 across all files.
