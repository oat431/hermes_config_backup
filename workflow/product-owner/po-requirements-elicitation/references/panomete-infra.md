# Panomete Platform — Infrastructure Reference

> Snapshot as of 2026-07-24. Update when infra changes.

## Deployment Status

**Phase 1 (Foundation): ✅ DEPLOYED & VERIFIED (2026-07-24)**

| Service | Domain | Port | Technology | Status |
|---------|--------|------|-----------|--------|
| Flowero Guard | `auth.panomete.com` | 8001 | Keycloak (shared PostgreSQL 18) | ✅ Live |
| Flowero Discover | `discovery.panomete.com` | 8999 BE / 3999 FE | Spring Cloud Eureka | ✅ Live |
| Flowero Gate | `api.panomete.com` | 8000 | Spring Cloud Gateway + Valkey rate limiting | ✅ Live |

**Phase 2 (Foundation Hardening): 📋 Planned**

| Initiative | Components | Priority | Status |
|-----------|-----------|----------|--------|
| A — CI/CD + GHCR | GitHub Actions, GHCR (`ghcr.io/oat431/...`) | 🔴 Must | 📋 Planned |
| B — Observability | Prometheus (:9090, `metrics.panomete.com`), Grafana (:3000, `grafana.panomete.com`), Loki (:3100, internal) | 🔴 Must | 📋 Planned |
| C — Alerting | Grafana alerts → Discord webhook | 🟡 Should | 📋 Planned |
| D — Backup | `pg_dumpall` cron daily 3AM, 7-day retention, rclone → OneDrive | 🟡 Should | 📋 Planned |
| E — Uptime | Uptime Kuma (:3001, `status.panomete.com`) | 🟢 Nice | 📋 Planned |

**Phase 3 (Business Services): 🔲 Future**
- First business service TBD (DEC-008 deferred). Candidates: Cute Gufo (Blog), Fluffy Mouton (URL), Tiny Mchwa (Todo).

## Live Infrastructure (Pre-existing)

| Component | Status | Details |
|-----------|--------|---------|
| Docker + Compose | ✅ | All services run as containers |
| Cloudflare Tunnel | ✅ | TLS termination + external ingress |
| Nginx Reverse Proxy | ✅ | Subdomain-based routing |
| PostgreSQL 18 | ✅ | Shared DB, port 5432 |
| Valkey 9 | ✅ | Shared cache, port 6379 |
| MongoDB 8 | ✅ | Document store, port 27017 |
| SeaweedFS S3 | ✅ | Object storage, ports 8333/8888/9333 |
| Tailscale | ✅ | Remote access VPN |
| UFW + Fail2ban | ✅ | Host firewall |

## Business Services (Planned — Phase 3+)

| Service | Port BE | Port FE | Subdomain | Language |
|---------|---------|---------|-----------|----------|
| Cute Gufo (Blog) | 8005 | 3005 | blog.panomete.com | Go |
| Fluffy Mouton (URL) | 8002 | 3002 | short.panomete.com | TypeScript |
| Tiny Mchwa (Todo) | 8003 | 3003 | todo.panomete.com | TypeScript |
| Big Schwein (Ledger) | 8004 | 3004 | ledger.panomete.com | TypeScript |
| Shy Ardilla (Cook) | 8006 | 3006 | recipe.panomete.com | TypeScript |
| White Jelen (Hora) | 8007 | 3007 | hora.panomete.com | TypeScript |

## Traffic Flow

```
Internet → Cloudflare (TLS) → cloudflared → Nginx ─┬─ auth.panomete.com → Guard :8001
                                                    ├─ discovery.panomete.com → Discover :3999
                                                    └─ api.panomete.com → Gate :8000 → business APIs
```

## Tech Stack (Current)

| Layer | Technology | Version |
|-------|-----------|---------|
| Foundation language | Java | 25 |
| Framework | Spring Boot | 4.1.x |
| Build tool | Gradle | 9.5+ |
| Gateway | Spring Cloud Gateway | 2025.1.x |
| Discovery | Spring Cloud Netflix Eureka | latest |
| Identity | Keycloak | latest |
| CI/CD | GitHub Actions + GHCR | Phase 2 |
| Deployment | Docker Compose → k3s (Phase 3+) | — |

## Spec Repository

- Path: `F:\projects\project_spec\`
- Templates: `template/`
- Plans: `plan/` (phase plans go here)
- Platform umbrella: `spec/panomete_platform/`
- Service specs: `spec/flowero_guard/`, `spec/flowero_discover/`, `spec/flowero_gate/`
- Meeting minutes: `spec/meeting-minute/`

## Key Design Decisions

1. Guard IS Keycloak — no wrapper service. Gate validates JWT locally against JWKS.
2. Nginx is the edge proxy. Gate is internal only (port 8000) behind Nginx.
3. Foundation services get own subdomains routed by Nginx. Gate only routes business APIs.
4. TLS terminated at Cloudflare. Internal traffic is plain HTTP.
5. Shared PostgreSQL 18 + Valkey 9 — no dedicated DB containers for foundation services.
6. Observability is Phase 2 (Prometheus + Grafana + Loki). Uptime Kuma for basic monitoring.
7. CI/CD deploy model: manual approval (`workflow_dispatch`), NOT auto-deploy on push.
8. Alerting channel: Discord webhook.
9. Backup: daily `pg_dumpall` at 3 AM, 7-day retention, rclone to OneDrive.
