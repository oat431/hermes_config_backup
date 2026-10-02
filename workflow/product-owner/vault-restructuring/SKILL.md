---
name: vault-restructuring
version: 0.1.0
description: Split or move vault folders; repoint every cross-reference.
author: Panomete, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, vault, restructuring, migration, references, wikilinks]
    related_skills: []
---

# Vault Restructuring

Split, move, or rename parts of an Obsidian knowledge vault and systematically repoint every cross-reference so nothing breaks silently. Use when the user reorganizes vault structure — extracting a subfolder into a standalone repo, merging vaults, renaming folders, or moving notes between locations.

## When to Use

- User moves a vault subfolder to its own repo or standalone vault.
- User renames or restructures vault folders.
- User merges or splits vault sections.
- Any vault reorganization where cross-references (wikilinks, absolute paths, prose) could break.

Don't use for: creating/editing a single note (use the `obsidian` skill), or auditing content quality (use `knowledge-base-quality-audit`).

## Procedure

### 1. Classify files: what moves vs what stays

Scan both source and target locations. For each remaining file, determine coupling:

- **Zero coupling** — file references nothing outside its own folder. Move it.
- **Internal coupling only** — file links to siblings that also move. Move together; links resolve within the new location.
- **External coupling (bridge)** — file uses Obsidian wikilinks to resolve into a vault it would leave behind. These wikilinks break across separate Obsidian vaults. Decide: convert wikilinks to absolute paths (loses clickability) or keep the file as a bridge layer in the original vault.

Bridge-layer principle: a file that maps vault content to an external knowledge base (e.g., BOK mapping docs linking to body-of-knowledge chapters) couples to that vault's structure. It doesn't belong in a portable repo. Keep it in the source vault; move the content it indexes.

### 2. Inventory all reference types before touching files

Scan every file in the move set for:

