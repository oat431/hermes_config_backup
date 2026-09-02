#!/usr/bin/env bash
# Homelab server audit — single batched SSH probe.
# Run via: ssh flowero@remote.panomete.com 'bash -s' < references/ssh-audit-script.sh
#
# Checks everything in one round-trip: Docker, networks, ports, DBs, Nginx,
# Cloudflare, firewall, Tailscale, Fail2ban. Read-only — no changes.
# Adjust container names, ports, and paths to match the target server.

echo "========== 1. DOCKER =========="
echo "--- Docker version ---"
docker --version 2>&1
docker compose version 2>&1
echo ""
echo "--- Containers (running + stopped) ---"
docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' 2>&1

echo ""
echo "========== 2. DOCKER NETWORKS =========="
docker network ls 2>&1
echo ""
echo "--- db-network members ---"
# Change 'db-network' to the actual shared network name
docker network inspect db-network --format '{{range .Containers}}{{.Name}} {{end}}' 2>&1

echo ""
echo "========== 3. PORTS LISTENING =========="
# Adjust the grep pattern to the ports you care about
sudo ss -tlnp 2>/dev/null | grep -E ':(5432|6379|27017|8000|8001|8080|8999|3999|80|443|7000|7001)\b' \
  || ss -tlnp 2>/dev/null | grep -E ':(5432|6379|27017|8000|8001|8080|8999|3999|80|443|7000|7001)\b'

echo ""
echo "========== 4. POSTGRESQL =========="
# Adjust container name + user
docker exec local-postgres psql -U postgres -c "\l" 2>&1
echo ""
echo "--- specific DB check (edit datname) ---"
docker exec local-postgres psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname='keycloak'" 2>&1
echo "--- role check ---"
docker exec local-postgres psql -U postgres -c "\du" 2>&1

echo ""
echo "========== 5. VALKEY / REDIS =========="
# 'ping' reveals if auth is required (NOAUTH vs PONG)
docker exec local-valkey valkey-cli ping 2>&1
docker exec local-valkey valkey-cli info server 2>&1 | grep -E 'redis_version|valkey_version|tcp_port|uptime'

echo ""
echo "========== 6. NGINX =========="
echo "--- status ---"
sudo systemctl is-active nginx 2>&1
echo "--- sites-available ---"
ls -la /etc/nginx/sites-available/ 2>&1
echo "--- sites-enabled ---"
ls -la /etc/nginx/sites-enabled/ 2>&1
echo "--- config test ---"
sudo nginx -t 2>&1

echo ""
echo "========== 7. CLOUDFLARE =========="
sudo systemctl is-active cloudflared 2>&1

echo ""
echo "========== 8. UFW FIREWALL =========="
sudo ufw status 2>&1 | head -30

echo ""
echo "========== 9. TAILSCALE =========="
tailscale status 2>&1 | head -5

echo ""
echo "========== 10. FAIL2BAN =========="
sudo systemctl is-active fail2ban 2>&1

echo ""
echo "========== 11. RESOURCES =========="
echo "--- CPU ---"
nproc
lscpu | grep 'Model name'
echo "--- Memory ---"
free -h
echo "--- Disk ---"
df -h /

# ===========================================================================
# FOLLOW-UP PROBE (run as a SEPARATE ssh call): read config files + secrets
# ===========================================================================
# ssh flowero@host 'bash -s' << 'EOF'
#
# # Nginx site configs
# for f in /etc/nginx/sites-available/*; do
#   echo "=== $f ==="; cat "$f"; echo ""
# done
#
# # Cloudflare tunnel config
# sudo cat ~/.cloudflared/config.yml 2>/dev/null || sudo cat /etc/cloudflared/config.yml
#
# # Database compose files (reveal container names, ports, networks, auth)
# cat ~/database/postgres/compose.yml
# cat ~/database/valkey/compose.yml
#
# # Container actual startup command (reveals passwords!)
# docker inspect local-valkey --format '{{range .Config.Cmd}}{{println .}}{{end}}'
# docker inspect local-postgres --format '{{range .Config.Env}}{{println .}}{{end}}'
#
# # Prove host.docker.internal doesn't exist on Linux
# ping -c1 host.docker.internal 2>&1 | head -2
# EOF
