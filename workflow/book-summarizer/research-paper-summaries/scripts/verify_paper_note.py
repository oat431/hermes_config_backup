#!/usr/bin/env python
"""Verify a staged paper study note against its source extract (safety net).

Usage:
    python verify_paper_note.py --note NOTE.md --source EXTRACT.md [--numbers "a,b,c"]
        [--quotes extra_quotes.txt] [--allow-links stem1,stem2] [--allow-numbers 2026]
        [--scan-all] [--ocr-tolerant]

Checks:
  1. Quotes: lines shaped  > [**Prefix:**] "<quote>" (p. N)  are checked against the
     source with whitespace/quote-glyph normalization, retrying with hyphenated
     line-breaks joined (PDF layers split words as "develop-\nment"). A quote that
     still fails is retried as a SPLIT quote (sentence split by a floating caption at
     a page break): both halves must occur in the source with only caption-like text
     between them. Extra quotes can be supplied one-per-line via --quotes.
     With --ocr-tolerant (scanned PDFs), ligatures map to ASCII and quotes/numbers
     are also compared with ALL whitespace and ASCII hyphens stripped, which
     survives merged-word text layers ("Eventhoughwehave").
  2. Numbers: every value in --numbers must appear in the source, trying comma and
     hyphen/space variants. With --scan-all, every numeric token in the note is
     checked the same way (--allow-numbers skips known meta values like the date).
  3. Style: em-dash count must be 0; fences balanced; frontmatter has
     title/tags/created/source; with --allow-links, wikilinks must be a subset of the
     allow-list; prints the word count.

Exit code 0 only when all checks pass. A MISS means verify that item manually (the PDF
layer can interleave captions); never edit the source or the quote just to make a check
pass.
"""
import argparse
import re
import sys

EM_DASH = "\u2014"
QUOTE_LINE = re.compile(r'>\s*(?:\*\*[^*\n]+\*\*:?\s*)?"(.+?)"\s*\((?:p|pp)\.\s*[0-9][0-9\u2013\u2014\-]*\)')
NUM_TOKEN = re.compile(r"\d[\d,\.]*[TBMK]?")


_LIGATURES = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl"}


def norm(s: str) -> str:
    for lig, plain in _LIGATURES.items():
        s = s.replace(lig, plain)
    s = (s.replace("\u2019", "'").replace("\u2018", "'")
          .replace("\u201c", '"').replace("\u201d", '"'))
    return re.sub(r"\s+", " ", s).strip()


def nospace(s: str) -> str:
    """OCR layers: merged words and hyphen breaks. Drop ALL whitespace/ASCII hyphens."""
    return re.sub(r"[\s\-]+", "", norm(s))


def source_variants(raw: str):
    base = norm(raw)
    joined = base.replace("- ", "")               # hyphenated line-break join
    dense = re.sub(r"(?<=\d) (?=\d)", "", base)   # "50 000" -> "50000"
    return [base, joined, dense, dense.replace("- ", "")]


def number_variants(value: str):
    v = value.strip().strip(".,;: ")
    out = {value.strip(), v, v.replace(",", ""), v.replace("-", "- "), v.replace("-", "")}
    return [x for x in out if x]


def split_check(quote: str, source: str):
    """Try to verify a quote whose halves are separated by interleaved caption text."""
    words = quote.split(" ")
    for i in range(4, len(words) - 3):
        head, tail = " ".join(words[:i]), " ".join(words[i:])
        j1 = source.find(head)
        if j1 < 0:
            continue
        j2 = source.find(tail, j1 + len(head))
        if j2 < 0:
            continue
        between = source[j1 + len(head):j2].strip()
        if len(between) < 1500 and re.search(r"\b(Figure|Table)\b", between):
            return head, tail, between
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--note", required=True, help="staged note path")
    ap.add_argument("--source", required=True,
                    help="source extract path (with [PDF p. N] markers)")
    ap.add_argument("--numbers", default="",
                    help="comma-separated numbers that must appear in the source")
    ap.add_argument("--quotes", default="", help="extra expected quotes, one per line")
    ap.add_argument("--allow-links", default="",
                    help="comma list of allowed wikilink stems (check runs only when given)")
    ap.add_argument("--allow-numbers", default="",
                    help="tokens to skip in --scan-all (e.g. the created date)")
    ap.add_argument("--scan-all", action="store_true",
                    help="check every numeric token in the note, not just --numbers")
    ap.add_argument("--ocr-tolerant", action="store_true",
                    help="scanned PDFs: also compare with ligatures mapped and ALL "
                         "whitespace/ASCII-hyphens stripped (survives merged words)")
    args = ap.parse_args()

    note = open(args.note, encoding="utf-8").read()
    raw = open(args.source, encoding="utf-8").read()
    sources = source_variants(raw)
    ocr_src = nospace(raw) if args.ocr_tolerant else None

    ok = True
    style_ok = True

    print("=== QUOTES (verbatim; hyphen-joined retry; split-quote aware) ===")
    quotes = QUOTE_LINE.findall(note)
    if args.quotes:
        quotes += [l.strip() for l in open(args.quotes, encoding="utf-8") if l.strip()]
    if not quotes:
        print("WARN: no quote lines found; check the quotes section")
    for q in quotes:
        nq = norm(q)
        if any(nq in s for s in sources) or (ocr_src and nospace(q) in ocr_src):
            print("OK       " + nq[:78])
            continue
        split = None
        for s in sources:
            split = split_check(nq, s)
            if split:
                break
        if split:
            print("OK-SPLIT " + nq[:60] + " ...  (inspect the between-text)")
            print("         between: " + split[2][:130])
            continue
        ok = False
        print("MISS     " + nq[:78])

    print()
    print("=== NUMBERS ===")
    values = [n.strip() for n in args.numbers.split(",") if n.strip()]
    if args.scan_all:
        allow = {t.strip() for t in args.allow_numbers.split(",") if t.strip()}
        for tok in NUM_TOKEN.findall(note):
            base = tok.strip(".,;: ")
            if len(base) < 2 or base in allow or tok in allow:
                continue
            values.append(tok)
    if not values:
        print("(none)")
    for value in sorted(set(values)):
        hit = any(v in s for s in sources for v in number_variants(value))
        if not hit and ocr_src:
            hit = any(nospace(v) in ocr_src for v in number_variants(value))
        if not hit:
            ok = False
        print(("OK       " if hit else "MISS     ") + value)

    print()
    print("=== STYLE / STRUCTURE ===")
    em = note.count(EM_DASH)
    style_ok = style_ok and em == 0
    print("em-dash count (must be 0):", em)
    has_fm = note.startswith("---\n")
    fm_block = note.split("---")[1] if has_fm else ""
    keys_ok = all(k in fm_block for k in ("title:", "tags:", "created:", "source:"))
    style_ok = style_ok and has_fm and keys_ok
    print("frontmatter (title/tags/created/source):", has_fm and keys_ok)
    fences = note.count("```")
    style_ok = style_ok and fences % 2 == 0
    print("code fences balanced:", fences % 2 == 0, f"({fences} markers)")
    if args.allow_links:
        allowed = {t.strip() for t in args.allow_links.split(",") if t.strip()}
        links = set(re.findall(r"\[\[([^\]|#]+)\]\]", note))
        bad = sorted(links - allowed)
        style_ok = style_ok and not bad
        print("wikilinks:", sorted(links), ("UNEXPECTED: " + ", ".join(bad)) if bad else "(all allowed)")
    print("word count (approx):", len(note.split()))

    print()
    good = ok and style_ok
    print("RESULT:", "ALL CHECKS PASS" if good else "FAILURES PRESENT")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
