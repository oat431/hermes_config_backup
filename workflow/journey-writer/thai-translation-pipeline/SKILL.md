---
name: thai-translation-pipeline
description: "Translate or refine Thai prose at scale."
version: 1.1.0
author: Panomete + Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [thai, translation, kien-thai, kode-thai, subagents, audit, obsidian]
    related_skills: [kien-thai, kode-thai, obsidian, mermaid-render-validation]
---

# Thai Translation Pipeline

Translate English prose into Thai that reads native, or refine Thai prose that already exists (Mode B). `kien-thai` owns the rules and `kode-thai` owns the convergence loop; this skill owns the orchestration around them: sizing, decision-locking, chunking, calibration, and mechanical triage.

**Both rule skills are external** (installed from `chakrit/kien-thai`, under active upstream iteration). Never edit their files to make an output come out right; local policy lives here and upstream stays re-syncable. `kien-thai` loads in full — `SKILL.md` plus all eight references — for both drafting and auditing.

## When to use

- More than one paragraph, more than one file, or a whole vault to translate into Thai.
- Book-note sets, docs pages, marketing long-form, essays, translation of existing notes.
- Refining Thai prose that already exists at scale (Mode B below): teaching notes, documentation, a whole vault section.
- Not for single words, UI strings, code identifiers, chat replies (kien-thai counter-triggers), or Thai→English.

## Step 1 — Size the job before promising a shape

Measure, do not estimate. System Python usually has no `pip` and PEP 668 blocks global installs, so use a throwaway venv:

```sh
cd "$TMPDIR" && uv venv tokscratch --quiet
uv pip install --python tokscratch/Scripts/python.exe tiktoken --quiet   # POSIX: tokscratch/bin/python
```

Then count both sides of the equation: the rule bundle and the source corpus.

| Measured reference | Tokens (cl100k) |
| --- | --- |
| `kien-thai` full bundle (SKILL.md + 8 references) | ~43k |
| A ~2,000-word book note | ~1.6k source → ~3k Thai output |

`kode-thai` reloads the full bundle on **every** audit pass, so the cost is `43k + source + output` per agent pass, not once. A whole corpus in one context is not a close call; the working unit is **2–3 files per subagent**. State the total token estimate to the user before launching a wave.

## Step 2 — Lock five decisions before any drafting

Subagents cannot ask questions. An unlocked decision lands in every file at once. Ask all five in one clarify call; offer the defaults below as the recommended options.

| Decision | Default | Why |
| --- | --- | --- |
| Register | Register 5 Academic for book/non-fiction prose; Explainer for docs | `register.md` routes "book translations of confident essayists" to Academic |
| Quotes | English blockquote kept verbatim, Thai rendering beneath as `> แปลว่า ...`; inline quotes translated inline with the English in parentheses | keeps citation and page refs intact while staying readable |
| Layout | mirror folder `<Source>_TH/`, identical filenames, path-qualified wikilinks with a Thai alias | duplicate basenames make Obsidian wikilinks ambiguous |
| Terms | Two tiers: **Tier A** author coinages stay English in Latin script (`imagined order`, `luxury trap`, the revolution names, `full/partial script`); **Tier B** settled domain nouns take Thai (`science`→วิทยาศาสตร์, `empire`→จักรวรรดิ, `capitalism`→ทุนนิยม). Headings, H1 titles and link labels keep their locked Thai either way. Full table + drift check: `references/term-policy.md` | "Concepts in English" is not a testable boundary: parallel translators split 44/20 on `empire` because each decided for itself which nouns counted as concepts |
| Start | one calibration file end-to-end, user's ear, then fan out | catches a systemic mistake for one file's cost |

Also state the invariants you will **not** touch: YAML tags, source citation lines, PDF/page refs, mermaid blocks, code blocks. Translate headings and body only.

## Step 3 — Calibrate one file in the main session

Draft it yourself (not via subagent), run the full `kode-thai` loop to `CLEAN`, and present: the file path, the pass log with the rule slug behind each fix, and the judgment calls the user should overrule. Do not fan out until that file is approved — the calibration is the quality gate for the whole run.

