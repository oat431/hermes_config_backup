#!/usr/bin/env python3
"""Verify an Obsidian career-path (or any) vault fill.

Hard checks (determine PASS/FAIL):
  - per-area NN_* file counts (default 8: area overview + 7 topic notes)
  - size floors: 00_overview.md >= 4 KB, topic notes >= 5 KB
  - frontmatter `role:` present (career-path convention)
  - mermaid arrow syntax — only `-->` edges, no single-dash `->`
  - wikilink resolution under Obsidian's ACTUAL semantics:
      * bare names resolve iff the filename is unique vault-wide, OR a
        same-named file sits in the linking file's own folder (same-folder
        wins ties when duplicate basenames exist across folders);
      * path-style links match by equality OR path suffix;
      * relative links (../x) resolve against the linking file's folder;
      * stripped before resolving: #anchors, plain aliases [[target|alias]],
        and escaped-pipe aliases [[target\\|alias]] (the correct form inside
        markdown tables).
      Comparison is CASE-INSENSITIVE (Windows vaults are), so
      [[DMBOK v2 - Overview]] legitimately resolves to DMBoK v2 - Overview.md.
  - optional baseline.json: per-file byte sizes from a previously verified
    fill — mismatches/missing files are reported as damage.

Warnings (reported, never fail the run):
  - missing standard sections
  - no mermaid block in a file
  - non-ISO created:/updated: dates

Usage:
  python verify_vault_fill.py <vault_root> <path_rel> [files_per_area] [baseline.json]
    path_rel       e.g. career-path/03_Staff_Engineer
    files_per_area expected .md count per NN_* area dir (default 8)
    baseline.json  optional: previously saved sizes JSON; mismatches reported

Save the report's "sizes" map as the baseline for a later damage check:
  python verify_vault_fill.py VAULT PATH 8 > report.json
"""
import json
import os
import re
import sys

COMMON_SECTIONS = ["## Why This Matters", "## Practical Applications",
                   "## Common Pitfalls", "## Success Indicators", "## Summary"]
