# Windows Go Review Verification

Use this reference when reviewing Go repositories on Windows, especially with Git Bash/MSYS and `core.autocrlf=true`.

## Distinguish module drift from line-ending noise

A clean checkout may contain CRLF working-tree files even though the committed blobs use LF. `go mod tidy -diff` can then print a diff containing only CRLF-to-LF changes. Do not report that as dependency drift. A production import that is still marked `// indirect`, or a real dependency/version change, is different and should remain a finding.

For a trustworthy read-only module check, build a disposable copy from the exact Git blobs rather than from the autocrlf-converted worktree:

```bash
python - "$tmp" <<'PY'
import pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1]); root.mkdir()
for name in subprocess.check_output(["git", "ls-files"], text=True).splitlines():
    out = root / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(subprocess.check_output(["git", "show", f"HEAD:{name}"]))
PY
(cd "$tmp" && go mod tidy -diff)
```

Record the logical result and the line-ending caveat separately. Never run `go mod tidy` without `-diff` during a review.

## Keep probes out of the review worktree

Do not extract `git archive | tar -x` into the repository itself on Windows. MSYS tar may convert LF files to CRLF, making every tracked file appear modified even though the content is semantically unchanged. Use a disposable directory outside the worktree, or populate it byte-for-byte with `git show` as above. Check `git status --short --branch` before and after any probe; if a verification command dirties the tree, restore only the incidental changes after confirming the initial worktree was clean.

## Database fixture probes

For PostgreSQL integration tests that call `TRUNCATE` and reuse fixed identifiers:

- Run the project's documented integration target sequentially first.
- Then, if supported parallelism is relevant, run `go test -p=2 -count=...` for the affected packages against the isolated test database.
- If concurrent runs fail because tests erase one another's rows, classify this as test-fixture isolation/flakiness, not automatically as a production defect.
- Do not leave probe data or temporary directories in the worktree; remove only artifacts created by the review and confirm `git status` is clean.

## Report the evidence precisely

- State whether the module check passed on exact committed bytes.
- If the normal Windows checkout shows only CRLF noise, do not call it a PR defect.
- Keep real functional findings (for example, a missing direct dependency) separate from environment-specific line-ending behavior.
- Include the final clean-worktree check in JSON-only review verification.
