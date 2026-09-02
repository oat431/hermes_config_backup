# Component-Template Workflow — Remapping Library Colors & Fonts

> Verified 2026-08-25 on Penpot 2.16 with a component-rich design system template (724 components, 34 library colors, 0 token sets). Covers the workflow for remapping a pre-built component template to a custom palette without a token system.

## When this workflow applies

- The Penpot file has **pre-built components** (100+) but **no token sets** (`penpot.library.local.tokens.sets.length === 0`)
- Components reference **library colors directly** (not through tokens)
- You need to change the palette of ALL components at once

This is the opposite of the token-system workflow (see `references/design-token-system.md`). No theme switching, no 3-tier reference chain. But you get production-ready components immediately.

## Inspection checklist

```js
const lib = penpot.library.local;
const tok = penpot.library.local.tokens;
return {
  tokenSets: tok.sets.length,        // 0 = no token system
  themes: tok.themes.length,         // 0
  libraryColors: lib.colors.length, // 34 = color-driven system
  libraryTypographies: lib.typographies.length,
  libraryComponents: lib.components.length  // 724
};
```

Then inspect the 34 colors to understand the naming convention:
```js
return lib.colors.map(c => ({name: c.name, path: c.path, color: c.color}));
```

Common naming patterns:
- `d.color.background.primary` = dark-mode background (the `d.` prefix)
- `l.color.background.primary` = light-mode background (the `l.` prefix)
- `d.color.accent.primary` = dark-mode brand accent
- `d.color.foreground.primary` = dark-mode text color
- `d.color.accent.success/warning/error/info` = status colors

## Remapping colors — the batch-size constraint

**CRITICAL:** Each `color.color = '#...'` assignment cascades to every component that references that color. With 724 components, a single color change can trigger thousands of internal updates. Batches of 30+ colors in one `execute_code` call **TIME OUT** at the 120s MCP task limit.

**Safe batch size: 3-5 colors per call.** Group by role:

```
Call 1: dark backgrounds (4-5 colors)
Call 2: foreground (2 colors)
Call 3: accent/brand (3-5 colors)
Call 4: status colors (4-6 colors)
Call 5: light mode mirrors (5-11 colors)
Call 6: avatar colors (skip — per-user, keep as-is)
```

### The mapping table (daisyUI forest → component-template colors)

| Component-template color | Forest value | Role |
| --- | --- | --- |
| `d.color.background.primary` | `#1B1717` | base-100 page background |
| `d.color.background.secondary` | `#161212` | base-200 elevated surface |
| `d.color.background.tertiary` | `#110D0D` | base-300 borders/depth |
| `d.color.background.quaternary` | `#0A0808` | darkest |
| `d.color.foreground.primary` | `#CAC9C9` | body text on dark |
| `d.color.foreground.secondary` | `#CDD3D1` | muted text |
| `d.color.accent.primary` | `#1FB854` | brand green |
| `d.color.accent.secondary` | `#1EB88E` | secondary teal-green |
| `d.color.accent.tertiary` | `#1FB8AB` | accent cyan-teal |
| `d.color.accent.primary.muted` | `#19362D` | neutral (unsaturated UI) |
| `d.color.accent.success` | `#00A96E` | success |
| `d.color.accent.warning` | `#FFBE00` | warning |
| `d.color.accent.error` | `#FF5861` | error |
| `d.color.accent.info` | `#00B5FF` | info |
| `d.color.background.success` | `#0A2927` | dark success bg |
| `d.color.background.warning` | `#441606` | dark warning bg |
| `d.color.background.error` | `#500124` | dark error bg |
| `d.color.background.info` | `#082C49` | dark info bg |
| `l.color.*` mirrors | darker green for light bg | `#1A9D47` etc. |

### Code pattern per batch

```js
const lib = penpot.library.local;
const updates = [
  ['d.color.background.primary', '#1B1717'],
  ['d.color.background.secondary', '#161212'],
  ['d.color.background.tertiary', '#110D0D']
];
let done = [];
for (const [name, hex] of updates) {
  const c = lib.colors.find(cl => cl.name === name);
  if (c) { c.color = hex; done.push(name); }
}
return {updated: done};
```

## Typography swap

Pre-built templates typically use a default font (e.g. Work Sans, DM Sans). Swapping to a custom font requires updating all library typographies:

```js
const lib = penpot.library.local;
const sarabun = penpot.fonts.findByName('Sarabun');
for (const t of lib.typographies) {
  t.fontFamily = 'Sarabun';
  t.fontId = sarabun.fontId;
  const v = sarabun.variants.find(vari => vari.fontWeight === t.fontWeight);
  if (v) t.fontVariantId = v.fontVariantId;
}
```

This cascades to all text shapes that use library typographies. Text shapes with inline font settings (not via library typography) won't change — those need `font.applyToText()` per shape.

## Verification without PNG export

Files with 700+ components can't export via `export_shape` (times out). Verify color changes by reading a component's fills:

```js
const lib = penpot.library.local;
const btn = lib.components.find(c => c.path === 'Dark / Button / Primary / Text' && c.name === 'Default');
const main = btn.mainInstance();
const shapes = penpotUtils.findShapes(s => true, main);
return shapes.filter(s => s.fills?.length > 0).map(s => ({
  name: s.name, fill: s.fills[0]?.fillColor
}));
// Confirm: fill === '#1FB854' (your target)
```

## Component-template vs token-system — when to use which

| | Component template | Token system (Tokens starter kit) |
| --- | --- | --- |
| **Components** | 724 pre-built, drag-and-drop | 0 — build from scratch |
| **Palette change** | Modify 34 library colors (cascades) | Modify token sets (cascades via references) |
| **Theme switching** | No — manual color swap | Yes — switch active sets/themes |
| **Font swap** | Update 7 library typographies | Update typography tokens |
| **Best for** | Immediate UI building with real components | Design systems that need theme variants |
| **Export** | Times out (too heavy) | Works (lighter file) |

If the user wants **production-ready components now** and doesn't need theme switching → component template.
If the user needs **multiple themes** or wants the daisyUI-style `data-theme` behavior → token system.
