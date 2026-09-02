---
name: career-artifact-prep
description: Build resume, LinkedIn, STAR stories from master profile.
tags: [career, resume, linkedin, interview, star, job-search]
---

# Career Artifact Preparation

Build and refine job search artifacts (resume, LinkedIn profile, cover letters, STAR stories) from a single master profile source of truth. Designed for the `career-coach` profile's workflow.

## When to Use

- User is actively job hunting or updating career materials
- User asks for resume review, LinkedIn audit, or interview prep
- User wants to extract STAR stories from their experience
- User needs to tailor artifacts for a specific role or market

## Core Workflow

### Phase 1: Audit Existing Artifacts

Review what the user already has (resume PDF, LinkedIn URL, existing cover letters):

1. **Extract content** from PDF resume using `read_file` (auto-converts PDFs)
2. **Fetch LinkedIn** via `mcp__searxng__web_url_read` (public profile) or browser if blocked
3. **Cross-reference** resume vs LinkedIn for inconsistencies:
   - Headline/title mismatches
   - Metric discrepancies (e.g., resume says "10+ interns", LinkedIn says "4")
   - Missing sections on one but not the other
   - Dates that don't align
4. **Score each artifact** (0-100) with explicit criteria
5. **Save findings** to user's vault with before/after rewrites

### Phase 2: Build Master Profile

Create a single source of truth (`<Name>.md`) containing 8 data blocks:

| Block | Content |
|-------|---------|
| 1. Core Identity | Name, contact, location, languages, nationality |
| 2. Professional Narrative | Career story, target roles, industries |
| 3. Experience Database | Each job: raw metrics, tech stack, achievements, team size |
| 4. Education & Credentials | Degrees, GPA, honors, certifications, test scores |
| 5. Skills Inventory | Categorized with proficiency (Expert/Proficient/Familiar) |
| 6. Projects Portfolio | Curated list with descriptions, tech, impact, links |
| 7. STAR Stories | 8-12 reusable behavioral stories (see STAR Extraction below) |
| 8. Job Search Parameters | Target salary, location, work arrangement, deal-breakers |

**Separate artifact-specific notes** alongside the master:
- `<Name>-Resume.md` — resume-specific improvements and rewrites
- `<Name>-LinkedIn.md` — LinkedIn-specific improvements and rewrites
- `<Name>-STAR-Stories.md` — full STAR story portfolio
- `<Name>-Cover-Letters.md` — tailored cover letters per application

### Phase 3: Metric Validation

User-provided numbers often differ from your estimates. **Always confirm**:

- Present estimated metrics in a checklist format
- Ask user to confirm or correct each number
- Rough estimates are fine — "about 50%" is better than nothing
- Flag numbers that are **below industry standard** (e.g., 95% uptime when 99.9% is expected) and advise omitting or reframing

### Phase 4: STAR Story Extraction

Use the `grill-me` skill to extract stories via iterative questioning. Run 3-4 rounds per story:

**Round 1: Set the Scene**
- What was the system/project? Who were the users?
- What were the pain points? (Be specific — not "slow", but "took a day to deploy")
- Team structure and your role
- Why was this project initiated?

**Round 2: Your Specific Role**
- What did YOU do vs. what the team did? (Critical for avoiding overclaiming)
- Were you assigned specific modules/components?
- Did you make architectural decisions?
- Did you mentor or coordinate others?

**Round 3: Technical Challenges**
- ONE specific difficult problem you solved
- What made it hard? (Complexity, dependencies, no documentation, data issues)
- What specific technical approach did you take?
- Tools, libraries, patterns used

**Round 4: Final Impact**
- Timeline (how long did you work on it?)
- Quantified outcomes (real numbers, not estimates)
- What did you learn?
- Business feedback (if any)
- How did it end? (Handoff, go-live, next phase)

### Phase 5: Fact Verification Pass

Before delivering ANY artifact, run the verification protocol: primary sources, official names, URL checks, cross-file grep, attribution. Full checklist lives in the `career-coaching` skill under "Fact Verification Pass". Non-negotiable — drafts accumulate fabrication across rewrites (real cases: wrong university, fake award, misattributed work, non-existent GitHub URLs all survived multiple drafts).

### Phase 6: ATS Optimization

