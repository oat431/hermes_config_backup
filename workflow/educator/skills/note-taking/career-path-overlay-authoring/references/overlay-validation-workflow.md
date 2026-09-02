# Overlay Validation Workflow

Use this reference after creating multiple capability-area notes in an Obsidian vault. It captures the repeatable checks that protect scope and note quality.

## 1. Establish the workspace and manifest

- Confirm the concrete vault or repository root before file operations.
- Read the existing role overview and list the target folder before writing.
- Write an explicit manifest containing the two folder paths, each `00_overview.md`, and the expected numbered topic files.
- Treat sibling capability areas as out of scope even when they already contain uncommitted work.

## 2. Write with scoped file operations

- Prefer complete `write_file` calls for new Markdown notes.
- For a large batch, use `execute_code` to call the file writer once per manifest path. Keep the content in the call, but do not use shell redirection or heredocs to create notes.
- Do not modify a role overview or adjacent capability folder unless the request explicitly includes it.
- Do not commit unless explicitly requested.

## 3. Validate the exact file set

For each requested folder, verify:

- The folder exists.
- The actual Markdown filenames exactly equal the manifest.
- Every file has YAML frontmatter and a non-empty title.
- Overview notes contain topic table, concept map, existing-vault anchors, self-assessment, and related links.
- Topic notes contain the senior-skill framing, core frameworks, practical exercise, knowledge connections, and key takeaways.
- Every topic contains at least one comparison or decision table and one practical exercise.

## 4. Validate Obsidian and Mermaid constraints

- Count Mermaid blocks and inspect every block's first line. It must begin with `flowchart`, never `graph`.
- Reject parentheses and bare ampersands inside Mermaid blocks. Rephrase labels or use safe HTML entities only when necessary.
- Scan new files for em-dashes and ASCII tree characters.
- Scan for placeholder markers such as `TODO`, `TBD`, `stub`, or `lorem ipsum`.
- Check trailing whitespace so diffs stay readable.

## 5. Resolve wikilinks in context

Do not resolve every link from the vault root. Split each link at the first `|` alias and `#` heading fragment, then resolve according to its form:

| Link form | Resolution base |
|---|---|
| `career-path/...`, `software-engineering-note/...`, or another vault-root path | Vault root |
| `03_.../...` or another capability-area path from a topic note | Security or role folder containing the capability areas |
| `01_Topic_Name` from a topic note | Current capability folder |
| A link with an alias | Resolve the target before the `|`, not the display text |

Report broken targets with the source file and raw target. Do not silently remove a link to make the check pass.

## 6. Verify scope in Git

Use a path-scoped status command with all untracked files shown:

```bash
git status --short --untracked-files=all -- <requested folder 1> <requested folder 2>
```

The expected result for a new fill is one untracked entry per created Markdown file. If the broader role folder shows unrelated modified or untracked entries, report them as pre-existing or out of scope and do not touch them.

## 7. Report the artifact

Return:

- What the two capability areas add
- The absolute path of every created file, grouped by folder
- File counts and any useful size summary
- Validation results, including link and Mermaid checks
- Any unrelated working-tree entries observed
- Confirmation that no commit was made
