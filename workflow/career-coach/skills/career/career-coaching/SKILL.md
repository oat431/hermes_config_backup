---
name: career-coaching
description: Review resumes, LinkedIn profiles, and job applications.
tags: [career, resume, linkedin, interview, star, job-search]
---

# Career Coaching Workflow

Comprehensive workflow for job seekers: resume review → LinkedIn audit → master profile → STAR stories → tailored applications.

## When to Use

- User asks for resume/CV review or rewrite
- User asks for LinkedIn profile audit or optimization
- User wants to build a "master profile" for job applications
- User needs STAR stories extracted for behavioral interviews
- User is preparing cover letters or job applications

## The Master Profile Pattern

Build ONE master profile (Obsidian note) that serves as the single source of truth for all job artifacts. Structure:

### 8-Block Master Profile Framework

1. **Core Identity** — Name, contact, location, languages, LinkedIn URL
2. **Professional Narrative** — 50-word story: who you are, where you've been, where you're going
3. **Experience Database** — Each job with: company, dates, role, metrics, tech stack, achievements
4. **Education & Credentials** — Degree, GPA, honors, certifications, test scores, TA experience
5. **Skills Inventory** — Categorized by proficiency (Expert/Proficient/Familiar)
6. **Projects Portfolio** — Curated list with descriptions, tech, impact, links
7. **STAR Stories** — 8-12 reusable stories covering leadership, conflict, failure, ambiguity, influence, judgment
8. **Job Search Parameters** — Target roles, industries, salary range, location preferences, deal-breakers

### Artifact Generation Order

1. Master profile (source of truth)
2. Resume (ATS-optimized, quantified)
3. LinkedIn (keyword-rich, discoverable)
4. Cover letter template (tailored per application)
5. STAR story portfolio (extracted via `/grill-me`)

## Resume Review Checklist

See `references/resume-review-checklist.md` for the full scoring rubric.

**Critical checks:**
- ATS compatibility (single-column, standard headings, no tables/graphics in headers)
- Quantification (every bullet has metrics: %, time, users, revenue)
- Action verbs (Led, Built, Migrated, Reduced — not "Responsible for")
- Professional summary (50 words, keyword-rich, achievement-focused)
- Skills section (categorized, specific technologies, not vague categories)
- Contact info (includes LinkedIn URL, language proficiency for Thai market)

## LinkedIn Audit Checklist

See `references/linkedin-audit-checklist.md` for the full audit framework.

**Critical checks:**
- Headline (keyword-rich, 220 chars max, includes role + top 4 tech + architecture keywords)
- About section (first 3 lines are critical — show before "see more" click)
- Experience detail (same quantification as resume, but expanded)
- Language levels (Thai = Native/bilingual, English = Professional working for B2+)
- Open to Work (enabled — ASK the user which visibility they use: public green frame vs Recruiters-only. The headline must match: with a public frame, drop redundant "Open to New Opportunities" phrasing and spend those characters on keywords; with Recruiters-only, keep availability text in the headline but never the green frame)
- Projects (curate to 2-4 strong projects, remove trivial learning exercises)
- Certifications (relevant to target roles)

## STAR Story Extraction

Use `/grill-me` skill to extract stories. Run 3 sessions minimum:

**Session 1: Technical Leadership**
- Biggest technical project or migration
- Focus: problem-solving, technical judgment, impact

**Session 2: People/Influence**
- Mentoring, teaching, or leading without authority
- Focus: communication, influence, team dynamics

**Session 3: Initiative/Ownership**
- Stepping up in ambiguity, taking ownership
- Focus: decision-making, accountability, learning from failure

Each session produces one polished STAR story. Add to Block 7 of master profile.

## Thai Market Specifics

See `references/thai-market.md` for salary ranges, job platforms, and conventions.

**Quick reference:**
- Mid-level SWE Bangkok: 40,000–70,000 THB/month
- Remote/international: 60,000–100,000+ THB/month
- Key platforms: JobsDB Thailand, LinkedIn, Blognone
- Always include language proficiency (Thai + English)
- Indicate relocation willingness if applying to Bangkok from provinces

## Fact Verification Pass (mandatory on EVERY review)

Agent drafts accumulate fabrication over time — details carried from earlier drafts, wrong guesses, and plausible-sounding specifics survive rewrites. Run this pass before approving any artifact:

1. **Primary-source check** — re-read the user's own resume PDF / official documents; never trust details carried from earlier drafts. (Real cases that had to be removed: an NSTDA job entry, a KMUTNB degree/award for a CMU graduate, a Node upgrade attributed to an intern instead of the user.)
2. **Official-name check** — web-search official names of tests, certifications, institutions before writing them. (Real case: CMU's English exit test is officially **CMU-eGrad** per reg.cmu.ac.th — guessed acronyms like "CMU TEP/TEGS" were wrong twice in a row.)
3. **URL check** — HTTP-check every GitHub/portfolio URL in the artifact (`curl -s -o /dev/null -w "%{http_code}" <url>`); 404 = remove the link or mark "none yet". A 404 under a personal account does NOT prove the repo doesn't exist — university/team projects often live under a GitHub **organization** account. Before deleting a link, probe `https://api.github.com/orgs/<Org>/repos` or ask the user where the repo lives. (Real case: Transmatter lived under github.com/Transmatter org; it was nearly cut because probes only hit personal accounts.)
4. **Cross-file contradiction scan** — after ANY fact correction, grep ALL artifact files (resume, LinkedIn, master profile, STAR stories) for the old value and fix every occurrence, including memory. Verify clean with a final grep.
5. **Same-file consistency scan** — look for numeric contradictions within one file (e.g., "50-person team" in About vs "20+ developers" in Experience).
6. **Attribution check** — for every achievement claim, confirm who actually did the work (user vs intern vs team). Misattributed work collapses under interview probing. When two claims LOOK contradictory (e.g., "user upgraded Node 12→24" AND "intern upgraded Node 12→24"), do NOT assume one is wrong and flip the attribution — ask about project structure first. Real case: one legacy project had 4 modules (3 API + 1 web); user did the 3 API modules (0→90%+ tests), the intern independently did the web module (Babel→Vite, 100%). Both claims were true and both belong on the resume — module-level ownership questions resolve these. Split-ownership stories are STRONGER: one bullet shows technical execution, the parallel intern result shows mentoring.
7. **Planned-but-never-used tech** — users often list tech they plan to learn. Confirm "did you use this in production?" — learning plans never go on resume/LinkedIn.
8. **Log corrections** — append a numbered "Review Notes (date)" section to the vault note documenting every correction and why, so future sessions don't reintroduce errors. Save durable corrections to memory too.

When unsure about a fact, ask the user in ONE batched question (2–4 items) before rewriting — don't guess.

### English Certification → Fluency Level (honest mapping)

| Certification | LinkedIn/resume fluency |
|---|---|
| TOEIC < 600 / A2–B1 | Limited Working Proficiency |
| TOEIC 600–780 / B2 (e.g., CMU-eGrad B2) | Professional Working Proficiency |
| TOEIC 785–900 / C1 | Full Professional Proficiency |
| TOEIC 900+ / C2 | Native or Bilingual Proficiency |

Never claim "Full Professional" on a B2 cert — interviewers probe English live and the mismatch reads as dishonesty. Keep resume and LinkedIn fluency identical.

## Pitfalls

- **Never invent metrics** — estimate and mark `[CONFIRM]`, let user verify
- **Company names must be consistent across artifacts** — use full legal names everywhere (e.g., "Agoda Services Co., Ltd.", not "Agoda" in one artifact and the full name in another). Ask the user for the registered name if unknown.
- **Headline vs discretion conflict** — "Open to New Opportunities" in a public headline contradicts a Recruiters-only Open to Work strategy (which hides the search from the current employer). Flag it; let the user choose.
- **Every skills keyword must be evidenced** — only list skills backed by an experience bullet or project; cut the rest (they invite interview questions the user can't answer).
- **Always show before/after rewrites** — suggestions alone are not actionable
- **Test ATS compatibility by extracting PDF** — if text is jumbled, ATS will reject it
- **LinkedIn language levels are often wrong** — native speakers underrate themselves
- **Curate LinkedIn projects** — 10 projects dilutes the strong ones; keep 2-4
- **Don't skip market research** — Thai conventions differ from US/EU conventions

## Related Skills

- `grill-me` — Use for STAR story extraction sessions
- `grill-with-docs` — Use when grilling also needs domain modeling
