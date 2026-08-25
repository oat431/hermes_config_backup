---
name: weekly-training-review
description: Structured weekly review of Panomete's training log — compute weight trends, check SOUL triggers, compare actuals to targets, set next week's targets, and update the program file.
---

# Weekly Training Review

This skill governs the end-of-week check-in workflow. The coach reads Panomete's log, analyzes progress, flags issues, and updates the program file with the review + next week's targets.

## Triggers
- User says "end of the week," "review my log," "check my progress," "Week X review"
- User provides updated training log data
- Any mention of completing a training week

## Workflow

### 1. Locate and Read Current-Phase Sources
- Discover the current vault layout before reading: the user may organize files under `fitness/phase_N/` with shared references under `fitness/00_gym_knowledge/`.
- Read the current phase's training log, the current phase program, and—when present—the separate smart-scale/watch tracking file. Do not assume the old flat `training-log-week1.md` path.
- For Phase 2 the usual sources are `phase_2/training-log-phase2.md`, `phase_2/phase2-program.md`, and `phase_2/smart-scale-tracking.md`; verify paths rather than guessing.
- Read the entire current-week block, including daily check-in, body-composition row, and watch-metrics row. Historical weeks are context, not current data.

### 2. Extract and Compute Metrics

**Weight trend:**
- Pull daily weights from the check-in table
- Compute 7-day average (sum of the seven values / 7) and start→end change
- Compare both with the prior week's 7-day average and with standardized Sunday smart-scale readings when available
- Never describe a single week's endpoint drop as equivalent fat loss; explain water/glycogen/sodium/training noise and prioritize the rolling average
- If a standardized BIA reading is present, compare fat mass, muscle mass, visceral-fat rating, and body-water trend, but label one-week BIA changes as noisy rather than definitive

**Watch metrics:**
- Pull average steps/day, PAI, average sleep, and resting HR from the separate watch-tracking row
- Treat impossible or ambiguous values (for example, a resting HR of 10.8 bpm) as invalid data: flag for verification and do not use them for training or health decisions
- When a value is physiologically impossible, explain the metric in plain language and ask for its exact label/unit in the app — Panomete once logged the wrong tile for three weeks ("10" was not resting HR; real RHR was 57/59/78 bpm), then corrected it himself. Backfill the review after correction. Interpretation baseline: 57–59 bpm at 120+ kg is healthy; a +15–20 bpm week-over-week spike after the heaviest training week is a recovery signal (fatigue + heat), not danger — act only if it stays elevated 2+ weeks.
- Use watch calorie estimates as secondary context only; do not prescribe eating back active calories from a wrist wearable
- Compare actual steps against the current achievable baseline. If the user is far below a long-term step goal, ramp gradually (for example, 3,573/day → 5,000/day before 8,000/day) rather than imposing the long-term target immediately
- Treat PAI 100/week as a long-term cardiovascular reference, not a reason to add HIIT or extra hard sessions to a beginner's plan

**Activity dose:**
- Compare prescribed run/walk duration with actual duration. Extra running volume is a protocol violation, not automatically a positive
- For a beginner at high body mass, return to the prescribed duration after an overshoot; offer walking, cycling, or swimming for extra low-impact movement
- Build steps separately from running. Prefer small daily walks (e.g., 10 minutes after two meals) over unscheduled extra running

**Protein compliance:**
- Count days at 160g+ (target)
- Compute weekly average
- Note which days missed and by how much

**Sleep:**
- Compute weekly average
- Count days at or below 6h
- SOUL trigger: if average <6h for the week → flag session reduction

### 3. Check SOUL Triggers (Active Balance rules)
Apply these rules from SOUL.md without asking the user:

| Signal | Action |
|--------|--------|
| Weight (7d MA) drops >0.6 kg/week for 2 consecutive weeks | +200 kcal/day |
| Weight (7d MA) drops <0.15 kg/week for 3 weeks | -150 kcal/day, or audit adherence |
| Failed same lift twice in a row (same weight/reps) | -10% weight, linear progression restart |
| Run/cardio >90s below expected pace two sessions | Flag deload next week |
| Sleep <6h average for the week | Cut one quality session |

### 4. Compare Actual Weights to Targets
- For each exercise, compare the logged weight to the target from the previous review
- Note: overshoots, undershoots, rep drops, form notes, ramping (multiple weights logged for same exercise)
- Flag exercises where the user ignored a prescribed weight drop (e.g., I said 12 kg, user did 20 kg)

