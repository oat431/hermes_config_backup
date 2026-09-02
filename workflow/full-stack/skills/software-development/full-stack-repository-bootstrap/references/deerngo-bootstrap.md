# Deerngo Bootstrap Reference

## Source setup

- Workspace: `F:\projects\deerngo`
- Backend: `deerngo-bot`
- Frontend: `deerngo-web`
- Shared specs/plan: `F:\projects\project_spec\external_spec\deerngo_bot` and `F:\projects\project_spec\external_plan\phase1-deerngo-bot-mvp.md`
- Port registry: backend `8008`, frontend `3008`
- Deployment contract: Go + Next.js on homelab Docker `db-network`; existing PostgreSQL is external; streamer.bot remains on the Windows PC.

## Backend setup shape

The Go scaffold used Fiber v3 with:

```text
cmd/server/main.go
internal/config/
internal/database/
internal/handler/
internal/server/
migrations/001_initial_schema.up.sql
migrations/001_initial_schema.down.sql
Dockerfile
docker-compose.yml
Makefile
```

`/healthz` returned `200`, while planned business paths returned a JSON
`501 NOT_IMPLEMENTED` response. This made the API surface visible without
pretending the sprint stories were implemented.

The initial module had Fiber listed only as indirect and no source packages.
After adding the scaffold, the durable dependency repair was:

```bash
go get github.com/jmoiron/sqlx@v1.4.0 github.com/jackc/pgx/v5@v5.8.0
go mod tidy
gofmt -w cmd internal
go test ./...
go vet ./...
go build -trimpath -o bin/deerngo-bot ./cmd/server
```

## Frontend setup shape

The frontend already contained a create-next-app App Router repository with an
existing `bun.lock`, `.git`, `main`, and initial commit. It was adapted rather
than recreated. Setup changes established:

- Next.js scripts on port `3008`;
- TypeScript typecheck script;
- Tailwind 4 + DaisyUI 5 theme from the shared style guide;
- metadata and an honest setup landing page;
- `next.config.ts` with `output: "standalone"`;
- `.env.example`, Dockerfile, Compose file, and `.dockerignore`.

Adding `daisyui` changed `package.json`; running `bun install --frozen-lockfile`
before regenerating the lockfile failed with “lockfile had changes”. The fix
was:

```bash
bun install
bun install --frozen-lockfile
bun run lint
bun run typecheck
bun run build
```

The first frontend implementation attempt added a client-side scoreboard fetch,
but setup scope did not require business UI/API integration and a Docker-only
hostname would not be browser-resolvable. The final setup landing page defers
that integration to the sprint issue.

## Docker verification lessons

Both Compose files validated with:

```bash
docker compose config
```

Both Dockerfiles built successfully. A first frontend Docker build transferred
roughly `451 MB` because local `node_modules` and `.next` were in the context.
Adding `.dockerignore` reduced the context to under `1 KB` in the subsequent
build and is essential for this class of repository.

The local Docker host did not have the external `db-network`; that is not a
setup failure. Validate Compose syntax and image builds locally, but do not
create or mutate the production external network during bootstrap.

A temporary backend binary smoke test confirmed:

```text
GET /healthz -> 200 {"service":"deerngo-bot","status":"ok"}
GET /api/v1/scoreboard -> 501 NOT_IMPLEMENTED
```

A temporary frontend container smoke test confirmed the production image became
ready and `/` returned HTML containing `DEERNGO BOT`. Temporary processes and
containers were stopped/removed after verification.

## Git handoff state

For a fresh backend repo, initialize with `main`, commit the scaffold, and make
`develop` point at the same commit. For an existing frontend repo, preserve its
initial commit and add setup commits; align `develop` only after inspecting its
history. Leave remotes unset until the user explicitly asks to create/configure
and push to GitHub.
