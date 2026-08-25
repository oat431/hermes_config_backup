# ATS Score Optimization Guide

ResumeWorded (and similar ATS scanners) score resumes on 5 categories. This guide
maps each category to concrete fixes you can apply to `resume.yml` and the LaTeX
build pipeline.

## The Iteration Workflow

```
Upload resume.pdf to resumeworded.com → get score → read category flags
  → edit resume.yml → rebuild via build.sh → re-upload → repeat
```

Scores below 60 need structural fixes (section order, length). Scores 60-75 need
content fixes (verbs, keywords). Scores 75+ are application-ready.

## Category 1: Repetition

**What the scanner checks:** Repeated words/concepts across bullets.

**Diagnose with:**
```python
from collections import Counter
import re
text = open('resume.md').read().lower()
words = re.findall(r'\b[a-z]+\b', text)
for word, count in Counter(words).most_common(30):
    if count > 2: print(f"{word}: {count}x")
# Also check concept repetition:
for concept in ['intern', 'team', 'project', 'coverage', 'across']:
    print(f"{concept}: {len(re.findall(concept, text))}x")
```

**Fixes:**
- Replace "intern" with "junior developer" in some bullets (keep in job titles)
- Vary "across" → "spanning", "throughout", or restructure sentence
- Reduce "project" → use specific names ("warehouse system", "platform")
- Don't repeat the same metric in both Summary and Work bullets

## Category 2: Teamwork

**What the scanner checks:** Collaboration, coordination, cross-functional signals.

**Target keywords (aim for 5+):**
`collaborated`, `coordinated`, `cross-functional`, `stakeholders`, `team`,
`partnered`, `co-authored`, `co-led`, `facilitated`

**How to add them naturally:**
- "coordinating with DevOps engineers to standardize releases"
- "collaborated with product managers to scope features"
- "coordinated cross-functional stakeholders across backend, QA, and DevOps"
- "mentored junior developers via structured code reviews"

**Common gap:** Tech resumes read like solo work. Even IC work involves coordination
— surface it. "Led backend on a 50-person team" is teamwork even if you coded alone.

## Category 3: Communication

**What the scanner checks:** Verbs showing information flow.

**Target keywords (aim for 4+):**
`authored`, `presented`, `facilitated`, `demonstrated`, `documented`,
`reported`, `translated`, `communicated`, `negotiated`, `maintained`

**How to add them naturally:**
- "authored technical documentation adopted as the official onboarding reference"
- "translated business requirements into technical specifications"
- "demonstrated [feature] to stakeholders"

## Category 4: Analytical

**What the scanner checks:** Problem-solving, investigation, decision verbs.

**Target keywords (aim for 3+):**
`analyzed`, `identified`, `resolved`, `evaluated`, `assessed`,
`determined`, `diagnosed`, `investigated`, `measured`, `discovered`

**How to add them naturally:**
- "analyzing slow queries and implementing Redis caching"
- "identified and resolved an overnight incident-detection blind spot"
- "evaluated usage patterns to decommission legacy code"

## Category 5: Length & Depth

**What the scanner checks:** Bullet richness, action-verb-first, quantified impact.

**Bullet structure that scores well:**
```
[Action verb] + [what you did] + [how/method] + [quantified result]
```

**Examples:**
- ❌ "30% API response improvement on shipment endpoints" (metric-first, no method)
- ✅ "Improved API response time by 30% by analyzing slow queries and implementing Redis caching"

- ❌ "Documentation adopted as official reference" (passive, no verb)
- ✅ "Authored technical documentation adopted by the service owner as the official onboarding reference"

**Length rule:** 1 page for ≤5 years experience. If you hit 2 pages, tighten margins
(top/bottom 2cm → 1.27cm) and line spacing (\setstretch 1.125 → 1.0) in patch_tex.py.

## Build Pipeline Fixes for ATS

These are handled by `scripts/patch_tex.py` — verify they're applied:

| Fix | Why |
|-----|-----|
| Reorder sections: Work before Education | ATS + recruiters expect experience-first for non-entry-level |
| Rename "Basics" → "Summary" | Standard section name ATS recognizes |
| "Score:" → "GPA:" | Standard keyword |
| Remove "Keywords:" labels | Looks robotic; content stays, label goes |
| Add location to header | ATS filters by location; missing = filtered out |
| Tighten margins + spacing | Keeps 1-page fit after adding richer bullets |

## Verifying Fixes After Rebuild

