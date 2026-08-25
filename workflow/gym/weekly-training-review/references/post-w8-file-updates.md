# Post-W8 File Update Flow — weekly review targets

Since Panomete's W8 vault restructure, a weekly review must update THREE file targets (not one program file). Some SKILL.md sections (e.g. "Inline Weight Column Pattern") still describe the old single-file pattern — treat this file as authoritative for phases with `daily-workouts/`.

## The three targets

### 1. `weekly-review-summary.md` (phase dir)
- Append `## Week N Review (date range)`: metrics table, performance→targets table, flags list, nutrition decision.
- Update the trailing "Current status after Week N" bullets (calories, step target, run/walk dose, form gates).
- If Panomete fills in watch/scale data AFTER the review (he does this often), re-read the tracking file and patch the review's metrics rows + flags + targets table + memory. The vault must reflect the final truth.

### 2. `phase{N}-program-overview.md`
- Barbell progression map: mark intentional repeats with reason, e.g. `**35 kg (repeat — Hard)**`, `**42.5 kg (repeat — ramping fix)**`.
- Run/walk progression table: keep repeats consistent ("30 min — repeat; log the minutes") — never show an automatic increase for a dose that was held.
- Nutrition section: new kcal number when a SOUL trigger fires (e.g. 2,200 → 2,050 after 3-week flat 7d MA), with the revert condition stated.
- Week heading + footer ("Current live target: Week N").
- Do NOT append review history here.

### 3. `daily-workouts/*.md` (all four day notes)
- For EVERY changed exercise: update the working weight AND recompute the inline warm-up ladder (≈50% ×5 / ≈70% ×3 / ≈90% ×2 of the NEW working weight, rounded to nearest 2.5 kg; empty bar if 50% < 20 kg).
- Update light ramp-set loads for first-of-group machines (~50–60% of new working load).
- Keep "Warm-up: none — <reason>" lines accurate when exercise order changes.
- Rest columns/notes: barbell ladder 60–90 sec between ramp sets; light ramp set rest ~60 sec after; working rest unchanged (2–3 min barbell / 90 sec machine / 60 sec isolation).

## Consistency audit additions for the day-note era

- A repeated load (OHP Hard, squat ramping-fix) must appear as a repeat in BOTH the overview map and the day note target — no silent auto-increase anywhere.
- Warm-up ladder is part of the prescription: if the day note says 45 kg working but the ladder still says "42.5 × 2" from last week, that is a stale file.
- After any user-side rename of day notes (he numbers them: `1_Monday.md`…), grep the vault for the old link names and patch the overview + warmup-protocol references — Obsidian does NOT auto-update agent-written wikilinks.

## Known data-quality patterns to keep handling (W5–W7 history)

- Run/walk minutes often unlogged ("Run/Walk Easy" is not data) — demand the number, hold the dose at 30 min until evidence exists.
- Watch metrics arrive late or missing (steps/PAI/RHR) — request explicitly each review; the W7 row was filled only after prompting.
- Resting HR: values like "10" are a wrong tile, not bpm. Real RHR 57/59 → 78 bpm jump = fatigue + heat signal, not danger; act only if elevated 2+ weeks.
