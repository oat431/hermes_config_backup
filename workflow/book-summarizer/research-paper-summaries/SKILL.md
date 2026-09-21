---
name: research-paper-summaries
description: "Use when summarizing a research paper or technical report into Obsidian notes. Single-file or split-set workflows with quote, number, and style verification against the PDF."
version: 1.2.0
author: curator
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [papers, summarization, obsidian, arxiv, verification]
    related_skills: [narrative-book-summaries, oralita-book-sum-obs, obsidian]
---

# Research Paper → Obsidian Study Notes (Single File or Split Set)

## When to Use

A research paper, preprint, or technical report the user wants as ONE durable note. A paper is one coherent unit, so the default output is a single study note written by one writer in one pass. This is a different shape from book vaults.

| Source | Skill |
|---|---|
| Research paper / preprint / tech report (one note) | **this skill** |
| Technical book or multi-file source set (vault) | `oralita-book-sum-obs` (user-protected) |
| Narrative/argument book (per-chapter vault) | `narrative-book-summaries` |

**Large reports split into sets.** Rule confirmed with this user on a 59-page technical report: papers/guides up to about 25–30 pages get ONE file; large reports (60+ pages, with results/appendices taking roughly half) get a **numbered set in a subfolder**. The user's preferred split for big technical reports: content files (methods and story) + one tests file + an overview:

- `00_Overview.md` — MOC: lineup table, headline numbers, file map, reading paths.
- `01_...md` and up — content files in the report's own order, method-focused, pointing to the tests file for full numbers.
- an evaluation file (for example `04_Evaluation.md`) — the tests file: ALL formal evaluation material consolidated (benchmark tables, human-evaluation win rates with representative cases, case studies, appendix test sections).

Present the split as a table (file / covers / source pages) in one clarify when a big report first appears; afterwards apply the convention. Full pattern and worked example: `references/large-report-splits.md`.

Default landing zone for this user's paper summaries: `F:/obsidian_note/oralita_md/daily-paper/` with a kebab-case filename (e.g. `deepseek-llm-scaling-with-longtermism.md`). Confirm destination and depth the first time a new paper or format comes up; afterwards apply the established convention and state it in the report instead of re-asking. oralita_md and ai-knowledge are separate Obsidian vaults, so cross-vault `[[wikilinks]]` do not resolve; reference other vaults as plain code paths.

## Always-On Rules

- **Feasibility first, from inspection.** When the user asks "can this be one file / which approach", answer from the actual PDF: page count, a content breakdown (main body vs references vs appendix), a one-file verdict, and the proposed note sections. Never answer from the abstract or from vibes.
- **Direct synthesis, no delegation.** One file has nothing to parallelize, and even split sets (4–6 files) are written directly for voice consistency. Read the full extract, write the note(s), verify. Delegation stays for chapter-level book vault runs.
- **Confirm shape decisions in ONE clarify call** the first time a new paper or format comes up: destination, granularity (single file vs split set), and depth. Depth options: study note ~1,800–3,500 words (recommended for this user), brief ~1,000, deep dive ~5,000+.
- **Citations:** establish whether printed page = PDF page (check page footers in the extraction) and state the convention in the note header. When they differ (journal articles, old scans), compute the offset from the footers (printed = PDF page + k), record it in the note header AND the manifest row, and cite printed pages in the body. Cite pages from the source only; never invent page numbers or quotes.
- **Version fidelity:** cite the exact version matching the PDF (page-1 stamp reads `arXiv:<id>vN`). Summarize what that version says, not the latest revision.
- **Quotes verbatim and page-attributed; everything else own words.** Short quotes only, never long passages.
- **Style (standing user preferences):** no em-dashes in prose (use commas/colons/parens); en-dashes only in page ranges (`pp. 8–9`); English; label your own additions `(synthesis)`; kebab-case filename in oralita_md.
- **Report real counts at the end:** quotes verified, number spot-checks, hash match, and honest limitations (including what was deliberately not summarized).

## Workflow

### 1. Inspect and decide the shape

