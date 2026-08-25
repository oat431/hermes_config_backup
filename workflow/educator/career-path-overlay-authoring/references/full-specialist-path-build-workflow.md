# Full Specialist-Path Build: 7 Areas in One Session

Proven pattern for filling a complete 7-area specialist career path (50 Markdown files) in a single session using parallel delegation. Validated on `08_Security_Engineer` and `09_Data_and_ML_Engineer`.

## Why a Dedicated Workflow

A 7-area path is 50 files (1 root overview + 7 overviews + 42 topic notes). Sequential creation takes too long for a single session. The three-batch fan-out below keeps each subagent's context manageable while completing the whole path in ~15 minutes.

## Phase 1: Structure and Scaffolding

1. Confirm the existing path overview at `career-path/<NN_Path_Name>/00_overview.md`. Read it to understand the 7 capability areas already defined.
2. Search the vault for existing BOK anchors (DMBOK, SWEBOK, CyBOK, SEBoK chapters) that the specialist topics should link to rather than duplicate.
3. Create all 7 capability-area folders and verify:
   ```bash
   mkdir -p 'career-path/<path>/01_...' ... 'career-path/<path>/07_...'
   ```

## Phase 2: Three-Batch Parallel Delegation

Dispatch 3 subagents with this split:

| Batch | Capability areas | Files per batch |
|---|---|---|
| Task 1 | 01, 02 | 14 |
| Task 2 | 03, 04 | 14 |
| Task 3 | 05, 06, 07 | 21 |

Each subagent's prompt must include:
- The vault root path and target folder
- All 7 critical rules (colons not em-dashes, `flowchart` not `graph`, no Mermaid parentheses/ampersands/numbered-dots, no ASCII trees, YAML frontmatter on every file)
- Exact file list with topic titles and one-line focus per file
- Frontmatter templates for both overview and topic notes
- The required topic-note sections (Why This Is a Senior Skill, Core Frameworks, In Practice, Practical Exercise, Knowledge Connections, Key Takeaways)
- Existing vault anchor wikilinks to reference
- Target line count per file (100-180 lines)
- Self-verification instruction: count files, check for em-dashes, confirm Mermaid uses `flowchart`

## Phase 3: Verification Sweep

After all subagents report completion, run a single Python sweep over the entire path folder:

```python
import os, re, json
root = r"F:\obsidian_note\swe-knowledge\career-path\<NN_Path>"
files = []
for dp, _, fn in os.walk(root):
    for f in fn:
        if f.endswith('.md'):
            files.append(os.path.join(dp, f))

fail = {k: [] for k in [
    'em_dash', 'graph_syntax', 'ascii_tree',
    'mermaid_parentheses', 'mermaid_ampersand', 'mermaid_numbered_dot',
    'placeholder', 'missing_frontmatter'
]}
for p in files:
    text = open(p, encoding='utf-8').read()
    rel = os.path.relpath(p, root)
    if '—' in text: fail['em_dash'].append(rel)
    if re.search(r'(?m)^\s*graph\s+', text): fail['graph_syntax'].append(rel)
    if re.search(r'[├└│─]', text): fail['ascii_tree'].append(rel)
    if not (text.startswith('---\n') and re.search(r'(?m)^---\s*$', text[4:])):
        fail['missing_frontmatter'].append(rel)
    for block in re.findall(r'```mermaid\s*\n(.*?)```', text, re.S):
        if '(' in block or ')' in block: fail['mermaid_parentheses'].append(rel)
        if '&' in block: fail['mermaid_ampersand'].append(rel)
        if re.search(r'\b\d+\.\s', block): fail['mermaid_numbered_dot'].append(rel)
    if re.search(r'(?i)\b(TODO|TBD|PLACEHOLDER|coming soon)\b', text):
        fail['placeholder'].append(rel)

areas = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))
counts = {a: sum(1 for f in os.listdir(os.path.join(root, a)) if f.endswith('.md')) for a in areas}
print(json.dumps({
    'files': len(files),
    'areas': len(areas),
    'area_counts': counts,
    'mermaid_blocks': sum(open(p, encoding='utf-8').read().count('```mermaid') for p in files),
    'failures': fail
}, indent=2))
```

Expected result: 50 files, 7 areas, 7 files each, all failure arrays empty. Fix any hits before proceeding.

## Phase 4: Overview Integration

The root `00_overview.md` already exists but its Capability Areas table uses BOK wikilinks. Replace the table with linked rows pointing to the newly created area folders:

```markdown
| Capability | Focus | Files |
|---|---|---|
| [[01_Area_Name/00_overview|Area Name]] | Brief focus summary | 1 overview + 6 topics |
```

Add a **Total** line below the table: `**Total:** 7 capability areas × 7 files = 49 topic files + 1 path overview = 50 files`.

## Phase 5: Commit

```bash
git add -- 'career-path/<NN_Path_Name>'
git commit -m "Complete <NN_Path_Name> career path"
```

Do NOT touch unrelated files in the working tree (e.g. checklist edits from other sessions).

## Timing Reference

| Path | Duration | Files | Mermaid blocks |
|---|---|---|---|
| 08_Security_Engineer | ~20 min | 50 | 52 |
| 09_Data_and_ML_Engineer | ~15 min | 50 | 18 |

## Pitfalls

- **Do not dispatch 4 or more subagents.** The fourth batch adds marginal speed but strains concurrent write safety on the same vault folder.
- **Do not let a subagent modify the root overview.** The root is yours to integrate in Phase 4.
- **BOK wikilinks in the existing overview may not resolve.** The root overview often references `[[02_Data_Architecture]]` or `[[11_Data_Quality]]` from a DMBOK folder that may not exist yet. Replace with local area-folder links during integration.
- **Subagent Mermaid counts vary.** Security Engineer produced 52 diagrams; Data/ML produced 18. Both passed verification. Do not enforce a minimum diagram count per area — let the subagent decide based on topic complexity.
