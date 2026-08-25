---
name: presentation-design
description: "Build colorful, decorated PPTX presentations with themes."
version: 1.0.0
author: deck
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [pptx, powerpoint, design, presentation, color, layout, visual]
    category: creative
    related_skills: [powerpoint, claude-design, baoyu-infographic]
---

# Presentation Design

Design principles and practical patterns for building **visually rich**
PPTX presentations using python-pptx (via the `powerpoint` skill's
`pptx_create.py`). This skill covers the *design layer* — color,
decoration, layout, visual hierarchy — while `powerpoint` covers the
*mechanical layer* (JSON spec format, create/read/edit commands).

## When to Use

- Building a presentation that needs to look polished, not just functional.
- Adding color themes, decorative shapes, section backgrounds, accent bars.
- Choosing color palettes for educational or informational decks.
- Converting a plain text-heavy deck into a visually engaging one.

## Pitfalls

### ⚠️ Units: Inches, Not Points

`pptx_create.py` uses `Inches()` for ALL shape positions and sizes.
The JSON spec values are **inches**, not points.

| What you mean | Points | Inches (what to put in spec) |
|---|---|---|
| Full slide width (16:9) | 960 | 13.333 |
| Full slide height (16:9) | 540 | 7.5 |
| 8pt decorative bar | 8 | 0.111 |
| 6pt thin accent | 6 | 0.083 |
| 50pt shape | 50 | 0.694 |

**Conversion:** inches = points ÷ 72

If you put `960` meaning "960 points = full width", the shape will be
960 inches wide — invisible or broken. Always convert first.

### ⚠️ pptx_read.py Does NOT Report Decorations

`pptx_read.py --outline` reports texts, tables, images, charts, and
notes — but **NOT** background colors or decorative shapes. To verify
that backgrounds and shapes were applied, read the file directly:

```python
from pptx import Presentation
prs = Presentation('deck.pptx')
for slide in prs.slides:
    bg = slide.background.fill
    print(f'bg_type={bg.type}, shapes={len(list(slide.shapes))}')
```

### ⚠️ Blank Layout for Full Control

When using decorative shapes and custom backgrounds, use `"layout": "blank"`.
Title and title_content layouts have placeholders that may overlap with
your decorations. For section divider slides, always use blank.

## Design Patterns

### Color-Coded Sections

Give each major section its own color identity. This creates visual
wayfinding — the audience knows where they are in the deck by the color.

**Structure:**
- Section divider slide: bold solid background in the section color
- Content slides within section: light tinted background (10-15% opacity feel)
- Top accent bar: full-width thin stripe in the section color
- Left accent bar: short colored line under the title area

**Example palette (5 sections):**

| Section | Bold BG | Tinted BG | Accent |
|---|---|---|---|
| Opening/Title | `1B2A4A` (navy) | `F8F9FA` (light gray) | `FF6B6B` (coral) |
| Reviews | `FF6B6B` (coral) | `FFF5F5` (light pink) | `FF6B6B` |
| Storytelling | `4ECDC4` (teal) | `F0FAF9` (light teal) | `4ECDC4` |
| Scripts | `6B5B95` (purple) | `F5F3FA` (light purple) | `6B5B95` |
| Wishing | `F18F01` (amber) | `FFF8EE` (light amber) | `F18F01` |
| Summary | `1B2A4A` (navy) | — | mixed accents |

### Decorative Shape Recipe (per content slide)

```json
{
  "layout": "title_content",
  "background": "F0FAF9",
  "shapes": [
    {"type": "rectangle", "left": 0, "top": 0, "width": 13.333, "height": 0.083, "fill": "4ECDC4"},
    {"type": "rectangle", "left": 0.833, "top": 1.25, "width": 0.694, "height": 0.069, "fill": "4ECDC4"}
  ]
}
```

- Top bar: `left=0, top=0, width=13.333, height=0.083` — full-width thin stripe
- Accent line: `left=0.833, top=1.25, width=0.694, height=0.069` — short bar near title

### Section Divider Recipe

```json
{
  "layout": "blank",
  "background": "FF6B6B",
  "shapes": [
    {"type": "rectangle", "left": 0, "top": 0, "width": 13.333, "height": 0.111, "fill": "FFFFFF"},
    {"type": "rectangle", "left": 0, "top": 7.389, "width": 13.333, "height": 0.111, "fill": "FFFFFF"}
  ],
  "title": "Section Name",
  "subtitle": "Tagline"
}
```

White bars at top and bottom create a "framed" effect on bold backgrounds.

### Semantic Color Mapping

Assign colors by *meaning*, not randomly:

| Color | Use for |
|---|---|
| Blue (`2E86AB`) | Information, expository, facts |
| Orange (`F18F01`) | Narrative, storytelling, warmth |
| Red (`C73E1D`) | Warnings, persuasive, emphasis |
| Coral (`FF6B6B`) | Evaluation, reviews, verdicts |
| Teal (`4ECDC4`) | Growth, processes, positive |
| Purple (`6B5B95`) | Creative, scripts, performance |
| Navy (`1B2A4A`) | Authority, title, summary |
| Dark text on light bg | Default body text |
| White on bold bg | Section divider text |

### Bookend Slides (Title & Summary)

Use the darkest color (`1B2A4A` navy) with mixed accent bars from all
sections. This frames the deck visually — the audience returns to the
same "home base" color at the end.

## Workflow: Plain → Colorful

1. **Build the plain deck first** — get content, structure, and one-concept-per-slide right.
2. **Identify sections** — group slides by topic, assign each a color.
3. **Add backgrounds** — section dividers get bold BG, content slides get tinted BG.
4. **Add accent shapes** — top bars and title underlines on every content slide.
5. **Color the text** — headings and key terms get semantic colors, body stays dark.
6. **Verify with python-pptx** — `pptx_read.py` won't show decorations; read directly.
7. **Regenerate** — overwrite the .pptx with `pptx_create.py`.

## Quick Reference: Shape Dimensions (16:9)

| Element | Left | Top | Width | Height |
|---|---|---|---|---|
| Full-width top bar | 0 | 0 | 13.333 | 0.083 |
| Full-width thick bar | 0 | 0 | 13.333 | 0.111 |
| Bottom bar | 0 | 7.389 | 13.333 | 0.111 |
| Title accent line | 0.833 | 1.25 | 0.694 | 0.069 |
| Left sidebar | 0 | 0 | 0.15 | 7.5 |

All values in inches. For 4:3 slides, use 10.0 × 7.5 instead of 13.333 × 7.5.
