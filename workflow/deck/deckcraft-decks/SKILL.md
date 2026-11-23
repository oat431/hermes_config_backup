---
name: deckcraft-decks
description: "Build branded PPTX decks with DeckCraft CLI/MCP."
version: 1.0.0
author: deck
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [deckcraft, pptx, presentation, mcp, brand-ci]
    category: creative
    related_skills: [presentation-design, powerpoint]
---

# DeckCraft Decks

## When to Use

- Building a PPTX/PDF deck with DeckCraft (CLI `deckcraft-cli` or the
  `mcp__deckcraft__*` tools) — especially branded, multi-slide decks.
- Automating slide production from notes, a brand CI, or a JSON outline.
- Debugging a DeckCraft build where shapes land on the wrong slide, ids do not
  resolve, or a long command run aborts mid-way.

DeckCraft is a Rust PowerPoint reimplementation (`deckcraft-cli`) whose every UI
action is a command. Drive it headless through the CLI or the MCP server
(`mcp__deckcraft__*`) to build branded decks. Use this skill for anything built
with DeckCraft; use `presentation-design` for the design layer and `powerpoint`
for python-pptx work.

## Discover the command surface first (never guess)

```bash
deckcraft-cli commands            # 226 commands as JSON (id, params, menu)
deckcraft-cli describe design.colors
```

Only a subset of commands have MCP wrappers. `run_command` / `batch` cover the rest,
and anything the CLI can do is a command id + JSON params.

Commands that matter when building a slide deck:

| Need | Command |
|---|---|
| New file / theme | `file.new {blank?: true, theme?}`, `design.theme {name}`, `design.themes` |
| Brand palette | `design.colors {colors: {accent1..6, dk1, lt1, dk2, lt2}}`, `design.fonts {major, minor}` |
| Slides | `slide.new {layout, at}`, `slide.notes {index, text}`, `slide.inspect {index}`, `section.add {name, at}` |
| Background | `design.background {color, index?, all?}` |
| Shapes | `shape.insert {preset, rect:[x,y,w,h] pt, text}`, `shape.fill {color, transparency}`, `shape.line` |
| Text | `insert.textBox {rect, text}` (`\n` = new paragraph), `text.set {id, text}` |
| Formatting | `edit.select {ids:[...]}` then `format.font/size/color/bold/align/anchor/margins/lineSpacing` |
| Tables | `insert.table {rows, cols, rect}` + `table.style{none}`, `table.cellFill {id, cells}`, `table.columnWidth`, `table.rowHeight`, `text.edit {id, cell:[r,c]}` + `insert/selectAll/format` + `text.exit` |
| Export | `file.export {path, format: pptx\|pdf\|png\|outline, slide?, all?, scale?, layout?}` |
| Verify visually | `file.export {format:"png", all:true, scale:1}` then read the PNGs |

Slide size is in **points**: 16:9 is `960 x 540`. Note `file.new {blank:true}` creates
**zero** slides — any insert before the first `slide.new` fails with "no slides".

## The eight pitfalls that break long builds

1. **`slide.new` inserts after the current slide, and a fresh CLI session sits on
   slide 0.** Always pass `at`: `slide.new {layout:"blank", at:<index>}`. Without it,
   slides created in later sessions land in the middle of the deck and shapes scatter.
2. **Chunk only at slide boundaries.** A chunk that starts mid-slide inherits the
   session's active slide (0) and parks that slide's remaining shapes there.
   Pack whole slides per invocation, never a fixed command count.
3. **Shape ids are not stable across sessions.** The ids printed by inserts are
   *not* the ids in the saved file (the counter jumps between runs). After the
   creation pass, call `slide.inspect {index}` for every slide and zip the returned
   shape ids to your emitted order — inspect returns shapes in creation order.
4. **Shape-addressed commands act on the active slide only.** Emit `slide.go {index}`
   before styling a slide, and before `chart.options {id}` (a chart cannot be
   `edit.select`-ed — pass `id` explicitly).
5. **`format.*` with no `edit.select` first fails** ("nothing selected"), and a
   failing command aborts the run: the `--save` never happens, so a long run that
   fails at the end loses everything. Chunk moderately and keep groups intact.
