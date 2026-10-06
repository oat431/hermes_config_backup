# Vault Reorg Playbook

Battle-tested sequence for reorganizing an Obsidian vault that is ALSO a git repo
(possibly public). Proven on oralita_md 2026-08-22: 99 notes, catch-all "Quick Note"
dissolved into topic homes, 2 commits pushed, zero newly-broken links.

## 0. Scope rules
- Ask which folders are out of scope (tool backups, etc.) and prune them from EVERY
  scan, not just the first.
- Always prune `.git/` and `.obsidian/`. On a git vault, `search_files` returns object
  noise — prefer `find <vault> -type d <prunes> -prune -o -type f -name '*.md' -print`.

## 1. Recon (before proposing anything)
a) **git state**: `git -C <vault> status --short` + `ls-files`.
   - Detects half-done USER moves: on-disk deletions + untracked new folders mean the
     user already started reorganizing while the git index still points at OLD paths.
   - Consequence: tracked files must move via `git mv`; untracked via plain rename.
b) **Link map**: parse all `[[links]]`, resolve by basename (case-insensitive), record
   out/in counts per file, unresolved targets, cross-folder links.
   - Blast-radius rule: basename-style wikilinks SURVIVE folder moves untouched.
     Only RENAMES break links — inbound links AND self-links citing the old title.
c) **Read heads of similar/suspect notes** to classify: near-duplicates (merge
   candidates), different doc types of one system (keep both + cross-link), stubs
   (absorb into a topic note).
d) **PII/secret scan** when the vault is a pushed repo — regex over files that might
   stay public: `(token|secret|password|api[_-]?key|client[_-]?secret|Bearer|sk-|AIza|ghp_|gho_)`.
   Sanitized docs (placeholders like `sk-or-...`, `<secret>`) are fine to publish;
   real names, emails, phone digits, income, private DNS IDs are not.

## 2. Propose → clarify
Present findings + a menu of escalating approaches (light touch / regroup /
conventions pass / repo split). Ask the PII question separately with concrete options
(unpublish now, full history scrub, user handles repo side). One clarify call, several
questions. Do not start moving files before the user picks.

## 3. Execute moves
- Move files FIRST, edit content SECOND (indexes, cross-links, stale internal links).
- `git mv` for tracked paths; `os.rename` for untracked; `git add -A` catches the rest.
- Repeated unresolved links to one nonexistent note (e.g. 6 audits →
  `[[Homelab-Infra-Checklist]]`) = a missing MOC the user intended to create. Create it
  with an index table + standing sections drawn from the linking files' structure.
- Renames: fix inbound links and the file's own self-references to its old title.

## 4. Unpublish-but-keep-local (PII)
1. Rewrite `.gitignore` (folder-level `/career/` or file-level entries).
2. `git rm --cached <paths>` — keeps disk copies, drops from index.
3. Commit + push.
4. VERIFY: `git ls-files | grep -iE '<pii-patterns>'` returns nothing; every file
   still exists on disk.
5. Tell the user git HISTORY still contains the data; `git filter-repo` scrub or
   flipping the repo private is a separate, explicit decision.

## 5. Post-move verification
Re-run link resolution over the whole vault. Classify remaining unresolved:
- Pre-existing cross-VAULT links (e.g. grammar notes living in another vault) →
  leave alone, document the policy (README note works well).
- Newly broken by YOUR renames → fix immediately and commit.
The bar is zero NEW breaks, not zero breaks overall.

## Pitfalls encountered
- **Windows + Obsidian**: `os.rmdir` on an empty folder Obsidian holds open →
  `PermissionError`. Harmless — git doesn't track empty dirs; clears after an
  Obsidian restart. Note it for the user instead of retrying.
- **LF→CRLF warnings** on `git add` are cosmetic on Windows; ignore.
- Unicode/Thai filenames move fine with `git mv`; keep paths quoted.
- **Self-link rename break** is easy to miss: inbound-link scans skip it because the
  source IS the renamed file.
