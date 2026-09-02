---
name: multilingual-note-conversion
description: Translate bilingual educational notes between languages.
---

# Multilingual Note Conversion

Translate educational notes from one natural language to another while preserving every structural element. Use when the user asks to "convert", "translate", or "rewrite" notes that exist in two languages (e.g. Thai narrative + English terminology tables), or to localize technical material between languages.

## When to use

- The user has notes where one language carries the prose and another carries the technical terms, and they want a single-language version (or a flipped version with the other language as primary).
- The user asks for a conversion to "match [reference file] style".
- The source contains YAML frontmatter, LaTeX/MathJax, code-fenced chemistry (`\ce{}`), mermaid, wikilinks, and tables — all of which must survive intact.
- Common context: Thai IPST curriculum notes (ว301/ว311/ว312) being converted to English narrative.

## When NOT to use

- The user wants to translate a casual document with no technical structure (use a generic translation tool).
- The user wants to create new notes from source material — that's `obsidian-note-authoring`.
- The user wants to reorganize/merge/split notes — that's `obsidian-vault-restructuring`.

## Workflow

### 1. Establish the target style

Read the reference file the user points to (e.g. a "Physics style" sample). Note its narrative voice, sentence rhythm, and how it handles bilingual terminology. If no reference is provided, default to academic English narrative with source-language technical terms in `(...)` parentheses on first mention.

### 2. Inventory the source

Before writing anything, read every source file end-to-end. Note the consistent sections across files:
- YAML frontmatter (preserved verbatim)
- `## 1 | Course Coverage` (Scope / Key Skills table — translate prose, keep technical terms in parens)
- `## 2 | Key Terminology` (Thai–English bilingual table — usually preserved as-is)
- `## 3 | Key Concepts` with numbered subsections
- `## 4 | Common Problem Types`
- `## 5 | Cross-Links` (preserve wikilink targets; translate trailing descriptive text)

### 3. Plan and track

Build a todo list with one item per file. Mark them sequentially as you convert each.

### 4. Convert file by file

For each file, use `write_file` with the **complete** converted content (do not patch in place — the changes are too extensive). Preserve verbatim:

- YAML frontmatter (every tag, source line, course code)
- All heading levels and their order (`#` → `##` → `###`)
- All tables' column structure; only translate cell content
- All code blocks (`\ce{}`, `$LaTeX$`, `mermaid`, etc.)
- All wikilink targets (`[[path]]`); translate only the trailing description text
- Blockquote epigraphs
- Horizontal rules

Translate or reshape:

- The intro paragraph(s) below the title — English narrative with source-language technical terms in `(...)` parens on first mention.
- `## 1` Scope column: English prose with Thai technical terms in parens. Key Skills column: fully English.
- `## 3.x` subsection headings — English primary. Add the source-language heading in parens when informative (e.g. `### 3.1 Structure of the Periodic Table (โครงสร้างตารางธาตุ)`).
- All body prose — target-language narrative.
- `## 4` problem-type headings — translate; keep example chemistry intact.
- `## 5` Cross-Links — translate the trailing description after each wikilink target.

### 5. Verify

After all conversions:

- Confirm line counts match the originals (translation should be roughly length-neutral).
- Spot-check 2–3 files for: YAML intact, headings hierarchy intact, all `\ce{}` and `$...$` blocks intact, all wikilinks still resolve.
- Confirm column structure in every table matches the original.

## Pitfalls

- **Do not translate chemical formulas.** `\ce{CO2}`, `\ce{^35_17Cl}`, `$Z_{eff}$`, etc. are language-agnostic. Same for chemical symbols in cell text.
- **Do not translate symbol annotations in tables** like `$p^+$, ประจุ $+1$`. The Thai phrase there is a label, not prose.
- **Section 2 terminology tables** (Thai ↔ English) are usually already the right format — leave them alone unless the user explicitly asks otherwise.
- **Wikilink targets are paths, not prose.** Translate only the trailing description text, never the bracketed path.
- **Bilingual section headings are usually redundant** after conversion. Don't list both languages as separate headings; pick the target-language one and put the source in parens.
- **Section 1 Scope cells get partial translation** — prose becomes English, technical Thai terms stay in `(...)`. The Key Skills column goes fully English.
- **The first mention of a technical term** in body prose gets the source-language form in `(...)` parens; subsequent mentions can be target-language only.
- **`write_file` overwrites the entire file.** Don't try to patch — there's too much changing.
- **Line-count drift is a sanity check.** If your output is 30% longer or shorter than the source, you've over- or under-translated somewhere.

## Class-level note

This skill generalizes beyond Thai↔English. The same workflow applies to any bilingual technical/educational document where structure (formulas, code, tables, cross-references) must survive translation. Adjust the bilingual parens convention to whatever pair is in play (e.g. Japanese→English, Spanish→English, German→English for technical curricula).

## Reference

- `references/thai-to-english-ipst-case-study.md` — worked example converting 7 Thai-narrative IPST Chemistry notes to English narrative matching a pre-existing Physics style reference. Includes the specific heading conventions, table-cell patterns, and verification results.