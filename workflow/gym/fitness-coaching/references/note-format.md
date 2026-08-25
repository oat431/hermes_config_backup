# Baseline Assessment Note Format

Write to `{vault}/fitness/baseline-assessment.md`. Template:

```
---
date: YYYY-MM-DD
tags: [fitness, baseline]
---

# Baseline Assessment

## Body Metrics
| Metric | Value |
|--------|-------|
| Age | N |
| Weight | N kg |
| Height | N cm |
| BMI | N |
| BMR (Mifflin-St Jeor) | N kcal |
| Est. TDEE (moderate activity) | ~N kcal |

## Goals
1. **Primary:** goal
2. **Secondary:** goal (if any)
3. Current metrics relevant to goals

## Training Status
- Training age: N days/months/years
- Equipment: description
- Schedule: N days/week
- Current lifts: description
- Injuries: list or "none known"

## Recovery
- Sleep: N hours/night
- Nutrition: description

## Initial Targets

### Calories
- Deficit target: N kcal/day (N kcal deficit)
- Protein: N g/day
- Guard: deficit guard rule

### Weight Loss Trajectory
- Starting: N kg
- Target rate: N kg/week
- First milestone: N kg (estimated N weeks)

### Marathon Pathway (if applicable)
- Phase 1 (0-6 months): description
- Phase 2 (6-12 months): description
- Phase 3 (12-18 months): description
- Rule: weight gates

---

*Last updated: YYYY-MM-DD — Coach (Hermes gym profile)*
```

## Key rules

- The YAML frontmatter must be valid (no unquoted colons in values).
- All numeric values must match calculated results exactly (BMR, BMI, TDEE).
- The "Guard" field documents the active-balance rule being applied.
- Marathon pathway only included if endurance is a stated goal.
