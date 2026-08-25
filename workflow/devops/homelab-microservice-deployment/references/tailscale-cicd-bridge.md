# Tailscale-Bridged CI/CD Deployment Pattern

When a homelab server resolves to a Tailscale IP (100.x.x.x), GitHub Actions runners on the public internet cannot SSH to it directly. Use the `tailscale/github-action` to temporarily join the runner to the Tailnet.

## Problem

```
GitHub Actions Runner (public internet)
  → SSH to remote.example.com
  → DNS resolves to 100.73.143.25 (Tailscale IP)
  → Connection refused / timeout
```

## Solution — Two-Stage Pipeline

### Stage 1: CI (automatic on push)

Standard build + test + push to container registry. No server access needed.

### Stage 2: Deploy (manual `workflow_dispatch`)

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: homelab
    steps:
      # 1. Join Tailnet temporarily
      - name: Connect to Tailscale
        uses: tailscale/github-action@v3
        with:
          auth-key: ${{ secrets.TS_AUTH_KEY }}
          hostname: github-actions-deploy

      # 2. SSH now works — server is reachable
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: remote.example.com
          username: deploy-user
          key: ${{ secrets.HOMELAB_SSH_KEY }}
          script: |
            cd ~/platform
            docker compose pull && docker compose up -d

      # 3. Smoke test runs ON the server (not from runner)
      - name: Smoke Test
        uses: appleboy/ssh-action@v1
        with:
          host: remote.example.com
          username: deploy-user
          key: ${{ secrets.HOMELAB_SSH_KEY }}
          script: |
            curl -sf http://localhost:PORT/actuator/health || exit 1
```

The Tailscale node auto-removes when the job ends if using an ephemeral auth key.

## Pitfalls Discovered in Practice

### 1. `gradlew: Permission denied` on GitHub Actions

Windows doesn't preserve Unix execute bits in git. The `gradlew` file arrives at the runner without `+x`.

**Fix (two parts):**
```bash
# In the repo — fix the tracked permission
git update-index --chmod=+x gradlew
git commit -m "fix: make gradlew executable"
```

```yaml
# In the workflow — safety net step
- name: Make gradlew executable
  run: chmod +x gradlew
```

### 2. `Task 'checkstyleMain' not found`

Only run Checkstyle if the project has the plugin in `build.gradle`. If not configured, the CI step fails immediately. Remove the lint step or add Checkstyle to the project.

### 3. `.dockerignore` excludes files needed by Dockerfile

The Guard CI failed because `panomete-realm.json` was listed in `.dockerignore` but the Dockerfile had `COPY panomete-realm.json ...`. Always verify `.dockerignore` doesn't exclude files referenced by `COPY`.

### 4. GHCR package visibility ≠ repo visibility

Making a repo public does NOT make its GHCR image public. Package visibility is set separately in GitHub UI → Package settings → Change visibility. Or link the package to the repo to inherit visibility.

### 5. Smoke tests should run ON the server

Don't `curl` from the runner — it resolves to the public/Tailscale IP which may not work. Use `appleboy/ssh-action` to run health checks via SSH on the server itself. This tests the actual deployed state.

## Required Secrets

| Secret | Purpose | How to Generate |
|--------|---------|-----------------|
| `TS_AUTH_KEY` | Tailscale auth key (ephemeral) | Tailscale admin console → Settings → Keys → Generate → check "Ephemeral" |
| `HOMELAB_SSH_KEY` | SSH private key for server | `ssh-keygen -t ed25519`, add public key to server's `authorized_keys` |

## Why Manual Deploy (`workflow_dispatch`)?

For single-developer homelabs, auto-deploy on push is risky. The two-stage model gives:
- **CI runs automatically** — catches compile/test failures before they reach the server
- **Deploy is a conscious click** — developer chooses when to update production
- **Rollback is built in** — smoke test fails → previous image restored

## Smoke Tests Run on Server, Not Runner

Since the runner joins Tailscale temporarily, smoke tests should run via SSH on the server itself (using `appleboy/ssh-action`), NOT via `curl` from the runner. This avoids DNS resolution issues and tests the actual deployed state.
