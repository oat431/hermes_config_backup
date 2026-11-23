---
name: vault-note-cleanup
description: "Use when cleaning up a note or vault to house style."
version: 1.1.0
author: Panomete (journey-writer)
license: MIT
category: note-taking
metadata:
  hermes:
    tags: [obsidian, cleanup, em-dash, humanizer, mermaid]
    related_skills: [humanizer, swe-knowledge-vault-refine, obsidian-vault-maintenance, mermaid-render-validation]
---

# Vault note cleanup

Standard sequence for Panomete's "clean up this note" requests. He says "clean up" and expects all of
it: AI tells removed, em dashes gone, links resolving, diagrams themed, evidence attached.

## When to Use

- "clean up this note", "clean this folder", "de-AI my notes", "remove the em dashes"
- Any request to bring an existing Obsidian folder up to house style

## Step 0a: fix the scope in one line

A folder path is not consent for a whole-folder pass. When the named path is a directory, say which
of these you are doing before auditing anything: the single root/index note, the folder's hub notes,
or every note inside. Report the result as three lines — what changed, what was deliberately left,
the one open question — and get a yes before any wave. A next-step menu at the end of a long report
reads as a scope proposal the user has to decode.

## Step 0: humanizer audit first (always)

Load `humanizer` and run its 34-pattern audit before touching punctuation. Use that skill's
folder-audit reference: measure, report, then edit. Do not restructure prose or "improve"
sentences; a cleanup keeps the author's words and changes punctuation only.

A pattern hit is a suspect, not a finding. Check every hit against the document's own conventions:

- OK, cross and warning emojis are Panomete's correct/incorrect/warning markers, not AI decoration.
- Title Case headings used consistently from file 01 are house style, not the marketing-heading tell.
- "emphasizes", "highlights" describing what a grammar point does is domain vocabulary.
- Teaching notes are full of deliberate wrong examples: leave them wrong on purpose.

Report what you are leaving alone and why, then proceed.

## Step 1: em-dash removal (the deterministic part)

The per-sentence decision table lives in the `humanizer` skill's em-dash-removal reference. Apply it
with `humanizer/scripts/emdash_apply.py`, never a hand-written replacer:

```
python emdash_apply.py "<root>" plan.json --dry   # validate every line first
python emdash_apply.py "<root>" plan.json         # write
```

Plan = `{relpath: {lineno: [token per dash on that line, left to right]}}`. Tokens: `:` gloss or
label, `,` aside, `;` independent clauses, `P` sentence break + capitalise, `SP` same when the left
side already ends in `? ! ...` (a `P` there yields `about?.`), `(`/`),` parenthesis pair, `)` bare
closing paren when a pair mid-sentence would end `),` and leave a comma splice, `BOLD`
colon inside `**Label**`, `N/A` empty table cell, `KEEP` glyph being taught, `...` spoken self-repair.

- Survey first: file count, em count, en count, fenced-block dashes, frontmatter dashes, mermaid
  count, EOL mix. The scan decides the plan; do not trust a previous session's totals, and re-count
  each residue class (frontmatter, fenced, inline backticks) in your own scan. A handoff's residue
  breakdown drifts from disk: 18 frontmatter + 4 fenced in the doc measured 24 + 3 on the notes.
