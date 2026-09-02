#!/usr/bin/env python3
"""Verify an Obsidian career-path (or any) vault fill.

Checks: per-area file counts, size floors, frontmatter presence, mermaid
arrow syntax, and wikilink resolution using Obsidian's ACTUAL semantics
(bare-name uniqueness + path suffix match). Optionally compares current
per-file byte sizes against a saved baseline to detect damage from later
delegation waves that claim to have touched/reverted pre-existing files.

Usage:
  python verify_vault_fill.py <vault_root> <path_rel> [files_per_area] [baseline.json]
    path_rel       e.g. career-path/03_Staff_Engineer
    files_per_area expected .md count per NN_* area dir (default 8)
    baseline.json  optional: previously saved sizes JSON; mismatches reported

Output: JSON on stdout. Exit 0 on PASS, 1 on FAIL. The "sizes" map is the
baseline you can save for the next fill's damage check:
  python verify_vault_fill.py VAULT PATH 8 > path_baseline.json   (then edit,
  or capture sizes from the report of a verified fill)
"""
import json
import os
import re
import sys

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

    # Index the whole vault for Obsidian-style resolution
    vault_paths, name_index = set(), {}
    for dp, _, fns in os.walk(vault_root):
        for fn in fns:
            if fn.endswith(".md"):
                rel = os.path.relpath(os.path.join(dp, fn), vault_root).replace("\\", "/")
                vault_paths.add(rel)
                vault_paths.add(rel[:-3])
                name_index.setdefault(fn[:-3], []).append(rel)

    def resolves(link: str) -> bool:
        link = link.split("#")[0].strip()
        if not link:
            return True
        if "/" in link:
            n = link.replace("\\", "/")
            return any(p == n for p in vault_paths) or any(p.endswith("/" + n) for p in vault_paths)
        return len(name_index.get(link, [])) == 1

    link_re = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")
    problems = []

    # Discover areas (NN_* subdirs) and files
    areas = sorted(d for d in os.listdir(path_dir)
                   if os.path.isdir(os.path.join(path_dir, d)) and re.match(r"^\d\d_", d))
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

    # Scan every file: links, mermaid, frontmatter
    all_files = [(os.path.join(path_dir, f), f) for f in os.listdir(path_dir) if f.endswith(".md")]
    all_files += [(os.path.join(path_dir, a, f), f"{a}/{f}") for a in areas
                  for f in os.listdir(os.path.join(path_dir, a)) if f.endswith(".md")]
    checked = 0
    arrow_bad, broken = [], []
    for p, rel in all_files:
        text = open(p, encoding="utf-8").read()
        if not re.search(r"^role:", text, re.M):
            problems.append(f"{rel}: missing role: frontmatter")
        for m in link_re.finditer(text):
            checked += 1
            if not resolves(m.group(1)):
                broken.append(f"{rel} -> [[{m.group(1)}]]")
        for block in re.findall(r"```mermaid\n(.*?)```", text, re.S):
            for line in block.splitlines():
                s = line.strip()
                if re.search(r"(?<!-)->(?!-)", s):
                    arrow_bad.append(f"{rel}: {s[:60]}")

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
        "sizes": sizes,
        "verification": "PASS" if not (broken or arrow_bad or damage or problems) else "FAIL",
    }
    print(json.dumps(result, indent=2))
    return 0 if result["verification"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
