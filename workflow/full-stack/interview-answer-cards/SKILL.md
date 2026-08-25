---
name: interview-answer-cards
description: Convert study notes into spoken interview answer cards.
---

# Interview Answer Cards

Convert the user's structured question lists / study notes (typically under
`F:\obsidian_note\interview-preparation\<company>\`) into drill-ready **answer cards**:
short spoken-style answers sized for verbal rehearsal, placed in a sibling `note/` folder
inside the vault.

## Trigger
- User asks for "answer cards" / "answer notes" for interview questions or study notes.
- User points at a folder of knowledge-gap / study-plan notes and wants reviewable answers.

## Workflow
1. **Read the WHOLE scope first.** List every note in the target folder
   (`search_files target=files`) and read all of them — PLUS the cross-referenced files
   they wikilink to (drill-question lists, personal scripts/STAR stories). Answers must be
   consistent with the user's confirmed-facts scripts; never invent personal experience.
2. **One answer card per study note**, named `Answers_NN_<Topic>.md` in the `note/`
   subfolder of the study-plan directory. Start from `templates/answer-card.md`.
3. **Index note** `00_Answer_Cards_Index.md` in the same folder: source-note → card table,
   drill-question → card map, and a scripts cross-reference (personal-story answers point
   to the Scripts file, they are NOT duplicated into cards — one source of truth).
4. **Backlink**: append a short section with `[[wikilink]]` to the index in the original
   study-plan overview note so the cards are discoverable from the existing workflow.
5. **Flag gaps honestly.** Topics in the drill list with no card (e.g. fundamentals not in
   the knowledge-gap folder) get an explicit "no card yet" row in the index — never silently
   skip them.
6. Batch writes: independent cards in parallel `write_file` calls; index + backlink patch last.

## Card format rules (what makes them drill-ready)
- **Spoken length**: each answer must be sayable in ~20–45 seconds. Written to be read
  aloud, not skimmed — the user's drill method is question → answer out loud → check card.
- **Mermaid flowcharts over tables for decision trees and selection criteria** (user
  preference). Small comparison tables are fine for 2–4 column trade-offs.
- End every card with a **⚡ Rapid-fire recap** — 5–8 one-liners for the last 10 minutes
  before the interview.
- Frontmatter: `document_type: Answer Card`, tags `[interview-prep, <company>, <topic>, answer-card]`.
- Link the card back to its source study note in the intro line.

## Pitfalls
- **Never fabricate personal stories.** "What did YOU use / YOUR app" answers must come from
  the user's confirmed-facts scripts (e.g. Scripts_A_to_F) — cross-reference, don't restate.
- Don't duplicate script content into cards; scripts and cards are cross-referenced, not copied.
- Technical content must be precise — these answers get spoken to a real panel. Verify
  numbers (e.g. Web Vitals thresholds) against current standards before writing them.
- Keep answers in English — the user rehearses aloud in English even though the chat language may differ.

## Verification
- Every study note has exactly one card; index lists all of them.
- Wikilinks resolve to real filenames in the same folder.
- No personal-experience claims that aren't traceable to the scripts/STAR files.

## Support files
- `templates/answer-card.md` — copy-and-modify starter for a new answer card.
