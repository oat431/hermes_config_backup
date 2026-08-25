---
name: homelab-microservice-deployment
description: Deploy and configure containerized microservices on a Docker-based homelab — Keycloak, Spring Cloud Gateway, Eureka, Nginx + Cloudflare tunnel, Docker Compose multi-service management.
triggers:
  - deploying a new service to the homelab
  - configuring Keycloak / OAuth2 / OIDC
  - setting up Spring Cloud Gateway or Eureka
  - Docker Compose for multi-service platforms
  - Nginx reverse proxy behind Cloudflare
  - troubleshooting container healthchecks or networking
  - consolidating bundled databases into shared infrastructure
  - connecting containers to db-network
  - Infisical deployment or configuration
  - OTS / one-time-secret deployment
  - migrating bundled Redis/Valkey/PostgreSQL to shared infrastructure
  - SearXNG configuration or rate limiting
  - MCP server pointing at homelab services
  - Tailscale routing for local development tools
---

# Homelab Microservice Deployment

Deploy and configure containerized microservices on a Docker homelab server behind Nginx + Cloudflare Tunnel.

## Core Patterns

### 1. Docker Network Convention

All services join a shared external network `db-network`. Container-to-container communication uses **container names** as hostnames.

```yaml
# Every compose file includes:
networks:
  shared-network:
    external: true
    name: db-network
```

**Never use `host.docker.internal` on Linux** — it's a Docker Desktop feature. Use container names on the shared network instead.

### 2. Port Binding Convention

All services bind to `127.0.0.1` — Nginx proxies externally. Never expose to `0.0.0.0`.

```yaml
ports:
  - "127.0.0.1:8001:8080"   # ✅ localhost only
  # - "8001:8080"            # ❌ exposed to LAN
```

**Exception:** When a service needs direct Tailscale access (e.g., MCP tools on the host machine), bind to `0.0.0.0`. UFW blocks public access by default — only Tailscale peers can reach it. Example: SearXNG for MCP integration.

### 3. Nginx + Cloudflare Tunnel Pattern

Cloudflare terminates TLS. Nginx receives HTTP via the tunnel. Always hardcode `X-Forwarded-Proto: https` — `$scheme` would be `http` since Nginx receives HTTP from the tunnel.

```nginx
server {
    server_name myservice.panomete.com;
    location / {
        proxy_pass http://127.0.0.1:PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;  # Hardcoded, not $scheme
    }
}
```

DNS is automatic — `*.panomete.com` wildcard routes everything through the Cloudflare tunnel. No manual DNS records needed for new subdomains.

### 4. Healthcheck Pattern

Tool availability varies by base image — never assume:

| Base Image | `wget` | `curl` | `which` |
|------------|:------:|:------:|:-------:|
| Alpine (`*-alpine`) | ✅ (busybox) | ❌ | ❌ |
| Ubuntu/Noble (`*-noble`) | ❌ | ❌ | ❌ |
| `grafana/grafana` | ✅ | ✅ | ✅ |
| `prom/prometheus` | ✅ | ❌ | ✅ |
| `grafana/loki` | ✅ | ❌ | ✅ |
| `louislam/uptime-kuma` | ❌ | ✅ | ✅ |
| `infisical/infisical` | ❌ | ❌ | ❌ |
| Keycloak | ❌ | ❌ | ❌ |

**When `wget` is available (Alpine/busybox):**
```yaml
healthcheck:
  test: ["CMD", "wget", "-qO-", "http://localhost:PORT/health"]
```

**When `curl` is available:**
```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -sf http://localhost:PORT/health > /dev/null"]
```

**When neither is available (Keycloak, etc.):**
```yaml
healthcheck:
  test: ["CMD-SHELL", "timeout 5 bash -c '</dev/tcp/localhost/PORT' || exit 1"]
```

**When nothing is available (Infisical, etc.):**
Override with `test: ["CMD-SHELL", "exit 0"]` or remove healthcheck entirely.