```python
import pymupdf
doc = pymupdf.open(pdf_path)
print(doc.page_count, doc.get_toc())      # page count + section map
print(doc[0].get_text()[:1200])           # title page: version stamp, abstract
```

- Sample first/middle/last pages to confirm a real text layer. LaTeX PDFs extract clean; scans with a usable (even noisy) text layer can go straight through with `--ocr-tolerant` verification; re-OCR via `ocr-and-documents` only when there is no text layer or it is unusably corrupt.
- Build the content breakdown: main body pages (source of the summary), references pages (skip for summary value), appendix pages (substance vs boilerplate).
- Pin section boundaries from page text heads: `get_toc()` entries can be one page off; the first line of a page is ground truth.
- Present breakdown table + one-file verdict + proposed sections, then stop for the user's destination/depth decisions.

### 2. Preflight

- Confirm the target path and check the target file does not already exist.
- Workspace outside the vault: `tempfile.gettempdir()/oralita-book/<slug>/`, with a light `manifest.json` (source metadata, page ranges, one output row, status).
- Nothing except the final note may land in the vault folder.

### 3. Extract with page markers

```python
with open(out, "w", encoding="utf-8") as f:
    for i in range(start - 1, end):        # inclusive, 1-based pages
        f.write(f"\n\n===== [PDF p. {i+1}] =====\n\n")
        f.write(doc[i].get_text())
```

- Extract the main body (title page through conclusion) as `extract_main.md`; extract appendix substance sections separately; inventory remaining appendix pages as first-lines only.
- Tables re-order in the text layer: rebuild table values deliberately from the extract cells and spot-check them later; never trust extracted row order.

### 4. Write the note (direct synthesis)

Follow `templates/paper-study-note.md` (for split sets, reuse this anatomy per file). Anatomy:

