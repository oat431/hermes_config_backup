---
name: exercise-authoring
description: "Enrich existing educational notes with hands-on coding exercises and LeetCode assignment tables. For algorithm/data-structure topics: read the note, design TODO-stub exercises, curate progressive LeetCode problems, and append both sections to the end of each file."
tags: [education, exercises, leetcode, algorithms, data-structures, obsidian, note-taking]
---

# Exercise Authoring

Enrich existing educational notes with **hands-on exercises** and **assignment problem sets**. Designed for algorithm and data-structure notes, but the pattern applies to any technical topic.

## When to Use

- User has existing notes (Obsidian, markdown) and wants practice material added
- User wants LeetCode/competitive-programming problems mapped to specific topics
- User wants guided coding exercises with TODO stubs, not just reading material

## Workflow

### 1. Scan the Notes

- Use `search_files(target='files')` to list all note files in the target directory
- Use `read_file` to read each note — understand the topic, patterns, and code examples
- Skip overview/index files (no exercises for table-of-contents notes)
- Note the programming language used in the notes (Java, Python, etc.) — exercises must match

### 2. Design Hands-On Exercises (3–4 per note)

Each exercise follows this structure:

```markdown
### Exercise N: [Pattern Name] — [Task Description]
[1-2 sentence description of what to build/solve]

```java
[Method signature with TODO comments guiding the approach]
```

**Hint:** [One-line hint that doesn't spoil the solution]
```

**Design principles:**
- **Direct application:** Each exercise maps to a specific algorithm/pattern in THAT note
- **TODO stubs, not solutions:** Give method signature + guiding comments, not working code
- **Test cases included:** "Test with X → expect Y" so the learner can verify
- **Progressive difficulty:** Exercise 1 = simplest application, last exercise = combines patterns
- **Match the note's style:** Use the same language, naming conventions, and code style

### 3. Curate Assignments (LeetCode Problems)

Build a table of curated problems:

```markdown
## Assignments

| # | Problem | Difficulty | Key Technique |
|---|---------|:----------:|---------------|
| 1 | [Problem Name](leetcode-url) (LC N) | 🟢 Easy | Technique |
| ... | ... | ... | ... |

### Assignment Guidelines
- **Start** with N–M (Easy). [Why these first]
- **Then** N–M (Medium). [What pattern they practice]
- **Problem N** (Hard) — [special note if it's a classic interview problem]
- **Target time:** X min per Easy, Y min per Medium, Z min per Hard
```

**Selection principles:**
- **6–10 problems per note** — enough for practice, not overwhelming
- **Difficulty progression:** Start Easy (2–4), then Medium (3–5), optional Hard (1–2)
- **Map each problem to a technique** from the note — don't just pick random problems
- **Include classic interview problems** (Two Sum, Valid Parentheses, etc.) where relevant
- **"Binary search on answer" problems** go under Searching, not just Arrays
- **Cross-reference:** If a problem fits multiple notes, put it in the most relevant one

### 4. Append to Notes

Use `execute_code` with a Python script to batch-append to all files. This is more efficient than individual `patch` calls when updating 10+ files:

```python
# Pattern: read file, append content, write back
for rel_path, content in exercises.items():
    full_path = os.path.join(base, rel_path)
    with open(full_path, 'a', encoding='utf-8') as f:
        f.write(content)
```

**Important:** Always append AFTER the Sources section (at the end of the file). Never insert before existing content.

## Output Format

Each note gets two new sections appended:

1. **`## Hands-On Exercises`** — 3–4 guided coding exercises with TODO stubs
2. **`## Assignments`** — Table of 6–10 LeetCode problems with difficulty and technique

Sections are separated by `---` horizontal rules.

## Problem Selection Reference

For algorithm/data-structure topics, see `references/leetcode-by-topic.md` for curated problem lists organized by topic. Use this as a starting point — always verify problems are still available and match the note's content.

## Pitfalls

- **Don't create exercises for overview/index files.** Only enrich notes with actual content.
- **Don't repeat the note's code as an exercise.** The exercise should require the learner to IMPLEMENT something, not copy.
- **Don't use `patch` for batch appends to 10+ files.** Use `execute_code` with a Python script — much faster and less error-prone.
- **Match the note's language.** If notes are in Java, exercises must be in Java. Don't mix languages.
- **Don't give away solutions in hints.** A hint should point the learner in the right direction, not solve the problem.
- **Verify LeetCode problem numbers.** Problem numbers can change. Use the problem slug (URL) as the canonical identifier.
- **`read_file` dedup after modification.** If you read a file with `read_file`, then modify it (via `write_file`, `patch`, or `terminal`), subsequent `read_file` calls may return a dedup response (`"status": "unchanged"`) instead of the actual content. Use `terminal("cat '<path>'")` to read the current content when this happens. Always check `result.keys()` — if it contains `content_returned` instead of `content`, you got deduped.
- **Windows line endings.** When splitting/rejoining file content on Windows, normalize line endings: `.replace("\r\n", "\n").replace("\r", "\n")`. MSYS/Git Bash `cat` may produce `\r\n`. Without normalization, string matching (e.g., finding section headers) can silently fail.
- **Exercise-to-chapter mapping.** When adding exercises to combined multi-chapter files, map each exercise to the specific chapter it covers. Track this mapping explicitly — don't just append all exercises to the end without knowing which chapter they belong to. This matters when the file later gets split.

## Advanced Topics (CLRS-style)

For theoretical/advanced algorithm notes (CLRS, graduate-level), the exercise format differs from practical notes:

**Hands-on exercises mix three types:**
1. **Coding exercises** — implement algorithms from the note (Union-Find, RSA, Miller-Rabin)
2. **Trace-by-hand exercises** — manually step through algorithms (B-tree insertion, Bellman-Ford relaxation, Floyd-Warshall matrices, Simplex pivots)
3. **Theory/proof exercises** — prove amortized bounds, construct LP duals, trace NP-completeness reductions

**Assignments mix:**
- LeetCode problems (where applicable — Union-Find, geometry, graph algorithms)
- Theory problems (prove X, analyze Y)
- Mini-projects (implement full algorithm — B-tree, Fibonacci heap, Simplex solver)

See `references/clrs-exercise-patterns.md` for detailed patterns by chapter.
