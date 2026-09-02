#!/bin/bash
# 502 Bad Gateway Debugging Ladder for Docker + Nginx homelab
#
# Usage: bash scripts/502-debug-ladder.sh <ssh-target> <container-name> <port> <domain>
# Example: bash scripts/502-debug-ladder.sh flowero@remote.example.com flowero-guard 8001 auth.example.com
#
# Runs the full diagnostic chain: container → port → health → nginx → logs → external
# Identifies the root cause in seconds instead of guessing.

SSH_TARGET="${1:?Usage: $0 <ssh-target> <container-name> <port> <domain>}"
CONTAINER="${2:?Missing container name}"
PORT="${3:?Missing port number}"
DOMAIN="${4:?Missing domain name}"

echo "=========================================="
echo "  502 BAD GATEWAY DEBUG LADDER"
echo "  Container: $CONTAINER | Port: $PORT | Domain: $DOMAIN"
echo "=========================================="
echo ""

ssh -o ConnectTimeout=10 "$SSH_TARGET" 'bash -s' << AUDIT_EOF
CONTAINER="$CONTAINER"
PORT="$PORT"
DOMAIN="$DOMAIN"

echo "========== 1. CONTAINER STATUS =========="
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep -i "$CONTAINER" || echo "❌ NO CONTAINER FOUND"
echo ""

echo "========== 2. RESTART COUNT (crash loop?) =========="
RESTARTS=\$(docker inspect $CONTAINER --format '{{.RestartCount}}' 2>/dev/null || echo "N/A")
echo "Restart count: \$RESTARTS"
if [ "\$RESTARTS" -gt 3 ] 2>/dev/null; then
    echo "⚠️  HIGH RESTART COUNT — container is in a crash loop"
fi
echo ""

echo "========== 3. PORT BINDING =========="
ss -tlnp | grep "$PORT" || echo "❌ PORT $PORT NOT LISTENING"
echo ""

echo "========== 4. LOCAL HEALTH =========="
curl -sf --max-time 5 http://localhost:$PORT/health/ready 2>&1 && echo "" || echo "❌ NO RESPONSE ON :$PORT"
curl -sf --max-time 5 -o /dev/null -w '%{http_code}' http://localhost:$PORT/ 2>&1 || echo " (no root response)"
echo ""
echo ""

echo "========== 5. NGINX CONFIG =========="
# Try common naming patterns
NGINX_CONFIG=""
for f in /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-available/auth.conf /etc/nginx/sites-available/api.conf; do
    if [ -f "\$f" ]; then
        NGINX_CONFIG="\$f"
        break
    fi
done
if [ -n "\$NGINX_CONFIG" ]; then
    echo "Config: \$NGINX_CONFIG"
    cat "\$NGINX_CONFIG"
else
    echo "❌ NO NGINX CONFIG FOUND for $DOMAIN"
    echo "--- All enabled sites: ---"
    ls -la /etc/nginx/sites-enabled/
fi
echo ""

echo "========== 6. NGINX TEST =========="
sudo nginx -t 2>&1
echo ""

echo "========== 7. CONTAINER LOGS (last 30 lines) =========="
docker logs --tail 30 "$CONTAINER" 2>&1
echo ""

echo "========== 8. VOLUME MOUNT CHECK (directory-vs-file trap) =========="
docker inspect "$CONTAINER" --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' 2>/dev/null
echo "--- Check each source path: is it a file or directory? ---"
docker inspect "$CONTAINER" --format '{{range .Mounts}}{{.Source}}{{println}}{{end}}' 2>/dev/null | while read -r src; do
    if [ -e "\$src" ]; then
        if [ -d "\$src" ]; then
            echo "❌ \$src is a DIRECTORY (Docker volume trap!)"
        else
            echo "✅ \$src is a file"
        fi
    else
        echo "❌ \$src does NOT EXIST on host"
    fi
done
echo ""

echo "========== 9. EXTERNAL ACCESS =========="
curl -sf --max-time 10 -o /dev/null -w '%{http_code}' https://$DOMAIN/ 2>&1 || echo "FAILED"
echo ""
AUDIT_EOF
