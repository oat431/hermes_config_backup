# Naming-Drift Repair Playbook

Concrete drift patterns found in the `general-knowledge` vault (2026-08-20). These recur in the `swe-knowledge` vault and any vault that grew organically, so expect the same families.

## Pattern families (and the fix)

### 1. Space ↔ underscore / hyphen
Baseline overviews write human names (`Cooking and Nutrition`, `Factors, Multiples, and Number Theory`); content files use numbered snake_case (`01_Cooking_and_Nutrition`, `03_Factors_Multiples_and_Number_Theory`).
**Fix:** remap target to `NN_underscore` name, keep the human name as alias: `[[01_Cooking_and_Nutrition|Cooking and Nutrition]]`.

### 2. Number-prefix drift
Baseline links often drop or renumber the prefix the content file carries (`[[Animal Husbandry]]` vs `06_Animal_Husbandry`, `[[Atomic Structure]]` vs `01_Atomic_Structure`).
**Fix:** match on the stripped normalized name, then write the full numbered basename.

### 3. Fine-grained BOK → consolidated content
The baseline strand overview enumerates a *finer* taxonomy than the content actually holds. E.g. Religion BOK lists 18 concept areas (`01_Buddha_Biography` … `18_Other_Religions`) but `Social Studies/01 Religion/` holds 7 consolidated notes (`01_Buddhist_Principles`, `02_Buddhist_Ceremonies_and_Meditation`, …).
**Fix (do NOT fabricate the missing notes):** map several fine-grained links to one consolidated parent:
- `01_Buddha_Biography`, `02_Buddhist_History`, `03_Jataka_Tales`, `04_Four_Noble_Truths`, `05_Eightfold_Path`, `06_Five_Aggregates`, `07_Three_Marks_of_Existence`, `08_Karma_and_Rebirth`, `09_Dependent_Origination`, `10_Five_Precepts`, `11_Thirty_Eight_Blessings`, `12_Dhamma_for_Social_Harmony`, `13_Dhamma_for_Success`, `14_Six_Directions`, `16_Tipitaka` → `01_Buddhist_Principles`
- `15_Meditation_Practice`, `17_Buddhist_Ceremonies` → `02_Buddhist_Ceremonies_and_Meditation`
- `18_Other_Religions` → `03_Other_Religions`
Same shape in Civics/Economics/History/Geography: many `NN_<name>` links map to a smaller set of content notes.

### 4. Folder-name drift (lowercase/singular/underscore)
`Science/Advance/physic` (should be `Physics`), `Computer_Science`/`Earth_Science` (should be spaces).
**Fix:** `git mv` the folder (preserves history), then fix any `physic/`-style path references inside content that broke.

### 5. Cross-note wrong-number / stale-name links
Content notes link siblings by a stale or renumbered name (e.g. `[[01_Introduction_to_Computer_Science]]` → `01_Computational_Thinking`, `[[06_Organic_Chemistry]]` → `14_Organic_Fundamentals`, `[[05_Quantum_Mechanics]]` → `19_Quantum_Physics`).
**Fix:** explicit per-target map (these rarely auto-normalize cleanly).

### 6. Career cross-references to not-yet-built folders
`career/` overviews link `[[../doctor/Medicine - Overview]]`, `[[../pharmacist/Pharmacy - Overview]]`, `[[Psychiatrist]]`, `[[Diplomat]]`, etc. — those folders/notes don't exist.
**Classification:** genuine gaps (content not yet built), NOT drift. Flag in the report; don't invent them.

## The collision guard (non-negotiable)

Before ANY auto-remap, run `broken_links.py --collisions`. If a *target* normalizes into a collision group, never auto-rewrite it — a valid `[[17_Probability]]` must not be flipped to `19_Probability`. Build an explicit file-scoped map for collision groups instead. Groups seen:

- `probability`: `17_Probability`, `19_Probability`
- `human body systems`: `04_Human_Body_Systems` (Science/Fundamental), `13_Human_Body_Systems` (Science/Advance/Biology)
- `digital citizenship`: `12_Digital_Citizenship` (CS), `21_Digital_Citizenship` (Career&Tech)
- `sound`: `09_Sound` (Physics), `17_Sound` (Fundamental)
- `weather and climate`: `06_…` (Earth Science), `20_…` (Fundamental)
- `solar system and astronomy`: `09_…` (Earth Science), `21_…` (Fundamental)
- `การเขียนจดหมาย`: `05_…`, `14_…` (duplicate files, different content)

The general lesson: a *name-normalizing* remap is only safe when the normalized form is UNIQUE in the vault; when it isn't, the rewrite must be scoped to a specific source file or carry an explicit target.

## Verified numbers (for calibration)

- Vault: 573 md files (56 baseline + 517 content) across 11 top folders.
- Drift fixed: 316 BOK links + 111 content links + 3 folder renames + 11 prose paths.
- After repair: 24 remaining broken links, ALL genuine content gaps (missing notes/folders), zero drift.
