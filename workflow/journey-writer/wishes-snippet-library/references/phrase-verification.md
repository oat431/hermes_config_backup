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
- **"Ārambhatha nikkhamatha…" ≠ Dhp 382** — it is *Theragāthā 3.13* (PTS Th 256); SC reads ārambhatha/nikkamatha, PTS ārabhatha/nikkhamatha.
- **Thai สุขสันติ์ is not a dictionary spelling** — use สุขสันต์ (สุขสันติ์ occurs only in names).
- **Sanskritized नूतनवर्ष is effectively unused** — prefer नववर्ष (118 vs 0 full-text hits on hi.wikipedia).
- **Pindar "ἀρχομένου δ' ἔργου…" = *Olympian* 6.3–4** — any "fragment" citation is a miscitation.
- **"ves þú heill" is unattested** — use "ves heill" (FJ) / "ver þú heill" (Neckel–Kuhn), Hymiskviða 11.
- **Roman formula split**: the long "quod bonum faustum felix fortunatumque sit" is epigraphic (Arval Acts, Q.B.F.F.S.); Livy = "quod bonum, faustum felixque sit" — don't cross-attribute.
- **"bonis auspiciis" is not the classical set phrase** — use "bonis avibus" (Ovid *Met.* 15.640; *Fasti* 1.513).
- **Dagaz "breakthrough" / Berkanan "growth" = modern esoteric** — the poems say Day = the Lord's messenger; Beorc = fruitless yet fair (Dickins even glosses 'poplar').
- **"τὰ μὲν προτετύχθαι ἐάσομεν…" = Iliad 19.65–66** (also 18.112–113; 16.60 shorter) — NOT 24.522–524; the Priam consolation has different wording ("ἄλγεα δ' ἔμπης…").
- **"Pax vobiscum" is liturgical, not biblical** — the Clementine Vulgate reads "Pax vobis" (Luke 24:36; John 20:19); "pax et bonum" provenance unverified.
- **"सर्वे भवन्तु सुखिनः…" is not in any Upaniṣad** (the "Bṛhadāraṇyaka 1.4.14" citation is false) — real variants: Garuḍa Purāṇa 35.51, Bhaviṣya Purāṇa 3.2.35.14, Uvaṭa colophon; popular 4-line form is modern.
- **"lokāḥ samastāḥ sukhino bhavantu" is not Vedic/Upaniṣadic** — medieval mangala inscription (Sangama dynasty) + modern yoga closing chant.
- **Mettā precision**: root reads "sabbasattā bhavantu sukhitattā" (Khp 9/Sn 1.8); the "averā… sukhī attānaṁ pariharantu" formula is AN 10.176/MN 41 (long ī), not the Mettā Sutta; "sabbe sattā dukkhā pamuccantu" has NO canonical locus (modern karuṇā appendage).
- **Aeneid numbering**: "forsan et haec…" = 1.203; "durate…" = 1.207 (speech runs 1.198–207); Seneca "curae leves…" = Phaedra 607.
- **No Hávamál "patience / fair-weather-after-foul" stanza exists** — only st. 74 (weather changes fast, wry register).
- **Statius' birthday poem = *Silvae* 2.7** (not 4.5) — and it is posthumous (dead addressee, commissioned by his widow); no attested classical birthday-wish line exists (birthday POEMS ≠ greetings).
- **"compos voti" is dictionary Latin** — corpus form: Suetonius' accusative "voti compotem" (*Cal.* 13).
- **"May it come through the gate of horn" is craft** — the attested texts are descriptive (Od. 19.562–567; Verg. *Aen.* 6.893–898); and Aeneas exits via the ivory gate (6.898).
- **Baldrs draumar is not a Codex Regius poem** (AM 748 I a 4to only) — and it is death-dream/necromancy register, not a generic dream poem.
- **"Idaṃ me puññaṃ āsavakkhayāvahaṃ hotu" is a traditional chanting formula** (no sutta locus); Khp 7 reads "Idaṃ VO ñātīnaṃ hotu" — the *me* form is Petavatthu 27.
- **No "four kinds of dreams" sutta** — AN 5.196 = five great dreams of the Bodhisatta; the sixteen dreams are King Pasenadi's (Ja 77).
- **Thai ฝัน is native Tai** (*hwan), not from Pali supina/Sanskrit svapna; जन्मदिन की शुभकामनाएँ / मुबारक हो are modern Hindi (मुबारक Arabic via Urdu).
- **"Vesper adest, iuvenes…" = Catullus 62.1–2**, not 61 (and possibly not Catullus); 61's refrain is "o Hymenaee Hymen, o Hymen Hymenaee".
- **"jīvema śaradaḥ śatam" = RV 7.66.16**, not 1.89.9 (that verse is "where sons are with fathers"); the singular birthday form is a modern adaptation.
- **The Œþel/Beorc rune poems are Old English (Anglo-Saxon)**, not Old Norse; the ON younger-futhark poems have no óðal rune (ON material = óðal vocabulary + Icelandic Maðr line).
- **The Hymen/Hymenaeus cry is not in Thesmophoriazusae** — attested in Aristophanes *Peace* 1331ff and *Birds* 1731ff.
- **Sappho fr. 112 ≠ fr. 44** (fr. 44 = Hector–Andromache narrative); the epithalamia are frs. 112/115/116/117 V.
- **Saptapadī mantras are Gṛhya-Sūtra liturgy, not RV 10.85**; the **maṅgalasūtra is not Vedic** (Gṛhya Sūtras silent; medieval Smārta/regional, tāḷi).
- **"पुत्रपौत्राभिवृद्धिरस्तु" is not the pūṇyāhavācana wording** — "putra-pautra-samṛddhir astu" / "-saṃpad-astu" are (they travel right after धनधान्यसमृद्धिरस्तु).
- **DN 31 has no "six ways of cherishing"** — the duties are fivefold, set in six directions.
- **Catullus 101 "ave atque vale" = funeral epicedium** ("ad inferias") — never a travel farewell, despite line 1's travel language.
- **"Ubi bene, ibi patria" is not Cicero verbatim** — *Tusc.* 5.108 has "Patria est, ubicumque est bene" (Teucer/Pacuvius); the familiar form is a later proverb.
- **"Navigare necesse est" is Greek in origin** — Plutarch, *Pomp.* 50 (Πλεῖν ἀνάγκη, ζῆν οὐκ ἀνάγκη); the Latin wording is a later rendering, not classical Latin.
- **RV 1.89: only v.6 is the svasti verse** (v.7 = Maruts; v.8 = bhadraṁ karṇebhiḥ). "svasti prāpta" and "kṣemaṁ gaccha" are unattested; the epic imperative is **svasti prāpṇuhi** (MBh 3.37.24), spoken by Draupadī, not Kuntī.
- **DN 32 Āṭānāṭiya contains no travel wording** — the traveller application is later paritta practice; avihiṁsā = "non-harming," rendered loosely as "safety".
- **Thai ไปดีนะ** doubles as a death/breakup farewell — not a cheerful send-off; keep ใน in ชีวิตใหม่ในต่างแดน.

## Provenance footer

Close each type file's Sources section with the verification note (e.g. "every attested item cross-checked against primary texts by verification subagents") — it tells the user which half of the file is folklore and which is craft.
