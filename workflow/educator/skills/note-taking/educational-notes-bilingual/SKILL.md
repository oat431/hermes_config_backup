---
name: educational-notes-bilingual
description: "Convert Thai notes into bilingual English Obsidian format."
platforms: [linux, macos, windows]
tags: [obsidian, notes, bilingual, thai-english, ipst, curriculum, conversion, physics, chemistry, math-sci, translation]
triggers:
  - User asks to convert or translate Thai-narrative educational notes into English while preserving structure
  - User mentions matching the style of an already-converted subject (e.g., "matching Physics style")
  - User is processing a batch of curriculum notes (e.g., "convert notes 14-20")
  - The vault contains Thai IPST (สสวท.) STEM curriculum notes with a 5-section template
---

# Bilingual Educational Notes Conversion

Convert Thai-narrative educational notes into English-narrative bilingual format while strictly preserving the original's structure. The source is the Thai IPST (สสวท.) STEM curriculum — Physics (ว302), Chemistry (ว311-313), Biology, Mathematics, etc. Each source note follows a strict 5-section Obsidian template; the conversion translates narrative prose and section headings into English but keeps Thai terms visible (in `(...)` parens) and keeps Section 2 (terminology table) entirely in Thai.

**This skill is for whole-file conversion of an existing note's narrative language. It is NOT for synthesis from external sources** (use `obsidian-note-authoring`) and NOT for gap analysis or BOK creation (use `educational-content-authoring`).

## Linked Files

- **`references/ipst-bilingual-style-guide.md`** — Concrete before/after pattern examples from the Chemistry 14-20 conversion batch. 15 numbered patterns covering Thai section headings, table cells, equation-containing paragraphs, and tricky comparative cases. Refer to this when the SKILL.md style guide is ambiguous.
- **`templates/bilingual-educational-note.md`** — Starter template for new bilingual educational notes. Copy and modify; don't write from scratch.

## When to use this skill

- User has a batch of Thai-narrative Obsidian notes that need conversion to English (e.g., "convert Chemistry topics 14-20 from Thai narrative to English narrative")
- An already-converted subject exists (e.g., Physics) whose style the new notes must match
- The source notes have YAML frontmatter, a fixed 5-section structure (Course Coverage / Key Terminology / Key Concepts / Common Problem Types / Cross-Links), LaTeX formulas, and `\ce{}` chemical equations
- Thai technical terms should remain visible to bilingual Thai-student readers — translate to English but keep Thai in `(...)` parens after

**Do NOT use this skill when:**
- The source note uses prose-only narrative without the 5-section template (use general translation)
- The user wants a fresh note synthesized from a textbook or article (use `obsidian-note-authoring`)
- The note is English-only (no-op)
- The user wants Thai→Thai language polishing or stylistic rephrasing (no skill needed)

## Workflow

### Phase 1: Anchor the style with a reference file

Before touching the target files, **read at least one already-converted reference note from the same curriculum family**. For Chemistry, read a Physics note (e.g., `physics/14_Electromagnetic_Induction.md`). For new subjects, read the most recently converted note in the same vault.

Why: the user's preferred style is empirically defined by what they've already approved. Skip this step and you'll invent a different style and the user will catch the inconsistency on the first read.

Specifically extract from the reference:
- Title format: `# English Term — Thai Term` (em-dash separator, NOT hyphen, NOT colon)
- Overview prose: English-first with Thai `(...)` parens after each Thai term
- Section heading format: `### 3.1 English Title` (Thai term may remain as a sub-heading ONLY when the section is purely a Thai-anchored reference like `### ม.6 (ว313)`)
- Whether the "Scope" column in Course Coverage is English or Thai
- Whether the "Symbol/Notes" column in Terminology keeps Thai glosses

### Phase 2: Batch-read all source files

For batches of 5+ files, issue parallel `read_file` calls in a single assistant turn. This is critical for context budget — each Thai-narrative note is typically 5-10 KB and reading 7 in serial would burn unnecessary round-trips.

### Phase 3: Convert each file with `write_file`

For each source file, produce a converted version via `write_file`. The conversion is a **language swap on prose, not a rewrite**. Preserve everything that isn't prose:
- ✅ YAML frontmatter unchanged (tags, source, created, course_codes)
- ✅ LaTeX formulas (`$\ce{...}$`, `$...$`) unchanged
- ✅ `\ce{...}` chemical equations unchanged
- ✅ Tables preserved (only cell text changes if Thai prose)
- ✅ Wikilinks `[[filename]]` unchanged
- ✅ Quote blocks unchanged
- ✅ Cross-link `[[filename]] — description` paths unchanged; only translate the description
- ✅ Numbered subsections (`3.1`, `3.2`) unchanged
- ❌ Body prose: translate Thai → English
- ❌ Section headings: translate Thai → English (Thai term may stay as a sibling heading)
- ❌ List bullets that are pure Thai prose: translate
- ❌ Numbered steps in problem solutions: translate

