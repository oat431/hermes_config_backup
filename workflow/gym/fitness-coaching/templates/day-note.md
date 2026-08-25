# Day Note Template — per-training-day gym file

Panomete's W8+ workflow: at the gym he opens ONE file for the day and follows it top to bottom. One note per training day, numbered so they sort in session order: `1_Monday.md`, `2_Tuesday.md`, `3_Wednesday.md`, `4_Saturday.md`, stored in `phase_N/daily-workouts/`.

Copy this template for each training day and fill in the current week's targets. Warm-up goes INLINE under each exercise — never only in a separate warmup file.

```markdown
---
date: YYYY-MM-DD
tags: [fitness, phase-N, daily-workout, <day>]
---

# <Day> — <Focus>

Focus: <key lifts>. Time: ~<XX> min.

**Before anything:** general warm-up 5–8 min (cycle/walk + dynamic moves) → `[[warmup-protocol]]`

---

## 1. <Barbell compound>

- **Warm-up ladder:** <~50%> kg × 5 → <~70%> kg × 3 → <~90%> kg × 2 (rest 60–90 sec between ramp sets)
- **Working:** 3 × 5 @ **<target> kg** — rest 2–3 min
- **Standard:** <execution cue; one uniform load across work sets>

## 2. <First machine/accessory for a muscle group>

- **Warm-up:** 1 light set — <~50–60%> kg × 10–12 (first <group> exercise; rest ~60 sec after)
- **Working:** <sets × reps> @ **<target> kg** — rest <90/60 sec>
- **Standard:** <execution cue>

## 3. <Same muscle group, later in session>

- **Warm-up:** none — <muscle> is warm from <earlier exercise>
- **Working:** <sets × reps> @ **<target> kg** — rest <sec>
- **Standard:** <execution cue>

---

Done → log working sets in `[[training-log-phase<N>]]`. Back to `[[phase<N>-program-overview]]`.
```

## Conventions baked into this template

- **Barbell ladder:** ≈50% ×5 / ≈70% ×3 / ≈90% ×2 of the working weight, rounded to nearest 2.5 kg; empty bar when 50% < 20 kg. Rest 60–90 sec between ramp sets, then the full prescribed rest before the first working set.
- **Light ramp set** (first machine/accessory per muscle group): ~50–60% of working load ×10–12, rest ~60 sec after. Later exercises for the same group: "Warm-up: none — <reason>".
- **Run/walk warm-up:** 3–5 min brisk walk, counts inside the session time.
- **General warm-up:** no rest — continuous movement.
- Warm-up sets are never logged as working sets.
- **When a weekly review changes a working weight, RECOMPUTE the inline ladder in the day note.** A stale ladder is worse than no ladder.
- Week headings in day notes are per-week; update all four notes after every weekly review, not just the review summary.

## Obsidian pitfalls observed with these files

- **Renames do not auto-update agent-written wikilinks.** Panomete renamed `Monday.md` → `1_Monday.md` in Obsidian and no `[[daily-workouts/Monday]]` link was rewritten. After any user-side rename, grep the vault for stale links and patch every referencing file (overview, warmup-protocol).
- **Obsidian pads table columns on save**, which breaks exact-string patches. Re-read the file immediately before patching; prefer `write_file` full rewrites when the file keeps changing shape.
- Never assume the vault file tree matches the last session — `search_files` first, always.
