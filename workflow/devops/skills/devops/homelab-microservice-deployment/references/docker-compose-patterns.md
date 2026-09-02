# Docker Compose Patterns — Homelab Microservices

> Patterns verified on the Panomete Platform homelab (Docker 29.6.2, Compose v5.3.1, Ubuntu).

## Multi-Service Compose Structure

```yaml
services:
  flowero-guard:
    image: quay.io/keycloak/keycloak:latest
    container_name: flowero-guard
    ports:
      - "127.0.0.1:8001:8080"
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://local-postgres:5432/keycloak
      # ... env vars from .env
    volumes:
      - ./keycloak/panomete-realm.json:/opt/keycloak/data/import/panomete-realm.json:ro
    networks:
      - shared-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G

  flowero-discover:
    build:
      context: ./flowerodiscovery
      dockerfile: Dockerfile
    container_name: flowero-discover
    ports:
      - "127.0.0.1:8999:8999"
      - "127.0.0.1:3999:8999"
    networks:
      - shared-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8999/actuator/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
    restart: unless-stopped

  flowero-gate:
    build:
      context: ./flowerogate
      dockerfile: Dockerfile
    container_name: flowero-gate
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - REDIS_HOST=local-valkey
      - REDIS_PASSWORD=${VALKEY_PASSWORD}
      - EUREKA_CLIENT_ENABLED=true
      - EUREKA_URI=http://flowero-discover:8999/eureka
      # ... more env vars
    networks:
      - shared-network
    depends_on:
      - flowero-discover
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M

networks:
  shared-network:
    external: true
    name: db-network
```

## Adding a New Service Safely

When appending to an existing compose file, use Python YAML library — NOT shell heredoc append. Heredoc append can nest the service under the wrong YAML key.

```python
# Safe approach
import yaml
with open(path) as f:
    data = yaml.safe_load(f)
data["services"]["new-service"] = { ... }
with open(path, "w") as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
```

## Healthcheck Without curl

Alpine-based JRE images don't have `curl`. Options:
1. Install in Dockerfile: `RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*`
2. Use `wget` (Alpine busybox): `wget -qO- http://localhost:PORT/actuator/health`
3. Use `CMD-SHELL` in compose for shell features

## Spring Boot Profile Activation

```yaml
environment:
  SPRING_PROFILES_ACTIVE: prod
```

Prod profile (`application-prod.yaml`) overrides base config with env-var-driven values:
```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD:}
```

## Eureka Client Configuration for Gateway

```yaml
# In application-prod.yaml
eureka:
  client:
    enabled: true
    service-url:
      defaultZone: ${EUREKA_URI:http://flowero-discover:8999/eureka}
    registry-fetch-interval-seconds: 30
```

And in compose:
```yaml
EUREKA_CLIENT_ENABLED: "true"
EUREKA_URI: http://flowero-discover:8999/eureka
```
