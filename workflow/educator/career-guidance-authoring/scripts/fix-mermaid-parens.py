"""
fix-mermaid-parens.py — Replace parentheses inside Mermaid node labels with HTML entities.

Mermaid uses () for round-rectangle node shapes, so literal ( and ) inside 
["Label (text)"] break the parser, producing "unsupported markdown: list" errors.

Fix: ( → &#40;  and  ) → &#41;
These HTML entities render identically but don't confuse Mermaid.

Usage:
  python3 fix-mermaid-parens.py <root_directory>
  
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
            if in_mermaid and '(' in line and '[' in line:
                old = line
                # Fix ["..."] labels
                line = re.sub(
                    r'\["([^"]*?)"\]',
                    lambda m: '["' + m.group(1).replace('(', '&#40;').replace(')', '&#41;') + '"]',
                    line
                )
                if line != old:
                    lines[i] = line
                    changed = True
                    count += 1
        
        if changed:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write('\n'.join(lines))
            print(f'Fixed {count} issues: {os.path.basename(path)}')

print(f'\nTotal: {count} parentheses fixed')
