# Thai Social Studies Topic Notes Pattern

## Overview

Social Studies (สังคมศึกษา ศาสนา และวัฒนธรรม) topic notes follow the same swe-knowledge style as Math and Science notes, but with strand-specific content patterns.

## File Location

Topic notes go in `F:\obsidian_note\general-knowledge\Social Studies\` (NOT in `body-of-knowledge/`).

## File Naming

`01_Topic_Name.md` — numbered sequentially, underscores for spaces.

## YAML Frontmatter

```yaml
---
tags: [social-studies, <strand-tag>, <topic-tag>, primary, lower-secondary]
source: "OBEC Basic Education Core Curriculum B.E. 2551 (2008), revised 2560 (2017)"
created: YYYY-MM-DD
course_codes: ["ส11101", "ส12101", ...]
strand: "สาระที่ X: <strand name>"
---
```

## Standard Sections

1. **Title** — English name + Thai name
2. **Overview** — 1-2 paragraphs
3. **Grade Band Breakdown** — Table with ป.1-3, ป.4-6, ม.1-3 columns
4. **Concept Areas** — Numbered table with wikilinks
5. **Key Content Tables** — Strand-specific (see below)
6. **Thai Terminology** — Thai → English table
7. **Cross-Links** — Back to Social Studies overview + related topics

## Strand-Specific Content Patterns

### Religion (สาระที่ 1)
- Four Noble Truths, Noble Eightfold Path, Five Precepts
- Buddhist doctrines (ขันธ์ 5, ไตรลักษณ์, ปฏิจจสมุปบาท)
- Other religions in Thailand (Islam, Christianity, Hinduism, Sikhism)
- Buddhist proverbs (พุทธศาสนสุภาษิต)

### Civics (สาระที่ 2)
- Thai government structure (three branches)
- Constitution and laws
- Rights and duties of citizens
- Thai culture and traditions (4 regions)
- ASEAN studies
- Social institutions (family, education, religion, economy, healthcare)
- Social norms, roles, and stratification
- Socialization (agents, theories, identity, digital socialization)
- Culture and change (diffusion, globalization, preservation)
- International relations (UN, foreign policy, global issues)
- Media literacy (bias, propaganda, misinformation, digital citizenship)
- Conflict resolution (negotiation, mediation, civic participation)

**Full 13 concept areas for Civics strand (สาระที่ 2):**
01. Democracy and Government
02. Thai Culture and Traditions
03. ASEAN Studies
04. Rights, Duties, and Laws
05. Thai Constitution
06. Government Structure
07. Social Institutions
08. Social Norms and Status
09. Socialization
10. Culture and Change
11. International Relations
12. Media Literacy
13. Conflict Resolution

### Geography (สาระที่ 5)
- Thailand's six regions, physical features, climate
- Natural disasters (floods, droughts, earthquakes, tsunami)
- Map skills, GIS, GPS, coordinates
- Plate tectonics, rock cycle, weathering/erosion
- Monsoon system, Köppen climate classification, climate change
- Natural resources (renewable/non-renewable, energy, dams)
- Population geography (demographic transition, aging society)
- Urbanization (Bangkok primacy, smart cities)
- Economic geography (agriculture, industry, EEC)
- Environmental conservation (biodiversity, SDGs, protected areas)
- World regions, continents, trade routes, geopolitical blocs
- Geographic skills (fieldwork, GIS analysis, research methods)

**Full 14 concept areas for Geography strand (สาระที่ 5):**
01. Geography of Thailand
02. Natural Disasters and Environment
03. Map Skills and Geographic Tools
04. Physical Geography — Landforms
05. Climate
06. Natural Resources
07. Population Geography
08. Settlement and Urbanization
09. Economic Geography
10. Environmental Conservation
11. Thailand's Regions
12. World Regions
13. Geographic Coordinates
14. Geographic Skills

## Topic Note Format (Established Pattern)

Each topic note follows this structure:

```yaml
---
tags: [social-studies, <strand-tag>, <topic-tag>, primary, lower-secondary, upper-secondary]
source: "OBEC Basic Education Core Curriculum B.E. 2551 (2008), revised 2560 (2017)"
created: YYYY-MM-DD
course_codes: ["ส11102", "ส12102", ...]
strand: "สาระที่ X: <strand name>"
---
```

```markdown
# English Title — ภาษาไทย Title

> *"Quote that captures the essence of this topic."*

[1-2 paragraph introduction]

---

## 1 | Grade Band Breakdown

| Grade | Key Content |
|---|---|
| **ป.1–3** | ... |
| **ป.4–6** | ... |
| **ม.1–3** | ... |
| **ม.4–6** | ... |

---

## 2 | [First Content Section]
[Tables with Thai/English columns, Mermaid diagrams for hierarchies]

...

## N | Thai Terminology

| Thai | English |
|---|---|
| คำศัพท์ | Vocabulary |

---

## N+1 | Cross-Links

- [[Social Studies - Overview|← Back to Social Studies]]
- [[Related_Topic]] — How it connects
```

### Key Format Elements
- Bilingual title (English — Thai) with italicized quote
- Numbered sections starting with Grade Band Breakdown
- Thai-English tables for terminology and comparisons
- Mermaid diagrams for hierarchical content (government, institutions)
- Terminology table near the end
- Cross-links to related topics using actual filenames

## Key Differences from Math/Science

- **No formulas** — Social Studies is narrative/analytical, not computational
- **More emphasis on Thai context** — Culture, history, governance specific to Thailand
- **Buddhist terminology** — Pali/Sanskrit terms alongside Thai
- **Course codes use ส prefix** — ส11101-ส33102 (vs ค for Math, ว for Science)
- **Spiral across all 12 years** — Unlike Math/Science which split at ม.4

## Example Topics Created

| # | File | Strand |
|---|---|---|
| 01 | 01_Buddhist_Principles | Religion |
| 02 | 02_Democracy_and_Government | Civics |
| 03 | 03_Economics_Fundamentals | Economics |
| 04 | 04_Thai_History | History |
| 05 | 05_Geography_of_Thailand | Geography |
| 06 | 06_Thai_Culture_and_Traditions | Civics |
| 07 | 07_World_History_and_Civilizations | History |
| 08 | 08_Natural_Disasters_and_Environment | Geography |
| 09 | 09_ASEAN_Studies | Civics |
| 10 | 10_Personal_Finance | Economics |
