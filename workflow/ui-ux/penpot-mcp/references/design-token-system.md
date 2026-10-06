# Design Token System — Inspecting & Building on the "Tokens Starter Kit"

> Verified 2026-08-25 on Penpot 2.16 with the official "Tokens starter kit" template file. Covers the 3-tier token architecture, the theme switcher, and the rebuild/import workflow for adapting it to a custom design system (e.g. daisyUI forest theme).

## What the Tokens starter kit is

A professionally architected **3-tier token system** — not just a swatch collection. The architecture mirrors daisyUI's semantic-token design:

```
Tier 1 — Raw colors       (e.g. greenblue.600, graypink.950)     ~300 tokens in "Foundations - Colors"
   ↓ {references}
Tier 2 — Theme tokens     (e.g. accent.600, neutral.100)         ~22 tokens in "Color theme - <name>"
   ↓ {references}
Tier 3 — Semantic tokens  (e.g. buttonPrimary.background.default) ~62 tokens in "Light - Base" / "Dark - Base"
   ↓ applied to
Shapes / components on the canvas
```

Reference syntax: a token's `value` can be `"{accent.800}"` (a reference to another token by name) — `resolvedValue` then contains the final hex. This is how daisyUI's `--color-primary` → `primary` → `buttonPrimary.background.default` chain works, replicated natively in Penpot.

## Token set inventory (template's 14 sets)

| Set | Active by default | Purpose |
| --- | --- | --- |
| Foundations - Fixed | ✅ | opacity, rotation, sizing (breakpoints), dimension — structural primitives |
| Foundations - Colors | ✅ | ~300 raw colors across 20 hue families (green, bluegreen, greengray, etc.) × 050–950 shades |
| Density - Modular Scales | ✅ | 8 musical-ratio scales (minor-second → augmented-fourth) |
| Density - Compact / Comfortable / Spacious | only Comfortable | density presets — switchable via themes |
| Modular Scale | ✅ | size.modular.3xs → 3xl (9 values) |
| Linear Scale | ✅ | linear.025 → 800 (12 values) |
| Foundations - Scales | ✅ | size.*, radius.*, space.*, font-size.* — 20+ values each, referencing Modular/Linear |
| Typography | ✅ | 7 levels: display.title → label |
| Color theme - Muted / Vibrant | only Vibrant | accent.050–950 + neutral.050–950 — the theme-able layer |
| Light - Base | ✅ | 62 semantic color tokens (buttonPrimary.*, layerBase.*, input.*, link.*, etc.) |
| Dark - Base | (inactive) | same 62 semantic names, dark-mode values |

## Theme switcher (8 themes)

| Theme | Group | Effect |
| --- | --- | --- |
| Global | Always enabled | foundations — cannot be turned off |
| Compact / Comfortable / Spacious | Density | activates one Density set |
| Light / Dark | Color mode | activates Light-Base or Dark-Base semantic set |
| Vibrant / Muted | Color theme | activates one Color-theme set (the accent/neutral values) |

Switching themes activates/deactivates sets. A shape styled with `buttonPrimary.background.default` restyles instantly when the color-mode theme changes from Light to Dark — because the semantic token resolves through the active theme set.

## Probing the token system (execute_code patterns)

**Token overview (lean — set → type → token-name list):**
```js
return penpotUtils.tokenOverview();
// returns { "Set Name": { "color": ["accent.700", ...], "spacing": [...] } }
```

**Theme + set list (lean):**
```js
const tok = penpot.library.local.tokens;
return {
  themeCount: tok.themes.length,
  setCount: tok.sets.length,
  themes: tok.themes.map(t => ({name: t.name, group: t.group})),
  sets: tok.sets.map(s => ({name: s.name, active: s.active}))
};
```

**Sample one token to confirm reference chain:**
```js
const set = penpot.library.local.tokens.sets.find(s => s.name === 'Dark - Base');
return set.tokens.filter(t => t.name.includes('buttonPrimary')).slice(0, 4)
  .map(t => ({name: t.name, value: t.value, resolvedValue: t.resolvedValue, type: t.type}));
// value: "{accent.800}", resolvedValue: "#422281"
```

