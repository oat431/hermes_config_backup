---
name: homelab-infra-audit
description: >
  Audit a homelab / single-server Docker infrastructure for readiness against
  project design specs. SSH in, batch-verify every component (Docker, databases,
  reverse proxy, DNS/tunnel, firewall, networks), cross-check design-doc
  assumptions against live state, surface spec-vs-reality discrepancies, and
  produce DevOps documents (meeting minutes, deployment plan, CI/CD config,
  runbook). Use whenever the user asks "can we deploy / progress / start
  building on this server" or asks to verify infra matches a spec.
---

# Homelab Infrastructure Audit

Verify a real server can support a planned architecture — then produce the
DevOps documents that prove it.

## When to use

- User asks "is this server ready / can we progress to the next phase"
- User hands you design docs + an SSH address and wants a readiness check
- User asks to verify live infra matches documented architecture
- User wants a deployment plan, CI/CD config, or runbook produced for a homelab stack

## Method — 5 phases

### Phase 1: Read all specs FIRST (before touching the server)

Batch-read every relevant document: meeting minutes, design docs (ADRs, API
specs, DDLs), architecture overviews, and home-lab install notes. Build a
mental model of what the server SHOULD look like *before* you SSH in.

Read with `read_file`. For directory trees, use `search_files target=files` or
`terminal find <path> -type f -name "*.md"`. Obsidian `[[wiki-links]]` point to
files without folder prefixes — resolve them by searching.

### Phase 2: SSH audit (one batched heredoc, not N round-trips)

Run a SINGLE SSH command with a `bash -s << 'EOF'` heredoc that checks
everything at once. This avoids 10+ round-trips. See `scripts/ssh-audit-probe.sh`
for the full probe — it covers:

- Docker version + all containers (`docker ps -a`)
- Docker networks + members (`docker network inspect`)
- Listening ports (`ss -tlnp`)
- Each database (exec into container, list DBs / check auth)
- Nginx status + all site configs
- Cloudflare tunnel status + config
- UFW firewall rules
- Tailscale + Fail2ban

Use `StrictHostKeyChecking=accept-new` on first connect. The user often
provides the SSH string directly — trust it.

### Phase 3: Inspect config files (second batched SSH)

Read the actual config files that control routing and secrets:
- Nginx site configs (`/etc/nginx/sites-available/*` + `sites-enabled/`)
- Cloudflare tunnel config (`~/.cloudflared/config.yml`)
- Docker compose files (`~/database/*/compose.yml`)
- Container command/env (`docker inspect <name> --format '{{.Config.Cmd}}'`)

This is where discrepancies hide — the compose file reveals the REAL container
name, port binding, and auth requirements that docs may have wrong.

### Phase 4: Cross-check specs vs reality — find the discrepancies

This is the highest-value phase. Compare every design-doc assumption against
verified server state. The classic homelab deployment pitfalls are documented
in `references/spec-vs-reality-discrepancies.md`. The recurring ones:

1. **`host.docker.internal` doesn't exist on Linux Docker.** It's a Docker
   Desktop (Mac/Windows) feature. On Linux, services must use container names
   on a shared Docker network (`local-postgres:5432`, not
   `host.docker.internal:5432`). Ping it from the host to prove it doesn't
   resolve.

2. **Host-level Nginx can't resolve Docker container names.** If Nginx runs as
   a host process (not in a container), every `proxy_pass` must target
   `127.0.0.1:PORT`, never `http://container-name:port`. Services must bind
   `127.0.0.1:PORT:PORT` in compose.

3. **Password-protected databases aren't in the specs.** Valkey/Redis often run
   with `--requirepass` (visible via `docker inspect ... --format
   '{{.Config.Cmd}}'`). If the app config omits the password, connections fail.

4. **Wildcard DNS means subdomain DNS work is already done.** If Cloudflare
   tunnel config has `*.domain.com → localhost:80`, every subdomain works
   automatically — flag any task that asks to "add DNS records" as already
   satisfied.

Rate each discrepancy as 🔴 critical (blocks build) or 🟡 concern (non-blocking).
Document each with: what the spec says, what the server shows, the fix.

### Phase 5: Produce DevOps documents

