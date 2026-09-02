# Spring Boot Docker Deployment Patterns — Homelab

Generic patterns for deploying Spring Boot services (Gradle, Java 25, Boot 4.1)
on a Docker homelab behind Nginx + Cloudflare Tunnel. Applies to any service
that follows the Panomete Platform conventions.

---

## Multi-stage Dockerfile (Gradle)

```dockerfile
# ---- Stage 1: Build ----
FROM eclipse-temurin:25-jdk-noble AS build
WORKDIR /app
COPY gradlew gradlew.bat ./
COPY gradle/ gradle/
COPY build.gradle settings.gradle ./
RUN chmod +x gradlew && ./gradlew dependencies --no-daemon -q || true
COPY src/ src/
RUN ./gradlew bootJar --no-daemon

# ---- Stage 2: Runtime ----
FROM eclipse-temurin:25-jre-noble
WORKDIR /app

# Install curl for Docker healthchecks (NOT in JRE images!)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd -r flowero && useradd -r -g flowero flowero
COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE <port>
USER flowero

ENTRYPOINT ["java", \
    "-Xms128m", \
    "-Xmx192m", \
    "-XX:+UseZGC", \
    "-XX:MaxHeapFreeRatio=20", \
    "-XX:MinHeapFreeRatio=10", \
    "-jar", "app.jar"]
```

**Pitfall:** `eclipse-temurin:25-jre-noble` does NOT include `curl`. Without
the `apt-get install curl` line, Docker healthchecks using `curl` fail silently.
The container runs fine but shows "unhealthy" in Portainer.

---

## Compose service pattern

```yaml
services:
  my-service:
    build:
      context: ./myservice
      dockerfile: Dockerfile
    container_name: my-service
    ports:
      - "127.0.0.1:HOST_PORT:CONTAINER_PORT"   # MUST bind 127.0.0.1
    networks:
      - shared-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:CONTAINER_PORT/actuator/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 384M    # adjust per service

networks:
  shared-network:
    external: true
    name: db-network
```

**Key conventions:**
- Always bind to `127.0.0.1` — Nginx proxies externally
- Always join `db-network` — for inter-service communication
- Always include healthcheck — Portainer shows container health
- `start_period: 30s` — Spring Boot takes 10-20s to start

---

## Nginx server block pattern

```nginx
server {
    server_name myservice.panomete.com;

    location / {
        proxy_pass http://127.0.0.1:HOST_PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;    # Hardcoded, NOT $scheme
    }
}
```

**Pitfall:** `$scheme` is `http` behind Cloudflare Tunnel. Services that check
the protocol reject requests with "HTTPS required". Always hardcode `https`.

---

## Eureka standalone configuration

For the Eureka server itself (Flowero Discover):

```yaml
# application.yaml
server:
  port: 8999

eureka:
  instance:
    hostname: flowero-discover
  client:
    register-with-eureka: false    # standalone
    fetch-registry: false          # standalone
  server:
    enable-self-preservation: true
    eviction-interval-timer-in-ms: 5000
    renewal-percent-threshold: 0.85
    wait-time-in-ms-when-sync-empty: 0
```

**Dual-port trick:** Standard Eureka serves API + dashboard on one port. To
separate them for Nginx routing, use Docker port mapping:

```yaml
ports:
  - "127.0.0.1:8999:8999"   # REST API (services register here)
  - "127.0.0.1:3999:8999"   # Dashboard (Nginx proxies here)
```

Nginx routes `discovery.panomete.com` → `:3999`. Services register on `:8999`.

---

## Eureka client configuration (for services that register)

```yaml
# application.yaml
eureka:
  client:
    service-url:
      defaultZone: http://flowero-discover:8999/eureka/
  instance:
    prefer-ip-address: true
```

The service must join `db-network` to resolve `flowero-discover` by container name.

---

## JVM tuning for homelab

| Service Type | Xms | Xmx | Memory Limit | Notes |
|-------------|-----|-----|-------------|-------|
| Lightweight (Eureka) | 128m | 192m | 384M | In-memory, minimal |
| Medium (Gateway) | 128m | 384m | 512M | Reactive/Netty, efficient |
| Heavy (Keycloak) | 256m | 768m | 1G | JVM + Liquibase + Infinispan |

Use ZGC (`-XX:+UseZGC`) for low-latency GC. Set `MaxHeapFreeRatio=20` and
`MinHeapFreeRatio=10` to reduce memory footprint.

---

## Healthcheck verification

After deploying any service:

```bash
# Check container health status
docker ps --format '{{.Names}} | {{.Status}}' | grep <service>

# If shows "unhealthy" but service works:
docker exec <service> which curl
# If "not found" → add curl to Dockerfile

# Manual health check
curl -sf http://localhost:<PORT>/actuator/health && echo " ✅"
```

---

## Common issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Container "unhealthy" in Portainer | `curl` not in JRE image | Add `apt-get install curl` to Dockerfile |
| 502 from Nginx | Service not responding on port | Check container status, check port binding |
| "HTTPS required" (403) | `$scheme` is `http` behind Cloudflare | Hardcode `X-Forwarded-Proto https` in Nginx |
| Service can't reach DB | Not on `db-network` | Add `networks: [shared-network]` to compose |
| Service can't resolve other services | Not on `db-network` | Same — join the shared network |
| Port conflict | Another service using the port | `ss -tlnp | grep <PORT>` to check |
| Slow startup | First-boot initialization | Normal — wait 30s. Check `start_period` in healthcheck |