6. **Every slide needs an explicit background.** New slides inherit the theme
   default (light), so `design.background {color, index}` right after each
   `slide.new`; dark deck = one background command per slide.
7. **`shape.fill` / `shape.line` `ids` resolve only on the ACTIVE slide.** A batch
   referencing shapes on other slides fails with "no such shape" — emit
   `slide.go {index}` before each `ids`-bearing command. Creation-printed ids are
   valid *within one continuous server session* (inspect confirms), but re-verify
   with `slide.inspect` after any file reload.
8. **`shape.insert` draws a default outline in theme `accent1`.** For flat/borderless
   designs run `shape.line {none:true, ids:[...]}` on every drawn shape (once per
   slide, with `slide.go` first) — otherwise every chip/ellipse carries a thin
   accent-colored hairline, invisible in thumbnails but visible at 2x zoom.
9. **Never emit white text on a saturated brand fill** when the CI says
   primary-content is black; that rule exists for a contrast reason.
8. **Charts keep their own text colours.** Axis/label text stays dark, so a chart
   on a dark slide is unreadable — put it on a light inset panel or draw the data
   with shapes (proportional bars) instead.

## Two-phase build pattern

```
# phase 1: file.new + slide.new{at} + background + all inserts, per-slide groups
# phase 1b: slide.inspect every slide -> idmap (emission order == inspect order)
# phase 2: per slide: slide.go + grouped edit.select + shape.fill + format.*
# phase 3: section.add + file.saveAs
```

Group styling aggressively: select *many* shapes that share a style in one
`edit.select`, then one `format.size` / `format.color` applies to all of them.
This cuts command counts by roughly 5x versus per-shape formatting. Fills still
need one `shape.fill` per colour group.

Express the document with a tiny helper layer rather than raw commands:

```python
def C(cmd, params=None):     # command -> 'cmd=json' string
    return cmd if params is None else cmd + "=" + json.dumps(params, ensure_ascii=False)
# Ref = handle emitted during creation; styling commands carry a sentinel token
# (e.g. '@@REF12@@') substituted with the real id once phase 1b resolved the map.
```

Use `json.dumps` for params — hand-written JSON breaks on a stray brace, and a
naive `"token" in raw_json` guard misses tokens because `json.dumps` escapes
control characters into `\u0001` text.

## Brand CI

Read the brand file at build time (`02_visual-identity.md`, `03_style-guide.md`)
and drive every hex from it — never from memory. Map sections to brand tokens by
semantic role, keep the CI's two-font rule, and respect its content-on-colour
rule (e.g. black on the primary fill, never white). Tint surfaces with
`transparency` and use the brand's neutral/border tokens for hairlines so the
deck reads as one system.

## Windows / environment notes

- CLI path: `C:\Program Files\DeckCraft\deckcraft-cli.exe`; pass **native**
  forward-slash paths (`F:/dir/file.pptx`) — MSYS `/f/...` paths are not translated
  for the native binary.
- Shape geometry is points; python-pptx `Inches` math does not apply.
- Transparency is the tint tool: `shape.fill {color, transparency: 0.88}` renders a
  12% tint of the colour over the slide background (cards on a dark deck).
- Fonts come from the system: check the brand font is installed before assuming a
  mono/display family will render. Verify glyph coverage (✓ ✗ → ✱ ▲, Thai) with a
  throwaway render before relying on symbols in body text.
- Exporting PNG/PDF works headless; `soffice`/`pdftoppm` are not needed.

## Always verify by rendering

```bash
deckcraft-cli run --in deck.deckcraft --cmd 'file.export={"path":"render/slide","format":"png","all":true,"scale":1}' --print
```

Build PIL contact sheets (3x2 per sheet) and inspect them with vision, zooming into
individual slides where geometry is custom. Renders catch what JSON cannot: clipped
text, dark-on-dark, overlaps, text boxes collapsed to a 10pt-wide column (a
proportional bar wider than `width - 250` starves the note text beside it).
Also verify the exported PPTX independently: it is a zip — count
`ppt/slides/slideN.xml` and `ppt/notesSlides/notesSlideN.xml` with `zipfile`
to confirm slide count and that speaker notes survived the export.
