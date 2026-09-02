# Visual Component Library

Rich visual components for python-pptx presentations. Use these instead of plain text and bullets — the user prefers decorated, component-based layouts.

## Component Philosophy

**Never use plain bullets.** Every slide should have at least one visual component: card, table, flow, badge, panel, or chip row. Plain text walls are "dull" — the user explicitly called this out.

**One concept per slide, but visually rich.** The content should be focused, but the presentation should use components to structure and emphasize that content.

---

## Core Components

### Cards (2-col, 3-col, 4-col)

Multi-column card layouts for comparing concepts, showing options, or organizing related information.

**When to use:**
- Comparing 2-4 related concepts side-by-side
- Showing different approaches or methods
- Organizing related information into digestible chunks

**Structure:**
```python
cards_data = [
    ("TITLE", "Subtitle", "Detail text", ACCENT),
    ("TITLE", "Subtitle", "Detail text", PRIMARY),
    # ... 2, 3, or 4 items
]
two_col_cards(s, cards_data)  # or three_cards, four_cards
```

**Visual elements:**
- Panel background (usually tinted base-90)
- Left accent strip in the card's color
- Title in accent color, monospace font
- Subtitle in near-content color (slightly bolder)
- Detail in content color

**Example from SWEBOK:**
```python
# Comparing QA vs QC
two_col_cards(s,
    "QUALITY ASSURANCE (QA)", [
        ("Process-focused", "Prevent defects"),
        ("Proactive", "Standards, reviews, audits"),
    ], PRIMARY, "✓",
    "QUALITY CONTROL (QC)", [
        ("Product-focused", "Detect defects"),
        ("Reactive", "Testing, inspection"),
    ], SECONDARY, "⚙",
    card_h=4.0)
```

### Styled Tables

Tables with colored headers, alternating row styling, and semantic coloring.

**When to use:**
- Exact values need to be compared
- Structured data (categories, metrics, tools)
- When the data has clear column semantics

**Structure:**
```python
data = [
    ["Header 1", "Header 2", "Header 3"],  # header row
    ["Row 1", "Detail", "More"],
    ["Row 2", "Detail", "More"],
]
col_widths = [3.0, 5.0, 4.5]  # in inches
styled_table(s, ML, 1.82, CW, data, col_widths, ACCENT, row_h=0.55)
```

**Visual elements:**
- Header row: accent color background, black text
- Data rows: base-90 or white background
- Alternating row colors for readability
- Font size can be adjusted for dense tables

### Flow Diagrams

Horizontal or vertical step-by-step flows with numbered badges.

**When to use:**
- Process workflows (3-6 steps)
- Lifecycle stages
- Sequential procedures

**Structure:**
```python
flow_steps(s, "section-tag", "Process Name", ACCENT, [
    ("STEP 1", "Description"),
    ("STEP 2", "Description"),
    ("STEP 3", "Description"),
], [
    R("Note: ", 12.5, NCONTENT, bold=True),
    R("additional context here", 12.5, CONTENT),
])
```

**Visual elements:**
- Numbered circles (badges) for each step
- Connecting lines or arrows
- Step title in accent color
- Description in content color
- Optional footer note

### Badges and Chips

Small labeled elements for categorization, numbering, or highlighting.

**When to use:**
- Numbering items (1, 2, 3...)
- Category labels
- Status indicators
- Tagging concepts

**Structure:**
```python
# Numbered badge
badge(s, x, y, 0.5, "01", PRIMARY)

# Chip row
chips = [("Requirements", ACCENT), ("Architecture", PRIMARY)]
chip_row(s, chips, y=5.5, x_end=12.5)
```

**Visual elements:**
- Badge: circle with number/label, accent color background
- Chip: rounded rectangle, light tinted background, accent border

### Code Blocks

Monospace code display with syntax highlighting and background.

**When to use:**
- Code examples
- Formulas or equations
- Technical specifications
- Command examples

