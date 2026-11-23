# Career Path Note Formats

Exact schemas for the two note types in a career-path folder. Copy from the exemplar files when possible; these are the distilled requirements.

## Schema choice (read first)

- **One schema per path.** The unified schema below governs new paths and migrated paths. When ADDING notes to an existing path whose siblings use a different schema (e.g. `note_type`/`career_path`/`prerequisite` frontmatter, a `## Knowledge Connections` link section instead of `## Related`), match the siblings exactly — intra-path consistency beats cross-path uniformity, and Dataview queries work per path. Copy keys and section names from a sibling topic the brief names as the style exemplar.
- Do NOT reintroduce `note_type`/`career_path`/`prerequisite` keys into paths that already carry the unified schema.

## Capability-area overview (`00_overview.md`)

Frontmatter (unified schema — new/migrated paths; see Schema choice):

```yaml
---
title: "Area Name"
role: Applied AI Engineer
capability_area: Area Name
status: complete
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [career-path, applied-ai, ai-engineering, <area-tag>, overview]
source_frameworks:            # optional, keep if present
  - "[[computing-foundation-note/Artificial_Intelligence/AI Overview]]"
---
```

Body sections in order:

- `# Title`
- `> **Capability area:** one-line positioning`
- `## Why This Matters at Senior Level` — mid-vs-senior contrast paragraph + "Senior judgment shows in:" bullet list
- `## Topics in This Area` — table `| # | Topic | Senior Focus |` with bare wikilinks `[[01_Topic_Name]]`
- mermaid flowchart of the area's process (`flowchart LR` or `TD`)
- `## Scope Boundary` — in-scope vs out-of-scope, pointing to the owning area/path for each excluded item
- `## Sources` — vault notes as wikilinks + verified external URLs
- `## Related` — wikilinks

## Capability topic (`0N_Topic_Name.md`)

Frontmatter (unified schema — new/migrated paths; see Schema choice):

```yaml
---
title: "Topic Name"
role: Applied AI Engineer
capability_area: Area Name
topic: Topic Name
status: complete
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [career-path, applied-ai, ai-engineering, <topic-tag>]
---
```

Role overviews (`NN_Path/00_overview.md`) keep their own schema: `note_type, career_family, level, entry_from, next_paths, source_frameworks, created, tags`.

Body sections in order (the wave brief's contract — older families name the links section `## Knowledge Connections` and omit the checklist/pitfalls/success sections; match the family when extending):

- `# Title`
- `> **Core skill:** one-liner` — byte-locked to the contract's topic-table row (older families use a plain `> one-line definition`, byte-locked to the contract's definition string)
- `## Why This Is a Senior Skill` — "A mid-level engineer ... A senior ..." contrast (the level-delta section)
- `## Core Frameworks` — tables: what-to-track | why; tool comparison (tool | strengths | weaknesses | best-for); maturity levels
- ONE mermaid flowchart — double-quoted node labels, `-->` arrows only, no edge labels
- `## In Practice` — 5+ bold principle sentences, each followed by a 2–4 sentence explanation
- `## Practical Exercise` — numbered 5–8 scenario steps
- `## Practical Applications` — 5–8 item checklist and/or one fenced fill-in template
- `## Common Pitfalls` — 3-column table (Pitfall | Why It Fails | Better Approach), 4–7 rows
- `## Success Indicators` — 4–6 bullets
- `## Related` (or the family's equivalent link section) — 3–6 whitelisted wikilinks
- `## Sources` — 2–5 real books/standards by name; no fabricated URLs

Target 6–13 KB per topic file (the wave contract's floor and ceiling). Dense and specific, no fluff.

## Wikilink styles

- Always vault-root-relative with folder path + `|alias`.
- Parent path: `[[career-path/18_Applied_AI_Engineer/00_overview|Applied AI Engineer]]`
- Cross-area: `[[career-path/18_Applied_AI_Engineer/04_AI_Security_and_Guardrails/00_overview|AI Security and Guardrails]]`
- AI notes: `[[computing-foundation-note/Artificial_Intelligence/10_LLM_Production_Patterns]]`
- Inside the same area only: bare `[[01_Topic_Name]]` in the topics table, bare `[[00_overview]]` in prerequisites.
- Inside markdown tables, escape the alias pipe: `[[path\|alias]]`.

## Voice rules

- Open every "Why" section with the mid-vs-senior contrast.
- Capabilities at principle level; frameworks/tools appear only as examples in comparison tables.
- English, direct, no filler.