OVERVIEW_EXTRA = ["## Topics in This Capability Area", "## Related Capabilities"]
NOTE_EXTRA = ["## Related Topics"]
ISO_DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def link_target(inner: str) -> str:
    """Extract the link target from [[...]] inner text.

    Escaped-pipe aliases ([[target\\|alias]]) come first: they are the correct
    Obsidian form inside markdown tables, and splitting on the plain pipe first
    would keep the trailing backslash on the target.
    """
    if "\\|" in inner:
        inner = inner.split("\\|")[0]
    elif "|" in inner:
        inner = inner.split("|")[0]
    return inner.split("#")[0].strip()


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    vault_root = sys.argv[1]
    path_rel = sys.argv[2].replace("\\", "/")
    expected = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    baseline_path = sys.argv[4] if len(sys.argv) > 4 else None

    path_dir = os.path.join(vault_root, *path_rel.split("/"))
    if not os.path.isdir(path_dir):
        print(json.dumps({"error": f"not a directory: {path_dir}"}))
        return 2

    # Index the WHOLE vault, LOWERCASED — Windows filesystems are
    # case-insensitive; links also legitimately point into sibling areas
    # (software-engineering-note/, body-of-knowledge/, ...), so a
    # scope-limited index would false-flag every cross-area link.
    vault_paths, name_index = set(), {}
    for dp, _, fns in os.walk(vault_root):
        for fn in fns:
            if fn.endswith(".md"):
                rel = os.path.relpath(os.path.join(dp, fn), vault_root).replace("\\", "/").lower()
                vault_paths.add(rel)
                vault_paths.add(rel[:-3])
                name_index.setdefault(fn[:-3].lower(), []).append(rel)

    def resolves(link: str, containing_rel: str) -> bool:
        link = link.replace("\\", "/").lower()
        if not link:
            return True
        if link.startswith("../"):
            # Relative links resolve against the linking file's own folder.
            resolved = os.path.normpath(os.path.join(containing_rel, link)).replace("\\", "/").lower()
            return resolved in vault_paths
        if "/" in link:
            return link in vault_paths or any(p.endswith("/" + link) for p in vault_paths)
        # Bare name: a same-folder match wins when duplicate basenames exist
        # across folders (Obsidian prefers the closest file).
        same_dir = [p for p in name_index.get(link, []) if os.path.dirname(p) == containing_rel]
        if same_dir:
            return True
        return len(name_index.get(link, [])) == 1

    link_re = re.compile(r"\[\[([^\]]+?)\]\]")
    problems, warnings = [], []

    # Discover areas (NN_* subdirs) and files
    areas = sorted(d for d in os.listdir(path_dir)
                   if os.path.isdir(os.path.join(path_dir, d)) and re.match(r"^[0-9][0-9]_", d))
    sizes = {}
    for area in areas:
        ad = os.path.join(path_dir, area)
        md = sorted(f for f in os.listdir(ad) if f.endswith(".md"))
        if len(md) != expected:
            problems.append(f"{area}: {len(md)} files (expected {expected})")
        for f in md:
            p = os.path.join(ad, f)
            sizes[f"{area}/{f}"] = os.path.getsize(p)
            floor = 4000 if f == "00_overview.md" else 5000
            if os.path.getsize(p) < floor:
                problems.append(f"{area}/{f}: {os.path.getsize(p)}B below {floor} floor")

    # Scan every file: links, mermaid, frontmatter, sections
    all_files = [(os.path.join(path_dir, f), f) for f in os.listdir(path_dir) if f.endswith(".md")]
    all_files += [(os.path.join(path_dir, a, f), f"{a}/{f}") for a in areas
                  for f in os.listdir(os.path.join(path_dir, a)) if f.endswith(".md")]
    checked = 0
    arrow_bad, broken = [], []
    for p, rel in all_files:
        text = open(p, encoding="utf-8").read()
        is_overview = os.path.basename(p) == "00_overview.md"
        containing_rel = os.path.dirname(os.path.relpath(p, vault_root)).replace("\\", "/").lower()
        if not re.search(r"^role:", text, re.M):
            problems.append(f"{rel}: missing role: frontmatter")
        for m in link_re.finditer(text):
            checked += 1
            if not resolves(link_target(m.group(1)), containing_rel):
                broken.append(f"{rel} -> [[{m.group(1)}]]")
        blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
        if not blocks:
            warnings.append(f"{rel}: no mermaid block")
        for block in blocks:
            for line in block.splitlines():
                s = line.strip()
                if re.search(r"(?<!-)->(?!-)", s):
                    arrow_bad.append(f"{rel}: {s[:60]}")
        for section in COMMON_SECTIONS + (OVERVIEW_EXTRA if is_overview else NOTE_EXTRA):
            if section not in text:
                warnings.append(f"{rel}: missing section {section}")
        fm = re.match(r"^---\n(.*?)\n---", text, re.S)
        if fm:
            for key in ("created", "updated"):
                line = next((ln for ln in fm.group(1).splitlines()
                             if ln.startswith(key + ":")), None)
                if line:
                    value = line.split(":", 1)[1].strip().strip("'\"")
                    if value and not ISO_DATE.match(value):
                        warnings.append(f"{rel}: non-ISO {key}: {value}")

    # Baseline damage check
    damage = []
    if baseline_path and os.path.exists(baseline_path):
        baseline = json.load(open(baseline_path, encoding="utf-8"))
        for rel, was in baseline.items():
            if rel in sizes and sizes[rel] != was:
                damage.append(f"{rel}: {sizes[rel]}B now, {was}B at baseline")
        for rel in baseline:
            if rel not in sizes:
                damage.append(f"{rel}: in baseline, missing now")

    result = {
        "path": path_rel,
        "areas": {a: len([f for f in os.listdir(os.path.join(path_dir, a)) if f.endswith(".md")]) for a in areas},
        "root_files": sorted(f for f in os.listdir(path_dir) if f.endswith(".md")),
        "links_checked": checked,
        "broken_links": broken,
        "mermaid_arrow_issues": arrow_bad,
        "baseline_damage": damage,
        "other_problems": problems,
        "warnings": warnings,
        "sizes": sizes,
        "verification": "PASS" if not (broken or arrow_bad or damage or problems) else "FAIL",
    }
    print(json.dumps(result, indent=2))
    return 0 if result["verification"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