```python
import pymupdf  # or: import fitz
doc = pymupdf.open('resume.pdf')
text = doc[0].get_text().lower()

# Check section order
import re
sections = re.findall(r'\b(SUMMARY|WORK|EDUCATION|SKILLS|LANGUAGES)\b', text, re.IGNORECASE)
print(f"Section order: {' → '.join(sections)}")
# Expected: Summary → Work → Education → Skills → Languages

# Check pages
print(f"Pages: {doc.page_count}")  # Must be 1 for ≤5 years exp

# Check keyword coverage
for category, keywords in {
    'communication': ['authored', 'collaborated', 'coordinated', 'mentored'],
    'analytical': ['analyzing', 'identified', 'resolved'],
    'teamwork': ['collaborated', 'coordinated', 'cross-functional', 'stakeholders'],
}.items():
    hits = [w for w in keywords if w in text]
    print(f"{category}: {len(hits)}/{len(keywords)} — {hits}")
```

## Score Benchmarks

| Score Range | Status | Action |
|-------------|--------|--------|
| <50 | Structural issues | Fix section order, length, format |
| 50-62 | Content gaps | Add teamwork/analytical/communication verbs |
| 63-74 | Good, minor gaps | Fine-tune repetition, depth |
| 75+ | Application-ready | Start submitting |
| 85+ | Excellent | Top-tier applications |
| 90+ | Achievable with Pro-plan fixes | See Pro Plan category fixes below |

**Proven: 51% → 99% in one session** with the full fix ladder (structural → verbs →
repetition → Pro-plan depth). Do not stop at 75% — the last 25 points come from
Pro-plan categories.

## Pro Plan Category Fixes (ResumeWorded paid feedback)

The free scan shows 5 categories; the Pro plan reveals 7 more. These are the
categories that separate 75% from 99%:

| Category | What it checks | Fix |
|----------|---------------|-----|
| Repetition (phrases) | Exact phrases repeated across Summary AND Work | Never reuse the same metric phrase twice — Summary says "Slashed release cycles by 95%", Work says "Reduced deployment time by 95%" |
| Readability | Filename should contain full name | Output `FirstName-LastName-Resume.pdf` (not resume.pdf) — build.sh copies it |
| Education | For mid-level, education should be 1 line, not 2 bullets | Condense to: "First-Class Honors (GPA 3.58) — Senior project won 1st Place at [competition]" |
| Length & Depth | Add ~30 words + 2 more bullets for mid-level | Pull verified achievements from master profile (parcel delivery, HR platform) |
| Growth Signals | Shows career growth; promotion mention | If user has no promotion, skip — 8/10 growth score is fine without it |
| Weak Roles | Roles described too thinly | 7-9 bullets for current role, 3 for older roles, all action-verb-first |
| Teamwork detail | Wants specific team sizes/interactions | "50-person team", "5-person DevOps team", "3-person platform team", "3 internal teams", "QA leads" |

**Word-count target:** ~430 words for 3-5 years experience (397 was "slightly too
short", 467 was fine). Mid-level = richer bullets than entry-level.

## Team Sizes Technique

ResumeWorded specifically rewards naming team sizes and counterpart teams. Every
teamwork bullet should answer "with whom, how many":
- "Led backend on a **50-person team**"
- "coordinating with a **5-person DevOps team** to standardize releases"
- "monitored by a **3-person platform team**" (Agoda)
- "analyzing usage patterns across **3 internal teams**"

## Session Case Study

**User:** Software Engineer, 3+ years, Thailand market
**Scores:** 51% → 63% → 73% → 74% → 99%

**Round 1 (51% → 63%):** Section reorder (Education before Work → Work first),
section rename (Basics → Summary), GPA label, location added, Keywords removed.

**Round 2 (63% → 73%):** Added teamwork verbs (collaborated, coordinated,
cross-functional, stakeholders), analytical verbs (analyzing, identified, resolved),
communication verbs (authored, maintained, mentored, guided), reduced repetition
(intern 6x → 2x, across 5x → 2x).

**Round 3 (73% → 74%):** Readability (all bullets ≤18 words), consistency
(React/ReactJS/React.js → single variant), education condensed, summary split
(Agoda observability vs Gosoft mentoring were merged in one bullet — misleading).

**Round 4 (74% → 99%, Pro plan):** Removed exact phrase repetition between
Summary and Work ("Drove 95% release cycle reduction" + "incident detection
latency by 87%" both appeared twice), renamed PDF to include full name, condensed
education to 1 line, added 2 bullets (parcel delivery + HR platform), added team
sizes everywhere (50-person, 5-person DevOps, 3-person platform team, 3 internal
teams). Final: 1 page, 467 words.
