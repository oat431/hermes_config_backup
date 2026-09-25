# Workflow Overview

> *Agent-created Hermes skills — copy to `~/.hermes/skills/` on any new machine to restore full capability.*
>
> **Structure:** main-profile skills live in `hermes-main-profile/`, profile-specific skills in their own folder per profile.

---

## Skills Map (22 Main + 8 shared + 71 Profile-Specific = 101)

### 📚 PDF & Book Summarization _(in `hermes-main-profile/`)_

| Skill | Use when |
|-------|---------|
| **oralita-book-sum-obs** | Summarizing a PDF book (200-1000pp) into Obsidian vault as cross-linked `.md` files. 5-phase pipeline: TOC → topic mapping → chapter extraction → parallel sub-agents → overview + polish. Proven on Clean Code, Clean Coder. |
| **bok-essential-documents** | Extracting only the essential/reference documents from a body-of-knowledge PDF — skips narrative, keeps rules, checklists, and catalogs. |

### 🏗️ Obsidian Vault Management

| Skill | Use when |
|-------|---------|
| **obsidian-vault-builder** | Building out an incomplete Obsidian vault from skeleton overview files. Creates missing topic notes in bulk. |
| **obsidian-vault-filling** | Filling in missing notes identified by gap analysis. Reads Overview/MOC, finds missing `[[wikilinks]]`, fills them. |
| **obsidian-vault-maintenance** | Detecting and fixing broken wikilinks, adding YAML frontmatter, normalizing tags. |
| **vault-completion** | General vault completion — filling missing Obsidian vault notes from overview/MOC files and web research. |

### 📄 Project Documentation

| Skill | Use when |
|-------|---------|
| **project-launch-checklist** | Building two-tier production launch checklists — generic (framework-agnostic) + framework-specific companions. |
| **project-document_templates** | Generating project document templates (PRD, tech spec, architecture decision records). |
| **md-project-document_templates** | Markdown-native project document templates — lighter, faster than the full template system. |
| **document_template-authoring** | Authoring new document templates — defining sections, prompts, and output formats. |

### 🎬 Presentations

| Skill | Use when |
|-------|---------|
| **pptx-deck-series** | Creating a series of `.pptx` decks from vault content — consistent theming across multiple presentations. |
| **presentation-from-vault** | Extracting Obsidian vault content into a structured presentation outline, ready for deck assembly. |

### 💻 Development

| Skill | Use when |
|-------|---------|
| **go-fiber-api** | Building Go REST APIs with Fiber v3 + sqlx. Clean architecture, PostgreSQL, spec-driven. Also handles full-stack monorepo scaffolding (absorbed `full-stack-monorepo`). |
| **software-specification** | Writing detailed software specifications from user requirements — features, architecture, data models. |

### 🖥️ Homelab

| Skill | Use when |
|-------|---------|
| **homelab-server-setup** | Setting up and managing a homelab server — SSH hardening, Docker, Cloudflare Tunnel, Tailscale, Nginx reverse proxy, database containers, deployment. Re-created as a standalone live skill (distinct from the archived pre-merge version). |
| **homelab-infra-setup** | Infrastructure provisioning — networks, volumes, DNS, reverse proxy. Absorbed `homelab-setup` + `homelab-server-setup`. |
| **homelab-infrastructure** | Infrastructure-as-code for homelab services — compose files, configs, monitoring. Absorbed `homelab-management`. |

### ⚙️ Hermes Configuration

| Skill | Use when |
|-------|---------|
| **hermes-profile-setup** | Creating and configuring Hermes profiles for separate use cases. Profiles = isolated memory, skills, SOUL, tools per persona. |
| **hermes-web-backends** | Fixing or configuring Hermes `web_search`/`web_extract` backends (firecrawl, searxng, tavily, exa, parallel, ddgs). Provider capability matrix + troubleshooting. |
| **hermes-setup-replication** | Replicating a Hermes install onto a new Windows machine — souls, skills, profiles handoff pack. Windows HERMES_HOME + install one-liner + runbook pointer. |
| **mcp-server-patterns** | Adding or troubleshooting MCP servers in Hermes Agent (filesystem, github, postgres, drawio, searxng). |
| **skill-library-maintenance** | Reviewing or improving a Hermes skill library — consolidation, curation, health checks. |

### 📦 Profile-Specific Skills

Skills created inside individual specialist profiles (not in the main library). Each profile has its own top-level folder in `workflow/`.

