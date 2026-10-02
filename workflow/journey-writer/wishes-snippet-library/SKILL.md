---
name: wishes-snippet-library
version: 1.0.0
author: journey-writer curator
license: MIT
description: "Use when writing wishes snippet files in oralita_md."
metadata:
  hermes:
    tags: [writing, wishes, folklore, obsidian]
    triggers:
      - wish snippet
      - luck wishes
      - best wishes library
      - gacha wish
      - rune wish
      - blessings file
      - types of wishes
      - love wishes
      - health wishes
---

# Wishes Snippet Library

## When to Use

- Writing or extending any `NN-<Type>-Wishes.md` file under the vault's `wishes/` folder
- Crafting ritual-style wish snippets (runes, charms, ancient-language blessings) for any occasion
- Verifying folklore phrases across languages for copy-paste use

Build the `F:\obsidian_note\oralita_md\wishes\` snippet library — short, copy-pasteable *ritual* wishes (distinct from social occasion notes, which live in the vault's `[[04-Wishing-Note-Guide]]` and `oralita_md/templates/writing/wishing.md`). Read `wishes/00_overview.md` first: it carries the taxonomy (10 wish types), roadmap of numbered files, craft rules, and the gacha origin story.

## User-confirmed format (applies to every type file)

- **Six languages:** Viking Rune (Old Norse + Elder Futhark), Latin, Ancient Greek, Thai, English, Sanskrit. Other ancient languages may appear as bonus quotes (e.g. Old English/Beowulf).
- **Every snippet = 4 layers** — original script + transliteration + English + source citation (work/section or "traditional proverb") — **rendered as:** a fenced code block containing ONLY the paste-ready wish text, with all other layers BELOW it as italic plain text (`*Translit:* … · *EN:* …`; `*Source:* …`). User-corrected twice: blockquotes rejected (annoying to copy), then meta-lines inside blocks rejected too — the copy button must yield exactly what gets pasted into chat. English/`[craft]` snippets carry their full text inside the block.
- **3–4 snippets per language**, curated — no padding.
- **Thai script only in the Thai section**; ancient-language sections get EN glosses, not TH.
- **Occasions per type file:** gacha pulls, exams/tests, job interviews, everyday luck, lottery/risks (for the Luck file; adapt the occasion set per type, keep gacha where chance applies).
- Each file structure: parent links · occasion tags legend · Quick-Pick Map table (occasion → first pick → why) · snippets by language · a reproducible recipe where the topic supports one (e.g. the 5-step Viking Rune Wish) · ⚠️ misuse warnings · Sources with verification provenance.

## Procedure

1. Read `wishes/00_overview.md` and the existing `04-Wishing-Note-Guide` — never duplicate the social-wish craft rules; link them.
2. **Verify every phrase against real sources before it enters the file** — the user copy-pastes these to friends; an invented Latin line or wrong rune meaning is a real embarrassment. Dispatch **2 parallel verification subagents, languages split ~3+3** (e.g. Norse/Latin/Greek | Sanskrit/Thai), each returning per item: original + transliteration + EN + source (work+line) + register/use note + [VERIFIED: source] / [UNVERIFIED], kept short (≤2 chat lines) and never invented. Full recipe, tested source endpoints, post-processing rules (exclude unverifiable items, label modern-vs-attested, never fabricate transliterations), and the caught-traps catalog: `references/phrase-verification.md`.
3. Register matters: screen out wrong-flavor quotes (e.g. funeral/death-register lines from epic poetry are not luck wishes even if famous — a death-preparation verse was rejected for exactly this).
4. Cite folklore/game sources for the ritual context (gacha superstition culture is documented player folklore — lucky chairs, postures, pull rituals).
5. Update the roadmap checkboxes in `00_overview.md` when a file lands.

## Pitfalls

- **Respect rule:** borrow symbols, never parody living traditions — Sak Yant, mantras, novenas, and Pali blessings carry real religious weight; mark them as prayers where applicable.
- **Never promise outcomes** in snippet wording ("may the runes favor you", not "this gets you the 5-star").
- **write_file stale-guard on vault overwrites:** a rewrite of an existing vault file can be refused ("partial view") even after a full `read_file` — don't loop re-reading. Write the complete new content to a NEW scratch filename, `cp` it over the vault path via terminal, then verify (`wc -c`, count of fence lines). If the scratch file itself is refused, just use a fresh filename there too.
- Fandom pages are Cloudflare-walled for HTML fetch; use the MediaWiki API path (see wiki-lore-research skill) when a fandom quote is needed.
- **Thai text dies in this shell:** MSYS bash mangles Thai characters in URL params and filenames (mojibake, empty results, "No such file"). Run Thai lookups through Python (`execute_code` + `urllib` with explicit encoding) and keep any shell-loop filenames ASCII (`ld1.html`, never `ld<Thai>.html`) — endpoints in `references/phrase-verification.md`.
- **Scripted verification checks wait on user approval:** subagent `execute_code` checks auto-refuse after ~60s of user silence ("silence is not consent"). This is not a method failure — the lane marks the item pending and finishes the rest; when the user returns (or asks to retry), re-run the blocked check from the parent session and it passes.
- Vault convention: numbered files `NN-Name.md`, hyphenated wikilinks only (never spaces).
