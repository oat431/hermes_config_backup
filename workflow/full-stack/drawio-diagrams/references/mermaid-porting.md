# Porting a Mermaid Diagram to draw.io

Needed only when the source is a mermaid block. draw.io's Mermaid parser converts
syntax, but the `%%{init ...}%%` theme directive has **no draw.io equivalent** —
that palette must be translated by hand, or the port silently loses the source's
identity.

## themeVariables → draw.io

Read the source's init block and map every key it actually sets. Keys not present
in the source should be left to draw.io defaults rather than guessed.

| mermaid themeVariable | Meaning | draw.io target |
|---|---|---|
| `background` | canvas | `background="…"` on `<mxGraphModel>` |
| `primaryColor` | default node fill | `fillColor=` on vertex styles |
| `primaryTextColor` | default node text | `fontColor=` |
| `primaryBorderColor` | default node border | `strokeColor=` |
| `nodeBorder` | decision/shape border | `strokeColor=` |
| `mainBkg` | principal shape fill | `fillColor=` |
| `lineColor` | connector stroke | `strokeColor=` on edge styles |
| `edgeLabelBackground` | edge label chip | `labelBackgroundColor=` on edge styles |
| `clusterBkg` | group/container fill | `fillColor=` on `swimlane` / `group` |
| `clusterBorder` | group/container border | `strokeColor=` on the container |
| `titleColor` | diagram title text | `fontColor=` on the title cell |
| `fontSize` | base text size | `fontSize=` |

## Per-node and per-edge styling

Mermaid's three styling mechanisms all collapse to ordinary style strings:

| mermaid | draw.io |
|---|---|
| `style Node fill:#RRGGBB,color:#RRGGBB` | `fillColor=` / `fontColor=` on that vertex |
| `classDef` + `Node:::cls` / `class A,B cls` | same two properties, applied to each vertex |
| `linkStyle N stroke:#RRGGBB` | `strokeColor=` on the N-th edge (edges are emitted in definition order) |

Mermaid and draw.io both use `#RRGGBB`, so hex values copy across unchanged.

## Porting checklist

1. **Delete the init directive** after translating it — leaving it produces a
   literal text node.
2. **Set the canvas explicitly** on `<mxGraphModel>`; do not rely on the default
   white page.
3. **Copy per-node fills verbatim, including duplicates.** If the source paints
   two different tiers the same hex, port it as-is and record the collision as a
   finding — this user reviews before committing and does not want a silent
   redesign. Offer the distinct hue as a follow-up change.
4. **Do not set `adaptiveColors="auto"`** on an explicitly dark canvas; it
   inverts colors that were chosen deliberately.
5. **Keep emoji.** draw.io renders them correctly with `html=1`, so a 🧪 / 🏠 /
   🔴 tier marker survives the port intact. (This is unlike Excalidraw, which
   drops emoji entirely.)
6. **Escape line breaks.** Mermaid's `<br/>` inside a label becomes
   `&lt;br/&gt;` inside the XML attribute, with `html=1` on the style.
7. **Preserve branch structure exactly**, including paths that look wrong — a
   `C -->|No| T4` alongside `D -->|No| T4` is a converging pair that needs
   distinct `entryX`/`entryY` anchors, not a reason to reroute the logic.
8. **Choose the layout pass from the tool schema** (ELK thresholds, hand-placed
   grids) rather than guessing — that guidance lives in `open_drawio_mermaid` /
   `open_drawio_xml`.
9. **Verify against the source list, not memory.** Re-read the mermaid block and
   confirm every node id, edge label, and style line made it across; a port is
   complete only when the edge count and endpoint mapping match.