### 5. Identify Flags
Common flags across Panomete's sessions:
- **Ramping within sessions** (logging 3-5 different weights for one exercise) — user should do 1-2 warm-up sets then all 3 working sets at same weight
- **Extra sets/reps** (4×12 instead of 3×8) — more volume on a deficit = unrecoverable fatigue
- **Unscheduled work** (extra exercises outside the program) — adds unaccounted fatigue
- **Skipped days** — note the reason (OT, fatigue, motivation) and adjust
- **Exercise swaps** — if reasonable (reverse lunges for Bulgarian SS), approve and update the program. If not, revert
- **Form concerns** — weights that jumped improbably (e.g., collapsed at 20 kg last week, "Medium" at 20 kg this week without explanation)

### 6. Set Next Week's Targets
- Increase by 2.5-5 kg for exercises marked "Easy" or "Medium" with clean form
- Stay at same weight for exercises marked "Hard" (right intensity)
- Drop weight for exercises with rep failure or form collapse
- Include calorie adjustment if SOUL trigger fired

### 7. Update the Files (two-file structure — Panomete's explicit preference)
Panomete restructured the vault so the program file is a LIVE PLAN ONLY; historical reviews live in a separate summary file per phase.

- **`weekly-review-summary.md`** (in the phase directory): append `## Week N Review (date range)` with metrics table, performance→targets table, flags list, and nutrition status; update the trailing "Current status after Week N" bullets.
- **Program file** (`phaseN-program.md`): update ONLY the current-week target tables, progression map, and nutrition/recovery numbers. Never append review history to it. If legacy reviews are embedded, offer to extract them instead of extending them.
- Use `patch` for targeted edits; re-read the target file first (Obsidian may have reformatted tables — see Pitfalls).

### 8. Present Summary to User
- Be concise and direct: lead with the verdict, then the numbers, then the action table. Avoid a long narrative unless the user asks for detail.
- Separate three judgments explicitly: training adherence, activity-dose adherence, and nutrition/recovery status.
- State what went well and what was actually wrong; do not flatter or call a water drop fat loss.
- Give one clear target per problem for the next week (e.g., exact run duration, step floor, calorie decision).
- Ask ONE clarifying question only if needed (e.g., "leg pain — muscle or joint?").
- End with clear next-week instructions and list exactly which metrics to bring back.
- If external evidence was consulted, cite the source or name the guideline briefly; do not use generic "research says" language without a concrete source.

## Smart Scale Integration

For Phase 2 wearable + smart-scale review rules, see `references/phase-2-watch-scale-review.md`.

When the user provides body composition data (Xiaomi S400 or similar), incorporate these metrics:

| Metric | What to compute | Action |
|--------|----------------|--------|
| Body fat % | fat_kg / weight × 100 | Compare trend week-over-week. Is the deficit burning fat or just water? |
| Muscle mass (kg) | — | Track to ensure muscle preservation. A drop >2 kg in 4 weeks on 2,200 kcal suggests protein or deficit too aggressive |
| Visceral fat | — | 🚨 The most important health metric. 23 is very high. Drops fast on a deficit + cardio. Track every Sunday |
| Body water % | — | <45% = dehydration (scale readings unreliable). >48% = hydrated (readings trustworthy) |
| BMR (scale) | — | Use scale BMR over formula estimates. It accounts for actual body composition |
| Waist-to-hip | — | >0.9 = central obesity. Track as secondary trend |

**Target math from body comp:** If muscle mass is high (e.g., 76 kg at 178 cm), compute a realistic goal weight:
```
goal_kg = (muscle_mass - 3) / (1 - target_bf_pct)
```
The -3 kg accounts for expected muscle loss on a prolonged cut.

**Smart scale tracking table:** Add a weekly smart scale table to the review section so the user sees all body comp metrics trending.

## Inline Weight Column Pattern

After setting Week N+1 targets, update the main exercise tables at the top of the program file with a `W{N+1} Weight` column. This embeds the current week's targets directly in the exercise tables so the user doesn't need to scroll to the review section.

- Replace the section heading (e.g., "Week 1-2: Learn the Movements" → "Week 4 — Current Targets")
- Add `| W4 Weight |` column between Rest and Notes in every day's table header
- Populate with bolded targets
- Remove the obsolete generic progression table if it exists

## Handling Prescribed Weight Drops

When the user is told to drop weight on an exercise (e.g., "OHP: drop to 12 kg") and they ignore it (doing 20 kg instead), two possibilities:
1. **The drop was too conservative** — if they hit the higher weight with clean form this week after collapsing last week, accept the higher weight and adjust targets up
2. **Form regression** — if the jump is improbable (collapsed 20→15→10 last week, "Medium" at 20×3 this week), they're cutting ROM or using momentum. Compromise at a middle weight and demand form proof

Don't fight indefinitely. After 2 weeks of ignoring a prescribed drop, accept their working weight but flag it for form review.

## Phase Completion Review

When Phase N is complete (Week 4, 8, 12, etc.), the final review must also:

