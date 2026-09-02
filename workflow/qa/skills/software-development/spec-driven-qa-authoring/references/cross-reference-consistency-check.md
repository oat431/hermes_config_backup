# Cross-Reference Consistency Check

When multiple writers (main agent + subagents) author QA documents in parallel, each tends to invent their own ID naming convention for test cases and defects. Documents that cross-reference test case IDs (e.g., 044 regression suite references "GATE-TC-001" from 042 test cases) can end up with mismatched schemas.

## The Problem

**Example from a real session:**
- Subagent wrote `042_test_cases.md` for Flowero Guard using IDs: `TC-G001`, `TC-G002`, ..., `TC-G046`
- Main agent wrote `044_regression_test_suite.md` referencing: `GUARD-TC-001`, `GUARD-TC-010`, `GUARD-TC-020`
- Result: 23 cross-reference mismatches across 4 documents (043, 044, 045, 061)

**Another example:**
- Subagent wrote `042_test_cases.md` for Flowero Discover using IDs: `TC-001`, `TC-002`, ..., `TC-021`
- Main agent wrote `044_regression_test_suite.md` referencing: `DISC-TC-001`, `DISC-TC-002`
- Result: 15 cross-reference mismatches, plus orphaned documents (045, 061 had no test case refs at all)

## Prevention: Define Schema Upfront

Before dispatching subagents, define the ID schema for each project and include it in the subagent prompt:

```
For Flowero Gate, use ID scheme: GATE-TC-### (e.g., GATE-TC-001, GATE-TC-002)
For Flowero Discover, use ID scheme: TC-### (e.g., TC-001, TC-002)
For Flowero Guard, use ID scheme: TC-G### (e.g., TC-G001, TC-G002)
For Panomete Platform, use ID scheme: PLAT-TC-### (e.g., PLAT-TC-001, PLAT-TC-002)
```

## Detection: Audit Script

After all documents are written, run this audit to detect mismatches:

```bash
# For each project, extract IDs from 042 and check if 044/045/061 reference them

# Flowero Gate (expected: GATE-TC-###)
grep -oP '\*\*ID\*\*\s*\|\s*\K[TC-GA-Z-]+' "flowero_gate/04_testing/042_test_cases.md" | head -1
# Should show: GATE-TC-
grep -oP 'GATE-TC-\d+' "flowero_gate/04_testing/044_regression_test_suite.md" | head -1
# Should show: GATE-TC-001

# Flowero Discover (expected: TC-###)
grep -oP '\*\*ID\*\*\s*\|\s*\KTC-\d+' "flowero_discover/04_testing/042_test_cases.md" | head -1
# Should show: TC-001
grep -oP 'TC-\d+' "flowero_discover/04_testing/044_regression_test_suite.md" | head -1
# Should show: TC-001

# If the prefixes don't match, you have a schema drift.
```

## Fix: Systematic Replacement

When mismatches are found, fix them with find-and-replace across all affected documents:

```python
from hermes_tools import patch

# Example: Guard documents used GUARD-TC-### but 042 used TC-G###
guard_fixes = {
    "GUARD-TC-001": "TC-G001",
    "GUARD-TC-010": "TC-G010",
    "GUARD-TC-020": "TC-G020",
    # ... all mismatched IDs
}

for old_id, new_id in guard_fixes.items():
    patch("04_testing/043_defect_report.md", old_id, new_id, replace_all=True)
    patch("04_testing/044_regression_test_suite.md", old_id, new_id, replace_all=True)
    patch("04_testing/045_coverage_report.md", old_id, new_id, replace_all=True)
    patch("06_security/061_security_test_report.md", old_id, new_id, replace_all=True)
```

## Verification

After fixes, re-run the audit script. All projects should show consistent ID prefixes between 042 and cross-referencing documents (043, 044, 045, 061).

Final check: `grep -oP 'GATE-TC-\d+' ...` should return IDs that actually exist in 042.
