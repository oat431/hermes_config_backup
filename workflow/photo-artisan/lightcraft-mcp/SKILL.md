---
name: lightcraft-mcp
description: Use when driving LightCraft MCP for photo edits and exports.
---
# LightCraft MCP — operating procedure

## Workflow (order matters)
1. `mcp__lightcraft__import` {paths, mode: "add"} — reference files in place; first photo becomes active; returns ids.
2. `mcp__lightcraft__read_resource` uri `lightcraft://photo/active` — check metadata, format, and develop state before editing.
3. `mcp__lightcraft__set_develop` {id, values: {controlId: n}, settings: {…}, label} — one undo step for all `values` + one for `settings`.
4. Orientation/flip via `mcp__lightcraft__command_run` {id: "photo.flipHorizontal"} — sets crop flip_h, non-destructive.
5. `mcp__lightcraft__select_photos` {ids, active} then `app.export` via `command_run` — export needs a non-empty selection or it's disabled.
6. QC the exported render with `vision_analyze` before delivering.

## Key facts
- Slider ids are flat dotted: `light.exposure`, `light.highlights`, `wb.temp`, `wb.tint`, `color.vibrance`, `effects.texture|clarity|dehaze`, `vignette.amount|midpoint|feather|highlights`, `detail.sharpenAmount|sharpenRadius|sharpenDetail|sharpenMasking|nrLuminance|nrColor`. Full list: `lightcraft://controls`.
- Setting `wb.temp`/`wb.tint` needs `settings: {wb: {mode: "custom"}}` or the mode stays asShot.
- `app.export` params: path, format, longEdge 0 = full size, quality, colorSpace, conflict: "overwrite", sharpen: "none" (develop sharpening already baked in — don't double-sharpen).
- All commands: `lightcraft://commands` (309 commands; use `command_run` {id, params} for anything not exposed as a tool). `command_batch` runs steps in order.

## Pitfalls
- The deferred tool catalog FLAPS: `tool_search` for lightcraft terms can return empty and `tool_describe` can 404 names that exist minutes later. Retry `tool_search` with a concrete action word ("lightcraft library.import", "command_run") before concluding a tool is missing.
- Phone JPEGs (no RAW): keep highlight recovery ≤ -80, no heavy dehaze; banding appears fast in dark backgrounds.
- `app.export` writes wherever path points — proofs go to the profile scratch dir, deliver via MEDIA:, never overwrite the original (export.checkTarget also guards this).

## Edit recipes
- "Professional natural portrait": highlights -80, shadows +35, whites -10, blacks +15, contrast +8; wb.temp ~5850 + tint 6 for indoor yellow cast; vibrance +15 (never saturation around skin); texture +6, clarity +5; vignette -18 / midpoint 45 / feather 65 / highlights 25 (highlight priority); sharpen 45 r1.2 detail 30 masking 35; NR lum 15 / color 25. Light → color → effects → detail.