1. **Write the final review to the phase program file** (standard workflow from §7).
2. **Update `baseline-assessment.md`** with current weight, body comp, and phase transition notes.
3. **Create the next phase's files** under `{vault}/fitness/phase_{N+1}/`:
   - `phase{N+1}-program.md` — new program document
   - `training-log-phase{N+1}.md` — pre-filled log template with daily check-in tables for EVERY week
   - `smart-scale-tracking.md` — separate tracking file (do NOT embed in program)
4. **Cross-reference between files** — the program file references tracking/log by relative path, not inline content.
5. **Include a Phase N summary table** in the final review: each week's weight, protein adherence, ramping behavior, extra sets, and one key lesson.

### Phase 2 Program Specifics
When transitioning to Phase 2 (barbell foundation):
- Body composition baseline table from smart scale
- 4-week linear progression table for barbell lifts (bench, squat, OHP, deadlift, front squat)
- Warm-up protocol: empty bar practice + sets at 50%/70%/90% of working weight
- Continuation of run/walk progression from Phase 1
- Separate the tracking/log files — don't embed them in the program document

## Post-Review Consistency Audit

Before finalizing a weekly review, synchronize every place that carries next-week instructions:

1. **Active target tables:** update the current exercise tables with the new week, not just the review table. If the user overshot a load, use the actual clean working load as the next-week repeat target rather than blindly adding again.
2. **Progression tables:** update the barbell progression table and the run/walk progression table when a lift or cardio dose is intentionally repeated. A repeated dose must not remain represented as an automatic increase elsewhere in the file.
3. **New-lift gate:** for a first exposure to a barbell movement (especially deadlift), repeat the load when form evidence is limited. Progress only after clean, flat-back reps—not solely because the set was rated Medium.
4. **Form-gated exercises:** if the user repeatedly ignores a prescribed strict-form load (e.g., lateral raises), keep the lower load in the active target and state the objective form gate: full ROM, no shrug/torso swing, controlled eccentric. Do not accept an “Easy” rating as proof of valid reps.
5. **Cardio vs steps:** never solve a low step count by adding unscheduled running. Return to the prescribed run/walk duration and use easy walking, cycling, or swimming for extra activity.
6. **Wearable-settings sync:** when a step/PAI/sleep goal changes, update both the headline Daily Goals table and any day-by-day settings table in the watch note; stale duplicate targets are worse than no target.
7. **Date sanity:** validate the logged week/date against the current review date and neighboring rows. If a date is inconsistent (e.g., month typo), flag or clarify it; do not silently rewrite the user's historical data.
8. **Late or corrected data:** Panomete often fills in missing watch/scale data AFTER the review. Re-read the tracking file, then patch the review's metrics rows, flags, targets table, and memory — the vault must reflect the final truth, not just the chat reply.
9. **Warm-up compliance:** if a lift rated Medium last week comes back Hard at a heavier load, ask whether the warm-up was done. Panomete has admitted skipping warm-ups; the program links a `warmup-protocol.md` from every day, and its exercise tables carry a "Need Warmup" Yes/No column.

## Pitfalls

1. **Weight notation confusion.** Panomete sometimes logs warm-up sets as separate weights (15→20→20→25 for 3 sets). Clarify whether the first number is a warm-up or a working set. Ask: "is this warm-up + 3 working sets, or 4 working sets?"

2. **Vault path changes.** The Obsidian vault may move (it moved from `F:\projects\orlita_md` to `F:\obsidian_note\oralita_md` mid-session). Always use `search_files` if `read_file` returns "file not found." The user may restructure the vault (flat → subdirectories per phase). Use `find` or `search_files` to discover the current layout before writing files.

3. **User-requested changes mid-review.** If the user corrects a weight or adds context (e.g., "it was 20 kg, not 25"), rebuild the review with the corrected numbers before saving to the file.

4. **Avoid verification temp-file loops.** When the system flags files as "unverified," use inline `python -c "..."` instead of creating temp scripts. Temp scripts get flagged as additional changed paths, creating a cycle where deletion of the temp file triggers another verification demand.

5. **Program file ≠ history file.** Never append weekly reviews to the program file — Panomete explicitly moved reviews into `weekly-review-summary.md` so the program stays a pure live plan. Legacy embedded reviews should be extracted, not extended.

6. **Daily check-in tables for ALL weeks.** When creating log templates, every week needs its own daily check-in table (sleep, weight, protein). The user WILL notice if any week is missing — do not only include Week 1's check-in table and skip the rest. In a 4-week template, that means 4 separate check-in tables.

7. **Separate tracking from program.** The user prefers smart scale tracking in its own file (`smart-scale-tracking.md`) rather than embedded in the program document. The program file should reference it by relative path, e.g., "Log every Sunday → `smart-scale-tracking.md`." Same applies to training logs — keep them separate from program documents rather than duplicating tables.
