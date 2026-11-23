# Theming mermaid to a design system

## When to use

- The user asks for diagrams that match their brand or CI ("style it as my CI").
- A vault's diagrams look off-brand next to the rest of a design system.
- You are about to hand-roll hex values into `classDef`s and need a derivation, not a guess.

## 1. Find the source of truth before picking a color

In order of reliability:

1. A tokens file: `*.tokens.css` with `:root { --color-primary: ... }` — machine-readable, exact.
2. A visual-identity / style guide note: palette table, typography, icon rules, dark or light surfaces.
3. An existing themed artifact in the same brand (a dashboard, a deck) — reverse-engineer, then confirm against (1) or (2).

Ask which surface the diagram will live in (dark note, light vault, print). The same tokens need different backgrounds.

Panomete reference set:

- `F:\obsidian_note\oralita_md\personal\brand\panomete.tokens.css` — raw tokens
- `F:\obsidian_note\oralita_md\personal\brand\02_visual-identity.md` — palette, type, iconography, WCAG notes
- `F:\obsidian_note\oralita_md\personal\brand\03_style-guide.md` — chart colors, dark-slide spec

## 2. Base theme

Use `theme: base`. The named themes (`default`, `forest`, `dark`, `neutral`) override `themeVariables` inconsistently; `base` gives you the whole surface.

## 3. Init block

One directive line, first line inside the fence:

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Sarabun, Leelawadee UI, system-ui, sans-serif","fontSize":"14px","background":"transparent","lineColor":"#5E6B67","textColor":"#CAC9C9","clusterBkg":"#161212","clusterBorder":"#2A4A40","edgeLabelBackground":"#1B1717"}}}%%
```

- `background: transparent` so the note's surface shows through.
- `lineColor` one step muted from body text; brand colors are for structure, not for every arrow.
- `clusterBkg` / `clusterBorder` should match elevated surfaces, not the page background.

## 4. Map meaning to tokens

Decide what each color *means* in the diagram before choosing it. One `classDef` per semantic role:

```mermaid
classDef foundation fill:#19362D,stroke:#1EB88E,color:#CDD3D1,stroke-width:1px
classDef receptive  fill:#161212,stroke:#1FB8AB,color:#1FB8AB,stroke-width:1px
classDef productive fill:#161212,stroke:#1FB854,color:#1FB854,stroke-width:1px
classDef application fill:#161212,stroke:#1EB88E,color:#1EB88E,stroke-width:1px

class S4 foundation
class S1,S3L receptive
class S2,S3S productive
class S5 application

style RECEPTIVE fill:#161212,stroke:#2A4A40,color:#1FB8AB
```

Panomete role map (dark surfaces, flat):

| Role | Fill | Stroke | Text | Token |
| --- | --- | --- | --- | --- |
| Foundation / base group | `#19362D` | `#1EB88E` | `#CDD3D1` | neutral + secondary |
| Receptive (read, listen, watch) | `#161212` | `#1FB8AB` | `#1FB8AB` | accent |
| Productive (write, speak) | `#161212` | `#1FB854` | `#1FB854` | primary |
| Application / outcome | `#161212` | `#1EB88E` | `#1EB88E` | secondary |
| Stage node (timeline) | `#19362D` | `#1FB854` | `#CDD3D1` | neutral + primary |
| Detail node | `#161212` | `#2A4A40` | `#CAC9C9` | base-200 + base-300 |

Rules that come from the brand, not from taste:

- **Black on green.** `primary-content` is `#000000`; white text on `#1FB854` fails contrast (1.58:1).
- **Flat.** `depth 0`, 1px strokes, box radius 1rem. No shadows, no gradients, no 3D.
- **No emoji as icons** when the system specifies outline iconography (1.5px stroke, 24×24). Emoji in node labels read as clip-art.
- **60/30/10.** Neutral surfaces dominate, primary is structure, secondary/accent are highlights. A diagram where every node is green violates the ratio.

## 5. Typography

Pick a family with glyph coverage for the content language. Sarabun covers Thai + Latin and is the Panomete body face. `JetBrains Mono` is the code face and has **no Thai glyphs** — a Thai diagram set in mono will tofu. Fall back through `Leelawadee UI` on Windows.

## 6. Validate by render, on the real background

```sh
# the PNG you inspect should use the vault's actual surface, not white
./node_modules/.bin/mmdc.exe -i block.mmd -o block_dark.png -p puppeteer.json -b "#1B1717" -s 2 -q
```

Then look at the image. Check: Thai glyphs complete (no tofu), cluster titles clear of arrows, label contrast, nothing clipped at the edges, colors match the tokens you intended.

## 7. Pitfalls

- **`-w` is not a width flag** in current mmdc; it errors with `unknown option '-w'`. Scale with `-s 2` instead.
- **`-i <note>.md` switches to Markdown mode** and then requires `-o` to end in `.md`/`.svg`/`.png`/`.pdf`. Block-level validation needs the block extracted to `.mmd` first (fence-aware walk, not regex).
- **Generating `puppeteer.json` from Python**: pass the browser path with forward slashes (`C:/Program Files (x86)/.../msedge.exe`) and let `json.dumps` handle escaping. A pre-escaped string goes through `json.dumps` a second time and lands in the file as `C:\\\\Program...`, which mmdc cannot open — the symptom is a browser-not-found error that looks like a puppeteer problem.
- **Same directory as `node_modules`.** Write `.mmd` files next to the installed CLI, or pass absolute native paths. On Windows, bash `$TMPDIR` is not the Hermes Python scratch directory; files written from Python do not exist for a shell that `cd`s to `$TMPDIR`.
- **Edges through cluster titles** is a layout defect, not a syntax error. Uncluster single-node groups (a one-node subgraph only adds a title for arrows to cross), add `direction LR` inside wide clusters, and re-render. Expect one or two iterations before the picture is clean.
- **Mermaid may render cluster borders lighter than the `stroke` you set** (theme variable wins over `style` for some elements). Judge the PNG, not the hex in the source.
- **Emoji/`\n` labels.** Prefer `<br/>`; `\n` inside quoted labels renders inconsistently between mermaid versions.
