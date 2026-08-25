# Verified Onion Resources & Address-Verification

Research-backed reference (searxng/web search, 2026-08-25). Addresses rotate — **never hardcode .onion addresses in guidance**; teach the verified-address pattern. Where possible cite clearnet URLs for reaching each resource.

## Resource trust table

| Resource | URL | Trust | Notes |
|---|---|---|---|
| Ahmia | ahmia.fi | 🟢 High | Open-source Tor search engine; actively filters illegal/abuse content. Safest "central station". Has own onion + clearnet gateway |
| DuckDuckGo onion | via Tor | 🟢 High | Classic entry search engine |
| dark.fail | dark.fail | 🟢 High | Most trusted verified link directory (uptime-checked, community-vetted) — still verify individual addresses |
| Tor Project docs | torproject.org | 🟢 High | Official documentation, download, bridges |
| EFF guides | eff.org | 🟢 High | Surveillance self-defense |
| tor.taxi / daunt | tor.taxi, onion.live | 🟡 Medium | Community directories; "link works" ≠ "safe content"; some list illegal categories |
| tornews.com "top 100" lists | tornews.com | 🔴 Low | SEO content farm, VPN affiliate marketing, stale links |
| deepstrike.io, dexpose.io, wizcase | — | 🔴 Low | Same content-farm category; wizcase pushes Tor-over-VPN (bad advice) |
| The Hidden Wiki + clones | — | 🔴 Low | 80% dead links, 15% scams/honeypots. Skip |

## Known-good orgs with onion mirrors (legal, interesting)

- BBC / NYT / ProPublica — journalism for censored regions; great "it's just a website" lesson
- archive.today (archive.ph) — web archiving over Tor
- Proton Mail — email fully over onion
- SecureDrop portals — real whistleblower submission infrastructure
- CIA (cia.gov) — official onion site
- Facebook — onion mirror for censored regions; impressive engineering scale

## Address-verification principle

The onion address IS the server's public-key hash — connecting proves you reached the real server (no CA, no DNS poisoning). Therefore:

- Address from a **trusted channel** (org's own clearnet HTTPS site, Onion-Location) → cryptographically certain it's real.
- Address from a **random directory** → zero assurance; typosquatted fake mirrors are trivial.

**Onion-Location**: visiting a clearnet site that offers an onion shows a purple onion icon in the Tor Browser address bar — click to jump to the site's own verified onion address.

## Verification commands (Windows)

```powershell
certutil -hashfile .\tor-browser-windows-x86_64-portable.exe SHA256
```

Compare output against official checksum from torproject.org download page. `certutil` is built into Windows; `-hashfile` computes the file fingerprint; `SHA256` selects the algorithm.

## Search-engine ecosystem (beyond the top 3)

Security-research sources also name: Torch, Haystak, OnionLand, Deep Search, VormWeb, Tor66, Excavator. Less vetted than Ahmia/DDG — mention only if user asks for depth; note the trade-off.
