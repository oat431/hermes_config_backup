#!/usr/bin/env python3
"""Validate narrative-book chapter notes against chapter extracts.

Checks per note: frontmatter, source line (chapter + PDF range), H1,
required section order, Memorable Quotes verbatim against the extract
(normalized), quote page attribution against [PDF p. N] markers, and
wikilinks restricted to the vault's own note stems.

Usage:
  python check_chapter_notes.py --vault "F:/vault/Book/Title" \
      --extracts "C:/temp/run/extracts" \
      --expect "C:/temp/run/expect.json" \
      [--skip "Title - Overview.md"]

expect.json maps filename -> [chapter_number, pdf_start, pdf_end]
(1-based inclusive), e.g.:
  {"01_An_Animal_of_No_Significance.md": [1, 11, 26], ...}
Extracts must be named chNN.txt (zero-padded chapter number).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata

SECTIONS = [
    "## Key Idea",
    "## The Argument",
    "## Key Concepts",
    "## Memorable Quotes",
    "## Connections",
    "## Takeaway",
]

SOURCE_RE = re.compile(
    r"Chapter (\d+).*?PDF pp\. (\d+)[\u2013-](\d+) \(printed pp\. unknown\)"
)
QUOTE_RE = re.compile(r"^> (.+?)\s*\(PDF p\. (\d+)\)\s*$", re.M)
MARKER_RE = re.compile(r"\[PDF p\. (\d+)\]")
LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    for a, b in [
        ("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'),
        ("\u201d", '"'), ("\u2013", "-"), ("\u2014", "-"),
    ]:
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--vault", required=True)
    ap.add_argument("--extracts", required=True)
    ap.add_argument("--expect", required=True, help="path to expect.json")
    ap.add_argument("--skip", default="", help="comma-separated filenames to skip")
    args = ap.parse_args()

    with open(args.expect, encoding="utf-8") as f:
        expect = json.load(f)
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}

    stems = {fn[:-3] for fn in os.listdir(args.vault) if fn.endswith(".md")}

    problems = []
    checked = 0
    for fn, (ch, p1, p2) in expect.items():
        if fn in skip:
            continue
        checked += 1
        path = os.path.join(args.vault, fn)
        if not os.path.exists(path):
            problems.append((fn, "missing file"))
            continue
        text = open(path, encoding="utf-8").read()

        if not re.match(r"^---\n(.*?)\n---\n", text, re.S):
            problems.append((fn, "frontmatter missing"))
            continue
        m = SOURCE_RE.search(text)
        if not m:
            problems.append((fn, "source line missing/malformed"))
        elif (int(m.group(1)), int(m.group(2)), int(m.group(3))) != (ch, p1, p2):
            problems.append((fn, f"source range wrong: {m.groups()}"))
        if not re.search(rf"^# {ch:02d}: ", text, re.M):
            problems.append((fn, "H1 missing/malformed"))
        pos = [text.find(s) for s in SECTIONS]
        if any(p < 0 for p in pos):
            problems.append((fn, "missing required section(s)"))
        elif pos != sorted(pos):
            problems.append((fn, "section order wrong"))

        quotes = QUOTE_RE.findall(text)
        if not 2 <= len(quotes) <= 4:
            problems.append((fn, f"quote count {len(quotes)} outside 2-4"))
        ext_path = os.path.join(args.extracts, f"ch{ch:02d}.txt")
        if os.path.exists(ext_path):
            extn = norm(open(ext_path, encoding="utf-8").read())
            for quote, page in quotes:
                qn = norm(quote).strip('"')
                idx = extn.find(qn)
                if idx < 0:
                    problems.append((fn, f"quote NOT verbatim (cited p.{page}): {qn[:70]}"))
                    continue
                marks = MARKER_RE.findall(extn[:idx])
                actual = int(marks[-1]) if marks else None
                if int(page) != actual:
                    problems.append((fn, f"quote page mismatch: cited {page}, near {actual}"))
        else:
            problems.append((fn, f"extract missing: {ext_path}"))

        bad = [l for l in LINK_RE.findall(text) if l not in stems]
        if bad:
            problems.append((fn, f"non-canonical links: {bad}"))
        print(f"OK  {fn} | quotes {len(quotes)}")

    print(f"\nchecked {checked} notes, {len(problems)} problems")
    for fn, msg in problems:
        print(f"FAIL {fn}: {msg}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