## Step 4 — Fan out the draft wave

One subagent per 2–3 files. Each task context must carry: absolute source paths, target paths, the locked policy (register, term list, quote layout, link form), and an instruction to `skill_view('kien-thai')` plus all eight references before drafting. Require the child to write the file itself and report the path. Then read at least one written file yourself; a child's "written successfully" is intent, not proof.

Resolve the vault root before a single path-qualified link is written: it is the directory holding `.obsidian`, not the note's own folder. Obsidian resolves `[[path/note]]` from the vault root, so a mirror folder nested under `Book/` needs `[[Book/<Source>_TH/note|label]]`; a bare `[[<Source>_TH/note]]` is a dead link. Nothing else in the pipeline catches this until the audit script runs over all files, so check one link the moment the first translation lands.

## Step 5 — Audit wave with kode-thai

Batch 2–3 files per auditor. Per batch: mechanical pre-check, then read end-to-end, fix, re-read, repeat; stop only on a pass with zero issues.

```sh
python3 scripts/audit_thai_prose.py path/to/file.md [more.md ...]
```

The script is triage, not verdict. Gates: forbidden phrases, ซึ่ง/โดย/ดังนั้น budget (≤1 each per paragraph), ถูก/โดน, ทำการ/การที่, mid-paragraph periods, em-dash/semicolon, ๆ spacing, ครับ/ค่ะ, dummy มัน, and wikilink targets that do not exist yet.

Then judge each hit in context. Known false positives, each confirmed by inspection:

- `ถูก` inside `ไม่ถูก` (incorrect), `ถูกต้อง` (correct), `ถูกกว่า` / `ถูกลง` (cheaper), `ถูกหวย` / `ถูกล็อตเตอรี่` (winning, idiomatic), and inside a quoted use/mention of the word itself.
- `;` inside the invariant `> **Source:**` line: the stripper drops frontmatter and code fences but not blockquotes, so the citation's semicolon fires on every file that has one.
- `[[path\|label]]` inside markdown tables reports as unresolved; the escaped pipe is vault convention, so strip the trailing backslash before judging.

Thai combining marks make naive substring comparison lie about spelling; compare codepoints before "fixing" a word that already looks right.

## Step 6 — Cross-file consistency QA

Glossary sweep (one rendering per term across all files), wikilink integrity, frontmatter tags untouched, mermaid labels intact, and file count equal to the source folder's count. Report a table of what matched and what did not.

Build the sweep as a per-file × per-term count matrix, not as a read-through. Count with plain substring matching: `\b` never fires around a Latin term embedded in Thai, because Thai letters are word characters, so `\bempire\b` reports zero while the page is full of it. A file whose **body prose** carries two renderings of one term is a defect; headings and link labels are exempt because they hold the locked Thai titles. Detect the split before dispatching auditors and hand each one the corrected rendering — otherwise each auditor resolves the same term its own way and the drift survives the audit wave.

## Mode B — refining existing Thai prose (not translation)

Same orchestration, different contract: the prose already exists, so the job is defect removal, not rewriting. Use it when a set of notes must read better without changing what they teach.

- **Preserve content literally.** Facts, numbers, definitions, quoted verse, language examples, table data and column alignment, heading order, wikilinks, frontmatter, filenames. Put these in every agent context as invariants; an agent told only "refine the prose" will smooth a grammar note's example sentence and destroy the teaching point.
- **Group agents by subject strand, not by file count.** A strand shares terminology and examples; an arbitrary slice does not, and mixed terminology is the defect the audit then has to chase.
- **Fix the link layer yourself, deterministically, before dispatch.** `../` never resolves in a wikilink, duplicate basenames need vault-root paths, and stale targets point at notes that were planned but never written. One script pass over the whole set beats ten agents each inventing a resolution rule mid-file.
- **Theme diagrams in a separate central pass, not through the prose agents.** Scripted init injection is idempotent; prose agents editing prose while another pass rewrites fences is an invisible write conflict. Tell agents the fenced blocks are off-limits.
- **Register:** Explainer for teaching material (particle-free, direct), Academic for literature analysis. Both ban ครับ/ค่ะ in body.
- The calibration gate still applies: refine one note end-to-end and show it before fanning out.

