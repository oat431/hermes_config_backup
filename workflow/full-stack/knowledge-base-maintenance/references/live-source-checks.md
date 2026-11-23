# Live source checks for staleness audits

Where to verify what the docs claim. Prefer registry APIs and official release pages over search results — they answer "what is current" deterministically and do not rate-limit like search engines.

## Package/tool versions (curl JSON, no auth)

- npm: `https://registry.npmjs.org/<pkg>` → `dist-tags.latest` (scoped: `@scope%2Fpkg` in the URL)
- PyPI: `https://pypi.org/pypi/<pkg>/json` → `info.version`, `info.requires_python` (the floor matters as much as the version)
- crates.io: `https://crates.io/api/v1/crates/<name>` → `max_version` / `max_stable_version`
- Go modules: `https://proxy.golang.org/<module>/@latest` (module path includes `/v2` etc. for major bumps); a release tag's `go.mod` shows the declared toolchain floor: `raw.githubusercontent.com/<org>/<repo>/<tag>/go.mod`
- Maven Central: `https://repo1.maven.org/maven2/<group-as-path>/<artifact>/maven-metadata.xml` → `release`/`latest`
- GitHub: `https://api.github.com/repos/<o>/<r>/releases/latest` and `/tags` (unauthenticated works for public repos)

## EOL / support status

- endoflife.date JSON: `https://endoflife.date/api/<product>.json` — cycles and EOL dates (python, nodejs, dotnet, postgresql, …)
- Toolchain/distro download pages are canonical for "current stable" (go.dev/dl/?mode=json, nodejs.org/dist/index.json, nginx.org/en/download.html, vendor release-cycle pages)

## Standards, frameworks, regulations

- OWASP: owasp.org (Top 10, ASVS, API Security editions); genai.owasp.org (LLM / Agentic Top 10). Editions renumber IDs — cite the edition year and remap every ID when a new edition ships; the project's own announcement page confirms what changed.
- NIST: csrc.nist.gov/pubs — revisions supersede and often retitle (cite Rev. numbers).
- IETF: datatracker.ietf.org/doc/<draft>/ — check status before citing; a draft that "will become" an RFC is not an RFC.
- Supply chain / delivery: slsa.dev (spec version and level names), dora.dev (metric names change).
- W3C: w3.org/TR for editions and success-criterion numbers.
- Bibliographic claims (is that title a book or a paper?): `https://api.crossref.org/works?query.bibliographic=...&rows=5` → `type` distinguishes journal-article from book. Use Crossref, not DBLP — DBLP serves bot-checks to curl.

## Vendor renames and retirements

- A redirect is the evidence: `curl -sI <old-docs-url-or-domain>` — a 301 to a new vendor/product name justifies "(formerly X)" phrasing.
- Retirement/end-of-support notices live on the product page or vendor blog (cloud services, SaaS tools). Confirm on the vendor's own domain before flagging a product dead.

## Fetching page content

- JSON APIs via curl + `python3 -c` or grep. HTML: `curl -sL <url> | sed 's/<[^>]*>/ /g' | grep -iE '...'`.
- For readable page text use `mcp__searxng__web_url_read` or curl; `web_extract` may be search-only depending on the configured backend — route around it rather than retrying.
- When search engines return empty or the SearXNG MCP pauses on rate limits, go straight to the authoritative URL — the audit already knows which domains to check.

## Phrasing rules for evergreen docs

- If the doc set declares "no version trivia", hedge pins instead of asserting them: "X 18 (19 GA <date>)", "current stable — verify before install". Date the transition, not the claim.
- Tag standards by edition + year (e.g. "OWASP Top 10 (2026)") — unversioned cites silently drift when editions renumber.
- Keep a renamed product's old name once as "(formerly X)" — readers still search the old name; strip the old name everywhere else.
- For a superseded but still-supported baseline, say which is safe today and what lands when ("18 is the safe default; 19 GA <date>"), rather than hard-swapping the number the day of a release.
