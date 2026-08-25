# YAMLResume Build Workflow

End-to-end pipeline for generating ATS-compatible PDF resumes using [yamlresume](https://yamlresume.dev).

## Setup

```bash
npm install -g yamlresume   # or use npx
```

**LaTeX dependency:** yamlresume generates `.tex` files that require `xelatex` or `tectonic` to compile to PDF.

### Windows: MiKTeX + xelatex

```powershell
winget install MiKTeX.MiKTeX
# Then in MiKTeX Console → Packages → search "xetex" → Install
# Enable auto-install to avoid GUI prompts during builds:
initexmf --set-config-value="[MPM]AutoInstall=1"
```

**Restart terminal/gateway** after MiKTeX install so PATH picks up `xelatex.exe`.

### Required MiKTeX Packages

Auto-install handles most, but pre-install these to avoid 30-second timeout hits:
```bash
mpm --install=fontawesome5
mpm --install=fontawesome7
```

## Core Commands

| Command | Purpose |
|---------|---------|
| `npx yamlresume new resume.yml` | Scaffold from template with correct schema |
| `npx yamlresume validate resume.yml` | Check against YAMLResume JSON schema |
| `npx yamlresume build resume.yml` | Build all configured output formats (PDF, DOCX, HTML, MD) |
| `npx yamlresume dev resume.yml` | Watch mode — rebuild on file changes |
| `npx yamlresume templates list` | Show available templates per engine |

## Available Templates

| Template | Engine | Style |
|----------|--------|-------|
| `jake` | LaTeX | Simple, developer-focused (recommended for SWE) |
| `moderncv-banking` | LaTeX | Professional, banking style |
| `moderncv-casual` | LaTeX | ModernCV casual variant |
| `moderncv-classic` | LaTeX | ModernCV classic variant |
| `calm` | HTML + DOCX | Clean, minimalist |
| `vscode` | HTML | Dark theme, developer aesthetic |

## Schema Constraints (Validation Rules)

These cause `yamlresume validate` to fail or warn:

| Field | Constraint | Fix |
|-------|-----------|-----|
| `basics.summary` | Max 1024 characters | Condense bullet points, remove filler |
| `basics.phone` | Must be valid phone format | Use E.164: `+66836306462` (no spaces/dashes) |
| `certificates[].date` | Must be parseable date | Use `"Jan 2024"` not `"2024"` |
| `projects[].startDate/endDate` | Must be parseable dates | Use `"Jan 2024"` not `"2024"` |
| `education[].score` | String, not number | Use `"3.58"` not `3.58` |
| `languages[].fluency` | Must be one of: Elementary Proficiency, Limited Working Proficiency, Minimum Professional Proficiency, Full Professional Proficiency, Native or Bilingual Proficiency | Match exact string |
| `skills[].level` | Must be one of: Novice, Beginner, Intermediate, Advanced, Expert, Master | Match exact string |

### Valid Fluency Values

```yaml
- "Elementary Proficiency"
- "Limited Working Proficiency"
- "Minimum Professional Proficiency"
- "Minimum Professional Proficiency"     # ← B2 maps here (= LinkedIn's "Professional Working")
- "Full Professional Proficiency"     # ← C1+ only; never use for B2 certs
- "Native or Bilingual Proficiency"   # ← Native Thai maps here
```

## Known LaTeX Build Issues on Windows

### 1. Font: Linux Libertine not found

The Jake template tries Linux Libertine, which isn't installed by default.

**Fix:** After `npx yamlresume build` generates `resume.tex`, patch it before running xelatex:

```latex
% Replace the \IfFontExistsTF{Linux Libertine} blocks with:
\setmainfont{Times New Roman}
```

### 2. CJK fonts (SimHei, Noto Serif CJK SC) not found

The template includes `\usepackage{ctex}` which requires Chinese fonts. For English-only resumes, strip the entire ctex block.

**Fix:** Remove from `resume.tex`:
```latex
\usepackage[UTF8, heading=false, punct=kaiming, scheme=plain, space=auto]{ctex}
\IfFontExistsTF{Noto Serif CJK SC}{...}{}
\IfFontExistsTF{Noto Sans CJK SC}{...}{}
```

### 3. yamlresume 30-second internal timeout

yamlresume imposes a 30-second timeout on the xelatex invocation. If MiKTeX needs to download packages, it will timeout even though xelatex would succeed if given more time.

**Workaround:** Run xelatex directly with a longer timeout:
```bash
cd <project-dir>
xelatex -interaction=nonstopmode resume.tex    # pass 1: generates PDF + aux files
xelatex -interaction=nonstopmode resume.tex    # pass 2: resolves cross-references
```

### 4. MiKTeX GUI dialog blocks headless builds

MiKTeX tries to pop up a Qt dialog to ask about installing missing packages, which fails from non-interactive shells.

**Fix:** Enable auto-install before building:
```bash
initexmf --set-config-value="[MPM]AutoInstall=1"
```

## Recommended Build Sequence

The cleanest approach uses `--no-pdf --no-validate` to generate only `.tex`, then patches and compiles manually. This avoids yamlresume's 30-second xelatex timeout entirely.

**Use the automated build script** (`scripts/build_resume.sh` + `scripts/patch_tex.py`) which handles all steps:

```bash
bash scripts/build_resume.sh    # from the resume project directory
```

**Manual steps (if script unavailable):**

```bash
# 1. Generate .tex from YAML (no PDF compilation, no validation timeout)
npx yamlresume build resume.yml --no-pdf --no-validate

# 2. Patch fonts (see Known Issues below, or use scripts/patch_tex.py)
python3 scripts/patch_tex.py

# 3. Build PDF directly (2 passes for cross-references)
xelatex -interaction=nonstopmode resume.tex
xelatex -interaction=nonstopmode resume.tex

# 4. Open result — resume.pdf is in the same directory
```

## Workflow for Resume Updates

1. Edit `resume.yml` (your source of truth)
2. `npx yamlresume validate resume.yml` — catch schema errors early
3. Run `bash scripts/build_resume.sh` — handles generation, patching, and compilation
4. Review `resume.pdf`

## ATS Filename Convention

ResumeWorded Pro flags `resume.pdf` as a readability issue — the filename should
contain the full name so hiring managers can track it in their ATS.

**Fix:** after building, copy to `FirstName-LastName-Resume.pdf`:

```bash
cp resume.pdf "Sahachan-Tippimwong-Resume.pdf"
```

Upload the NAMED file to ATS scanners and job portals, not the generic one.
The `build_resume.sh` script includes this copy step — make sure new resume
projects keep it.

## Section Reordering (Mid-Level Candidates)

yamlresume's Jake template renders sections in YAML order with Education before
Work — wrong for anyone with 3+ years experience. ATS and recruiters expect
Experience-first. `patch_tex.py` reorders to:

```
Summary → Work → Education → Skills → Languages
```

Verify after rebuild that the PDF section order matches (see diagnostic script
in `references/ats-optimization.md`).

## Version Control

```bash
git init
echo "resume.aux" >> .gitignore
echo "resume.log" >> .gitignore
echo "resume.out" >> .gitignore
git add resume.yml resume.tex resume.pdf
git commit -m "Initial resume"
```

Track `resume.yml` (source), `resume.tex` (build artifact), and `resume.pdf` (output). Rebuild `.tex` and `.pdf` are regenerable from `.yml`.
