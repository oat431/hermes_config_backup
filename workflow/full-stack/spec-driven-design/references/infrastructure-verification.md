# Infrastructure Verification Commands

> Run these AFTER the grill session but BEFORE writing any design document. Grill questions extract intent; these commands reveal reality.

## When to Use

- User has a homelab or existing server
- User provides SSH access or says "check it yourself"
- PO meeting minute describes deployment but you haven't verified it physically
- Multiple machines involved (e.g., "Windows PC" + "homelab server")

## Quick Verification (5 commands, 30 seconds)

```bash
# 1. What's running?
ssh user@host "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'"

# 2. What networks exist and who's on them?
ssh user@host "docker network ls --format 'table {{.Name}}\t{{.Driver}}'"
ssh user@host "docker network inspect db-network --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{println}}{{end}}'"

# 3. What databases already exist?
ssh user@host "docker exec local-postgres psql -U postgres -l"

# 4. How is the tunnel/proxy configured?
ssh user@host "systemctl status cloudflared 2>/dev/null | head -5"
ssh user@host "docker ps | grep -i nginx"

# 5. What's the machine's IP?
ssh user@host "hostname -I"
```

## Pre-Flight: Port Registry (before SSH)

Before running any SSH commands, read the user's port registry to understand their allocation scheme:

```bash
# Common location for homelab port registries
cat "F:\obsidian_note\oralita_md\Quick Note\Home Lab App.md"
# Or ask the user: "Do you have a port allocation document?"
```

**Why:** Users with homelabs have strict port ranges (e.g., 8000-9000 BE, 3000-4000 FE, 7000-8000 self-hosted). Assigning 8080 when 8008 is next available breaks their convention and requires rewrites.

**What to extract:**
- Port ranges by category (BE, FE, self-hosted, infra)
- Next available port in each range
- Naming convention (project names, subdomain patterns)

## What to Look For

| Check | Why It Matters | Example Finding |
|-------|---------------|-----------------|
| Container names & ports | Deployment diagram accuracy | `local-postgres` on `127.0.0.1:5432` |
| Docker networks | How containers communicate | `db-network` has postgres, valkey, grafana |
| Existing databases | Whether to create or use existing | `deerngo` DB already exists |
| Tunnel/proxy type | systemd vs Docker vs manual | `cloudflared.service` (systemd, not Docker) |
| Host IP | streamer.bot connection target | `192.168.1.121` |
| OS & Docker version | Docker Compose compatibility | Ubuntu 26.04, Docker 29.6.2, Compose v5.3.1 |

## Deerngo Bot Session — What SSH Revealed

The PO meeting minute said "Local Windows deployment" and the user said "PostgreSQL exists, Cloudflare Tunnel running." SSH revealed:

```
# docker ps showed:
local-postgres    postgres:18    127.0.0.1:5432->5432/tcp    Up 8 days (healthy)
local-valkey      valkey/valkey:9    127.0.0.1:6379->6379/tcp    Up 8 days (healthy)

# docker network inspect db-network showed:
local-postgres 172.20.0.3/16
local-valkey 172.20.0.4/16
flowero-gate 172.20.0.10/16
grafana 172.20.0.13/16
# ... 15+ containers all on db-network

# psql -l showed:
deerngo    postgres    UTF8    (already exists!)

# systemctl status cloudflared showed:
Active: active (running) — systemd service (NOT a Docker container)

# hostname -I showed:
192.168.1.121 172.17.0.1 ...
```

This changed the deployment model from "everything on Windows PC" to:
- Go backend + Next.js -> Docker containers on homelab, joining `db-network`
- PostgreSQL -> existing `local-postgres` container
- Cloudflare Tunnel -> systemd service on homelab
- streamer.bot -> Windows PC, connects via LAN `192.168.1.121:8008`

**Port assignment note:** After SSH, also confirmed port registry at `F:\obsidian_note\oralita_md\Quick Note\Home Lab App.md` — next available: 8008 (BE), 3008 (FE). Registered new service in the registry.

## Impact on Design Documents

| Document | Section Affected | What Changed |
|----------|-----------------|--------------|
| ADR-004 | Entire decision | "Local Windows" -> "Homelab Docker + Windows PC for streamer.bot" |
| ADR-011 | Context | Cloudflare Tunnel is systemd on homelab, not on Windows |
| API Spec (022) | Base URL, Deployment | `localhost:8008` -> `192.168.1.121:8008` (LAN) + `deerngo-bot:8008` (Docker) |
| SAD (025) | Deployment diagram, Docker Compose | Full rewrite -- Docker topology, network communication table |
| Arch Overview (029) | Component map, port table | Corrected locations for all components |