| Profile folder | # Skills | New since 2026-08-24 marked ★ |
|---------|----------|-------|
| product-owner | 12 | po-requirements-elicitation, go-hexagonal-api, go-backend-api/service, spec-document-elicitation, grill-me-requirements, requirements-to-backlog, project-spec-authoring, knowledge-base-quality-audit, evidence-based-document-audit, privacy-regulatory-research, go-fiber-backend-development |
| full-stack | 13 | go-fiber-api-server, go-background-scheduler-api-poller, react-vite-spa, spec-driven-design, full-stack-repository-bootstrap, construction-docs, checklist-review, github-pr-qa-followup, interview-prep-coaching, interview-answer-cards, web-research, ai-chatbot-grounded-retrieval ★, job-hunting-loop-repo ★ |
| educator | 11 | curriculum-vault-authoring, educational-content-authoring, career-guidance-authoring, career-path-overlay-authoring, educational-notes-bilingual, multilingual-note-conversion, obsidian-note-authoring, obsidian-vault-restructuring, exercise-authoring, iso-standards-compliance-review, self-learning-course-authoring ★ |
| devops | 8 | homelab-infra-audit, homelab-microservice-deployment, keycloak-deployment, keycloak-docker, devops-doc-authoring, release-readiness-audit, windows-pc-audit ★, windows-pc-ops ★ |
| qa | 7 | spec-driven-qa-authoring, spec-driven-code-review, github-pr-follow-up-review, checklist-audit, knowledge-vault-audit, obsidian-vault-audit, knowledge-vault-scaffolding ★ |
| journey-writer | 4 | campaign-journal, wiki-lore-research, writing-practice-audit, online-profile-cards ★ |
| ui-ux | 4 | penpot-mcp, project-spec-docs, nginx-streaming-proxy, branding-ci ★ |
| career-coach | 3 | career-artifact-prep, career-coaching, career-path-vault-authoring ★ |
| book-summarizer | 2 | narrative-book-summaries ★, research-paper-summaries ★ |
| gym | 2 | fitness-coaching, weekly-training-review |
| security-engineer | 2 | security-review-pass, tor-darkweb-exploration |
| deck | 1 | presentation-design |
| audiophile | 1 | personal-audio-guidance ★ |
| data-engineer | 1 | publish-personal-project ★ |
| financial-advisor · llmops | 0 | souls backed up in `soul-collection/`; no custom skills yet |

**Restore:** copy `workflow/<profile-name>/*` → `%LOCALAPPDATA%\hermes\profiles\<profile-name>\skills\` on a new machine.

---

## Common Workflows

### Workflow A: Summarize a Book → Obsidian Vault

```
1. Place PDF in accessible location (e.g., F:\books\)
2. Load skill: /skill oralita-book-sum-obs
3. Run: "Summarize F:\books\my-book.pdf into F:\projects\orlita_md\My Vault\"
4. Pipeline auto-runs: TOC → topic map → extract → sub-agents → overview
5. Result: cross-linked .md vault with checklist, wikilinks, code examples
```

### Workflow B: Build Out an Incomplete Vault

```
1. Create Overview.md with [[wikilinks]] to all desired topics
2. Load skill: /skill obsidian-vault-builder
3. Run: "Fill missing notes from Overview.md in F:\projects\orlita_md\My Vault\"
4. Agent fills in blanks, creates consistent .md files
```

### Workflow C: Create a Project Launch Checklist

```
1. Load skill: /skill project-launch-checklist
2. Run: "Create a launch checklist for <project type>"
3. Produces: generic checklist (~45 items) + framework-specific companion
```

### Workflow D: Spec → Code (Go/Fiber API)

```
1. Write spec doc in Obsidian vault
2. Load skill: /skill go-fiber-api
3. Run: "Build API from spec at F:\projects\orlita_md\...\spec.md"
4. Produces: structured Go project with Fiber v3, sqlx, clean architecture
```

---

## Restoring on a New Machine

```bash
# Copy main-profile skills into Hermes
cp -r F:/obsidian_note/hermes_config_backup/workflow/hermes-main-profile/* ~/AppData/Local/hermes/skills/

# Copy profile-specific skills back into each profile
# (for each profile <name>):
cp -r F:/obsidian_note/hermes_config_backup/workflow/<name>/* \
      ~/AppData/Local/hermes/profiles/<name>/skills/

# Verify
hermes skills list | grep local

# Load any skill
hermes -s <skill-name>
```

---

## Skill Lifecycle

```
[Create] → [Prove on real task] → [Save as skill] → [Use across sessions]
                                                        ↓
                                              [Backup to Obsidian vault]
                                                        ↓
                                              [Restore on new machine]
                                                        ↓
                                          [Consolidate] → [Archive in vault]
```

---

## Archived Skills (4)

These skills were consolidated into others. Full content preserved in `archived/`.

| Archived Skill | Absorbed Into | Reason |
|----------------|---------------|--------|
| **full-stack-monorepo** | go-fiber-api | Monorepo scaffolding now part of go-fiber-api workflow |
| **homelab-setup** | homelab-infra-setup | Merged — redundant with infra-setup's provisioning pipeline |
| **homelab-server-setup** | homelab-infra-setup | Merged — server bootstrap is now part of infra-setup |
| **homelab-management** | homelab-infrastructure | Merged — day-to-day mgmt now part of infrastructure skill |

---

*Last updated: 2026-08-24*