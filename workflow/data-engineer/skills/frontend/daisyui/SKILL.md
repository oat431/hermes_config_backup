---
name: daisyui
description: "Official daisyUI 5 component library skill. Use when generating HTML/JSX with DaisyUI components, colors, themes."
---

# daisyUI 5

daisyUI 5 is a CSS library for Tailwind CSS 4. It provides class names for common UI components, semantic color names and themes.

## Install

```css
@import "tailwindcss";
@plugin "daisyui";
```

## Usage Rules

1. Add daisyUI class names to HTML elements — component class + part classes + modifier classes
2. Customize with Tailwind CSS utility classes when daisyUI classes aren't enough (e.g. `btn px-10`)
3. Use `!` suffix for specificity overrides as last resort (e.g. `btn bg-red-500!`)
4. Create custom components with Tailwind utilities when daisyUI doesn't have one
5. Use responsive prefixes for `flex` and `grid` layouts
6. Only use existing daisyUI class names or Tailwind CSS utility classes
7. No custom CSS — prefer daisyUI classes + Tailwind utilities
8. Use default variant unless user specifies otherwise

## Key Components

- **Button:** `btn` + modifiers: `btn-primary`, `btn-secondary`, `btn-accent`, `btn-ghost`, `btn-link`, `btn-outline`, `btn-sm`, `btn-lg`, `btn-xs`, `btn-circle`, `btn-square`
- **Input:** `input` + `input-bordered`, `input-ghost`, `input-primary`, `input-sm`, `input-lg`, `input-xs`
- **Textarea:** `textarea` + `textarea-bordered`, `textarea-ghost`, `textarea-primary`, `textarea-sm`, `textarea-lg`
- **Select:** `select` + `select-bordered`, `select-ghost`, `select-primary`, `select-sm`, `select-lg`
- **Checkbox:** `checkbox` + `checkbox-primary`, `checkbox-secondary`, `checkbox-accent`, `checkbox-sm`, `checkbox-lg`, `checkbox-xs`
- **Toggle:** `toggle` + `toggle-primary`, `toggle-secondary`, `toggle-accent`, `toggle-sm`, `toggle-lg`, `toggle-xs`
- **Badge:** `badge` + `badge-primary`, `badge-secondary`, `badge-accent`, `badge-ghost`, `badge-outline`, `badge-sm`, `badge-lg`, `badge-xs`, `badge-info`, `badge-success`, `badge-warning`, `badge-error`
- **Card:** `card` with `card-body`, `card-title`, `card-actions`, `card-bordered`, `card-compact`, `card-side`
- **Modal:** `modal` with `modal-box`, `modal-action`, `modal-open`, `modal-backdrop`, `modal-toggle`
- **Navbar:** `navbar` with `navbar-start`, `navbar-center`, `navbar-end`
- **Drawer:** `drawer` with `drawer-toggle`, `drawer-content`, `drawer-side`, `drawer-overlay`
- **Dropdown:** `dropdown` with `dropdown-content`, `dropdown-hover`, `dropdown-open`, `dropdown-end`, `dropdown-left`, `dropdown-right`, `dropdown-top`
- **Alert:** `alert` + `alert-info`, `alert-success`, `alert-warning`, `alert-error`
- **Toast:** `toast` with `toast-start`, `toast-center`, `toast-end`, `toast-top`, `toast-middle`, `toast-bottom`
- **Loading:** `loading` + `loading-spinner`, `loading-dots`, `loading-ring`, `loading-ball`, `loading-bars`, `loading-infinity`, `loading-xs`, `loading-sm`, `loading-md`, `loading-lg`
- **Table:** `table` with `table-zebra`, `table-compact`, `table-normal`
- **Tabs:** `tabs` with `tab`, `tab-active`, `tab-bordered`, `tab-lifted`, `tab-boxed`
- **Collapse:** `collapse` with `collapse-title`, `collapse-content`, `collapse-arrow`, `collapse-plus`, `collapse-open`
- **Join:** `join` with `join-item`, `join-vertical`, `join-horizontal`
- **Tooltip:** `tooltip` with `tooltip-open`, `tooltip-top`, `tooltip-bottom`, `tooltip-left`, `tooltip-right`, `tooltip-primary`, `tooltip-secondary`, `tooltip-accent`, `tooltip-info`, `tooltip-success`, `tooltip-warning`, `tooltip-error`
- **Status:** `status` + `status-info`, `status-success`, `status-warning`, `status-error`
- **Progress:** `progress` + `progress-primary`, `progress-secondary`, `progress-accent`, `progress-info`, `status-success`, `status-warning`, `status-error`
- **Radial progress:** `radial-progress`

## Colors

Semantic color names:
- `primary`, `secondary`, `accent`, `neutral`
- `base-100`, `base-200`, `base-300`, `base-content`
- `info`, `success`, `warning`, `error`

## Themes

Apply with `data-theme="THEME_NAME"` on `<html>` element.
Built-in: light, dark, cupcake, bumblebee, emerald, corporate, synthwave, retro, cyberpunk, valentine, halloween, garden, forest, aqua, lofi, pastel, fantasy, wireframe, black, luxury, dracula, cmyk, autumn, business, acid, lemonade, night, coffee, winter, dim, nord, sunset, caramellatte, abyss, silk

## Config

```css
@plugin "daisyui" {
  themes: light --default, dark --prefersdark;
  root: ":root";
  include: ;
  exclude: ;
  prefix: ;
  logs: true;
}
```

Full reference: https://daisyui.com/SKILL.md

## References

- `references/vite-react-setup.md` — Vite + React + DaisyUI 5 + Tailwind CSS 4 project setup
- `references/tanstack-query-patterns.md` — TanStack Query hooks pattern with query invalidation

## See Also

- **Frontend Checklist:** When reviewing a React + DaisyUI project against the frontend checklist, see `references/frontend-checklist-review.md` for Vite/SPA adjustments.