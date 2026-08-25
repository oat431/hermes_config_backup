# Infisical — Homelab Configuration

> Verified on Infisical latest, Docker 29.6.2, Panomete homelab.

## Container Details

| Item | Value |
|------|-------|
| Image | `infisical/infisical:latest` |
| Port | `0.0.0.0:7005` → `8080` (container) |
| Network | `db-network` |
| DB | Shared `local-postgres` (PG18) |
| Cache/Queue | Shared `local-valkey` (Valkey 9, password-protected) |

## Database Setup

Infisical needs its own PostgreSQL database and user on the shared instance:

```bash
# Create user
docker exec local-postgres psql -U postgres -c "CREATE USER infisical WITH PASSWORD 'infisical';"

# Create database
docker exec local-postgres psql -U postgres -c "CREATE DATABASE infisical OWNER infisical;"

# Grant privileges
docker exec local-postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE infisical TO infisical;"
```

On first start, Infisical runs **Prisma migrations** automatically — creates ~763 tables. PG18 is fully compatible.

## Compose File (consolidated)

```yaml
# Infisical — using shared local-postgres and local-valkey on db-network

services:
  backend:
    container_name: infisical-backend
    restart: unless-stopped
    image: infisical/infisical:latest
    pull_policy: always
    env_file: .env
    ports:
      - 7005:8080
    environment:
      - NODE_ENV=production
    networks:
      - db-network

networks:
  db-network:
    external: true
```

## .env (key lines)

```bash
ENCRYPTION_KEY=<your-key>
AUTH_SECRET=<your-secret>

# Shared PostgreSQL on db-network (alias: postgres)
DB_CONNECTION_URI=postgres://infisical:infisical@postgres:5432/infisical

# Shared Valkey on db-network (alias: valkey) — with auth
REDIS_URL=redis://:PASSWORD@valkey:6379

# Website URL
SITE_URL=http://localhost:7005
```

## Pitfalls

1. **PG version mismatch is OK** — Original compose used `postgres:14-alpine`. Shared instance is PG18. Prisma handles the version difference fine.

2. **Port** — Mapped `7005:8080` per homelab port scheme (7000-8000 for self-hosted apps).

3. **SMTP error on startup** — `connect ECONNREFUSED 127.0.0.1:587` is expected when SMTP is not configured. Not a real error.

4. **Removed `depends_on`** — Original had `depends_on: [db, redis]` with health checks. Since shared infra is always running, these are unnecessary.

5. **Removed `version: "3"`** — Deprecated in modern Docker Compose. Remove it.

6. **`ALLOW_EMPTY_PASSWORD=yes` on bundled Redis** — Original Redis had no auth. Shared Valkey requires a password. The `REDIS_URL` must include it.

## Verification Checklist

After deploying:

- [ ] `docker ps` shows container on `db-network`
- [ ] `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:7005/api/status` → 200
- [ ] `docker exec local-postgres psql -U infisical -d infisical -c "\dt"` → shows tables
- [ ] `docker logs infisical-backend 2>&1 | grep -i "refused\|ECONN"` → only SMTP (expected)
