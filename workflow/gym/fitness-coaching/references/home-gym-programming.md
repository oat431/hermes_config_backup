# Home Gym Programming — Phase 3+ (post-2026-08-23)

**Status 2026-08-31:** monthly gym membership REINSTATED — the home-first arrangement lasted one week (W9 lost to flu-A; user judged home gym insufficient). Gym day notes are primary; home notes are storm/gym-closed backup. Keep the design decisions below for backup days and any future home phase.

## Equipment reality

In hand: electric treadmill, 10 kg kettlebell, 2 kg dumbbells ×2, push-up machine, sit-up machine, yoga mat.

Planned tier-1 buys (~500–2,000 ฿, Lazada/Shopee/Decathlon/Mr. DIY):
1. **Spinlock dumbbell handles + plates** (2 handles, 4×5 + 4×2.5 + 4×1.25 kg) — unlocks pressing/rowing/RDL at real loads. Buy plates, never fixed dumbbells.
2. **Resistance band set** (tube + door anchor) — face pulls, band rows, pallof.
3. **Doorway pull-up bar** — hangs now, negatives later; check door frame type first.

Tier 2 (later): adjustable bench, 16 kg kettlebell. Tier 3 (only if day-pass gyms die entirely): barbell + rack (~10,000+ ฿, needs floor space). What NOT to buy: fixed dumbbell sets, spring-grip bars, more ab machines, EMS gadgets.

## Schedule (W9+, confirmed with user)

Mon Upper · Tue Lower · Wed run/walk + core · **Thu/Fri unavailable (work)** · Sat full body · **Sun easy treadmill cardio 30–40 min (Zone 2)** — the marathon-base day that replaced the old Sunday rest. User chose this explicitly over Sunday-as-rest.

## Loading strategy — the core idea

- **Bodyweight IS the load at ~120 kg.** Bulgarian split squat (rear foot elevated) and push-ups are the money movements. Do not chase barbell-equivalent loading at home.
- Rep-range progression: 8→12 reps (or 10→15), then +1.25–2.5 kg/hand or a harder push-up progression, back to the bottom of the range. Tempo (2-sec eccentric) is the load multiplier.
- Push-up progression ladder: wall → incline → knee → full → diamond.
- KB 10 kg: goblet squat 3×12, one-arm row 3×10, suitcase carry 2×30 s/side, swings 3×12 (hinge gate passed at DL 70 Easy).
- 2 kg DBs: lateral raises (strict form practice) only — everything else needs handles. Never bump a 2 kg form exercise's load because it's "Easy"; the strict gate is the point.

## Barbell maintenance (the honest trade-off)

Home cannot load squat 42.5 / bench 45 / DL 70. Barbell lifts are MAINTAINED, not progressed:

- `daily-workouts/gym/gym-day-barbell-session.md` holds day-swap blocks (Mon upper / Tue lower / Sat full body) at W8-earned weights: bench 45 (47.5 was ramped=invalid), OHP 35, squat 45 attempt (clean 42.5 earned), DL 75, front squat 40.
- Rule: **3 weeks without a day-pass gym → book one.** Pattern rot is the real risk of home phases.
- Gym sessions log in the same training log with a "(gym)" tag.
- Warm-up ladders for the gym note: ≈50/70/90% rounded to nearest 2.5 kg.

## Pitfalls specific to home phases

- Never prescribe KB/DB "equivalents" of barbell lifts at 10 kg — that's warm-up weight for him; use single-leg / tempo / high-rep instead.
- KB swings only after the hinge gate (clean flat-back heavy DL).
- Treadmill: user must NOT hold the handles — grip kills wrist-HR accuracy; distance from the console.
- No daily run-walk at 120+ kg — dose control; extra movement = walking (steps column).
- Day notes split `daily-workouts/home/` (numbered 1_Monday..5_Sunday) vs `daily-workouts/gym/` — user requested the two-folder structure for day-pass gym days.

## Flipping gym↔home priority (2026-08-31 pattern)

When the user re-gains gym access and home becomes backup:
1. Write full per-day GYM notes (`daily-workouts/gym/1_Monday..4_Saturday`) with barbell ladders + form GIFs; delete any single "gym-day swap" note it supersedes and grep for references to it.
2. Demote every home note with a banner directly under the title: `> ⚠️ **Backup note.** Gym is primary — use this only when the gym is closed / storm. Gym version: [[daily-workouts/gym/N_Day]]`.
3. Rewrite the program overview: purpose, schedule table, a backup rule (one backup day fine; 2+ forced-home days in a row → message the coach), and re-label the shopping list as backup-only/optional.
4. Log convention flips: gym sessions need no tag (default again); home backup sessions get a "(home)" note.
