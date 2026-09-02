# GitHub Stats Cards — Current Landscape (2026-08-31)

## The original: `github-readme-stats`

**Status: UNMAINTAINED** — repo reads: "This repository is no longer maintained. Please use the successor project GitHub Stats Extended instead!"

- Repo: `anuraghazra/github-readme-stats`
- URL: `https://github-readme-stats.vercel.app`
- Cards: GitHub Stats (`/api`), Top Languages (`/api/top-langs`), Repo Pins (`/api/pin`), Gist Pins (`/api/gist`), WakaTime (`/api/wakatime`)
- Themes: `dark`, `radical`, `merko`, `gruvbox`, `tokyonight`, `onedark`, `cobalt`, `synthwave`, `highcontrast`, `dracula`, `transparent`

## The successor: `github-stats-extended`

**Status: ACTIVE** — community fork that took over maintenance.

- Repo: `stats-organization/github-stats-extended`
- URL: `https://github-stats-extended.vercel.app`
- Same API, same card designs, same themes
- New features over the original:
  - `show=reviews,discussions_started,discussions_answered,prs_merged,prs_merged_percentage,prs_authored,prs_commented,prs_reviewed,issues_authored,issues_commented`
  - `rank_icon=github|percentile|default` — pick how rank displays
  - `repo=` and `owner=` filters — scope stats to specific repos or orgs
  - `locale=th` — Thai and 50+ other languages supported
  - `layout=donut|donut-vertical|pie` for top languages
  - `number_format=short|long` and `number_precision=0|1|2`
  - `transparent` theme — works on both light and dark GitHub themes
  - `<picture>` element support for proper dark/light mode switching
  - `hide_values=true` — display top languages without numbers
- Docs: `docs/advanced_documentation.md` (58KB, comprehensive)
- Deploy guide: `docs/deploy.md`

## Self-Hosting Options

### Option 1: GitHub Action (easier, zero infra)

- Repo: `stats-organization/github-readme-stats-action`
- How: Create `.github/workflows/grs.yml` in your profile repo
- Action generates static SVGs → commits them to your repo → embed from your own repo
- Updates: once daily (cron) or on-demand (workflow_dispatch)
- No server, no Vercel, no external dependency

```yaml
name: Update README cards
on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v6
      - name: Generate stats card
        uses: stats-organization/github-readme-stats-action@v2
        with:
          card: stats
          options: username=${{ github.repository_owner }}&show_icons=true
          path: profile/stats.svg
          token: ${{ secrets.GITHUB_TOKEN }}
      - name: Commit cards
        run: |
          git config user.name "github-actions[bot]"
          git add profile/*.svg
          git commit -m "Update README cards" || exit 0
          git push
```

Embed: `![Stats](./profile/stats.svg)`

### Option 2: Vercel Self-Host (full control)

- Fork the repo, deploy to Vercel, set `PAT_1` env var
- Point at `release` branch (not `master` — master is unstable)
- Root directory: `apps/backend`
- Env vars: `PAT_1` (required), `CACHE_SECONDS`, `WHITELIST`, `EXCLUDE_REPO`, `FETCH_MULTI_PAGE_STARS`
- Optional: SQL database (Postgres via Nile), custom OAuth app

## Panomete's Situation

- Original README had `github-readme-stats.vercel.app` cards — removed because the instance is paused
- User wants to talk to DevOps about self-hosting before re-adding
- When ready, either:
  - Use the public `github-stats-extended.vercel.app` instance (fresher, maintained)
  - Or self-host via GitHub Action (easier) or Vercel (more control)
- Recommended cards for his profile:
  - `https://github-stats-extended.vercel.app/api?username=oat431&show_icons=true&theme=tokyonight&hide_border=true&count_private=true`
  - `https://github-stats-extended.vercel.app/api/top-langs/?username=oat431&layout=compact&theme=tokyonight&hide_border=true`