### Phase 4: Convert in batches of parallel `write_file` calls

When the batch is 4+ files, issue the `write_file` calls in a SINGLE assistant turn after reading. This is the highest-leverage pattern — converting 7 files serially takes 14+ round-trips; converting 7 in one turn takes 2 (read + write).

### Phase 5: Verify with `wc -l`

After writing all files, run `cd "F:/path/to/folder" && wc -l *.md` to confirm line counts are within ±10% of the originals. A 30% drop means you accidentally stripped content; a 30% jump means you accidentally added paraphrasing that wasn't in the source. The conversion should be roughly length-preserving.

## Style Guide (specific to this user)

### Title format
```
# English Term — Thai Term
```
- Em-dash `—` (U+2014), NOT hyphen, NOT colon
- English first, Thai second
- Both halves preserved — the Thai half is the bilingual anchor

### Quote blocks
Preserve verbatim. The author's quoted attribution must stay exactly as-is.

### Overview paragraphs (post-quote, pre-`##`)
Convert to English narrative. Each Thai technical term gets its own `(...)` paren on first introduction. Example:

**Before (Thai):**
> Organic chemistry เป็นสาขาของเคมีที่ศึกษาโครงสร้าง สมบัติ องค์ประกอบ และปฏิกิริยาของสารประกอบคาร์บอน...

**After (English-bilingual):**
> Organic chemistry (เคมีอินทรีย์) is the branch of chemistry that studies the structure, properties, composition, and reactions of carbon compounds (สารประกอบคาร์บอน). It forms the foundation of living systems, the chemical industry, pharmaceuticals, and materials science.

