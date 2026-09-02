# Observability Stack Reference

> Prometheus + Grafana + Loki + Promtail deployment on a Docker homelab.
> Verified on Panomete Platform Sprint 3 (2026-07-24).

## Architecture

```
┌─────────────┐     scrape      ┌─────────────┐
│ flowero-gate │ ◄────────────── │             │
│ :8000        │                 │  Prometheus  │
├─────────────┤     scrape      │  :9090       │
│flowero-disc. │ ◄────────────── │             │
│ :8999        │                 └──────┬──────┘
├─────────────┤     scrape             │
│flowero-guard │ ◄──────────────      │ query
│ :9000        │                 ┌──────▼──────┐
└─────────────┘                 │   Grafana   │
                                │   :3000     │
┌─────────────┐    push logs    │ grafana.    │
│  Promtail   │ ──────────────► │ panomete.com│
│  (agent)    │    ┌──────┐    └──────┬──────┘
└─────────────┘    │ Loki │           │ alerts
                   │:3100 │    ┌──────▼──────┐
                   └──────┘    │  Discord    │
                               │  Webhook    │
                               └─────────────┘
```

## Compose File Structure

Use a **separate compose file** from the platform services:

```yaml
# docker-compose.observability.yml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports: ["127.0.0.1:9090:9090"]
    volumes:
      - ./observability/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--storage.tsdb.retention.time=15d"
      - "--web.enable-lifecycle"
    networks: [shared-network]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:9090/-/healthy"]
      interval: 15s
      timeout: 5s
      retries: 3

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports: ["127.0.0.1:3000:3000"]
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD}
      GF_SERVER_ROOT_URL: https://grafana.panomete.com
      GF_AUTH_ANONYMOUS_ENABLED: "false"
      DISCORD_WEBHOOK_URL: ${DISCORD_WEBHOOK_URL}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./observability/grafana/provisioning:/etc/grafana/provisioning:ro
      - ./observability/grafana/dashboards:/var/lib/grafana/dashboards:ro
    networks: [shared-network]
    restart: unless-stopped

  loki:
    image: grafana/loki:3.4.2
    container_name: loki
    ports: ["127.0.0.1:3100:3100"]
    volumes:
      - ./observability/loki/loki-config.yml:/etc/loki/local-config.yaml:ro
      - loki_data:/loki
    command: -config.file=/etc/loki/local-config.yaml
    networks: [shared-network]
    restart: unless-stopped

  promtail:
    image: grafana/promtail:3.4.2
    container_name: promtail
    volumes:
      - ./observability/promtail/promtail-config.yml:/etc/promtail/config.yml:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml
    networks: [shared-network]
    restart: unless-stopped
    depends_on:
      loki: {condition: service_healthy}

  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    ports: ["127.0.0.1:3001:3001"]
    volumes: [uptime_kuma_data:/app/data]
    networks: [shared-network]
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
  loki_data:
  uptime_kuma_data:

networks:
  shared-network:
    external: true
    name: db-network
```

## Prometheus Config

```yaml
# observability/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

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
      - targets: ["flowero-guard:9000"]  # Management port!
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
```

## Grafana Provisioning Structure

```
observability/grafana/
├── provisioning/
│   ├── datasources/datasources.yml
│   ├── dashboards/dashboards.yml
│   ├── alerting/alert-rules.yml
│   └── contact-points/contact-points.yml
└── dashboards/
    ├── platform-overview.json
    ├── jvm-health.json
    └── gate-traffic.json
```

### Datasources provisioning

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
```

### Alert rules provisioning

Alert rules MUST use the actual datasource UID, not a placeholder. Get the UID after Grafana starts:

```bash
curl -sf -u admin:$GRAFANA_ADMIN_PASSWORD http://localhost:3000/api/datasources \
  | python3 -c "import sys,json; [print(d['uid']) for d in json.load(sys.stdin) if d['type']=='prometheus']"
```

Then use that UID in alert-rules.yml:

```yaml
apiVersion: 1
groups:
  - orgId: 1
    name: Panomete Platform
    folder: Panomete
    interval: 1m
    rules:
      - uid: service-down
        title: Service Down
        condition: C
        data:
          - refId: A
            relativeTimeRange: {from: 60, to: 0}
            datasourceUid: PBFA97CFB590B2093  # Actual UID from Grafana
            model:
              expr: up{job=~"flowero-.*"} == 0
              refId: A
          # ... reduce + threshold expressions
        for: 1m
        labels: {severity: critical}
        annotations: {summary: "Service {{ $labels.job }} is down"}
```

### Discord contact point

```yaml
apiVersion: 1
contactPoints:
  - orgId: 1
    name: Discord
    receivers:
      - uid: discord-webhook
        type: discord
        settings:
          url: ${DISCORD_WEBHOOK_URL}
```

## Loki Config

```yaml
# observability/loki/loki-config.yml
auth_enabled: false
server:
  http_listen_port: 3100
common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory
schema_config:
  configs:
    - from: "2024-01-01"
      store: tsdb
      object_store: filesystem
      schema: v13
      index: {prefix: index_, period: 24h}
limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  ingestion_rate_mb: 16        # Default 4MB/s is too low
  ingestion_burst_size_mb: 32
  per_stream_rate_limit: 16MB
  per_stream_rate_limit_burst: 32MB
analytics:
  reporting_enabled: false
```

## Promtail Config

```yaml
# observability/promtail/promtail-config.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0
positions:
  filename: /tmp/positions.yaml
clients:
  - url: http://loki:3100/loki/api/v1/push
scrape_configs:
  - job_name: docker-logs
    static_configs:
      - targets: [localhost]
        labels:
          job: docker-logs
          __path__: /var/lib/docker/containers/*/*.log
    pipeline_stages:
      - docker: {}
```

**Pitfall:** `docker_sd_configs` with `filters` is NOT supported in all Promtail versions.
Use filesystem log reading instead — it's simpler and more reliable.

## Keycloak Metrics Pitfall

Keycloak 26+ with `KC_METRICS_ENABLED=true` exposes metrics on the **management interface** (port 9000), NOT the main application port (8080). The Prometheus scrape target must use port 9000.

```yaml
# ✅ Correct
- job_name: "flowero-guard"
  metrics_path: "/metrics"
  static_configs:
    - targets: ["flowero-guard:9000"]

# ❌ Wrong — returns 404
- job_name: "flowero-guard"
  metrics_path: "/metrics"
  static_configs:
    - targets: ["flowero-guard:8080"]
```

## Nginx Routes

```nginx
# grafana.panomete.com
server {
    server_name grafana.panomete.com;
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

# status.panomete.com (Uptime Kuma — needs WebSocket upgrade)
server {
    server_name status.panomete.com;
    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

**Prometheus should NOT be exposed externally** — it has no built-in authentication.
Access via SSH tunnel: `ssh -L 9090:localhost:9090 flowero@remote.panomete.com`

## .env Additions

```bash
# Grafana
GRAFANA_ADMIN_PASSWORD=***

# Discord webhook for alerts
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/.../...
```
