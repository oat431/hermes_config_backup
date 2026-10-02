---
name: obsidian-decision-note
description: Use when writing oralita_md decision notes.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Notes, Documentation, DecisionRecords]
    related_skills: [obsidian, checklist-review]
---

# Obsidian Decision Notes (oralita_md)

## When to Use

- The user asks for an opinion/verdict ("what do you think about X") and asks to save it under `F:\obsidian_note\oralita_md\personal\note`.
- They frame a technical argument with two camps ("some said A, some said B") and want it settled.
- Extending the decision-note series: `when-not-to-use-graphql.md`, `monolith-first-decision.md`, `ui-library-vs-own-design-system.md`.

Do NOT use for how-to notes, meeting notes, or checklist items — those are different genres (`checklist-review`).

This is a *decision note*, distinct from a checklist or a how-to. Existing examples to imitate: `when-not-to-use-graphql.md`, `monolith-first-decision.md`, `ui-library-vs-own-design-system.md`.

## Non-negotiable house style

Kebab-case filename describing the *decision axis*, not the topic: `api-aggregate-vs-client-composition.md`, `monolith-first-decision.md`. Never `notes-on-x.md`.

Structure, in this order:

1. YAML frontmatter, single line: `tags: [domain, decision-notes, tradeoffs, software-engineering]` — always include `decision-notes` and `tradeoffs`.
2. `# Title` stated as a decision or question, not a noun phrase. Siblings use "When NOT to Use X", "X First: When NOT to...", "A vs B".
3. Blockquote header with exactly three lines: `**Created:**` (real date from `date`, never guessed), `**Grew out of:**` (the concrete trigger — usually *the checklist gap* naming the vault checklist path it extends), `**The question:**` (the user's actual question, restated).
4. `## TL;DR` — a numbered verdict list. Lead with the recommendation, not the background.
5. Numbered `## N. Section` body — tables, concrete numbers, anti-pattern tables.
6. `## Key takeaways` — bullets, each a claim with its consequence.
7. `## Links` — vault checklist paths + `[[wikilinks]]` to adjacent decision notes.

## Two rules that make these notes good instead of generic

**Anchor to a checklist gap.** Search `F:\obsidian_note\swe-knowledge\checklist\` for the relevant checklist first (e.g. `api-checklist/api.md`) and name the section in "Grew out of" and "Links". A checkbox can't carry the *why* — that is the note's reason to exist. Verify the gap is real by grepping the checklist for the topic; don't claim a gap that isn't there.

**Compute the numbers, never hand-wave them.** These notes are persuasive because they carry real arithmetic. Use `execute_code` for availability multiplication (0.999^n and monthly minutes on a 43,800 min month), latency models, cache-variant counts, connection-pool multipliers. Cite the modelling assumptions in-line. If the honest model *undercuts* the popular argument, say so — that reversal is the most valuable content in the note (e.g. client-parallel vs backend-aggregate latency is a tie, so latency is not the deciding axis).

## Mermaid: decision trees only, and validate before writing

The user prefers Mermaid flowcharts over tables for **decision trees / selection criteria**; keep plain tables for costs, trade-offs and anti-patterns. One `flowchart TD` after the TL;DR is the pattern.

Mermaid is silently fragile in Obsidian — validate before finishing:

- Quote **every** node label: `Q1{"Same bounded context?"}` `R1["Ship it"]`. Bare parentheses and slashes in unquoted labels break rendering.
- Use `<br/>` for line breaks inside labels; `-->|Yes|` for edge labels; reachable terminal node per branch.
- Verify with node: extract fenced `mermaid` blocks, assert 1 block, count `-->` edges, assert no bracket line lacks quotes, assert total ``` fences is even.

## Finish by linking, then offer the checklist update

Wikilinks must resolve to notes that actually exist in the same folder — list the directory before writing. After writing, offer (do not unilaterally edit) adding the missing item to the swe-knowledge checklist, since that is the durable follow-through.

## Write it in one pass

`write_file` the whole note at once — never build it incrementally with appends. Read two sibling notes first for tone; the prose is direct, declarative, opinionated, and uses "🔴/🟡" or bold for verdicts. Avoid hedging: the value of the note is that it takes a position.
