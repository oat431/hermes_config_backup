# Training Log Template

After writing a program, always provide a fillable log template. The user fills it during sessions and brings it back for review.

## Log Structure

One file per program phase (4 weeks). Each week contains:

1. **Exercise tables** for each training day — pre-filled with exercise names, blank weight/reps/notes columns
2. **Daily check-in table** — sleep hours, body weight, protein hit?, notes

## Exercise Table Format

```
### Mon — Upper
| Exercise | Weight (kg) | Sets × Reps | Notes |
|----------|-------------|-------------|-------|
| Dumbbell Bench Press | | 3×8 | |
```

- Exercise names must match the program exactly
- "Weight (kg)" column: the user fills in per-set weights (e.g., `12, 12, 12` or the working weight)
- For bodyweight exercises (plank, dead bugs): put `—` in the weight column
- Run/Walk intervals: use a "Time" note instead of weight (e.g., `24 min`)

## Daily Check-In Format

```
| Day | Sleep (hrs) | Body Weight (kg) | Protein hit? | Notes |
|-----|-------------|-------------------|--------------|-------|
| Mon | | | | |
```

- **Sleep:** hours, rounded to nearest half
- **Body weight:** morning weight, same scale, same conditions
- **Protein hit?:** yes/no or grams if known
- **Notes:** anything unusual — bad sleep, missed meal, extra cardio, feeling sick

## Instruction Header

Always include a brief usage guide at the top of the log file:

```
Fill in **Weight** and **Reps** after every set. If you did 3 sets of 8 at 10 kg, 
write `10 × 8, 8, 8`. If reps dropped (e.g., 8, 8, 6), write that — it tells me 
where you're failing. Notes column is for anything weird: "felt shoulder," 
"too easy," "gym packed, used alt."
```

## Rep Recording Convention

- Record all working sets: `12 × 8, 8, 7` (weight × set1, set2, set3)
- Warm-up sets are NOT recorded in the log
- If all sets completed at target reps: `12 × 8, 8, 8`
- If reps dropped: `12 × 8, 8, 6` — the drop-off is the diagnostic signal

## File Naming

`training-log-week{N}.md` or `training-log-template.md` if pre-filling all 4 weeks.
