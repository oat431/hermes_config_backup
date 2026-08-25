# Answer-card recipe

Proven format from the MISUMI prep (2026-08-18). Cards live in `<study-folder>/note/` next to the study notes.

## Files

| File | Purpose |
|---|---|
| `Answers_NN_<topic>.md` | One per study note, Q&A pairs |
| `00_Answer_Cards_Index.md` | Card list, drill-question → card map, scripts cross-reference, house rules |

## Card structure

```markdown
---
document_type: Answer Card
tags: [interview-prep, <company>, <topic>, answer-card]
---

# Answers NN — Topic 🗂️

> Pairs with [[NN_Study_Note]]. Drill: question → answer aloud → check card.

### Q1. <Question as an interviewer would ask it>
**A:** <20–45s spoken answer, conclusion-first>

...

## ⚡ Rapid-fire recap
- one-line essentials only (5–10 bullets)
```

## Writing rules

- **Spoken-length**: 20–45 seconds when read aloud. Conclusion first, then detail (Japanese-panel style: structure before detail).
- **Mermaid flowcharts** for decision logic (e.g., "which tool / which rendering strategy / why is it re-rendering"). Keep to 5–8 nodes.
- **Tables** for comparisons (Context vs Redux, offset vs cursor pagination). Max ~5 rows.
- **Code snippets** only when they demonstrate the mechanism (stale-closure fix, event-loop ordering). Keep <10 lines.
- Where a card touches the candidate's own experience, write "your story / your app" and point at the scripts note — never restate confirmed facts (they drift if duplicated).
- Honest gaps stay honest: bridge phrasing ("I haven't hit that in production, but here's how I'd reason about it…") instead of bluffing.

## Index structure

1. Priority table: study note ↔ answer card (wikilinks both ways)
2. Drill-question → card map (covers every drill question, flags uncovered ones)
3. Scripts cross-reference (which personal-story script answers which moment)
4. House rules block

## After writing

- Patch the study-plan index note with a link to `[[00_Answer_Cards_Index]]`.
- Verify all wikilinks resolve (card names must match filenames exactly).
