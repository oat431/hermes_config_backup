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

## Stale shape references across execute_code calls (CRITICAL)

`penpotUtils.findShape()`, `findShapeById()`, and `findShapes()` return **snapshot objects**, not live DOM references. If you obtain a board reference in call #1 and try `board.appendChild(child)` in call #2, the call **silently no-ops** — the child is created but lands on `penpot.root` (the page root), not inside the board. No error is thrown; `board.children.length` doesn't increase. `findShapes(s => true, board)` in a later call WILL find them at root level, with `parent.name === 'Root Frame'`.

**Root cause:** the Penpot plugin API returns serializable snapshots across the MCP boundary. Mutations on snapshots don't propagate back. Only the original variable from `createBoard()` / `createRectangle()` / `createText()` in the SAME call is a live reference that accepts `appendChild`.

**Fix — build board + ALL children in one call:**
```js
// ALL in one execute_code call:
const board = penpot.createBoard();
board.resize(480, 340); board.x = 100; board.y = 100;
board.fills = [{ fillColor: '#1B1717', fillOpacity: 1 }];
penpot.root.appendChild(board);

const t = penpot.createText('Flowero Discover');
t.resize(400, 32); t.x = 24; t.y = 24; t.growType = 'auto-height';
t.fontSize = '21'; t.fills = [{ fillColor: '#CAC9C9', fillOpacity: 1 }];
board.appendChild(t);  // ← works: same call, live reference
```

**Fix — reparent orphans from root to board (when board already exists):**
```js
const root = penpot.root;
const board = root.children.find(c => c.name === 'Service Status Card' && c.type === 'board');
const orphans = root.children.filter(c => c !== board);
for (const child of orphans) {
  const absX = child.x, absY = child.y;
  board.appendChild(child);              // preserves absolute position
  penpotUtils.setParentXY(child, absX - board.x, absY - board.y);  // fix relative
}
```

## `storage` helper functions silently fail (stale closure)

Helper functions stored in `storage` (e.g. `storage.txt = (parent, chars, x, y, ...) => { ... }`) may fail when called in a LATER `execute_code` call — not because `storage` is cleared (it persists within a page), but because the helper captures `storage.sarabun` / `storage.jbm` by closure reference, and these may be stale or undefined after a page-switch re-init that didn't re-run. The call throws `[PENPOT PLUGIN] Value not valid: <number>. Code: :createText` — the `<number>` is the ASCII code of the first character of the font variant ID being passed (e.g. `38` = `'n'` from `'normal-600'`).

**Fix:** don't use `storage`-stored helper functions for text creation across calls. Build text inline in each call, or re-define the helper at the top of every call that uses it.

## `addTheme()` signature — object, not positional args

The high-level overview documents `addTheme(group: { group: string; name: string })`. At runtime, calling `tok.addTheme('Color theme', 'Forest')` (two positional strings) fails with `Value not valid: <first-char-of-second-arg>`. The correct call is:

```js
const theme = tok.addTheme({group: 'Color theme', name: 'Forest'});
// NOT: tok.addTheme('Color theme', 'Forest')  ← fails
```

## Verifying color changes without PNG export

When `export_shape` times out (heavy files with 700+ components), verify that library color changes cascaded to components by reading a component's fill directly:

```js
const lib = penpot.library.local;
const btn = lib.components.find(c => c.path === 'Dark / Button / Primary / Text' && c.name === 'Default');
const main = btn.mainInstance();
const shapes = penpotUtils.findShapes(s => true, main);
return shapes.filter(s => s.fills?.length > 0).map(s => ({
  name: s.name, fill: s.fills[0]?.fillColor
}));
// Confirm: fill === '#1FB854' (your forest primary)
```

This is the programmatic QA gate when visual export isn't available.
