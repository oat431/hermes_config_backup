#!/usr/bin/env python3
"""Verify that every vault path referenced in SOUL files resolves.

Usage:
    python verify_soul_refs.py <soul-dir> [vault-root] [template-root]

Scans every .md file under <soul-dir> (recursively) and checks each
backtick-wrapped reference that looks like a vault path:

    `document_template\\15_Data_Management\\Data-Catalog.md`   -> template-root
    `career-path\\02_Senior_Software_Engineer\\`               -> vault-root
    `SWEBOK\\05_Software_Testing.md` (also CyBOK/DMBOK/...)    -> vault-root/body-of-knowledge
    `F:\\obsidian_note\\...`                                   -> absolute
    `Business-Case.md` after another ref in the same cell     -> same folder as that ref

Backslash and forward-slash references are both handled. Folder references
(trailing slash) are checked too. Bare relative folders with no known prefix
(e.g. `01_Problem_Discovery\\`) are skipped — check those by hand.

Defaults:
    soul-dir      = current directory
    vault-root    = F:/obsidian_note/swe-knowledge
    template-root = F:/obsidian_note/document_template

Exit code 1 if any reference is missing.
"""
import os
import re
import sys

DEFAULT_VAULT = "F:/obsidian_note/swe-knowledge"
DEFAULT_TEMPLATES = "F:/obsidian_note/document_template"

VAULT_PREFIXES = (
    "body-of-knowledge/", "software-engineering-note/",
    "computing-foundation-note/", "career-path/",
)
BOK_PREFIXES = ("SWEBOK/", "CyBOK/", "DMBOK/", "BABOK/", "PMBOK/")
TEMPLATE_PREFIXES = ("document_template/", "document-template/")

CODE_SPAN = re.compile(r"`([^`]+)`")


def resolve(ref, prev_dir, vault, templates):
    """Return the filesystem path a reference points to, or None to skip."""
    r = ref.replace("\\", "/").strip()
    if not r:
        return None
    if re.match(r"^[A-Za-z]:/", r):
        return r
    for p in TEMPLATE_PREFIXES:
        if r.startswith(p):
            return templates + "/" + r[len(p):]
    if r.startswith(VAULT_PREFIXES):
        return vault + "/" + r
    if r.startswith(BOK_PREFIXES):
        return vault + "/body-of-knowledge/" + r
    # Bare filename continuing a multi-file cell: same folder as previous ref.
    if "/" not in r and r.endswith(".md") and prev_dir:
        return prev_dir + "/" + r
    return None


def main():
    soul_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    vault = (sys.argv[2] if len(sys.argv) > 2 else DEFAULT_VAULT).replace("\\", "/").rstrip("/")
    templates = (sys.argv[3] if len(sys.argv) > 3 else DEFAULT_TEMPLATES).replace("\\", "/").rstrip("/")

    checked, missing = set(), []
    for root, _, files in os.walk(soul_dir):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
            for line_no, line in enumerate(lines, 1):
                prev_dir = None
                for ref in CODE_SPAN.findall(line):
                    target = resolve(ref, prev_dir, vault, templates)
                    if target is None:
                        continue
                    target = target.rstrip("/")
                    prev_dir = os.path.dirname(target) if target.endswith(".md") else target
                    checked.add(target)
                    if not os.path.exists(target):
                        missing.append((os.path.relpath(path, soul_dir), line_no, ref))

    print(f"unique vault refs checked: {len(checked)}")
    if missing:
        print("MISSING:")
        for f, n, r in missing:
            print(f"   {f}:{n}  {r}")
        sys.exit(1)
    print("ALL VAULT REFS RESOLVE")


if __name__ == "__main__":
    main()
