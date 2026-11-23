---
name: technology-selection-trade-study
description: "Use when choosing a platform or vendor for a client."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Architecture, Vendor-Selection, Trade-Study, Consulting, Client-Deliverable]
    category: software-development
    related_skills: [grounded-citations, plan, spike]
---

# Technology Selection Trade Study

For "should we build X or buy X", "which platform should the client use", "isn't
this already solved" — the recurring consulting task of picking a platform,
framework, or vendor and defending the pick to someone who is paying.

The deliverable is **a defensible shortlist plus one recommendation**, not a
feature-comparison dump. The client should be able to make a decision after one
read, and you should be able to defend every number in it.

## When to Use

- A client or stakeholder asks for "a website / app / portal" and the honest
  answer is that a product already exists
- Build-vs-buy, vendor shortlist, framework or hosting choice with money attached
- A client supplies a reference site or competitor as the requirement proxy
- Any decision where the output is "use platform A, not B, and here's why"

## Procedure

### ① Frame what is actually being bought

Separate the *software* from the *operated system*. Clients ask for "a news
website" and are really buying hosting, hardening, backups, theme, SEO config,
monetization surfaces, content migration, staff training, and someone to call
when it breaks. The platform is typically 20% of the deliverable and the
cheapest line item in it.

State this framing explicitly and early. It does two things: it justifies your
fee, and it answers "isn't this already solved?" honestly — the software is
solved, the operation is not.

### ② Fingerprint the client's reference before arguing from principle

When the client supplies a reference site, inspect its live stack. Their own
example is the strongest possible evidence and it costs one tool call:

```js
// what platform / plugins / analytics are actually running
[...document.querySelectorAll('script[src],link[href]')]
  .map(e => e.src || e.href)
  .filter(u => /wp-content|wp-includes|\/_next\/|cdn\.shopify|sites\/default|static\//.test(u))
  .slice(0, 20)
```

Then read `document.querySelector('meta[name=generator]')?.content`, the
`?ver=` query strings (often the CMS version), `<link rel="https://api.w.org/">`
and `/xmlrpc.php` (WordPress), and `<meta property="og:locale">` for the
content language.

**Mine the reference for requirements the client did not state.** Read the nav,
category URLs, author bylines, and permalink shape:

| What you see | Requirement it implies |
|---|---|
| A category named after a brand | Advertiser-branded channel pages — monetization, not taxonomy |
| Advertorial-style posts | Sponsored-content type + disclosure handling |
| Every post by one author account | No editorial roles configured; attribution + security gap |
| `/2026/10/24/164712` style URLs | Numeric permalinks, no keywords — an SEO defect to fix regardless of platform |
| No paywall or member area | Revenue is advertising, not subscriptions |

Requirements stated by the client are often narrower than the reference
implies. Trust the reference; quote it back to them.

### ③ Survey the market in tiers, not as a flat list

Always cover the same four tiers so the client sees you surveyed honestly:

1. **Mature open source / self-hosted** — the pragmatic default
2. **Category-specific specialist products** — the tier clients don't know exists
3. **Headless / composable** — right architecture, usually wrong commercial answer
4. **Hosted site builders** — often the wrong answer; if so, say why

**Find the authoritative vendor directory for the domain instead of relying on
listicles.** Regulated or institutional domains maintain vetted vendor lists
(industry bodies, platform-owner foundations, government programmes). Those
lists are the credible long tail that blog comparisons omit. Search
`<domain> vendor directory` or `<domain> cms-providers` before writing the
landscape.

### ④ Verify every price at the source

- Open the vendor's own pricing page and read the figures from the rendered page.
- Enterprise vendors **do not publish prices**. If a page says "request pricing",
  the honest output is "does not publish pricing" plus a clearly-labelled floor
  from the vendor's own comparison page or third-party analysis — never a bare
  invented number.
- Label every figure that is an estimate. Never blend verified and estimated
  numbers in one table without marking which is which.
- Convert to the client's operating currency for the headline, using a rate you
  looked up rather than recalled.
- Prices drift. Re-verify at write time; state in the appendix that the figures
  were taken from the vendor pages.

### ⑤ Detect constraint conflicts and name them

The highest-value sentence in the whole study is usually the one the client
did not want to hear. When stated constraints cannot all be satisfied, say so
arithmetically:

> "Fully managed with no technical staff" + "under $100/month" are mutually
> exclusive at the tier that solves the problem. Managed *hosting* is buyable at
> that price; managed *everything* is not. Nobody owns the pager at 3am.

Build a small table of `platform → real cost → multiple over budget`. A 7× or
20× gap ends the discussion faster than any feature argument.

Then close the gap with options: (a) client self-serves on vendor support and
accepts the risk, (b) add a maintenance retainer, (c) compromise on
flexibility for a more-managed product. Recommend one of the three explicitly.