### Section 1 | Course Coverage
- Heading: `## 1 | Course Coverage`
- Sub-heading: `### ม.6 (ว313)` — leave the Thai grade-band notation AS-IS (it's a curriculum code, not translatable)
- Table column "Scope": translate to English
- Table column "Key Skills": translate to English

### Section 2 | Key Terminology
**Leave the entire table in its Thai | English | Symbol/Notes form.** This is the reference glossary — its purpose is to show Thai students the Thai term they know alongside the English term. Translating the Thai column breaks the bilingual contract.

Light improvement only: the "English" column may have parenthetical Thai glosses where useful (e.g. `Carbon | C; atomic number 6, 4 valence e⁻`). Don't add new Thai terms to a row; just lightly clarify the English cell if the original was already short.

### Section 3 | Key Concepts
- Convert section sub-headings: `### 3.1 ความพิเศษของคาร์บอน` → `### 3.1 The Special Properties of Carbon`
- Body prose: translate, with Thai `(...)` parens on key terms
- LaTeX equations and `\ce{...}` blocks: preserve verbatim
- Bullet items: translate the prose; preserve any formula/formula-symbol items
- Subsubsection headings with both English and Thai: convert to `#### (a) Polyethylene (PE)` style with Thai dropped from the heading (it's in the prose if needed)
- Parenthesized Thai like `(ต่อในบทถัดไป)` becomes `(continued in the next note)` if it carries meaning, otherwise drop

### Section 4 | Common Problem Types
- `### Type N: <problem type>`: translate the title
- The problem prompt after `>`: translate; preserve Thai in `(...)` for problem-domain terms when relevant
- The `**Solution:**` body: translate
- Equations and chemicals: verbatim

### Section 5 | Cross-Links
- Wikilinks `[[filename]]`: unchanged
- `[[filename]] — Thai description` becomes `[[filename]] — English description`
- Order preserved

## Worked Example: Heading Conversions

| Source (Thai) | Output (English-bilingual) |
|---|---|
| `# Organic Chemistry Fundamentals — พื้นฐานเคมีอินทรีย์` | (unchanged — title is already bilingual) |
| `### 3.1 ความพิเศษของคาร์บอน` | `### 3.1 The Special Properties of Carbon` |
| `### 3.2 ประเภทของไฮโดรคาร์บอน` | `### 3.2 Classes of Hydrocarbons` |
| `### (1) อัลเคน (Alkanes) — CₙH₂ₙ₊₂` | `### (1) Alkanes (อัลเคน) — CₙH₂ₙ₊₂` |
| `- **Tetravalent (เตตระวาเลนต์):** C มี 4 valence electrons...` | `- **Tetravalent (เตตระวาเลนต์):** C has 4 valence electrons...` |
| `$$\ce{CH4, C2H6, C3H8, C4H10, ...}$$` | (unchanged — LaTeX) |
| `- [[14_Organic_Fundamentals]] — โครงสร้างพื้นฐาน` | `- [[14_Organic_Fundamentals]] — Basic structures` |

## Pitfalls

1. **Don't skip reading a reference note first.** Without anchoring to a converted reference, you'll invent a different bilingual style and the user will spot the inconsistency immediately. The reference note IS the spec.
2. **Don't translate Section 2 (terminology table).** The whole purpose is bilingual anchoring — Thai students need to see the Thai term they know. Translating the Thai column breaks the educational contract.
3. **Don't paraphrase or restructure while translating.** The conversion is a language swap, not a content rewrite. If a heading is `### 3.1`, keep `### 3.1`. If a bullet has three items, keep three items. Compression during translation introduces factual drift and the user will read both versions side-by-side.
4. **Don't use colons (`:`) where the reference uses em-dashes (`—`).** Em-dash is the user's chosen separator for title `English — Thai`. Read the reference file to see if em-dashes are used elsewhere; some users apply them broadly in prose too. When in doubt, match the reference.
5. **Don't drop `(continued in the next note)` and similar Thai fragments silently.** If the Thai carries no English meaning (like `(ต่อในบทถัดไป)`), translate it to `(continued in the next note)`. If you think it's redundant, convert it anyway — the source had it for a reason.
6. **Don't change YAML frontmatter values.** Tags, source string, course_codes, created date — all unchanged. The user maintains them manually.
7. **Don't touch `\ce{...}` chemical equations.** They are exact ChemDraw-style notation and any alteration changes the chemistry. Same for `\Delta`, `\leftrightarrow`, `\rightarrow`, subscripts, and LaTeX environments like `{aligned}`.
8. **Don't reorder Cross-Links.** The user may have a preferred ordering (prerequisite → dependent → related); preserve it exactly.
9. **Don't read source files one at a time when there are 5+ files.** Read them all in parallel in one assistant turn. Same for `write_file`.
10. **Don't forget to verify with `wc -l`.** If your converted file is 30% shorter or longer than the source, you've either stripped content or added paraphrasing. Both are regressions.
11. **Don't write "AI-style" English.** Don't add connective phrases ("It is worth noting that..."), don't soften ("It's important to note..."), don't editorialize. Match the reference note's prose register.
12. **Don't translate proper nouns that already cross languages unchanged**: `IPST`, `สสวท.`, `B.E. 2551`, `ว313`, `ม.6`. These are curriculum codes — leave them.
13. **Don't translate credit and course codes in prose:** leave `ใน ว302 Semester 2`, `ในวิชา ว313`, `ม.6 (ว313)` intact — they're identifiers, not prose.
14. **On F:\ drives, use MSYS forward-slash paths in terminal and quoted Windows paths elsewhere.** `cd "F:/obsidian_note/..."` works in bash; `F:\...\...` works in `read_file` / `write_file` / `search_files`. The two path styles are equivalent, just route through different tools.
15. **On F:\ drives, `search_files(target='files')` returns silently empty; `search_files(target='content')` returns IO error.** Prefer `ls` via `terminal` for file listing on F:\ drives, and `find` via `terminal` for batch enumeration. This is a persistent environment quirk on this Windows host's MSYS terminal — don't retry with different slash styles.

16. **Don't use `search_files(target='files')` on F:\ drives — it returns empty.** Use `terminal` with `ls` or `find` to enumerate files. `search_files(target='content')` may also fail with IO errors on F:\ drives. This is a persistent environment quirk on this Windows host.
17. **Don't convert notes without reading an already-converted reference first.** The user's preferred style is empirically defined by what they've already approved (e.g., Physics for Chemistry, or the most recent conversion for new subjects). Skip this anchoring step and you'll invent a different style.
18. **Don't convert ASCII-art flowcharts or diagrams during bilingual conversion — flag them for a separate mermaid-enrichment pass.** ASCII art with arrows (`↓`, `→`) should be converted to mermaid `flowchart` diagrams in a follow-up task, not during language conversion. Mermaid rules: use `flowchart` (not `graph`), no `()` in labels, no `"1."` dots, no `&`.

## Verification

After converting each batch:
1. `wc -l` on source vs converted — should be within ±10%
2. `grep -c '\\ce{' source_file.md` vs converted — should be identical (equation preservation)
3. `grep -c '\[\[' source_file.md` vs converted — should be identical (wikilink count preservation)
4. Spot-check the first 25 lines of 1-2 files to confirm the title, quote, and overview match the reference style

## Related skills

- `obsidian-note-authoring` — use when synthesizing a new Obsidian note from external source material (books, articles, transcripts)
- `educational-content-authoring` — use when running gap analysis against the IPST curriculum or building Body-of-Knowledge overviews
- `obsidian` — basic Obsidian CRUD (read, list, search, append)