**Run the resume through an ATS scanner** (resumeworded.com, jobscan.co) and iterate
until the score is 75+. Scores below 60 indicate structural issues; 60-74 indicate
content gaps. **Proven achievable: 51% → 99% in one session** — the full fix
ladder is documented in `references/ats-optimization.md`, including the Pro-plan
categories (phrase-level repetition, filename, team sizes, education condensation).

The 5 categories ResumeWorded scores (and how to fix each):
1. **Repetition** — Vary repeated words (intern → junior developer, across → spanning)
2. **Teamwork** — Add collaboration verbs: collaborated, coordinated, cross-functional, stakeholders
3. **Communication** — Add info-flow verbs: authored, translated, maintained, mentored
4. **Analytical** — Add problem-solving verbs: analyzed, identified, resolved, evaluated
5. **Length & Depth** — Bullets must start with action verbs, include method + quantified result

**For mid-level candidates (3+ years):** yamlresume's Jake template puts Education
before Work — the patch script reorders this. ATS and recruiters expect
Experience-first for anyone past entry-level.

Full category-by-category fix guide with diagnostic scripts: `references/ats-optimization.md`

### Phase 7: Polish & Deliver

For each artifact:
- Show **before/after** rewrites with explanation of *why* each change works
- Include **interview tips** and **watch out for** follow-up questions
- Map each STAR story to the behavioral questions it can answer

## Interview-Prep Vault Structure (multi-company)

When the user has several concurrent interviews, organize the interview-prep vault on one rule:

> `career/` = facts about YOU (true regardless of which company interviews you).
> `<company>/` = facts about THEM + your application to them (changes per company).

If a note is still true when walking into the NEXT company's interview → it belongs in `career/`. If it mentions the company's JD, panel, or date → it stays in the company folder and links UP to `career/` via wikilinks instead of duplicating.

