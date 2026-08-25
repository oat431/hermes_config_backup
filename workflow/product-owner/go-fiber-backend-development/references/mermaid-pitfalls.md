# Mermaid Diagram Pitfalls (GitHub/Obsidian rendering)

User renders mermaid in markdown spec docs; parse errors surface as "Unable to render rich display — Parse error on line N".

## Hard rule: special characters in node labels

Mermaid flowchart treats certain characters inside **unquoted** node labels as shape/edge tokens:

| Character | What mermaid thinks it is | Symptom |
|-----------|---------------------------|---------|
| `{` `}` | diamond shape start (`{{...}}`) | `Expecting 'SQE', ... got 'DIAMOND_START'` — e.g. `idx:pos{i}:d` in a label breaks the whole diagram |
| `->` | edge arrow | parse error downstream |
| `&` | text marker | risky in some shapes |

**Fix pattern:**
1. Quote the label: `A["Positional index sets — 60 sets"]` — quoted labels accept braces and arrows safely.
2. Prefer removing braces entirely from diagram labels (keep `{i}` notation in prose/tables only — those are not parsed by mermaid).
3. Cylinder `[(...)]` with quoted label `[("...")]` is inconsistent across renderers — when the label needs special chars, use a plain rectangle with quotes and keep cylinders only for simple labels.
4. `<br>` line breaks inside labels are fine.

## Verified-safe constructs

- Quoted subgraph titles: `subgraph Hot["Hot Pool — Valkey/Redis"]`
- Edge labels with `|...|`: `A -->|status: reserved| B` (keep `=`, `+`, spaces fine)
- Dotted edges: `E -.->|label| R`
- `style` lines after edges are fine.

## Pre-commit check

Before committing any spec/proposal doc with a diagram, scan ONLY the mermaid blocks for `{`, `}`, `->` inside `[...]`/`(...)` labels (grep the whole file, then ignore prose/table matches). If a user reports "Unable to render rich display", the fix is always label quoting/shape simplification — not restructuring the diagram logic.
