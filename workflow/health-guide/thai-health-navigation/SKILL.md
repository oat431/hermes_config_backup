---
name: thai-health-navigation
description: Use when Thai health routing or refills. Gates + book ops.
version: 1.0.0
author: Health Guide
license: MIT
metadata:
  hermes:
    tags: [health, thai-health-system, sss, health-book, triage]
    related_skills: []
---

# Thai Health Navigation

Operational layer over the health-guide SOUL: how a guidance session actually gets done. Triage ladder, OTC limits, and the health-book template live in the SOUL — do not restate them here.

## When to Use

- Triage / "where do I go for this symptom" questions — run the SOUL's door map, with this skill's coverage gate.
- Medication refills, chronic-med continuity, hospital/clinic/pharmacy visits under any scheme.
- Coverage-scheme work: designated facility changes, effective dates, what's covered, which hotline.
- Health book upkeep: plan/visit notes, evidence archiving, handoff summaries, memory sync.

## Session procedure

1. **Read the health book first.** `F:\obsidian_note\oralita_health\00-Health-Book.md` — allergies §2 and meds §4 before ANY medication or refill guidance; coverage §1 and pointers §10 before routing. The book wins over memory on conflict.
2. **Establish the coverage gate before routing.** Which scheme (บัตรทอง/UCS, ประกันสังคม/SSS, สวัสดิการข้าราชการ/CSMBS, private), which designated facility, and whether the right is **active — not merely applied-for**. A visit to a facility whose rights are not yet effective is out-of-pocket; see `references/sss-scheme.md` for the SSS effective-date rule.
3. **Verify facility facts against current sources** — hours, scheme acceptance, phone. See retrieval pitfalls below.
4. **Deliver: door + gate + checklist** — where to go, whether the right is live, what to bring, what to say (a ready-to-speak Thai phrase for the desk). Emergency pictures lead with 1669 per the SOUL.
5. **Write the outcome artifacts:**
   - Plan/visit notes → `F:\obsidian_note\oralita_health\Health\`, topic-named (e.g. `Insulin-Refill-Plan.md`), wikilinking back to [[00-Health-Book]].
   - Evidence artifacts (app screenshots proving rights/status) → archive into `Health/` with date-stamped names, then add a §10 pointer row in the book.
   - Book updates via targeted `patch` calls, never a full rewrite: §1 coverage status, §10 pointers, §11 handoff summary filled for the next visit.
   - Memory: only durable high-signal facts (designated facility, coverage changes), patched compactly — the book holds the detail.

## Pitfalls

- **Distinguish "applied" from "active" for SSS hospital changes** — the change takes effect on fixed dates (references/sss-scheme.md). Routing to the new designated hospital before its effective date costs the user money.
- **1506 is the SSO hotline** (ประกันสังคม). 1330 is NHSO/บัตรทอง only — never route SSS questions there. 1669 EMS · 1323 mental health · 1422 disease control.
- **SSO Connect home screen shows the ACTIVE designated hospital** ("สิทธิโรงพยาบาลของคุณ"): a pending change still displays the old one, and no effective date is printed there. That card screenshotted is good evidence; exact dates come from 1506 or the hospital's SSS desk.
- **Thai OCR on app screenshots misreads small fonts** — facility names and personal names come back garbled. State which fields were legible; cross-check locator/identity fields against known facts instead of quoting OCR verbatim.
- **Fetch page content with `mcp__searxng__web_url_read`** (HTML→markdown, PDF text extraction) — the `web_extract` path here is backed by a search-only backend and rejects URL reads. Facebook post bodies return empty even via web_url_read (JS-only); the operative facts (hours changes, announcements) usually live in the search snippet, so mine the snippets.
- **Patch the health book, never rewrite it** — the user maintains it between sessions; whole-file writes clobber their concurrent edits.

## References

- `references/sss-scheme.md` — SSS (ประกันสังคม) navigation: effective-date rule, change channels, workplace-move exception, coverage scope, emergency provisions.