## Token-dump timeout pitfall (CRITICAL)

`penpotUtils.tokenOverview()` and `penpot.library.local.tokens` enumeration are **safe** — they return names, not full token objects.

But: **iterating `set.tokens.map(t => ({name, value, resolvedValue, type}))` across ALL 14 sets in one execute_code call TIMES OUT at 30s** when a set has 300+ tokens (Foundations - Colors alone is ~300). The MCP has a 30-second task limit.

**Fix — never dump all tokens at once.** Either:
- Use `penpotUtils.tokenOverview()` (returns only names, no values — fast, sufficient for mapping)
- Or iterate sets one at a time, or filter to a token-type subset, before mapping to full objects
- Or slice heavily: `set.tokens.slice(0, 20).map(...)` when you only need a sample

The full dump is never needed — the token *names* (from `tokenOverview()`) plus a *sample* of the reference pattern (one or two semantic tokens resolved) tell you everything you need to replicate the architecture in a new file.

## Adapting the kit to a custom design system

The template's own "How to use" page states the intended reuse path: *"If you want to reuse these tokens as a starter kit, you can duplicate the file or export and import the tokens from the TOOLS button at the bottom of the TOKENS tab."*

Two viable workflows:

**Option A — Native TOOLS export/import (recommended, preserves reference chain):**
1. In the template file → TOKENS tab → TOOLS button → Export tokens (downloads a JSON/W3C tokens file)
2. Open the target design file → TOKENS tab → TOOLS → Import tokens
3. Modify the theme/semantic token values to the custom palette (~60 value changes, not 300)
4. The `{accent.800}`-style references survive the import — only the resolved values change

**Option B — Programmatic rebuild (slower, value-set during creation):**
1. `const set = penpot.library.local.tokens.addSet({name: 'Foundations - Panomete Colors'})`
2. `set.addToken({type: 'color', name: 'color.primary', value: '#1FB854'})`
3. `set.addToken({type: 'color', name: 'color.accent.800', value: '{color.primary}'})` — reference syntax
4. Rebuild all 3 tiers. Useful when you want to pre-fill values during creation, but it's 300+ API calls.

Prefer A — the native import keeps the reference architecture intact and the modification surface is small.

## Token types available (Penpot TokenCatalog)

`TokenType`: `"color" | "dimension" | "spacing" | "typography" | "shadow" | "opacity" | "borderRadius" | "borderWidth" | "fontWeights" | "fontSizes" | "fontFamilies" | "letterSpacing" | "textDecoration" | "textCase"`

`addToken({type, name, value})` — value can be a direct value (`"#1FB854"`) or a reference (`"{color.primary}"`).

Applying tokens to shapes: `shape.applyToken(token, properties)` where `properties` is an array of `TokenProperty` values (e.g. `["fill"]` for a color token, `["borderRadiusTopLeft", ...]` for a radius token). Application is async — wait ~100ms.

## Mapping daisyUI theme concepts to this token system

| daisyUI concept | Template token type | How to map |
| --- | --- | --- |
| `--color-primary` etc. | `color` | raw tokens in Foundations tier, referenced by theme tier |
| `--color-base-100/200/300` | `color` (neutral) | map to `neutral.050/100/200` in the theme tier |
| `--radius-selector/field/box` | `borderRadius` | map to `radius.*` in Foundations - Scales |
| `--border: 1px` | `borderWidth` | single token |
| `--size-field` / 8pt spacing | `spacing` | map to `space.linear.*` (linear.050=4px, linear.100=8px, ...) |
| font family (Sarabun etc.) | `fontFamilies` | one token per family |
| font sizes (H1→caption) | `fontSizes` | map to the 7 Typography levels |
| `--depth: 0` (no shadows) | `shadow` | set to transparent |
| status colors (info/success/...) | `color` | raw tokens, referenced semantically |

A daisyUI theme maps cleanly: raw colors → theme tier, semantic names → semantic tier, theme switcher → Penpot themes. The whole forest theme can be expressed as one new "Color theme - Forest" set + one "Dark - Panomete Base" semantic set.
