# Merge-and-Style Technique for Large Presentations

When generating large presentations (100+ slides), use a split-merge-style workflow to avoid JSON size limits and ensure consistent styling.

## When to Use

- Decks with 100+ slides
- Multi-chapter or multi-section presentations
- When you need to apply consistent styling across all slides after generation

## Workflow

### 1. Split Content into Parts

Break the presentation into logical chunks (e.g., by chapter or section group):

```
Part 1: Opening + Chapters 01-07 (57 slides)
Part 2: Chapters 08-18 + Closing (65 slides)
```

Generate separate JSON specs for each part.

### 2. Generate Parts Separately

```bash
python pptx_create.py Part1.json Part1.pptx
python pptx_create.py Part2.json Part2.pptx
```

### 3. Merge and Apply Styling

Write a Python script that:
- Loads all parts using python-pptx
- Creates a new merged presentation
- Copies all slides (shapes + notes)
- Applies brand CI styling programmatically to each slide
- Saves the final merged deck

```python
from pptx import Presentation
from pptx.dml.color import RGBColor
import copy

# Load parts
prs1 = Presentation("Part1.pptx")
prs2 = Presentation("Part2.pptx")

# Create merged presentation
merged = Presentation()
merged.slide_width = prs1.slide_width
merged.slide_height = prs1.slide_height

# Copy slides from Part 1
for slide in prs1.slides:
    layout = slide.slide_layout
    new_slide = merged.slides.add_slide(layout)
    for shape in slide.shapes:
        new_slide.shapes._spTree.append(copy.deepcopy(shape._element))
    if slide.has_notes_slide:
        new_slide.notes_slide.notes_text_frame.text = slide.notes_slide.notes_text_frame.text

# Copy slides from Part 2
for slide in prs2.slides:
    layout = slide.slide_layout
    new_slide = merged.slides.add_slide(layout)
    for shape in slide.shapes:
        new_slide.shapes._spTree.append(copy.deepcopy(shape._element))
    if slide.has_notes_slide:
        new_slide.notes_slide.notes_text_frame.text = slide.notes_slide.notes_text_frame.text

# Apply styling
def apply_styling(slide, accent_color):
    # Background
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = RGBColor.from_string(BASE_100)
    
    # Accent bar
    accent_bar = slide.shapes.add_shape(
        1,  # Rectangle
        Inches(0), Inches(0),
        Inches(13.333), Inches(0.15)
    )
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = RGBColor.from_string(accent_color)
    accent_bar.line.fill.background()

# Apply to all slides
for i, slide in enumerate(merged.slides):
    accent = determine_accent_color(i)  # Your logic here
    apply_styling(slide, accent)

merged.save("Final.pptx")
```

## Benefits

- Avoids JSON spec size limits
- Easier to debug individual parts
- Styling logic is centralized and consistent
- Can handle 100+ slide decks reliably

## Example Use Case

SWEBOK v4 presentation: 122 slides covering 18 chapters
- Split into 2 parts (57 + 65 slides)
- Generated separately
- Merged and styled with Panomete CI colors
- Result: Single branded deck with section-coded accent colors
