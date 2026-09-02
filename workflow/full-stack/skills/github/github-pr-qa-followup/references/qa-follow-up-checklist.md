# QA Follow-Up Checklist

Use this after a reviewer comments on an open PR.

## Gather evidence

```bash
gh pr view <PR> --repo <OWNER>/<REPO> --json number,state,baseRefName,headRefName,headRefOid,mergeStateStatus,reviewDecision,statusCheckRollup,url

gh api repos/<OWNER>/<REPO>/pulls/<PR>/reviews --paginate
gh api repos/<OWNER>/<REPO>/pulls/<PR>/comments --paginate
gh api repos/<OWNER>/<REPO>/issues/<PR>/comments --paginate
gh pr diff <PR> --repo <OWNER>/<REPO>
```

## Go/Fiber verification matrix

```bash
make fmt
make test
make vet
make build
go test -race ./...
go mod tidy -diff
git diff --check
```

Required boundary checks commonly include:

- Empty JSON request: exact required-field messages and four details.
- Overlong handle/name: exact max-length message, separate from required.
- Repository failure: generic client response plus captured structured log.
- 100 requests accepted, 101st request returns `429 RATE_LIMITED`.

## Mandatory integration gate

The gate must fail without a DSN, then pass against an isolated PostgreSQL
instance:

```bash
make test-integration
DEERNGO_TEST_DATABASE_URL='<isolated-test-dsn>' make test-integration
```

On Windows with PostgreSQL in Docker, use TCP from the host or run compiled
Linux test binaries inside the database container when using the container's
Unix socket. Record the actual output; never report a failed run as passed.

## Publish follow-up

```bash
git status --short --branch
git push origin <feature-branch>
gh pr comment <PR> --repo <OWNER>/<REPO> --body-file follow-up.md
gh issue comment <ISSUE> --repo <OWNER>/<REPO> --body-file follow-up.md
gh pr view <PR> --repo <OWNER>/<REPO> --json headRefOid,mergeStateStatus,reviewDecision,state,url
```

Leave the PR open for fresh QA review; do not merge based only on local tests.
