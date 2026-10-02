---
name: note-plaintext-cleanup
description: "Strip em-dashes/uncommon chars from notes; keep emoji."
version: 1.1.0
author: LLMOps
license: MIT
metadata:
  hermes:
    triggers:
      - "remove the em-dash"
      - "uncommon character"
      - "plain text cleanup"
      - "distracting characters"
    related_skills: [personal-ai-notes]
---

# Note Plaintext Cleanup

Refine Obsidian notes so they use plain ASCII (+ Thai). Panomete finds em-dashes and uncommon characters distracting and asked for their removal (2026-09-21).

## When to Use

- Requests like "remove the em-dash or uncommon character"
- Pre-delivery pass on notes written for his vaults (swe-knowledge, oralita_md, ai-knowledge)

## Scope Discipline

- Clean only the requested file/folder; offer to extend elsewhere instead of sweeping unasked.
- **Back up first** (copy originals to a scratch dir before rewriting).
- **Preserve Thai** (U+0E00-U+0E7F) and **emoji** (user wants emoji kept - never strip them). Strip only typographic/uncommon chars: em-dash, arrows, box-drawing, math symbols.

## Replacement Map

| Char | Replace with | When |
|---|---|---|
| em-dash | `: ` | headers `## X - Y` and bold-lead bullets `- **X** - y` |
| em-dash | ` - ` | everywhere else |
| en-dash | `-` | |
| arrows (right/left) | `->` `<-` | |
| down arrow | drop, keep indent | flow blocks |
| not-equal | `!=` | |
| ge/le/approx | `>=` `<=` `~` | |
| times | `x` | |
| middle dot | `, ` | |
| section sign | `section ` | |
| superscript 2 | `2` | |
| accented e | `e` | |
| box-drawing | 2 spaces per level | convert trees to plain indentation |
| emoji | KEEP | user likes emoji - do not strip (revised 2026-09-21) |

## Procedure

1. Scan: `Counter(ch for ch in text if ord(ch) > 127)`, split Thai vs typographic.
2. Backup originals to scratch.
3. Replace in order: title fixes, header/bullet colons, emoji clusters, dashes, arrows, symbols, box-drawing.
4. Cleanup outside code fences only: collapse `  +`, fix ` ,` ` .`, strip trailing spaces.
5. Verify: remaining non-ASCII must be Thai only; fence count even; mermaid blocks clean; spot-check trees via `repr()`.

## Pitfalls

- Emoji regex (for detection only, NOT stripping): `[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2300-\u23FF\uFE0F]+ ?`
- Down-arrow deletion regex `^(\s*)↓\s*` can merge lines; check flow blocks afterward.
- Never collapse double spaces inside code fences (mermaid indentation, trees).
- Trees: `│   ` `├── ` `└── ` each map to 2 spaces; delete lone `│` lines; leftover `─` to `-`.
- If emoji were wrongly stripped: regenerate from the pre-cleanup backup with the strip step disabled, and validate the regeneration (diff vs current) before overwriting.

## Verified

2026-09-21: `oralita_md/personal/ai` folder (8 files, 324 em-dashes) cleaned; emojis restored same day per user request - cleanup now keeps emoji.
