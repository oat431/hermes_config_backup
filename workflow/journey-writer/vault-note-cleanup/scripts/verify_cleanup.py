"""Gate a vault cleanup pass against its pre-edit baseline.

usage: python verify_cleanup.py <root_dir> <baseline_dir> [--expect-residue N]

Gates, per markdown file:
  1. line-count parity with the baseline
  2. content-word equality, alignment-aware (difflib), init/blank insertions allowed
  3. EOL style unchanged (LF stays LF, CRLF stays CRLF, mixed stays mixed)
  4. no punctuation defects introduced (compare defect SETS, never absolute text)
  5. every mermaid block has exactly one %%{init line, zero unterminated fences

Exits 0 when clean, 1 when a gate fails. All reads use newline="" so verification never
rewrites line endings as a side effect.
"""
import difflib
import os
import re
import sys

EM = chr(0x2014)
CR = chr(13)
LF = chr(10)
CRLF = CR + LF

WORD = re.compile(r"[\w\u0E00-\u0E7F]+")
DEFECTS = [
    (r"::", "double colon"),
    (r",,", "double comma"),
    (r",\s*\.", "comma-period"),
    (r";\s*\.", "semicolon-period"),
    (r"\?\s*\.", "period after ?"),
    (r"\s[,.;]", "space before punct"),
    (r":[A-Za-z]", "colon-no-space"),
    (r",[A-Za-z]", "comma-no-space"),
]


def read(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


def words(line):
    return [w for w in WORD.findall(line.lower()) if w not in ("n", "a")]


def eol_style(text):
    crlf, nl = text.count(CRLF), text.count(LF)
    if nl == 0:
        return "empty"
    if crlf == nl:
        return "crlf"
    return "lf" if crlf == 0 else "mixed"


def defects(text):
    out = set()
    lines = text.split(LF)
    for pat, label in DEFECTS:
        for m in re.finditer(pat, text):
            idx = text[:m.start()].count(LF)
            out.add((label, lines[idx].strip()[:100]))
    return out


def mermaid_blocks(text):
    """Return (block_count, init_counts, unterminated_flag)."""
    counts = []
    cur = None
    for line in text.split(LF):
        m = re.match(r"^\s*(`{3,})(.*)$", line)
        if cur is None:
            if m:
                cur = {"len": len(m.group(1)), "tag": m.group(2).strip(), "init": 0}
            continue
        if m and len(m.group(1)) >= cur["len"] and m.group(2).strip() == "":
            if cur["tag"].startswith("mermaid"):
                counts.append(cur["init"])
            cur = None
        elif line.strip().startswith("%%{init"):
            cur["init"] += 1
    return len(counts), counts, cur is not None


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    root, base = argv[1], argv[2]
    expect = None
    if "--expect-residue" in argv:
        expect = int(argv[argv.index("--expect-residue") + 1])

    fails = []
    em_total = 0
    em_lines = []
    changed = 0
    blocks = 0

    for dirpath, _dirnames, filenames in os.walk(root):
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), root)
            new_path = os.path.join(root, rel)
            old_path = os.path.join(base, rel)
            if not os.path.exists(old_path):
                fails.append((rel, "missing in baseline"))
                continue
            old, new = read(old_path), read(new_path)

            for i, line in enumerate(new.split(LF), 1):
                if EM in line:
                    em_total += line.count(EM)
                    em_lines.append((rel, i, line.strip()[:90]))

            if eol_style(old) != eol_style(new):
                fails.append((rel, "EOL style " + eol_style(old) + " -> " + eol_style(new)))

            count, counts, unterm = mermaid_blocks(new)
            blocks += count
            if unterm:
                fails.append((rel, "unterminated fence"))
            for idx, n in enumerate(counts, 1):
                if n != 1:
                    fails.append((rel, "mermaid block " + str(idx) + " has " + str(n) + " inits"))

            if old == new:
                continue
            changed += 1
            a, b = old.split(LF), new.split(LF)
            if len(a) != len(b):
                fails.append((rel, "line count " + str(len(a)) + " -> " + str(len(b))))

            for d in sorted(defects(new) - defects(old)):
                fails.append((rel, "new defect " + d[0] + ": " + d[1]))

            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal":
                    continue
                if tag in ("insert", "delete"):
                    ins = b[j1:j2] if tag == "insert" else a[i1:i2]
                    if all(x.strip().startswith("%%{init") or not x.strip() for x in ins):
                        continue
                    fails.append((rel, "unexpected " + tag + ": " + repr(ins[:1])))
                    continue
                for x, y in zip(a[i1:i2], b[j1:j2]):
                    if words(x) != words(y):
                        fails.append((rel, "word drift: " + repr(x[:60]) + " -> " + repr(y[:60])))

    print("files changed: %d | mermaid blocks: %d | em-dashes: %d" % (changed, blocks, em_total))
    for rel, line, text in em_lines:
        print("  residue %s:%d  %s" % (rel, line, text))
    if expect is not None and em_total != expect:
        fails.append(("<folder>", "em residue %d, expected %d" % (em_total, expect)))
    for rel, msg in fails[:40]:
        print("FAIL %s: %s" % (rel, msg))
    if len(fails) > 40:
        print("... %d more failures" % (len(fails) - 40))
    print("RESULT: PASS" if not fails else "RESULT: FAIL (%d)" % len(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
