#!/usr/bin/env python3
"""Render an emdash_apply.py plan in memory and flag lines whose punctuation would read wrong.

    python preview_plan.py <root> <plan.json> [--all]

Why this exists: the per-dash token chooser sees only the text between the previous dash
and the current one, so it cannot know that the line already carries a colon, that a second
dash is closing an aside, or that the segment opens a subordinate clause. Reading the
finished line is the only reliable check, and on a 600-line plan that is expensive. This
prints just the suspects so they can be fixed with per-line overrides before writing.

Exit 1 when anything is flagged (use it as a gate before the applier), 0 otherwise.
`--all` also prints clean multi-dash lines, which is where a line-wide rule misfires.

The preview is for FLAGGING. The applier is authoritative for the final text: P and SP are
approximated here (period + capitalise) because a preview needs the shape, not the bytes.
"""
import json
import re
import sys
from pathlib import Path

G = "\u2014"
TOK = {":": ": ", ",": ", ", ";": "; ", ".": ". ", "(": " (", "),": ") ", "N/A": " N/A "}

FLAGS = [
    (r":\s+(and|but|so|yet|because|which|who|while|whereas)\b", "colon+conjunction"),
    (r"::", "double colon"),
    (r",,", "double comma"),
    (r"\s[,.;](?=\s|$)", "space before punctuation"),
    (r"[?!.]\s+[a-z]", "lowercase after sentence end"),
]


def cap(s):
    return s[:1].upper() + s[1:] if s else s


def render(line, tokens):
    parts = line.split(G)
    out = parts[0]
    for i, tok in enumerate(tokens):
        nxt = parts[i + 1]
        if tok == "KEEP":          # glyph under discussion: leave it and the rest alone
            out += G + nxt
            continue
        out = out.rstrip()
        nxt = nxt.lstrip()
        if tok == "BOLD":
            out += ": " + nxt
        elif tok in ("P", "SP"):
            out += ". " + cap(nxt)
        elif tok in TOK:
            out += TOK[tok] + nxt
        else:
            out += G + nxt          # unknown token: keep the glyph so the flag surfaces
    return out


def read(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    root, plan_path = Path(argv[1]), Path(argv[2])
    show_all = "--all" in argv
    plan = json.loads(read(plan_path))
    flagged = total = 0
    for rel, spec in plan.items():
        path = root / rel
        if not path.exists():
            print(f"MISSING FILE {rel}")
            flagged += 1
            continue
        lines = read(path).replace("\r\n", "\n").split("\n")
        for key in sorted(spec, key=int):
            n = int(key)
            old = lines[n - 1]
            if old.count(G) != len(spec[key]):
                print(f"COUNT MISMATCH {rel}:{n}  dashes={old.count(G)} tokens={len(spec[key])}")
                flagged += 1
                continue
            total += 1
            new = render(old, spec[key])
            hits = [label for pat, label in FLAGS
                    if len(re.findall(pat, new)) > len(re.findall(pat, old))]
            if new.count(":") >= 2 and old.count(":") == 0 and not new.lstrip().startswith("|"):
                hits.append("two colons")
            if hits:
                flagged += 1
                print(f"\n[{', '.join(hits)}] {rel}:{n}")
                print(f"  O: {old.strip()[:190]}")
                print(f"  N: {new.strip()[:190]}")
            elif show_all and len(spec[key]) >= 2:
                print(f"\n[ok] {rel}:{n}")
                print(f"  N: {new.strip()[:190]}")
    print(f"\n{flagged} flagged of {total} planned lines")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
