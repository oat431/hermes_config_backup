---
name: fitness-coaching
description: >-
  Fitness coaching — baseline assessments, program design, nutrition targets,
  and progress tracking. Write structured notes to Obsidian vault.
category: fitness
---

# Fitness Coaching

Load this skill when acting as Panomete's gym coach (gym profile) — conducting baseline assessments, calculating calorie/macro targets, designing training programs, or tracking progress.

## Baseline Assessment Workflow

When a new metric or goal is provided, follow this sequence:

1. **Gather the minimum viable set:** weight (kg), height (cm), age, primary goal, training age, equipment, schedule, current lifts, injuries, cardio, nutrition tracking status, sleep (hours).
2. **Calculate targets** using the formulas in `references/formulas.md`.
3. **Write a structured note** to `{OBSIDIAN_VAULT}/fitness/baseline-assessment.md` using the format in `references/note-format.md`.
4. **Verify the note** — read it back and run the integrity checks in `scripts/verify-baseline.py` (pass the vault path as argument).
5. **Save durable facts to memory** (weight, height, age, BMR, TDEE, goals, training age, equipment, schedule, sleep).

## Calorie Target Rules (from SOUL.md active-balance)

| Signal | Action |
|--------|--------|
| Weight (7d MA) drops >0.6 kg/week for 2 consecutive weeks | +200 kcal/day |
| Weight (7d MA) drops <0.15 kg/week for 3 weeks | -150 kcal/day or audit adherence |
| Sleep <6h average for the week | Cut one session |

## Deficit Starting Point

For untrained individuals at BMI >30: start at TDEE minus 800-1000 kcal. Protein floor: 1.3-1.6 g/kg bodyweight. Reassess after 2 weeks of data.

## Pitfalls

- **Don't skip age.** BMR calculation requires it; guessing produces wrong calorie targets.
- **Marathon + obesity = joint risk.** Enforce weight gates before distance milestones (no runs >10K above 100 kg).
- **Sleep at exactly 6h is borderline.** Flag it but don't cut sessions until the 7d average dips below 6h.
- **Complete beginners need form-first programming.** Don't prescribe heavy singles or aggressive progression. Start with bar/light weight, 3×5-8 compounds, linear progression at 2.5 kg/session.
- **Don't over-program cardio alongside deficit.** 2-3 sessions/week max for beginners; one should be low-impact (cycle/swim).
- **Default schedule ≠ actual schedule.** Always confirm which days the user can train before writing the program. When days are clustered (3+ consecutive), restructure to a 3-lift + 1-cardio split with the middle day intentionally light (cardio + small muscle groups only). Never run the same movement pattern on consecutive days.
- **Daily check-in tables for every week.** When creating log templates, all weeks need their own daily check-in table (sleep, weight, protein). The user will notice missing tables immediately. A 4-week template = 4 check-in tables.
- **Separate tracking from program.** Smart scale tracking goes in its own file (`smart-scale-tracking.md`), not embedded in the program. The program file references it by relative path only.
- **Write to phase subdirectories.** Use `fitness/phase_N/` for phase-specific files, `fitness/00_gym_knowledge/` for reference materials. Never write phase files flat in `fitness/`.
- **Obsidian reformats tables.** Opening/saving a note in Obsidian can auto-align table columns with padding whitespace, which breaks exact-string patches on tables (observed: a V4A multi-hunk patch failed wholesale on padded tables). Re-read the file immediately before patching program/log tables, and if a hunk fails, re-read and retry with the exact current text — never re-issue the same patch blind.
- **Obsidian renames don't auto-update agent-written wikilinks.** Panomete renamed day notes to `1_Monday.md`…`4_Saturday.md` mid-session; every `[[daily-workouts/Monday]]`-style link stayed stale. After any user-side rename, grep the vault for the old link names and patch all referencing files.
- **Another Hermes session operates on the same vault.** Files can move or vanish between sessions (observed: the `fitness/template/` folder was MOVED to the global Obsidian templates folder `F:/obsidian_note/oralita_md/templates/fitness/` by the other coach session — a later patch failed with "Failed to read file"). If a read/patch fails, `search_files` for the note name before assuming anything was deleted; then repatch references in place.

## Program Design Workflow

When the user has baseline data and asks for a training program:

1. **Determine split.** 4 days/week default → Upper/Lower. 3 days → Full-body. 2 days → Full-body both days.
2. **Check schedule constraints.** If available days don't match the default spread (e.g., Mon-Tue-Wed consecutive), restructure. See **Schedule Restructuring** rules below. Written programs must use actual day names, not "Day 1/2/3/4."
3. **Exercise selection — compound-first.** For complete beginners: start with dumbbells and machines, progress to barbell when form is stable. Each day: 4-5 exercises, 2-3 compounds, 1-2 accessories.
4. **Sets × reps.** Compounds: 3×5-8. Accessories: 2-3×8-15. Core: 2×20-30 sec holds.
5. **Progression.** Linear: add 2.5 kg to compounds each session when all reps completed with good form. Miss reps twice → deload 10%.
6. **Cardio pairing.** 2-3 sessions/week. Run/walk intervals for beginners. One low-impact option (cycle/swim). Weight gates: no runs >10K above 100 kg.
7. **Write program note** to `{vault}/fitness/phase_1/{name}.md` using format in `references/program-format.md`. Include a Time column in the schedule table (~55 min Upper, ~50 min Lower, ~40 min light, ~60 min Full Body). Every exercise table must include a Rest column (see Key Rules in program-format.md). Write phase-specific files into subdirectories (`phase_1/`, `phase_2/`), not flat in `fitness/`.
8. **Write supplementary files:**
   - Reference materials go in `{vault}/fitness/00_gym_knowledge/`: meal templates (`meal-templates-{protein}g-protein.md`), alternative exercises (`alternative-exercises-crowded-gym.md`), baseline assessment.
   - Training log goes in the phase directory: `{vault}/fitness/phase_1/training-log-week1.md` — 4-week pre-filled log with daily check-in tables for EVERY week, not just the first.
   - **Warm-up notes (two layers, W8+):** (a) `warmup-protocol.md` in the phase directory holds the GENERAL rules: 5–8 min general warm-up, ladder template, accessory rule, run/walk walk-warm-up, never-log-warmups. (b) The exact ladder weights go INLINE in each day note under its exercise (see `references/vault-restructure-w8.md` and `templates/day-note.md`). Rest conventions: barbell ladder = 60–90 sec between ramp sets, then full prescribed rest before the first working set; light ramp set = rest ~60 sec after; general warm-up = no rest. Ladder = ~50% ×5 / ~70% ×3 / ~90% ×2 of the working weight, rounded to nearest 2.5 kg (empty bar when 50% < 20 kg). Exercises that need no warm-up say "Warm-up: none — <muscle> already warm from <exercise>". Panomete skips warm-ups when they aren't explicit — that's why heavy first sets feel hard. When a review changes a working weight, RECOMPUTE the inline ladder in the day note.
9. **Verify program note** — run `scripts/verify-program.py <vault_path> <program_filename>` to confirm schedule days match the user's availability and all sections are present.

### Schedule Restructuring

When the user's available days don't match the default spread, apply these rules:

| Constraint | Action |
|-----------|--------|
| 3+ consecutive available days | Convert one middle day to light (cardio + accessories only). Never hit the same muscle group back-to-back. |
| 4 days in 3 consecutive slots (e.g., Mon-Tue-Wed + Sat) | Make the 3-day block: Upper → Lower → Cardio/Light. The isolated day (Sat) becomes Full Body with compound focus. |
| Gap of 3+ days between sessions | The session after the gap should be moderate volume, not max intensity — detraining risk is low, injury risk from over-eagerness is high. |
| Only 2-3 days available | Drop to Full Body each session. Cardio as separate low-impact sessions or post-lift finishers. |

Design principle: **no objective breaks, no objective explodes.** When consecutive days are forced, the middle day must carry the lowest CNS/fatigue load. Small muscle groups (arms, lateral delts, core) recover in ~24h and are safe on consecutive days. Heavy compounds need 48-72h between sessions for the same movement pattern.

## Illness / Skipped-Week Re-Entry Protocol

When a week is lost to illness (flu, COVID, etc.), rebuild deliberately — never revenge-train:

