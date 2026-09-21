---
name: self-learning-course-authoring
description: "Use when designing a self-paced learning course."
platforms: [windows, linux, macos]
tags: [course, curriculum, self-learning, obsidian, study-plan, interview-prep]
triggers:
  - "I want to learn X, draft the course"
  - "build a study plan / curriculum / syllabus for X"
  - "place the course in my vault"
  - user invokes /grill-me to design a learning plan
related_skills: [grill-me, curriculum-vault-authoring, obsidian-note-authoring]
---

# Self-Learning Course Authoring

Design a personal, project-based learning course and deliver it as an Obsidian
course folder: a Course Map (hub), a full upfront syllabus, a verified
resources file, and lesson files written just-in-time as the learner reaches
them. The design interview runs on `grill-me`; this skill supplies the
course-specific structure, conventions, and proven defaults.

Not for mapping external curricula into BOK structures (that is
`curriculum-vault-authoring`) — this is a personal skill course for one learner.

## When to Use

- User names a topic to learn and asks for a course, syllabus, or study plan in their vault
- User says "grill me" / "create the course with me" for a learning goal
- Continuing a course: releasing the next lesson, phase checkpoints, syllabus edits

## Course Conventions (this user)

- **Location:** `F:\obsidian_note\interview-preparation\self-learning\<topic-slug>\` (confirm if the user names another location).
- **Root files:** `00_Course_Map.md` (hub: mission, rules, protocol, phase tracker, capstone ladder, open items) · `01_Syllabus.md` (ALL lessons mapped upfront: `# | lesson | focus | resources | est | checkbox` in per-phase tables, plus dojo lists and checkpoints) · `02_Resources.md` (verified links: spine vs optional vs orientation maps; cross-vault assets).
- **Lessons:** `phase-N-<name>/NN_Title.md`, GLOBAL numbering across phases (00, 01, 02 ... through the last phase).
- **Style:** English, colons over em-dashes, Mermaid over ASCII, numbered prefixes. Frontmatter: `document_type: Lesson`, `lesson_type`, `course`, `lesson`, `phase`, `estimated_time`, `prerequisites`, `related`, `project`, `tags`.
- **Lesson shape:** Learning Objectives · Prerequisites · Concept · Visual Reference · Hands-On · Going Deeper · Interview Lens · Done When (checkboxes) · Key Takeaways. Skeleton in `templates/lesson.md`.

## Procedure

