#!/bin/bash
# Resume build script — generates PDF from resume.yml using yamlresume + xelatex
# Handles: font fixes (Linux Libertine → Times New Roman), CJK removal (English-only)
# Place in the resume project directory alongside resume.yml
# Usage: bash scripts/build_resume.sh  (or: bash build.sh from project root)
set -e
cd "$(dirname "$0")/.."  # go to project root (parent of scripts/)

echo "==> Step 1: Generate resume.tex from YAML..."
npx yamlresume build resume.yml --no-pdf --no-validate 2>&1 || true

echo ""
echo "==> Step 2: Patch resume.tex (fix fonts, remove CJK)..."
python3 "$(dirname "$0")/patch_tex.py"

echo ""
echo "==> Step 3: Compile PDF with xelatex (2 passes for cross-refs)..."
xelatex -interaction=nonstopmode resume.tex > /dev/null 2>&1 || true
xelatex -interaction=nonstopmode resume.tex > /dev/null 2>&1 || true

echo ""
echo "==> Done! resume.pdf is ready."
echo "    Location: $(pwd)/resume.pdf"

# Show page count
PAGES=$(grep -oP 'Output written.*\(\d+ pages\)' resume.log | grep -oP '\d+ pages')
if [ -n "$PAGES" ]; then
  echo "    Pages: $PAGES"
else
  echo "    ERROR: PDF not generated. Check resume.log"
fi
