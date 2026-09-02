# ByteStash — Homelab Configuration

> Verified on ByteStash latest, Docker 29.6.2, Panomete homelab.

## Container Details

| Item | Value |
|------|-------|
| Image | `ghcr.io/jordan-dalby/bytestash:latest` |
| Port | `0.0.0.0:7008` → `5000` (container) |
| Network | Default (own network, not `db-network`) |
| Storage | SQLite (`better-sqlite3`) — file-based |

## Database Integration: NOT Possible

ByteStash uses **SQLite** (`better-sqlite3` npm package). There is no network database support — no PostgreSQL, no Redis/Valkey. The bundled data is stored in a local file volume.

**Do NOT attempt to migrate ByteStash to `db-network` for database sharing.**

## Compose File

```yaml
services:
  bytestash:
    image: "ghcr.io/jordan-dalby/bytestash:latest"
    restart: always
    volumes:
      - ./data/snippets:/data/snippets
    ports:
      - "7008:5000"
    environment:
      BASE_PATH: ""
      JWT_SECRET: <generate-with-openssl-rand-base64-32>
      TOKEN_EXPIRY: 24h
      ALLOW_NEW_ACCOUNTS: "true"
      DEBUG: "false"
      DISABLE_ACCOUNTS: "false"
      DISABLE_INTERNAL_ACCOUNTS: "false"
      OIDC_ENABLED: "false"
```

## Pitfalls

1. **Placeholder values in default compose** — The template compose has `/your/snippet/path` and `JWT_SECRET: your-secret`. Both MUST be replaced before starting:
   - Volume: `./data/snippets:/data/snippets` (create dir first: `mkdir -p data/snippets`)
   - JWT secret: `openssl rand -base64 32`

2. **No `.env` file** — All config is in compose YAML environment block. Consider extracting `JWT_SECRET` to `.env` for consistency.

3. **SQLite means no backup via pg_dump** — Backup the volume mount directory (`./data/snippets`) instead.

## Verification Checklist

After deploying:

- [ ] `docker ps` shows container running
- [ ] `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:7008/` → 200
- [ ] Create a test snippet and verify it persists
