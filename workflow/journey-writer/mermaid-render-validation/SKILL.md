---
name: mermaid-render-validation
description: Use when validating or repairing mermaid diagrams in vaults.
---

# Mermaid Render Validation & Repair

Static checks (init block present, no off-brand hex) do NOT prove a diagram renders. Obsidian render breakage is common in source notes and only a real render catches it. This skill is the mmdc (mermaid CLI) validation loop + the repair rules learned the hard way.

## Setup (one-time per machine)

```bash
# in a scratch dir; do NOT download Chromium — use installed Edge
export PUPPETEER_SKIP_DOWNLOAD=true
bun add @mermaid-js/mermaid-cli puppeteer
```

puppeteer.json:
```json
{"executablePath": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
 "args": ["--no-sandbox", "--disable-gpu"]}
```

Invoke mmdc as `node_modules/.bin/mmdc.exe` directly — `bun x mmdc` from Python subprocess fails (FileNotFoundError). Smoke test: `mmdc -i block.mmd -o out.png -p puppeteer.json -q`.

## Extraction: fence-aware, never regex

Regex `\`\`\`mermaid\n(.*?)\`\`\`` over-captures when fences are mis-fenced or unterminated: it pairs the opener with the NEXT ``` anywhere in the file, swallowing sections into the block. Real vault case: regex found 209 blocks, a line-based fence walk (open on ```mermaid, close on next ``` line, EOF = unterminated) found 218 — the 9 extra were broken blocks the first render pass never tested. Always walk fences line-by-line; include unterminated-to-EOF blocks in the render (they are broken in Obsidian and must be repaired too).

## Batch render

~2.5s/render; 200+ blocks exceeds the execute_code 5-min cell cap. Write a runner script: iterate .mmd files, call mmdc, append failure name + FIRST stderr lines to fails.log, ok-names to done.log. Launch via terminal background=true + notify=true; read logs on completion. Report ok AND fail totals.

## Reading the error

mmdc prints a long puppeteer stack trace; the actual message is the FIRST stderr lines (`Error: Parse error on line N:`). Capturing `stderr[-600:]` keeps only the stack — re-run failures capturing stderr HEAD (first ~8 lines).

## Failure classes (both pre-exist in source; theming/appends only inherit them)

1. **Mis-fenced block** — closing ``` sits far later (or is missing): headings/tables/blockquotes swallowed inside the diagram. Fix per block: find the last real diagram line, insert one ``` there; the orphaned later fence re-pairs with its own content. Unterminated mermaid at EOF is the same class.
2. **Cascade shift** (one missing closer shifts EVERY later pair) — a ` ```mermaid ` opener pairs with the NEXT ` ```mermaid ` (or a language-tagged ` ```ebnf `/` ```java `) as its "closer" and swallows all markdown between; the even/odd fence-count balance check still passes. After any fence pass list fences in pairs and flag any ` ```mermaid ` whose next fence is also ` ```mermaid ` or a tagged opener (mermaid→mermaid mispair check). Two sub-shapes: (a) a SPURIOUS extra fence splitting one plain code block shifts the whole alternation from that point — DELETE it, never insert around it; (b) an earlier repair pass inserting a DUPLICATE closer where one already exists — check the line after the insertion point isn't already ` ``` `, and verify the marker line has diagram tokens (`-->`, `[...]`, `style `, `subgraph`, `end`); the walk-back from a `---` horizontal rule lands on the PROSE line just above it, placing the closer after prose.
3. **Mermaid syntax errors** — pattern fixes:
   - unquoted multi-word node target: `|Generates| Editor Support` → `G -->|Generates| "Editor Support"`
   - parentheses inside a label: `D1[Contract testing (Pact)]` → `D1["Contract testing (Pact)"]`
   - subgraph titles with spaces referenced in edges: `subgraph Level 1: Overview` + `Level 1 --> Level 2` → give subgraphs ids: `subgraph Level1["Level 1: Overview"]`, then `Level1 --> Level2`.

## Repair rules

- NEVER blanket-fix fences with a heuristic walker inserting ``` at "markdown-looking" lines. Multi-line node labels (`["line1\nline2"]`), `|...|` edge labels, and class-member lines (`- item`) misclassify as boundaries; one such walker broke 69 previously-good diagrams (reverted via `git checkout -- <folders>`). Repair ONLY blocks that fail the render, surgically, per block.
- Vault under git (auto-backup job): `git checkout -- <paths>` is the undo handle for any over-wide write.
- After repairs, re-render ALL blocks (not just the fixed ones) and require zero failures.
- Repair is a LOOP, not one pass: render → collect failures → fix surgically bottom-up (descending line order so indices stay valid) → re-extract blocks → re-render ALL → repeat until zero failures. A cleanup that shifts fence pairing CAN break blocks that passed the previous round; the first render round is never the last. The background-notify output is TRUNCATED at the head — poll the process log for the FULL failure list; the first failing block is the one most likely to be a lingering cascade shift, and missing it means the next round fails again.
- Sequence: render baseline BEFORE touching a vault (are the diagrams already broken?); render again after any edit pass; compare fail sets — do not attribute pre-existing breakage to your edits.

## When to use

- User reports "some mermaid is broken" after a vault-wide edit pass (theme injection, dash cleanup) — diagnose by render, not by eye.
- After any scripted transformation of mermaid blocks (init injection, color remap): every run ends with a full re-render or you have not finished.
