---
name: narrative-book-summaries
description: "Use when summarizing narrative/argument books into vaults."
version: 1.0.0
author: curator
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [books, summarization, obsidian, mermaid, markdown-style]
    related_skills: [oralita-book-sum-obs, obsidian, research-paper-summaries]
---

# Narrative Book → Obsidian Study Vault

## When to Use

Argument-driven books where each chapter is a self-contained essay with a thesis: big history, popular science, philosophy, case-study narratives. For technical/practice books, use `oralita-book-sum-obs` (the execution engine: extraction, manifest, delegation, verification) with its study templates. That skill is user-protected; this companion skill carries the narrative-book FORMATS the user has approved and the style rules that apply to everything generated. For research papers (single-file study notes with quote and number verification), use `research-paper-summaries`.

Signals: 10–20+ titled chapters with distinct arguments; the user asks to "plan the format first" because the book is "different from other books"; a prior narrative-book vault exists to mirror (e.g. `psychology_book/schema_therapy`).

## Approved Note Anatomy (user-approved 2026-09-03, Sapiens run)

One file per chapter, `NN_Title_With_Underscores.md`, plus `Book Title - Overview.md`:

- YAML frontmatter: `tags: [booktag, part-tag, 1-3 topic tags, history]` — no `title:` field.
- Source blockquote: `> *Source: <Title> by <Author> (<publisher, year>), Chapter N "<exact title>", PDF pp. A–B (printed pp. unknown)*`
- H1: `# NN: <Exact Chapter Title>` (colon, never em-dash)
- `## Key Idea` — the chapter's thesis + why it matters, 2–3 paragraphs (~250–350 words), mentor voice.
- `## The Argument` — bold-led bullets reconstructing the evidence spine in own words.
- `## Key Concepts` — `### Name` per durable concept: define + example + why it matters. The book's terminology.
- `## Memorable Quotes` — 2–4 short verbatim quotes, each `> "..." (PDF p. N)`.
- `## Connections` — `- [[Stem]]: one-line reason` wikilinks to sibling notes + the overview last. Colon separator, never em-dash.
- `## Takeaway` — one line worth remembering.

Full spec, per-section word budgets, and the Sapiens worked example: `references/narrative-note-anatomy.md`.

## Style Rules (embed from the start — user preferences)

- **No em-dashes in generated prose.** Use commas, colons, parentheses, or split sentences. En-dashes stay in page ranges (`PDF pp. 84–104`).
- **Verbatim quotes are sacred.** Never alter quoted punctuation, including short quoted fragments inside prose (skip them in any bulk punctuation edit).
- Mermaid node labels with special chars must be quoted (`A["text (parens)"]`); edge labels with special chars quoted as `-->|"label ()/"|`.
- Match the destination vault's naming/link conventions over any global rule — underscore stems are fine where the local reference vault uses them.
- Overview/MOC: chapter-map table grouped by part with PDF-page sources, one Mermaid argument map, reading paths (goal → start notes), 5–9 core ideas, honest footer with extraction limitations.

## Workflow

1. **Plan first when asked.** Inspect the PDF (pymupdf `get_toc()`, page count, text-layer vs OCR check), read 1–3 reference-vault notes, then present the concrete plan: per-chapter anatomy, citation scheme, file list. Confirm granularity and quote sections with the user before writing anything.
2. **Extract with page markers.** Insert a `[PDF p. N]` marker at every PDF-page boundary inside each chapter extract. Writers then attribute quotes from markers, and validation can check attribution mechanically. Verify chapter boundaries by reading head/tail text of each extract, not the TOC alone.
3. **Delegate in live-limited batches.** Query `delegation.max_concurrent_children` at run time. Every writer gets: extract path, staging path, format spec, an exemplar note, and the complete canonical link allow-list. A child's report is NOT proof — validate every staging file (frontmatter, source line, section order, quotes verbatim + page attribution, links) before promotion. Use `scripts/check_chapter_notes.py`.
4. **Promote, verify, spot-check.** Promote validated files, run the vault verifier, then spot-check 5+ factual claims per representative note against the source text (grep with normalized whitespace — extracts are line-wrapped, so phrase search must flatten whitespace first; PDF text layers also hyphenate across lines ("develop-\nment"), so also try the "- "-joined form before concluding a quote is absent).
5. **Compression pass (optional).** The user may ask for shorter notes after the first draft. Rules in `references/narrative-note-anatomy.md`.

## Mermaid Diagram Rubric

Add a diagram only when the chapter's structure IS a relationship:

- **Strong candidates:** cycles/feedback loops (luxury trap, capitalist circle), abstraction ladders (money), taxonomies (religion tree), branching futures (three paths), vicious circles as `stateDiagram-v2`.
- **Good candidates:** ontologies (objective/subjective/inter-subjective), imperial cycles, self-defeating prophecy (`stateDiagram-v2`), science↔politics↔economics loops, three-way alliances.
- **Skip:** plain lists, debates without a spine, psychological findings. Never force a sequence diagram; use `stateDiagram-v2` where the structure is genuinely stateful.
- Place each diagram inside the Key Concept it illustrates.
- After editing, verify: code fences balanced, square brackets matched, vault verifier passes.

## Pitfalls

- **Fuzzy patch can over-match.** A long `old_string` that partially matches may swallow a preceding sentence (observed: a patch deleted the opening sentence of a concept paragraph). Check every diff and restore immediately; prefer short unique anchors (heading lines) over long paragraph anchors.
- **patch escape-drift.** Do not backslash-escape double quotes in patch strings; plain quotes match plain quotes in the file. If a match fails with "Did you mean", re-grep the exact glyphs (apostrophes, dashes) before retrying.
- **Calibre/PDFDrive conversions have no folio numbers.** Scan for digit-only lines to detect printed page numbers; if absent, cite PDF pages and mark `printed pp. unknown` everywhere. Never invent printed ranges.
- **Endnote texts are usually absent from e-book extracts** — never assert footnote content.
- **Homo Deus (Sapiens sequel) is queued** in `F:/books/human_book/` — reuse this anatomy and the Sapiens vault as the format reference.

## Reference Map

- `references/narrative-note-anatomy.md` — full per-section spec, compression-pass rules, Sapiens case study incl. the 14-diagram map.
- `scripts/check_chapter_notes.py` — validates staging/vault notes: frontmatter, source line, H1, section order, verbatim quotes + page attribution, wikilink allow-list.