### 5. .env for Secrets

Never put passwords in compose YAML. Use `.env` file at `~/platform/.env` (chmod 600). Compose references with `${VAR_NAME}` or `${VAR_NAME:-default}`.

### 6. Compose YAML Structure Pitfall

When appending a new service to an existing compose file, Python/yaml.dump is safer than shell heredoc append — heredoc append can nest the new service under the wrong key (e.g., under `networks:` instead of `services:`).

## Keycloak 26+ Pitfalls

See `references/keycloak-pitfalls.md` for the full list. Critical ones:

- `KC_PROXY=edge` is DEPRECATED → use `KC_PROXY_HEADERS=xforwarded`
- `KEYCLOAK_ADMIN` is DEPRECATED → use `KC_BOOTSTRAP_ADMIN_USERNAME`
- Bootstrap admin is ALWAYS temporary → create permanent admin via Admin Console
- `KC_CACHE=local` is REQUIRED for single-node (JGroups clustering timeout without it)
- Realm `sslRequired` must be `none` when behind Cloudflare (Nginx sends HTTP)
- Docker bind mount creates a DIRECTORY if the source file doesn't exist → create the file BEFORE starting the container

## Spring Cloud Gateway + Eureka Pattern

### Gateway compose environment (verified)

```yaml
environment:
  SERVER_PORT: "8000"
  MANAGEMENT_SERVER_PORT: "8000"    # Merge actuator onto main port
  SPRING_PROFILES_ACTIVE: prod
  # JWT — realm name must match, not "flowerogate" or other legacy names
  JWT_ISSUER_URI: https://auth.panomete.com/realms/panomete
  JWT_JWK_SET_URI: https://auth.panomete.com/realms/panomete/protocol/openid-connect/certs
  # Valkey — container name + password (not host.docker.internal)
  REDIS_HOST: local-valkey
  REDIS_PORT: "6379"
  REDIS_PASSWORD: ${VALKEY_PASSWORD}
  REDIS_SSL: "false"
  # Eureka — enable + correct URL (not eureka:8761)
  EUREKA_CLIENT_ENABLED: "true"
  EUREKA_URI: http://flowero-discover:8999/eureka
  # Disable features not yet needed
  SPRING_AUTOCONFIGURE_EXCLUDE: org.springframework.cloud.circuitbreaker.resilience4j.Resilience4JAutoConfiguration
  OTLP_ENABLED: "false"
  # SecurityConfig requires this — no default in code
  APP_POST_LOGIN_REDIRECT_URL: ${POST_LOGIN_REDIRECT_URL}
  KEYCLOAK_GATEWAY_SECRET: ${KEYCLOAK_GATEWAY_SECRET}
```

### Gateway Dockerfile (Alpine — uses wget for healthcheck)

```dockerfile
FROM eclipse-temurin:25-jdk-alpine AS builder
WORKDIR /app
COPY gradlew gradlew.bat settings.gradle build.gradle ./
COPY gradle/ gradle/
RUN chmod +x gradlew && ./gradlew dependencies --no-daemon 2>/dev/null || true
COPY src/ src/
RUN ./gradlew bootJar --no-daemon -x test

FROM eclipse-temurin:25-jre-alpine
RUN addgroup -S flowero && adduser -S flowero -G flowero
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar
EXPOSE 8000
USER flowero
# Alpine has wget via busybox — no curl install needed
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:8000/actuator/health/liveness || exit 1
ENTRYPOINT ["java", "-XX:+UseZGC", "-XX:MaxRAMPercentage=75.0", "-jar", "app.jar"]
```

**Key difference from Ubuntu-based images:** Alpine (`jre-alpine`) has `wget` via
busybox but NOT `curl`. Ubuntu (`jre-noble`) has neither. Use `wget` for Alpine
healthchecks, or `apt-get install curl` for Ubuntu.

