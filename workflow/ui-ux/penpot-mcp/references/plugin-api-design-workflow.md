# Building Designs in Penpot via the Plugin API (MCP)

> Verified workflow from building the Deerngo Bot scoreboard (5 boards, desktop + mobile + 3 states) live in Penpot 2.16 via `mcp__penpot__execute_code`.

## Prerequisites

- Penpot tab open with the target file, MCP button → "Connect here" (bridge active)
- Read the high-level overview once; query exact API shapes with `mcp__penpot__penpot_api_info` BEFORE writing code — especially `Penpot`, `Text`, `Color`, `Shadow`, `FontsContext`. The types have surprising members (e.g. `resize()` semantics, `growType`).

## Step 1 — fonts

`penpot.fonts.all` lists ~1900 Google fonts. `findByName('Inter')` returns the full family; variants carry `fontWeight` as strings ("400", "700", ...). Apply:

```js
const { font, variant } = { font: penpot.fonts.findByName('Inter'),
  variant: penpot.fonts.findByName('Inter').variants.find(v => v.fontWeight === '700') };
font.applyToText(textShape, variant);
```

## Step 2 — library colors (design tokens)

```js
const c = penpot.library.local.createColor();
c.name = 'Primary / Forest Green';
c.color = '#2D6A4F';
```

These appear in the file's ASSETS panel — useful for a design-system feel.

## Step 3 — board + shapes

- `penpot.createBoard()` / `createRectangle()` / `createText(chars)` — all created shapes are NOT attached until you `parent.appendChild(shape)`.
- `width`/`height` are READ-ONLY; set size with `shape.resize(w, h)`. `x`/`y` are absolute page coords and writable directly.
- Board background: `board.fills = [{ fillColor: '#FAFBF5', fillOpacity: 1 }]`.
- Strokes: `shape.strokes = [{ strokeColor: '#E5E7E0', strokeOpacity: 1, strokeWidth: 1 }]`.
- Shadows: `shape.shadows = [{ style: 'drop-shadow', offsetX: 0, offsetY: 10, blur: 25, spread: 0, color: { color: '#000000', opacity: 0.12 } }]`.
- Border radius: `shape.borderRadius = 12` (number).

## Text pitfalls (the ones that bite)

1. **`resize()` forces `growType = 'fixed'`** — text then overflows silently instead of auto-sizing. After resize, set `t.growType = 'auto-width'` or `'auto-height'` to restore natural sizing.
2. **Centered text**: `resize(w, fontSize*1.5)` → `growType='auto-height'` → `align='center'` → position by center-x minus half width.
3. **Right-aligned text** (e.g. table points columns): `growType='fixed'` + `resize(colW, 20)` + `align='right'` + set `x` to the column start.
4. Text color is a FILL: `t.fills = [{ fillColor: '#1F2937', fillOpacity: 1 }]`.
5. `textDecoration = 'underline'` works for link-styled text.

## Helper pattern — store reusable builders in `storage`

The interpreter is fresh per call but `storage` persists. Define once, reuse across calls:

```js
storage.f = (w) => { const font = penpot.fonts.findByName('Inter');
  return { font, variant: font.variants.find(v => v.fontWeight === w) || font.variants[0] }; };
storage.rect = (parent, x, y, w, h, fill, radius) => { /* createRectangle + resize + fills + appendChild */ };
storage.ctxt = (parent, chars, cx, y, w, fontSize, weight, color) => { /* centered text */ };
storage.ltxt = (parent, chars, x, y, fontSize, weight, color) => { /* left text */ };
```

Keep a palette object in storage (`storage.C = { primary, accent, surface, border, ... }`) so later calls reference the same hexes.

## Page management pitfall

`penpot.createPage()` does NOT become the active page — subsequently created shapes land on the ACTIVE page's root regardless of which page root you `appendChild` to (cross-page reparenting via appendChild silently no-ops). Result: everything piles onto the currently open page.

**Fix that worked**: build on the active page, then rename it (`page.name = 'Scoreboard'`). Delete/rename leftovers after. Don't fight cross-page moves.

**Later refinement (multi-page workflow)**: `penpot.openPage(page)` DOES switch pages, but the first call may silently not take effect — call it, then VERIFY `penpot.currentPage.name` matches before building; repeat the call once if not. Once switched, `createBoard()` correctly lands on the new page.

**`storage` is CLEARED on page switch.** The first `execute_code` call after switching pages will fail with `Cannot read properties of undefined (reading '<key>')` if it references helpers/palette stored in `storage`. Re-initialize ALL `storage` helpers and the palette object in the first call after any page switch (the reference says storage persists across calls — true within a page context, NOT across page switches).

**Failed calls leave orphan shapes.** If a call throws mid-way, any board created before the throw exists but is empty. After an error, sweep the page for zero-child boards (`page.root.children.filter(c => c.children.length === 0)`) and `.remove()` them before continuing.

## Reusable components with variants (library components)

> Verified from converting the Deerngo design-system boards into drag-and-drop assets.

**Single component** — build a Board containing the shapes, then wrap it:

```js
const board = penpot.createBoard();
board.name = 'Skeleton Loader'; board.resize(720, 32);
/* ... build children via storage.rect/storage.ltxt ... */
const comp = penpot.library.local.createComponent([board]);
comp.name = 'Skeleton Loader';
```

