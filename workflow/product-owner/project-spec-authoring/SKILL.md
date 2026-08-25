---
name: project-spec-authoring
description: "Use when writing a spec package from a requirements doc."
version: "1.0.0"
author: "curator"
license: "MIT"
tags: [spec, authoring, project-spec, templates, requirements, interview-challenge, product-owner]
metadata:
  hermes:
    tags: [spec, authoring, project-spec, templates, requirements, interview-challenge, product-owner]
    related_skills: [spec-document-elicitation, po-requirements-elicitation, requirements-to-backlog]
---

# Project Spec Authoring (Written Source)

Author a complete spec package from a **written requirements source** (interview challenge README, RFP, external API doc, RFC) using the template tree at `F:\projects\project_spec\template\`. No stakeholder interviews — the source is a document.

> **Trigger distinction:** if the user says "grill me" / "interview me" and wants interactive Q&A, use `spec-document-elicitation` instead. That skill is elicit-one-doc-at-a-time; THIS one is batch-write-a-package-from-a-document.

## When to Use

- User provides a written requirements source (GitHub challenge README, RFP, spec doc) and says "create a spec first before we implement"
- User names a target folder (e.g. `F:\...\.agents\spec`, per-project spec dir)
- User references `F:\projects\project_spec\template\` and lets you pick templates
- Context is an assessment/interview where "bonus points" matter

## Workflow

### 1. Fetch the source
- **GitHub files:** `curl -sL https://raw.githubusercontent.com/<owner>/<repo>/<ref>/<path>` — works even when `web_extract` is unavailable ("SearXNG is a search-only backend" error → curl raw URLs; for gists: `gist.githubusercontent.com/<user>/<id>/raw/<file>`).
- Only use `web_extract` if a real extract backend is configured; treat failure as the signal to curl.

### 2. Inventory + read templates
- `search_files(pattern='*', target='files')` on the template dir to see the tree.
- Read the templates that map to the scope. For a backend/API project: `011_business_objective`, `012_user_stories`, `013_acceptance_criteria`, `015_definition_of_done`, `022_API_specification`, `023_database_schema_DDL`, `025_software_architecture_document`, `031_README_developer_guide`, `041_test_plan`.

### 3. Review & frame (present BEFORE writing)
Produce a compact review for the user:
- Requirement → interpretation table (each bullet of the source, one row)
- **For assessments: evaluation criteria ARE the business objectives.** Map them 1:1.
- **Bonus/optional analysis:** look for synergy — e.g. "Go interfaces for DB" simultaneously enables the required "mock DB in tests"; "hexagonal architecture" is the structure that makes interfaces + clean tests effortless. Sell the package as one coherent bet, not N independent features.
- State the verdict (go/no-go) and the proposed doc set with template mapping.

### 4. Clarify ONLY material forks (1–2 max)
- Ask forks that change MULTIPLE docs (scope items, optional features, architecture style). Use `clarify` with curated presets and a recommended one. Example: bonus scope → "Full send / All except X / Minimal" — because gRPC-or-not touches stories, ACs, API spec, architecture, and test plan.
- **Do NOT ask about minor decisions** (port numbers, register-returns-token, pagination, field limits). Bake them as stated assumptions — see §Assumptions below.
- After answers, confirm the plan in one short message, then write.

### 5. Write the package
- Use a `todo` list for 5+ docs; batch `write_file` calls 2–3 per turn.
- Batch writing the whole package is CORRECT in written-source mode (user asked for the package, not a doc-at-a-time review — this differs from grill mode).
- Fill frontmatter completely (author, dates, project_name, project_id, status `Draft`). No placeholder text — either fill or deliberately trim a section with a one-line note.

### 6. Verify & report
- `search_files` to confirm every file landed on disk.
- Report: package map table, key decisions locked, assumption list pointer, and next steps (implementation reading order).

## Doc Set & Numbering Convention

