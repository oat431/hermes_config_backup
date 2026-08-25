# Vault Restructure W8 — program split into overview + day notes

Panomete restructured Phase 2's program file in Week 8. This is now the canonical layout for current and future phases. The SKILL.md tree may lag behind this file — this is authoritative.

## Why

Gym workflow: Panomete opens ONE file per training day and follows it top to bottom. A single big program file forced scrolling through rules and history. Also: reviews mixed with live targets made the plan unreadable.

## Structure (phase_N/)

| File | Contents | Updated when |
|------|----------|--------------|
| `phase{N}-program-overview.md` | Schedule, barbell progression map, run/walk progression, progression rules, logging conventions, session protocol, nutrition/recovery targets, kettlebell section, file links | Weekly review (live numbers only) |
| `daily-workouts/1_Monday.md` … `4_Saturday.md` | ONE note per training day, numbered to sort in session order. Exercises in session order; warm-up ladder (concrete weights) INLINE under each exercise; "Warm-up: none — <reason>" where nothing needed | Weekly review (working weights + ladders) |
| `warmup-protocol.md` | GENERAL warm-up rules only: 5–8 min general warm-up, ladder template (50/70/90%), accessory ramp rule, run/walk walk-warm-up, never-log-warmups rule | Rarely (rules don't change) |
| `training-log-phase{N}.md` | Completed sessions + daily check-ins | User, daily |
| `smart-scale-tracking.md` | Sunday BIA + watch metrics + phase targets | User, Sundays |
| `weekly-review-summary.md` | ALL historical weekly reviews + "Current status after Week N" block | Coach, every Sunday |

## Warm-up rest conventions (asked and answered in W8)

| Warm-up type | Rest | Why |
|---|---|---|
| Barbell ladder (50/70/90%) | 60–90 sec between ramp sets, then full prescribed rest before first working set | Light sets = rehearsal, not fatigue |
| Light ramp set (first machine/accessory per group) | ~60 sec after the set | Brief catch, then working sets |
| General warm-up (5–8 min) | None | Continuous movement by design |

## Weekly review update flow (three targets, no exceptions)

1. `weekly-review-summary.md` — append review; update "Current status" bullets.
2. `phase{N}-program-overview.md` — progression map (mark repeats like "35 kg (repeat — Hard)"), run/walk table, calorie number if SOUL trigger fired, week heading.
3. All four day notes — every changed exercise: working weight AND recomputed inline ladder (≈50/70/90% of new weight, nearest 2.5 kg), plus light ramp-set loads.

## Pitfalls specific to this structure

- **Obsidian renames don't auto-update wikilinks written by the agent.** User renamed day notes to numbered names mid-session; all `[[daily-workouts/Monday]]` links stayed stale. After renames, grep for old link patterns and patch every referencing file.
- **Obsidian table padding breaks exact-match patches** (columns get padded with whitespace on save). Re-read immediately before patching tables; full `write_file` rewrite is often safer.
- User edits vault mid-session: check file timestamps/`search_files` before assuming layout.
- User may create empty folders alongside (e.g. an empty `program/` folder while discussing). Consolidate, don't duplicate: pick the agreed name, remove the empty folder, and say so.
