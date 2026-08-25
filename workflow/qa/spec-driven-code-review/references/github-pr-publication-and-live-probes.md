# GitHub PR Publication and Live-Boundary Verification

Use this reference when a specification-driven review is authorized to interact with GitHub or when a local build must be exercised beyond unit tests.

## 1. Determine whether a formal review state is possible

Before choosing `APPROVE` or `REQUEST_CHANGES`, compare the authenticated viewer to the PR author:

```bash
gh pr view <number> --json author,headRefOid,baseRefOid,baseRefName,headRefName
```

GitHub rejects a formal approval or change-request review submitted by the PR author for their own PR (`422`, `Review Can not request changes on your own pull request`). If the authenticated account owns the PR, submit an evidence-backed `COMMENT` review instead, clearly state that the requested verdict is changes requested, and explain that GitHub could not represent it as a blocking review state. Do not claim that a blocking review was posted.

## 2. Submit and verify an authorized review

When posting is explicitly authorized, use the authenticated `gh` CLI/API; GitHub MCP is unnecessary when `gh auth status` succeeds. Prefer one atomic review containing the summary and inline comments, anchored to the PR head SHA. Use `side=RIGHT` and the new-file line for changed-code comments.

After submission, read the review and inline comments back from GitHub and verify:

- review ID, URL, and `commit_id` equal the PR head SHA;
- returned state is the actual state (`COMMENTED` is expected for a self-authored PR);
- every intended inline comment exists with the expected path, line, and body;
- `gh pr checks` is reported accurately, including the explicit no-checks case;
- `reviewDecision` is not treated as evidence of a blocking decision when the reviewer is the PR author.

## 3. Exercise live boundaries, not only tests

For an HTTP/API PR, run the application against an isolated database or test service and probe the acceptance path:

1. health/readiness endpoint;
2. valid request and expected success status/envelope;
3. duplicate or normalized request and expected idempotency/upsert result;
4. empty/malformed/invalid-boundary requests and field-level errors;
5. operational controls required by the specification, especially rate-limit `N` and `N+1`, generic client errors, CORS/auth headers, body limits, and error logging.

Discard response bodies during high-volume probes so the shell/client does not fail on output handling. Remove only the probe's own fixtures afterward, or use a disposable database/schema. Record the exact observed status codes rather than inferring behavior from source inspection.

## 4. Classify verification honestly

Use separate labels for:

- default suite passed;
- uncached suite passed (`-count=1`);
- race/vet/build passed;
- database integration passed with an explicitly configured isolated DSN;
- integration skipped because the DSN/service was absent;
- unavailable tools or CI checks;
- no GitHub checks reported;
- review comment published versus formal blocking review published.

A green default test command that contains `t.Skip` is not database integration evidence. A PR description saying an integration test passed is a claim until independently reproduced.

## 5. Review summary language

When the authenticated reviewer owns the PR, use wording such as: "The technical verdict is changes requested; GitHub does not allow this account to submit a blocking review on its own PR, so the findings were posted as a COMMENTED review." Include links/IDs returned by GitHub and distinguish local verification from hosted CI status.

## 6. GitHub comment body formatting

When posting comments via `gh pr comment --body` or `gh api` from a terminal tool call, literal `\n` escape sequences in a shell string are **not** interpreted as newlines — they produce literal backslash-n characters in the GitHub comment body.

**Wrong** (produces literal `\n` in the comment):
```bash
gh pr comment 11 --body '## Title\n\nFirst paragraph\n\nSecond paragraph'
```

**Correct** — use `execute_code` with Python to pass a proper multi-line string:
```python
import subprocess
body = """## Title

First paragraph

Second paragraph"""
result = subprocess.run(
    ["gh", "pr", "comment", "12", "--body", body],
    capture_output=True, text=True
)
```

For `gh api` with `--input -`, the body must be valid JSON with real newlines:
```python
import json, subprocess
body = """## Title

Content here"""
payload = json.dumps({"body": body})
result = subprocess.run(
    ["gh", "api", "repos/OWNER/REPO/issues/comments/ID", "--method", "PATCH", "--input", "-"],
    input=payload, capture_output=True, text=True
)
```

After posting, always verify the comment rendered correctly by reading it back:
```bash
gh api repos/OWNER/REPO/issues/comments/ID --jq '.body' | head -5
```
