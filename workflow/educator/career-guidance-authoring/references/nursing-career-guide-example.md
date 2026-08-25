# Nursing Career Guide — Worked Example

> Complete file listing and key patterns from the nursing career guidance session (2026-07-27).
> Use as a template when building career guides for other professions.

## Target Vault

```
F:\obsidian_note\general-knowledge\career\nurse\
```

## Files Created (9 files, ~80 KB total)

| # | File | Size | Purpose |
|---|---|---|---|
| 🏠 | `Nursing - Overview.md` | 8 KB | Entry point: profession definition, regulatory framework (สภาการพยาบาล), education pathway (Mermaid), reading paths |
| 01 | `01_Foundation_Sciences.md` | 7 KB | 7 foundation subjects: Anatomy, Physiology, Biochem, Micro, Pharma, Pathophysio, Nutrition |
| 02 | `02_Nursing_Fundamentals.md` | 7 KB | Nursing Process (ADPIE), vital signs, infection control, 5 Rights med admin, wound care |
| 03 | `03_Medical_Surgical_Nursing.md` | 8 KB | 7 body systems, perioperative nursing, emergency/critical care |
| 04 | `04_Maternal_Child_and_Mental_Health_Nursing.md` | 9 KB | OB/GYN + Pediatrics + Mental Health (3 specialties in 1 file) |
| 05 | `05_Community_and_Public_Health_Nursing.md` | 9 KB | Thai primary healthcare, อสม., epidemiology, Sufficiency Economy Health |
| 06 | `06_Nursing_Administration_Ethics_and_Law.md` | 9 KB | POSDC management, ICN Code, Thai Nursing Profession Act B.E. 2540 |
| 07 | `07_Clinical_Practice_and_Research.md` | 9 KB | 2,000+ hrs practicum, EBP/PICO, evidence hierarchy, APN pathway |
| 08 | `08_University_Guide_and_Career_Paths.md` | 14 KB | TCAS, 15+ universities (3 tiers + MOPH), tuition, salaries, career ladder, international paths |

## Key Patterns Established

### 1. Overview Structure
- Quote block (English + Thai)
- "What Is This?" — target audience and purpose
- 3 core requirements (education → exam → license)
- Numbered knowledge domain list with `[[wikilinks]]` and emoji category headers
- Regulatory body table (Thai/English/Role columns)
- Legal framework with key section summaries
- Mermaid `graph TD` education pathway diagram
- Thai-English terminology table
- Reading paths for different user types

### 2. Chapter File Structure
- YAML frontmatter: tags, source, created, domain, prerequisites
- Quote block at top
- Numbered sections (## 1 | Section Name)
- Thai-English terminology table (mandatory in every file)
- Mermaid diagrams for processes
- `[[wikilinks]]` to related chapters and back to overview

### 3. University Guide Pattern (File 08)
- Admission requirements table
- TCAS rounds with exam weights
- University tier lists (🥇 Tier 1, 🥈 Tier 2, 🥉 Tier 3)
- MOPH/government college alternative pathway
- Tuition table by institution type
- Scholarship table
- Career settings with salary ranges
- Mermaid career ladder diagram
- "Is this profession right for you?" comparison table
- International pathway requirements and salaries

### 4. Bilingual Pattern
- Headers: English
- Body text: English with Thai terms in parentheses
- Terminology tables: Thai | English | Notes (in every file)
- Profession-specific Thai legal/regulatory terms included

### 5. Thai-Specific Content
- Professional council (สภา) with Thai name and act reference
- TCAS admission system
- Universal Health Coverage schemes (for healthcare)
- MOPH scholarship and service commitment
- Sufficiency Economy Philosophy integration (where relevant)
- Thai university tiers and locations

## Common Pitfalls Discovered

1. **Web search unreliability:** SearXNG returns 403. Thai .go.th domains block curl. Wikipedia API works for general overviews but "Nursing in Thailand" page doesn't exist. Fall back to training knowledge.
2. **Wikipedia API quirks:** `action=query&prop=extracts` sometimes returns empty for specific pages. Try `action=parse&prop=wikitext` as alternative. Some pages only exist as redirects.
3. **File size balance:** Overview + university guide should be the largest files (8-14 KB). Domain chapters ~7-9 KB each. Don't make domain chapters too thin (<5 KB) or too dense (>15 KB).
4. **Cross-links:** Every chapter should link back to overview AND to adjacent chapters. The overview links forward to all chapters.
