# Backup Automation Pattern

Automated PostgreSQL backup + Docker volume backup with rclone to OneDrive.
Verified on Panomete Platform Sprint 2 (2026-07-24).

## Architecture

```
Cron (3:00 AM daily)  → backup-db.sh      → pg_dumpall → gzip → rclone → OneDrive
Cron (4:00 AM Sunday) → backup-volumes.sh  → docker run tar → rclone → OneDrive
```

## Database Backup Script (verified)

```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/home/flowero/backups/postgres"
LOG_FILE="/home/flowero/backups/backup.log"
RETENTION_DAYS=7
RCLONE_REMOTE="onedrive:panomete-backups/postgres"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
BACKUP_FILE="pg_dumpall_${TIMESTAMP}.sql.gz"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }
mkdir -p "$BACKUP_DIR" "$(dirname "$LOG_FILE")"
log "========== Backup started =========="

# Dump all databases (not just one)
if docker exec local-postgres pg_dumpall -U postgres | gzip > "$BACKUP_DIR/$BACKUP_FILE"; then
    SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    log "✅ Database dump complete: $BACKUP_FILE ($SIZE)"
else
    log "❌ Database dump FAILED"
    exit 1
fi

# Clean old local backups
DELETED=$(find "$BACKUP_DIR" -name "pg_dumpall_*.sql.gz" -mtime +$RETENTION_DAYS -delete -print | wc -l)
log "Deleted $DELETED old backup(s)"

# Sync to cloud
if rclone copy "$BACKUP_DIR" "$RCLONE_REMOTE" --include "pg_dumpall_*.sql.gz" --no-traverse 2>>"$LOG_FILE"; then
    log "✅ OneDrive sync complete"
else
    log "⚠️ OneDrive sync failed (backup still available locally)"
fi

TOTAL_LOCAL=$(find "$BACKUP_DIR" -name "pg_dumpall_*.sql.gz" | wc -l)
log "Local backups: $TOTAL_LOCAL"
log "========== Backup finished =========="
```

## Volume Backup Script (verified)

```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/home/flowero/backups/volumes"
LOG_FILE="/home/flowero/backups/backup.log"
RETENTION_WEEKS=4
RCLONE_REMOTE="onedrive:panomete-backups/volumes"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }
mkdir -p "$BACKUP_DIR"
log "========== Volume backup started =========="

# IMPORTANT: Use actual volume names from `docker volume ls`, NOT compose keys
VOLUMES=(
    "postgres_postgres_data"
    "valkey_valkey_data"
    "portainer_data"
)

for VOL in "${VOLUMES[@]}"; do
    log "Backing up volume: $VOL"
    if ! docker volume inspect "$VOL" >/dev/null 2>&1; then
        log "⚠️ Volume $VOL does not exist, skipping"
        continue
    fi
    if docker run --rm \
        -v "$VOL":/source:ro \
        -v "$BACKUP_DIR":/backup \
        alpine:latest \
        tar czf "/backup/${VOL}_${TIMESTAMP}.tar.gz" -C /source .; then
        SIZE=$(du -h "$BACKUP_DIR/${VOL}_${TIMESTAMP}.tar.gz" | cut -f1)
        log "✅ $VOL backed up ($SIZE)"
    else
        log "❌ Failed to backup $VOL"
    fi
done

# Clean old backups
DELETED=$(find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$((RETENTION_WEEKS * 7)) -delete -print | wc -l)
log "Deleted $DELETED old backup(s)"

# Sync to cloud
if rclone copy "$BACKUP_DIR" "$RCLONE_REMOTE" --include "*.tar.gz" --no-traverse 2>>"$LOG_FILE"; then
    log "✅ OneDrive sync complete"
else
    log "⚠️ OneDrive sync failed"
fi

log "========== Volume backup finished =========="
```

## Cron Setup (verified)

```bash
# Add to crontab — single command, not separate appends
(crontab -l 2>/dev/null; echo "# Panomete Platform Backups"; echo "0 3 * * * /home/flowero/scripts/backup-db.sh"; echo "0 4 * * 0 /home/flowero/scripts/backup-volumes.sh") | crontab -

# Verify
crontab -l
```

## Restore Procedures

### Restore Database

```bash
# 1. Stop services using the database
docker stop flowero-guard

# 2. Restore
gunzip -c /home/flowero/backups/postgres/pg_dumpall_YYYY-MM-DD_HHMMSS.sql.gz | \
  docker exec -i local-postgres psql -U postgres

# 3. Restart
docker start flowero-guard
```

### Restore Volume

```bash
# 1. Stop the service
docker stop flowero-guard

# 2. Restore
docker run --rm \
  -v volume_name:/target \
  -v /home/flowero/backups/volumes:/backup \
  alpine:latest \
  sh -c "cd /target && tar xzf /backup/volume_name_YYYY-MM-DD_HHMMSS.tar.gz"

# 3. Restart
docker start flowero-guard
```

## Pitfalls

- **Volume names are NOT compose keys** — `docker volume ls` shows actual names like `postgres_postgres_data`, not `postgres_data`. Always check before writing backup scripts. Compose prefixes the project name: `{project}_{service}_{volume}`.
- **`pg_dumpall` vs `pg_dump`** — Use `pg_dumpall` to capture ALL databases + roles. Use `pg_dump` for a single database.
- **rclone token expiry** — OAuth tokens expire. Test with `rclone lsd onedrive:` before relying on cron. Re-auth with `rclone config reconnect onedrive:`.
- **Retention is local only** — rclone doesn't delete old files from OneDrive. Add `rclone delete` with age filter if OneDrive storage is a concern.
- **Error handling** — Always check return codes from `pg_dumpall` and `rclone`. A silent failure means no backup. Log both success and failure.

## Verification

```bash
# Test database backup manually
/home/flowero/scripts/backup-db.sh

# Check OneDrive sync
rclone lsd onedrive:panomete-backups/postgres

# Check local retention
ls -la /home/flowero/backups/postgres/

# Check backup log
cat /home/flowero/backups/backup.log
```