**Structure:**
```python
code_block(s, ML, 1.92, CW, 1.8,
    "def example():\n    return 'code here'",
    size=12)
```

**Visual elements:**
- Base-95 background (dark)
- JetBrains Mono font
- Optional syntax highlighting (manual via color runs)

### Concept Panels

Rounded panels with title and bullet points, used for explaining a single concept.

**When to use:**
- Explaining a core idea
- Listing key points about one topic
- When you need more space than a card but less than a full slide

**Structure:**
```python
panel(s, ML, 1.82, CW, 2.5, radius=0.08)
tb(s, ML + 0.4, 2.0, CW - 0.8, 0.5,
   [P(R("Main concept title", 16, NCONTENT, bold=True))])
tb(s, ML + 0.4, 2.6, CW - 0.8, 1.5, [
    P(R("•  ", 13, ACCENT, bold=True),
      R("Key point", 13, NCONTENT, bold=True),
      R(" — supporting detail", 13, CONTENT), sa=6),
])
```

### Banners

Full-width colored bars at the bottom of slides for emphasis or summary statements.

**When to use:**
- Key takeaway or summary
- Important note or warning
- Call to action

**Structure:**
```python
banner(s, 4.6, [
    R("Important: ", 13, WARNING, bold=True),
    R("this is the key insight", 13, NCONTENT, bold=True),
], h=0.65)
```

### Section Dividers with Ghost Numbers

Bold section transitions with large ghost numbers in the background.

**When to use:**
- Transitioning between major sections
- Marking the start of a new topic area

**Structure:**
```python
section_slide("08", "Section Title", "Tagline or description", SECONDARY)
```

**Visual elements:**
- Solid background in section accent color
- Large ghost number (200pt, 10% opacity) in top-right
- Title in black, large font
- Subtitle in near-black

---

## Layout Patterns

### Two-Column Comparison

Use `two_col_cards` for side-by-side comparisons. Include emoji icons for visual distinction.

```python
two_col_cards(s,
    "LEFT TITLE", [
        ("Point 1", "Detail"),
        ("Point 2", "Detail"),
    ], PRIMARY, "✓",
    "RIGHT TITLE", [
        ("Point 1", "Detail"),
        ("Point 2", "Detail"),
    ], SECONDARY, "⚙",
    card_h=4.0)
banner(s, 6.35, [
    R("Left ", 12.5, NCONTENT, bold=True),
    R("prevents", 12.5, PRIMARY, bold=True),
    R(". Right ", 12.5, NCONTENT, bold=True),
    R("detects", 12.5, SECONDARY, bold=True),
], h=0.55)
```

### Grid of Ovals

For showing 5-10 related concepts, use ovals arranged in rows.

```python
items = [
    ("INTEGRATION", "Coordinate all", ACCENT),
    ("SCOPE", "Define boundaries", PRIMARY),
    # ... up to 10 items
]
n = len(items)
ow, gap = 2.0, 0.42
total_w = n * ow + (n - 1) * gap
x0 = (SW - total_w) / 2
for i, (name, desc, c) in enumerate(items):
    x = x0 + i * (ow + gap)
    o = oval(s, x, 2.0, ow, 1.4, c)
    shape_text(o, [P(R(name, 12, BLACK, bold=True), align=PP_ALIGN.CENTER)])
    tb(s, x, 3.5, ow, 0.5,
       [P(R(desc, 10.5, CONTENT, italic=True), align=PP_ALIGN.CENTER)])
```

### CMMI-Style Maturity Levels

Numbered badges stacked horizontally for progression or levels.

```python
levels = [
    ("1", "Initial", "Ad hoc"),
    ("2", "Managed", "Planned"),
    # ... up to 5 levels
]
for i, (num, name, desc) in enumerate(levels):
    x = ML + i * (ow + gap)
    badge(s, x + 0.7, 2.0, 0.6, num, SECONDARY)
    tb(s, x, 2.8, ow, 0.7,
       [P(R(name, 12, NCONTENT, bold=True), align=PP_ALIGN.CENTER)])
    tb(s, x, 3.6, ow, 0.7,
       [P(R(desc, 10.5, CONTENT, italic=True), align=PP_ALIGN.CENTER)])
```

