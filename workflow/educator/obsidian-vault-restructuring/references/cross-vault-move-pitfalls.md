# Cross-Vault Move Pitfalls — 2026-07-16

## Pitfalls Discovered During Framework-Aligned Vault Restructuring

1. **When moving files between vaults, move the whole directory tree.** Use `shutil.move(src_dir, dst_dir)` for folders. Don't try to move individual files from a directory you already moved — the path will be gone.

2. **After moving a directory with `shutil.move`, the original path no longer exists.** If you need to move some files from a folder and move the rest elsewhere, do the selective moves FIRST, then move the remaining folder.

3. **Verify moves with `os.walk` counts.** After moving, count .md files in both source and destination to confirm nothing was lost.

4. **Preserve duplicates when the user asks.** If the user says "keep the duplicates," don't delete the source copies. Some users keep quick-reference notes alongside deep content in a different vault.

5. **When mapping topics to frameworks, check for content overlap across vaults.** The same topic (e.g., Clean Code) may exist in multiple vaults at different depths. Don't assume one is "wrong" — ask the user which is the canonical location.

6. **Filename parsing for selective moves.** When moving numbered files (e.g., "01 Core Concepts.md"), parse the number from the start of the filename with `int(parts[0])` after splitting on space. Don't assume the whole filename is a number.
