---
name: figcraft-design-system
description: Use when building or extending FigCraft design-system files.
version: 1.0
author: UX (Hermes ui-ux profile)
license: MIT
metadata:
  hermes:
    tags: [figcraft, design-system, components, automation, headless]
    related_skills: [daisyui, branding-ci]
---

## When to Use

- Creating or extending any `.figcraft` design-system/component-library file via `figcraft-cli run`.
- Anything touching Panomete's `panomete_design_system.figcraft` (variant sets, tokens, publishing, QA renders).
- When FigCraft layout renders empty/collapsed and you need the known failure modes.

# FigCraft headless design-system building

Proven while building `F:\projects\design\panomete_design_system\panomete_design_system.figcraft` (26 sets / 165 variants, published library `83a34195523e9ac5`). Reusable harness: `F:\projects\design\panomete_design_system\tools\build_harness.py` (`H.run`, `build_set`, `preview`). CLI: `"C:\Program Files\FigCraft\figcraft-cli.exe"`.

## Core mechanics

1. **Every `run` is a FRESH session.** Each batch MUST start with `file.open {path}` and end with `file.save`. Chain node ids ACROSS batches; within one batch ids are sequential but unknowable until results return.
2. **Variant names:** `"Size=sm, Style=primary, State=default"` — COMMA+space separates properties. Space-only = one corrupted property.
3. **Build order per set:** batch A `page.select` + heading + variant frames **pre-positioned in a grid** (combine wraps the bbox) → batches of children level-by-level (parent ids from prior batch) → binds → `component.create {ids:[...]}` per frame → `component.combineVariants {ids}` → `node.set {name}`.
4. **Text property:** `component.addProperty {id:set, name:Label, type:text, default}` then per variant text layer `component.bindProperty {layer, property:Label, field:characters}`.
5. **Tokens:** `variable.createCollection {name,modes}` → `variable.create {collection,name,type,value}`; bind via `variable.bind {ids, field:"fills/0/color"|"strokes/0/color"|"cornerRadius", variable}`. Bind preserves paint alpha.
6. **Publish:** `library.publish {description}` (increments version; save first). Export: `variable.export {format:"css", path}`. Zoom QA export: `figcraft-cli export <file> -o x.png --node <ID|name> --scale 6` — prefer IDs, name matching is ambiguous.

## Pitfalls (each cost a rebuild)

- **`hug` parent + `fill` children ⇒ width 0 collapse.** Parent frame needs `sizingH:"fixed"` with explicit width whenever children use `sizingH:"fill"` (hit: table, list, dropdown menu).
- **Component sets never re-hug after you resize variants** — fix with `node.set {ids:[set], width/height}` (bbox = 20px pad + children extents).
- **frame/rect/ellipse children drop x,y unless passed explicitly** — absolute-positioned children (dots, checks, connectors) need `x`/`y` in create params; text/vector pass them natively.
- **No `fillOpacity` key** — alpha lives in the paint: `fills:[{r,g,b,a}]` with 0-1 floats. Same-hue alpha over same-hue is invisible (progress lesson: outer dim track `a≈0.3`, inner solid fill).
- **Hug sizing on a pill/track collapses it to content size** — fixed w/h for toggle tracks.
- **`edit.delete` (not node.delete).** Deleting a set deletes its variants. `select.byName {query, page:"all"}` matches layer-name SUBSTRINGS; text layers auto-name from content unless explicitly named.
- **Props that DON'T exist:** `fillOpacity`. Valid oddities: `strokeSides [t,r,b,l]`, `dashes`, `mainAlign:"spaceBetween"`, `layout:null` for absolute children.

## QA loop (VLM alone is unreliable on small UI — it misreported correct toggles/checkboxes)

1. `render` page → vision review for layout/overlap.
2. Zoom: `export --node <id> --scale 6` → vision.
3. **Ground truth:** PIL pixel-count exact colors (fill ratios, text presence `#CAC9C9`); `inspect.properties {id}` (W/H/pos + `token:` names); `inspect.componentCode {id}` → generated HTML exposes EMPTY variants (missing children) instantly.
4. Audit sweep: inspect every variant, flag W or H < 8.

## Panomete conventions used
daisyUI names for sets (btn, alert…), variants Size×Style×State, radii: field=32 (buttons/fields), box=16 (cards/modals), selector=16; flat, no shadows; disabled=50% opacity; Sarabun/JetBrains Mono (both installed user-level).