Match the project's existing document conventions (folder numbering, frontmatter
fields, SWEBOK/SEBoK standard refs, `[[wiki-link]]` cross-references). Use
`read_file` on a template if templates exist. Produce:

| Document | When | Content |
|----------|------|---------|
| Meeting minute (MM##) | Always | Audit findings, discrepancies, action items, verdict |
| Deployment plan (052) | When deploy steps are defined | Pre-deploy checklist, step-by-step commands, compose file, verification, rollback |
| CI/CD pipeline (051) | When user plans to ship code | Pipeline stages, GitHub Actions YAML, secrets, registry |
| Runbook (054) | When services will run in prod | Troubleshooting matrix, startup/shutdown, backup/restore |
| Release notes (053) | Only after a release ships | Placeholder until first release — don't fabricate features |

## Workflow preferences (this user)

**Review-then-execute.** Produce ALL documents for the user's review FIRST.
Do NOT execute server-side changes (create databases, add Nginx blocks) until
the user has reviewed the documents and explicitly approved. Offer execution
as a follow-up via `clarify`, but default to "document now, execute later."

**Full-detail, self-contained per-service docs.** When the project has BOTH a
platform-level spec AND per-service spec folders, produce DevOps docs at BOTH
levels — platform (one set) AND each service (one set each). The user
explicitly rejected "lean with cross-references" in favor of full-detail docs
where each service's DevOps documents are self-contained (a developer or
operator can pick up a single service's 051-054 and work from those alone
without needing the platform docs). Cross-references to platform docs are
included as "Related Documents" links, not as substitutes for content.

This means: if there are 3 services + 1 platform, you produce 4 × 4 = 16
DevOps documents. Each service doc covers that service's specific Dockerfile,
compose service definition, env vars, health checks, troubleshooting incidents,
and deployment sequence — not a one-liner pointing at the platform doc.

**Security boundary — high-risk operations the user handles themselves.** The
user explicitly manages passwords, API keys, firewall rules, and SSL
certificates. Do NOT write actual passwords into `.env` files, compose files,
or any file on the server. Use placeholders like `<password>` or
`${KC_DB_PASSWORD}`. The `.env` file template shows the variable names; the
user fills in the values. Specifically off-limits:
- `.env` files with actual passwords
- Cloudflare API keys / tunnel tokens
- SSH private keys
- UFW firewall rules (wrong rule = locked out)
- PostgreSQL/Valkey superuser passwords

**Web search for up-to-date information.** The user explicitly requested using
web search for current documentation rather than relying on potentially outdated
agent knowledge. When troubleshooting or documenting a specific tool version
(Keycloak 26+, Spring Boot 4.1, etc.), fetch the current official docs or
GitHub issues via `curl` rather than guessing from training data.

**Obsidian operational notes for each deployed service.** After deploying a
service, create an operational note in the user's Obsidian vault at
`F:\obsidian_note\oralita_md\home-lab-installation\microservice_component\<service>.md`.
Follow the established format (see `keycloak.md`, `discovery.md`, `gateway.md`
for examples). The note MUST be self-contained — an operator should be able to
pick up just that file and manage the service. Template structure:

```
# <Service Name>
> <One-line description>
> Last updated: YYYY-MM-DD

## Deployment Status       ← Add after first successful deploy
## What & Why              ← Role in the platform, how other services use it
## Setup                   ← Table: Image, Container, Port, Network, Domain, Database, Mode
## Prerequisites           ← Checklist: Docker, db-network, Nginx, ports free, deps running
## Deploy                  ← Step-by-step: clone, Nginx block, compose, build, verify
## Access                  ← Table: all URLs (dashboard, health, API, admin)
## Common Commands         ← Health, logs, restart, force deregister, etc.
## Configuration           ← Key settings table with rationale
## Troubleshooting         ← Numbered incidents: Symptom → Cause → Verify → Fix
## Project Structure       ← File tree with annotations
## Related                 ← Cross-links to other notes and spec docs
```

Add `## Deployment Status` at the TOP (after the header) once the service is
verified working. Include: deploy date, container status, key endpoints with
pass/fail. This is the first thing an operator looks for.

