# Tracking Template Design — Conventions & User Preferences

Built 2026-08-20/23 (data-gap audit → 8-file template suite → Phase 3 live files). Future template or phase-file work should follow these instead of re-litigating them.

## The 8-file template suite (global: `F:/obsidian_note/oralita_md/templates/fitness/`)

| File | Role |
| --- | --- |
| tracking-index.md | Map of templates → which live Phase 3 file each becomes |
| daily-check-in.md | Sleep, weight, protein ✓/✗, kcal ✓/▲/⚠, steps, notes |
| training-log-week.md | Session tables; the one-load rule written in |
| run-walk-log.md | Minutes + distance + avg HR per cardio session |
| blood-pressure-log.md | Measurement protocol + schedule + classification |
| blood-panel-baseline.md | Panel request list + results table + glossary |
| body-metrics.md | BIA weekly + tape monthly + photos monthly (ONE file) |
| food-log.md | Thai anchors + dish table + weekly audit |

The suite was MOVED (not copied) to the GLOBAL Obsidian templates folder `F:/obsidian_note/oralita_md/templates/fitness/` by another session — `fitness/template/` no longer exists. When the user says "create by this template", read the global copy and conform the live phase files to it.

## Measurement frequencies — user asked; answers are settled

- **BP:** daily only in the baseline week (first 7 days, 2 readings 1 min apart, record both + average), then Sunday + Thursday. Never daily forever — ±5–10 mmHg day-to-day noise; the weekly average is the trend. Exception: 2 sessions ≥140/90 → daily for a week + doctor visit.
- **Blood panel:** baseline now → 6-month retest. Monthly draws are pointless (HbA1c is a 3-month average; lipids swing ±5–10% biologically). Conditional: a ▲ marker → recheck that one marker at 3 months.
- **Run/walk:** 1 structured session/week at 120+ kg (Wed), plus Sun easy treadmill once home-based. Daily walking lives in the steps column. No daily run-walk — joint risk.
- **Body metrics:** BIA weekly (Sunday, fasted), tape + photos monthly (1st Sunday). One file because all three happen in one Sunday sitting — the user renamed the file to `body-metrics.md` for exactly this reason. Later split (2026-08-23) when the vault restructured: weekly BIA → phase `logs/weekly/smart-scale-weekly.md`; tape + photos → vault-root `body-measurements-monthly.md`. The template file still bundles all three as a design.

## User preferences (encode in files, don't re-ask)

- **Plain-language glossaries required** for medical aliases: full name + "what it actually is" + target value to maintain. The user asked for this explicitly ("i am little dummy"). Put the glossary under the cadence/retest section.
- **Estimates-first food tracking:** dish-table estimates (±20%) are the default system; NO calibration homework. The weekly audit (Thursday) is a tiebreaker that activates only when the scale stalls for 2–3 weeks. User chose this explicitly over custom-dish calibration.
- **Kcal scored, not counted:** check-in column uses ✓ (day assembled within ~2,000–2,200 structure) / ▲ (over) / ⚠ (under), 6/7 ✓ = target. Exact daily kcal logging does not survive Thai street food.
- **Single file per function group** — merged scale+tape+photos; don't fragment into tiny files.
- BP cuff type still UNCONFIRMED (upper-arm valid, wrist unreliable) — ask before trusting BP data.

## Thai food system method (from food-log.md)

- Anchors: protein 160 g (640 kcal) + 3 rice ladles/day (thap pi ≈ 130 g cooked ≈ 170 kcal) + ~60 g visible fat.
- Day structure ~2,050: breakfast fixed (3 eggs + whey + fruit ≈ 500), lunch/dinner freestyle from the dish table (~650 each, protein anchor first), snack ~250.
- Dish table: 17 common street dishes with kcal + protein estimates (±20%). 7-Eleven rule: packaged labels beat estimates.
- Thursday audit: count everything + weigh one rice ladle; landing 2,000–2,200 = anchors calibrated. First 3 weeks weekly, then monthly.
- The boredom answer (user asked directly): bodybuilders eat repetitive STRUCTURES, not identical meals — two fixed anchors + two free slots from ~17 dishes = variety without daily math.
