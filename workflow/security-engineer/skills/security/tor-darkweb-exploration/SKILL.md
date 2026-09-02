---
name: tor-darkweb-exploration
description: Use when guiding safe Tor/dark web exploration.
version: 1.0.0
author: hermes-curator
license: MIT
metadata:
  hermes:
    tags: [security, tor, darkweb, privacy, opsec]
    related_skills: [security-review-pass, homelab-infrastructure]
---

# Tor & Dark Web Safe Exploration

## When to Use

- User asks how to start/explore the dark web or Tor onion services (setup, safety, what to visit).
- User asks what the dark web is, why people use it, or whether something is safe/legal there.
- User is mid-exploration and needs verified entry points, OPSEC reminders, or legal framing.

Guide Panomete (or any user) through **safe, legal** exploration of the Tor network / onion services. The user is actively exploring (started 2026-08-25, Tor Browser on main machine; Whonix homelab VM noted as a future upgrade).

## Core framing (say this first — it kills the myths)

- The dark web is regular websites with different **network properties**: anonymity, censorship resistance, self-authenticating addresses (the onion address IS the server's public-key fingerprint — no CA/DNS trust chain).
- It's a **spectrum**, not a binary: HTTP → HTTPS → VPN → Tor Browser → onion services → Tails/Whonix. Same motive as a homelab: control over who observes.
- The "underworld" is mostly **scams, honeypots, and content-farm marketing**. Illegal markets are exit scams or LE stings.
- **Golden rule: search, don't browse.** Get addresses from trusted channels only.

## Setup steps (main machine, proportionate tier)

1. Tor Browser **only** from `https://torproject.org` — fake Tor Browser is a top malware vector; verify the download with `certutil -hashfile <file> SHA256` against the official checksum.
2. First launch: Connect → shield icon → **Safer** level (kills most JS attack surface) → don't maximize (screen-size fingerprint) → no extensions → no real accounts (exit nodes can hijack sessions).

## OPSEC rules (non-negotiable)

- Never reuse real-life usernames/passwords · never pay crypto for "deals" (~95% scam) · never torrent over Tor (IP leak) · never share personal details (accumulation de-anonymizes) · never download files or open documents · no VPN "for extra privacy" (adds a trust party; bridges only if blocked).

## Entry workflow (the safe path)

1. **DuckDuckGo onion** — primary search inside Tor
2. **Ahmia** (`ahmia.fi`) — open-source search engine that filters illegal content; safest "central station"
3. **dark.fail** — most trusted verified link directory
4. **Onion-Location** — purple onion icon in Tor Browser when a clearnet site offers an onion; click to jump to the site's OWN verified address (zero directory trust)

## Legal red lines (plain language)

- Viewing onion sites: legal in most jurisdictions incl. Thailand. Buying/selling/possessing illegal goods: not legal; Thailand's Computer Crime Act has real teeth — don't test edges. Work/ISP networks log "connected to Tor".

## Escalation tier

Tor Browser on main OS is enough for casual exploration. Escalate to **Tails** (RAM-only USB) or **Whonix** (gateway+workstation VMs, fits homelab) only if handling something sensitive. Whonix homelab VM is a noted future project for this user — offer it, don't push it.

## User preferences (Panomete)

- Step-by-step structure, checklists, tables (trust levels), plain-language legal framing, explain every command (e.g. what `certutil` does).
- Full step-by-step note lives in the vault: `F:\obsidian_note\oralita_md\personal\note\darkweb-exploration.md` (follow local sibling-file naming conventions when updating).
- Direct, risk-first tone; no FUD; proportionate controls (start simple, escalate only if needed).

## Pitfalls

- SEO "top 100 dark web sites" content farms (tornews.com, deepstrike.io, dexpose.io, wizcase affiliate guides) — never recommend their link lists as sources.
- The Hidden Wiki + clones: mostly dead links, scams, honeypots. Skip.
- Do NOT hardcode `.onion` addresses in guidance — they rotate; teach the verified-address pattern instead.
- Onion directories rot fast; "link works" ≠ "safe content" (tor.taxi/daunt are least-bad, still caveat).

## References

- `references/verified-onion-resources.md` — resource trust table, known-good orgs with onion mirrors, address-verification principle.
