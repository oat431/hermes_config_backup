# Reference: BOK Overview Pattern Examples

Concrete examples from the swe-knowledge vault showing the established BOK overview pattern.

## Top-Level Overview Pattern (Body of Knowledge - Overview.md)

From `F:\obsidian_note\swe-knowledge\body-of-knowledge\Body of Knowledge - Overview.md`:

**Structure:**
1. YAML frontmatter: `tags: [overview, body-of-knowledge, ...]`
2. Blockquote purpose statement
3. Summary table with emoji per BOK, source, edition, file count, size, focus
4. Per-BOK section: wikilink to full overview + 2-3 sentence summary + key table
5. Mermaid flowchart showing BOK relationships (nested subgraphs)
6. One-liner explanations ("PMBOK tells you *how to manage the work*")
7. Reading paths per role
8. Related links

**Key conventions observed:**
- Each BOK has a distinctive emoji: 💻 SWEBOK, 📋 PMBOK, ⚙️ SEBoK, 📊 BABOK, 🔒 CyBOK, 🗄️ DMBOK
- File counts and approximate sizes in the summary table
- Mermaid diagram uses nested subgraphs to show containment (SWEBOK inside SEBoK, PMBOK inside SEBoK)
- Reading paths are role-based ("New software engineer", "Senior engineer / tech lead", etc.)

## Subject Overview Pattern (e.g., SWEBOK v4 - Overview.md)

From `F:\obsidian_note\swe-knowledge\body-of-knowledge\SWEBOK\SWEBOK v4 - Overview.md`:

**Structure:**
1. YAML frontmatter: `tags: [overview, swebok]`
2. Blockquote with source, editor, year, topic count, page count
3. "What Is This?" — 2-3 paragraphs of context
4. Topic breakdown organized by category (e.g., 🔧 Core Engineering, 📋 Management & Process)
5. Each topic: `[[filename]]` wikilink + 1-2 sentence description + 🆕 tag for new topics
6. "What's New in V4" section (version-specific)
7. "How to Use This Vault" section
8. Reading paths by role

**Key conventions observed:**
- Categories use emoji headers: 🔧 Core Engineering, 📋 Management & Process, 🎯 Quality, 👤 Professional Practice, 🧮 Foundations
- New/changed topics get 🆕 markers
- Each topic description is 1-2 sentences — concise, not exhaustive
- Wikilinks point to filenames without paths (Obsidian resolves them)

## Math-Sci BOK Pattern (created 2026-07-18)

From `F:\obsidian_note\general-knowledge\body-of-knowledge\`:

**Top-level overview adds:**
- Inter-subject mermaid diagram with labeled edges ("rates of change", "reaction rates")
- Reading paths by academic track ("Engineering track", "Medicine track", "Tech/CS track")

**Subject overviews add:**
- Year/semester distribution table
- Prerequisites per year (explicit scaffolding)
- Internal topic dependency mermaid diagram
- Cross-links to related subjects with specific topic references
- "Key Connections to Other Subjects" section with concrete examples

## Anti-Patterns to Avoid

- ❌ Don't use SWEBOK-specific language ("Knowledge Area", "Chapter XX") for non-SWEBOK domains
- ❌ Don't skip the mermaid diagram — it's the most scannable representation
- ❌ Don't make topic descriptions longer than 2 sentences in the overview
- ❌ Don't forget reading paths — different users have different goals
- ❌ Don't create a BOK without a top-level index file
