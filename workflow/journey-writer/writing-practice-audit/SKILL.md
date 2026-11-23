---
name: writing-practice-audit
description: Use when Panomete requests a writing audit or critique.
---

# Writing Practice Audits (journey-writer ✒️)

Class-level workflow for Panomete's writing-practice vault (`F:\obsidian_note\oralita_md\writing\`) and the LLM-as-auditor role agreed 2026-08-23 (POC validated by user; he returns for repeat audits).

## Vault layout — three-layer system

| Layer | Path | Content |
|-------|------|---------|
| Knowledge | `00_knowledge/` | Numbered guides (NN-Name.md): 00 types map · 01 review · 02 storytelling (8 structures incl. kishōtenketsu) · 03 media scripts · 04 wishing (+ TH↔EN register map) |
| Audit | `01_audit/` | One audit file per practice piece |
| Practice | `review/` `short_story/` `wishing/` | His drafts; live-file naming `YYYYMMDD-<title>.md` |

Fill-in templates live separately at `F:\obsidian_note\oralita_md\templates\writing\` (quick-note, review, short-story, media, wishing-template). Mirrors the fitness vault pattern (knowledge → audit → practice areas).

## The Auditor Contract (agreed, non-negotiable)

1. **Problems first, praise second** — never open with compliments
2. **Every problem cites quoted evidence** from the piece (line-level quotes); an audit without quotes is opinion
3. **Tag every finding** `[objective]` (violates the written framework) vs `[taste]` (you'd do differently) — taste can be freely rejected
4. **Minimum 3 specific weaknesses** even for good pieces; an all-positive audit is worthless by definition
5. **Never rewrite the piece** unless explicitly asked — the story/wish/review belongs to the writer
6. **Final say is always his**

## Beyond the writing-practice vault

The contract is not scoped to `writing/`. When he says "review this note" about a knowledge-vault note (curriculum, teaching, translation), the same order holds:

1. **Mechanical checks first** — links resolve, frontmatter fields present, no dead targets. They are objective and cheap; do them before judging prose. Link-repair procedure: `obsidian-vault-maintenance`.
2. **Then the prose** against the governing rule set — `kien-thai` for Thai prose; his own knowledge guides for drafts.
3. **Problems first**, each quoted, tagged `[objective]` / `[taste]`; his ear decides.

Language matters: **"refine" / "แก้ให้" grants permission to rewrite in place** — back up the file first, then edit. **"Review" / "audit" / "วิเคราะห์" does not** — report and wait. When refining, rewrite prose freely but leave structural claims (what a diagram asserts, what a table includes) alone; flag those as suggestions instead of changing them silently.

## Audit file placement & naming

`01_audit/yyyymmdd_[category]_<title>.md` — e.g. `20260823_review_00example.md`.

Frontmatter: `date`, `tags` ([audit, category]), `piece: "[[<practice file>]]"`, `auditor: journey-writer`.

Report shape (fill-in skeleton: `templates/audit-report.md`):
1. **Summary Judgment** — 2–4 sentences, honest overall call
2. **Skeleton Compliance** — table mapping piece against the relevant knowledge guide's steps (✅/⚠️/❌)
3. **Problems (cited)** — numbered, quoted, tagged
4. **What Works** — genuine strengths (after problems, never before)
5. **Fix Priority** — 3–4 concrete moves for the next draft

Audit against HIS knowledge guides (`00_knowledge/`), not generic writing advice — the rubric lives in his vault.

## Template-layer rules

- **Templates are EN-only language-neutral skeletons.** User explicitly declined TH duplicates (2026-08-23): structure transfers across languages; do NOT offer per-language template versions again.
- Culture/register specifics (Thai particles, elder honorifics, blessing stacks) live in the KNOWLEDGE layer (`04-Wishing-Note-Guide` register map), referenced by pointer from templates — not baked into template bodies.
- Media scripts exception that stays: format vocabulary (`INT./EXT.`, `V.O.`, B-ROLL) is English industry-standard always; spoken/dialogue content goes in the audience's language. This is craft correctness, not translation duplication.

## Pitfalls

- Identical practice filenames (`00_example.md` × N folders) make `[[wikilinks]]` ambiguous in Obsidian — encourage dated unique filenames from birth.
- ALWAYS `read_file` before overwriting any vault file (past data-loss incident in BG3 vault).
- Genre honesty: label pieces what they are (a reflective true essay filed under short_story is personal essay/memoir lane — fine, but say so).
- Facts about reviewed media split in two: verifiable public facts (cast, character names, runtime, release dates) CAN be checked via web_search against studio/Wikipedia sources — do it and report the result honestly (validated 2026-10-16 Whalefall audit); unverifiable plot claims stay the author's responsibility — note this once per audit if plot-heavy.
- Recurring root cause seen in POC audits: idea arrives before the specific (philosophy without person, thesis without counterargument). Probe for "one detail only this subject could have generated" in every audit.

## Exemplars

The three validated POC audits live in `writing/01_audit/20260823_{review,short_story,wishing}_00example.md` — match their depth and tone.
