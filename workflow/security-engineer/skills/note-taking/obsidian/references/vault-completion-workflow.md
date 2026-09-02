# Vault Completion Workflow

Use this when the user has an Overview/MOC file with `[[wikilinks]]` and wants missing topic notes filled in from source material or general knowledge.

## Trigger

- User has a vault where some `[[Topic Name]]` links in an Overview file point to non-existent notes
- "Fill in the missing notes", "Complete the vault", "Summarize X based on the overview"

## Workflow

1. **Read source material first** — if the user has a reference document (textbook outline, SWEBOK chapter, book TOC), read it to understand what each topic should cover.

2. **Read the Overview/MOC** — the file with `[[wikilinks]]` that acts as the table of contents. Identify which links have existing files vs which are dead.

3. **Present gap analysis** — show a table: Topic | In Overview? | Has Note? | Status. Let the user confirm scope before writing.

4. **Fill missing notes** — for each missing topic, synthesize content. Sources in priority order:
   - User-specified URL (GeeksForGeeks, etc.) — fetch with curl if the page is an SPA, extract relevant sections
   - The reference/source material already provided
   - Your own knowledge of the topic
   - Do NOT fabricate — if uncertain, flag it

5. **Update the Overview** — add proper `[[wikilinks]]` to any topics that only had plain-text headings.

## Note Format (Panomete's Preferences)

Every note follows this structure:
- `# Topic N: Title`
- Brief intro (1-2 sentences)
- **Structure/Formula** — tables for rules, patterns, formulas; use LaTeX for math
- **When to Use** — categorized usage with clear examples; use tables for comparisons
- **Comparisons** — if there are similar/confusable concepts, contrast them side-by-side
- **Practical Applications / Why This Matters** — connect to real-world use; for technical topics link to SE; for language topics link to communication
- **⚠️ Target-Audience Traps** — if the user teaches a specific audience (Thai speakers, etc.), include a dedicated error-pattern section
- **Quick Test** — 5 short questions with answers
- **Sources** — cite the reference material

### Key style rules
- **Tables over prose** for rules, comparisons, and patterns
- **Bold keywords** in examples for quick scanning
- **Scannable** — someone should be able to teach from this without re-reading
- **Practical, not academic** — the user teaches functioning adults, not university students
- **❌/✅ pairs** — show wrong and right side-by-side for immediate contrast. This is more effective than describing what to avoid in prose
- **Images: `![](url)`** — embed real images from authoritative web sources (lawsofux.com, MDN, etc.). Never fabricate or generate image URLs. If you can't find a good one, skip the image rather than invent one

## Directory Structure (Panomete's Preferences)

- **Category folders** with numbered prefixes: `01 Foundation/`, `02 Tenses & Time/`
- **Flat files inside** — NOT folder-per-topic. Each `Topic Name.md` goes directly in its category folder
- Files numbered for teaching order: `01 Parts of Speech.md`, `02 Articles.md`
- For topics with sub-topics deep enough to warrant individual files, use a subfolder with an Overview index: `05 12 English Tense/` containing `05 12 English Tense Overview.md` + `05.1 Present Simple.md` through `05.12 Future Perfect Continuous.md`
- The Content/Overview file stays at vault root

## Anti-patterns to Avoid

- Don't build a university-style syllabus when the user wants a practical teaching guide — ask about the target student first
- Don't over-engineer the taxonomy — the user pushed back on an 8-section academic structure for English. Keep categories practical and minimal. If you're designing more than 6–8 top-level categories, reconsider.
- Don't create `Topic/Topic.md` folder-per-file wrappers — the filename is self-explanatory, flat is cleaner
- Don't write notes as walls of prose — tables, bullets, and clear headers make them teachable
- Don't skip the gap analysis step — the user should see what's being filled before you write 25 files
- Don't fabricate image URLs — use known authoritative sources or skip the image entirely
