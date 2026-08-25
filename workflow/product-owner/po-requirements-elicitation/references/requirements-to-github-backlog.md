# Requirements-to-GitHub Backlog Checklist

Use this reference when converting an approved requirements package into issues across multiple repositories.

## Preflight

- [ ] Read `012_user_stories.md` and extract stable story IDs, story points, priority, sprint, epic, and objective.
- [ ] Read `013_acceptance_criteria.md` and copy the current AC wording, including any later QA/PO decisions.
- [ ] Read the phase plan for implementation ownership, dependencies, and non-story DevOps/security work.
- [ ] Inspect each repository README and root contents.
- [ ] Query existing issues, labels, milestones, and branches.
- [ ] Confirm the default branch and repository names.

## Ownership Map Pattern

| Work type | Owner repository | Example |
|---|---|---|
| API, database, migrations, schedulers | Backend | `US-002`, `US-003`, `US-020` |
| streamer.bot configuration/integration | Backend/integration repo | `US-010`, `US-011`, `US-012` |
| Public API consumed by the UI | Backend | `US-031` |
| Public page, components, loading/error/empty states | Frontend | `US-030` |
| DevOps/security controls | Keep in phase plan or separate operational issue | CI/CD, tunnel, key rotation |

A story must have one owner repository. Create the backend/provider issue before the frontend/consumer issue and put the actual issue URL in the consumer body.

## Metadata

Create only missing custom labels. A useful baseline is:

- `user-story`
- `priority:must-have`, `priority:should-have`, `priority:could-have`
- `epic:<name>`
- `sprint:1`, `sprint:2`, `sprint:3`
- `repo:backend`, `repo:frontend`
- `integration`

Create milestones only where that repository has work. For example, a backend repo may have Sprint 1–3, while a frontend repo may only have Sprint 3.

## Issue Body Template

```markdown
## User Story

**As a** <role>
**I want** <capability>
**So that** <value>

## Story Metadata

- **Story:** US-XXX
- **Epic:** E-XX — <name>
- **Objective:** OBJ-XX
- **Priority:** 🔴 / 🟡 / 🟢
- **Story points:** <points>
- **Sprint:** Sprint N
- **Repository:** <repo>

## Acceptance Criteria

- [ ] **AC-XXXa:** <current accepted criterion>
- [ ] **AC-XXXb:** <current accepted criterion>

## Implementation Notes

- <constraints and design references>

## Source Documents

- `<path to user stories>`
- `<path to acceptance criteria>`
- `<path to relevant design document>`

## Cross-Repository Dependency

- Depends on <owner repo> issue URL, if applicable.
```

## Idempotent Creation and Verification

- Use exact stable story IDs in issue titles, such as `US-031: Implement paginated public scoreboard API`.
- Before creating, search all issues (open and closed) and skip an exact existing story title.
- After creating, read back each issue and verify: title, state, labels, milestone, body, and returned URL.
- Verify milestone open-issue counts and that every story appears exactly once.
- Verify cross-repository URLs are present in consumer issues.
- Report concrete URLs/numbers; never report a remote write as successful without read-back evidence.
