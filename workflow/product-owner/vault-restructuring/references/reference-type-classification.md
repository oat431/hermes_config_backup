# Reference Type Classification Matrix

When scanning for old-path references after a vault move, classify each hit before acting. The table below covers every form a reference can take and whether it is actionable.

## Path-style references (ACTIONABLE — update these)

| Form | Example | Where it appears | Action |
|---|---|---|---|
| Absolute path | `F:\obsidian_note\old-parent\subfolder\File.md` | SOUL.md section headers, skill frontmatter `description`, table cells, footer lines | Replace with new absolute path |
| Absolute path (forward slash) | `F:/obsidian_note/old-parent/subfolder/` | Python code blocks, shell commands, some prose | Replace with new forward-slash path |
| Relative with prefix | `old-parent/subfolder/File.md` | Table cells in SOUL.md, skill `references/` files | Replace with `subfolder/` (folder now at vault root) |
| Standalone relative | `subfolder\File.md` (backslash) or `subfolder/File.md` | Backtick-quoted paths in table cells | Replace with `new_name\` or `new_name/` |
| Obsidian wikilink (external) | `[[old-folder/subfolder/Note-Name]]` | Career-path notes, BOK chapters | Convert to absolute path `F:\path\to\note.md` |
| Obsidian wikilink (relative) | `[[subfolder/Note-Name\|Alias]]` | Career-path notes with aliases | Convert to absolute path, drop alias or use Markdown link |
| Prose folder name | "the old-name library", "old-name system" | Skill descriptions, llmops SOUL.md, skill pitfall text | Update to new folder name |
| Obsidian tag | `tags: [..., old-name, ...]` in YAML frontmatter | Skill `tags:` arrays | Update tag to match new folder name |

## Identifier references (DO NOT TOUCH — preserve these)

| Form | Example | Why preserved | How to recognize |
|---|---|---|---|
| YAML skill name | `name: old-name-authoring` | Registered Hermes skill identifier; changing breaks catalog lookups | Line starts with `name:` in YAML frontmatter block |
| Prose skill-by-name | `` `md-project-old-name` in productivity category `` | References another skill by its registered name, not a folder path | Backtick-quoted, followed by "category" or skill-context prose |
| Wikilink to bridge doc | `[[old-folder/00_Essential Document/Note]]` | Bridge docs deliberately stay in source vault | Path contains `00_Essential Document` or the agreed bridge-layer subfolder |
| Historical audit evidence | `` `[[Security-Controls]]` — targets never existed `` | Quoted evidence in QG/audit reports documenting past broken links | Inside a table row or callout documenting a repair that was done |

## Non-source-of-truth files (EXCLUDE from scan — do not report as stale)

| File type | Path pattern | Why excluded |
|---|---|---|
| Session dumps | `sessions/request_dump_*.json` | Immutable conversation records; contain old system prompt as historical evidence |
| Skill snapshot | `.skills_prompt_snapshot.json` | Auto-regenerating cache; Hermes rebuilds on next startup |
| Usage tracking | `.usage.json` | Auto-regenerating cache; tracks skill view/use counts |
| Hub index | `.hub/index-cache/*.json` | Auto-regenerating cache; Hermes rebuilds from installed skills |
| NPM package data | `node_modules/**/db.json` | Third-party data; not the user's content |
| Memory file | `memories/MEMORY.md` | May legitimately describe the move ("moved from X to Y") — the old name appears as context, not a live reference |
| Cache spillover | `cache/spillover/*.txt`, `cache/delegation/*.txt`, `cache/exec/stdout-*.txt` | Internal temp files; auto-pruned within 24h |
| Obsidian workspace | `.obsidian/workspace.json` | Editor state (`lastOpenFiles`); auto-regenerates on vault open; hand-editing risks corruption |

## Classification decision flow

1. Is the file in a `cache/`, `sessions/`, `.hub/`, or `node_modules/` path? → **EXCLUDE** (non-source-of-truth)
2. Is it `MEMORY.md` describing the move? → **EXCLUDE** (correct context)
3. Is it `.obsidian/workspace.json`? → **EXCLUDE** (auto-regenerates)
4. Does the line start with `name:` in YAML frontmatter? → **PRESERVE** (skill identifier)
5. Is it a backtick-quoted skill name with "category" context? → **PRESERVE** (skill-by-name reference)
6. Does the path contain the bridge-layer subfolder (e.g. `00_Essential Document`)? → **PRESERVE** (bridge doc stays)
7. Is it inside an audit/QG report documenting a past broken link? → **PRESERVE** (historical evidence)
8. Otherwise → **ACTIONABLE** (update the path)