### ⑥ Shortlist exactly three, with an explicit "why not"

Three options: primary, upgrade path, and one that loses for a specific reason.
The losing option earns credibility — it proves you surveyed rather than
defaulted.

When you drop a candidate the client themselves proposed, give the technical
reason in one line (no workflow support, lock-in, cannot export). Never remove
it silently; they will notice.

### ⑦ Structure the deliverable

Use this skeleton — it front-loads the decision:

1. **Verdict up front** — the recommendation in the first screen
2. **What the reference actually requires** — the reverse-engineered table
3. **Landscape in tiers** — including the tier they didn't know about
4. **Comparison matrix** of only the realistic shortlist
5. **What the budget cannot buy** — the constraint-conflict table
6. **Recommendation** — primary, backup, and "not at this stage"
7. **Decision tree** — Mermaid flowchart, not a table
8. **Scope you would actually sell** — the 8–10 workstreams, not "a website"
9. **Risk table** — severity + mitigation
10. **Open questions** — only ones that change the answer
11. **Sources appendix** — every price with its URL

**Mermaid over tables for decision trees.** The user prefers flowcharts for
selection logic and decision paths; reserve tables for dense feature matrices
and cost comparisons where row-by-row scanning is the point.

For a non-English client deliverable, produce the localised client-facing
version as the primary artifact and keep an English working copy alongside it.
Name files in the client's language; the agent reads either.

### ⑧ Ask only questions that change the answer

Batch these into one `clarify` call. Each one below can eliminate a whole tier:

| Question | What it eliminates |
|---|---|
| Multilingual content needed? | Platforms with theme-only i18n |
| Revenue model: ads, subscriptions, or both? | Ad-native vs membership-native platforms |
| Who operates it after launch? | Hosted vs self-managed |
| Monthly budget for hosting + maintenance? | The managed and enterprise tiers |
| Desired deliverable (shortlist / proposal / demo)? | What you write next |

Ask before spending effort on the detailed comparison — the answers reorder the
shortlist.

## Pitfalls

- **Dumping whole pages into tool output.** Never print a page's full
  `innerText`, a complete `page_info()` payload, or an entire scraped body.
  Slice around an anchor and cap the length (`t[t.find('PRICING'):][:1200]`), or
  return only the specific DOM text you need. Full-page dumps bloat context,
  slow every later turn, and can abort the response outright. Prefer several
  medium extractions that append findings to a file over one huge grab.
- **Arguing from principle instead of from their reference.** "Use a CMS" is
  weak; "the site you showed me *is* WordPress 6.9.10, verified from its own
  asset paths" is unanswerable. Fingerprint first, argue second.
- **Taking the stated requirement at face value.** "News only" collapses the
  moment the reference shows advertiser-branded categories and advertorials.
  The stated scope understates the real one; find the gap in the evidence.
- **Quoting a price you did not open the page for.** Search-result snippets
  carry stale and rounded numbers. Open the pricing page; if the vendor hides
  it, say so rather than filling the gap.
- **Burying the constraint conflict.** Delivering an in-budget option that
  cannot actually be operated is the mistake that becomes a support call in
  month four. Put the impossible arithmetic in its own section.
- **Silently dropping the client's own suggestion.** Removing a platform they
  proposed needs one explicit technical reason, in the document.
- **Recommending headless to a non-technical operator.** Headless moves design,
  SEO, editorial UX, ad integration, and all maintenance onto whoever builds
  the frontend. It wins only when the client explicitly wants a differentiated
  product and accepts ongoing development cost.
- **Shipping a localised document without a script check.** After writing Thai
  (or any non-English) prose, scan the file for characters from other scripts —
  a stray CJK glyph in Thai text is invisible to a quick skim and immediately
  discredits the document. Check programmatically, e.g.
  `any('\u4e00' <= c <= '\u9fff' for c in text)`, before delivering.
- **Treating "managed hosting" as "managed everything".** Name what managed
  hosting includes and, in a second column, what it does not (incident
  response, plugin conflicts, performance tuning, SEO, search-engine issues).

## Verification

Before delivering:

- [ ] Reference site fingerprinted; hidden requirements table included
- [ ] Every price traced to a vendor page URL in the sources appendix
- [ ] Estimated vs published prices visually distinguished
- [ ] Constraint conflicts stated with the cost multiples
- [ ] Exactly three options; rejected ones carry a reason
- [ ] Decision tree is Mermaid, not a table
- [ ] Open questions are the ones that would change the recommendation
- [ ] Localised text checked for foreign-script characters
- [ ] Scope section lists workstreams, not "build a website"

## References

- `references/news-publishing-cms.md` — news/media publishing landscape: the
  Google News Initiative vendor directory, tier map, cost points, and the
  WordPress / Ghost / Newspack trade-offs. Load when selecting a publishing or
  news platform.
