---
name: drawio-diagrams
description: "Use when creating or porting diagrams to draw.io files."
version: 1.0.0
author: Hermes Agent
license: MIT
dependencies: []
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DrawIO, Diagrams, Flowcharts, Architecture, Visualization, XML, Mermaid]
    related_skills: [excalidraw, architecture-diagram]

---

# draw.io Diagram Skill

Author `.drawio` files directly and prove they render correctly. Covers porting a
diagram (mermaid block, prose spec, another tool) into draw.io and placing the
result at a requested path.

XML syntax, style properties, containers, layers, tags and layout passes are
documented in the `open_drawio_xml` tool schema — read it at generation time
rather than reproducing it here. This skill carries the **workflow and the
defects the schema does not mention**.

## When to Use

- A request names a `.drawio` file, draw.io, or asks to place a diagram at a path.
- A mermaid block, prose spec, or another tool's diagram must become a `.drawio`.
- An existing `.drawio` needs a page added, edited, or verified — use the MCP's
  `list_pages` / `get_page` / `set_page` against it.

Not the tool for hand-drawn Excalidraw JSON (see `excalidraw`) or an HTML/SVG
render (see `architecture-diagram`).

## Workflow

### 1. Establish the source of truth

Read the source and decide what "faithful" means: structure, labels, and the
source's *own* palette. Port those colors rather than accepting draw.io defaults
(see **Palette fidelity**). When the source has a quirk — a repeated color, two
paths converging on one outcome — replicate it and record it as a finding; do not
silently redesign. This user reviews before committing and wants discrepancies
surfaced, not smoothed over.

### 2. Write the `.drawio` file directly

The drawio MCP's `open_drawio_xml` / `open_drawio_mermaid` / `open_drawio_csv`
**open the editor and never write to disk.** An `open_*` call cannot satisfy a
"place it at this path" request; create the file with `write_file`, then use the
MCP's file operations to inspect it.

Envelope — store pages uncompressed (readable, diffable, and the MCP
decompresses either way):

```xml
<mxfile host="app.diagrams.net" agent="Hermes Agent" type="device">
  <diagram id="my-diagram" name="Page Name">
    <mxGraphModel grid="1" page="1" pageWidth="1160" pageHeight="1250"
                  background="#1B1717">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- vertices then edges -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

If the destination is a directory that already exists, place a content-named
file inside it — do not assume the requested path was meant as the filename.

### 3. Verify it parses through the MCP

`list_pages(path)` first: cheap, returns index/id/name/size, and proves the file
round-trips. Reach for `get_page` only when you need actual cell content — it
pulls the whole page into context. Re-run `list_pages` after any edit.

### 4. Render it and LOOK at the image

Reading XML cannot reveal routing defects: the router computes arrowhead anchors
and bend points at render time, and a syntactically perfect file can still draw
two arrows into the same point.

```bash
"/c/Program Files/draw.io/draw.io.exe" --export --format png --scale 1 \
  --output "C:/absolute/out.png" "F:/absolute/in.drawio"
```

Give `--output` and the input Windows-style forward-slash paths — the CLI is a
native executable and does not understand MSYS `/tmp` paths. Exit 0 plus a
non-empty file is the gate; do not claim the diagram works on the strength of a
successful parse alone.

Then `vision_analyze` the PNG with pointed questions, because a general "does
this look right" prompt misses defects. Ask specifically about:

- text clipped or overflowing inside diamonds / small shapes
- connector lines running **through** a shape
- two arrowheads landing on the **same point** of one target
- edge labels colliding with shapes or with each other
- emoji rendering as tofu boxes

Fix, re-export, and re-inspect until clean.

To assert an exact color, probe the PNG's pixels — vision cannot reliably tell
`#000000` from `#1B1717` and will report a dark background as black:

```bash
python scripts/png_probe.py out.png --at 2,2 --at -3,-3
```

(Negative indices count from the far edge. Stdlib only, no PIL required.)

### 5. Deliver

Ship the `.drawio` plus a rendered `.png` beside it — this user keeps preview
PNGs alongside diagram files.

## Always-on rules

**Palette fidelity when porting from mermaid.** Translate the source's
`%%{init ... themeVariables}%%` block onto draw.io instead of accepting defaults;
see `references/mermaid-porting.md` for the mapping table. Set the canvas with
`background="..."` on `<mxGraphModel>`. Do not set `adaptiveColors="auto"` on an
explicitly dark canvas — it inverts colors you deliberately chose.

**Give converging and diverging edges distinct anchors.** draw.io auto-computes
anchor points from the nodes' relative centers, so two edges entering one shape
land on the *same* point and their arrowheads stack — it reads as a drawing
error. Two edges leaving one shape likewise share an exit stub. This is the
"specific geometric intent" that justifies connection-point overrides:

- multiple edges into one target → set a distinct `entryX`/`entryY` per edge
  (e.g. left edge `0,0.5` and bottom edge `0.5,1`)
- multiple edges out of one source → set `exitX`/`exitY` per edge
- check that the two paths then run in separate channels and do not cross

**Give edge labels a background chip.** On a dark canvas a `Yes`/`No` label sits
on top of its own connector line; set `labelBackgroundColor` on the edge style.
Keep labels to one to three words.

**Size text-bearing shapes for their longest line.** A decision diamond's usable
text area is roughly 70% of its box — split long questions with explicit `<br/>`
so the router cannot wrap them into the shape's sloped corners.

## Pitfalls

- **Never report success from `list_pages` alone.** It proves the XML parses, not
  that the diagram draws correctly — those are different claims.
- **Do not hand-route with `<mxPoint as="points">` waypoints** to dodge a
  collision; move a node or set an entry/exit anchor instead. Hard-coded
  waypoints break the moment anything is nudged or a layout pass runs.
- **Do not re-send a full page of XML to `open_drawio_xml`** to "show" a file you
  just wrote: the editor opens a detached copy that is not linked to the path, so
  edits made there never reach the deliverable and the two diverge.
- **Escape label markup.** `<br/>` in an attribute value must be `&lt;br/&gt;`,
  and every style carrying HTML needs `html=1` or the tags print literally.
- **Do not `get_page` to confirm an edit landed** — grep the file for the changed
  attribute instead; `get_page` costs a full page of context for one bit of
  confirmation.

## Support files

- `references/mermaid-porting.md` — themeVariable → draw.io style mapping and the
  porting checklist (needed only when converting a mermaid diagram).
- `scripts/png_probe.py` — stdlib PNG pixel probe for asserting exact colors.