### Gateway routing (application.yaml)

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: blog
          uri: lb://cute-gufo              # Eureka service name
          predicates: [Path=/api/blog/**]
          filters:
            - StripPrefix=1                # /api/blog/posts → /posts
            - RemoveRequestHeader=Authorization
            - name: RequestRateLimiter
              args:
                key-resolver: "#{@ipKeyResolver}"
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 200
        # ... more routes
```

### Gateway prerequisites checklist

Before deploying Gate, verify:
- [ ] Guard healthy (JWKS endpoint reachable)
- [ ] Discover healthy (Eureka registry available)
- [ ] Valkey healthy (password known)
- [ ] `.env` has: `VALKEY_PASSWORD`, `KEYCLOAK_GATEWAY_SECRET`, `POST_LOGIN_REDIRECT_URL`
- [ ] `flowero-gateway` OAuth2 client registered in Keycloak `panomete` realm
- [ ] Nginx block for `api.panomete.com` created
- [ ] Port 8000 free

### Gateway 401 behavior

- **Browser request** (`Accept: text/html`) → 302 redirect to Keycloak login
- **API request** (no token) → 401 JSON body
- **API request** (valid JWT) → route to backend via Eureka → 502 if no backend registered (expected in Phase 1)

### Post-login redirect URL

`SecurityConfig` uses `@Value("${app.post-login-redirect-url}")` with NO default.
If `POST_LOGIN_REDIRECT_URL` is not set in `.env`, the app crashes on startup.
Always set it before deploying Gate.

## Repository Architecture

**NOT a monorepo.** Each service has its own GitHub repo. CI/CD workflows live inside each repo (not a shared `.github/workflows/` at root).

```
oat431/flowero-guard      → .github/workflows/{ci,deploy}.yml
oat431/flowero-discovery  → .github/workflows/{ci,deploy}.yml
oat431/flowero-gateway    → .github/workflows/{ci,deploy}.yml
```

Each repo gets its own `TS_AUTH_KEY` and `HOMELAB_SSH_KEY` secrets (duplicated across repos).

## High-Risk Boundary (User Handles)

The user handles these manually — never automate:
- Passwords, API keys, SSH keys
- `.env` file edits with secrets
- UFW firewall rules
- Portainer admin password
- rclone OAuth re-authentication

Everything else (container lifecycle, DB provisioning, Nginx configs, realm JSON, CI/CD workflows) the assistant can handle.

## Obsidian Documentation Pattern

Operational knowledge lives in Obsidian at `F:\obsidian_note\oralita_md\home-lab-installation\`, NOT in the spec folder. Structure:

```
home-lab-installation/
├── database_component/     # PostgreSQL, Valkey, MongoDB
├── microservice_component/ # Keycloak, Discovery, Gateway
├── deployment/             # CI/CD, Tailscale setup
└── essential_component/    # Nginx, Cloudflare, Tailscale
```

Each service gets a full-detail self-contained note with: What & Why, Setup, Deploy, Access, Common Commands, Configuration, Troubleshooting, Project Structure, Related.

## Deployment Order

For Spring Cloud microservice platforms, deploy in dependency order:
1. Databases (PostgreSQL, Valkey) — already running
2. Identity provider (Keycloak) — needs DB only
3. Service registry (Eureka) — standalone, no deps
4. API Gateway — depends on all above

**Pitfall:** Deploying Gateway before Discovery forces hardcoded routes that must
be rewritten later. Always deploy Discovery first — it's standalone and takes
30 seconds to build.

## Observability Stack Pattern

See `references/observability-stack.md` for the full Prometheus + Grafana + Loki + Promtail deployment.

### Quick Summary

Deploy as a **separate compose file** (`docker-compose.observability.yml`) to keep observability isolated from platform services.

| Service | Port | Domain | Purpose |
|---------|:----:|--------|---------|
| Prometheus | 9090 | Internal only | Scrape metrics from all services |
| Grafana | 3000 | `grafana.panomete.com` | Dashboards + alerts |
| Loki | 3100 | Internal | Log aggregation |
| Promtail | — | Internal | Tail container logs → Loki |
| Uptime Kuma | 3001 | `status.panomete.com` | Uptime monitoring |

### Key Pitfalls

1. **Prometheus target "down" with 404** — Spring Boot needs `micrometer-registry-prometheus` dependency AND `prometheus` in `management.endpoints.web.exposure.include`. Without the dependency, the endpoint returns 404.

2. **Keycloak metrics on management port 9000, NOT main port 8080** — With `KC_METRICS_ENABLED=true`, metrics are at `http://container:9000/metrics`. Prometheus scrape target must use port 9000.

3. **Promtail `docker_sd_configs` with filters fails** — Use filesystem log reading instead:
   ```yaml
   scrape_configs:
     - job_name: docker-logs
       static_configs:
         - targets: [localhost]
           labels: {job: docker-logs, __path__: /var/lib/docker/containers/*/*.log}
       pipeline_stages:
         - docker: {}
   ```

4. **Loki ingestion rate limit exceeded** — Default is 4MB/s. Increase in loki-config.yml:
   ```yaml
   limits_config:
     ingestion_rate_mb: 16
     ingestion_burst_size_mb: 32
   ```

5. **Grafana alert rules "data source not found"** — Alert rules need the actual Prometheus datasource UID, not a placeholder. Get it via:
   ```bash
   curl -sf -u admin:$GRAFANA_ADMIN_PASSWORD http://localhost:3000/api/datasources | python3 -c "import sys,json; [print(d['uid']) for d in json.load(sys.stdin) if d['type']=='prometheus']"
   ```

6. **Keycloak healthcheck — no tools in image** — Keycloak image has no curl, wget, or even `which`. Use TCP check:
   ```yaml
   healthcheck:
     test: ["CMD-SHELL", "timeout 5 bash -c '</dev/tcp/localhost/8080' || exit 1"]
   ```

7. **Uptime Kuma healthcheck — `wget` not found** — The `louislam/uptime-kuma` image does NOT have `wget` (unlike Prometheus/Grafana/Loki which do). The default image healthcheck uses `wget` and permanently fails with `exec: "wget": executable file not found in $PATH`. Fix by overriding in compose:
   ```yaml
   uptime-kuma:
     healthcheck:
       test: ["CMD-SHELL", "curl -sf http://localhost:3001 > /dev/null"]
       interval: 15s
       timeout: 5s
       retries: 3
   ```
   `curl` IS available in the Uptime Kuma container. Container will go from `unhealthy` to `healthy` within one check interval after recreating.

### Prometheus Scrape Config (verified)

```yaml
scrape_configs:
  - job_name: "flowero-gate"
    metrics_path: "/actuator/prometheus"
    static_configs:
      - targets: ["flowero-gate:8000"]
  - job_name: "flowero-discover"
    metrics_path: "/actuator/prometheus"
    static_configs:
      - targets: ["flowero-discover:8999"]
  - job_name: "flowero-guard"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["flowero-guard:9000"]  # Management port, NOT 8080
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
```

## Backup Automation Pattern

See `references/backup-automation.md` for the full pg_dumpall + rclone + cron pattern.

### Quick Summary

Two scripts on the server at `/home/flowero/scripts/`:

| Script | Schedule | What | Retention |
|--------|----------|------|-----------|
| `backup-db.sh` | Daily 3:00 AM | `pg_dumpall` → gzip → rclone → OneDrive | 7 days local |
| `backup-volumes.sh` | Weekly Sunday 4:00 AM | Docker volumes → tar → gzip → rclone | 4 weeks local |

### Docker Volume Naming Pitfall

When using named volumes in Docker Compose, the actual volume name on disk is NOT the compose key. Always check with `docker volume ls` before writing backup scripts. The backup script's `VOLUMES` array must use the actual volume names.

## Service Consolidation Pattern (Shared Databases)

When a third-party application ships its own bundled database (Valkey, Redis, PostgreSQL), replace it with the shared instance on `db-network`. This reduces resource usage and centralizes data management.

### Steps

1. **Remove the bundled service** from the application's `docker-compose.yml`
2. **Remove its volume** (the shared instance has its own)
3. **Add the application to `db-network`**:
   ```yaml
   services:
     app:
       networks:
         - db-network
   networks:
     db-network:
       external: true
   ```
4. **Configure the connection** — point the app at the shared service. If the shared service has a DNS alias matching the old bundled service name (e.g., `local-valkey` has alias `valkey`), the app may work with zero config changes.
5. **Handle authentication** — shared services may have passwords the bundled ones didn't. Add credentials via `settings.yml`, `.env`, or environment variables.

### DNS Alias Trick

`local-valkey` on `db-network` has aliases `["local-valkey", "valkey"]`. Applications that reference `valkey:6379` resolve to the shared instance automatically — no config rename needed.

### Verifying Connection

```bash
# Check container is on the right network
docker ps --filter "name=APP" --format "{{.Networks}}"

