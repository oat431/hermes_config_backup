---
name: project-spec-docs
description: "Fill/update project_spec docs (templates, MM handoffs)."
version: "1.0"
author: curator
license: MIT
metadata:
  hermes:
    tags: [project-spec, templates, meeting-minutes, documentation, persona-workflow, deerngo]
    related_skills: [meeting-action-items, document-to-action-items]
---

# project_spec Document Workflow

## When to Use

- User asks to "fill the missing document by this template", "read X then fill Y", or hands you requirement docs + a template path under `F:\projects\project_spec`
- Multi-persona handoffs (SA/Designer, PO, Dev, UX/UI) coordinated via `meeting_minute/MM*_*.md`
- Any request to update meeting minutes after producing documents

## Layout (verified on this machine)

```
F:\projects\project_spec\
├── template\                      # canonical templates (source of truth)
│   ├── 01_requirement\   (011_business_objective … 015_definition_of_done)
│   ├── 02_design\        (021_ADR … 029_architecture_overview)
│   ├── 03_construction\  04_testing\  05_devops\  06_security\  07_pm\
├── external_spec\<project>\        # per-project filled docs (e.g. deerngo_bot)
│   ├── 01_requirement\   02_design\
└── external_spec\meeting_minute\MM*_*.md   # persona handoff records
```

## Workflow

1. **Read everything first**: all requirement docs in the project dir + the relevant meeting minutes + the template(s) for the missing doc(s)
2. **Fill the template** with project content — keep the frontmatter block: `document_type, version, status, author, created, last_updated, project_name, project_id, classification, tags, standard_ref`
3. Save into the project dir under the **same filename as the template** (e.g. `026_wireframes_lofi.md`), not a renamed variant
4. **UPDATE the existing meeting minutes — never create new MM files unless asked** (explicit user rule). Patch the tables: mark action items ✅ Complete, add produced docs to "Documents Produced", update `last_updated`, adjust "What's Next"
5. `Related Documents` sections use wiki-links: `[[022_API_specification]]`

## Deliverable mapping (UX/UI persona)

- `026_wireframes_lofi.md` — 🔴 low-fi wireframes (ASCII-box structures + layout spec tables + annotations)
- `028_style_guide.md` — colors/typography/spacing/components
- `027_interactive_prototype.md` — intentionally skipped for single-page apps; don't fill unless a multi-step flow exists

## Pitfalls

- Directories are **singular**: `01_requirement`, `meeting_minute` (NOT `01_requirements`, `meeting_minutes`) — guessing the plural makes read_file 404
- `search_files` globs can return 0 matches on Windows drive paths (`F:\...`); when that happens enumerate with `ls -R` in the terminal, then read files by exact path
- Meeting minutes reference templates by path (`02_design/026_wireframes_lofi.md`); keep produced docs at those exact paths so links stay valid
- When a meeting minute lists design constraints (CSS framework, states, data fields), the filled doc MUST respect them — they are binding, not suggestions
- Status values on deliverables: use the project's convention (e.g. `0.1 Draft` for design docs); update `last_updated` to today's date
