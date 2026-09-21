# Career Path Note Formats

Exact schemas for the two note types in a career-path folder. Copy from the exemplar files when possible; these are the distilled requirements.

## Capability-area overview (`00_overview.md`)

Frontmatter:

```yaml
---
title: "Area Name"
note_type: capability-area-overview
capability_area: kebab-case-name
career_path: kebab-case-path-name
source_frameworks:
  - "[[computing-foundation-note/Artificial_Intelligence/AI Overview]]"
tags: [career-path, applied-ai, ai-engineering, <area-tag>, overview]
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

Frontmatter:

```yaml
---
title: "Topic Name"
note_type: capability-topic
capability_area: kebab-case-name
career_path: kebab-case-path-name
prerequisite:
  - "[[00_overview]]"
tags: [career-path, applied-ai, ai-engineering, <topic-tag>]
---
```

Body sections in order:

- `# Title`
- `> one-line definition`
- `## Why This Is a Senior Skill` — "A mid-level engineer ... A senior ..." contrast
- `## Core Frameworks` — tables: what-to-track | why; tool comparison (tool | strengths | weaknesses | best-for); maturity levels
- `## In Practice` — 5+ bold principle sentences, each followed by a 2–4 sentence explanation
- `## Practical Exercise` — numbered 5–8 steps

Target ~100–150 lines per topic file, ~100 per area overview. Dense and specific, no fluff.

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