1. Frontmatter: `title`, `tags`, `created`, `source` (fit the destination vault's convention; oralita_md uses title/tags/created, add `source`).
2. H1 + source blockquote: full citation, page convention, coverage note.
3. `## TL;DR` — 2–3 paragraphs in mentor voice: what it does, the load-bearing findings, why it matters.
4. `## Why This Paper Matters` — context, what it changes.
5. `## The Paper at a Glance` — section / pages / what-it-delivers table.
6. Body sections in the paper's own order. Formulas restated in inline code with the original constants (`M_opt = 0.1715 · C^0.5243`); condensed results tables (representative rows, not every table); at most one Mermaid diagram, only for a real relationship.
7. `## Limitations and Future Work` — the paper's own section; keep it.
8. `## Practitioner Takeaways (synthesis)`.
9. `## Memorable Quotes` — 3–4 verbatim quotes as `> "..." (p. N)` (the checker parses this exact line shape).
10. `## Related` — source PDF path, arXiv URL, related vault paths as code, not wikilinks.
11. Footer: date, version summarized, verification statement.

### 5. Verify, then promote

Stage the note outside the vault, run the checker, fix findings, then copy into the vault and compare hashes:

```
python scripts/verify_paper_note.py --note <staged.md> --source <extract.md> --numbers "0.5243,5.8316,89.8" [--scan-all] [--quotes extra.txt] [--allow-links stem1,stem2]
sha256sum <staged.md> <vault.md>   # must match
```

The checker verifies: quotes verbatim (whitespace-normalized, split-quote aware, retried with hyphen line-breaks joined), number checks with variants (trailing punctuation stripped, thousands separators and inter-digit spaces tolerated; optional --scan-all over every token), zero em-dashes, frontmatter keys, balanced fences, wikilink allow-list (--allow-links), word count. For scanned PDFs pass `--ocr-tolerant`: ligatures map to ASCII and quotes/numbers are re-compared with all whitespace and ASCII hyphens stripped, which survives merged-word layers. Treat a MISS as "verify manually", then repair. Update the manifest row to written with the hash; report only after hash equality.

## Pitfalls

- **A scratch script named after a stdlib module breaks pymupdf.** `inspect.py` shadows stdlib `inspect`, and pymupdf dies at import with a misleading "partially initialized module / circular import" error. Name scratch scripts with a prefix (`pdf_inspect.py`).
- **Split quotes across page breaks.** The PDF text layer can place a floating figure caption between the two halves of a sentence that spans a page break, so a valid quote fails a naive grep. Verify both fragments and confirm the only text between them is the caption/footer/page marker; for high-stakes quotes cross-check the arXiv HTML (`curl -sL https://arxiv.org/html/<id>vN | grep ...`). Never alter or drop the quote to make the check pass.
- **PDF outline numbers can be off by one.** Verify each section's start page against the page's own text, not the `get_toc()` entry.
- **References and boilerplate appendix pages get a page range, not a summary.** Summarize appendix pages only where they carry substance; list the rest in the coverage note.
- **The number spot-check list is the extraction's tripwire.** Keep a list of the note's load-bearing numbers (fitted constants, dataset sizes, benchmark scores) and grep them against the extract; extraction garbling shows up here first.
- **Separate Obsidian vaults do not share wikilinks.** Inside a note in oralita_md, `[[ai-knowledge/...]]` will not resolve. Use plain code paths for cross-vault references.
- **Hyphenated line breaks break verbatim quote and number checks.** PDF text layers split words across lines ("develop-\nment", "Qwen3-\nCoder"); whitespace flattening is not enough. On any MISS, retry with "- " removed (joined form) before concluding anything; for hyphenated tokens also try the spaced form (`Qwen3-Coder` matches source `Qwen3- Coder`).
- **Scanned/OCR PDFs need artifact-tolerant quote matching.** Old scans (PDF 1.3-era conversions, no TOC, first-page sample full of ligatures like ﬁ/ﬂ or merged words like "Eventhoughwehave") break whitespace normalization: words merge and characters corrupt ("my be" for "may be", "built-ln" for "built-in", "i~s" for "is"). Use `--ocr-tolerant` (ligatures to ASCII, then compare with ALL whitespace and ASCII hyphens stripped); pick quotes from clean passages of the text layer and paraphrase anything too corrupt to verify verbatim. A quote you cannot verify against the layer is not quotable.
- **Scans often do not print their own bibliographic data.** When venue/year/DOI are absent from the PDF, complete the citation from the ACM DL / DBLP record, keep the page range as the scan's own footers show it, and mark the completed fields as externally verified in the note footer and manifest. Label non-source body content (e.g. "the language became CLU") with an explicit (external) marker, distinct from (synthesis).
- **Number checks need variants.** Tokens pick up trailing punctuation ("4.32."); "50,000" may be "50 000" in the extract. Strip trailing punctuation, remove thousands commas, and on the source side remove inter-digit spaces. A full-token scan (--scan-all) catches transcription typos a hand-written list misses.
- **The zero-em-dash gate covers titles and link lists too.** Em-dashes sneak in as "Title — Subtitle" and in Related bullets (wikilink then em-dash then reason); use ":" as the separator in both. Prefer quotes without em-dashes so the gate stays clean; a verbatim quote that contains one keeps its punctuation.
- **Sibling papers link both ways.** When a companion summary lands, patch the older note's Related section to wikilink the new note (read the file first, minimal patch, announce it in the report) and keep staged copies plus manifest hashes in sync so run records stay truthful.

## Reporting

Close with the real numbers: output path and word count, coverage (what was summarized, what was skipped), verification results (quotes checked, numbers checked, hash), and honest limitations. The user values verified counts over optimistic summaries.

## Files

- `templates/paper-study-note.md` — fill-in starter with the approved anatomy.
- `scripts/verify_paper_note.py` — staged-note checker: quotes (hyphen-break and split-quote aware), number checks with variants, em-dash/fence/frontmatter/wikilink gates, `--ocr-tolerant` for scanned PDFs (ligature map + whitespace/hyphen-stripped comparison). A safety net, not a substitute for reading the note.
- `references/large-report-splits.md` — the numbered-set pattern for big technical reports, with the worked example.
