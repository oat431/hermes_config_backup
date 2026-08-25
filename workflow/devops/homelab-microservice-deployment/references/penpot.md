# Penpot — Homelab Configuration

> Verified on Penpot 2.16.2 (backend/frontend/exporter/mcp images), Docker 29.6.2, Panomete homelab.

## Container Details

| Item | Value |
|------|-------|
| Images | `penpotapp/{frontend,backend,exporter,mcp}:2.16` |
| Frontend ports | `127.0.0.1:7009:8080` + `9001:8080` (both — scheme port + default) |
| Public URI | `https://design.panomete.com` |
| Config dir | `~/application/penpot/docker-compose.yaml` |
| Assets volume | `penpot_assets` → `/opt/data/assets` (fs backend) |
| Mail catcher | `sj26/mailcatcher` at `127.0.0.1:1080` (dev SMTP, port 1025) |

## Shared DB Wiring (db-network)

Penpot ships bundled `penpot-postgres` (PG15) + `penpot-valkey` (8.1). Both removed; all five services join `db-network` instead.

### DB setup on shared PostgreSQL

```bash
docker exec local-postgres psql -U postgres -c "CREATE USER penpot WITH PASSWORD 'penpot';"
docker exec local-postgres psql -U postgres -c "CREATE DATABASE penpot OWNER penpot;"
docker exec local-postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE penpot TO penpot;"
```

### Backend env (the critical part)

```yaml
environment:
  # URI carries NO credentials — user/password are separate env vars!
  PENPOT_DATABASE_URI: postgresql://postgres/penpot
  PENPOT_DATABASE_USERNAME: penpot
  PENPOT_DATABASE_PASSWORD: penpot
  # Shared valkey with auth
  PENPOT_REDIS_URI: redis://:Saha_6462@valkey/0
  # Assets stay filesystem-based
  PENPOT_OBJECTS_STORAGE_BACKEND: fs
  PENPOT_OBJECTS_STORAGE_FS_DIRECTORY: /opt/data/assets
```

### TWO services need the Valkey URI

`penpot-backend` AND `penpot-exporter` both declare `PENPOT_REDIS_URI` — update both, not just the backend. The exporter silently fails websocket-driven renders without it.

## Pitfalls

1. **`depends_on` with `condition: service_healthy` on removed services breaks `docker compose up`** — the original compose had:
   ```yaml
   depends_on:
     penpot-postgres:
       condition: service_healthy
     penpot-valkey:
       condition: service_healthy
   ```
   Remove these blocks entirely when deleting the bundled DB services (external services can't satisfy `depends_on`).

2. **YAML anchors must survive the rewrite** — the stock compose defines `x-flags`, `x-uri`, `x-secret-key` anchors and merges them with `<< : [*penpot-flags, ...]`. Keep anchor definitions; only swap values inside them (e.g., `PENPOT_PUBLIC_URI`).

3. **Secret key placeholder** — stock compose ships `PENPOT_SECRET_KEY: change-this-insecure-key`. Regenerate:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(64))"
   ```

4. **Validate before starting** — `docker compose config --quiet` catches anchor/YAML breakage fast.

5. **Migrations run on backend startup** — first boot applies ~150 numbered migrations (`app.util.migrations - action="apply migration"`). Wait for `hint="welcome to penpot"` in logs before judging success; verify with `SELECT count(*) FROM information_schema.tables WHERE table_schema='public'` (~60 tables for 2.16).

6. **Mailcatch is dev-only** — `PENPOT_SMTP_HOST: penpot-mailcatch` with port 1025. Production needs a real SMTP provider; email verification flag can stay disabled meanwhile.

## Dual-Port Convention (user preference)

User asked to "use 7009 and keep 9001" — bind BOTH:
- `127.0.0.1:7009:8080` — scheme port, used by Nginx proxy
- `9001:8080` — app's default port, kept for direct/Tailscale access

Pattern: when a self-hosted app has a well-known default port outside the 7000-8000 scheme, keep both mappings.

## Verification Checklist

- [ ] `docker ps --filter "name=penpot"` → 5 containers Up on `db-network`
- [ ] Backend log contains `hint="welcome to penpot"` and no DB connect errors
- [ ] `docker exec local-postgres psql -U penpot -d penpot -c "\dt"` → ~60 tables
- [ ] `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:7009/` → 200
- [ ] Backend log shows `uri="redis://:Saha_6462@valkey/0"` (shared valkey, not bundled)