### Reporting a scoped vault pass

Lead with three lines: what changed, what was deliberately left untouched, and the exact options for going further. A next-step menu buried at the end of a long report reads as a scope proposal the user has to decode; when the ask is only "what shell should I do next", say that in one sentence before the menu.

## House style (always on for this user)

- No em-dashes in Thai prose; use commas, colons, or parentheses. En dash is fine for ranges.
- Numbered filenames, English/hyphenated basenames, path-qualified wikilinks for non-unique basenames.
- Confident essayists stay confident: no added ครับ/ค่ะ, no `อาจจะ` where the source asserts.
- Say plainly that `kode-thai` converges to **ruleset-clean**, not native-ear clean. The user's ear is the final gate; never present `CLEAN` as a quality verdict.

## Common pitfalls

1. **Editing kien-thai/kode-thai to force an output.** They are upstream-owned and iterated; edits fork the ruleset and break re-sync. Put local policy in this skill.
2. **Treating kien-thai's `examples.md` as style authority.** Its academic-translation example uses em-dashes and mid-paragraph periods that the same skill's `em-dash-semicolon` and `mid-paragraph-period` rules ban, and that this user's house style forbids. Rules win over examples.
3. **Counting grep hits as an audit.** Thai particles and negation collide (`ถูก`, `ไม่ถูก`), and combining marks break substring checks. Inspect context and codepoints.
4. **Dispatching subagents before policy is locked.** They cannot ask; one wrong register or term decision replicates across every file.
5. **One agent for the whole corpus.** The ~43k bundle reloads per pass and will not fit alongside the source and output. Chunk by file.
6. **Trusting child self-reports.** Read the artifact on disk before calling a wave done, and verify term choices with the count matrix rather than the report — a summary describes intent, and translators do not notice when their own file mixes two renderings of one term.
7. **Producing every file before showing one.** Calibration exists precisely to avoid paying 20× for a systematic mistake.
8. **Believing a child's statement about files outside its assignment.** Children hold a snapshot taken when they started: one auditor reported that a neighbouring chapter still carried Latin `empire` after that chapter's own auditor had already converted it. Re-measure the whole set on disk before repeating any cross-file claim in a report.
9. **Stripping code fences line-by-line when auditing terms.** Skipping lines that begin with ``` removes the delimiters and leaves the fence body behind, so mermaid labels get counted as term drift. Remove whole blocks first, or track fence state — otherwise every diagram looks like six English terms the translator forgot.
10. **Giving a refinement agent creative latitude.** "Refine this note" without an explicit preserve-list licenses rewriting examples, tightening verse, and "fixing" deliberate repetition. Refinement is defect removal against the written rules; anything that changes meaning, data, or an example is out of scope unless the user asked for it.

## Verification checklist

- [ ] Token estimate stated; chunk size justified by measurement
- [ ] Five decisions locked in writing before dispatch
- [ ] Calibration file reached a clean audit pass and user reviewed it
- [ ] Every drafted file exists on disk and was read back at least once
- [ ] Mechanical pre-check run; every hit inspected, not just counted
- [ ] Glossary consistent across files; originals untouched; file count matches
- [ ] `CLEAN` reported as ruleset-clean, with the native-ear caveat

## Support files

- `scripts/audit_thai_prose.py` — mechanical `kode-thai` pre-check over one or more files. Encodes the known false positives (cheap/correct/winning `ถูก`, the Source-line semicolon, table `\|` links) so only real hits reach the auditor; run it once on a known-clean file before trusting its verdict.
- `references/term-policy.md` — the two-tier term ruling, the reasoned boundary test, and the drift-matrix recipe. Load it while locking the Terms decision in Step 2.