**Centralize in `career/` (reusable):**
- Master profile (`<Name>.md`) — single source of truth
- STAR story portfolio (one file; merge spoken versions in — never keep a second copy in a company folder)
- Honesty/landmine scripts (e.g. Scripts A–F: "years of React?", "state management?", "why leaving?") — company flavor becomes a per-company variant note
- Attribution rules (who did what — survives probing in EVERY interview)
- Positioning / narrative spine
- Confirmed-facts (verified during one company's prep: real years of X, never-used tech Y, test tools) — **must be written back into the master profile**, or the next prep session re-discovers them the hard way
- Study content (React deep dive, testing, build tools) — reusable material; only the gap PRIORITIZATION is JD-specific
- "Why I'm leaving current employer" private note — raw version stays private; only the public flip script leaves the vault

**Keep in `<company>/` (company-specific):** battle card, JD fit assessment (line-by-line JD mapping), practice plan/day-of checklist, company research, post-interview retro, drill questions.

**Recruiter emails:** store inside the company folder as `00_Recruiting_Email.md` — do NOT keep a shared `context/` folder. One folder per company must be self-contained.

**Refactor mechanics (verified workflow):**
1. Use `git mv` for every move — history survives, git detects renames
2. Obsidian wikilinks resolve vault-wide by FILENAME: plain moves (folder change, same filename) don't break links; RENAMES do
3. After any rename, grep the whole vault for stale links: `grep -rn --include='*.md' -E '\[\[(Old_Name|Other_Old_Name)\]\]' .` — check ALL subfolders (study notes, answer cards, drills are the usual stragglers), not just the files you think reference it
4. Also grep absolute path references (`F:\...\old\folder\...`)
5. A "broken" wikilink may point to a file at the vault ROOT (misplaced, not missing) — search the whole vault for the target name before declaring it broken
6. When patching markdown tables, keep the full row in BOTH old_string and new_string — a partial-row patch can silently swallow an adjacent row (caught this live: a JD-mapping table row got deleted and had to be restored)

Full worked example (MISUMI prep → central `career/`): `references/interview-prep-vault-structure.md`

## Key Principles

### Resume Length: 1-Page Resume vs Multi-Page CV

Users often confuse resume and CV, or bring a 2-3 page resume. Clarify early:

| | Resume | CV (Curriculum Vitae) |
|---|---|---|
| Length | 1 page (2 max for senior) | No limit (2-10+ pages) |
| Purpose | Get an interview | Document full career |
| Content | Only what's relevant to THIS role | Everything: publications, all projects |
| Used for | Industry jobs | Academia, research, medicine |
| Thai market | **Resume format is the norm** | Rare unless applying to universities |

**Rule of thumb:** For ≤5 years experience targeting industry roles, push for 1 page.

**To cut from 2 pages → 1 page (in priority order):**
1. Remove **Projects** section — if already covered in Work Experience, it's redundant
2. Remove **Interests** section — no hiring value
3. Condense **Summary** to 3 bullets max
4. Fold **Awards** into Education (1 line)
5. Reduce **Skills** from 5 categories to 3, condensed
6. Trim longest Work Experience bullets (keep top 5 per role)
7. Remove **Keywords** lines under each role (already in Skills section)

### Metric Framing

- **Strong numbers → highlight**: 95% reduction, 100% test coverage, 10,000 devices
- **Weak numbers → omit or reframe**: 95% uptime (below 99.9% standard) → focus on transaction volume instead
- **No numbers → estimate with user confirmation**: Always get user to verify before publishing

### Story Framing

Reframe potentially negative situations positively:
- "Internal outsource team" → "Internal consulting team trusted for high-priority projects"
- "They couldn't code" → "I recognized their strengths and channeled them into work where they excelled"
- "Helped finish" → "Collaborated to complete" (own your specific contribution)
- "Temporary lead" → "Led during critical phase" with explanation of resource pool model

### Honesty Guard

- Never let user overclaim: If they say "I built X" but actually "helped finish X", probe for specific contribution
- Cross-reference numbers between resume and LinkedIn (e.g., "10+ interns" vs actual "4")
- Flag when a story might not survive interview probing

## Common Pitfalls

- **Two-column resume layouts** break ATS parsing — always recommend single-column
- **Thai market specifics**: Include language proficiency (Thai = Native), LinkedIn is essential in 2025+, Open to Work setting for recruiters
- **Missing target roles**: Industry alone is insufficient — need specific job titles for keyword optimization
- **Generic professional summaries**: Replace personality traits ("quick learner", "friendly") with selling points (years of experience, key achievements, tech stack)
- **Underselling**: Users often underestimate their impact. Push for real numbers — they're usually more impressive than expected
- **Attribution drift when pulling bullets from master profile**: Real case — master profile said "Built IoT monitoring platform (Golang)" but the truth was "only contributed Node 12→24 upgrade, platform is Node.js, did NOT build it". Every time you move an achievement from the master profile into a resume/LinkedIn bullet, re-verify (a) did the user actually BUILD it or only CONTRIBUTE, (b) the tech stack is right. Users are busy; they will not re-read every bullet — the agent must ask specifically. Ask one pointed question per suspicious bullet: "did you build this or just upgrade/help?"
- **English test name guessing**: Do NOT guess the name of a university's English proficiency test. User said "something like CMU TEP" — web search found the official registrar page (CMU-eGrad at reg.cmu.ac.th/egrad-reserve), which was the correct official name; the agent's earlier guess (CMU TEGS) was wrong. Always verify institutional test names via the registrar's official site before writing them.
- **Company legal names**: Verify full legal company names (e.g., "Agoda Services Co., Ltd.") — user or their documents know these; asking takes 5 seconds, getting it wrong looks careless in both resume and LinkedIn.
- **Award claims need primary sources**: "2nd place KMUTNB competition" in an old draft was wrong three ways (1st not 2nd, CMU not KMUTNB, SE Show Pro CAMT 14 not generic). User provided the official CMU news article as proof — treat award claims as unverified until the user shows a primary source URL.

## Market Research

For Thai job market (update annually):
- Use `mcp__searxng__web_url_read` on Robert Walters Thailand, Tech Interview Handbook, local job boards
- Salary ranges vary significantly by company type (Thai corporate vs. international vs. startup)
- ATS adoption is growing in Thailand — single-column format increasingly important

## Related Skills

- `grill-me` — Use for STAR story extraction rounds
- `obsidian` — Use for saving artifacts to vault
- `pdf` — Use if user needs PDF output of final resume

## Support Files

- `references/star-question-bank.md` — Common behavioral questions mapped to story dimensions
- `references/yamlresume-workflow.md` — YAMLResume build pipeline, schema constraints, LaTeX troubleshooting on Windows/MiKTeX
- `references/ats-optimization.md` — ResumeWorded ATS score optimization: 5 categories, diagnostic scripts, bullet rewriting guide
- `scripts/build_resume.sh` — Automated build: YAML → patched TeX → PDF (handles font/CJK fixes)
- `scripts/patch_tex.py` — Patches resume.tex: Linux Libertine → Times New Roman, disables ctex/CJK for English-only resumes
