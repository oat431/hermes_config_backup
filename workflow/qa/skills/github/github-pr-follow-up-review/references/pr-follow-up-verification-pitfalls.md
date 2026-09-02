# PR Follow-up Verification Pitfalls

Reusable notes from a Deerngo Bot re-review.

## Fiber limiter boundary probe

If code uses:

```go
standardAPI := app.Group("/api/v1", rateLimit(100))
webhookAPI := app.Group("/api/v1/webhooks", rateLimit(200))
```

assume the groups overlap until proven otherwise. The parent prefix middleware also matches the webhook path. Start a fresh server/app, send 201 webhook requests, and record the first rejected request. Correct non-overlapping behavior is requests 1–200 allowed and request 201 rejected.

Root and health routes may be outside API groups. If the security standard says all endpoints are rate-limited, send 101 requests to `/healthz` and either verify `429` or document an explicit exemption in the specification.

## Integration gate checks

1. Unset the database-test DSN and run `go test ./...`; scan output for `SKIP`.
2. Unset the DSN and run `make test-integration`; it should fail non-zero.
3. Inspect `make all`, `make test`, and `.github/workflows/`; a separate target is not a gate unless CI or the standard target invokes it.
4. Run the target with an isolated DSN.
5. Run package-parallel stress: `go test -p=2 -count=20 -failfast ./internal/repository ./internal/server`.

Tests that truncate a shared database and reuse fixed fixture handles can produce false `created=false`/HTTP 200 results or missing rows when packages overlap. Prefer isolated schemas/databases or unique fixtures; serialization is an acceptable short-term guard.

## Contract assertions

For create endpoints, assert the complete response contract: ID, all input/returned fields, timestamps, status, and normalization. Add a dedicated test for each rate-limit tier. Exact validation messages should be asserted at both top-level and detail level.

## Windows line endings

With Git for Windows `core.autocrlf=true`, `go mod tidy -diff` may show only CRLF/LF differences. Use a disposable LF-normalized copy for read-only verification. Do not rewrite the review worktree or treat line-ending-only output as a dependency defect.

## GitHub comment formatting (critical)

`gh pr comment --body 'line1\nline2'` posts **literal backslash-n** characters, not newlines. The comment renders as one long line with visible `\n` on GitHub. This also applies to `gh pr review --body` and `gh api -f body='...'` for long content.

**Correct approaches:**

1. **Heredoc with `gh pr comment`:**

```bash
gh pr comment 123 --body "$(cat <<'EOF'
## Title

Paragraph with **markdown**.

- Item 1
- Item 2
EOF
)"
```

2. **JSON payload via `execute_code`** (most reliable, especially on Windows):

```python
import json, subprocess
body = """## Title

Paragraph with **markdown**.

- Item 1
- Item 2"""

payload = json.dumps({"body": body})
subprocess.run(
    ["gh", "api", "repos/OWNER/REPO/issues/123/comments", "--method", "POST", "--input", "-"],
    input=payload, capture_output=True, text=True
)
```

3. **Fix an already-posted broken comment** (PATCH):

```python
import json, subprocess
payload = json.dumps({"body": corrected_body})
subprocess.run(
    ["gh", "api", "repos/OWNER/REPO/issues/comments/COMMENT_ID", "--method", "PATCH", "--input", "-"],
    input=payload, capture_output=True, text=True
)
```

Find comment IDs: `gh pr view N --json comments --jq '.comments[] | .id'`.

## Correcting an earlier verdict

When new evidence overturns an approval, post one clear correction stating that the prior verdict is superseded. Include the current head SHA, exact reproduction, requirement references, required fixes, and the remaining items that were verified as fixed.
