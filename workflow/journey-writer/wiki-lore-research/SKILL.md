---
name: wiki-lore-research
description: "Use when researching game/movie canon on fan wikis."
version: 1.0.0
author: journey-writer curator
license: MIT
category: creative
metadata:
  hermes:
    triggers:
      - canon check
      - lore lookup
      - fandom wiki
      - wiki canon
      - canon story notes
      - spoiler notes
      - what officially happened
---

# Wiki Lore Research

Verify fiction canon — BG3 today, any game, movie, or book tomorrow — against fan-maintained wikis, and turn the findings into spoiler-safe canon-reference notes for the vault.

## When to Use

- Fact-checking a campaign log while drafting ("was it Dammon at the Grove?")
- Building / extending a `spoiler_cannon_story` section in a game memoir vault
- Worldbuilding research for fiction set in an established universe
- Any "what officially happened in canon?" question about a game, film, or show

## Access Paths

### Path A — mediawiki MCP server (preferred when tools are present)

`@professional-wiki/mediawiki-mcp-server` is registered as **`mediawiki`** on this profile; its tools arrive as `mcp_mediawiki_*` (search-page, get-page, get-pages, get-site-info, list-wikis, cargo-query, …). Config: `$HERMES_HOME/profiles/journey-writer/mcp/mediawiki-mcp.json` — add new wikis there or via the `add-wiki` tool at runtime.

Note: MCP tools inject at session startup — in a session started before registration, use Path B.

### Path B — raw MediaWiki API via curl (always works)

Every MediaWiki wiki exposes `api.php`. Workflow that verifiably works:

1. **Find exact page titles first**: `action=query&list=search&srsearch=<query>&srlimit=5` — quest/character pages often have non-obvious names (e.g. "Rite of Thorns (ritual)", "Raid the Emerald Grove").
2. **Pull content one title at a time**: `action=query&prop=extracts&explaintext=1&titles=<one title>` — see pitfalls.
3. **Send a descriptive User-Agent** (`-A "HermesAgent/1.0 (contact: …)"`) — MediaWiki API etiquette; CDN-fronted wikis may filter default clients.

Full endpoint table and tested behaviors: `references/mediawiki-api-quirks.md`.

## Wiki Selection (BG3)

- **bg3.wiki** (wiki.gg) — community canon, fresh, complete quest-journal text. Default for BG3.
- **baldursgate.fandom.com** — mechanically works, but BG3 content is sparse: Fandom merged the BG3 wiki into the classic-saga wiki. Use only for BG1/BG2 lore.
- **forgottenrealms.fandom.com** — wider D&D / Forgotten Realms lore.

For a new franchise: check whether a wiki.gg community wiki exists before defaulting to Fandom; wiki.gg wikis ship Cargo (structured data) and are usually the community-maintained one.

## Canon-Note Vault Pattern

One topic per file under `spoiler_cannon_story/<act>/`, built from the skeleton in `templates/Canon-Story-Note.md`:

- Source URLs + `verified:` date in frontmatter (wikis change — date every claim)
- **The Official Story** — canon, in verified prose
- **Canon Beats That Matter Later** — seeds that pay off in later acts, so spoilers stay useful instead of trivia
- **Our Run vs Canon** — where the party's chronicle diverges, wikilinked to session logs
- A `00-Canon-Index.md` at the folder root with wikilinks; hyphenated link targets only (vault convention — never spaces)

## Pitfalls

- **API path varies by host**: bg3.wiki serves it at `/w/api.php`; Fandom at `/api.php`. If one 404s, try the other, or ask `get-site-info`.
- **`prop=extracts` returns ONE full extract per request** — pass multiple titles and every extract after the first comes back empty. Loop over titles individually.
- **cargo-query needs auth on bg3.wiki** (anonymous = permissiondenied; wiki policy, not a bug). search + get-page covers most writing needs; Cargo's bonus (structured spell/dialogue tables) only unlocks with a wiki account.
- **Fandom merges**: always sanity-check that the wiki you're querying actually covers the game you're asking about (search a character you know is in the game before trusting results).

## Support Files

- `references/mediawiki-api-quirks.md` — endpoint table, tested API behaviors, and the stdio MCP test-harness pattern
- `templates/Canon-Story-Note.md` — the canon-note skeleton used for the BG3 vault
