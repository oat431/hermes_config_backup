# PostgreSQL Database Setup for Keycloak

## Create role + database

```bash
docker exec -it local-postgres psql -U postgres << 'SQL'
CREATE ROLE keycloak WITH LOGIN PASSWORD 'YOUR_PASSWORD';
CREATE DATABASE keycloak
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    OWNER keycloak;
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
GRANT ALL ON SCHEMA public TO keycloak;
SQL
```

## Verify

```bash
docker exec local-postgres psql -U postgres -c "\l keycloak"
docker exec local-postgres psql -U postgres -c "\du keycloak"
```

## Cleanup (drop + recreate)

When realm import fails partway through, the database has corrupted/partial data.

```bash
docker stop flowero-guard
docker exec local-postgres psql -U postgres << 'SQL'
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='keycloak' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS keycloak;
CREATE DATABASE keycloak
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    OWNER keycloak;
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
GRANT ALL ON SCHEMA public TO keycloak;
SQL
```

## Pitfall: Collation mismatch

The PostgreSQL template database uses `en_US.utf8` (not `en_US.UTF-8`). If you get:
```
ERROR: new collation (en_US.UTF-8) is incompatible with the collation of the template database (en_US.utf8)
```
Use `template0` as the template:
```sql
CREATE DATABASE keycloak WITH ENCODING 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8' OWNER keycloak TEMPLATE template0;
```

## Pitfall: Database locked by active sessions

If `DROP DATABASE` fails with "database is being accessed by other users":
```sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'keycloak' AND pid <> pg_backend_pid();
```
