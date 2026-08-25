---
name: interview-prep-coaching
description: Use when building or reviewing interview prep notes.
version: 1.0.0
author: Dev (full-stack profile)
license: MIT
metadata:
  hermes:
    tags: [interview-prep, coaching, obsidian, evidence-audit]
    related_skills: [obsidian, grounded-citations]
---

# Interview Prep Coaching

Use when the user builds or reviews interview-preparation notes in their Obsidian vault (theirs is `F:\obsidian_note`, folders under `interview-preparation/<company>/`): converting study/question notes into rehearseable answer cards, auditing the prep before the interview, or proposing improvements under a time budget. This user does this repeatedly (multiple company folders), so treat it as a durable workflow, not a one-off.

Vault path rule: when the user provides an absolute path in the message, use it directly — it takes precedence over any default vault location. Work with file tools (`read_file`/`write_file`/`patch`/`search_files`), never shell heredocs.

## The vault shape

Prep folders follow five pillars (create whichever are missing):
1. **Battle card** — company research, panel reading, logistics, questions to ask them
2. **Fit assessment** — JD line-by-line vs resume evidence, with 🔴/🟢 fit flags
3. **Knowledge gaps / study plan** — per-topic notes, priority-ordered
4. **STAR stories + drill questions** — spoken versions rehearsed aloud
5. **Practice plan + day-of checklist**

Two extra artifacts this user expects:
- `note/` subfolder of **answer cards** paired 1:1 with the study notes
- A **review note** when asked to "review my prep" (triaged findings, not a rewrite)

## Answer-card pattern

- One card per study note + one index card. Frontmatter: `document_type: Answer Card`.
- Answers are **spoken-length (20–45s)** — written to be said aloud, matching the user's drill method ("read question → answer aloud → check card").
- **Mermaid flowcharts** for decision logic (the user prefers visual decision trees over prose), small tables for comparisons, code snippets only where they earn their place.
- Every card ends with a **⚡ rapid-fire recap** for the last 10 minutes before the interview.
- Index maps drill questions → cards, and **cross-references personal-story scripts instead of duplicating them** — one source of truth for confirmed facts.
- Backlink from the study-plan index so cards are discoverable from the existing workflow.
- Full recipe: `references/answer-card-recipe.md`.

## Evidence audit (the high-value review step)

When asked to review prep, ground every finding in real artifacts — never take the notes at face value:
1. Read **every** prep file, including scripts and STAR stories.
2. Extract every claim backed by an artifact: promised repos, code samples, metrics.
3. Verify each against reality with `scripts/audit_github_evidence.sh` (authenticated `gh api`).
4. Audit each candidate repo: README promises vs actual source tree, dead dependencies, test presence, CI presence.
5. Cross-check dates: "publish by Tuesday" claims against today's date.
6. Report as **P0/P1/P2 triage** with time costs, and recommend ONE track when options exist.

## Time triage

With <24h to the interview: a mock interview round and code-walkthrough rehearsal outrank more silent reading. Sequence recommendations as an evening plan with per-item time budgets.

## Pitfalls

- Never duplicate personal-story content into answer cards — cross-reference the scripts note; confirmed facts must have one source of truth.
- Prep materials should model the senior behaviors the scripts claim (a repo preaching CI gates should have CI).
- Unauthenticated `curl` against the GitHub API rate-limits fast (empty body breaks JSON parsing) — always use `gh api`.
- On Windows git-bash, native tools need `C:/...` forward-slash paths; `$LOCALAPPDATA/Temp` works for scratch files.
- Sensitive data (meeting IDs, passcodes, phone numbers) lives in battle cards — fine in a private vault, flag it if the note might leave the vault.
