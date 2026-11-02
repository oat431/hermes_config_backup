# hermes_config_backup

The safety net for my AI workstation. Hermes runs on this Windows box across 18 profiles, and the machine has already died on me once. This repo is how I rebuild the whole thing from scratch: the souls, the skills, and a step-by-step runbook.

## What's in here

- **[soul-collection/](https://github.com/oat431/hermes_config_backup/tree/main/soul-collection)**: the personalities. The main soul (plus old v1) and 17 profile souls in two groups: **AI-SDLC** (the engineering crew: full-stack, devops, security, qa, data, llmops, product-owner, ui-ux) and **Life Styles** (journey-writer, book-summarizer, educator, career-coach, financial-advisor, gym, audiophile, deck, photo-artisan). The index is [profile-registry.md](https://github.com/oat431/hermes_config_backup/blob/main/soul-collection/profile-registry.md).
- **[workflow/](https://github.com/oat431/hermes_config_backup/tree/main/workflow)**: the skills. Every profile's skill library (500+ notes), shared skills, and archived old iterations.
- **[Hermes-Setup-Install.md](https://github.com/oat431/hermes_config_backup/blob/main/Hermes-Setup-Install.md)**: the runbook. Steps 0 to 9 to replicate this setup on any Windows machine: install Hermes, wire up the model provider, searxng search (homelab via Tailscale or local Docker), drop in skills and souls, hook up MCP servers, verify.
- **Hermes-Config-Review-2026-10-23.md**: the latest full audit of the live config. Gateway migration story and the decisions still sitting on my desk.

## What's not in here

No `config.yaml`, no `.env`, no live keys. Those get typed by hand on the new machine, and the runbook says exactly where each one goes. This repo is markdown only (plus a little Python hiding in the skills).

## How to use it

Clone it on a fresh machine, open [Hermes-Setup-Install.md](https://github.com/oat431/hermes_config_backup/blob/main/Hermes-Setup-Install.md), follow the steps. Everything else is reference material for the runbook.

## License

Public domain under [The Unlicense](https://github.com/oat431/hermes_config_backup/blob/main/LICENSE). Take what's useful.