**User sometimes wants to do server work manually.** The user explicitly said
"i want to do a server thing by hand somehow." When they say this, provide the
commands/steps as a reference they can execute, rather than executing via SSH.
Offer to verify after they're done. This is NOT the default — the default is
"review-then-execute" (I produce docs, user approves, I execute). But watch for
signals like "i will do it manually" or "let me try" and switch to reference
mode.

## Phase 6: Spec maintenance & code review (post-audit follow-ups)

After the initial audit and document production, the user will often return with
related tasks. Two patterns recur:

### Spec version migration

When the user changes a technology decision (e.g., Java 21→25, Boot 3.x→4.1,
Maven→Gradle), update ALL spec documents to match — not just the ones you wrote.

**Technique:**
1. `grep -rn -i "<old-version-patterns>" <spec-root> --include="*.md"` to find
   every reference. Cast a wide net: version strings, tool names, artifact IDs,
   image tags, file paths.
2. Update in priority order: ADRs (full rewrite of the decision entry, not just
   the index line) → SAD component tables → requirement docs (business objective,
   user stories) → architecture overviews → READMEs → CI/CD configs (build
   commands, Dockerfiles, repo structure, artifact paths).
3. When build tool changes (Maven→Gradle), update: CI YAML commands
   (`./mvnw compile`→`./gradlew compileJava`), Dockerfile base images
   (`maven:3.9-eclipse-temurin-21`→`eclipse-temurin:25-jdk-alpine`), artifact
   paths (`/target/*.jar`→`/build/build/libs/*.jar`), repo structure
   (`pom.xml`→`build.gradle`, `mvnw`→`gradlew`), local testing commands.
4. Final grep sweep to confirm zero stragglers.

**Pitfall:** Historical meeting minutes are records of what was discussed at the
time — do NOT rewrite them to match new decisions. They are immutable history.

### Existing-code-vs-spec gap analysis

When the user hands you an existing project to review against the specs:

1. Read EVERY config file: build config, all application profiles (base/dev/prod),
   docker-compose, Dockerfile, and all Java source relevant to the spec.
2. Compare each spec requirement against the actual implementation.
3. Categorize: ✅ aligned / 🔴 must-fix (blocks deployment) / 🟡 nice-to-have.
4. Identify the biggest decision point (usually a version mismatch) and present
   options with trade-offs.
