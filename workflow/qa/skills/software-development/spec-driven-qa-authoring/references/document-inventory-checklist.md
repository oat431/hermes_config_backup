# Document Inventory Checklist

> The 7-document-per-project inventory shape for spec-driven QA backfill. Use this as the verification oracle in Phase 3 of the workflow.

## Expected documents per project

| # | Folder | File | Template source | Content oracle |
|---|--------|------|-----------------|----------------|
| 1 | `04_testing/` | `041_test_plan.md` | `template/04_testing/041_test_plan.md` | Spec: business objectives, user stories, architecture |
| 2 | `04_testing/` | `042_test_cases.md` | `template/04_testing/042_test_cases.md` | Spec: user stories + acceptance criteria; Code: endpoints/classes |
| 3 | `04_testing/` | `043_defect_report.md` | `template/04_testing/043_defect_report.md` | Code review findings OR realistic spec-derived findings |
| 4 | `04_testing/` | `044_regression_test_suite.md` | `template/04_testing/044_regression_test_suite.md` | Test cases from doc #2 |
| 5 | `04_testing/` | `045_coverage_report.md` | `template/04_testing/045_coverage_report.md` | Code: test files found; Spec: requirements count |
| 6 | `06_security/` | `061_security_test_report.md` | `template/06_security/061_security_test_report.md` | Code: SecurityConfig, CORS, rate limiter; Spec: ADRs |
| 7 | `06_security/` | `062_coding_standards_security.md` | `template/06_security/062_coding_standards_security.md` | Code: actual classes/patterns; Spec: coding standards |

**Total per project: 7 documents.**
**For N projects: 7 × N documents.** Typical: 4 projects → 28 documents.

## Verification command (run once at the end)

```python
# Python via execute_code — checks all expected files exist and are non-empty
from hermes_tools import terminal

projects = [
    ("Project Name", "F:/path/to/spec/project"),
    # ... one tuple per project
]
docs = {
    "04_testing": ["041_test_plan.md", "042_test_cases.md", "043_defect_report.md",
                    "044_regression_test_suite.md", "045_coverage_report.md"],
    "06_security": ["061_security_test_report.md", "062_coding_standards_security.md"],
}

total_expected = 0
total_found = 0
for proj_name, proj_path in projects:
    print(f"\n📁 {proj_name}")
    for folder, files in docs.items():
        for f in files:
            total_expected += 1
            r = terminal(f'ls -la "{proj_path}/{folder}/{f}" 2>&1')
            if r["exit_code"] == 0:
                parts = r["output"].split()
                size = parts[4] if len(parts) > 4 else "?"
                print(f"  ✅ {folder}/{f}  ({size} bytes)")
                total_found += 1
            else:
                print(f"  ❌ {folder}/{f}  — MISSING")

print(f"\nTOTAL: {total_found}/{total_expected} documents")
```

A successful run prints `TOTAL: 28/28 documents` (or 7N/7N for N projects).

## Per-file completeness checks

For each filled file, confirm:

- [ ] No `[bracketed]` placeholders remain (grep for `[` excluding code blocks).
- [ ] YAML frontmatter present with: `project_name`, `project_id`, `created`, `last_updated`, `author: "QA Engineer"`, `status: Draft`.
- [ ] For `042_test_cases.md`: every test case has a `Requirement:` field tracing to a US-XXX or AC-XXX.
- [ ] For `043_defect_report.md`: every defect has ID, severity, steps-to-reproduce, expected, actual, environment, remediation.
- [ ] For `045_coverage_report.md`: coverage numbers are either measured (cite the test files) or marked `—` (not fabricated).
- [ ] For `061_security_test_report.md`: OWASP Top 10 table is filled with ✅/🟡/🔴 per category, not blank.
- [ ] For projects WITH a code repo: document bodies reference real class names / endpoints / config keys from the code.
- [ ] For projects WITHOUT a code repo (container-only, overview): defects are configuration/flow-level, not code-level; coverage focuses on flows/config.

## Common gaps to watch

| Gap | Symptom | Fix |
|-----|---------|-----|
| Template placeholder leaked | `[Project Name]` still in output | Search-and-replace all `[...]` |
| Missing traceability | Test case has no `Requirement:` | Add US-XXX / AC-XXX field |
| Fabricated coverage | `87%` with no test files cited | Replace with `—` or cite the test file |
| Generic defect | Defect could apply to any project | Add project-specific class name / endpoint |
| Orphan folder | `04_testing/` exists but `06_security/` doesn't | Create both; both are must-have |

## Output to user

End with a summary table:

```
| Project | 04_testing | 06_security | Total |
|---------|:----------:|:-----------:|:-----:|
| Proj A  | 5 ✅       | 2 ✅        | 7     |
| Proj B  | 5 ✅       | 2 ✅        | 7     |
| Total   | 10         | 4           | 14    |
```
