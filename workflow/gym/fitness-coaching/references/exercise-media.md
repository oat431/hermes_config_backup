# Exercise Media — finding, verifying, embedding demos

How to source demo images/GIFs for exercise and form notes in the fitness vault.

## Source of truth: `hasaneyldrm/exercises-dataset`

- GitHub repo. `data/exercises.json` is a flat list of ~1,300 records (17 MB — never load it into context).
- Record fields: `id`, `name`, `category`, `body_part`, `equipment`, `instructions`, `instruction_steps`, `muscle_group`, `secondary_muscles`, `target`, `image` (`images/<id>-<media_id>.jpg`), `gif_url` (`videos/<id>-<media_id>.gif`), `media_id`, `attribution` (© Gym Visual).
- Direct GIF URL: `https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/videos/<id>-<media_id>.gif`
- The workout notes already embed this dataset — keep new embeds on it so rendering matches in Obsidian.

## Query workflow

1. Download to scratch: `curl -s -L -o exercises.json https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/data/exercises.json`
2. Query with Python: `json.load`, match `name.lower()` against keywords, print `id | name | equipment | body_part | gif_url`.
3. Names follow GymVisual conventions — search synonyms, not exact drill names (`romanian deadlift`/`good morning` for hip hinge; `glute bridge` returns several variants).
4. Known gaps and substitutes: band pull-apart, wall slide and bird dog are **not** in the dataset — use `scapular pull-up` (0688), `scapula push-up` (3021), `low glute bridge on floor` (3013), `farmers walk` (2133), or a verified web image for the missing drill.

## Machine variants used as program defaults

| Exercise | Record | GIF file |
|---|---|---|
| Lever shoulder press | 0603 | `0603-67n3r98.gif` |
| Lever chest press | 0577 | `0577-T0yTjgW.gif` |
| Lever incline chest press | 1299 | `1299-jHAnWmT.gif` |
| Lever seated row | 1350 | `1350-7I6LNUG.gif` |
| Lever narrow-grip seated row (alt) | 0588 | `0588-IGjKj1v.gif` |
| Lever seated leg curl | 0599 | `0599-Zg3XY7P.gif` |
| Lying leg curl (alt) | 0586 | `0586-17lJ1kr.gif` |
| Lever leg extension | 0585 | `0585-my33uHU.gif` |
| Lever standing calf raise | 0605 | `0605-ykUOVze.gif` |
| Sled calf press on leg press | 1391 | `1391-ykHcWme.gif` |
| Sled hack squat | 0743 | `0743-Qa55kX1.gif` |
| Smith squat | 0770 | `0770-jFtipLl.gif` |

## Finding images outside the dataset

- SearXNG image search: call the search tool with `categories: "images"`; each result carries an `Image Source:` direct URL.
- Verify every URL before embedding: `curl -s -o /dev/null -w "%{http_code} %{content_type}" -L --max-time 25 "<url>"` → expect `200 image/*`.
- Known-good static sources: `hingehealth.com` ctfassets (abdominal bracing), `proactivehealth.ca` / `wasilzafar.com` (plumb-line posture), `strengthlog.com` (band pull-apart GIF). Hotlinks can die — swap the source if one breaks.

## Embedding in Obsidian notes

- Remote embeds: `![|200](url)` — width in px. GIFs animate in Obsidian; the Hermes desktop chat also renders remote image URLs.
- Keep a **Sources & licensing** footer in any note that embeds them (dataset GIFs are © Gym Visual).
- Group a visual guide by section (bracing, hinge, squat, ankle mobility, scapular, core) with 2–3 execution cues per picture — the user reads it phone-in-hand at the gym.
