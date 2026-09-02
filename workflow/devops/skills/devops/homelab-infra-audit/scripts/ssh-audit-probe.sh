#!/usr/bin/env bash
# SSH Infrastructure Audit Probe
# Run via: ssh <user>@<host> 'bash -s' < references/ssh-audit-probe.sh
#
# Batched single-SSH probe for homelab infrastructure audit (Phase 2).
# Checks: Docker, networks, ports, databases, Nginx, Cloudflare, firewall,
# Tailscale, Fail2ban. Read-only — no state changes on the server.

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
echo "--- Shared network members (adjust 'db-network' if named differently) ---"
docker network inspect db-network --format '{{range .Containers}}{{.Name}} {{end}}' 2>&1
echo ""
echo "========== 3. PORTS LISTENING =========="
# Adjust the grep pattern to the project's port range
ss -tlnp 2>/dev/null | grep -E ':(5432|6379|27017|8000|8001|8080|8999|3999|80|443|7000|7001)\b'
echo ""
echo "========== 4. POSTGRESQL =========="
docker exec local-postgres psql -U postgres -c "\l" 2>&1
echo ""
echo "--- Specific DB check (rename for your project) ---"
docker exec local-postgres psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname='keycloak'" 2>&1
echo "--- Roles ---"
docker exec local-postgres psql -U postgres -c "\du" 2>&1
echo ""
echo "========== 5. VALKEY / REDIS =========="
docker exec local-valkey valkey-cli ping 2>&1
echo "--- Startup command (reveals passwords!) ---"
docker inspect local-valkey --format '{{range .Config.Cmd}}{{println .}}{{end}}' 2>&1
echo ""
echo "========== 6. NGINX =========="
sudo systemctl is-active nginx 2>&1
echo "--- sites-available ---"
ls -la /etc/nginx/sites-available/ 2>&1
echo "--- sites-enabled ---"
ls -la /etc/nginx/sites-enabled/ 2>&1
echo "--- nginx -t ---"
sudo nginx -t 2>&1
echo ""
echo "========== 7. CLOUDFLARE =========="
sudo systemctl is-active cloudflared 2>&1
sudo cat ~/.cloudflared/config.yml 2>&1
echo ""
echo "========== 8. UFW FIREWALL =========="
sudo ufw status 2>&1
echo ""
echo "========== 9. TAILSCALE =========="
tailscale status 2>&1 | head -5
echo ""
echo "========== 10. FAIL2BAN =========="
sudo systemctl is-active fail2ban 2>&1
echo ""
echo "========== 11. RESOURCES =========="
echo "--- Disk ---"
df -h / 2>&1
echo "--- Memory ---"
free -h 2>&1
echo "--- CPU ---"
nproc 2>&1
echo "--- host.docker.internal (should FAIL on Linux) ---"
ping -c1 host.docker.internal 2>&1 | head -2
echo ""
echo "========== 12. COMPOSE FILES =========="
# Adjust paths to match the server's layout
for f in /home/*/database/*/compose.yml; do
    echo "--- $f ---"
    cat "$f" 2>&1
    echo ""
done
