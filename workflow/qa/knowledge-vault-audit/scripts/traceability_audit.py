#!/usr/bin/env python3
"""Traceability audit: baseline [[wikilinks]] -> content files, with normalization.

Extracts every [[wikilink]] from files under the baseline directory and resolves
each against actual content-file basenames using normalized matching. Prints:
  - totals (md files, baseline files, content files, links resolved/unresolved)
  - per-subject missing-link counts
  - unique missing targets per subject (the candidate gap list)
  - content-file counts per top-level folder

IMPORTANT: the "missing" list is a HYPOTHESIS, not a finding. Confirm each
candidate against the real folder contents (taxonomy drift produces false gaps).

Usage:
  python traceability_audit.py --root "F:/obsidian_note/general-knowledge" \
                               --baseline "body-of-knowledge"
"""

import argparse
import collections
import os
import re

LINK_RE = re.compile(r"\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]")
SKIP_DIRS = {".git", ".obsidian", "node_modules"}


def walk_md(base):
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.lower().endswith(".md"):
                out.append(os.path.join(dirpath, f))
    return out


def norm(s):
    """Normalize a link target / basename for tolerant matching."""
    s = s.strip().rstrip("\\").strip()
    s = re.sub(r"^\d{1,2}[_\-\s]+", "", s)  # strip leading numeric prefix
    s = s.replace("_", " ").replace("-", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def is_nav(target):
    t = target.strip()
    return ("overview" in t.lower()) or ("ภาพรวม" in t) or t.endswith("\\")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--baseline", default="body-of-knowledge")
    args = ap.parse_args()

    root = args.root.rstrip("/\\")
    bok_root = os.path.join(root, args.baseline)

    all_md = walk_md(root)
    bok_files = [p for p in all_md if os.path.normpath(p).startswith(os.path.normpath(bok_root) + os.sep)]
    content_files = [p for p in all_md if p not in bok_files]

    # index content files by normalized basename
    content_index = collections.defaultdict(list)
    for p in content_files:
        base = os.path.splitext(os.path.basename(p))[0]
        content_index[norm(base)].append(os.path.relpath(p, root))

    results = []
    for p in bok_files:
        with open(p, encoding="utf-8") as fh:
            text = fh.read()
        rel = os.path.relpath(p, root)
        for m in LINK_RE.finditer(text):
            results.append((rel, m.group(1).strip()))

    missing_all = []
    for rel, target in results:
        if is_nav(target):
            continue
        base = os.path.basename(target.replace("\\", "/"))
        if norm(base) not in content_index:
            missing_all.append((rel, target))

    def subject_of(rel):
        parts = rel.split(os.sep)
        return parts[1] if len(parts) > 1 else "(root)"

    print("TOTAL md files:", len(all_md))
    print("Baseline files:", len(bok_files))
    print("Content files:", len(content_files))
    print("Wikilinks extracted:", len(results))
    print("Missing link refs (normalized, nav excluded):", len(missing_all))
    print()

    print("=== Missing-link counts per subject ===")
    by_subject = collections.Counter(subject_of(rel) for rel, _ in missing_all)
    for s, c in by_subject.most_common():
        print(f"  {s}: {c}")

    print()
    print("=== Unique missing targets per subject (verify with ls before reporting) ===")
    for subj in sorted({subject_of(rel) for rel, _ in missing_all}):
        tgts = sorted({t for rel, t in missing_all if subject_of(rel) == subj})
        print(f"\n--- {subj} ({len(tgts)} unique) ---")
        for t in tgts:
            print(f"  [[{t}]]")

    print()
    print("=== Content file count per top folder ===")
    c = collections.Counter(os.path.relpath(p, root).split(os.sep)[0] for p in content_files)
    for k, v in sorted(c.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
