# OTS (One-Time Secret) — Homelab Configuration

> Verified on OTS v1.21.9, Docker 29.6.2, Panomete homelab.

## Container Details

| Item | Value |
|------|-------|
| Image | `ghcr.io/luzifer/ots:v1.21.9` |
| Port | `0.0.0.0:7006` → `3000` (container) |
| Network | `db-network` |
| Storage | Shared `local-valkey` (Valkey 9, password-protected) |

## Compose File (consolidated)

```yaml
# OTS (One-Time Secret) — using shared local-valkey on db-network

services:
  app:
    image: ghcr.io/luzifer/ots:v1.21.9
    restart: always
    environment:
      REDIS_URL: redis://:PASSWORD@valkey:6379/0
      # 168h = 1w
      SECRET_EXPIRY: "604800"
      # "mem" or "redis" (See README)
      STORAGE_TYPE: redis
    ports:
      - 7006:3000
    networks:
      - db-network

networks:
  db-network:
    external: true
```

## Pitfalls

1. **No .env file** — OTS original compose had no `.env`. Password is hardcoded in compose YAML. For consistency with other services, consider extracting to `.env`.

2. **`STORAGE_TYPE: redis` is required** — Without it, OTS uses `mem` (in-memory) storage. Secrets would be lost on restart.

3. **Valkey DB index** — Uses `/0` (default). If other services use different DB indexes, ensure no conflicts.

4. **Secret expiry** — Default is 1 week (`604800` seconds). Adjust `SECRET_EXPIRY` as needed.

## Verification Checklist

After deploying:

- [ ] `docker ps` shows container on `db-network`
- [ ] `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:7006/` → 200
- [ ] `docker logs ots-app-1 2>&1 | grep -i "started"` → `ots started`
- [ ] Create a test secret and verify it's stored in Valkey
