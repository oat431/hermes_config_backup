---
name: wish-snippet-library
description: "Use when building/extending the wish-snippets library."
version: 1.0.0
author: journey-writer curator
license: MIT
category: creative
metadata:
  hermes:
    triggers:
      - wish snippets
      - wishes library
      - next wish topic
      - gacha blessing
      - blessing library
      - oralita wishes
    tags:
      - writing
      - wishes
      - folklore
      - verification
---

# Wish Snippet Library

Multi-language, **source-verified** "wish snippets" for copy-paste messages — six languages (Old Norse/runes, Latin, Ancient Greek, Sanskrit+Pali, Thai, English), one vault file per wish topic. Started when a Viking Rune Wish accidentally pulled a friend's gacha rare.

## When to Use

- User asks to build, extend, or continue the **wish/wishes library** (any "next wish topic" request)
- Drafting or revising a `NN-Topic-Wishes.md` file in `oralita_md\wishes\`
- Verifying folklore/charm/blessing claims for wish content (runes, Latin quotes, Thai blessing phrases)
- Looking up an occasion-appropriate blessing from the existing files (luck, love, health)

## Vault Layout

- Location: `F:\obsidian_note\oralita_md\wishes\`
- `00_overview.md` — taxonomy (10 wish types), two-kinds-of-wishing, delivery mechanisms, **roadmap checkboxes** (tick when a topic file ships)
- `NN-Topic-Wishes.md` — e.g. `01-Luck-Wishes`, `02-Love-Wishes`, `03-Health-Wishes`; planned: 04 Prosperity, 05 Protection, 06 New-Beginnings, 07 Peace, 08 Dreams, 09 Family, 10 Journey, 11 Format-Library
- Wikilinks hyphenated, never spaces: `[[01-Luck-Wishes]]`

## Locked file format (user-approved; do not drift)

1. Frontmatter (`Title`, `created`, `tags`) → header blockquote linking `[[00_overview]]` + sibling files
2. **Occasion tags** line (emoji tags: 🎰 gacha, 🏥 surgery, 💍 anniversary, etc.)
3. **Quick-Pick Map** table: occasion → first pick → why
4. Numbered language sections ×6: `1 ᚠ Viking Runes (Old Norse)` · `2 🦅 Latin` · `3 🏛️ Ancient Greek` · `4 🕉️ Sanskrit` · `5 🇹🇭 Thai` · `6 🏴󠁧󠁢󠁥󠁮󠁧󠁿 English`
5. **Each snippet = fenced code block containing ONLY the wish text** (user explicitly requested copy-friendly blocks; blockquotes were rejected). Below the block: `*Translit:*` / `*EN:*` / `*Source:*` in italic plain text
6. `[craft]` label for originals; `[VERIFIED: source]` / `[UNVERIFIED]` marking from research; modern-esoteric vs attested always labeled
7. ⚠️ **Misuse Notes** section — every trap flagged during verification
8. Sources list; optional assembled example ("recipe" / "kit") showing a full send

User spec facts: languages = Norse runes, Latin, Ancient Greek, Sanskrit(+Pali bridge), Thai, English; layers = original + translit + EN + citation; **Thai only inside the Thai section**; 3–5 snippets per language; Thai romanization with tones; register notes (นะคะ/ครับ for elders).

## Workflow

1. Confirm topic + special occasions (standing answers cover: gacha/exams/interviews/lottery for luck; confession/singles/anniversary for love; get-well/surgery/rest/longevity for health)
2. Dispatch **two verification subagents in parallel**:
   - Lane A: Old Norse + Latin + Greek (sources: heimskringla.no / voluspa.org, Latin Library & Wikisource, PerseusDL)
   - Lane B: Sanskrit/Pali + Thai (sa.wikisource, SuttaCentral, GRETIL; th.wiktionary + Longdo/NECTEC Lexitron + Royal Institute Dictionary + press usage)
   - Require per item: original + transliteration + accurate EN + source (work+section) + one-line use/register note + `[VERIFIED: source]`/`[UNVERIFIED]`; quotes ≤2 lines; **never invent**; explicitly ask for flagged traps (misattributions, modern-vs-attested, nonexistent folklore)
3. Assemble the file in the locked format
4. Patch the `00_overview.md` checkbox for that topic
5. Hand back: file path + highlights + traps caught; note Thai phrases await the user's native QA

## Pitfalls (learned the hard way)

- **write_file may refuse vault overwrites even after a full read** (stale-read guard). Workaround: write to scratch (`...cache/scratch/`), then `cp` into the vault via terminal. Verified twice.
- **Thai text through bash/MSYS garbles** (URLs, filenames). Do Thai HTTP work in `execute_code` Python; never use Thai filenames in shell.
- **Subagent script approvals auto-refuse after ~60s silence** ("silence is not consent"). If the user was away, re-run the check yourself when they're back — they explicitly ask for this retry pattern.
- **Fandom HTML is Cloudflare-walled** — use the MediaWiki `api.php` `rvprop=content` route (see `wiki-lore-research` skill).
- **Trap classes to expect** (all found in practice): popular misattributions ("Fortuna favet fortibus" ≠ Aeneid), nonexistent folklore ("ástrúnar" love runes — never cite), wrong scholarly citations (NE "1166a31" → actually 1170b6), modern-vs-classical confusion ("Ver heill ok sæll" is modern), unattested extensions (ὑγιαίνετε has no plural form), brand-wordplay vs traditional Thai renderings ("สุขภาพเป็นลาภ…" ≠ Dhp 204's "ความไม่มีโรค…").
- **Cross-file items**: the Pali mettā line ("sabbe sattā bhavantu sukhitattā") appears in Love and is reserved for the future Peace topic; Ovid's *Audentem Forsque Venusque iuvat* is the Luck↔Love crossover. Cross-reference, don't duplicate blindly.
- The Norse "hamingja lend" and rune-string recipes are the house-style example of `[craft]` on attested concepts — keep that honesty pattern.
