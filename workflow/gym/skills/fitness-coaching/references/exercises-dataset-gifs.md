# Exercise Form GIFs — hasaneyldrm/exercises-dataset

Reusable workflow for linking form animations into Panomete's day notes (or any program note).

## Dataset facts

- Repo: https://github.com/hasaneyldrm/exercises-dataset — 1,324 exercises, MIT + media terms (media © GymVisual).
- Metadata: `data/exercises.json` — list of `{id, name, category, body_part, equipment, instructions{en,it,...}}`.
- Animation GIFs live in `videos/{id}-{random}.gif` — NOT `images/` (180×180 JPG thumbnails, same hash suffixes).
- Equipment naming quirks: machines = "leverage machine", leg press = "sled machine"; barbell/dumbbell/cable/body weight as expected.
- README shows example GIF paths (e.g. `videos/0025-EIeI8Vf.gif` = barbell bench press).

## Workflow

1. Get the full file tree in ONE call (avoids the paginated contents API):
   `curl -s "https://api.github.com/repos/hasaneyldrm/exercises-dataset/git/trees/main?recursive=1"` → build map `id → videos/{filename}` by splitting the filename on `-` (leading part is the exercise id).
2. Download `data/exercises.json` from the raw URL.
3. Match program exercises to dataset names by substring — BUT first-pass hits are often the wrong variant ("sled 45 degrees ONE leg press", "cable ONE arm tricep pushdown", "bodyweight incline side plank"). Print candidate lists per query and pick manually.
4. Verify every URL with a HEAD request (HTTP 200) before embedding. raw.githubusercontent.com URLs are stable.
5. Embed in Obsidian with resize syntax: `![form|150](url)` — renders an inline animated preview, click for full size. Requires internet at the gym; offer to download the GIFs into the vault (`daily-workouts/assets/`) for offline use.

## Known gaps + substitutions (Phase 2 mapping)

- **Face pull:** NOT in the dataset — leave unlinked, never fake a URL.
- **Plain plank:** not present; use "front plank with twist" (0464) and note to ignore the twist.
- **Plain side plank:** not present; "side bridge v. 2" (0705) is the classic alternative name.
- **Strict OHP:** use "barbell standing close grip military press" (1456) — closest standing barbell press.
- **Chest-supported row:** "lever t bar row" (0606) — same chest-pad pattern.
- **Pallof press:** only band versions exist (0979 band horizontal pallof press) — same anti-rotation pattern as the cable version.
- **Reverse lunge:** named "dumbbell rear lunge" (0381).
- **Lat pulldown:** "cable lat pulldown full range of motion" (2330).
- **Leg press:** "sled 45° leg press" (0739) — avoid 1425 (one-leg variant).

## Verified Phase 2 URLs (all HTTP 200 on 2026-08-17)

| Exercise | URL |
|---|---|
| Bench Press | videos/0025-EIeI8Vf.gif |
| OHP | videos/1456-wdRZISl.gif |
| Chest-Supported Row | videos/0606-aaXr7ld.gif |
| Tricep Pushdown | videos/0241-gAwDzB3.gif |
| Back Squat | videos/1436-Gnfo4FM.gif |
| Leg Press | videos/0739-10Z2DXU.gif |
| Lying Leg Curl | videos/0586-17lJ1kr.gif |
| Calf Raises | videos/0605-ykUOVze.gif |
| Plank | videos/0464-CosupLu.gif |
| Dead Bug | videos/0276-iny3m5y.gif |
| Pallof Press | videos/0979-9pa4H5m.gif |
| Side Plank | videos/0705-RKjH6Lt.gif |
| Dumbbell Curls | videos/0294-NbVPDMW.gif |
| Lateral Raises | videos/0334-DsgkuIt.gif |
| Deadlift | videos/0032-ila4NZS.gif |
| Front Squat | videos/0042-zG0zs85.gif |
| Lat Pulldown | videos/2330-LEprlgG.gif |
| Incline DB Press | videos/0314-ns0SIbU.gif |
| Reverse Lunges | videos/0381-SSsBDwB.gif |
| Seated Cable Row | videos/0861-fUBheHs.gif |

Full prefix: `https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/`
