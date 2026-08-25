"""Verify a program note for integrity — schedule days, sections, key elements.

Usage: python verify-program.py <vault_path> <program_filename>
Example: python verify-program.py "F:\\projects\\orlita_md" "4-week-program-phase1.md"

Checks:
- File exists and is non-empty
- Valid YAML frontmatter
- All expected section headings present
- Schedule days extracted from the file — reports which days appear
- Key programming elements (compounds, progression rules, recovery checklist)
- Run/walk schedule present
"""

import sys
import re
from pathlib import Path


def main(vault: str, filename: str) -> int:
    path = Path(vault) / "fitness" / filename
    if not path.exists():
        print(f"FAIL: {path} not found")
        return 1

    content = path.read_text()
    if len(content) < 500:
        print(f"FAIL: file too small ({len(content)} bytes)")
        return 1

    # Frontmatter check
    if not content.startswith("---"):
        print("FAIL: missing YAML frontmatter")
        return 1

    failures = 0

    # --- Required sections ---
    required_sections = [
        "Schedule",
        "Session Protocol",
        "Progression Rules",
        "Recovery Checklist",
        "Run/Walk Schedule",
    ]
    for section in required_sections:
        if section.lower() not in content.lower():
            print(f"FAIL: missing section '{section}'")
            failures += 1
        else:
            print(f"  Section: {section} ✓")

    # --- Extract training days ---
    # Look for "### Mon — ...", "### Tue — ...", etc.
    day_headings = re.findall(
        r'###\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b', content
    )
    if day_headings:
        print(f"  Training days: {sorted(set(day_headings))}")
    else:
        # Try bullet-style: "- **Mon:** Upper"
        day_bullets = re.findall(
            r'\*\*(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\*\*', content
        )
        if day_bullets:
            print(f"  Training days (inline): {sorted(set(day_bullets))}")
        else:
            print("WARN: no training days detected — check format")
            # Not a failure since compact tables may not match these patterns

    # --- Key programming elements ---
    compounds = ["Squat", "Bench", "Deadlift", "OHP", "Row", "Press"]
    found = [c for c in compounds if c.lower() in content.lower()]
    if not found:
        print("WARN: no compound lifts detected")
    else:
        print(f"  Compounds found: {found}")

    # Progression keywords
    prog_keywords = ["2.5 kg", "add weight", "progression", "deload"]
    found_prog = [k for k in prog_keywords if k.lower() in content.lower()]
    if not found_prog:
        print("FAIL: no progression rules detected")
        failures += 1
    else:
        print(f"  Progression: {found_prog} ✓")

    # Recovery
    rec_keywords = ["sleep", "water", "kcal", "protein"]
    found_rec = [k for k in rec_keywords if k.lower() in content.lower()]
    if len(found_rec) < 2:
        print("FAIL: recovery checklist incomplete")
        failures += 1
    else:
        print(f"  Recovery: {found_rec} ✓")

    # --- Time column in schedule table ---
    if "| Time |" in content:
        print("  Time column: present ✓")
    else:
        print("WARN: schedule table missing 'Time' column — add session duration estimates")

    # --- Rest column in exercise tables ---
    # Count "| Rest |" headers (one per training day — usually 4)
    rest_headers = len(re.findall(r'\|\s*Rest\s*\|', content))
    if rest_headers >= 3:
        print(f"  Rest column: {rest_headers} exercise tables ✓")
    elif rest_headers > 0:
        print(f"WARN: Rest column found in only {rest_headers} tables — expected all training days")
    else:
        print("FAIL: no Rest column in exercise tables — add rest times (2 min compounds, 90 sec compound-accessories, 60 sec isolations, 30 sec core)")
        failures += 1

    # --- Time estimates ---
    if "~" in content and "min" in content:
        times = re.findall(r'~(\d+)\s*min', content)
        if times:
            print(f"  Time estimates: {times} ✓")
        else:
            print("WARN: no time estimates in schedule")
    else:
        print("WARN: no time estimates in schedule")

    # --- Summary ---
    print(f"\n  Lines: {len(content.splitlines())}")
    if failures == 0:
        print("✅ All checks passed")
        return 0
    else:
        print(f"❌ {failures} failure(s)")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python verify-program.py <vault_path> <program_filename>")
        sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2]))
