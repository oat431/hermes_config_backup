# Thai → English Conversion: IPST Chemistry Notes

Worked example from a session that converted 7 Chemistry notes (topics 01–07) from Thai narrative to English narrative, matching a pre-existing "Physics style" reference file.

## Source / target context

- **Source vault:** `F:/obsidian_note/general-knowledge/Science/Advance/Chemistry/`
- **Target style file:** `01_Measurement_and_Scientific_Method.md` in the adjacent Physics folder.
- **Source format:** Thai prose narrative with English in tables/code/formulas, plus Thai on title lines (e.g. `# Atomic Structure — โครงสร้างอะตอม`).
- **Target format:** English prose narrative; Thai kept in `(...)` parens for technical terms; same line counts as originals (179/186/230/202/233/266/324 for the 7 files).

## Conversion patterns that worked

### Title line — keep both languages

```markdown
# Atomic Structure — โครงสร้างอะตอม
```

The bilingual title stays — Thai readers still see the original Thai alongside the English.

### Intro paragraph — narrative with parenthetical Thai

```markdown
Atomic structure (โครงสร้างอะตอม) is the fundamental building block of chemistry.
It explains the components inside the atom (อะตอม): protons (โปรตอน),
neutrons (นิวตรอน), and electrons (อิเล็กตรอน), as well as the arrangement of
electrons in different energy levels (ระดับพลังงาน).
```

The first mention of each Thai technical term gets the Thai form in `(...)`. Subsequent mentions can be English-only. Sentence rhythm should be assertive and explanatory, not bullet-list-y.

### Section 1 Scope cell — mixed Thai/English

```markdown
| **Semester 1** | Atomic structure (โครงสร้างอะตอม), subatomic particles (อนุภาคมูลฐาน), atomic number (เลขอะตอม), mass number (เลขมวล), isotopes (ไอโซโทป), electron configuration (การจัดเรียงอิเล็กตรอน), quantum numbers (เลขควอนตัม) | Explain structure, draw orbital diagrams, apply Aufbau/Hund/Pauli rules |
```

Same convention as the intro — English prose carrying Thai technical terms in `(...)`. The Key Skills column drops Thai entirely (it's already an English-language skill label).

### Section 2 Thai↔English terminology table — preserve as-is

The pre-existing Thai/English/Symbol-Notes three-column tables already do the right thing. Do not regenerate them.

### Section 3.x subsection headings — bilingual heading

```markdown
### 3.1 Structure of the Periodic Table (โครงสร้างตารางธาตุ)

### 3.5 Ionization Energy (IE)
```

Use English as the primary heading and append the Thai in parens **only when the Thai carries meaning beyond the English** (i.e. when a Thai reader would scan the heading list and want to find it via Thai). For headings whose English is unambiguous and idiomatic, skip the parens.

### Section 4 problem-type heading — translate to English

```markdown
### Type 1: Finding Atomic Number and Mass Number
```

The Thai phrase `หาเลขอะตอมและเลขมวล` becomes English prose, not literal translation. The pattern: action verb → object.

### Section 5 Cross-Links — translate only the description

```markdown
- [[01_Atomic_Structure]] — Electron configuration is the basis of the periodic table
- [[03_Chemical_Bonding]] — Valence electrons determine bonding
- [[../../Fundamental/10_Atoms_Elements_and_Compounds]] — Foundation of elements from ม.1-3
```

Wikilink paths stay exactly as-is. Only the trailing description text is translated. Keep the educational register ("— Foundation of...", "— ...is the basis of...").

## Conversion workflow that worked in this session

1. `ls` both Chemistry and Physics directories in one parallel call to see the full scope.
2. Read the Physics reference file (target style) first to lock in voice.
3. Read all 7 source Chemistry files (one batched parallel read pair at a time).
4. Create a `todo` list with one item per file.
5. For each file: `write_file` with the **full** converted content. Patching in place is impractical when changes touch dozens of prose blocks per file.
6. After all conversions: `wc -l` and a heading grep to verify line counts and section structure survived.

## Verification results

| File | Lines | Notes |
|---|---|---|
| 01_Atomic_Structure.md | 179 | matches original |
| 02_Periodic_Table.md | 186 | matches original |
| 03_Chemical_Bonding.md | 230 | matches original |
| 04_Intermolecular_Forces.md | 202 | matches original |
| 05_Stoichiometry.md | 233 | matches original |
| 06_Solutions.md | 266 | matches original |
| 07_Gases.md | 324 | matches original |

Line counts came out identical because the Thai-in-parens convention roughly preserves character counts. Spot-checked: YAML frontmatter intact, all `\ce{}` blocks intact, all `$...$` math intact, all `[[wikilinks]]` resolve.

## What I almost got wrong

- I almost translated the Thai phrase in the symbol column of Section 2 tables (`ประจุ $+1$` is a Thai-language label, not prose). Don't.
- I almost listed both languages as separate `###` headings. Don't — pick one, parens for the other.
- I considered using `patch` for the conversions. Switched to `write_file` after the first file because the changes touched ~30+ distinct blocks per file.

## Reusability

The user's Chemistry folder still has 13 more notes (topics 08–20) that follow the same Thai-narrative pattern. The Physics folder has 23 notes already in English narrative — but a future request to convert Biology/Business/Economics notes from Thai to English would use the same workflow with the same conventions.