#!/usr/bin/env python3
"""Patch resume.tex: Times New Roman font, disable CJK/ctex for English-only resume.

Called by build_resume.sh after yamlresume generates resume.tex.
Handles two issues with the Jake template on Windows/MiKTeX:
1. Linux Libertine font not installed → replace with Times New Roman
2. ctex package requires Chinese fonts (SimHei) not installed → comment out

Run from the directory containing resume.tex, OR pass the tex file path as arg.
"""
import re
import sys
import os

tex_file = sys.argv[1] if len(sys.argv) > 1 else 'resume.tex'

# Handle being called from scripts/ subdirectory
if not os.path.exists(tex_file):
    tex_file = os.path.join(os.path.dirname(__file__), '..', tex_file)

with open(tex_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Disable Linux Libertine checks (font not installed)
content = content.replace(
    r'\IfFontExistsTF{Linux Libertine}',
    r'\IfFontExistsTF{DISABLED}'
)
content = content.replace(
    r'\IfFontExistsTF{Linux Libertine O}',
    r'\IfFontExistsTF{DISABLED}'
)

# Add Times New Roman after fontspec if not already there
if r'\setmainfont{Times New Roman}' not in content:
    content = content.replace(
        r'\usepackage{fontspec}',
        r'\usepackage{fontspec}' + '\n' + r'\setmainfont{Times New Roman}'
    )

# Comment out ctex and CJK lines (not needed for English-only resume)
lines = content.split('\n')
patched = []
for line in lines:
    stripped = line.strip()
    if stripped.startswith(r'\usepackage[UTF8') and 'ctex' in stripped:
        patched.append('% ' + line)
    elif stripped.startswith(r'\setCJKmainfont'):
        patched.append('% ' + line)
    elif stripped.startswith(r'\setCJKsansfont'):
        patched.append('% ' + line)
    else:
        patched.append(line)

with open(tex_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(patched))

print('Patched: fonts -> Times New Roman, CJK disabled')