1. **Gather facts before asking anything.** Target folder state; related notes across BOTH vaults — an existing checklist or note for the topic often reveals the real goal and target stack, and it sharpens the interview questions; environment state via terminal (toolchain installed? editor? package manager?); sibling-folder conventions. On `F:\` drives prefer `terminal` `find`/`grep` for vault searches; an empty file-tool result there is not evidence of absence.
2. **Interview in frontier rounds** (`grill-me`, rounds delivered via `clarify`). Delivery rules for a round: one question per decision; recommended option FIRST in `choices` with the rationale in the question text (options belong only in `choices`, never in the question prose); an open scope question omits `choices`; **max 5 questions per call**, so carry overflow into the next round. Proven course frontier — R1: goal/track, weekly time budget, resource spine, content-generation model (full syllabus now + JIT lessons is the default), build environment. R2: taste-first preview yes/no, interview lens yes/no, capstone domain timing, open scope question ("anything in or out of scope?").
3. **Synthesize, then get explicit approval** before writing files: decisions table, phase architecture, vault layout tree, open items, explicit OUT-of-scope list.
4. **Verify every external fact** (see Verification) — at write time, every time.
5. **Write the root files + the setup lesson immediately** (it must be actionable the same day); later lessons are written when reached.
6. **Run the JIT loop:** learner reports `done NN` + outputs + blockers; verify; release lesson N+1; tick the syllabus checkbox. At phase ends: checkpoint (consolidation, shaky-lesson redo, answer cards, pace re-estimate).

## Proven Design Defaults

Adjust per interview; these recurred and worked.

- **Phase arc:** Foundations (fundamentals dominate the first half) → Intermediate → Domain/stack → Enterprise polish. When the user's vaults already contain a checklist for the target stack, make it the capstone's enterprise scorecard.
- **Taste-first option:** right after setup, one copy-along where the learner runs the destination artifact ("understanding optional — we explain why in Phase N").
- **Per lesson:** Going Deeper AFTER the practical block (user asks for depth post-learning) + Interview Lens (one common question + 60-second spoken skeleton, answered out loud) + Done When checkboxes. Phase checkpoints consolidate the interview answer cards.
- **Practice dojo:** 1-2 platform problems/week mapped to current topics (LeetCode primary). Confirm the platform really supports the language before writing the table — challenge domains get retired.
- **Capstone:** ONE project, ground-up → enterprise, introduced after fundamentals; "decide the domain together when Phase N starts" is a valid choice.
- **Pace honesty:** content burn ≠ weekly budget × weeks. State the honest total vs nominal ("expect drift to N weeks, or compress: pause dojo, merge reviews") and re-estimate at checkpoints.

## Verification (before publishing content)

- **Every URL:** `curl -sL -o /dev/null -w "%{http_code}" <url>`. Platform pages rot: challenge domains retire, hub pages 404 while article pages live. Prefer article-level and stable endpoints; replace dead links at write time; never publish an unverified URL in a Resources table.
- **JS-rendered sites:** fetch the data endpoint instead of scraping the DOM (e.g. `https://roadmap.sh/<slug>.json` for roadmap.sh; when parsing hits control characters use `json.loads(text, strict=False)`).
- **Resource liveness:** GitHub API gives `archived` + `pushed_at` — check before recommending a repo as spine; read the current official site for install flows (they move; never write setup steps from memory).
- **Windows installs:** resolve exact package IDs with `winget search <name>`; verify the current official install command before writing it.
- **"Is X useful?"** classify: official book/course = spine; ecosystem roadmap site = orientation map (good for later paths, not a curriculum). Tell the user which is which.
- **Code-bearing lessons:** build + run the code on the user's machine BEFORE writing the lesson. Embed the real output (with date) so the lesson ships verified, not theoretical. Pin crate/dependency versions to what the package manager actually resolved at build time — never write a `Cargo.toml` or equivalent from memory.
- **"Done NN" reports:** verify on the real machine, not by re-reading your own lesson file. Run their code, hit their service with curl, inspect their tool state. "The user said it's fine" or "the file I wrote says so" is not verification.

## Pitfalls

- **Never forward-link uncreated lesson files.** Syllabus rows stay plain text (`Lesson 07: Strings`) until the file is released; convert to `[[07_Strings]]` on release. JIT authoring creates broken links by default and this user's vaults are audited for link health.
- **Don't write all lesson files upfront** when the interview chose JIT — the syllabus maps everything; full content arrives one at a time.
- **Setup lessons:** include the traps the learner will actually hit (PATH/terminal refresh after installs, editor language-server download prompt, big one-time downloads with a time expectation).
- **Estimates** are content-time upper bounds including spine exercises; don't let summed estimates silently exceed the weekly budget.
- **Binary installed is not a tool initialized.** When verifying a setup report, check for the init OUTPUT, not just the binary. Tools with a separate init step (e.g. `rustlings init`, `git init`, `cargo new`) can have the binary on PATH but no project/exercises created. A setup lesson's "Done When" must list the init artifact, not just the version command.
- **Don't embed a code/working path in lesson content until the user has chosen it.** Suggest a path in the interview; if the user accepts a default, mark it as a suggestion and patch every reference when they tell you the real path. Hardcoding a guessed path then patching five files afterward is avoidable — wait for the path, or use a placeholder.

## Related

- `grill-me` — the interview engine (rounds delivered via `clarify`).
- `curriculum-vault-authoring` — external curricula → BOK vault structures (different artifact).
- `templates/lesson.md` — lesson file skeleton to copy for each release.