# Check logs for connection errors
docker logs APP 2>&1 | grep -i "redis\|valkey\|connect\|refused"

# HTTP health check
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:PORT/
```

### Pitfalls

- **Remove `depends_on` healthcheck conditions when deleting bundled DBs** — compose files often declare `depends_on: {bundled-db: {condition: service_healthy}}`. Once the bundled service is removed, these blocks break `docker compose up` with "dependency failed to start". Delete them along with the service (external services can't satisfy `depends_on` anyway).
- **Multi-service apps may reference the DB from several services** — e.g., Penpot's backend AND exporter both declare `PENPOT_REDIS_URI`. Grep the whole compose for DB connection env vars and update every occurrence, not just the main app service.
- **File permissions (UID mismatch):** Container config files are often owned by the container's internal UID (e.g., SearXNG uses UID 977). Regular shell redirection (`>`) fails with "Permission denied". Use `sudo tee` instead:
  ```bash
  sudo tee /path/to/container-owned/config.yml > /dev/null << 'EOF'
  content here
  EOF
  ```
- **Env var overrides config file:** Some apps (like SearXNG) let environment variables override config files. If you set the connection in `settings.yml` AND as an env var, the env var wins — and may use the wrong key name (causing deprecation warnings). Pick one approach, not both.
- **Network name collision:** If the bundled service had the same container name as a shared service alias, Docker DNS conflicts. Rename the bundled service before removing it, or just remove it entirely.
- **SQLite-based apps cannot integrate:** Some apps (e.g., ByteStash uses `better-sqlite3`) are file-based with no network database support. Check `package.json` or container dependencies before attempting migration.
- **Port conflicts:** Always check occupied ports (`ss -tlnp | grep 127.0.0.1:`) before deploying. Common conflicts: port 3000 (Grafana), port 80 (system services).

### Documentation Workflow

When consolidating services, create a running guide in the user's **Obsidian vault** at `F:\obsidian_note\oralita_md\home-lab-installation\miscellaneous\`, NOT on the homelab server. The user reviews and edits docs locally in Obsidian — server-side docs get ignored.

Also update the port reference in `F:\obsidian_note\oralita_md\Quick Note\Home Lab App.md` when ports change.

### Sequential Review Preference

Process one service at a time. After each migration:
1. Start the container
2. Verify it's healthy (HTTP check, logs, DB connectivity)
3. Present the results to the user
4. **Wait for user approval** before proceeding to the next service

Do NOT batch all migrations in one shot — the user reviews each change before moving on.

### Port Conflicts

Port 3000 is commonly taken by Grafana. Always check before deploying:

```bash
ss -tlnp | grep -E "127\.0\.0\.1:" | awk '{print $4}' | sort -t: -k2 -n
```

Known port allocations on the Panomete homelab:

| Port | Service |
|------|---------|
| 3000 | Grafana |
| 3001 | Uptime Kuma |
| 5432 | PostgreSQL |
| 5984 | CouchDB |
| 6379 | Valkey |
| 7000 | AdGuard |
| 7004 | SearXNG |
| 7005 | Infisical |
| 7006 | OTS |
| 7007 | StirlingPDF |
| 7008 | ByteStash |
| 7009 | Penpot |
| 8000 | Spring Cloud Gateway |
| 8001 | Keycloak |
| 8999 | Eureka |
| 9000 | Portainer |
| 9001 | Penpot (alt, direct access) |
| 9090 | Prometheus |
| 27017 | MongoDB |

## CI/CD Migration: build → image (Critical Pattern)

Once CI/CD is set up, the server must ONLY pull pre-built images from GHCR. Never build on the server.

**Wrong (building on server):**
```yaml
flowero-discover:
  build:
    context: ./flowerodiscovery
    dockerfile: Dockerfile
