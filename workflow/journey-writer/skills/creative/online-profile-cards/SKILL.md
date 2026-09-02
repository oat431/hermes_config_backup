---
name: online-profile-cards
description: Use when writing or redesigning GitHub profile READMEs.
tags: [creative-writing, github, profile, dnd, ttrpg, linkedin, bio]
---

# Online Profile Cards

Design and write online identity cards — GitHub profile READMEs, LinkedIn About sections, personal website bios — using creative formats. The signature pattern is the D&D character sheet: map real-world identity to RPG attributes, ability scores, equipment slots, and quest logs.

## When to Use

- User wants to write or redesign their GitHub profile README
- User wants a LinkedIn About section with personality
- User mentions "profile README", "github bio", "online card", "personal website bio"
- User wants to make their profile "fun", "creative", or "stand out"
- User asks for a template to share with friends

## The Interview Flow

Before writing, clarify:

1. **Theme/Vibe**: D&D character sheet? Cyberpunk? Minimalist? Coffee-shop? Meme-heavy? The user picks the aesthetic.
2. **Source material**: Where is their real data? (Career profile, resume, LinkedIn, existing README, etc.)
3. **Scope**: Full rebuild? Quick polish? Just add widgets?
4. **What to exclude**: Some users want project history hidden (resume-only), stats cards removed (self-hosting concerns), etc.
5. **Template needed?**: Does the user want a reusable template for friends?

## The D&D Character Sheet Pattern

This is the most-requested pattern. Every section maps to a TTRPG concept:

| Section | RPG Concept | Real Content |
|:---|:---|:---|
| Title block | Character name + class + level | Name, Role, Years of experience |
| Character Sheet | D&D attribute table | Job title, education, location, languages, alignment, familiar |
| Ability Scores | STR/DEX/CON/INT/WIS/CHA | Top 6 professional skills, scored 10-18 |
| Equipment | Inventory slots (Main Hand, Off-Hand, Armor, Boots, Rings) | Tech stack, each slot = one category with flavor text |
| Quest Log | Rarity tiers (Legendary/Epic/Rare/Uncommon/Side Quests) | Project portfolio with real metrics |
| Inventory | Backpack | Languages, frameworks, certs, traits and quirks |
| Current Quest | Active objective | What they're doing now, what they're looking for |
| Footer | Stats cards, visitor scroll, closing quote | github-readme-stats, visitor counter, thematic quote |

### Ability Score Mapping

Map professional skills to D&D stats. Be honest — 18 = god-tier, 10 = average. This is funny, not a flex:

| Stat | Typical mapping |
|:---|:---|
| STR | Backend, algorithms, raw coding power |
| DEX | DevOps, CI/CD, automation, speed |
| CON | Testing, reliability, uptime, resilience |
| INT | System design, architecture, planning |
| WIS | Mentoring, code review, debugging intuition |
| CHA | Communication, docs, stakeholder management |

### Equipment Slots

Eight slots — each gets a short paragraph of flavor text:

| Slot | What goes there |
|:---|:---|
| Main Hand | Primary language/framework (what they wield daily) |
| Off-Hand | Secondary stack (microservices, side language) |
| Ranged | Frontend / cross-stack reach |
| Helmet | Infrastructure / cloud / deployment |
| Armor | Databases / data layer |
| Boots | CI/CD / version control / how they ship |
| Ring 1 | Methodology / philosophy (how they think) |
| Ring 2 | Bonus skill / side quest carry-over |

### Quest Log Rarities

Projects get tiered by scope and impact:

| Rarity | Criteria |
|:---|:---|
| Legendary | Enterprise-scale, 50+ person team, multi-year, generational impact |
| Epic | Greenfield platform, 10K+ daily users, production at scale |
| Rare | High-impact contribution, measurable improvement (50%+ reduction) |
| Uncommon | Team project, notable achievement, award-winning |
| Side Quests | Smaller projects, one-line each |

## GitHub Stats Cards

See `references/github-stats-cards.md` for the current landscape — which services are maintained, which are paused, and self-hosting options.

Key points:
- `github-readme-stats` (anuraghazra) is **unmaintained** — use `github-stats-extended` instead
- `github-stats-extended` adds: `show=reviews,prs_merged`, `locale=th`, `rank_icon`, donut/pie layouts, `transparent` theme
- Two self-hosting paths: GitHub Action (static SVGs, zero infra) or Vercel (live API, full control)
- Always ask: "Is the public instance paused? Do you want to self-host?"

## Template Generation

When the user wants a template for friends:

1. Take the finished README and replace all personal data with `{{placeholder}}` syntax
2. Add comments explaining each slot's purpose and how to pick values
3. Include badge construction hints (shields.io URL format, Simple Icons logo names)
4. Save to the user's template directory (e.g. `templates/online-card/`)

Template file: `templates/dnd-character-sheet-github-readme.md`

## Pitfalls

- Don't force the D&D theme if the user wants something else — ask about vibe first
- The quest log is a resume substitute — some users want it hidden until their project-spec is done
- Stats cards from `vercel.app` go down when the maintainer pauses the project — always check before adding
- Badge URLs break silently — double-check for stray `\t` and encoding issues
- Typos in profile READMEs are visible to every visitor — audit for spelling before shipping
- The `Race` row in the character sheet is a D&D-ism — don't let it read as real-world race; always pair it with lineage/education context
- Home Base should be fun (`Terra, Siam` not `Thailand`) — the whole point is the fantasy layer

## Related Skills

- `campaign-journal` — for actual TTRPG session logs, not profile design
- `humanizer` — for stripping AI-isms from the profile prose
- `writing-practice-audit` — for deeper critique of the writing quality
