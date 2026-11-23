#!/usr/bin/env python3
"""Extract and render every mermaid block under a markdown file or folder.

mmdc's exit code is the only reliable parse verdict; this reports it per block
plus a summary line `TOTAL: <n> fails: <n>`. Extraction is fence-aware, so an
unterminated ```mermaid is still handed to the renderer instead of being
silently skipped.

Setup once per scratch dir (scratch entries are pruned after ~24h idle):
    PUPPETEER_SKIP_DOWNLOAD=true bun add @mermaid-js/mermaid-cli puppeteer
    printf '{"executablePath":"<path/to/msedge.exe>","args":["--no-sandbox","--disable-gpu"]}' > puppeteer.json

Usage:
    python render_mermaid_blocks.py --root <md-file-or-folder> [--work mermaid-verify]
                                    [--mmdc ./node_modules/.bin/mmdc] [--puppeteer puppeteer.json]
"""
import argparse
import os
import subprocess
import sys


def iter_blocks(md_path):
    """Yield (index, body_lines) for each ```mermaid fence, fence-aware."""
    with open(md_path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    in_fence = False
    info = ""
    cur = []
    idx = 0
    for ln in lines:
        s = ln.strip()
        if s.startswith("```"):
            if not in_fence:
                info = s[3:].strip()
                cur = []
            else:
                if info.startswith("mermaid"):
                    idx += 1
                    yield idx, cur
            in_fence = not in_fence
            continue
        if in_fence and info.startswith("mermaid"):
            cur.append(ln)
    if in_fence and info.startswith("mermaid"):
        idx += 1
        yield idx, cur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="markdown file or folder")
    ap.add_argument("--work", default="mermaid-verify", help="output dir for .mmd/.png")
    ap.add_argument("--mmdc", default="./node_modules/.bin/mmdc")
    ap.add_argument("--puppeteer", default="puppeteer.json")
    args = ap.parse_args()

    if not os.path.exists(args.mmdc):
        print(f"mmdc not found at {args.mmdc} — install mermaid-cli first (see docstring)")
        return 2

    if os.path.isfile(args.root):
        base = os.path.dirname(os.path.abspath(args.root))
        md_files = [args.root]
    else:
        base = os.path.abspath(args.root)
        md_files = []
        for dp, dn, fns in os.walk(args.root):
            dn[:] = [d for d in dn if not d.startswith(".")]
            md_files += [os.path.join(dp, f) for f in fns if f.endswith(".md")]

    os.makedirs(args.work, exist_ok=True)
    total = fails = 0
    for md in sorted(md_files):
        rel = os.path.relpath(os.path.abspath(md), base)
        for idx, body in iter_blocks(md):
            total += 1
            stem = rel.replace(os.sep, "__")[:-3] + f"__b{idx}"
            src = os.path.join(args.work, stem + ".mmd")
            out = os.path.join(args.work, stem + ".png")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write("\n".join(body) + "\n")
            r = subprocess.run(
                [args.mmdc, "-i", src, "-o", out, "-p", args.puppeteer, "-q"],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                fails += 1
                detail = (r.stderr or r.stdout).strip().splitlines()
                print(f"FAIL {rel} block {idx}: {' | '.join(detail[:2])}")
            else:
                print(f"ok   {rel} block {idx}")
    print(f"TOTAL: {total} fails: {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
