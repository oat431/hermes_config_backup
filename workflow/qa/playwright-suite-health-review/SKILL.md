---
name: playwright-suite-health-review
description: "Use when reviewing an inherited Playwright E2E suite."
version: 1.0.0
author: Hermes Agent (QA)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [qa, playwright, e2e, review, automation, coverage, traceability]
    related_skills: [spec-driven-qa-authoring, dogfood]
---

# Playwright Suite Health Review (pre-improvement assessment)

## When to use

- Inherited or assigned Playwright project: "review the whole project first, then improve it".
- A team asks for coverage numbers, blockers, or a work plan before funding automation work.
- You must produce a review + open questions document set for a client/team handoff.

## Workflow

### 1. Recon (single batched pass)

Read: `package.json`, `playwright.config.ts`, full `tests/` tree (file sizes), `docs/` folders,
`.gitignore`, `git log --format="%ad %h %s" --date=short -25`, `git branch -a`, `git remote -v`.
Note: which fixtures/workbooks the code references vs what exists (grep `path.resolve`,
`captureWorkbookSnapshot`, `process.env`).

### 2. Fresh-clone runability probe (do this BEFORE reading every test)

```bash
pnpm install --frozen-lockfile          # or npm ci
pnpm exec playwright test --list        # WITHOUT .env first — catch module-load throws
```

Check the four classic blockers and record exact error text:
- `.env` missing → module-level `throw` breaks even `--list` (lazy-check fix is a finding).
- Workbook/fixture files referenced at repo root but absent (often gitignored `*.xlsx`).
- Browser: `channel: "chrome"` needs **system** Chrome (check `Program Files`, `Program Files (x86)`,
  AND `%LOCALAPPDATA%\Google\Chrome`); bundled browsers live in `ms-playwright` — compare build
  numbers via `pnpm exec playwright install --dry-run` (stale builds fail launch).
- No README/runbook; `.gitignore` exclusions (`*.md`, `.xlsx`, `.env*`) that block docs.

To keep surveying: create placeholder `.env` (printf, not write_file), copy source-of-truth
fixtures into expected locations. **Document every local change in the review.**

### 3. Test inventory (authoritative counts)

```bash
pnpm exec playwright test --list --reporter=json > testlist.json
```
Parse shape: `suites[].specs[].tests[]`; `test.annotations[].type` (`fixme`/`skip`);
`test.projectName`. Node: strip BOM (`raw.replace(/^\uFEFF/,'')`). Count per project and per file
(active vs fixme). Quote totals like "826 listed / 156 active / 670 fixme".

### 4. Source-of-truth traceability (when a test-case workbook exists)

Read `.xlsx` with exceljs from a scratch script:

```bash
NODE_PATH=<repo>/node_modules node <scratch>/inspect.cjs <workbook.xlsx>
```

- Find header row: cell(col 2) === "TC No." (sources often use header row 14 **or** 15 across revisions).
- Data rows = header+1 upward; effective TC ≈ row − headerRow. Count description-non-empty rows.
- Map spec case IDs (test titles / case arrays) vs workbook rows → represented / active / blocked /
  **unrepresented** (no code at all). Unrepresented tails are usually the newest additions.
- Verify row constants the code hardcodes (e.g. `row: 16` = TC1) against the real workbook —
  wrong mappings are silent data corruption in write-back suites.

### 5. Fixme taxonomy (why blocked)

Classify fixme titles by keyword buckets, **most-specific-first** (order determines result):
known defect → route 404 → workbook Question → multi-user → printer/hardware → time/SLA →
fixture/seed → selectors-unverified → mutating/no-cleanup → other. Report approximate counts;
label as heuristic.

### 6. Compose the review set (4 files pattern)

- `00_review_index.md` — purpose, TL;DR, reading order.
- `01_*_review.md` — snapshot, what works (give credit), verification log (numbered V1…Vn with
  exact results), numbered findings F-01… each with severity + evidence (file:line) + impact +
  recommendation, risk table, phased roadmap (Phase 0 runnability → stabilize → coverage → CI → scale).
- `02_coverage_and_traceability.md` — inventory tables, per-module workbook↔code table,
  fixme taxonomy, wishlist mapping, re-runnable commands.
- `03_questions_for_team.md` — numbered questions grouped by theme, each with why/blocks and an
  inline **Answer:** slot. Mark [BLOCKING] for runnability/data-contract items.

## Pitfalls

- **Credential redaction**: terminal *display* shows `***` even when the file on disk is correct;
  verify with `grep -c '[*][*][*]' file` (0 = clean). Create `.env` via `printf` in terminal, not write_file.
- **write_file re-write guard**: overwriting a scratch file you created earlier this session may be
  refused ("not seen its full current content") — read it first, or use a new filename (suffix v2/v3).
- **Windows paths for native tools**: pass `C:/...` forward-slash paths; `cd /f/...` (bash builtin) is fine
  but `node /f/...` is not. Use `NODE_PATH` for scratch scripts needing repo `node_modules`.
- **Don't run against shared/production UAT** without credentials and permission. Listing-level numbers
  are static facts — label them as such (not pass/fail evidence) in the report.
- **Count carefully, programmatically** — never eyeball per-file counts; dedupe duplicate TC references
  (same TC fixme'd in two project files) before summing.
- If `.gitignore` hides `*.md`, the review docs land untracked — mention it and ask before changing ignore rules.

## Deliverable quality bar

Every number traceable to a command; every finding has file:line evidence; no source file modified
without documentation; questions have answer slots; roadmap ordered by dependency (runnability before coverage).
