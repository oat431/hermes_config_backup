---
name: branding-ci
description: Use for brand/CI identity, style guides, and brand docs.
version: 1.0.0
author: ox-alpha (Hermes Agent)
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [branding, ci, style-guide, brand-identity, powerpoint]
---

# Branding & CI Documentation

## When to use

User asks for anything brand/corporate-identity shaped: "build a brand", "we need brand CI/guidelines", "make our decks consistent", competitor visual audits, style-guide authoring, brand-kit delivery. Pairs naturally with PowerPoint templating and UX/UI design-system work (§9 Digital Applications of the style guide is the bridge).

## Deliverable kit (established 2026-08-25)

Lives in the user's Obsidian vault: `F:\obsidian_note\oralita_md\personal\brand\` (NOT `templates/brand/` — the templates live elsewhere; personal brand docs go under `personal/`).

| File | Role |
| --- | --- |
| `00_brand-roadmap.md` | Master index: what CI is, 6-phase journey, one-pass checklist, study links |
| `01_brand-strategy.md` | Audience, competitor visual audit, positioning fill-in, mission/vision/values, personality sliders, voice do/don't |
| `02_visual-identity.md` | Moodboard → 3-tier palette (HEX/RGB/CMYK + WCAG gates) → type hierarchy → logo system (4 assets + don'ts) → supporting elements |
| `03_style-guide.md` | 10-section CI manual skeleton, incl. §9 digital apps (UI/social/email/presentations) |
| `04_design-process.md` | Client project checklist A→G with gates + delivery folder structure |

Live client copies: `YYYYMMDD-<brand>-<doc>.md`, placed near the project (vault quick-notes go to `F:\obsidian_note\oralita_md\Quick Note` unless told otherwise).

## Compressed scope — "design system, not a brand" (established 2026-08-25)

When the user explicitly says "not a brand, just a design system" / "I just want to pick colors without second-guessing" / "a design system identity" — they want the **visual identity lock** without the full positioning/mission/vision theatre. This is a legitimate, common scope for engineers and solo builders.

**Compress the 6-section strategy form to the 4 inputs that actually drive visual decisions:**
1. Personality adjectives (3–5) — drives color temperature, type weight, spacing density
2. Emotions (2–3) — drives palette energy and saturation
3. Primary surface mode (dark vs light) — drives which palette tier is "home"
4. Inspiration anchor — a concrete reference system (see below)

Skip: full audience analysis, competitor audit table, mission/vision/values fill-in, positioning statement paragraph. Replace with a 2-line positioning one-liner and a decision log. The strategy gate still passes — but on compressed inputs.

## Inspiration anchor (alternative to competitor audit)

When the user names a **concrete reference system** ("I like daisyUI's forest theme", "use the Linear aesthetic", "make it look like Stripe") — treat that as the inspiration anchor and **skip the 5-competitor visual audit** (§2 of the strategy template). The anchor IS the audit.

**Technique — pull real values, don't approximate from memory:**
- daisyUI themes: fetch `https://cdn.jsdelivr.net/npm/daisyui@5/themes.css` via curl, grep for `[data-theme=<name>]`, extract OKLCH values
- Convert OKLCH → HEX/RGB/CMYK with a Python script (oklch→oklab→linear-sRGB→sRGB→HEX; clamp values >255 to gamut)
- Verify WCAG contrast for every content-on-color pair before locking
- Record OKLCH source values in the identity doc for reproducibility

A palette chosen from real source values, with WCAG verified, is defensible. A palette guessed from memory is not.

## Method — zero → hero phases

0 Learn → 1 Strategy → 2 Visual identity → 3 Guidelines → 4 Application → 5 Maintain.

**Hard gate:** strategy approved before ANY design work. Positioning statement + 3–5 personality adjectives done first. Design expresses strategy; a great logo cannot fix wrong positioning.

## Framework cheat sheet

- **Process:** 5 stages (research/context → strategy → execution → measurement → adjustment)
- **Positioning:** 4 questions — who is it for / what do we do differently / what should people feel (pick 2–3 emotions) / brand personality as a person
- **Palette:** 3 tiers (primary recognition carrier / secondary accent 1–2 max / neutral backgrounds+text); record HEX (web) + RGB (screen) + CMYK (print); usage ratio ~60/30/10; WCAG AA ≥4.5:1 text, ≥3:1 large/UI
- **Typography:** usually one family with weights; if two → display face + workhorse; document H1→caption with weight/size/line-height/tracking + web fallback stack + license
- **Logo system, not a mark:** primary lockup, secondary/submark, wordmark, favicon; define clearspace, min sizes, approved backgrounds, variants (full color / reversed / single black) + written don'ts
- **Guidelines anatomy:** 10 elements — foundation, logo rules, color specs, typography system, imagery, voice/tone, iconography/graphic elements, layout/grid, digital applications, personality/positioning
- **Voice:** do-say/don't-say lists + banned words; tone shifts by context, voice never does

## Vault template conventions (match these)

- YAML frontmatter: `date: YYYY-MM-DD` + `tags: [domain, template, topic]`
- Opening blockquote = usage instruction (copy-as / link back to roadmap)
- Fill-in masters fenced in ```markdown blocks, each followed by a "Filled example" block
- Wikilinks `[[00_brand-roadmap]]` chaining kit files
- Tables for structured fills, checkboxes for checklists

## Pitfalls

- **Logo-first request:** redirect to Phase 1 — most businesses rush to a logo before answering harder questions
- >5 personality adjectives = no personality; >2–3 palette options shown = worse client decisions (Hick's law)
- Guidelines nobody reads: practical beats exhaustive; every rule paired with ✓ correct / ✗ incorrect visual example
- Always include version/date/changelog block — guidelines are a living document
- **"Not a brand" scope correction:** when the user says "not a brand, just a design system," DO NOT force the full 6-section strategy template on them. Use the compressed scope (above). Forcing positioning/mission/vision on an engineer who just wants locked colors is over-engineering — they'll disengage. Detect the signal early and compress.
- **Palette from memory is not a locked palette.** Never specify hex values from memory ("the daisyUI forest green is probably around #1abc5c"). Always pull real source values from the actual theme CSS / design file / API, convert precisely, and verify WCAG before locking. Guessing destroys the "no second-guessing" promise the design system exists to deliver.

## References

- `references/branding-sources.md` — condensed source bank: URLs, what each contributed, real-world guideline hubs to study, key stats