5. **Ask the user which direction** to resolve mismatches — don't assume
   "downgrade the code" or "upgrade the specs." They may have already decided
   but forgotten to tell you (happened this session: "lol, yes, i forgot to
   tell you").

**Pitfall:** When writing per-service spec docs, double-check frontmatter
`project_name` / `project_id` matches the service. Copy-paste from a sibling
service leaves the wrong name in the YAML frontmatter.

See `references/spec-migration-and-code-review.md` for the full reference with
concrete examples from the Panomete Platform migration.

## Keycloak-on-homelab specifics

When the project includes Keycloak (Flowero Guard pattern), several config
details are non-obvious and must be correct in the deployment plan and compose
file. See `references/keycloak-homelab-deploy.md` for the full reference.
Key points:
- `KC_PROXY_HEADERS: xforwarded` — trust X-Forwarded-* headers from Nginx/Cloudflare (replaces deprecated `KC_PROXY=edge` in Keycloak 25+)
- `KC_HTTP_ENABLED: "true"` — accept HTTP internally (Cloudflare handles TLS)
- `KC_CACHE: local` — disables JGroups distributed caching (single-node only, prevents 20s+ startup delay from cluster JOIN timeouts)
- `command: ["start", "--import-realm"]` — import realm JSON on boot
- `client_max_body_size 10M` in Nginx — Keycloak POST bodies can be large
- Liquibase runs on first boot (slow startup, creates 50+ tables)
- `KC_DB_URL` uses container name (`local-postgres`), not `host.docker.internal`

## Spring Boot service deployment patterns

When deploying any Spring Boot service (Eureka, Gateway, business services) on
the homelab, see `references/spring-boot-docker-patterns.md` for the full
reference. Key points:
- Multi-stage Dockerfile: JDK build stage → JRE runtime stage
- `curl` is NOT in JRE images — must `apt-get install curl` for healthchecks
- Always bind ports to `127.0.0.1` for Nginx proxy
- Always join `db-network` for inter-service communication
- Eureka dual-port can be a Docker port-mapping trick (both host ports → same container port)
- `$scheme` is `http` behind Cloudflare — hardcode `X-Forwarded-Proto https` in Nginx

## Output conventions

- Use the project's frontmatter schema exactly (copy fields from existing docs)
- Version `0.1` for drafts, `status: Draft`
- Cross-reference other docs with `[[filename_without_ext]]`
- Cite SWEBOK v4 / SEBoK v2 / ITIL v4 in `standard_ref` where the templates do
- Tables for checklists; mermaid diagrams for flows in deployment plans
- Include ACTUAL verified values (container names, ports, passwords-as-`<placeholder>`)
  in deployment plans — never the spec's assumed values if they differ

## Pitfalls

- **Don't trust the specs blindly.** The design docs were written before the
  server was verified. Always cross-reference. Specs frequently assume
  `host.docker.internal`, wrong container names, or miss auth requirements.
- **Don't run N SSH round-trips.** Batch into one heredoc probe, then one
  config-file-reading probe. Two SSH calls, not fifteen.
- **Don't fabricate release notes.** If no code has shipped, mark `053` as a
  placeholder with the roadmap, not invented features.
- **Don't execute changes mid-audit.** The audit is read-only. Changes happen
  after document review and explicit approval.
- **`docker inspect --format '{{.Config.Cmd}}'`** reveals the actual startup
  command including passwords — use it to find auth requirements the docs omit.
- **Check `db-network` (or equivalent shared network) membership** — if a
  database container isn't on the shared network, services can't reach it by
  name even if the name is correct.
- **Don't put code/config files in the spec folder.** The user explicitly
  corrected this: "the spec folder is really a spec folder." Realm JSON,
  compose fragments, and code belong in project directories or Obsidian notes,
  not in the spec tree. Use `templates/` within skills or the service's own
  project directory.
- **Don't assume `$scheme` is `https` behind Cloudflare Tunnel.** Cloudflare
  terminates TLS and sends HTTP to Nginx via the tunnel. `$scheme` is `http`.
  For services that check the protocol (Keycloak with `sslRequired: external`),
  hardcode `proxy_set_header X-Forwarded-Proto https;` in the Nginx config.
  This is the #1 cause of `"HTTPS required"` 403 errors on external access.
- **Don't use complex heredocs with embedded JSON/quotes over SSH.** Single
  quotes, double quotes, and JSON braces break bash heredoc escaping in SSH
  commands. Pattern that works: write a Python script to the remote host via
  scp or a simple `cat > /tmp/script.py`, then `python3 /tmp/script.py`.
- **Don't append to Docker Compose YAML files.** `cat >> docker-compose.yml`
  breaks YAML indentation (new service ends up nested under `networks:` or
  wrong parent). Always rewrite the entire file — use Python `yaml.dump` over
  SSH to generate correct YAML.
- **Realm JSON `sslRequired` overrides the `KC_SSL_REQUIRED` env var.** If
  the realm JSON has `"sslRequired": "external"`, Keycloak ignores
  `KC_SSL_REQUIRED=none` from the environment. The realm-level setting takes
  precedence. Fix: change the realm JSON to `"sslRequired": "none"` OR fix
  Nginx to send `X-Forwarded-Proto https` (preferred — keeps HTTPS enforcement).
- **Realm JSON composite roles referencing undefined client roles cause
  crashes.** A composite role like `default-roles-panomete` with
  `"client": {"account": ["view-profile", "manage-account"]}` will crash
  Keycloak if those client roles aren't defined in the `clients` section.
  Fix: remove client role references from composites, or define the client
  roles explicitly.
- **`KC_BOOTSTRAP_ADMIN_*` always creates temporary admins (Keycloak 26+).**
  The old `KEYCLOAK_ADMIN`/`KEYCLOAK_ADMIN_PASSWORD` are deprecated. The new
  `KC_BOOTSTRAP_ADMIN_USERNAME`/`KC_BOOTSTRAP_ADMIN_PASSWORD` create a
  temporary admin that shows a warning banner. This is by design — the user
  must create a permanent admin via the Admin Console. Document this in a
  "Post Install" section.
- **`curl` is NOT installed in JRE-based Docker images.** `eclipse-temurin:*-jre-*`
  images (Ubuntu-based like `jre-noble`) do NOT include `curl`. Docker healthchecks
  that use `curl` will fail silently, showing the container as "unhealthy" in
  Portainer even though the service is running fine. Fix: add
  `RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*`
  to the Dockerfile's runtime stage. Or use `wget` if available.
  **Verify:** `docker exec <container> which curl` — if "not found", the healthcheck
  is broken.
- **Eureka "dual-port" can be a Docker port-mapping trick.** Standard Eureka
  serves both REST API and dashboard on a single port. The spec may call for
  separate ports (e.g., 8999 for API, 3999 for dashboard). A pragmatic solution:
  map both host ports to the same container port:
  ```yaml
  ports:
    - "127.0.0.1:8999:8999"   # REST API
    - "127.0.0.1:3999:8999"   # Dashboard (same container port, different host port)
  ```
  Nginx proxies `discovery.panomete.com` → `:3999`, services register on `:8999`.
  This avoids the complexity of configuring Eureka to serve on two separate ports.

## Phase 7: Live deployment debugging (when the user hits 502 / crash loops)

After documents are approved and the user starts deploying by hand, they WILL
hit issues. The most common is "I deployed X but get 502 Bad Gateway." Run
`scripts/502-debug-ladder.sh` (adapt the SSH target) or hand-type the chain:

1. **Container running?** `docker ps -a | grep <name>` — check Status + RestartCount
2. **Port listening?** `ss -tlnp | grep <PORT>` — is the host port bound?
3. **Service responds locally?** `curl -sf http://localhost:<PORT>/health` — does the app answer?
4. **Nginx configured?** `cat /etc/nginx/sites-available/<domain>` — is the server block there?
5. **Nginx valid?** `sudo nginx -t` — does the config parse?
6. **Logs?** `docker logs --tail 30 <name>` — what error is crashing it?
7. **External?** `curl -sf -o /dev/null -w '%{http_code}' https://<domain>` — full path test

### The Docker volume directory-creation trap (CRITICAL)

**This is the #1 cause of Keycloak crash loops on first deploy.**

When a Docker volume mount targets a FILE path that doesn't exist on the host,
Docker **silently creates a DIRECTORY** at that path instead of failing. The
container then tries to read a file but finds a directory:

```yaml
# Compose mount:
volumes:
  - ./panomete-realm.json:/opt/keycloak/data/import/panomete-realm.json:ro
```

If `./panomete-realm.json` doesn't exist on the host when `docker compose up`
runs, Docker creates a directory. Keycloak crashes with:

```
ERROR: /opt/keycloak/data/import/panomete-realm.json (Is a directory)
```

The container enters a restart loop (check `docker inspect <name> --format
'{{.RestartCount}}'` — a high count means crash loop).

**Fix:** ALWAYS create the file on the host BEFORE starting the container.
Then `docker compose down && docker compose up -d` (must recreate, not just
restart, to fix the mount).

**Prevention:** Use a verified realm JSON template
(`templates/realm-template.json`) and scp it to the host before first boot.

### Deployment sequencing — least-dependent first

When deploying multiple interconnected services, sequence by dependency:

```
Least dependent → Most dependent
Keycloak (needs only PG) → Discovery (needs nothing) → Gateway (needs all 3)
```

Deploying the most-dependent service before its dependencies exist forces
temporary workarounds (hardcoded URLs, disabled features) that must be undone
later. Always ask: "what does this service need to be running before it starts?"

See `references/deployment-debugging.md` for the full session transcript of the
Keycloak 502 debugging, including the exact SSH commands used.

## Verification

After producing documents, confirm:
- Every discrepancy is traced to a specific doc + a specific server finding
- Action items have owners (DevOps / Dev / PO) and due dates
- The deployment plan's compose file uses VERIFIED container names and ports
- The runbook's troubleshooting matrix covers the specific stack (Keycloak + Eureka + Gateway, or whatever the actual services are)
- The verdict (can/cannot progress) is explicit and justified

When debugging live deployments, confirm:
- The 502 ladder was run top-to-bottom (don't skip to logs — check container first)
- Container RestartCount was checked (high = crash loop, not a transient error)
- Volume mounts were verified as FILES not directories (`ls -la` on the host path)
- The verdict (can/cannot progress) is explicit and justified
