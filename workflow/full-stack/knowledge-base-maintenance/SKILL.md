---
name: knowledge-base-maintenance
description: "Use when auditing stale docs or building checklists. Verify."
version: 1.0.0
author: Dev (Senior Full-Stack Developer)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [documentation, knowledge-base, audit, staleness, bulk-update, subagents]
    related_skills: [obsidian, grounded-citations, plan]
---

# Knowledge Base Maintenance

Staleness/currency audit of a documentation set (vault checklists, specs, guides), then a user-gated bulk update. The docs' subject matter — framework majors, standards editions, product names — moves faster than the model's knowledge, so no version/edition/product claim is blessed or changed without a live source.

## When to Use

- The user asks whether a doc set (vault checklists, specs, guides) is up to date, current, or stale
- Periodic refresh of technical docs that name versions, editions, tools, standards, or vendors
- Bulk-correcting a corpus after a standards renumbering, product rename, or product retirement

Skip for: single factual lookups (just answer with a source), docs without verifiable technical claims, and code changes.

## Always-on rules

1. **Research → review gate → apply.** This user reviews drafts and research before any file is committed: produce the audit report first, ask ONE scope question (all / must-fix + should-fix / must-fix only / hold), edit only after the answer. If the scope question times out unanswered, apply the most conservative reversible interpretation (annotate instead of delete) and flag it in the summary.
2. **Audit phases are read-only.** Auditors never edit. After the audit, confirm with `find <root> -name '*.md' -newermt <today>` that nothing moved before presenting the report.
3. **Every finding is structured:** file · location · current text (short quote) · issue · proposed replacement · severity · source URL. A finding without a live source does not ship — verify it or label it an assumption in the caveats.
4. **Severity vocabulary:** must-fix = wrong or misleading today (broken examples, retired products, false version claims); should-fix = superseded baseline (old major, renamed tool, superseded standard edition); nit = polish (example pins, wording). Ask scope once, with counts per severity.

## Procedure

### 1. Recon — build the fact-checkable surface
- Inventory with mtimes: `find <root> -name '*.md' -printf '%TY-%Tm-%Td %8s %p\n' | sort`
- Extract version claims: `rg -o -N --no-filename '\b[A-Za-z][A-Za-z0-9+.#/]{1,25}\s+(v?[0-9]+(?:\.[0-9]+){1,3})\b' -g '*.md' | sort | uniq -c | sort -rn`
- Then grep the digit-less staleness classes that regex cannot see: standard/edition names (OWASP/NIST/ISO/W3C), products that get rebranded or retired, protocol drafts cited as final, removed API names. Renames leave no version trace — they surface only on the vendor's own pages.

### 2. Parallel read-only audit
- One subagent per category/directory with disjoint file sets — the same split later drives the apply phase, so editors never collide.
- Every child context carries: today's date (children answer "what is current" from stale memory otherwise — forbid answering version questions from memory), its file list, the seed claims from recon, the search instructions in `references/live-source-checks.md`, the finding structure, and "DO NOT EDIT FILES".
- Bound each child: 15–25 searches, ≤40 findings prioritized by severity, highest-impact claims verified first.

### 3. Spot-check the leverage findings
- Subagent findings are self-reports. Before presenting, independently re-verify the two or three findings that drive the most edits (e.g. a standard edition renumbering that fans out across files) plus anything an auditor labeled low-confidence. Fix wrong findings before they reach the report.

### 4. Report + scope question
- Write a decision-grade report file: counts by severity, headline themes, every must-fix with full proposed text, should-fix/nits condensed one line each, and a caveats section (low-confidence findings, degraded-search workarounds, scope exceptions). Chat summary stays compact; the report carries the detail.
- Ask one clarify with the scope choices, plus any editorial decisions the findings surfaced (e.g. remove vs annotate a suspect entry).

### 5. Apply — parallel editors
- Mirror the audit split; each editor works ONLY from its report section and its own files (say so explicitly — cross-applying causes write conflicts).
- Edit with patch and a unique anchor from the 'current' quote; never rewrite whole files; match the doc set's style (checkbox items, wikilinks, pipe tables) and keep heading numbers that other tables reference.
- Anything computed from other files' content — line counts in an index, totals — is deferred to the lead and patched AFTER all editors finish, recomputed at that moment.

