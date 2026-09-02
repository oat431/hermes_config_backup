# Fitness Calculation Formulas

## BMR — Mifflin-St Jeor (male)

```
BMR = 10 × weight_kg + 6.25 × height_cm − 5 × age + 5
```

## TDEE Multipliers

| Activity Level | Multiplier |
|---------------|------------|
| Sedentary (0-1 sessions) | 1.2 |
| Light (1-3 sessions) | 1.375 |
| Moderate (3-5 sessions) | 1.55 |
| Heavy (5-7 sessions) | 1.725 |

Default for 4x/week: **1.55**.

## BMI

```
BMI = weight_kg / (height_m)²
```

## Calorie Deficit

- **BMI >30, untrained:** TDEE − 800 to 1000 kcal.
- **BMI 25-30:** TDEE − 500 to 700 kcal.
- **Trained, any BMI:** TDEE − 300 to 500 kcal max.

## Protein Floor

- **Deficit:** 1.3−1.6 g/kg bodyweight (preserve muscle).
- **Maintenance:** 1.2−1.5 g/kg.
- **Bulk:** 1.6−2.0 g/kg.

## Weight Loss Rate

- 1 kg fat ≈ 7,700 kcal deficit.
- 500 kcal/day deficit ≈ 0.45 kg/week.
- 1000 kcal/day deficit ≈ 0.9 kg/week.

## Active-Balance Guards (from SOUL.md)

| Condition | Action |
|-----------|--------|
| 7d MA weight drop >0.6 kg/week × 2 weeks | +200 kcal/day |
| 7d MA weight drop <0.15 kg/week × 3 weeks | −150 kcal/day or audit |
| Same lift failed twice (same weight/reps) | −10% weight, restart LP |
| Cardio >90s off expected pace × 2 sessions | Flag deload |
| Sleep <6h average for week | Cut one quality session |
