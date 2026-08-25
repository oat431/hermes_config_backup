# Interview Prep Vault — Build & Review Workflow

Use when the user has a **confirmed upcoming interview** (recruiter email / JD / scheduled date). Produces a numbered-file prep vault, not a single doc.

## Vault structure (user's numbered-file + wikilink convention)

Create under `F:\obsidian_note\interview-preparation\<company>\`:

| File | Content |
|---|---|
| `00_Index` | One-line strategy, file map, top risks (revised after confirms) |
| `01_Battle_Card` | Logistics, company research, panel-reading (who cares about what), rehearsed intro, questions to ask them, red flags to watch for |
| `02_Fit_Assessment` | Line-by-line JD vs resume mapping (✅/🟡/🔴), gap scripts, positioning statement, **confirmed-facts table**, attribution rules |
| `03_Knowledge_Gaps_and_Study_Plan` | Gap topics ordered by probability, each with study points + wikilinks to the user's swe-knowledge / career-path vaults |
| `04_STAR_Stories_and_Drill_Questions` | 7+ STAR stories mapped to JD lines (Action section 60–70%), behavioral drill, 30–40 technical drill questions, senior meta-questions |
| `05_Practice_Plan_and_Day_Of` | Day-by-day schedule, day-of checklist, salary framework, mock-interview offer |

Process order: read JD context file + resume PDF + relevant vault indexes first → research the company → build all 6 files → user fills `[CONFIRM]` → **mandatory re-review** (below).

## [CONFIRM] marker workflow

Draft everything from the resume, but mark every assumption the candidate alone can verify: years in the JD's core tech, which libraries were actually used, wrote-it vs reviewed-it attribution, one concrete example per claim, real motivation for leaving/joining. Batch these into a short numbered list in the summary so the user can fill them in one pass.

## Mandatory re-review loop (the lesson)

The first draft overestimates fit because the resume overstates focus — that is what made it pass ATS. Real case (MISUMI, Aug 2026): resume implied 3+ yrs React; candidate confirmed **~1 actual year**, **Context only / never Redux**, Vitest testing, SSR chosen by architecture not by him. Fit verdict dropped ~80% → ~60% and the whole strategy flipped:

1. **Re-read the filled files** and extract every confirmed fact into a table at the top of 02.
2. **Revise the verdict honestly** — never keep the pre-confirm optimism.
3. **Write word-for-word scripts for the dangerous answers**:
   - Years gap → honest pivot: "about X years of focused [tech], and here's my velocity proof" — never inflate; getting caught ends the interview.
   - Never-used JD-named tech → ban "I don't understand X"; use deliberate-choice framing ("I chose Y for this scope; here's when I'd reach for X") **plus** a 2–3h crash-study section so follow-ups don't expose the bluff.
   - Unexpected strengths (e.g., Vitest tests found) → promote from gap to named strength.
4. **Update attribution rules** — which project leads which story (built vs reviewed vs supervised).
5. Propagate risk changes back to the index file.

## Interview-format adaptations

- **Japanese-company panels** (MISUMI pattern: Thai HoD + Thai team + optional Japanese Director): punctuality is respect (join 10 min early), answer conclusion-first, never badmouth employers, stability framing for 3–5 year questions (avoid "start my own company"), hou-ren-so (proactive report/communicate/consult) flavor in answers, short clear English sentences if the Director's English is limited.
- Panel-reading table: each interviewer type gets a "what they care about / how to play it" column.

## Pitfalls

- Don't draft STAR Action sections with invented specifics — leave them `[CONFIRM]`; generic actions collapse under probing.
- Don't let the candidate claim a senior specialist identity they can't defend (e.g., "React expert" with 1 year) — senior *behaviors* (mentoring, reviews, CI/CD ownership) are the honest differentiator for full-stack candidates applying to specialist roles.
- Salary: never anchor to current low base; quote the role's market range; walk-away number set before negotiation.