| Signal | Action |
|--------|--------|
| Week lost to illness | Annotate the log honestly: `## Week N — SKIPPED (illness)`. No fabricated metrics, no check-in table. A sick week is a data point, not a failure — say so to the user. |
| ≥2 weeks off, or respiratory illness | Re-entry barbell weights = −5% of last EARNED finals; rebuild +2.5 kg/week toward them |
| Re-entry week intensity | RPE gate: every working set Medium or easier. Hard = repeat next week, not a failure |
| Respiratory illness | Walk-first cardio for the first week back (no intervals); breathing gate: chest tightness / abnormal shortness → stop + report |
| Post-illness RHR | Expect 65–75 bpm for 1–2 weeks — recovery, not danger; don't cut training on RHR alone |
| Baseline-week schedules | Reschedule measurement baselines that fell in the sick week (e.g., BP baseline week slides to the return week) |
| Nutrition | Hold kcal; protein becomes THE priority if appetite is still suppressed (hit 160 g even if kcal lands under) |
| Missed week mentality | State "no make-up volume" explicitly — no extra sets, no double sessions, no bonus running |

Full playbook with the W10 flu-A worked example: `references/illness-reentry-protocol.md`.

## Week Review Workflow

When the user brings back a completed training log:

### 1. Analyze Weight Trend
- Plot morning weights across the week. Calculate net change from day 1 to day 7.
- If net change is 0 or positive: the deficit isn't working. Check protein adherence first (were they hitting the target?), then flag calorie tracking as the likely issue. Recommend either 3 days of tracking or a portion-reduction heuristic (cut rice by ¼ cup, drop one snack).
- If a mid-week spike appears (e.g., +1 kg in one day, then returns): explain water weight — sodium, training inflammation, glycogen. This is normal and not fat gain. The user will ask "why did I gain weight?" — answer it proactively.
- Apply calorie target rules (from active-balance table): flat weight for 3+ weeks → -150 kcal. Dropping >0.6 kg/week for 2 weeks → +200 kcal.

### 2. Assess Adherence
- **Protein:** average across the week. Report vs target. If below target on >3 days, flag meal prep as the fix.
- **Sleep:** average and distribution. ≥4 days at 6h is borderline — note it but don't cut sessions unless the 7d average dips below 6h.
- **Protocol violations:** did they double the run time? Skip exercises? Train on rest days? Flag each one.

### 3. Set Per-Exercise Week N+1 Targets
For each exercise, evaluate the Week N RPE (Easy/Comfortable/Medium/Hard) and set the next weight:

| Wk N Feel | Action |
|-----------|--------|
| Easy / Comfortable | Increase by 2-2.5 kg (or one machine plate increment) |
| Medium | Small increase — 1-2.5 kg |
| Hard | Stay at same weight. Hard = right intensity. |
| Failed reps | Stay or drop 10% depending on pattern |

Present this as a table: Exercise | Wk N Weight | Wk N Feel | Wk N+1 Target | Note.

### 4. Flag Issues
Categorize flags:

- **Pain flags:** "Leg kinda hurt" or similar. Ask the clarifying question: muscle burn (DOMS — normal, continue) or joint/tendon (sharp — stop, swap exercise). Don't increase weight until clarified. Provide a substitute exercise in the same movement pattern.
- **Form flags:** Suspicious weight-to-RPE mismatch. E.g., 15 kg lateral raises rated "easy" by a beginner = swinging with traps. Flag it, prescribe lower weight (5-6 kg) with strict form cues.
- **Protocol flags:** Run time doubled, extra sessions added, rest days skipped. State the protocol, state what happened, restate the protocol for next week.
- **Ramping flags:** If the user records 10→12→12 within one session (pyramiding), note that Week 1 is fine for finding weights, but Week 2+ should settle on one working weight after warm-ups. Warm-up sets are not logged.

### 5. Write Review to the Weekly Review Summary
Panomete keeps the program file as a live plan only. Append the review to `phase_N/weekly-review-summary.md` (create it if missing), then update the program file's current-week tables only. Section format:

```
## Week N Review (date range)

| Metric | Result | Verdict |
|--------|--------|---------|
| Weight | start → end | ... |
| Protein avg | Xg (target Yg) | ... |
| Sleep avg | Xh | ... |

### Week N Performance → Week N+1 Targets
(table)

### ⚠️ Flags from Week N
(per-flag bullets with resolution)

### Week N+1 Adjustments
(nutrition, form, protocol changes)
```

### 6. Provide Meal Templates and Alternative Exercises
After writing the initial program, also provide:
- **Meal templates** (`references/protein-examples.md`) — 3 sample days with real-food assemblies at the user's protein target
- **Alternative exercises** (`references/alternative-exercises.md`) — a swap list for every exercise, plus a "gym is packed" circuit
- **Training log** (`references/log-template.md`) — pre-filled 4-week template with daily check-in

