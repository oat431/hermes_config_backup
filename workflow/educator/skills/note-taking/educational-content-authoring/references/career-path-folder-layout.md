# Career Path Overview Folder Layout

Use this layout when creating a career-path map from a starting profession such as Software Engineer.

## Target Structure

```text
career-path/
├── 00_Career_Path_Overview.md
├── 01_Software_Engineer/
│   └── 00_overview.md
├── 02_Senior_Software_Engineer/
│   └── 00_overview.md
└── NN_Role_Name/
    └── 00_overview.md
```

The root overview is the navigation map. Each role gets a stable numbered folder and its overview is always named `00_overview.md`. Future detailed notes for that role go inside the same folder.

## Authoring Sequence

1. Scan existing career and BOK material first.
2. Create the root `career-path/00_Career_Path_Overview.md`.
3. Create one overview per role as a flat working set if that is faster.
4. Create one folder per role: `NN_Role_Name/`.
5. Move each role overview to `NN_Role_Name/00_overview.md`.
6. Update the root and every cross-role link to the folder-aware target.
7. Keep the root overview at the career-path root, not inside a role folder.

## Link Rules After Moving

Because every role folder contains a file named `00_overview.md`, bare links such as `[[00_overview]]` are ambiguous. Use explicit career-path targets with display text:

```markdown
[[career-path/02_Senior_Software_Engineer/00_overview|Senior Software Engineer]]
```

Use the same explicit form in YAML frontmatter when linking to another role. For references outside the career-path folder, prefix the owning vault section when the filename is not globally unique:

```markdown
[[software-engineering-note/02_Software_Architecture/Software Architecture Overview]]
[[body-of-knowledge/PMBOK/00_Introduction]]
```

Preserve the user's clean short links only when Obsidian can resolve them unambiguously. Do not use a role folder's bare numbered basename after the move.

## Verification Checklist

- One root overview exists.
- Every role folder has exactly one `00_overview.md`.
- No old flat role overview remains at the root.
- Root and cross-role links use `career-path/<role>/00_overview` targets.
- External BOK links resolve to their owning section.
- No missing or ambiguous links remain.
- YAML frontmatter exists in every overview.
- Mermaid diagrams are present where the overview explains progression or relationships.
- Detailed topic notes have not been created before the overview map is approved.