### 6. Verify, then report
- Per editor: search_files for the stale tokens that defined the audit (old majors, removed API names, retired product names) in its files; every remaining hit must be an intentional "formerly …" mention.
- Lead: recompute the deferred counts, spot-read a few edited sections, then report applied / adapted / skipped per finding — adapted says how it was adjusted, skipped needs a reason.
- Reconcile editors' `untouched_stale_tokens` reports across sections: disjoint scopes leave same-class staleness in *other* editors' files (an image tag fixed in one category but stale in another). The lead triages each — fix the clear same-class cases, leave legitimate generic usage (e.g. MTTR outside DORA metric sets) with a note.

## Extending a checklist family (framework layers)

When the user picks stacks to add under an existing checklist surface (e.g. cli-checklist, desktop-checklist):

1. One author per stack file, parallel, each briefed with: the shared section skeleton, the family's STYLE rules verbatim (title/blockquote/bold-lead-in items/Quick Sanity/Sources), a named *model sibling file* to read for depth (e.g. the same stack in api-checklist), the contract file's real section numbers for `→ [[contract]] §N` cross-links, and 'never invent API names — verify via curl of official docs/registries (GitHub API, npm view, pub.dev, Maven, NuGet are curl-friendly) or phrase "-class"/generic. No version pins.'
2. Pass settled vault facts forward so new files cannot contradict fresh fixes (e.g. retired products flagged in a prior audit).
3. Verified historical milestones ("since X") and protocol floors ("TLS 1.2+") are sanctioned pins; "current" product versions are not.
4. Afterward, the lead independently verifies: wc -l, version-pin scan (grep, excluding headers/URLs), family headers present in all files, wikilink targets resolve, item totals computed with awk — never trust self-reported counts (an off-by-one will appear).
5. Add a 'Stack Family' section to the contract file listing the layers; update Overview only for originals Overview actually tracks.

## Pitfalls

- Put delegate_task's reporting contract in the task text; use an output_schema only when it is trivial. One stray key inside `properties` (e.g. a bare `"type": "string"` entry) fails JSON-Schema validation and the fan-out is rejected atomically — nothing dispatches.
- Parallel auditors saturate search engines fast: a self-hosted SearXNG and built-in web_search throttle or return empty together under ten-child load. Budget queries per child and keep the curl fallback against authoritative URLs (see `references/live-source-checks.md`) — it does not touch search, so it works when engines are down.
- Never re-extract child results from their transcript logs: the logs stream truncated chunks and the final JSON is not recoverable. Consolidate from the returned messages, or have children write findings to files the lead reads back.
- When the shell and Python disagree about temp dirs (MSYS `/tmp` vs Windows `%TEMP%`), share files via `$HOME` or absolute Windows paths — a `curl -o $TMPDIR/x` can land where the next interpreter cannot see it.
- Editors' proposed texts come from the report, which condenses some findings: tell editors condensed items mean "implement this intent as a minimal edit in file style", not "skip".
- A fuzzy patch over a span reconstructed from memory can silently REVERT other fixes inside that span (it matched "approximately" and rewrote the block). Prefer narrow anchors; after any non-exact-match patch, re-read the whole patched region and diff-check for regressions.

## Building checklist families (framework layers)

- Contract first: the general file defines sections (§1..§N) that layers cross-link (`→ [[general]] §N`); the general file gains a Stack Family list pointing back at the layers. Two-way linking, no dead links.
- One author per layer file, shared skeleton brief: family header blockquote ("Companion to the general [[general]] checklist — that one is the contract, this one is the plumbing"), numbered sections, `- [ ] **Bold lead-in:**` items, `## Quick Sanity Check Before Release`, `## Sources` ending with `Master checklist: [[general]].`. NO version pins anywhere — '-class' phrasing for packages whose maintenance status is unverified.
- Authors verify API/package claims live (npm view, pub.dev, GitHub releases API, Maven Central, vendor docs via curl) and report claims_verified_via_web plus uncertain_items_avoided; a 404'd package is a finding, not a failure.
- Lead verification before reporting: version-pin regex scan must be empty; family-header count must equal file count; `wc -l` reconciled against author self-reports (they drift by ±1–2); declared item totals recomputed with `grep -c '^- \[ \]'` — never repeat an unverified total.
- Wiring: Stack Family list in the general file; Overview.md rows only for files it tracks, with line counts recomputed LAST after every edit.

## References

- `references/live-source-checks.md` — where to verify versions, EOL status, standards editions, and vendor renames; fetch recipes; phrasing rules for evergreen docs.