- En dashes stay: ranges (`Ch 12-13`) and compounds are correct typography. Where a dash is a domain
  symbol (quadrant label, decision-table don't-care), use an en dash rather than a colon so the em
  census stays 0 without breaking the syntax.
- Leave alone: YAML frontmatter quoting a standard, dashes inside fences and inline code, dashes
  that are the glyph under discussion.
- **Line art is not punctuation.** Interval tables draw with the dash itself (`| ○——○ |`, `●——●`) and
  a backticked `—` can mean a flat line in a slope table. Count these separately, report the exact
  lines, and ask before converting: they are the one legitimate reason to finish a pass with a
  nonzero census.
- **Numbered headings that already contain a colon.** `# 01 — Role Snapshot: "AI Engineer"` becomes a
  double colon if you use `:`. Use a middot for numbered series (`# 01 · Role Snapshot: "AI Engineer"`)
  and keep `:` for unnumbered headings; ask, since this is taste, not correctness.
- **Dashes inside quoted questions** need their own rule, or you get `quality: and specifically in Thai?`.
  Use a comma when the quoted clause continues the same question, a colon when a list follows, and a
  colon when the left side is a statement and the right side is a question ("…too: which of these is in
  my orbit?"). Never `P`/`SP` there: a question that ends in `?` must not gain a period.
- **The same holds for any other quoted span, including dialogue.** A dash inside someone's spoken
  sentence continues that sentence: `She says, "I don't have time to rest — the exam is in four months."`
  takes a comma, never a colon, and never `P`/`SP` (the quoted sentence does not end at the dash).
- **A `;` needs two independent clauses, one on each side.** A dash that closes a comma-opened aside
  leaves a subordinate fragment on its left, so the semicolon strands the main clause: `In Thai
  secondary schools, where pressure peaks during adolescence — this domain is the backbone` must take
  `,`. If the left segment opens with `where`/`when`/`although`/`because`/`while`, or starts with a
  preposition whose object is the whole clause, use `,`. Test: swap a period in; if the left half
  cannot stand alone, `;` is wrong.
- **Count the colon budget of the WHOLE line, not just the segment before the dash.** The chooser
  sees only the text between the previous dash and the current one, so a colon anywhere earlier in
  the line is invisible to it and it adds a second: `The promise is not recited and forgotten —
  each clause maps to a practice: loyalty…` becomes `forgotten: … practice: loyalty…`. Read the
  rendered line and take `,` whenever the finished line would carry two colons. Same trap at the
  line end: `Bangkok exemplifies the pattern — one city dominates the hierarchy:` already terminates
  in `:`, so the dash takes `,`.
- **A dash-opened aside that a second dash closes takes `,` on both sides.** The closing dash sits
  between two non-colon segments (`…democracy as practice — campaigns, votes, mandates — years
  before they vote`), so the default hands it `:` and the aside dangles off a colon. The pair of
  dashes is the aside's only delimiter; restore both to commas.
- **Assign tokens per dash, never per line.** A line whose first segment is a bold label still has
  ordinary dashes further on; a line-wide `["BOLD"] * n` makes the tool assert `BOLD needs trailing **`.
  Reserve `BOLD` for a segment that ends with `**` AND whose bold span sits in label position (start
  of line, start of table cell, after `- ` / `N.`, or after sentence-ending punctuation). Bold in the
  middle of a sentence is emphasis, so give it `,` or `;` and keep the colon out of the bold.
- **When the whole census is one category, skip the plan and use two anchored regexes.** A folder where
  every dash sits in an H1 (23 files, 45 dashes, `# NN — Title — Thai gloss`) needs no token plan:
  `^(#{1,6}\s+)(\d+)\s*—\s*` → `\1\2 · ` and then `^(#{1,6}\s+[^\n]*?)\s*—\s+` → `\1: `. Sort
  the categories before planning; a single-category census makes the mechanical path provably complete,
  and the plan's per-line assertions buy nothing.
- **Some shapes the token tool cannot express; convert those with a targeted regex pass.** A quoted
  epigraph with an attribution, `> *"The cell is the basic unit of life."* — Theodor Schwann`, needs a
  closing parenthesis with no comma, and the token set has none. Panomete's preferred rendering is
  `> *"quote"* (Author, year)`: match `^(>\s*\*".*"\*)\s*—\s*(.+)$` — the `.*"` is greedy on purpose,
  so on a line that carries an original, its translation and a source (`> *"thai"* — *"english"* — Ramkhamhaeng
  Inscription`) the last quoted span is captured as the quote, the attribution becomes `(Source)`, and the
  interior original→translation dash is left for the normal plan to turn into `:`. A non-greedy `.*?"` there
  captures the translation as the attribution and strands an em dash inside the parentheses. Fold a trailing
  `(1972)` into `(Author, 1972)`, and keep those lines OUT of the plan. When such a line also carries a dash inside
  the quote, convert the interior dashes with the normal rules first, then wrap the attribution.
- **A label-quote closes its italics at the line end, so a plain colon lands inside the emphasis.**
  `> *"ลูกเสือมีเกียรติเชื่อถือได้" — Scout Law 1*` has a single `*` pair wrapping quote AND label, so
  `:` yields `*"…": Scout Law 1*`. Move the closing marker ahead of the separator instead: match
  `^(>\s*\*")(.+)"[ \t]*—[ \t]*(.+?)\*[ \t]*$` and rebuild as group1 + group2 + `"*: ` + group3,
  giving `> *"…"*: Scout Law 1`. This is word-identical (asterisks are not words), so word-equality
  still passes, and the label stays legible outside the emphasis.
- **When a dash sits inside a bold label, replace the padded span, not the glyph.** A date-label line
  `- **July 1 — National Scout Day** — Schools hold parades` needs a middot for the inner dash, but
  substituting ` · ` for the bare `—` leaves the original spaces in place and yields
  `July 1  ·  National`. Consume `\s*—\s*` and write ` · `, then grep the file for double spaces:
  the stray space is invisible in a diff and only shows in the rendered note.
- **Rebuild the plan after any edit that changes a dash count.** A regex pre-pass (for example
  `— and` to `, and`) leaves an older plan asserting the old count on that line, and the tool aborts
  the whole batch at its `dash count` assertion. Regenerate the plan from the current text, not from
  the state you scanned an hour ago.
- Review the `NEW` text at a surface that scales with the job. Under about 200 dashes, read every
  line. Above that, read every line carrying two or more dashes, every line where the rule chose `;`
  or `BOLD`, every line whose right side starts with a capital (a missed sentence break), and a random
  sample of about 20 single-dash lines. Multi-dash lines are where a line-wide rule misfires, and the
  random sample is what catches a rule that is wrong across a whole category. Mechanical checks catch
  `::`, `,,`, `?.` and lowercase after a period; only reading catches a line that now stumbles.
  Pull the samples by searching their text, not by line number: an injected `%%{init}%%` shifts every
  later index, so `L[n-1]` prints a blank line and reads as a paragraph that went missing.

## Step 2: links

Resolve links the way Obsidian does, not the way a filesystem does: vault-root path first, then a
unique basename. Two rules a lenient resolver hides:

- `[[../x]]` never resolves. Obsidian wikilinks are not filesystem paths, so a resolver that walks
  ancestors passes a link that is dead in the app. Treat every `../` link as broken; rewrite it to a
  vault-root path.
- A basename fallback is valid only when that basename is unique in the vault. Hub names repeat by
  design (`00_ภาพรวม`, `00_overview`, `index`), so every bare link to them is ambiguous. Count stems
  with `collections.Counter` first and path-qualify every link whose stem repeats.
- **A partial path can be just as ambiguous as a bare name.** When two notes share a trail such as
  `Cheat_Sheet/00_Index`, `[[Cheat_Sheet/00_Index]]` still matches both. Write the full vault-relative
  path (`[[Science/Cheat_Sheet/00_Index|00_Index]]`) and keep the alias so the rendered text is unchanged.
- **Dead cross-vault references are reported, not invented.** A link whose target exists nowhere in
  the vault and names a sibling knowledge area (`../../Advance/biology/04_Water_Properties`) is a
  forward reference to a vault that is not here. Leave it, list it in the report by target name, and
  let the user decide; never repoint it at a similarly named note or delete it. The same applies to a
  hub link that every note in a folder repeats (`[[00_overview|… Overview (BOK)]]`) when no such file
  exists anywhere: that is an index nobody wrote yet. Do not delete it just to zero the broken count.

Strip the escaped pipe before matching. Keep aliases verbatim. Deep detail:
`swe-knowledge-vault-refine`.

## Step 3: diagrams

Inject the brand `%%{init}%%` as the first line of every mermaid block that lacks one, remap ad-hoc
`style` hexes to the 15-token palette, then render every block with mermaid-cli. Palette, per-type
variable sets and remap rules live in `swe-knowledge-vault-refine` (Panomete mermaid theme section).

Syntax traps that only a render catches:

- A colon or parentheses inside an unquoted quadrantChart label is a parse error. Quoting fixes it:
  `quadrant-1 "Q I (+,+)"` renders on the current mermaid-cli. An en dash is only needed when the
  label must stay unquoted.
- `subgraph Some Name` with spaces becomes an illegal edge target. Give it an id: `subgraph SN["Some Name"]`.
- Unquoted parentheses in node text break the parser: `A[X (e.g. Y)]` becomes `A["X (e.g. Y)"]`.
- **A block that opens with `---` (mermaid frontmatter, the `gitGraph` shape) must receive its init
  AFTER the closing `---`. Inserting it before the frontmatter breaks the diagram.**
- Replacing a legacy `%%{init: {'theme':'dark'}}%%` is not inserting: strip every existing init line in
  the block first, then add the brand one, or the diagram runs two directives and the last one wins.
- gantt honours `taskBkgColor`, `taskBorderColor` and `gridColor`, but paints `sectionBkgColor` and
  `altSectionBkgColor` as low-opacity washes, so the section bands stay pale. Do not chase it; note
  it and move on, the bars and labels are what carry the theme.
- `style X fill:#1FB854#000000` is a hex glued to a hex: an earlier automated pass ate the `,color:`
  separator. Repair to `fill:#1FB854,color:#000000`; until then the fill is invalid and the diagram
  only looks themed because the init supplies the rest.
- Extract render inputs from the edited note and assert every `.mmd` starts with the `%%{init` line
  before rendering. A body rebuilt without the injected line renders a diagram the note does not
  contain, so a passing render proves nothing about the page.

Run this as its own pass, never interleaved with a prose-editing wave: two writers on the same file
region overwrite silently. Tell any prose agent the fenced blocks are off-limits.

## Step 4: verification (do not skip, do not trust the tool's success line)

1. Em-dash count is 0 (or exactly the KEEP/frontmatter residue you reported).
2. Line counts identical per file; every changed line contained a dash before the edit.
3. Content-word equality against the backup, excluding `N/A`, parenthesis pairs and bold-label colons,
   computed from `difflib.SequenceMatcher` opcodes, never by zipping the two line lists. One inserted
   init line shifts every later pair and reports hundreds of phantom word changes; allowlist inserted
   lines that are `%%{init` or blank.
4. Defect set, not absolute: `::`, `,,`, `,.`, `;.`, `?.`, space before punctuation. Compare new vs
   old so pre-existing ellipses and ASCII art do not read as regressions.
5. Fence parity: every mermaid block has exactly one init, zero unterminated blocks.
6. Every diagram renders (exit code 0); count PNGs against blocks.
7. EOL style matches the backup: read both with `newline=""` and classify each file (CRLF when the
   CRLF count equals the line count, LF when zero, otherwise mixed). Comparing raw CRLF counts
   false-flags every CRLF file that gained an inserted line.
8. Run `scripts/verify_cleanup.py <root> <baseline_dir>` for gates 1-4 and 7 in one pass; nonzero exit
   means at least one gate failed and it prints the file plus the offending line.

## Pitfalls

- **`Path.write_text` / `read_text` normalise line endings.** In a mixed vault this rewrites every
  LF file as CRLF. Read and write with `newline=""` and assert the CRLF count is unchanged.
- **`emdash_apply.py` refuses any line inside frontmatter** (`assert n > fm`). YAML keys such as
  `source: "Book — Author"` must be edited outside the tool, one line at a time. Inside a QUOTED
  scalar `: ` is safe (`component: "กิจกรรมแนะแนว — การแนะแนวการศึกษา"` → `component: "กิจกรรมแนะแนว: …"`);
  in an UNQUOTED one a colon opens a nested mapping and breaks the frontmatter, so use a comma or
  rewrite the value instead.
- **Never put `\s*` before `$` in a multiline regex.** `^(> \*.*?\*)\s*—\s*(.+?)\s*$` swallowed the
  newline and merged paragraphs in one file, changing its line count. Use `[ \t]*` and rewrite only
  the single target line.
- **A file restored with `read()` + `write(newline="")` loses CRLF.** After any restore, re-check the
  CRLF count against the backup; the universal-newline read strips `\r` and the write does not put it
  back.
- **Take the snapshot before the first write, even for a six-file folder.** If you miss it, `git show
  HEAD:<path>` is a valid baseline only for tracked files; `git ls-files <path>` tells you in one
  call whether the note has any history. An untracked note has no baseline at all, so word-equality
  becomes "guaranteed by construction" rather than proven — say that out loud instead of implying a
  check you could not run.
- **Check `git remote -v` and `git check-ignore` before editing a personal folder.** A note that
  looks private (body metrics, food logs) can sit in a repo that is published to GitHub; flag it once,
  then edit as asked.
- **A patched script stays cached in the execute_code kernel.** Fixing `emdash_apply.py` and then
  importing it in the same session runs the pre-fix module and silently reintroduces the bug you just
  removed. After editing a script, `importlib.reload(module)` or run it as a subprocess
  (`python script.py ...`) so the bytes on disk are what execute.
- **The `patch` tool interprets escape sequences in CRLF files.** A patch containing a literal
  backslash-r backslash-n lands as a real newline and breaks the syntax. In Python source use
  `chr(13)` / `chr(10)`, or write through scratch and `cp` it.
- **`write_file` refuses files read with offset/limit or patched without a full read** (stale-read
  guard). Write to scratch, then `cp` to the target.
- **On Windows the bun-installed renderer is `mmdc.exe`, and MSYS paths are not translated for it.**
  Pass `C:/...`-style paths for `-i`, `-o` and `-p`; a `/c/...` path fails with "configuration file
  doesn't exist" even though bash resolves it.
- **Check `git log` before offering to commit.** These vaults have an auto-backup job that commits
  everything periodically; the work may already be in history under `vault backup: <date>`.
- **A git directory is not a rollback.** `git rev-parse --is-inside-work-tree` can return true while
  the repository has zero commits, and a repo rooted above the vault may not track the folder at
  all. Run `git log -1 -- <path>` and require a real commit before bulk edits; if there is none, copy
  the folder to a dated backup outside the vault — never inside it, where duplicate basenames would
  make every wikilink ambiguous.
- **Scratch backups are pruned after about 24h idle.** Take a fresh one at the start; a handoff's
  backup path may already be gone. Durable rollback is git HEAD.
- **The bun-installed mermaid toolchain is pruned with the same cache.** Its signature is every block
  failing at once with `mmdc.exe: No such file or directory`: an instant, uniform failure is a missing
  renderer, never a batch of diagram bugs. Reinstall into a fresh dir and test ONE block before
  launching the batch: `PUPPETEER_SKIP_DOWNLOAD=true bun add @mermaid-js/mermaid-cli puppeteer` (~45 s)
  plus a `puppeteer.json` pointing `executablePath` at Edge with `--no-sandbox --disable-gpu`. Keep one
  shared tool dir and call it with `C:/...` paths; a per-folder copy is pruned just as fast.
- **Never restore a folder wholesale from a pre-edit backup mid-run**: it silently reverts the
  mechanical pass and any injected diagram inits. Restore single files only.
- **`---` in the body is not frontmatter.** `emdash_apply.py`'s `frontmatter_end()` once returned the
  first `---` at any line > 1, so a note that opens with `# Title` and has a horizontal rule at line 7
  made every line above the rule look like frontmatter and the tool refused the whole plan
  (`AssertionError: line inside frontmatter`). The guard now requires line 1 itself to be `---`.
  Symptom to recognise: the refusal names a *low* line number (1, 3, 11) in a note whose first line
  is a heading.
- **Unquoted YAML `title: Foo — Bar` cannot become `title: Foo: Bar`.** A colon followed by a space
  ends the scalar and the note stops parsing; Obsidian then shows no properties at all. Quote the
  value when converting: `title: "Foo: Bar"`. Only quoted scalars take the colon safely.
- **Technical vaults: dashes inside code fences are content, not prose.** In homelab/runbook notes the
  survivors are shell comments (`# NOT \`down -v\` — that would DELETE the volumes`), config comments
  (`KC_CACHE: local  # ... — single node only`), captured command output and ASCII diagrams. Count
  them, verify fence text is byte-identical to the backup (`fences(before) == fences(after)`), and
  report them as intentional survivors — never as a failure to finish.
- **At 600+ lines, simulate the render and flag defects before writing.** Build the plan, apply every
  token in memory, then diff the *result* against the source for `: and|: but|: so`, `::`, `,,`,
  space-before-punct and "two colons where there were none". That surfaces the handful of lines
  needing an override without reading all 600. Expect false positives: a gloss such as
  `Route rules: which domain goes where` is correct even though `which` follows the colon.
  `python scripts/preview_plan.py <root> <plan.json>` runs exactly this: it renders every planned
  line, prints only the suspects with OLD vs NEW, exits nonzero when anything is flagged, and
  `--all` adds the clean multi-dash lines for a final skim. Run it before the applier, fix the real
  flags with per-line overrides, re-run until it exits 0, then write.

## Handoffs

Long jobs get a handoff pack in `F:\obsidian_note\.backups\<job>-<date>\`: `handoff.md`, `inventory.md`
(every line, OLD vs NEW, tagged AUTO/REVIEW), `plan_auto.json`, `plan_review.json`, `scan_raw.json`,
plus before/after snapshots of the folder. Write one when stopping mid-job so the next session can
continue without re-scanning, and read it before re-deriving anything.
