# Song Line Alignment Validator

Validates that English and Thai blockquote groups in song translation notes have matching line counts.

## When to Use

After creating or editing any song translation note. Run before presenting to the user.

## Script (Python with hermes_tools)

```python
from hermes_tools import terminal
import re

def has_thai(text):
    return bool(re.search(r'[\u0E00-\u0E7F]', text))

def has_cjk(text):
    """Check for Chinese/Japanese characters that shouldn't be in Thai text"""
    return bool(re.search(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))

def validate_song(filepath):
    """Validate a song translation note for alignment issues."""
    r = terminal(f'cat "{filepath}"')
    content = r.get('output', '')
    lines = content.split('\n')

    # Find "## Lyric + Thai Translation" section (not Detail)
    in_section = False
    pairs = []  # (type, [lines])
    current_group = []
    group_type = None

    for line in lines:
        if re.match(r'^## Lyric \+ Thai Translation$', line.strip()):
            in_section = True
            continue
        if in_section and line.startswith('## '):
            break
        if not in_section:
            continue

        if line.startswith('> '):
            text = line[2:]
            if has_thai(text):
                new_type = 'th'
            else:
                new_type = 'en'

            if group_type != new_type:
                if current_group:
                    pairs.append((group_type, current_group))
                current_group = []
                group_type = new_type
            current_group.append(text)
        elif line.strip() == '' and current_group:
            pairs.append((group_type, current_group))
            current_group = []
            group_type = None

    if current_group:
        pairs.append((group_type, current_group))

    issues = []

    # Check alignment
    for idx in range(0, len(pairs)-1, 2):
        if idx+1 >= len(pairs):
            break
        gtype_en, en_lines = pairs[idx]
        gtype_th, th_lines = pairs[idx+1]

        if gtype_en != 'en' or gtype_th != 'th':
            issues.append(f"Type mismatch at pair {idx//2+1}: {gtype_en}/{gtype_th}")
            continue

        if len(en_lines) != len(th_lines):
            issues.append(f"Count mismatch at pair {idx//2+1}: {len(en_lines)} EN vs {len(th_lines)} TH")
            for j in range(max(len(en_lines), len(th_lines))):
                en = en_lines[j][:60] if j < len(en_lines) else "(missing)"
                th = th_lines[j][:60] if j < len(th_lines) else "(missing)"
                issues.append(f"  {j+1}. EN: {en}")
                issues.append(f"     TH: {th}")

    # Check for CJK in Thai lines
    for gtype, glines in pairs:
        if gtype == 'th':
            for line in glines:
                if has_cjk(line):
                    cjk_chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', line)
                    issues.append(f"CJK characters found: {''.join(cjk_chars)} in '{line[:50]}'")

    # Check for em-dashes
    for gtype, glines in pairs:
        for line in glines:
            if '—' in line:
                issues.append(f"Em-dash found in: '{line[:50]}'")

    # Check duplicates (excluding legitimate repetitions)
    all_thai = []
    for gtype, glines in pairs:
        if gtype == 'th':
            all_thai.extend(glines)

    seen = {}
    for i, line in enumerate(all_thai):
        if line in seen:
            # Only flag if NOT paired with a repeated English line
            issues.append(f"Duplicate Thai: '{line[:50]}' (pos {seen[line]+1} and {i+1})")
        else:
            seen[line] = i

    return issues

# Usage:
# issues = validate_song(r"F:\obsidian_note\oralita_md\musical\Some Song.md")
# for issue in issues:
#     print(f"  ⚠️ {issue}")
# if not issues:
#     print("  ✅ All clean")
```

## Key Patterns

| Issue | Cause | Fix |
|-------|-------|-----|
| Count mismatch (e.g., 8 EN vs 5 TH) | Source translator combined lines | Acceptable if Detail table has per-line alignment |
| Count mismatch (e.g., 7 EN vs 8 TH) | Thai has extra line or is split wrong | Merge or realign Thai lines |
| Missing Thai line | Forgot to translate or copy-paste error | Add the missing translation |
| CJK characters | AI model produced Chinese instead of Thai | Replace with Thai equivalent (残酷→โหดร้าย) |
| Em-dash | Default punctuation style | Replace with colon (:) |
| Duplicate Thai | Song legitimately repeats (e.g., chorus, "One day more!") | Note as "legitimate song repetition" — only flag UNEXPECTED duplicates |

## Handling Legitimate Song Repetitions

Many songs intentionally repeat lines. The validator's duplicate check will flag ALL repeated Thai lines, but most are legitimate:

**Legitimate repetitions (do NOT fix):**
- Refrains/choruses that repeat (e.g., "อีกวันใหม่" appears 7 times in "One Day More")
- Call-and-response patterns where both sides say the same thing
- Intro/outro echoes of the same line
- Song motifs that return (e.g., "เฝ้ารอ เฝ้ารอ" in EPIC)

**Actual problems (DO fix):**
- The same Thai translation on two DIFFERENT English lines (mismatched)
- Duplicate lines caused by copy-paste errors
- Thai line duplicated when the English line is NOT duplicated

**How to triage:** When the validator reports a duplicate, check whether the CORRESPONDING English line is also repeated. If both EN and TH repeat → legitimate. If only TH repeats → bug.
