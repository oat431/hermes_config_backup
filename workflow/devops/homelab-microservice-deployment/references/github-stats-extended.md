# GitHub Stats Extended — Self-Hosted Deployment

## Overview

[github-stats-extended](https://github.com/stats-organization/github-stats-extended) generates dynamic GitHub stats SVG cards for READMEs. Self-hosting eliminates shared rate limits and allows custom cache durations. Deployed 2026-08-31 on the Panomete homelab.

| Property | Value |
|----------|-------|
| Port | 7010 (host) → 9000 (container) |
| Container | `github-stats-extended` |
| Source | `~/application/github-stats-extended/` |
| Branch | `release` (stable; `master` is unreleased/unstable) |
| License | MIT |
| Stack | Node.js 24, Express 5, pnpm monorepo (Turborepo) |

## Directory Layout

```
~/application/github-stats-extended/
├── Dockerfile              # Multi-stage: builder (pnpm install + build + deploy) → runner
├── docker-compose.yml      # Single service, port 7010:9000
├── .env                    # chmod 600 — PAT_1, CACHE_SECONDS, WHITELIST, etc.
├── .env.example            # Documented template
├── apps/backend/           # Express API server (entry: express.js)
├── apps/frontend/          # Card wizard UI (optional, not deployed)
└── packages/core/          # Shared SVG generation library
```

## Dockerfile (Verified Working)

```dockerfile
# Build stage
FROM node:24-alpine AS builder
RUN corepack enable && corepack prepare pnpm@10.34.1 --activate
WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/core/package.json packages/core/
COPY apps/backend/package.json apps/backend/
COPY tsconfig.base.json tsconfig.json ./
RUN pnpm install --frozen-lockfile
COPY packages/core packages/core
COPY apps/backend apps/backend
RUN pnpm --filter @stats-organization/github-readme-stats-core build
# Critical: --legacy without --prod (see pitfalls below)
RUN pnpm --filter ./apps/backend/ --legacy deploy ./deployment/

FROM node:24-alpine AS runner
WORKDIR /app
COPY --from=builder /app/deployment ./deployment
ENV NODE_ENV=production
ENV PORT=9000
EXPOSE 9000
WORKDIR /app/deployment
CMD ["node", "express.js"]
```

## docker-compose.yml

```yaml
services:
  github-stats:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: github-stats-extended
    restart: unless-stopped
    ports:
      - "7010:9000"
    env_file:
      - .env
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:9000/api/status/up"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
```

## Environment Variables (.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PAT_1` | ✅ Yes | — | GitHub PAT (classic: `repo` + `read:user`) |
| `CACHE_SECONDS` | No | 86400 (24h) | Card cache duration |
| `UPDATE_AFTER_HOURS` | No | 11 | Hours before proactive card regeneration |
| `DELETE_AFTER_HOURS` | No | 192 (8d) | Stop regenerating unused cards after this |
| `WHITELIST` | ⚠️ Critical | (allow all) | Comma-separated allowed GitHub usernames |
| `GIST_WHITELIST` | No | (allow all) | Comma-separated allowed Gist IDs |
| `EXCLUDE_REPO` | No | — | Repos excluded from stats |
| `FETCH_MULTI_PAGE_STARS` | No | false | Fetch all stars for accuracy |

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/api?username=X&...` | Stats card (SVG) |
| `/api/top-langs?username=X` | Top languages card (⚠️ NO trailing slash) |
| `/api/pin?username=X&repo=Y` | Repo pin card (⚠️ NO trailing slash) |
| `/api/gist?id=X` | Gist pin card (⚠️ NO trailing slash) |
| `/api/wakatime?username=X` | WakaTime stats card |
| `/api/status/up` | Health check (returns `"true"` or `"false"`) |
| `/api/status/pat-info` | PAT status (JSON: valid/expired/exhausted) |

## Pitfalls

### 1. PAT Expiration (Critical)
GitHub PATs expire. When cards show "Downtime due to GitHub API rate limiting" despite having a valid token:
- Check `/api/status/pat-info` — it returns `"expiredPATs": ["PAT_1"]` when expired
- Generate a new token at https://github.com/settings/tokens (classic token, scopes: `repo` + `read:user`)
- Update `.env` with the new token value
- Restart: `docker compose down && docker compose up -d`

**Never ask the user to paste the PAT token into chat.** They handle secrets manually per the high-risk boundary. Validate the token yourself by testing the `/api/status/pat-info` endpoint.

### 2. Healthcheck Returns `"false"` Initially
`/api/status/up` returns the string `"false"` when the PAT is invalid/expired, not a typical HTTP error. The wget `--spider` healthcheck considers HTTP 200 as healthy regardless of body content. For stricter checks, use `curl` with body inspection:
```bash
curl -sf http://localhost:9000/api/status/up | grep -q "true"
```

### 3. URL Routing: No Trailing Slashes
The Express router uses exact path matching. These URLs return 404:
```bash
❌ /api/top-langs/?username=X    # trailing slash = 404
❌ /api/pin/?username=X          # trailing slash = 404
```

Correct URLs:
```bash
✅ /api/top-langs?username=X
✅ /api/pin?username=X&repo=Y
```

The base `/api` endpoint accepts trailing slashes, but sub-routes do not.

### 4. Whitelist Configuration
If `WHITELIST` is set, ONLY those usernames are allowed. Requests for unlisted usernames return an SVG error card:
```svg
<text>This username is not whitelisted</text>
<text>Please deploy your own instance</text>
```

Either leave `WHITELIST` empty (allow all) or explicitly add every username you want to query. Common mistake: adding only the token owner's username, then trying to query other users.

### 5. Branch Selection
Always deploy from `release` branch, not `master`. `master` contains unreleased, potentially unstable code.

```bash
git clone --branch release --depth 1 https://github.com/stats-organization/github-stats-extended.git .
```

## Updating

```bash
cd ~/application/github-stats-extended
git fetch origin release
git checkout release
git pull origin release
docker compose build --no-cache
docker compose up -d
```

## Usage Examples

```markdown
<!-- Stats card -->
![GitHub stats](https://ghstatus.panomete.com/api?username=oat431&show_icons=true&theme=radical)

<!-- Top languages -->
![Top Langs](https://ghstatus.panomete.com/api/top-langs?username=oat431&theme=tokyonight)

<!-- Pin repo -->
![Repo](https://ghstatus.panomete.com/api/pin?username=oat431&repo=your-repo-name)
```

Note: Subdomain `ghstatus.panomete.com` requires DNS A record pointing to the server IP. Nginx config already exists at `/etc/nginx/sites-available/ghstatus.panomete.com`.
