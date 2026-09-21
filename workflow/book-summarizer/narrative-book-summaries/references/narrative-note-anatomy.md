# Narrative Note Anatomy — Full Spec + Sapiens Case Study

## Per-section budgets (full-length version)

| Section | Budget | Rule |
|---|---|---|
| Key Idea | ~250–350 words | Thesis + why it matters; mentor voice, no index-speak |
| The Argument | 4–6 bold-led bullets | 2–4 sentences each; evidence spine in own words; preserve reframes ("x is actually y") |
| Key Concepts | 3–7 `###` blocks | define + chapter evidence/example + why it matters later in the book |
| Memorable Quotes | 2–4 blockquotes | verbatim from extract, `(PDF p. N)` from markers |
| Connections | 2–6 bullets | only real callbacks/foreshadowing; overview link last |
| Takeaway | 1 line | optionally bold-led |

## Compression-pass rules (when the user asks for shorter notes)

- Target ~1,100–1,400 words per note.
- Key Idea: keep full. The Argument: compress to 4–6 bullets. Key Concepts: keep the 3–4 most load-bearing. Quotes: cut to 2–3. Connections + Takeaway unchanged.
- Trim first, never pad. Expect natural variance (900–1,550 words is fine; don't equalize artificially).

## Sapiens case study (approved 2026-09-03)

- Source: calibre-converted PDF, 439 pages, 4 parts × 20 chapters + Afterword; no printed folio numbers → all citations PDF pages, `printed pp. unknown`.
- 21 files: 20 chapter notes + `Sapiens - Overview.md`; underscore stems (local convention); part tags: cognitive-revolution / agricultural-revolution / unification-of-humankind / scientific-revolution.
- Extraction: pymupdf per-chapter ranges from TOC, `[PDF p. N]` marker per page; boundaries verified via head/tail text.
- Validation: `check_chapter_notes.py` passed all 20 notes (quotes byte-verbatim, page attribution exact); claim spot-check on ch05 = 18/18 matched the source (search with whitespace-flattened phrases — extracts are line-wrapped).
- Em-dash purge: 497 em-dashes replaced (362 → commas, 21 headings → colons, 110 connection bullets → colons, 3 mermaid labels → colons, 1 quoted fragment kept to source en-dash). Guard: blockquote lines and fenced blocks exempt.

### Diagram map (14 added; one per qualifying chapter)

| Ch | Diagram | Type |
|---|---|---|
| 02 | information → gossip (150 cap) → fiction → imagined orders → mass cooperation | flowchart |
| 05 | luxury trap cycle (wheat → camps → villages → population → no way back) | flowchart LR |
| 06 | 3-storey ontology: objective / subjective / inter-subjective | flowchart TD |
| 07 | brain limits → Sumerian writing → retrieval problem → bureaucracy → binary | flowchart LR |
| 08 | vicious circle: accident → stigma → exclusion → "proof" → stigma | stateDiagram-v2 |
| 10 | money ladder: barley → shekel → coin → electronic data → trust | flowchart LR |
| 11 | imperial cycle: conquest → standardisation → assimilation → new "they" | flowchart LR |
| 12 | religion taxonomy: polytheism / monotheism / dualism / natural-law / humanism | flowchart TD |
| 13 | level-two chaos: forecast → reaction → course change → prediction fails | stateDiagram-v2 |
| 14 | science ↔ politics ↔ economics feedback loop | flowchart LR |
| 15 | science ↔ empire ↔ capital triangle | flowchart TD |
| 16 | capitalist magic circle: credit → investment → growth → profits | flowchart LR |
| 17 | knowledge loop: shortage → research → new resource → growth | flowchart LR |
| 20 | natural selection → intelligent design → three paths → post-Homo sapiens | flowchart TD |

Overview keeps one argument-map flowchart (four revolutions). Skipped: ch01 (species list), ch03 (forager debates), ch19 (psychological findings) — prose serves better.

## Overview/MOC shape

- `What Is This?` — the book's argument in 2–4 sentences + why it matters
- Chapter Map — table grouped by part: `[[Stem]] | thesis in one line | Source (PDF pp.)`
- Mermaid argument map (one, not several)
- Reading Paths — table: goal → start notes (full order, fast tour, thematic lenses)
- Core Ideas — the 5–9 load-bearing ideas with chapter links
- Footer: honest generation note (counts, citation scheme, extraction limitations)