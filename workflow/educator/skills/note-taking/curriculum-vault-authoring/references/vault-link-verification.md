# vault-link-verification notes

Reusable patterns for verifying newly created curriculum content roots. proven 2026-08-28 on
`English Curriculum/` (28 files, 249 links). Run via `execute_code` (stdlib only).

## 1. Wikilink resolution check (the core QA gate)

Walks every `.md` under a content root, extracts `[[target]]` and `[[target|alias]]` links,
and resolves each against the FULL vault (not just the new folder — cross-links point at
sibling roots and `body-of-knowledge/`).

- Bare `[[Name]]` → match against vault-wide basename index (handles multi-basename files,
  e.g. the vault had 25 `00_overview.md` at one point).
- `[[path/to/note]]` or `[[../relative/note]]` → resolve on disk from the containing file's directory.
- Strip a trailing `\` from targets — table-escaped links in BOK tables appear as `[[Note\|alias]]`.

```python
import os, re, glob
from collections import defaultdict

BASE = r"F:/obsidian_note/general-knowledge"   # vault root
SCAN_ROOTS = [os.path.join(BASE, "English Curriculum"),
              os.path.join(BASE, "body-of-knowledge", "English", "English - Overview.md")]

all_files = {}
for root, dirs, files in os.walk(BASE):
    if ".git" in root or ".obsidian" in root:
        continue
    for f in files:
        if f.endswith(".md"):
            all_files.setdefault(f[:-3], []).append(os.path.join(root, f))

link_re = re.compile(r"\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
broken = defaultdict(list)
total = 0
for md in [p for r in SCAN_ROOTS if os.path.isdir(r)
           for p in glob.glob(os.path.join(r, "**", "*.md"), recursive=True)] + \
          [p for r in SCAN_ROOTS if os.path.isfile(r)]:
    text = open(md, encoding="utf-8").read()
    rel = os.path.relpath(md, BASE)
    for m in link_re.finditer(text):
        t = m.group(1).strip().rstrip("\\")
        total += 1
        if t.startswith("..") or "/" in t or "\\" in t:
            ok = os.path.exists(os.path.normpath(
                t if os.path.isabs(t) else os.path.join(os.path.dirname(md), t) + ".md"))
        else:
            ok = t in all_files
        if not ok:
            broken[t].append(rel)

print(f"Scanned links: {total}")
for t, s in sorted(broken.items()):
    print(f"  BROKEN [[{t}]] <- {s}")
print("ALL LINKS RESOLVE" if not broken else f"{len(broken)} broken targets")
```

**False positive to know:** `[[English Curriculum/01 Language for
Communication/00_overview]]` written from inside `body-of-knowledge/English/` is a valid
Obsidian VAULT-ROOT-relative path link. The naive resolver flags it; verify with
`os.path.exists(os.path.join(BASE, target + ".md"))` against the vault root before
reporting it broken.

## 2. Artifact greps (run in terminal after batch creation)

```bash
cd "<new content root>"
find . -name "*.md" -type f -exec du -b {} + | sort -k2   # size scan: sibling outliers = truncation
grep -rnP '[\x{0E01}-\x{0E5B}][A-Za-z]' --include="*.md" . | head   # Thai char + Latin letter = corruption
grep -rnP '[\x{4e00}-\x{9fff}]' --include="*.md" . | head           # CJK slips
grep -rn '\\\\\\\\' --include="*.md" . | head                       # double-backslash LaTeX
tail -15 <sample>.md                                                 # garbage-tail check (full-size corruption)
```

## 3. Session log (2026-08-28, English Curriculum closure)

- BOK finding: "English 🟡 Partial — supplementary English Skill/ only; 4-strand
  curriculum notes still absent". Contract = the BOK's own topic tables (24 concept areas).
- Created `English Curriculum/` with 4 strand folders, continuous numbering 01–24
  (Strand 1 = 01–06 ... Strand 4 = 19–24) + 4 × 00_overview.md trackers (6/6 each).
- Cross-linked into existing `English Skill/` notes by exact filename
  (`[[28 Academic Word List]]`, `[[32 Skimming & Scanning]]`, `[[44 Time Management]]` —
  section headings like `[[09 Vocabulary Building]]` are NOT files and don't resolve).
- BOK overview patched: "Curriculum Content Notes" wikilink table per strand section,
  strand-overview links in Related. No inline-code path references (audit N1).
- Result: 28 files, 3.9–7.3 KB, 249/249 links resolve, 0 artifacts.
