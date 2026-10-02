---
name: doc-localization
description: "Use when team docs need Thai localization or docx export."
version: 1.0.0
author: Hermes Agent (QA)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [localization, thai, documentation, docx, team-communication]
    related_skills: [playwright-suite-health-review, checklist-audit]
---

# Doc Localization for Teams (non-English teammates)

## When to use

- A teammate (e.g. Thai colleagues) cannot comfortably work in the English source doc and
  needs a localized copy they can read and answer in.
- A team-facing markdown doc should be forwarded to a corporate audience → also ship a `.docx`.

Default deliverable: the localized `.md` next to the master, plus a `.docx` the user can forward.

## Rules (apply every time)

- **Copy, don't replace**: same folder, same base name + locale suffix (`03_x_th.md`), identical
  numbering/IDs so answers cross-map between languages. The English original stays the master.
- **Keep technical tokens verbatim**: product codes, filenames, commands, env vars, question
  numbers, `[BLOCKING]`-style tags stay as-is; translate only the connective prose. Technical
  Thai audiences expect mixed English terms.
- **Mark status visibly**: which items are already answered vs open, and who answers where —
  otherwise readers re-answer answered items or skip open ones.
- **Be transparent about interpretation**: if translating an existing answer required a judgment
  call, say so in one clause so the team can correct it.
- **Register**: neutral formal Thai; write like the team writes (mixed Thai/English in specs is
  normal). Avoid literal machine-translation phrasing.
- After adding/removing items, **grep the whole doc set for stale counts** ("ทั้ง 19 ข้อ",
  "Q-1…Q-19", "N questions") and update every hit — status lines, headers, index rows.

## Workflow

1. Read the source doc fully; keep its section numbering and grouping.
2. Write `<name>_<locale>.md` next to the original.
3. Update the doc SET: index row, cross-links, stale counts elsewhere in the set.
4. Export `.docx` when it will be forwarded:
   `uv run --with python-docx python <skill>/scripts/md_to_docx.py <src.md> <out.docx> [font]`
5. Verify: re-extract the docx with `read_file` (auto-extracts .docx) and confirm numbering,
   content and clean rendering (no stray artifacts like lone ">" paragraphs).

## Tooling notes (host-friendly)

- `pandoc` or an importable `python-docx` are often NOT installed — don't plan around them.
  `uv run --with python-docx python …` creates a throwaway env in one command (works on hosts
  where pip is PEP-668 blocked).
- **Thai font**: set `Leelawadee UI` (Windows) on the Normal style AND on Title/Heading styles,
  including the complex-script attribute `w:cs` — without `w:cs` Thai can fall back to a wrong
  font. Sarabun/Tahoma are acceptable fallbacks for other machines.
- The ready converter is `scripts/md_to_docx.py` in this skill (headings, blockquotes, lists,
  bold/code inline; skips lone `>` separator lines). Run it — don't rewrite from memory.

## Pitfalls

- Identifiers are NOT translated: Q-6 stays Q-6, TC numbers stay TC numbers — answers must map
  back to the English master.
- Regenerate the `.docx` after ANY edit to the source `.md`; exports go stale silently.
- Don't leave the localized copy orphaned: the index / other docs must point to it.
