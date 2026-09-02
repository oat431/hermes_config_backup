# Thai Freestyle Food Tracking (2,050 kcal / 160 g protein)

System for Panomete's cut while eating Thai street food. Replaces app-logging: apps fail in Thailand (no labels, ±30% vendor variance, unreliable databases). Design principle: **log structure daily, audit with real numbers weekly.**

## Anchors (count once, forget)

- **Protein anchor:** every meal starts with palm-size lean protein. 160 g/day = 640 kcal. Portion amounts in `meal-templates-160g-protein.md` (protein rows valid; its kcal totals are 2,400-era, ignore them).
- **Rice anchor:** 1 ladle (thap pi) ≈ 130 g cooked ≈ 170 kcal. **Budget: 3 ladles/day.**
- **Fat anchor:** ~60 g/day visible fat (cooking oil, egg yolks, curry cream) — this is what makes the same dish swing ±300 kcal between stalls.

## Day structure (~2,050 kcal)

| Slot | What | ~Kcal |
|------|------|-------|
| Breakfast — fixed | 3 boiled eggs + 1 scoop whey + fruit | ~500 |
| Lunch — freestyle | dish-table item with protein anchor | ~650 |
| Dinner — freestyle | dish-table item with protein anchor | ~650 |
| Snack | moo ping ×2 or Greek yogurt 200 g | ~250 |

Free at any size: clear soups, vegetables, chili/vinegar/lime. Sugary nam jim is NOT free.

## Thai dish table (street portions, ±20% estimates)

| Dish | ~Kcal | ~Protein |
| ---- | ----- | -------- |
| Khao man gai — skin off, less rice oil | 600 | 35 g |
| Khao man gai — standard (skin on) | 750 | 35 g |
| Pad krapao moo kai dao + rice | 650 | 30 g |
| Khao pad moo | 600 | 20 g |
| Kuay teow nam (noodle soup) | 400 | 18 g |
| Gai yang ¼ chicken — skin off | 350 | 40 g |
| Moo ping — 1 skewer | 140 | 9 g |
| Som tam Thai (no sticky rice) | 150 | 4 g |
| Sticky rice — 1 fist | 250 | 5 g |
| Tom yum goong — clear | 200 | 25 g |
| Tom kha gai — coconut milk | 400 | 25 g |
| Curry (massaman / panang) + rice | 700 | 30 g |
| Pad thai gai | 600 | 20 g |
| Kai jeow — 2 eggs, pan-fried | 300 | 13 g |
| Pla kapong neung manao (steamed fish) | 400 | 45 g |
| Larb moo / nam tok | 300 | 28 g |
| Gai tod — 1 piece fried chicken | 400 | 20 g |

**7-Eleven rule:** packaged food carries a real label — the label beats this table; when unsure, 7-Eleven beats the stall.

## Weekly audit

- 1 day/week (Thursday): count everything via dish table; weigh one rice ladle once to calibrate.
- Day lands 2,000–2,200 → anchors calibrated, trust them all week.
- First 3 weeks weekly, then monthly.

## Scoring (kcal column in daily check-in)

- ✓ = day within structure (~2,000–2,200) · ▲ = over (fried/dessert/liquid kcal) · ⚠ = under (missed protein anchor)
- Target: 6/7 ✓ per week. Planned ▲ days are fine (80/20 rule from `foods-to-avoid.md`).

## Boredom question (user asked "eat same meal every day like bodybuilders?")

Answer: **not required.** What the cut requires is kcal consistency, not identical food. Bodybuilders rotate within a fixed *structure*, not identical meals — and they're paid to suffer. Prescribe: two fixed anchors + two free slots from the dish table = 30+ combinations. Boredom kills adherence; adherence is the whole game.

## Calibration step

Ask for the user's 5 most-eaten dishes NOT in the table; estimate honestly (±20%), add as custom rows. The live food-log file carries a blank custom-rows table for this.
