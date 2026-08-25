# QA → PO Spec Gap Review Meeting Minute Template

> Use this template when QA finds spec contradictions during Phase 2 that need PO resolution before test cases can be finalized.

## Naming Convention

```
meeting_minute/MM{N}_qa-to-po_{YYYYMMDD}.md
```

Example: `MM04_qa-to-po_20260730.md`

## Structure

```yaml
---
document_type: Meeting Minutes
version: "1.0"
status: Final  # Update to "Final" after PO responds
author: "QA Engineer"
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
project_name: "[Project Name]"
meeting_type: "QA → PO Spec Gap Review"
participants: ["QA Engineer", "PO"]
classification: "Internal"
tags: [meeting-minutes, spec-gaps, requirements, qa]
---
```

## Sections

### 1. Purpose
Why QA is raising these gaps (test case authoring found contradictions).

### 2. Context
- What QA produced (documents, coverage)
- Summary metrics (ACs covered, test cases written, gaps found)

### 3. Spec Gaps Requiring PO Decision
For each gap:
- **Source documents** (quoted contradiction)
- **Conflict** (what breaks if not resolved)
- **Impact on Testing** (which TCs depend on this)
- **Decision options** (2-3 resolution paths with trade-offs)

### 4. Spec Gaps — Dev-Facing (No PO Decision Needed)
Implementation risks Dev should be aware of. PO aware but no decision required.

### 5. Decision Record
| ID | Question | PO Decision | Date | Notes |
Fill after PO responds.

### 6. Action Items
| Action ID | Action | Owner | Priority | Depends On |
Include QA update tasks that depend on PO decisions.

### 7. Handoff Summary
- Flow diagram showing where in the pipeline this sits
- What PO gets (and what action is required)
- What happens after PO decides

## Key Patterns

1. **Always give PO options, not just the problem.** Each gap should have 2-3 resolution paths with clear trade-offs.
2. **Link each gap to specific TCs.** PO needs to understand the downstream impact of their decision.
3. **Separate PO decisions from Dev tasks.** PO decides *what* the behavior should be. Dev implements *how*. Don't mix them.
4. **Update the Decision Record in-place.** After PO responds, update the same meeting minute — don't create a new document. The decision table is the audit trail.
5. **After decisions, update test cases immediately.** Don't batch — update TCs, close DEF-S entries, then proceed to 044/045.
