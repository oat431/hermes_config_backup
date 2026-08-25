"""
fix-mermaid-ampersands.py — Replace bare ampersands inside Mermaid node labels.

Mermaid treats bare '&' as an HTML special character, breaking labels like "Research & Define".
Fix: replace with "and". Also handles "R&D" → "R and D".

Only operates inside ```mermaid ... ``` blocks.

Usage:
  python3 fix-mermaid-ampersands.py <root_directory>

  Defaults to F:\obsidian_note\general-knowledge\career\ if no arg given.
"""
import os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else r'F:\obsidian_note\general-knowledge\career'
count = 0

for dirpath, dirs, files in os.walk(root):
    for f in files:
        if not f.endswith('.md'):
            continue
        path = os.path.join(dirpath, f)
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()

        lines = content.split('\n')
        in_mermaid = False
        changed = False

        for i, line in enumerate(lines):
            if line.strip() == '```mermaid':
                in_mermaid = True
                continue
            if in_mermaid and line.strip() == '```':
                in_mermaid = False
                continue
            if not in_mermaid:
                continue
            old = line
            if '&' in line and '&amp;' not in line and '&#40;' not in line:
                line = line.replace(' & ', ' and ')
                line = line.replace('& ', 'and ')
                line = line.replace(' &', ' and')
                line = line.replace('R&D', 'R and D')
                line = line.replace('R & D', 'R and D')
            if line != old:
                lines[i] = line
                changed = True
                count += 1

        if changed:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write('\n'.join(lines))
            print(f'Fixed: {os.path.basename(path)}')

print(f'\nTotal: {count} ampersands fixed')
