#!/usr/bin/env python3
"""Verify Obsidian-safe Mermaid blocks in markdown notes.

Enforces the four hard rules from obsidian-note-authoring SKILL.md:
  (1) 'flowchart' keyword, not 'graph'
  (2) no bare parentheses in node labels
  (3) no '"N."' dot-number labels
  (4) no bare '&' in quoted labels

Usage: python mermaid_check.py <file-or-dir> [<file-or-dir> ...]
Prints 'ISSUE: <file> <block#> <reason>' lines and exits 1 on any hit.
Files with no mermaid block are skipped (hubs/index tables are fine).
"""
import os
import re
import sys
import glob


def check_block(b):
    issues = []
    if re.search(r"\bgraph\b", b):
        issues.append("uses 'graph' instead of 'flowchart'")
    for m in re.finditer(r'\[[^\]]*\([^\]]*\]', b):
        if '&#40;' not in m.group(0):
            issues.append("parens in label: %r" % m.group(0))
    for m in re.finditer(r'"\d+\.', b):
        issues.append("dot-number label: %r" % m.group(0))
    for m in re.finditer(r'"[^"]*&[^"]*"', b):
        if ' and ' not in m.group(0):
            issues.append("ampersand in label: %r" % m.group(0))
    return issues


def check_file(path):
    txt = open(path, encoding="utf-8").read()
    blocks = re.findall(r"```mermaid\n(.*?)```", txt, re.DOTALL)
    name = os.path.basename(path)
    out = []
    for i, b in enumerate(blocks):
        for reason in check_block(b):
            out.append((name, i, reason))
    return out


def main():
    args = sys.argv[1:] or ["."]
    files = []
    for a in args:
        if os.path.isdir(a):
            files += sorted(glob.glob(os.path.join(a, "**", "*.md"), recursive=True))
        else:
            files.append(a)
    all_issues = []
    for f in files:
        all_issues += check_file(f)
    if all_issues:
        for it in all_issues:
            print("ISSUE:", it)
        sys.exit(1)
    print("ALL CLEAR: %d files, every mermaid block Obsidian-safe." % len(files))


if __name__ == "__main__":
    main()
