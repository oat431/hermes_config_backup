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
- `NN-Topic-Wishes.md` — e.g. `01-Luck-Wishes`, `02-Love-Wishes`, `03-Health-Wishes`; shipped: 00–11 complete (ten type files + Format Library, 2026-11-05)
- Wikilinks hyphenated, never spaces: `[[01-Luck-Wishes]]`

## Locked file format (user-approved; do not drift)

1. Frontmatter (`Title`, `created`, `tags`) → header blockquote linking `[[00_overview]]` + sibling files
2. **Occasion tags** line (emoji tags: 🎰 gacha, 🏥 surgery, 💍 anniversary, etc.)
3. **Quick-Pick Map** table: occasion → first pick → why
4. **Numbered language sections ×6:** `1 ᚠ Viking Runes (Old Norse)` · `2 🦅 Latin` · `3 🏛️ Ancient Greek` · `4 🕉️ Sanskrit` · `5 🇹🇭 Thai` · `6 🏴󠁧󠁢󠁥󠁮󠁧󠁿 English` (user-approved 2026-11-03: slot 1 may read `1 ᚠ Old Norse: words & lore` when no rune material fits the topic, as in 07/08; strictly-labeled `Modern rune flavor [modern esoteric]` boxes are approved flavor; rune-poem items are glyph-dressed with their rune)
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
   - **Put an explicit time budget in every brief**: "Wrap up within ~35–40 minutes of work; anything unchecked by then gets marked `[UNVERIFIED — incomplete]` and you return the report anyway." Long-source topics (dictionary HTML, Perseus retries) can otherwise run 80+ minutes — and the batch only delivers when BOTH lanes finish, so one slow lane holds the whole batch hostage (05-Protection: lane 1 ran 81 min while lane 2 finished in 28).
3. Assemble the file in the locked format
4. Patch the `00_overview.md` checkbox for that topic
5. Hand back: file path + highlights + traps caught; note Thai phrases await the user's native QA

## Pitfalls (learned the hard way)

- **write_file may refuse vault overwrites even after a full read** (stale-read guard). Workaround: write to scratch (`...cache/scratch/`), then `cp` into the vault via terminal. Verified twice.
- **Overview/parent links must be path-qualified — `[[wishes/00_overview]]`, never bare `[[00_overview]]`** (15 files share that name vault-wide; bare links go ambiguous). Use in new files; fix on sight in old ones.
- **Thai text through bash/MSYS garbles** (URLs, filenames). Do Thai HTTP work in `execute_code` Python; never use Thai filenames in shell.
- **Subagent script approvals auto-refuse after ~60s silence** ("silence is not consent"). If the user was away, re-run the check yourself when they're back — they explicitly ask for this retry pattern.
- **A long-running lane is not a stuck lane**: before panicking, check `delegate_task(action='list')` + the live transcript's last lines (read_file; files at `cache/delegation/live/<deleg_id>/task-N.log`) for a recent timestamp. If it's alive but grinding, **steer** it to wrap up ("finish current check, mark anything incomplete, deliver the report NOW") rather than waiting or stopping it.
- **Fandom HTML is Cloudflare-walled** — use the MediaWiki `api.php` `rvprop=content` route (see `wiki-lore-research` skill).
- **Trap classes to expect** (all found in practice): popular misattributions ("Fortuna favet fortibus" ≠ Aeneid), nonexistent folklore ("ástrúnar" love runes — never cite), wrong scholarly citations (NE "1166a31" → actually 1170b6), modern-vs-classical confusion ("Ver heill ok sæll" is modern), unattested extensions (ὑγιαίνετε has no plural form), brand-wordplay vs traditional Thai renderings ("สุขภาพเป็นลาภ…" ≠ Dhp 204's "ความไม่มีโรค…"); newer catches: "Ārambhatha nikkhamatha…" ≠ Dhp 382 (it is Thag 3.13), สุขสันติ์ is not a Thai word (→ สุขสันต์), Pindar's τηλαυγές line = Ol. 6.3–4 (not a fragment), "ves þú heill" unattested (→ ves heill / ver þú heill); 07 catches: 'सर्वे भवन्तु सुखिनः' ≠ Upaniṣad (Purāṇic/medieval variants), 'Pax vobiscum' is liturgical (Vulgate: 'Pax vobis'), 'τὰ μὲν προτετύχθαι…' = Il. 19.65–66 not 24.522, no Hávamál 'patience' stanza exists; 08 catches: the birthday poem is Statius Silvae 2.7 (not 4.5, and posthumous), 'compos voti' is dictionary-form (corpus: 'voti compotem', Suet. Cal. 13), 'gate of horn greeting' is craft (sources are descriptive), no classical birthday-wish line exists; 09 catches: 'Vesper adest…' = Catullus 62 (not 61), 'jīvema śaradaḥ śatam' = RV 7.66.16 (not 1.89.9), the Œþel/Beorc rune poems are Anglo-Saxon not Old Norse, saptapadī mantras = Gṛhya-Sūtra not RV 10.85, DN 31 has no 'six ways of cherishing'; 10 catches: Catullus 101 'ave atque vale' is a funeral epicedium (never a travel farewell), 'Ubi bene ibi patria' is a later reshaping of Cicero's 'Patria est, ubicumque est bene', 'Navigare necesse est' is Greek (Plutarch Pomp. 50) with the Latin later, only RV 1.89.6 is the svasti verse, 'svasti prāpta'/'kṣemaṁ gaccha' unattested.
- **Cross-file items**: the Pali mettā line ("sabbe sattā bhavantu sukhitattā") appears in Love and is reserved for the future Peace topic; Ovid's *Audentem Forsque Venusque iuvat* is the Luck↔Love crossover. Cross-reference, don't duplicate blindly.
- The Norse "hamingja lend" and rune-string recipes are the house-style example of `[craft]` on attested concepts — keep that honesty pattern.
