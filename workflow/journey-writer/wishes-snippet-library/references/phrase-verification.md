# Phrase Verification — recipe for wishes snippet files

Every phrase in a wishes file is either source-attested or `[craft]` (original). This file is the verified workflow for the attested half.

## Dispatch pattern (2 parallel subagents)

Split languages ~3+3 across two subagents, e.g.:

- **Agent A:** Old Norse/runes + Latin + Ancient Greek
- **Agent B:** Sanskrit/Pali + Thai (+ any new language)

Task spec passed to each agent (this shape worked — keep it):

> For EACH item give: (1) original script text, (2) transliteration, (3) accurate EN translation, (4) source citation (work + line/section), (5) one-line register/use note, (6) mark `[VERIFIED: source]` or `[UNVERIFIED]`. Keep quotes ≤2 chat lines. Prefer primary texts. **Do not invent phrases** — if unverifiable, say so explicitly.

Also tell them which candidates to check per language (names, works, line refs) so they verify rather than browse.

## Tested source endpoints

| Language | Works | Notes |
|---|---|---|
| Ancient Greek | PerseusDL corpus on GitHub — raw files via curl (`github.com/PerseusDL/canonical-greekLit`, e.g. `tlg0012/tlg001.perseus-grc2` for Iliad, `tlg0033` for Pindar) | Scaife/Perseus Hopper for standard translations |
| Latin | The Latin Library (thelatinlibrary.com), Latin Wikisource for Cicero, Perseus for Vergil | quote-collector sites misattribute — always hit the corpus |
| Old Norse | heimskringla.no (ON texts, e.g. Hávamál), voluspa.org | Rune meanings: Wikipedia rune articles; rune poems are **medieval MSS** — label accordingly |
| Sanskrit / Pali | SuttaCentral (Pali canon, raw text OK), sa.wikisource; archive.org scans (Griffith 1892, Telang SBE 8) work when secondary sites block scripts (sacred-texts.com & wisdomlib Cloudflare scripts out) | GRETIL and Cologne MW API endpoints were flaky in practice — cross-check ≥2 concordant secondary sources instead |
| Thai | th.wiktionary API for spelling/meaning (`/w/api.php?action=query&prop=extracts&explaintext=1&titles=<word>&redirects=1`); Longdo mobile (`dict.longdo.com/mobile.php?search=…`, browser UA via Python → NECTEC Lexitron + Royal Institute Dictionary entries); press/social usage for naturalness | **Fetch via Python, not shell curl** (MSYS bash mangles Thai params). No classical corpus — naturalness is judged by the user (native speaker). **Always flag Thai lines as awaiting native-speaker sign-off.** |
| Fandom quotes | MediaWiki `api.php` → `action=query&prop=revisions&rvprop=content` | HTML is Cloudflare-walled; see wiki-lore-research skill |

## Post-processing rules (before anything enters the file)

1. **VERIFIED** → include with full citation in the `*Source:*` line.
2. **UNVERIFIED but grammatically sound & in modern liturgical use** → include ONLY with an explicit "traditional formula / no classical single-source attestation" label (or drop).
3. **No attestation found** → EXCLUDE. Report the exclusion in the hand-off message so the user knows it was considered.
4. **Hunt misattributions:** exact wording must match the primary corpus, not quote sites. When a trap is caught, name it in the file ("do not cite X as Y") so the user never repeats it, and add it to the Traps catalog below.
5. **Label modern vs attested:** rune meanings ("Algiz = protection" is modern esoteric; attested = elk), modern-language variants (Icelandic *til hamingju* ≠ Old Norse). Modern is fine as flavor — sold-as-ancient is not.
6. **Register screen:** reject wrong-flavor famous lines (funeral/death verses ≠ luck wishes, however beautiful). Living prayers (Gāyatrī, Sak Yant, mettā) get "use with respect" labels and are never used as casual charms.
7. **Keep quotes short** (≤2 chat lines) and paste-ready.
8. **Assemble strictly from verified layers — never fabricate a transliteration or translation the verifier didn't return.** Improvised phonetic guides look identical to verified data and ship as fabrication; if a translit is missing, omit the layer or give only agreed pronunciation hints (e.g. ON: ð = th as in "bathe").

## Caught traps (grow this list — check before trusting a popular phrase)

- "Fortuna favet fortibus" ≠ Aeneid — attested is *Audentis Fortuna iuvat* (Aen. 10.284).
- **"Ástrúnar" (Eddic love-runes) do not exist** — checked against the full Sigrdrífumál text; the real rune list is Sigrúnar, Ölrúnar, Bjargrúnar, Brimrúnar, Limrúnar, Málrúnar, Hugrúnar. Never cite "Eddic love runes".
- Aristotle, "the friend is another self" → cite *NE* **1170b6–7**, not the everywhere-copied "1166a31".
- ἀγάπη as a noun is post-classical (first citations LXX/NT); the "four Greek loves" trope is a later curation — don't sell it as one classical system.
- เนื้อคู่ is native Thai (เนื้อ+คู่) — do NOT claim it derives from Chinese 缘.
- Rune "love/protection" readings (ᚷ ᚹ ᛖ = partnership; ᛉ = protection) are modern esoteric; attested = gift/joy/horse/elk.
- kærleikr is 14th–15th c. religious prose, not a Viking-age word — label late if used.
- Modern-language cousins are not the originals: Icelandic *til hamingju* is modern, not Old Norse.

## Provenance footer

Close each type file's Sources section with the verification note (e.g. "every attested item cross-checked against primary texts by verification subagents") — it tells the user which half of the file is folklore and which is craft.