## Phase Transition Workflow

When Phase 1 is complete (4 weeks of consistent training), assess readiness for Phase 2:

### Barbell Readiness Signals
Move from dumbbell/machine to barbell when:
- **Goblet squat rated "Easy" at 20+ kg** → switch to barbell back squat. The grip is now the limiter, not the legs.
- **DB bench at 20+ kg per hand with stable form** → switch to barbell bench press. Barbell enables smaller increments and heavier loading.
- **RDL at 35+ kg for 8 reps** → introduce conventional barbell deadlift. Lower starting weight (60 kg) for form, then progress linearly.
- **User has done unscheduled barbell work** (e.g., tried barbell bench on their own) → they're ready. Channel the enthusiasm into the program.

### Starting Barbell Weights
- Back squat: 40 kg (2× bar-only warm-up sets for form, then load)
- Bench press: 40 kg (or last tested weight)
- OHP: 30 kg (strict, no leg drive)
- Deadlift: 60 kg (1 working set after warm-ups: 40×5, 50×3, 60×5)
- Front squat: 30 kg (lighter, teaches upright torso)

### Phase 2 Program Structure
Keep the same schedule but shift exercise selection:
- Mon (Upper): Barbell bench + barbell OHP as main lifts
- Tue (Lower): Barbell back squat as main lift
- Wed: Unchanged (run/walk + core)
- Sat (Full Body): Barbell deadlift + barbell front squat as main lifts

Rep scheme shifts from 3×8 to 3×5 on barbell compounds (strength focus). Accessories stay 3×8-12.

### Write Phase 2 Program
Create files under `{vault}/fitness/phase_2/` (not flat in `fitness/`):
- `phase2-program.md` — new program document with barbell progression tables, warm-up protocol, and run/walk progression
- `training-log-phase2.md` — pre-filled 4-week log template with daily check-in tables for ALL 4 weeks
- `smart-scale-tracking.md` — separate tracking file (do NOT embed the tracking table in the program document; only reference it by path)
The program document should reference the other two by relative path:
```
**Smart scale:** Log every Sunday → `smart-scale-tracking.md`
**Training log:** Fill after every session → `training-log-phase2.md`
```
Do not duplicate the tracking table inside the program file.

## Vault Structure Convention

Panomete organizes by phase. **v2 convention (from 2026-08-23):** cross-phase records live at the vault ROOT; phase folders hold the active program only.

```
fitness/
├── baseline-assessment.md          ← cross-phase (moved from 00_gym_knowledge)
├── blood-panel-baseline.md         ← cross-phase (one draw + 6-month retest)
├── body-measurements-monthly.md    ← cross-phase (tape + photos, 1st Sunday)
├── 00_gym_knowledge/               ← reference materials (meal templates, watch settings, shopping list)
├── audit/                          ← training_audit_YYYYMMDD.md
├── phase_N/
│   ├── phaseN-program-overview.md  ← live plan ONLY (no review history)
│   ├── warmup-protocol.md
│   ├── food-log.md                 ← live food system for this phase
│   ├── daily-workouts/{gym,home}/  ← numbered day notes 1_Monday..5_Sunday per location
│   └── logs/
│       ├── daily/                  ← training-log-phaseN.md (sessions + check-in tables), run-walk-log.md
│       └── weekly/                 ← smart-scale-weekly.md, blood-pressure-log.md, phaseN-weekly-review-summary.md
└── (templates live in the GLOBAL Obsidian templates folder, NOT inside fitness/)
```

