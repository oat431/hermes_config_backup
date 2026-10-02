---
name: knowledge-vault-curation
description: Use when auditing/expanding swe-knowledge study vaults.
version: 1.0.0
author: Ops (Hermes Agent)
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [Obsidian, knowledge-vault, audit, note-authoring]
    related_skills: [obsidian]
---

# Knowledge Vault Curation

## When to Use

Trigger on: auditing a study-knowledge vault for thin/missing coverage, expanding curriculum notes with new topics, checking notes for staleness, or renaming vault folders and fixing wikilinks. Also applies when the user says "check the knowledge note" / "is this folder too thin" / "add more topics" for anything under `F:\obsidian_note\swe-knowledge` or `cs-knowledge`.

Audit the user's curriculum/study vaults (`swe-knowledge`, `cs-knowledge` under `F:\obsidian_note`) for coverage gaps and thin notes, then expand them in the vault's house style. The user's standing preference: **audit and report FIRST, write only after explicit approval** — present findings as a prioritized tier plan and use `clarify` to get the go-ahead.

## Vault map

- `F:\obsidian_note\swe-knowledge\` — SE curriculum (career-path, body-of-knowledge, software-engineering-note, computing-foundation-note). `computing-foundation-note\Computing Foundation Overview.md` is the master index with a coverage-status table — update it whenever notes are added.
- `F:\obsidian_note\cs-knowledge\` — CS curriculum; its `CLAUDE.md` and `00_Roadmap.md` reference computing-foundation folder paths — check both when renaming folders.
- `F:\obsidian_note\hermes_config_backup\workflow\...\references\` — HISTORICAL gap-analysis artifacts. Never edit these; they document past state as-is.

## Audit procedure

1. Inventory: `search_files` target=files pattern=`*` on the vault root (full recursive list).
2. Measure depth per folder: one `terminal` call — `find "$d" -name "*.md" -exec cat {} + | wc -w` per folder, plus per-file `wc -l`. Judge thinness against the folder's own baseline, not a global one: cheatsheet-style folders (Networks, OS) run 100–200 lines/note; deep academic folders (Computer Organization, follows Hennessy & Patterson chapter-by-chapter) run 250–660 lines. Additions must match the folder's existing register.
3. Sample-read 3–5 notes across the priority folders (overviews + one deep + one thin) to internalize house style before judging anything.
4. Gap-analyze against the canonical sources the vault itself cites (SWEBOK chapters, textbooks, RFCs) AND against the user's actual work profile (DevOps/SRE: containers, TLS/PKI, Linux internals, BGP, io_uring are daily-bread topics a pure-SWEBOK pass misses).
5. Check notes for STALENESS, not just absence — kernel/tooling facts age (e.g. Linux default scheduler moved CFS → EEVDF in kernel 6.6). A folder can be "complete" per its coverage table and still be outdated.
6. Report as: overall health table (files/words/verdict per folder) → prioritized gap list (🔴 holes first) → what NOT to touch → tiered action plan (Tier 1 glaring holes, Tier 2 depth, Tier 3 fixes/modernization). Then `clarify` for approval.

## Writing new notes — house style (non-negotiable)

- YAML frontmatter with tags as a YAML list (`tags:\n- networking\n- programming\n- <topic>`) matching sibling notes' tag vocabulary.
- H1 matching the filename; one punchy intro sentence on why a working engineer cares; sections separated by `---` rules.
- Dense tables for comparisons, mermaid (sequenceDiagram/flowchart) or ASCII for flows, real bash/java/python command blocks, `## Sources` at the end with ONLY real RFCs/books/man-pages — never invented citations.
- Wikilinks `[[Note Name]]` to existing sibling notes; every new note gets linked FROM its folder's Overview note and the master overview's coverage table.
- Numbered filename prefixes must encode READING ORDER: format `[chapter][order]` — `011`, `012`… inside chapter folder `01`, and `000` for the folder's Overview note so it sorts first. The user requested this scheme (first applied in Computer Networks); Operating Systems and Computer Organization still use older schemes (`01 X`, `01_X`) — offer to align them when touching those folders. Order logically: bottom-up the stack, dependencies before dependents, debugging/tools last.
- Every note's H1 title matches its filename including the numeric prefix; keep them in sync on any rename.
- Windows filename pitfall: avoid `:` in note titles (illegal on NTFS) — use ` - ` instead (e.g. `01 Routing - BGP & OSPF.md`).

For batches of 4+ notes, delegate to parallel subagents: give each child the exact file paths to create, 2 sample files to read first for style, the full style rules above, and a per-note content outline (sections + must-cover facts). Have each child read back its files' first lines to verify; the parent re-verifies line counts and spot-reads — child self-reports of 'file written' are not proof. When batch notes cross-link each other, children will report 'unresolved link' deviations for siblings — expected; resolve after the whole batch lands, don't chase per-child. See `references/delegation-brief-template.md`.

After any expansion, sync the indexes: add new entries to the folder Overview's Topics list (reading order, one-line gloss each), and to the master overview (dated expansion-log section + coverage table). Coverage-table file totals are hard assertions — compute them with `find … -name '*.md' | wc -l`, never arithmetic from memory. Finish with an unresolved-link scan: collect every note basename (stem, no .md) into a set; regex `\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]` over all active notes; a target's last path segment missing from the set = unresolved. New notes must resolve cleanly; pre-existing broken links in untouched folders are report-only unless the user asks for a cleanup pass.

## Renaming folders or notes / fixing links

1. Before renaming, find ALL references vault-wide (`search_files` content-search over the ENTIRE `F:\obsidian_note` tree) — references live in other vaults, the master overview, sibling topic folders, and `checklist\` notes, not just the folder itself. Skip `hermes_config_backup\` — historical artifacts stay as-is.
2. For note renames, search every wikilink form: `[[old]]`, `[[old|`, `[[old#`, and path-style `folder/old|`, `folder/old]]`, `folder/old#`.
3. Do renames + link rewrites in one scripted Python pass (walk + read + str.replace + write) — replace the LONGEST old name first so a shorter name can't collide inside a longer one; rewrite each renamed note's H1 to match its new filename. `sed -i` via git-bash is fine only for a single simple global token (folder typo fix).
4. Verify: zero stale references (re-run the same scan), every file exists at the new path, and print a filename↔H1 agreement table for eyeballing. The filesystem is the source of truth — verify with file tools, not Obsidian's app view (it can hold stale caches).
5. After renumbering, re-sort the Overview's Topics list to match the new order, annotate each entry with a one-line 'why it sits here' gloss, and add a naming-convention note at the top of the Overview.
6. Wikilinks pointing at a FOLDER name (`[[Computer Organization]]`) are dead links even with correct spelling — repoint them to the folder's Overview note with a display alias: `[[Computer Organization Overview|Computer Organization]]`.
