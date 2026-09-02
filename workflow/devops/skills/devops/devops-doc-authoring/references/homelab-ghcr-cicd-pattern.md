# Homelab + GHCR + Docker Compose — CI/CD Pattern

Reference pattern from Deerngo Bot (DERNBOT-001). Applicable to any small project
deploying Docker containers to a homelab server via GitHub Actions.

## Architecture

```
GitHub (push to main)
  → GitHub Actions (lint, test, build)
    → GHCR (ghcr.io/org/repo:sha-abc1234 + :latest)
      → SSH to homelab
        → docker compose pull && up -d
          → health check curl
```

## Key Design Choices

- **SHA image tags** — immutable, enables rollback to any previous version
- **`latest` tag** — convenience for manual deploys
- **`appleboy/ssh-action`** — GitHub Action for SSH deploy step
- **`db-network`** — shared Docker network for database access
- **Host-level Nginx** — proxy to `127.0.0.1:PORT`, not container-level
- **Healthcheck in Compose** — gates deploy verification, enables `depends_on: condition: service_healthy`

## GitHub Actions Secrets Required

| Secret | Description |
|--------|-------------|
| `HOMELAB_HOST` | Server IP or Tailscale hostname |
| `HOMELAB_USER` | SSH username |
| `HOMELAB_SSH_KEY` | SSH private key |
| `GITHUB_TOKEN` | Auto-provided (no setup) |

## GitHub Actions Workflow Pattern (Go)

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:18
        env:
          POSTGRES_DB: test_db
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.24'
      - run: golangci-lint run
      - run: go test -v -cover ./...
      - run: go build -o /dev/null ./cmd/server

  build-and-push:
    needs: lint-and-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.HOMELAB_HOST }}
          username: ${{ secrets.HOMELAB_USER }}
          key: ${{ secrets.HOMELAB_SSH_KEY }}
          script: |
            cd ~/platform
            docker compose -f docker-compose.project.yml pull service-name
            docker compose -f docker-compose.project.yml up -d service-name
            sleep 5
            curl -sf http://localhost:PORT/health || exit 1
```

## Docker Compose Production Pattern

```yaml
services:
  service-name:
    image: ghcr.io/org/repo:latest
    container_name: service-name
    restart: unless-stopped
    ports:
      - "127.0.0.1:PORT:PORT"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    networks:
      - db-network
    depends_on:
      local-postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:PORT/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

networks:
  db-network:
    external: true
```

## Nginx Host-Level Proxy Pattern

```nginx
server {
    listen 80;
    server_name subdomain.panomete.com;

    location / {
        proxy_pass http://127.0.0.1:PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

## Rollback Procedure

```bash
# List available image tags
docker images ghcr.io/org/repo --format "{{.Tag}}\t{{.CreatedAt}}" | head -5

# Pin to known-good tag in compose file, then:
docker compose -f docker-compose.project.yml up -d
```
