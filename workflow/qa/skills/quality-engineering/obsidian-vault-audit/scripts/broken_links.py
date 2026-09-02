#!/usr/bin/env python3
"""Scan an Obsidian vault for broken wikilinks.

Resolves links the way Obsidian does: by note BASENAME (case-insensitive),
ignoring path, heading (#...), and alias (|...). Handles the escaped-pipe
markdown-table form [[note\\|alias]] and skips embeds ![[...]].

Usage:
    python broken_links.py "F:/obsidian_note/general-knowledge" [--collisions]

Output:
    - broken-link count by top-level folder
    - detail list (file -> [[target]])
    - with --collisions: normalized-name collision groups (>=2 distinct
      basenames sharing a stripped/space-normalized form). These are the
      dangerous cases for any auto-remap pass — a target that normalizes to
      a collision must NEVER be auto-rewritten; map it explicitly instead.
"""
import os
import re
import sys
import collections

def walk_md(root, exclude=('.git', '.obsidian', 'node_modules')):
    out = []
    for d, dn, fn in os.walk(root):
        dn[:] = [x for x in dn if x not in exclude]
        for f in fn:
            if f.lower().endswith('.md'):
                out.append(os.path.join(d, f))
    return out

def norm(s):
    """Strip leading number prefix, unify separators/case for collision detection."""
    s = re.sub(r'^\d{1,2}[_\-\s]+', '', s.strip().rstrip('\\').strip())
    s = s.replace('_', ' ').replace('-', ' ').replace(',', '')
    return re.sub(r'\s+', ' ', s).strip().lower()

LINK = re.compile(r'\[\[(.*?)\]\]', re.DOTALL)

def targets_of(text):
    for m in LINK.finditer(text):
        inner = m.group(1).replace('\\|', '|')   # unescape table pipe
        if inner.startswith('!'):
            continue                              # skip embeds
        if '#' in inner:
            inner = inner.split('#')[0]           # drop heading
        t = inner.split('|')[0].strip()           # drop alias
        if t:
            yield t

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    root = sys.argv[1]
    show_collisions = '--collisions' in sys.argv[2:]

    files = walk_md(root)
    basenames = [os.path.splitext(os.path.basename(p))[0] for p in files]
    bset = set(b.lower() for b in basenames)

    broken = []
    for p in files:
        rel = os.path.relpath(p, root)
        for t in targets_of(open(p, encoding='utf-8').read()):
            base = os.path.basename(t.replace('\\', '/'))
            if base.lower() not in bset:
                broken.append((rel, t))

    print(f"broken links: {len(broken)}")
    by = collections.Counter(rel.split(os.sep)[0] for rel, _ in broken)
    for top, c in sorted(by.items()):
        print(f"  {top}: {c}")
    print()
    for rel, t in sorted(set(broken)):
        print(f"  [{rel}]  [[{t}]]")

    if show_collisions:
        grp = collections.defaultdict(list)
        for b in basenames:
            grp[norm(b)].append(b)
        coll = [(n, sorted(set(v))) for n, v in grp.items() if len(set(v)) >= 2]
        print(f"\ncollision groups (>=2 distinct basenames): {len(coll)}")
        for n, v in coll:
            print(f"  '{n}': {v}")

if __name__ == '__main__':
    main()
