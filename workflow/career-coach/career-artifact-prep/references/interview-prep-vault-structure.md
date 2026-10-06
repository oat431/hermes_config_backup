# Interview-Prep Vault Structure — Worked Example

Real refactor (2026-08-31): centralized personal info from a company prep folder (`misumi/`) into `career/` while a new interview (ITOPLUS) was incoming.

## Before

```
interview-preparation/
├── career/          (hub existed but was missing the richest artifacts)
│   ├── Sahachan.md, Sahachan-Resume.md, Sahachan-Linkedin.md, Sahachan-STAR-Stories.md
├── context/         (recruiter emails — inconsistent with company folders)
│   ├── misumi.md, 7_solutions.md
├── misumi/          (company prep — contained STRANDED personal artifacts)
│   ├── 00 index, 01 Battle Card, Company_Research, Review_retro
│   ├── 02_Fit_Assessment/ (Positioning, Attribution_Rules, Scripts_A_to_F, JD mapping)
│   ├── 03_Knowledge_Gaps_and_Study_Plan/ (React deep dive, answer cards…)
│   ├── 04_STAR_Stories_and_Drill_Questions/ (STAR_Stories_S1_to_S7, drills)
│   └── 05_Practice_Plan_and_Day_Of.md
├── ITOPLUS/          (already used the good pattern: 00 Recruiting Email.md inside)
└── 7_solutions/      (empty dir)
```

## After

```
interview-preparation/
├── career/                      # facts about YOU — reusable everywhere
│   ├── Sahachan.md              # master profile (+ Confirmed Facts written back)
│   ├── Sahachan-STAR-Stories.md # S1–S7 spoken versions merged → Stories 1–8
│   ├── Sahachan-Interview-Scripts.md  # was Scripts_A_to_F
│   ├── Sahachan-Positioning.md        # was Positioning
│   ├── Sahachan-Attribution-Rules.md  # was Attribution_Rules
│   ├── Sahachan-Why-Leaving-Gosoft.md # NEW — raw reasons + never-say list + public flip
│   └── study/                   # was misumi/03_Knowledge_Gaps_and_Study_Plan
│       └── note/                # answer cards
├── misumi/                      # facts about THEM + your application
│   ├── 00_Recruiting_Email.md   # was context/misumi.md
│   ├── 00 index, 01 Battle Card, 02 Fit_Assessment (JD mapping only)
│   ├── 04 .../ (Behavioral_Drill, Technical_Drill_40, Senior_Meta_Questions)
│   └── 05_Practice_Plan_and_Day_Of.md
├── ITOPLUS/ 00 Recruiting Email.md
└── 7_solutions/ 00_Context.md   # was context/7_solutions.md
```

## What moved and why

| File | From | To | Rationale |
|---|---|---|---|
| STAR stories S1–S7 (spoken) | misumi/04/STAR_Stories_S1_to_S7.md | merged into career/Sahachan-STAR-Stories.md | one portfolio, one source of truth; 4 new stories (Node upgrade, Babel→Vite, Redis perf, HR UI) + spoken versions added to existing 3 |
| Scripts A–F | misumi/02/Scripts_A_to_F.md | career/Sahachan-Interview-Scripts.md | honest landmine answers reusable for every frontend interview |
| Attribution Rules | misumi/02/Attribution_Rules.md | career/Sahachan-Attribution-Rules.md | company-independent |
| Positioning | misumi/02/Positioning.md | career/Sahachan-Positioning.md | narrative spine is personal, not MISUMI's |
| Confirmed Facts (React ~1yr, Context-only, no Redux, Vitest) | buried in misumi/02/00_Fit_Assessment.md | career/Sahachan.md | biggest data-loss risk — must live in master profile |
| Study content + answer cards | misumi/03_Knowledge_Gaps_and_Study_Plan/ | career/study/ | reusable for any senior frontend role; gap priorities stay JD-derived |
| Why-leaving note | vault ROOT (`Why I want to move on from Gosoft.md`) | career/Sahachan-Why-Leaving-Gosoft.md | root orphan looked like a broken wikilink; content was real and personal |
| Recruiter email | context/misumi.md | misumi/00_Recruiting_Email.md | one folder per company self-contained (ITOPLUS pattern) |
| 7-solutions context | context/7_solutions.md | 7_solutions/00_Context.md | same |

## Mechanics that mattered

- All moves via `git mv` → git tracked them as renames (history preserved)
- Wikilinks by filename survived the folder moves untouched (Obsidian resolves vault-wide)
- Renames (Scripts_A_to_F → Sahachan-Interview-Scripts etc.) broke 19 references; first grep missed 9 stragglers in `career/study/note/` and drills — final sweep used `grep -rn --include='*.md' -E '\[\[(Old_Name)\]\]'` across the WHOLE vault
- Absolute path references (`F:\obsidian_note\interview-preparation\context\misumi.md`) also needed updating in indexes
- One patch accidentally deleted a JD-mapping table row (partial-row old_string/new_string) — caught immediately and restored; lesson: include full rows in table patches

## Payoff

Next company prep (ITOPLUS, AI Engineer) starts from `career/` — STAR stories, scripts, attribution, positioning all present; only battle card + fit assessment need building fresh. ~80% less rework per new interview.
