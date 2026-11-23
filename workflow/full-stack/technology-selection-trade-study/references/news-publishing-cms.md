# News / Media Publishing Platform Landscape

Domain depth for selecting a publishing platform. Load alongside the
`technology-selection-trade-study` procedure.

**All figures are point-in-time surveys — re-verify at the vendor pricing page
before quoting.** Prices and plan limits change quarterly.

---

## 1. The vendor directory trick

The Google News Initiative maintains a vetted directory of CMS providers built
specifically for newsrooms at `newsinitiative.withgoogle.com/cms-providers/`.
This is the credible long tail that blog listicles omit — search it before
writing the landscape. Providers listed:

> Arc XP · Atex · BLOX · Drupal Foundation · Eidosmedia · Ghost · InterRed ·
> Layout International · Livingdocs · Naviga Global · Newspack · Quintype Bold
> CMS · Ring Publishing · Stibo DX · Tresite · WhiteBeard News Suite · WoodWing ·
> WordPress Foundation · WordPress VIP · Xalok

Most clients have never heard of this category and are surprised it exists.
Naming it demonstrates coverage; most entries are correctly out of scope for a
single regional outlet.

---

## 2. Tier map

### Tier 0 — Hosted site builders

| Platform | Fit for news | Reality |
|---|---|---|
| **Wix** | ✗ Poor | No multi-role editorial workflow (writer → editor → publisher), shallow taxonomy, **cannot cleanly export structured content** (lock-in). Right for a brochure site, a trap for a newsroom |
| **Squarespace** | ✗ Poor | Templates look good; thin editorial tooling, limited ad-slot control |
| **Webflow** | △ Niche | Excellent design control, but a *design* tool — awkward for high-frequency publishing and large archives; needs a designer on staff |

### Tier 1 — Self-hosted open source

| Platform | Stack | Strengths | Watch-outs |
|---|---|---|---|
| **WordPress.org** | PHP / MySQL | ~43% of all websites, ~62% of the CMS market. Deepest news ecosystem: multi-level taxonomy, editorial roles, scheduled publishing, news sitemaps (Yoast / Rank Math), AMP/PWA, AdSense / Google Ad Manager, header bidding, mature Thai localisation, large local talent pool | The **single most attacked CMS on the web**. Plugin sprawl produces slow, fragile sites. Requires real hardening: managed updates, WAF, backups, staging, an allowlist of approved plugins |
| **Ghost** | Node.js | Purpose-built for publishing. Native newsletter + paid memberships via Stripe, clean editor, very fast, minimal attack surface. 300+ newsrooms in 40+ countries; partners with Google News Initiative, LION Publishers, Tiny News Collective | **No native multilingual *content*** (i18n covers theme strings only). Shallower taxonomy (tags, limited custom taxonomies). No native ads, comments, or ad-server integration. Self-hosted newsletter delivery is locked to Mailgun |
| **Drupal + Thunder** | PHP | Enterprise-grade structured content, granular editorial workflow. **Thunder** is a Drupal distribution built specifically for publishers (Hubert Burda Media) and is in the GNI directory | Steep curve, small talent pool in most markets, expensive to staff |
| **Craft CMS** | PHP | Superb relational content modelling, clean editorial UX | Small ecosystem; commercial licence (Solo free, Pro ~$299/project) |

### Tier 2 — Newsroom-specific products

| Platform | What it is | Cost surveyed | Fit |
|---|---|---|---|
| **Newspack** ⭐ | WordPress from Automattic, purpose-tuned for small/mid newsrooms; funded in part by Google News Initiative, Knight Foundation, Lenfest Institute. Ships custom homepage builder, multimedia story templates, integrated newsletter + metered paywall + memberships, ad management incl. AdX and header bidding, staging site, **free migration**, 200 GB storage, CDN + edge cache, security scanning, 99.9% uptime, designated Technical Account Manager | ~**$750/mo** (revenue <$300k) · **$1,500/mo** ($300k–600k) · **$2,500/mo** ($600k–1m); contact above $1m. **Price is tied to the client's revenue tier** — a structural gotcha for a growing publisher | Best-matched product for a small ad-funded regional newsroom that does not want to run a stack |
| **WordPress VIP** | Enterprise WordPress (Al Jazeera, Pew Research, Time). 99.95–99.99% uptime SLA, Parse.ly analytics, plugin review gate on every plugin | **Does not publish pricing** ("request pricing"). Floor commonly cited around **~$25,000/yr** from VIP's own comparison pages and third-party reviews | Overkill below serious scale, but the right name to raise if the client plans an ad-funded scale play |
| **Arc XP** | Born inside The Washington Post. Highly customisable content + site management | **Does not publish pricing**; third-party estimates ~**$10,000+/mo**, some outlets report $100–150k/yr | Enterprise media groups only |

Remaining GNI providers (Naviga, Stibo DX, Eidosmedia, Atex, Ring Publishing,
Quintype Bold, Livingdocs, BLOX, WoodWing, Xalok, InterRed, Tresite, Layout
International, WhiteBeard) are broadcast/large-media-group systems — six-figure
commitments. One line in the study to show coverage, then move on.