---

## Typography and Color

### Font Usage

- **Sarabun** (body text): All prose, headings, bullet points
- **JetBrains Mono** (technical): Code, formulas, commands, technical labels
- **Bold** for emphasis, titles, key terms
- **Italic** for descriptions, notes, secondary text

### Color Semantics

Use brand CI colors by semantic role:

| Color | Use for |
|-------|---------|
| PRIMARY | Core work, main concepts, first option |
| SECONDARY | Supporting work, related concepts, second option |
| ACCENT | Highlights, emphasis, third option |
| INFO | Information, neutral facts, fourth option |
| WARNING | Cautions, important notes, fifth option |
| ERROR | Failures, problems, sixth option |
| CONTENT | Body text |
| NCONTENT | Near-content (slightly bolder for titles) |
| MUTED | Secondary text, footnotes |

### Text Box Helper

Use `tb()` for text boxes with proper margin handling:

```python
tb(s, x, y, width, height, [
    P(R("Title", 16, PRIMARY, bold=True), sa=6),
    P(R("Body text", 14, CONTENT)),
], ml=0.3)  # margin-left in inches
```

---

## Pitfalls

### ⚠️ Don't Use Plain Bullets

The user explicitly finds plain text and bullets "dull." Always use a visual component:
- ❌ Plain bullet list
- ✅ Cards with accent strips
- ✅ Styled table
- ✅ Flow diagram
- ✅ Concept panel

### ⚠️ Card Tuple Length

`two_col_cards`, `three_cards`, and `four_cards` expect 4-element tuples: `(title, subtitle, detail, color)`.

If you only have 3 elements (title, detail, color), add an empty subtitle:
```python
("TITLE", "", "Detail text", ACCENT)  # correct
("TITLE", "Detail text", ACCENT)      # WRONG — will fail
```

Or use manual panel construction instead of the helper functions.

### ⚠️ Component Density

Don't overload a slide. If you have:
- 2 concepts → use `two_col_cards`
- 3 concepts → use `three_cards`
- 4 concepts → use `four_cards`
- 5+ concepts → split across multiple slides or use a grid of ovals

One component per slide is usually enough. Two at most.

### ⚠️ Section Divider Consistency

Every major section should have a divider slide. Use the same color throughout the section:
- Section divider: bold background in section color
- Content slides: accent shapes in section color
- Footer tag: section identifier in footer

This creates visual wayfinding — the audience knows where they are.

---

## Example: Full Slide with Components

```python
# Slide: Comparing two approaches
s = new_slide()
header(s, "design", "Two Design Approaches", SECONDARY)

two_col_cards(s,
    "APPROACH A", [
        ("Fast", "Quick to implement"),
        ("Simple", "Easy to understand"),
        ("Limited", "Hard to extend"),
    ], PRIMARY, "⚡",
    "APPROACH B", [
        ("Slower", "Takes more time"),
        ("Complex", "Requires expertise"),
        ("Flexible", "Easy to extend"),
    ], SECONDARY, "🔧",
    card_h=4.0)

banner(s, 6.35, [
    R("Choose ", 12.5, NCONTENT, bold=True),
    R("A for prototypes", 12.5, PRIMARY, bold=True),
    R(", ", 12.5, CONTENT),
    R("B for production", 12.5, SECONDARY, bold=True),
    R(".", 12.5, CONTENT),
], h=0.55)

footer(s, 42, "design")
```

This slide has:
- Header with section tag
- Two-column card comparison
- Banner with summary
- Footer with slide number and section tag

No plain bullets. Visually rich. Focused on one concept (the comparison).