**Variant group** — create one component per variant, then merge via `createVariantFromComponents`, passing each component's `mainInstance()`:

```js
const c1 = penpot.library.local.createComponent([boardPrimary]); c1.name = 'Button / Primary';
const c2 = penpot.library.local.createComponent([boardOutline]); c2.name = 'Button / Outline';
const c3 = penpot.library.local.createComponent([boardGhost]);   c3.name = 'Button / Ghost';

const vc = penpot.createVariantFromComponents([c1.mainInstance(), c2.mainInstance(), c3.mainInstance()]);
vc.name = 'Button';
vc.variants.renameProperty(0, 'Type');   // property 0 starts as 'Property 1'
```

Result: library shows ONE component "Button" with a "Type" property whose values are Primary/Outline/Ghost (derived from the component names after the ' / '). Verify with `vc.variants.properties` and `vc.variants.currentValues('Type')` — order may be scrambled from creation order; values are what matter.

Component boards must contain their children BEFORE `createComponent`. Keep each variant's board sized to its own content (e.g. Button 180x60, Rank Badge 80x80).

## Library typographies (type-scale tokens)

The `createTypography()` path has runtime quirks that differ from the docs:

```js
const t = penpot.library.local.createTypography();
t.name = 'Page Title';
// Docs claim t.setFont(font, variant) — it is NOT callable at runtime ("t.setFont is not a function").
// Set properties directly instead:
t.fontId = 'gfont-inter';          // font.fontId — NOT font.id (Font objects expose fontId, not id)
t.fontFamily = 'Inter';
t.fontVariantId = '700';           // variant.fontVariantId — NOT variant.id
t.fontSize = '36';                 // string
t.fontWeight = '700';
t.lineHeight = '44';               // string
t.letterSpacing = '0';
```

- `penpot.fonts.findByName('Inter')` may return 'Inter Tight' instead — filter `penpot.fonts.all` for an exact `name ===` match when the exact family matters.
- **There is NO delete API for library typographies** (`Library` exposes only create* methods). A failed create leaves junk entries with defaults (name + sourcesanspro/14/480). Sweep by renaming junk to `(unused) ...` so the user can delete them from the Assets panel; do not fight the API.
- **Name renames are unreliable in a single call** — some assignments silently don't stick (stale array snapshots). Re-read the list in a FOLLOW-UP execute_code call and retry misses individually, addressing objects by `id`.
- **`/` in a library name creates a FOLDER PATH, and re-renaming stacks it.** Setting `t.name = 'Section / Podium Name'` stores leaf `name = 'Podium Name'` and `path = 'Section'`. Renaming AGAIN with the same full string does NOT dedupe — it APPENDS another path segment (`path = 'Section / Section / Section'`). Fix: set `t.name` (leaf only) and `t.path` (folder) as two separate assignments. Read back `.name` + `.path` together to see the real structure. Same applies to colors (`c.name = 'Zebra'`, `c.path = 'Base'`) and components.

## Design System page pattern

When asked for a "design system" page, build it as one page holding several reference boards, one per concern — this mirrors how design tools organize style guides:

- **Colors board**: swatch grid — each swatch is a rectangle filled with the hex, bordered, with the color name + hex value as text ON the swatch (pick text color by contrast: white on dark fills, dark on light). Group by category (Primary / Accent / Neutrals / Text / Semantic / Podium) with a small group label.
- **Typography board**: for each level of the type scale, a left column with label + `size/weight` caption, and a live sample string at the right rendered at that exact size/weight. Use real UI strings ("DEERNGO BOT", "@forestfriend") as samples.
- **Spacing board**: horizontal bars of each spacing value (4/8/16/24/32/48) with px labels; radius section showing 8/12px pill/card shapes.
- **Components board**: live mini-replicas of the actual components — buttons (primary/outline/ghost), rank badges, one podium card, one table row, pagination, skeleton rows, and state summary cards.

The boards double as documentation for devs AND as reusable reference for future designs. Export each board to PNG for the user to review inline.

## Verification — export previews

`mcp__penpot__export_shape` with `shapeId` + `format:'png'` returns `MEDIA:<path>` — include these paths in the chat reply and they render INLINE for the user. Always export each finished board and paste the paths so the user can review without opening Penpot. This is the QA gate: build → export → show → iterate.

Also export with `shapeId:'page'` to preview a whole page.

## "Canvas looks empty" symptom

User opens the file and reports seeing nothing — but `penpotUtils.getPages()` shows all boards intact. This is a VIEWPORT problem, not a data problem: the canvas is panned/zoomed onto a sparse area (boards scattered on a large grid). Fix without user fiddling:

```js
penpot.viewport.zoomToFitAll();   // fits ALL shapes on the current page
// or target specific boards:
penpot.viewport.zoomIntoView(boards);
```

`penpot.viewport` also exposes `center` (writable), `zoom`, and `zoomReset()`. User-side shortcut is Shift+1. After zoomToFitAll, verify by reading back `viewport.bounds` — it should now span all board coordinates.

## Delivery rhythm that worked

1. Inspect file (pages, existing boards) → 2. query API types as needed → 3. setup call (palette + page + helpers in storage) → 4. one board per call (desktop, mobile, each state) → 5. export all as PNG → 6. present inline previews + offer refinement.
