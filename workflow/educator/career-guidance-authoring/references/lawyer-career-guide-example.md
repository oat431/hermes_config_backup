# Lawyer Career Guide — Worked Example

> Complete file listing and key patterns from the lawyer career guidance session (2026-07-27).
> Demonstrates Pattern C: single degree feeding multiple distinct career tracks.

## Target Vault

```
F:\obsidian_note\general-knowledge\career\lawyer\
```

## Files Created (8 files, ~79 KB total)

| # | File | Size | Purpose |
|---|---|---|---|
| 🏠 | `Lawyer - Overview.md` | 8 KB | 3 career pathways (Lawyer, Prosecutor, Judge) in one Mermaid diagram, Lawyers Council vs Thai Bar |
| 01 | `01_Foundations_of_Law.md` | 11 KB | Legal philosophy, hierarchy of Thai law (Mermaid), court system (Mermaid), IRAC reasoning |
| 02 | `02_Civil_and_Commercial_Law.md` | 9 KB | All 6 Books of ป.พ.พ.: Persons, Obligations, Specific Contracts, Property, Family, Succession |
| 03 | `03_Criminal_Law.md` | 10 KB | Penal Code: elements of crime, defenses, parties, major offenses, punishments |
| 04 | `04_Constitutional_and_Administrative_Law.md` | 8 KB | 20 constitutions, government structure, fundamental rights, administrative court |
| 05 | `05_International_and_Business_Law.md` | 9 KB | International law + Thai dualism, 7 business entities, IP law, tax, labor — corporate toolkit |
| 06 | `06_Legal_Procedure_and_Litigation.md` | 9 KB | Civil procedure flow, criminal procedure flow, evidence rules, ADR (mediation, arbitration) |
| 07 | `07_University_Guide_and_Career_Paths.md` | 14 KB | TCAS (no science needed!), 15+ universities, 3 career tracks with salaries, เนติบัณฑิต, law firms |

## Key Patterns for Multiple Career Track Professions

### 1. Overview Must Show ALL Tracks
- The overview Mermaid diagram is CRITICAL — it must show the branching from a single LL.B. into lawyer, prosecutor, and judge tracks with separate entry gates
- Include a table showing "who can practice" with license source for each role
- Distinguish between: lawyer (license from Lawyers Council), prosecutor (civil service exam from OAG), judge (judicial commission exam)

### 2. TCAS — All Tracks Accepted
- Law accepts ALL ม.6 tracks (Science, Arts, Vocational) — emphasize this accessibility
- No science/math requirements
- Emphasis on Thai language, analytical writing, logical reasoning
- This is a key differentiator from nursing/engineering

### 3. Professional Body Distinction
- Lawyers Council (สภาทนายความ) — licenses lawyers
- Thai Bar Association (เนติบัณฑิตยสภา) — advanced education, REQUIRED for judge/prosecutor
- These are SEPARATE organizations — don't conflate them

### 4. Civil Law System
- Thailand is a civil law system (ระบบประมวลกฎหมาย) — primary source is written codes, not precedent
- Supreme Court decisions (คำพิพากษาศาลฎีกา) are persuasive but NOT formally binding
- Include this distinction in the foundations chapter

### 5. Major Codes as Domain Files
- Map domain files to major Thai legal codes: ป.พ.พ. (Civil), ป.อ. (Criminal), รัฐธรรมนูญ (Constitutional)
- Each code gets its own chapter with section references
- Legal procedure (วิธีพิจารณา) gets its own file — it's as important as substantive law

### 6. Career Salary Differentiation
- Judge and prosecutor have civil service salary scales with benefits
- Law firm: wide range (small firm vs international firm)
- In-house counsel: corporate salary structures
- Include law firm names as examples (Baker McKenzie, Tilleke, etc.)

## Mermaid Issues Found & Fixed (This Session)

Two rendering bugs surfaced after the lawyer guide was created:

### Bug 1: `graph` → `flowchart` (deprecated syntax)
- **Symptom:** "syntax error" in Hierarchy of Thai Law diagram
- **Root cause:** `graph TD` is deprecated; Obsidian's Mermaid renderer requires `flowchart TD`
- **Fix:** Batch-replaced 37 instances across all 5 career folders
- **Prevention:** Never use `graph` — always `flowchart`

### Bug 2: Parentheses `()` inside node labels
- **Symptom:** "unsupported markdown: list" error on various diagrams
- **Root cause:** Mermaid uses `()` for round-rectangle node shapes, so `["Label (text)"]` confuses the parser
- **Fix:** 25 instances across 10 files — `(text)` → `&#40;text&#41;` (HTML entities)
- **Affected labels** (lawyer-specific):
  - `"LL.B. (น.บ.)"` → `"LL.B. &#40;น.บ.&#41;"`
  - `"พระราชบัญญัติ (พ.ร.บ.)"` → `"พระราชบัญญัติ &#40;พ.ร.บ.&#41;"`
  - `"Courts of Justice (ศาลยุติธรรม)"` → `"Courts of Justice &#40;ศาลยุติธรรม&#41;"`
  - `"(8 subjects)"`, `"(License)"`, `"(for corporate work)"`, `"(exit option)"`, etc.
- **Prevention:** Never put literal `()` in Mermaid labels — always use `&#40;`/`&#41;`
