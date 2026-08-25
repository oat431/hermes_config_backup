---
name: full-stack-repository-bootstrap
description: "Use when bootstrapping multiple full-stack repos from specs."
version: 1.0.0
author: "Hermes Agent"
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [full-stack, repository, bootstrap, scaffolding, go, nextjs, docker, git]
    related_skills: [github-repo-management, construction-docs, test-driven-development]
---

# Full-Stack Repository Bootstrap

## Trigger

Use when a user wants one or more repositories **set up only** from an implementation plan and design specification before PO-created issues/tasks drive feature implementation. This is a class-level bootstrap workflow for split backend/frontend projects, not a feature-implementation workflow.

## Output contract

A successful bootstrap leaves each repository with:

- a coherent language/framework scaffold matching the design documents;
- local configuration examples, build scripts, tests for the scaffold, migrations or schema placeholders where the plan explicitly calls for them, and Docker/Compose definitions;
- a README that explains the real setup commands and the boundary between scaffold and future feature work;
- an initialized, clean Git repository with `main` and `develop` aligned at the setup point;
- real build/test/lint/container verification output;
- **no remote or push** unless the user explicitly supplies/approves the remote operation.

Do not silently turn “just setup” into implementation of business stories. A health endpoint, route registration, or explicit `501 NOT_IMPLEMENTED` placeholder is acceptable when it proves the scaffold and makes the planned contract visible; business behavior is not.

## Workflow

### 1. Establish scope before editing

Read the phase plan and the key project contracts before creating files:

1. phase plan and repository/branch sections;
2. API specification;
3. database schema/DDL and ERD when the backend is stateful;
4. software architecture/deployment document;
5. frontend style/wireframe documents when a web repository is involved;
6. the workspace and both repository directories, including existing manifests, lockfiles, `.git`, generated app files, and ignored build output;
7. the port registry and infrastructure notes before assigning ports.

Run independent reads in parallel where possible. On Windows, if a directory search unexpectedly returns empty results, diagnose the path once and switch to a direct file read or a terminal-based listing; do not repeatedly retry the same broken path.

Record decisions from the documents rather than inventing defaults:

| Concern | Required source of truth |
|---|---|
| Backend/frontend ports | project port registry and confirmed infrastructure |
| Deployment topology | infrastructure documentation and user-confirmed reality |
| API paths and payloads | API specification |
| Tables, extensions, triggers | database schema/DDL |
| Framework and layering | ADR/SAD and phase plan |
| UI colors/components | style guide/wireframes |

If requirements and infrastructure conflict, stop the bootstrap at the boundary and report the conflict; do not “fix” the architecture by guessing.

### 2. Inspect before mutating

For each target directory, determine:

- whether it is empty, an existing scaffold, or an existing implementation;
- whether `.git` already exists and whether there are commits/remotes/branches;
- which package manager is implied by the existing lockfile (`bun.lock`, `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock`);
- whether `node_modules`, `.next`, Go binaries, or other generated artifacts are present;
- which files are user-authored and must be preserved.

Never delete a generated app, remove `.git`, or reinitialize a repository without inspecting it first. For an existing create-next-app directory, adapt the scaffold and preserve useful project metadata instead of recreating it.

### 3. Build the smallest useful scaffold

#### Go backend

Use the architecture’s package boundaries, normally:

```text
cmd/server/
internal/config/
internal/database/
internal/handler/
internal/server/
migrations/
```

Create only setup-level behavior:

- environment configuration with safe non-secret local defaults;
- Fiber application construction and a lightweight liveness endpoint;
- planned route registration, returning an explicit not-implemented response until sprint work exists;
- a database connection helper if the plan names sqlx/PostgreSQL;
- the initial migration only when the plan/design explicitly includes database setup;
- unit tests for configuration and route/scaffold behavior.

Keep direct dependencies in the main `require` block of `go.mod`. After adding imports, run `go mod tidy` and inspect the result; an empty or stale module often initially contains only indirect dependencies.

#### Next.js frontend

For a generated or empty Next.js app:

- preserve the existing App Router scaffold unless it is clearly disposable;
- set the application scripts to the registry port (for this project class, the FE port is commonly `3000`-range but must come from the registry);
- establish metadata, the shared Tailwind/DaisyUI theme, an honest setup landing page, `.env.example`, and production `next.config` settings;
- add the component and API work only when the user asked for implementation, not merely setup.

Do not make a browser-executed client fetch a Docker-only hostname such as `http://deerngo-bot:8008`. A service name is valid between containers, not from the user’s browser. At setup time, either defer browser API integration or document a browser-reachable API URL separately.

### 4. Make dependency installation reproducible

Use the package manager represented by the existing lockfile. When `package.json` changes:

1. run the package manager’s normal install once to regenerate the lockfile;
2. commit the updated lockfile;
3. verify that a clean/frozen install succeeds afterward.

A frozen install immediately after adding a dependency is expected to fail if the lockfile was not regenerated; the durable fix is to update the lockfile, not to remove the dependency or ignore the failure. Do not introduce a second lockfile merely to make installation pass.

For Go, use `go mod tidy` after the scaffold imports are present, then run the build/test commands from the repository root.

### 5. Add build and deployment scaffolding

Include, as appropriate:

- `.gitignore` and `.dockerignore` that exclude secrets, dependencies, framework caches, local binaries, and build output;
- a README with verified commands and the explicit setup/implementation boundary;
- a Makefile or equivalent repeatable commands for Go;
- a multi-stage Dockerfile;
- a repository-local Compose file using the assigned ports and the real external network name.

For Next.js standalone images, set `output: "standalone"` and copy `.next/standalone`, `.next/static`, and `public` into the runtime stage. Use a production-compatible runtime user and expose the assigned port.

Add `.dockerignore` **before** measuring Docker builds. Excluding `node_modules` and `.next` prevents a multi-hundred-megabyte local dependency/cache tree from becoming the Docker build context.

When Compose declares an external network, validate the YAML with `docker compose config` even if the developer machine does not have that deployment network. Do not create or destroy the homelab’s production network as part of local setup verification.

### 6. Initialize local Git safely

If a repository does not have `.git`:

```bash
git init -b main
git add .
git commit -m "chore(setup): scaffold <repository>"
git branch develop
```

If an existing repository already has history, commit only the setup changes with a Conventional Commit and inspect the current branch graph before changing branch pointers. For the normal fresh-repo case, `main` and `develop` should point at the same setup commit. If `develop` already exists and diverges, never force-move it without an explicit decision.

Do not configure `origin`, create GitHub repositories, push, or enable branch protection merely because the user mentioned a future push. Keep remote operations as a separate, explicit step.

### 7. Verify the artifact, not just the files

Run and record real output from both repositories.

#### Go

```bash
gofmt -w cmd internal
go test ./...
go vet ./...
go build -trimpath -o bin/<binary> ./cmd/server
docker compose config
docker build -t <image>:setup .
```

When practical, start the binary on a non-conflicting local port and exercise `/healthz` plus one planned route. The planned route should return the documented scaffold status, not a fabricated business response. Stop the temporary process afterward.

#### Next.js

```bash
bun install --frozen-lockfile   # or the lockfile’s native package manager
bun run lint
bun run typecheck              # if configured
bun run build
docker compose config
docker build -t <image>:setup .
```

When practical, run the built image on a temporary host port, fetch `/`, verify a recognizable page marker, and remove the smoke-test container. Do not leave temporary processes or containers running.

Finish with:

```bash
git status --short --branch
git diff --check
git log --oneline --decorate -3
```

A clean working tree and aligned branch pointers are part of the deliverable.

### 8. Handoff

Report:

- the exact local repository paths;
- what was scaffolded in each repository;
- ports and deployment assumptions taken from the registry/spec;
- verification commands and their real result;
- branch/commit state and whether a remote exists;
- explicit next step: PO creates issues/tasks, then Dev implements on feature branches.

Do not claim a push, remote creation, migration against a real database, or homelab deployment unless a tool returned verifiable evidence for that side effect.

## Pitfalls

- **Implementing stories during setup:** A scaffold is not Sprint 1–3. Leave business logic for issue-driven implementation.
- **Arbitrary ports:** Read the registry first. A port that “looks standard” can conflict with the user’s allocation.
- **Recreating an existing frontend:** Inspect and preserve the generated app, lockfile, and history.
- **Browser/container hostname confusion:** `deerngo-bot` works on `db-network`; it is not a browser-resolvable API URL.
- **Frozen lockfile too early:** Regenerate the lockfile after manifest edits, then verify frozen installation.
- **Huge Docker context:** Add `.dockerignore` before Docker builds; never send `node_modules`/`.next` as context.
- **Committing generated artifacts:** Ignore `.next`, `node_modules`, Go `bin/`, binaries, and local `.env` files.
- **External network mutation:** Compose config validation does not require creating the homelab network locally.
- **Branch drift:** Fresh setup branches may align; existing `develop` branches must be inspected before moving.
- **Unverified completion:** File creation is not verification. Build, test, lint, container-build, and smoke-test where practical.

## Reference material

- `references/deerngo-bootstrap.md` — worked, path-specific bootstrap matrix and the lockfile/Docker context lessons from the Deerngo Bot two-repository setup.
- `references/issue-driven-go-postgres-pr.md` — issue-to-PR workflow for Go backend slices with local Docker PostgreSQL, socket-auth integration tests, and evidence capture.