```

**Correct (pulling from GHCR):**
```yaml
flowero-discover:
  image: ghcr.io/oat431/flowero-discovery:latest
```

**Migration steps:**
1. Update compose: replace `build:` with `image: ghcr.io/...`
2. Remove local repo copies from server (`rm -rf ~/platform/flowerodiscovery`, etc.)
3. Server layout becomes: `.env`, `docker-compose.platform.yml`, `docker-compose.observability.yml`, `observability/` config dir
4. Verify: `docker ps` should show GHCR image names, not local build names

**Why:** The user explicitly corrected this — "why you modified the local repo in the first place, i thought we just setup ci/cd". Source code lives in GitHub. CI builds + pushes to GHCR. Server pulls. No source code on server.

## CI/CD for Tailscale-Behind Servers

When the homelab resolves to a Tailscale IP, GitHub Actions can't SSH directly.
Use `tailscale/github-action` to bridge the runner onto the Tailnet temporarily,
then deploy via SSH. Deploy should be manual (`workflow_dispatch`) for single-dev
safety. See `references/tailscale-cicd-bridge.md` for the full workflow pattern.

### CI Pitfalls (Gradle projects)

- **`gradlew: Permission denied`** — Windows doesn't preserve Unix execute bits.
  Fix: `git update-index --chmod=+x gradlew` AND add `chmod +x gradlew` step in CI.
- **`Task 'checkstyleMain' not found`** — Only run if Checkstyle plugin is in `build.gradle`.
  If the project doesn't have it, remove the lint step entirely.
- **`.dockerignore` excluding needed files** — The Guard CI failed because
  `panomete-realm.json` was listed in `.dockerignore`. Always verify `.dockerignore`
  doesn't exclude files referenced by `COPY` in the Dockerfile.

### GHCR Package Visibility Pitfall

GHCR package visibility is **separate from repo visibility**. Making a repo public
does NOT make its container image public. You must also set the package to public:

1. Go to `https://github.com/<owner>/<repo>/packages`
2. Click the container package → **Package settings**
3. Under **Danger Zone** → **Change visibility** → **Public**

Or link the package to the repo (inherits visibility). Without this,
`docker pull` from a public repo still returns `unauthorized`.

### Docker Volume Naming

When using named volumes in Docker Compose, the actual volume name on disk is
`{project}_{service}_{volume}`, NOT just the volume key. Always check with
`docker volume ls` before writing backup scripts. Example:
- Compose key: `postgres_data` in project `platform`
- Actual name: `platform_postgres_data` or `postgres_postgres_data` (depends on compose setup)

## Backup Automation Pattern

See `references/backup-automation.md` for the full pg_dumpall + rclone + cron pattern.

## Related

- References: `references/keycloak-pitfalls.md`, `references/docker-compose-patterns.md`, `references/tailscale-cicd-bridge.md`, `references/searxng.md`, `references/infisical.md`, `references/ots.md`, `references/bytestash.md`, `references/penpot.md`, `references/couchdb.md`, `references/observability-stack.md`, `references/backup-automation.md`
- See also: `homelab-infra-audit` for server auditing before deployment
