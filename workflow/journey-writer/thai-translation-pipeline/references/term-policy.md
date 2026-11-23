# Term policy for English → Thai translation

Lock this in Step 2 and paste the ruling into every child's context. A term list that says "concepts stay English" is not executable: each translator decides for itself which nouns are concepts, and a 21-file set comes back split.

## Tier A — the author's coinages stay English (Latin script)

Translating these invents terminology the author never used, and a coined Thai form will not match how readers met the idea elsewhere.

| Term | Note |
| ----- | ---- |
| `imagined order` | the book's central construct; no settled Thai form |
| `luxury trap` | author's coinage |
| `fictive language` | coined contrast with ordinary language |
| `Cognitive Revolution` / `Agricultural Revolution` / `Scientific Revolution` | named periodisations; the general noun `การปฏิวัติ` stays Thai around them |
| `full script` / `partial script` | technical distinction, not the ordinary word for writing |
| `inter-subjective` | philosophical term |
| `wheat's-eye view` | author's metaphor |
| `Homo sapiens`, `Sapiens`, `Neanderthal`, `Denisovan`, `DNA` | proper names and units; keep Latin italics on species names |

Rule of thumb: if the term does argumentative work in the book and Thai has no settled equivalent, leave it English and let Thai grammar run around it.

## Tier B — settled domain nouns take Thai

These are ordinary nouns Thai already owns. Leaving them in Latin script is the translation artifact this pipeline exists to avoid, and it invites drift because different translators make different calls.

| English | Thai |
| ------- | ---- |
| science | วิทยาศาสตร์ |
| empire | จักรวรรดิ |
| capitalism | ทุนนิยม |
| religion | ศาสนา |
| money | เงิน |
| industry | อุตสาหกรรม |
| patriarchy | ปิตาธิปไตย |

Rule of thumb: would a Thai newspaper use the Thai word without explanation? Then it is Tier B.

## The boundary test

1. Does Thai have this word in ordinary use? Yes → Tier B.
2. If no, is the term the author's own construct, doing argumentative work? Yes → Tier A, English, no coinage.
3. Neither: keep whatever the source uses, consistently, and do not introduce a third rendering.

Never coin a Thai term for Tier A. Never leave a Tier B noun in Latin script.

## Where the rule does not reach

- **Headings, H1 titles, wikilink labels** carry locked Thai titles. A Thai heading over English body terms is correct, not drift. Do not "fix" it.
- **English blockquotes** in the quotes section stay byte-identical to the source, page references included.
- **Proper names of empires** may keep the source form or take Thai; pick one per project and stay there.

## Drift matrix

Run this before the audit wave, and again after it. One row per file, one column per term bucket.

```python
import pathlib, re

terms = {
    "imagined order": "imagined order",
    "luxury trap": "luxury trap",
    "science EN": "science", "science TH": "วิทยาศาสตร์",
    "empire EN": "empire", "empire TH": "จักรวรรดิ",
    "capitalism EN": "capitalism", "capitalism TH": "ทุนนิยม",
}

for p in sorted(pathlib.Path(TH_DIR).glob("*.md")):
    t = p.read_text(encoding="utf-8")
    counts = {k: len(re.findall(re.escape(v), t)) for k, v in terms.items()}
    if any(counts.values()):
        print(f"{p.name}: {counts}")
```

Two rules for reading it:

- **Plain substring, never `\b`.** Thai letters are word characters, so a Latin term next to Thai text has no word boundary; `\bempire\b` reads zero on a page full of `empire`.
- **A file showing both columns of one term is a defect**, unless every occurrence of one side is in a heading, link label, or English blockquote. Read those exceptions rather than trusting the count.

## Per-project glossary (fill before dispatch)

| Term | Tier | Locked rendering | First-mention gloss |
| ---- | ---- | ---------------- | ------------------- |
| | | | |
