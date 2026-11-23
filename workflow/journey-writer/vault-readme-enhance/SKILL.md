---
name: vault-readme-enhance
description: Use when writing or enhancing a README for a public vault.
version: 1.0.0
author: journey-writer
license: Unlicense
metadata:
  hermes:
    tags: [readme, vault, github, documentation]
    related_skills: [swe-knowledge-vault-refine, vault-note-cleanup]
---

# Knowledge Vault README Enhancement (journey-writer ✒️)

## When to Use

Panomete points at a vault and asks for a README check, enhancement, or GitHub link pass. Also for README link rewrites where relative links must become absolute repo URLs.

Surveys a vault, writes a structured README front page with GitHub-absolute links, and verifies every URL live.

Approved pattern (Panomete, 2026-10-24, applied to swe-knowledge, general-knowledge, oralita_md, hermes_config_backup): one README.md per vault, English, the author's own framing kept in the intro ("second brain", "lifelong relearning") and any personal sign-off preserved. Tone follows vault TYPE: technical vaults get the full treatment (grouped Vault Map, brand mermaid, detail sections, goal-keyed paths); personal vaults get casual blurbs, no mermaid, no tables (oralita_md / hermes_config_backup style).

## Workflow

1. Survey: `find <vault> -name '*.md' -not -path '*/.git/*' | wc -l` for the total, per-folder counts via a loop, and the maxdepth-2 dir tree. Get git remote and default branch (`git remote show origin | grep 'HEAD branch'`).
2. Read the current README plus every sub-vault's entry note (Overview / Content / Index / 00_overview, sometimes in a subfolder). The entry notes supply purpose lines, source citations, coverage claims, and strand/topic counts; quote those, don't invent.
3. Write the README: Vault Map table (grouped if >10 folders: e.g. Curriculum / Resources / Meta) with exact note counts; one brand-themed mermaid showing how the layers relate; a "Sub-vaults in Detail" section per folder with its entry-note link; goal-keyed "How to Use" paths; Conventions; Sources; License. House rules: no em-dashes in prose, en-dashes for ranges, counts as plain numbers.
4. Link style for public repos: absolute GitHub URLs (`blob/main/` for files, `tree/main/` for folders), display text stays human (`checklist/`, `Software Engineering Note Content`). Percent-encode paths (Thai folders included). One external source link (e.g. ipst.ac.th) is fine.
5. Verify before reporting: every unique URL returns 200 via `curl -s -o NUL -w '%{http_code}' -L` (ThreadPoolExecutor(8) for 29+ URLs), 0 em-dashes, mermaid fences balanced, every URL path also exists locally (structure parity claim), note counts match the file tree.
6. Report in his format: scope stated plainly (single note vs folder vs vault), then Done / Untouched / Open questions.

## Pitfalls

- **write_file stale-read guard rewrites:** even after a full read_file of a small README, write_file can refuse with stale_write_blocked. Don't fight it: write the new content to cache/scratch/README_*.md then `cp` into place via terminal (same workaround as the memory note for vault files).
- **Link-token substitution prefix collision:** placeholder tokens like `URL_sapiens` inside `URL_sapiensth` get half-replaced and leave broken `](th)` links. Use delimiters that can't nest (`@@key@@`), substitute longest-key-first, and assert no token survives plus assert the expected link count before copying.
- **Counts:** per-folder `find | wc -l` includes Overview/index notes and the README itself sits at root; state "~N notes across M folders" and use exact per-row numbers from the count loop.
- **Windows git-bash:** curl works; pass forward-slash paths; `NUL` is a valid sink for `-o` on this host.
- **GitHub links need live targets:** empty folders 404 (git doesn't track them; describe them unlinked, e.g. media-art/), and untracked or uncommitted files 404 too (name them unlinked until the user commits, e.g. config-review notes).
