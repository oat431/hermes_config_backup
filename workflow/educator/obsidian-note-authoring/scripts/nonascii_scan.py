#!/usr/bin/env python3
"""Scan a markdown note: inventory non-ASCII chars and flag typographic chars to replace.

Usage: python nonascii_scan.py <note.md>

After a cleanup pass, expected leftovers are only emoji and legitimate script
(Thai glyphs must read as THAI CHARACTER ...; mixed Latin inside Thai words = mojibake).
Exit codes: 0 = clean, 1 = replaceable typographic chars still present, 2 = usage error.
"""
import sys
import unicodedata
from collections import Counter

if len(sys.argv) != 2:
    print("usage: python nonascii_scan.py <note.md>")
    sys.exit(2)

text = open(sys.argv[1], encoding="utf-8").read()

counts = Counter(ch for ch in text if ord(ch) > 127)
print("=== non-ASCII inventory ===")
for ch, n in counts.most_common():
    try:
        name = unicodedata.name(ch)
    except ValueError:
        name = "?"
    print(f"  {ch!r}  U+{ord(ch):04X}  x{n}  {name}")

bad = {
    "\u2014": "em-dash", "\u2013": "en-dash", "\u2026": "ellipsis",
    "\u2192": "arrow ->", "\u2190": "arrow <-", "\u00a7": "section sign",
    "\u2260": "not-equal", "\u201c": "curly quote", "\u201d": "curly quote",
    "\u2018": "curly quote", "\u2019": "curly quote",
}
found = [f"{name} x{text.count(ch)}" for ch, name in bad.items() if text.count(ch)]
print("bad chars to replace:", ", ".join(found) if found else "none")
sys.exit(1 if found else 0)
