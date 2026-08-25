"""
fix-mermaid-dots.py — Remove dots after numbers inside Mermaid node labels.

Mermaid misinterprets "1. Assessment" as list syntax inside labels.
Fix: "1. Assessment" → "1 Assessment" (remove dot, keep space).

Only operates inside ```mermaid ... ``` blocks.

Usage:
  python3 fix-mermaid-dots.py <root_directory>

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
            # Remove dot after digit in labels: "1. Something" → "1 Something"
            old = line
            line = re.sub(r'(\d+)\.\s', r'\1 ', line)
            if line != old:
                lines[i] = line
                changed = True
                count += 1

        if changed:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write('\n'.join(lines))
            print(f'Fixed: {os.path.basename(path)}')

print(f'\nTotal: {count} dots removed')