| File | Path | Use | Skip when |
|------|------|-----|-----------|
| `000_spec_index.md` | spec root | Doc map, reading order, **baseline assumptions table**, status checklist | never |
| `011_business_objective.md` | `01_requirement/` | Objectives, KPI gates, risks | never |
| `012_user_stories.md` | `01_requirement/` | INVEST stories, epics, points, sequencing | never |
| `013_acceptance_criteria.md` | `01_requirement/` | Given–When–Then per FR; AC IDs traceable to TC IDs | never |
| `015_definition_of_done.md` | `01_requirement/` | Submission/release gate checklist | never |
| `022_API_specification.md` | `02_design/` | REST contract + gRPC proto if in scope; error envelope; samples | no API surface |
| `023_database_schema_DDL.md` | `02_design/` | Works for Mongo too: collection shape, indexes, repo ops table | no persistence |
| `025_software_architecture_document.md` | `02_design/` | Style table, package tree, component table, ADRs, mermaid flowchart | trivial structure |
| `031_README_developer_guide.md` | `03_construction/` | Deliverable content: setup, samples, assumptions; doubles as repo README | no repo deliverable |
| `041_test_plan.md` | `04_testing/` | Strategy, fakes/mocks decision, coverage gates, TC↔AC trace, manual smoke | no testing requirement |
| `014_stakeholder_analysis.md` | `01_requirement/` | Personas, influence matrix | lean/interview scope |
| `071_risk_register.md` | `07_pm/` | Full risk register | lean scope — fold key risks into 011 instead |
| `072_meeting_minutes.md` | `07_pm/` | Cross-persona handoffs | no persona handoffs |

**Sizing rule:**
- **Lean (interview challenge / portfolio):** the core 10 docs, ~100–250 lines each, no enterprise ceremony, skip 014/071/072. The spec exists to drive a great implementation — the reviewer never reads it.
- **Full (platform/multi-service):** add 014, 071, 072 and follow `spec-document-elicitation` for the platform-umbrella/service-split pattern.

## Assumptions Pattern (state once, cite everywhere)

Numbered assumptions (A1, A2, …) live in ONE table in `000_spec_index.md`: statement + rationale. Downstream docs cite them inline (`(A7)`) instead of repeating rationale. Flag each as "flaggable" in the review so the user can veto cheaply. Only the forks you clarified become explicit decisions (D-01, …) in `011`.

## Conventions (user hard rules)

- Frontmatter always populated; `Related Documents` cross-refs at the bottom of every doc.
- Mermaid: **flowchart only** (TB/LR, subgraphs, color-coded), never mindmap; directory trees as plain code blocks or `treeView-beta`. Never ASCII art.
- Traceability chain: Objective → Story → AC ID → TC ID → DoD checklist.
- For interview repos: `031` carries a fenced `## README (repo)` section marked "copy verbatim to repo root as README.md", plus a deliverable-mapping table (challenge deliverable → README section). This makes the README a spec artifact instead of an afterthought.
- Sequence guard: required scope first, bonus items explicitly LAST in stories/epics and risk register (e.g. "gRPC after REST is green") so the bonus can't block the required deliverable.

## Pitfalls

- **web_extract search-only failure:** when extract backend is unconfigured, `web_extract` returns "SearXNG is a search-only backend". Go straight to `curl` on raw URLs — don't burn a turn retrying.
- **Don't over-clarify.** Max 1–2 material forks. Everything else = assumption. A wall of questions on an interview challenge reads as indecision.
- **Resolve bonus/optional scope BEFORE writing.** It touches 5+ docs; retrofitting is a rewrite.
- **Don't copy template placeholder text.** `[Author Name]`, `[X.Y]` left behind reads as sloppy — the user's convention is fully-populated frontmatter.
- **Don't write one doc and stop to ask "review or continue?"** in written-source mode — that's grill mode behavior. Deliver the package, then invite review.
- **Mongo ≠ skip the DDL doc.** Adapt `023` to collections + indexes + repo operation table; the interviewer still needs the schema contract.

## Support Files

- `references/interview-challenge-playbook.md` — worked example: Go + MongoDB + JWT challenge (SevenSolution), the 10-doc set, bonus-synergy analysis, and the assumption set that was baked in.
