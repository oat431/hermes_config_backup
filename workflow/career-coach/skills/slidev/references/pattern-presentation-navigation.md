---
name: pattern-presentation-navigation
description: Navigation patterns, styled buttons, and cross-file linking for Slidev teaching decks
---

# Slidev Presentation Navigation Patterns

## Critical: Use `<a href>` for Styled Navigation Buttons

The built-in `<Link>` component **silently drops the `class` attribute** — styled `<Link>` buttons render invisible. Always use native `<a href="/routeAlias">` with `inline-block`.

### ❌ Broken (`<Link>` swallows `class`)

```md
<Link to="next-topic" class="px-4 py-2 bg-blue-600 text-white rounded">Next</Link>
```

### ✅ Works (native `<a>` with `inline-block`)

```md
<a href="/next-topic" class="px-4 py-2 bg-blue-600 text-white rounded inline-block">Next</a>
```

**Why `<a href>`:** Slidev's client-side router intercepts `<a>` clicks, so `/routeAlias` URLs work for navigation. The `inline-block` class is required because `<a>` tags are inline by default — UnoCSS `bg-*` / `px-*` utilities won't render properly without it.

### Button Style Palette

| Purpose | UnoCSS Classes |
|---------|---------------|
| Home / neutral | `px-4 py-2 bg-gray-500 text-white rounded inline-block` |
| Prev | `px-4 py-2 bg-blue-400 text-white rounded inline-block` |
| Next / primary | `px-4 py-2 bg-blue-600 text-white rounded inline-block` |
| Section link | `px-4 py-2 bg-green-600 text-white rounded inline-block` |
| Topic card button | `px-4 py-2 bg-{color}-500 text-white rounded hover:bg-{color}-600 inline-block` |
| Small nav (corner) | `px-3 py-1 bg-gray-500/80 !text-white rounded text-sm inline-block` |

### Cover Slide Corner Navigation

Use `abs-bl` (absolute bottom-left) for persistent Home/Prev buttons on cover slides:

```md
---
layout: cover
---

# My Topic Title

<div class="abs-bl m-6 flex gap-2">
<a href="/home" class="px-3 py-1 bg-gray-500/80 !text-white rounded text-sm inline-block">Home</a>
<a href="/prev-topic" class="px-3 py-1 bg-blue-400/80 !text-white rounded text-sm inline-block">Prev</a>
</div>
```

### Key Takeaway / End Slide Navigation

Center a flex row of styled buttons:

```md
<div class="flex gap-3 justify-center mt-6">
<a href="/prev-topic" class="px-4 py-2 bg-blue-400 text-white rounded inline-block">Prev</a>
<a href="/home" class="px-4 py-2 bg-gray-500 text-white rounded inline-block">Home</a>
<a href="/next-topic" class="px-4 py-2 bg-blue-600 text-white rounded inline-block">Next</a>
</div>
```

### Topic Card Grid (Chapter Overview)

```md
<div class="grid grid-cols-2 gap-6 mt-8">
<div class="p-6 bg-blue-50 rounded-lg text-center">

### 1. Topic Name

<a href="/topic-1" class="px-4 py-2 bg-blue-500 text-white rounded inline-block">Start</a>

</div>
<div class="p-6 bg-green-50 rounded-lg text-center">

### 2. Topic Name

<a href="/topic-2" class="px-4 py-2 bg-green-500 text-white rounded inline-block">Go</a>

</div>
</div>
```

## Cross-File Navigation with `src:` Imports

### How It Works

Multiple `src:` entries in `slides.md` (or an overview file) create **one linear deck**. They are NOT separate presentations.

```md
---
routeAlias: chapter-overview
src: ./overview.md
---

---
routeAlias: topic-1
src: ./01-topic.md
---

---
routeAlias: topic-2
src: ./02-topic.md
---
```

- All files are concatenated into a single slide deck
- Arrow keys / next button traverse linearly through ALL files
- `routeAlias` creates named routes for `<a href="/routeAlias">` navigation
- `routeAlias` values must be URL-safe (hyphens, no spaces)

### Pitfalls

1. **Do NOT split into separate `bun run dev` instances** unless topics are truly independent. One deck with `src:` imports + `<a href>` navigation is cleaner.
2. **`routeAlias` must match exactly** in `<a href="/...">`. Typos cause silent failures.
3. **Slide numbering is global** across all imported files. Slide 1 is the first slide of the first file.
4. **`<Link>` does NOT forward `class`** — always use `<a href>` for styled buttons.

## Recommended File Structure for Teaching Decks

```
pages/
├── overview.md              # Chapter overview with topic card grid
├── 01-topic-name.md         # Each topic: cover → content → key takeaway → end
├── 02-topic-name.md
└── ...
```

Each topic file should have this navigation skeleton:

```
Cover slide        → Home button (abs-bl corner)
Content slides     → No nav needed (arrow keys work)
Key Takeaway slide → Prev + Home + Next buttons (centered)
End slide          → Home + Next buttons (centered)
```
