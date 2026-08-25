---
name: requirements-to-backlog
description: "Use when turning requirements into verified GitHub issues."
triggers:
  - User asks to create or update GitHub issues from user stories
  - A requirements pivot changes active stories, acceptance criteria, or repository ownership
  - Backlog metadata may already exist and must be updated idempotently
  - GitHub issue bodies require multiline Markdown, tables, emoji, or Unicode
metadata:
  class: product-management
  standards: [BABOK-v3, ISO-IEC-IEEE-29148, PMBOK-v8]
---

# Requirements-to-Backlog

## Purpose

Convert an approved requirements baseline into an implementation-ready GitHub backlog without duplicates, stale contracts, or unverifiable success claims.

## Workflow

1. Read current requirements, acceptance criteria, phase plan, design/API/DDL, and repository READMEs.
2. Inspect each repository's current issues, labels, milestones, default branch, and root layout.
3. Build an ownership map: backend/API/database/integration stories in the backend repo; public UI stories in the frontend repo. A story belongs in one repo only.
4. Map active stories to exact stable IDs; mark superseded stories historical/closed rather than leaving stale bodies active.
5. Create or update milestones only in repositories with work for that sprint.
6. Preserve default labels; add only missing custom labels for story, epic, priority, sprint, repository, and integration.
7. Make each issue implementation-ready: story statement, stable ID, objective, epic, priority, points, sprint, every AC checkbox, implementation notes, source paths, and cross-repo dependencies.
8. For provider integrations, create a separate technical gate for payload/auth/retry verification. For manual corrections, create a separate operational procedure issue.
9. Use temporary body files and `--body-file` for complex Markdown. Avoid fragile inline `--body` quoting.
10. Execute writes in small batches and record per-command exit codes.
11. Re-read GitHub after writes and verify title, state, body, labels, milestone, URL, duplicate absence, and dependency links.
12. Report actual issue URLs/numbers and milestone counts; distinguish created/updated/closed/blocked.

## Idempotency Rules

- Detect existing issues by exact stable story ID in title before creating.
- Update existing issue in place if the story remains active.
- If a story is superseded, preserve the decision/history in the issue body and close as `not planned`.
- Never create a second issue merely because the requirements document version changed.
- Verify both repositories independently; a multi-repo batch can partially fail.

## Issue Body Contract

```markdown
## User Story
As a [role], I want [capability], so that [outcome].

## Story Metadata
- Story: US-XXX
- Epic: E-XX
- Objective: OBJ-XX
- Priority: 🔴/🟡/🟢
- Story points: N
- Sprint: Sprint N
- Repository: owner/repo

## Acceptance Criteria
- [ ] AC-XXXa: ...

## Implementation Notes
...

## Cross-Repository Dependency
...

## Source Documents
...
```

Do not include API keys, OAuth tokens, webhook secrets, raw donor names, full provider payloads, or connection strings in issues.

## Verification Checklist

- [ ] Active story count matches the requirements baseline.
- [ ] Superseded stories are not open as active work.
- [ ] Each active story has exactly one owning repository.
- [ ] Each issue has all active ACs as checkboxes.
- [ ] Labels and milestones match the approved priority/sprint.
- [ ] Cross-repo consumer issues link to the actual provider issue URL.
- [ ] No duplicate stable IDs.
- [ ] Remote re-read confirms all writes.

## References

For provider-limited membership pivots, see `po-requirements-elicitation` and its `references/pivot-decision-matrix.md`.

## Pitfalls

- Inline `--body` quoting truncating or corrupting Markdown/Unicode.
- Reporting a batch as complete when one or more issue edits failed.
- Leaving closed issues with old subscriber/fuzzy/HMAC assumptions while developers treat them as current.
- Creating frontend issues before the backend provider contract issue exists.
- Treating issue creation as proof of implementation or test execution.