When creating new files:
- **Cross-phase → root.** Baseline assessment, blood panel, monthly tape/photos carry forward through every phase; never lock them inside a phase folder. User requested this split explicitly ("monthly log at root of the fitness").
- **Logs split by fill-cadence:** `logs/daily/` = "fill on the day" (training log with check-ins, run-walk log); `logs/weekly/` = "fill on Sunday" (BIA, BP, review summary). Keep the two-folder split minimal — don't fragment further.
- **Review-summary naming:** use `phaseN-weekly-review-summary.md`. Plain `weekly-review-summary.md` in two phases collides in Obsidian (name-based wikilinks go ambiguous; shortest path wins).
- **Day notes** → `fitness/phase_{N}/daily-workouts/`, numbered `1_Monday.md`…`4_Saturday.md`; exercises in session order with the warm-up ladder INLINE under each exercise (template: `templates/day-note.md`). Rationale: Panomete opens one file at the gym and follows it top to bottom.
- **Reference materials** (meal templates, alt exercises, watch settings, shopping lists) → `fitness/00_gym_knowledge/`
- **Never write phase files flat** in `fitness/` — the user will reorganize them into subdirectories anyway
- **Wikilinks are name-based** — they survive file moves; raw `file.md` path text does not. After ANY restructure (yours or the user's), grep for old paths and repatch every reference.
- **Before writing**, discover the current layout with `find` or `search_files` — the vault may have been restructured since last session

## Smart Scale Body Composition Analysis

When the user provides BIA scale data (Xiaomi S400 or similar), compute:

### Body Fat Analysis
```
BF% = fat_kg / total_weight × 100
Lean body mass = total_weight - fat_kg
```

**Muscle base assessment:** If LBM is unexpectedly high (e.g., 76 kg at 178 cm), the user has a solid muscular foundation from carrying excess bodyweight daily. This changes programming — they can handle barbell work sooner and may preserve more muscle on the cut.

### Goal Weight Calculation
```
goal_kg = (current_muscle_kg - 3) / (1 - target_bf_pct)
```
The -3 accounts for expected muscle loss on a prolonged deficit. Adjust target BF% based on user goals (20% is a realistic first milestone).

### Visceral Fat Priority
Visceral fat (scale rating 1-59) is the most important health metric:
- <9: normal
- 10-14: elevated
- 15+: very high — this is the priority to drop
- Falls fastest on a deficit + cardio
- Track every Sunday. Target: drop below 10 long-term, below 15 as Phase 2 milestone

### Hydration Check
- Body water <45%: dehydrated. Scale readings (especially BF%) will be unreliable. Prescribe increased water intake.
- Body water >48%: adequately hydrated. Scale readings more trustworthy.
- Trend water % alongside weight — rising water % with dropping weight = good (fat loss). Dropping water % with stable weight = dehydration masking fat loss.

### BMR Reconciliation
- If scale BMR differs from calculated BMR by >100 kcal, use the scale value. It accounts for actual body composition.
- Recalculate TDEE: scale_BMR × activity_multiplier (1.55 for 4×/week gym)

### Lateral Raise Weight Check
If a beginner rates lateral raises as "easy" at >8 kg, they are swinging — using traps and momentum instead of medial delts. Prescribe 5-6 kg, strict form (lead with elbows, 2-sec negative). They should burn by rep 10.

### Water Weight Spike
Mid-week weight spikes of 0.5-1.5 kg are water — sodium, glycogen replenishment, training inflammation. If weight returns to baseline by end of week, the deficit math is still sound. The user WILL ask about this. Answer: "Water weight. Normal. Look at the Sunday number, not Wednesday."

### Within-Session Ramping
Beginners often pyramid up within a session (10→12→12) while finding their working weight. This is acceptable in Week 1 only. For Week 2+: settle on one working weight after 1-2 warm-up sets, do all working sets at that weight. Warm-up sets are NOT recorded in the log — only working sets matter.

## Linked Files

- `references/formulas.md` — BMR, TDEE, BMI, deficit, and protein formulas with active-balance guard table.
- `references/note-format.md` — Obsidian baseline-assessment.md template with YAML frontmatter spec.
- `references/protein-examples.md` — Real-food protein equivalents for common targets, plus sample day assemblies.
- `references/program-format.md` — Obsidian program note template (4-week phase) with schedule-adaptation rules and mandatory Rest column.
- `references/alternative-exercises.md` — Per-exercise swap list for crowded gyms, plus "gym is packed" dumbbell-only and bodyweight circuits.
- `references/log-template.md` — Fillable 4-week training log format with daily check-in tables and rep recording conventions.
- `scripts/verify-baseline.py` — Integrity checker for baseline-assessment.md. Run: `python verify-baseline.py <vault_path>`
- `scripts/verify-program.py` — Integrity checker for program notes. Run: `python verify-program.py <vault_path> <program_filename>`
- `templates/day-note.md` — Per-training-day gym note template (warm-up inline under each exercise, rest conventions, Obsidian pitfalls).
- `references/vault-restructure-w8.md` — Canonical W8+ vault layout (overview + daily-workouts + warmup-protocol + review summary) and warm-up rest conventions.
- `references/illness-reentry-protocol.md` — Post-illness re-entry playbook (W10 flu-A worked example, re-entry weight tables, gates, bookkeeping).