### Tier 3 — Headless

| Platform | Model | Note |
|---|---|---|
| **Payload** | MIT, TypeScript-first, runs *inside* a Next.js app (Figma-owned) | Best DX for a bespoke news frontend + content API |
| **Sanity** | Managed, GROQ queries | Best editor UX and image CDN; content reuse across app and site |
| **Strapi** | MIT, Community edition free self-hosted; Strapi Cloud paid tier (no longer a free Cloud plan) | Self-hosted data ownership, auto-generated REST/GraphQL |
| **Directus · Storyblok · Hygraph · Prismic** | Managed headless | Varying niches |
| **Contentful** | Managed incumbent | Enterprise budget, multi-brand |

Headless is the right architecture for a media *product* with an app and the
wrong commercial answer to "we want a news website" — it transfers design, SEO,
editorial UX, ad integration, and all maintenance to the builder.

---

## 3. Cost points that decide real engagements

| Option | Realistic monthly | Notes |
|---|---|---|
| WordPress on a local managed host | 150–800 THB | Thai providers bundle WordPress firewall, malware scanning, 24/7 Thai support |
| WordPress.com **Business** | ~$25/mo yearly (~845 THB) | Allows plugins, SFTP/SSH, WP-CLI, GitHub deploys **and third-party ad code** (AdSense is gated to Business+) |
| Managed WordPress (Kinsta, WP Engine) | $28–35/mo entry | Real staging, daily backups, 24/7 chat |
| Ghost(Pro) | $15 / $29 / $199 / custom | Starter / Publisher / Business / Custom, billed yearly; member caps 1,000 / 1,000 / 10,000 / unlimited |
| Self-hosted Ghost | $4–12 VPS + Mailgun from ~$15/mo | Mailgun Basic ~10,000 emails/mo |

### The WordPress.com plugin-directory gotcha

WordPress.com Business grants plugin installs but **restricts you to the
WordPress.com plugin directory**, not the general WordPress.org repository. For
an ad-funded or sponsored-content outlet this is a hard constraint: the specific
ad-management and sponsored-post plugins may be unavailable. This is usually
the deciding fact between "WordPress.com Business" and "WordPress.org on a
managed host" — the managed host wins on flexibility at a lower price, the
WordPress.com plan wins on "nothing to operate".

---

## 4. Decision heuristics

```mermaid
flowchart TD
    A[News site requirement] --> B{Multilingual content?}
    B -->|Yes| W[WordPress + Polylang/WPML<br/>Ghost eliminated]
    B -->|No| C{Revenue model?}
    C -->|Subscriptions / paid newsletter| G[⭐ Ghost<br/>native Stripe memberships]
    C -->|Ads + sponsored content| D{Monthly budget?}
    C -->|Both| N[WordPress + membership plugin<br/>or Newspack]
    D -->|Under ~3,400 THB| E[⭐ WordPress on a local managed host<br/>full plugin freedom + local support]
    D -->|[~25,000 THB]| F[⭐ Newspack]
    D -->|Enterprise| V[WordPress VIP / Arc XP]
    E --> H{Anyone to operate it?}
    H -->|No| I[Add a maintenance retainer<br/>or accept documented risk]
    H -->|Yes| J[Proceed]
```

**Hard eliminations:**

- **Multilingual content** → eliminates Ghost (theme-only i18n)
- **Ad / sponsored-content revenue** → weakens Ghost badly (no native ads)
- **"Fully managed" + tiny budget** → eliminates Newspack and everything above
- **Non-technical operator** → eliminates headless and self-hosted-without-support

---

## 5. What a regional news WordPress site looks like under the hood

Useful expectations when fingerprinting a client's reference outlet. A typical
ad-funded regional news site is a stock WordPress install with a news theme:

| Signal | Reading |
|---|---|
| `/wp-content/uploads/`, `/wp-content/cache/minify/` | WordPress + a caching/minify plugin |
| `wp-includes/js/wp-emoji-release.min.js?ver=X` | WP core version in the `?ver=` string |
| `<link rel="https://api.w.org/" href="/wp-json/">` | Canonical WP REST API discovery link |
| `/xmlrpc.php?rsd` in `EditURI` | XML-RPC enabled — often should be disabled for security |
| `meta[name=generator]` = a plugin name | The generator tag is usually claimed by an SEO/analytics plugin, not WP core, so this alone does not confirm the CMS |
| Cloudflare beacon script | CDN in front |
| Permalinks `/%year%/%monthnum%/%day%/%post_id%/` | Numeric IDs, no keywords — SEO defect worth flagging |
| Author byline identical on every post | Single shared account; no editorial roles, no attribution, no security boundary |
| A nav category named after a brand | Advertiser channel — the site earns from sponsored sections, not subscriptions |

Fix list that applies regardless of platform: human-readable localised slugs,
per-person accounts with 2FA, a distinct sponsored-content type with a visible
disclosure label, news sitemap + `NewsArticle` structured data, and consent
handling for local privacy law (e.g. Thailand's PDPA).