- **External wikilinks** — `[[Note Name]]` pointing to files that stay behind. These break in the new location.
- **Internal wikilinks** — `[[Note Name]]` pointing to files that also move. These resolve fine; don't touch them.
- **Absolute path references** — `F:\path\to\old\location\` in prose or backticks. These break.
- **Relative path references** — `swe-knowledge/subfolder/` or `subfolder\` in backticks. These break if the folder moves.
- **Prose references** — the folder name mentioned in sentences (e.g., "the document_template library"). Update to the new name.
- **YAML frontmatter `name:` fields** — these are registered skill identifiers, NOT path references. NEVER change them.
- **Prose skill-by-name references** — backtick-quoted skill names like `` `project-document-templates` ``. These reference skills by registered name. NEVER change them.

### 3. Execute the move

- Create target directories (`_governance/`, category folders, `99_Archive/` as needed).
- Copy files to target, then delete from source (preserves content + clears old location).
- Delete duplicates that already exist in the target.
- Remove empty source directories (except those retaining bridge-layer files).

### 4. Repair links in moved files

Order matters — replace absolute paths first, then relative, then prose. This avoids partial-match collisions when the old and new names share a substring (e.g., `document-template` → `document_template`: hyphen vs underscore).

1. Absolute path form: `F:\old\parent\subfolder\` → `F:\new\location\`
2. Relative-with-prefix form: `old-parent/subfolder/` → `subfolder/` (the folder is now at vault root, not under old parent)
3. Standalone relative form: `subfolder\` → `new_name\` (when not preceded by old parent, not pointing to bridge docs)
4. Prose mentions: "the old-name library" → "the new-name library"
5. Obsidian tags: `document-template` → `document_template` (tag names should match the new folder name)

For wikilinks: convert `[[External Note]]` to the absolute path `F:\path\to\note.md`. Preserve `[[Internal Note]]` as-is if both notes moved together.

### 5. Scan and repoint incoming references

Search the source vault AND all related locations for references pointing INTO the moved files:

- `[[old-folder/subfolder/Template-Name]]` wikilinks — these are now broken. Repoint to absolute path.
- `old-folder/subfolder/` path references in prose — repoint.
- **Hermes profiles**: check `SOUL.md` files, skill `SKILL.md` files, and `references/` files across ALL profiles (the old path appears in section headers, table cells, and footers). Each profile's `skills/` dir is independent — the same shared skill is copied per-profile and must be updated in each copy.
- **Hermes backup**: if `F:\obsidian_note\hermes_config_backup` exists, it mirrors the live profiles (`soul-collection/` + `workflow/`). Sync it in the same pass — same replacement strategy, same skill-name exclusions.
- **Project context files**: `AGENTS.md`, `.hermes.md`, `CLAUDE.md` in any vault the user works in (e.g., `oralita_md/CLAUDE.md`).
- **External knowledge dirs**: any sibling vault that references the moved folder (e.g., `ai-knowledge/`).

### 6. Verify and commit

- Re-scan all modified locations for residual old-path references (excluding legitimate skill-name identifiers).
- **Categorize every residual** before concluding work is incomplete — a naive grep across the Hermes tree produces ~1,700+ false positives (see pitfalls 8–9). Classify each hit as source-of-truth (must fix) vs non-source-of-truth (preserve) before declaring done.
- Verify internal wikilinks in moved files still resolve within the new location.
- Verify the new repo's wikilink graph: count total wikilinks, count internally resolved, count external/broken. Target: zero unexpected broken.
- Commit to the repo and push.
- Commit and push the backup repo too if it exists.

## Pitfalls

> See `references/reference-type-classification.md` for the full matrix of which reference forms are actionable, which are identifiers to preserve, and which files to exclude from the scan entirely.

1. **YAML `name:` fields are skill identifiers, not path references.** Changing them breaks skill catalog lookups. A line like `name: document-template-authoring` in YAML frontmatter is a registered skill name — never touch it during path migration.
2. **Backtick-quoted skill names in prose are references to skills by name.** A line like `` `md-project-document-templates` in productivity category `` references a skill, not a folder. Preserve it.
3. **Bridge docs that couple to an external vault via wikilinks should stay, not move.** A BOK mapping doc with `[[BABOK v3 - Overview]]` links into a vault it would leave behind. Moving it breaks those links. Keep it as a bridge layer in the source vault.
4. **Replacement order matters when old and new names share a substring.** When renaming `document-template` to `document_template` (hyphen→underscore), replace absolute paths first, then relative, then prose. Replacing prose first can create partial matches that break later replacements.
5. **Obsidian wikilinks resolve case-insensitively.** `[[Definition-of-Done]]` resolves to `Definition-of-done.md`. A wikilink that looks mismatched may not be broken — verify before repairing.
6. **Use a mutable list container for counters inside `re.sub` callbacks.** Python's `nonlocal` binding fails inside nested functions in `exec()` contexts (like `execute_code`). Use `counter = [0]` and increment `counter[0]` instead.
7. **Quoted broken-link evidence in audit reports is not a live link.** A QG report documenting "`[[Security-Controls]]` — targets never existed" is historical evidence, not navigation. Don't repair it.
8. **Hermes session dumps and caches are not source of truth.** `sessions/request_dump_*.json` files are immutable conversation records containing the old system prompt at the time; `.skills_prompt_snapshot.json`, `.usage.json`, and `.hub/index-cache/` are auto-regenerating caches. They contain old paths but must be EXCLUDED from migration — editing immutable records falsifies history, and caches regenerate on next Hermes startup.
9. **A naive final-verification grep produces ~1,700 false positives.** Scanning the entire Hermes tree for the old name hits session dumps (immutable), snapshot/usage/hub caches (auto-regenerating), NPM `node_modules` data (third-party), and `MEMORY.md` (correctly describes the move). Categorize every hit before reporting "stale refs remain" — only `.md`/`.yaml`/`.yml` source files in `skills/` and `SOUL.md` are actionable.
10. **Do not edit Obsidian's `workspace.json` manually.** It tracks `lastOpenFiles` and will contain old paths after a move, but it is Obsidian editor state that auto-regenerates on vault open — moved files show as "not found" and drop off the recent list naturally. Hand-editing it risks corrupting workspace state.
11. **`re.sub` callback counters must use a mutable container in `execute_code`.** Python `nonlocal` raises `SyntaxError: no binding for nonlocal` inside `exec()` contexts (like `execute_code` / hermes_tools kernel). Use `counter = [0]` and increment `counter[0]` inside the callback function — never `nonlocal counter`.
12. **Check the path-stripped line, not the raw match, when classifying residuals.** When a YAML `name:` field spans two lines (`---\nname: document-template-authoring`), a line-based `rfind('\n')` capture returns the `---` delimiter line, not the `name:` line — causing misclassification as a stale path ref. Strip and match the full line including the field name.

## Verification

- [ ] Every moved file exists at the target and is gone from the source.
- [ ] Zero residual old-path references in moved files (excluding skill-name identifiers).
- [ ] Zero broken wikilinks in the new repo (all resolve internally or were converted to absolute paths).
- [ ] All incoming references from the source vault and related locations repointed.
- [ ] SOUL.md and skill files across all Hermes profiles updated (including shared skills copied per-profile).
- [ ] Hermes backup (`hermes_config_backup`) synced with the same replacements and pushed.
- [ ] Project context files (`AGENTS.md`, `CLAUDE.md`) in related vaults updated.
- [ ] Final verification: every residual categorized as source-of-truth or non-source-of-truth; only `.md`/`.yaml`/`.yml` in `skills/` and `SOUL.md` treated as actionable.
- [ ] Commits pushed to both the new repo and the backup repo.
