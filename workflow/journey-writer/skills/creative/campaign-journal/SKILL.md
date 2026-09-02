---
name: campaign-journal
description: Use when writing TTRPG campaign logs or session journals.
tags: [creative-writing, ttrpg, obsidian, campaign-logs]
---

# Campaign Journal System

Build living campaign journals for TTRPG groups — BG3, D&D, Pathfinder, or any tabletop game. Supports rotating narrators (each player writes from their character's perspective) and multiple narrative styles.

## When to Use

- User wants to create a campaign journal template system
- User just finished a TTRPG session and needs help writing the log
- User mentions "campaign log", "session journal", "adventure chronicle", or similar
- User is playing BG3, D&D, or any narrative RPG with a group

## The Interview → Template → Write Workflow

**Phase 1: Interview (use grill-me patterns)**
Ask about:
1. **Vibe/Style**: Chronicle (in-world adventurer's journal), casual (recounting over drinks), structured log, or hybrid
2. **Organization**: Per-session, by chapter/act, or event-by-event within sessions
3. **Narrator system**: Single narrator, rotating narrators (each player writes in-character), or omniscient
4. **Tracking needs**: Decisions & consequences, companion relationships, NPC index, locations visited
5. **Session length**: 2-3 hours (one event per session) vs 4-6 hours (multiple events per session)

**Phase 2: Template Design**
Build a template kit in Obsidian:
- `00-Index.md` — master hub linking everything
- `Session-Entry.md` — template for each session (with YAML frontmatter)
- `Party-Roster.md` — character profiles including "voice as narrator" guidance
- `Companion-Bonds.md` — relationship tracker (alliances, rivalries, romances)
- `Notable-NPCs.md` — NPC index with per-character opinions

**Phase 3: Write the Entry**
1. Get session details: key events, choices made, consequences, quotes, where session ended
2. Identify the narrator (which character is writing)
3. Write in that character's voice — formal paladin vs sardonic rogue vs poetic elf
4. Structure: chronicle prose → key moments → decisions table → quotes → current location → next session notes

## Narrative Styles

**Chronicle Style** (most popular):
- In-world adventurer's journal
- First-person from narrator's perspective
- Dramatic, literary prose
- "What did you see? What did you feel? What would you never tell the others?"

**Casual Style**:
- Recounting the session over drinks with the party
- Jokes, meme moments, "remember when..."
- Table moments highlighted

**Structured Log**:
- Clean sections, bullet points
- Easy to scan later
- Less narrative, more reference

## Rotating Narrator System

When each player takes turns writing from their character's perspective:
- **Party Roster** page tracks each character's "voice as narrator" (formal? sarcastic? poetic? blunt?)
- Same events told through different eyes — a paladin describes "righteous diplomacy" while the rogue writes "I picked his pocket while the paladin talked"
- **Narrator Rotation Log** in roster tracks who wrote each session
- **NPC opinions** section lets each character comment on recurring NPCs differently

## Template Structure Patterns

**Session Entry YAML frontmatter**:
```yaml
---
session: "01"
title: "The Betrayal at the Grove"
date: "2026-08-14"
narrator: "Character Name"
narrator_class: "Rogue"
attendees:
  - Character 1 (Class, Race)
  - Character 2 (Class, Race)
tags:
  - bg3/session
  - chronicle
---
```

**Key sections for chronicle style**:
- 📜 The Chronicle (main narrative prose)
- 🗡️ Key Moments (notable events as subsections)
- ⚖️ Decisions & Consequences (table: choice | who decided | consequence)
- 💬 Words Worth Remembering (quotes from table and in-game)
- 🗺️ Where We Are Now (location, objective, cliffhanger)
- 📝 Notes for Next Session (loose threads, NPCs to revisit)

**Companion Bonds tracking**:
- Party dynamics table (all pairs for party of 4 = 6 bonds)
- Turning points log (session | characters | what happened | shift direction)
- Optional approval tracker (for BG3's in-game system)

**NPC index**:
- Quick reference table at top
- Detailed entries with per-character opinions section
- Status tracking (alive/dead/unknown/fled)

## Pitfalls

- Don't over-structure casual content — BG3 logs are fun, not forensic
- Don't track every HP and spell slot unless user asks
- Ask about narrator voice BEFORE writing — a Halfling Rogue sounds very different from a Human Paladin
- For 4-6 hour sessions, use event-by-event logging within the session file, not one file per event
- When user describes chaotic evil playthroughs, lean into the dark humor and moral ambiguity in the narrator's voice

## Voice Examples

**Halfling Rogue (sardonic, pragmatic)**:
"Let me tell you something about survival. There are people in this world who'll tell you loyalty is a virtue. Those people are dead. Or they will be."

**Human Paladin (formal, righteous)**:
"The morning sun cast long shadows across the grove as we prepared for what must be done. Honor demanded we stand with the innocent, even when the cost was our own safety."

**Dwarf Wizard (pragmatic, philosophical)**:
"Magic teaches you that every action has consequences. Sometimes those consequences are measured in lives. Today we ended a war by ending all the combatants. Efficient, if not elegant."

## Obsidian Integration

Use wikilinks `[[Note-Name]]` to connect:
- Session entries to party roster, NPCs mentioned, locations visited
- NPC entries to sessions where they appeared
- Companion bond turning points to specific sessions

Tags: `bg3/session`, `bg3/roster`, `bg3/bonds`, `bg3/npcs`, `chronicle`

## Related Skills

- `grill-me` — for the interview phase
- `obsidian` — for file operations
- `humanizer` — for removing AI-isms from narrative voice
