# Custom python-pptx Script Patterns

When the JSON spec path is too limiting for visually rich decks, write a
raw python-pptx script. This reference covers the patterns, helpers, and
slide-builder structure proven across multiple production decks.

## When to Use This Over JSON Spec

- Complex visual components: cards with accent strips, numbered badges in ovals, flow diagrams with arrows
- Decks with 5+ slides that each need custom component layouts
- Need for reusable helper functions (card builders, flow steps, stat cards)
- Section-coded color themes with per-slide accent shapes

## The `I()` Helper

```python
def I(v):
    """Shorthand for Inches()."""
    return Inches(v)
```

All layout math stays as plain floats. Only call `I()` at the final
position/size call site. This avoids the `Inches * Inches = Emu` trap.

## Core Helper Library

```python
# Shapes
def rect(slide, l, t, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, I(l), I(t), I(w), I(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line: s.line.color.rgb = line
    else: s.line.fill.background()
    return s

def rounded(slide, l, t, w, h, fill):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, I(l), I(t), I(w), I(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    s.line.fill.background()
    return s

def oval(slide, l, t, w, h, fill):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, I(l), I(t), I(w), I(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    s.line.fill.background()
    return s

def right_arrow(slide, l, t, w, h, fill):
    s = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, I(l), I(t), I(w), I(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    s.line.fill.background()
    return s

# Text
def tb(slide, l, t, w, h):
    """Add a textbox, return (shape, text_frame)."""
    s = slide.shapes.add_textbox(I(l), I(t), I(w), I(h))
    s.text_frame.word_wrap = True
    s.text_frame.auto_size = None
    return s, s.text_frame

def p_add(tf, align=PP_ALIGN.LEFT, space_after=Pt(4)):
    if len(tf.paragraphs) == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.alignment = align
    p.space_after = space_after
    return p

def run_add(p, text, size=Pt(14), color=BODY, bold=False, italic=False, name='Calibri'):
    r = p.add_run()
    r.text = text
    r.font.size = size
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = name
    return r
```

## Slide Layout Patterns

### Content Slide Header

```python
def content_slide_header(slide, section_color, title, subtitle=None):
    set_bg(slide, WHITE)
    accent_bar(slide, section_color)        # full-width top bar
    accent_underline(slide, section_color)   # short bar under title
    title_text(slide, title)
    if subtitle:
        subtitle_text(slide, subtitle)
```

Standard positions:
- Title: `(ML, 0.35, CW, 0.7)` — ML=0.833", CW=11.667"
- Subtitle: `(ML, 0.95, CW, 0.4)`
- Top accent bar: `(0, 0, SW, 0.069)`
- Accent underline: `(ML, 1.2, 0.694, 0.056)`

### Dark Section Divider

```python
def build_slide3(prs):
    slide = new_slide(prs)
    set_bg(slide, NEUTRAL)
    rect(slide, 0, 0, SW_IN, 0.111, SECONDARY)    # top frame
    rect(slide, 0, 7.389, SW_IN, 0.111, SECONDARY) # bottom frame
    # Large quote text, supporting bullet points...
```

### Dark Bookend Slides (Title + Q&A)

```python
def build_slide1(prs):
    slide = new_slide(prs)
    set_bg(slide, BASE_100)
    rect(slide, 0, 0, SW_IN, 0.111, PRIMARY)       # top accent
    rect(slide, 0, 7.389, SW_IN, 0.111, PRIMARY)    # bottom accent
    rect(slide, 0, 0, 0.083, SH_IN, PRIMARY)        # left strip
    # Title, subtitle, divider line, name, date, tech badges...
```

## Component Builders

### Card Grid (3-col)

```python
def card_3col(slide, y, cards, card_w=3.5, gap=0.45):
    total_w = 3 * card_w + 2 * gap
    x0 = (SW_IN - total_w) / 2
    card_h = 3.2
    for i, (color, title, body_lines) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        rounded(slide, x, y, card_w, card_h, WHITE)
        rect(slide, x, y, card_w, 0.056, color)      # top accent
        rect(slide, x, y, 0.069, card_h, color)       # left accent strip
        # Title, body lines...
```

### Card Grid (2-col)

```python
def card_2col(slide, y, cards, card_w=5.3, gap=0.9):
    total_w = 2 * card_w + gap
    x0 = (SW_IN - total_w) / 2
    # Same structure as card_3col but wider cards
```

### Big Stat Cards

```python
def big_stat_card(slide, x, y, w, h, color, num, label, desc):
    rounded(slide, x, y, w, h, WHITE)
    rect(slide, x, y, 0.069, h, color)
    # Big number (28pt, color), label (12pt, DARK), desc (9.5pt, LIGHT)
```

### Numbered Badge

```python
def badge(slide, x, y, size, text, color, text_color=WHITE):
    s = oval(slide, x, y, size, size, color)
    s_tf = s.text_frame
    s_tf.word_wrap = False
    p = s_tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run_add(p, text, Pt(12), text_color, True)
```

### Full-Width Banner

```python
def banner(slide, y, text, color, text_color=WHITE, h=0.55):
    rect(slide, 0, y, SW_IN, h, color)
    s, tf = tb(slide, ML_IN, y + 0.1, CW_IN, 0.4)
    p = p_add(tf, PP_ALIGN.CENTER)
    run_add(p, text, Pt(13), text_color, True)
```

### Styled Table

```python
def styled_table(slide, l, t, w, rows, col_widths, header_color, row_h=0.42):
    n_rows = len(rows); n_cols = len(rows[0])
    h = row_h * n_rows
    shape = slide.shapes.add_table(n_rows, n_cols, I(l), I(t), I(w), I(h))
    tbl = shape.table
    for ci, cw in enumerate(col_widths):
        tbl.columns[ci].width = I(cw)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.text = ""
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if ri == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_color
                # white bold text
            else:
                # alternating row colors (F5F5F5 / white)
```

## Slide Builder Pattern

Each slide is a `build_slideN(prs)` function. The main function creates
the `Presentation`, sets slide size, calls each builder in order, and
saves. Speaker notes go in `slide.notes_slide.notes_text_frame.text`.

```python
def main():
    prs = Presentation()
    prs.slide_width = I(13.333)
    prs.slide_height = I(7.5)

    build_slide1(prs)   # Title
    build_slide2(prs)   # Content
    # ...
    build_slide10(prs)  # Q&A

    prs.save(output_path)
```

## Verification

1. `pptx_read.py --outline` — confirms all text, tables, notes are present
2. Python snippet to check backgrounds and shape counts:
```python
from pptx import Presentation
prs = Presentation('deck.pptx')
for i, slide in enumerate(prs.slides):
    bg = slide.background.fill
    bg_color = str(bg.fore_color.rgb) if bg.type == 1 else 'none'
    print(f"Slide {i+1}: bg={bg_color}, shapes={len(list(slide.shapes))}")
```
3. Open in PowerPoint for final visual check — the only way to verify
   overlapping shapes, text overflow, and color harmony.
