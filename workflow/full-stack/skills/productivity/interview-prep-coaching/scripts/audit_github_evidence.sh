#!/usr/bin/env bash
# Audit a GitHub user's repos as interview-prep evidence.
# Usage: bash scripts/audit_github_evidence.sh <github-user> [topic-filter]
# Requires: gh CLI, authenticated (gh auth status).
#
# NOTE: use authenticated `gh api` — unauthenticated curl against api.github.com
# rate-limits within minutes and returns empty bodies, which breaks JSON parsing.

set -euo pipefail

USER="${1:?usage: audit_github_evidence.sh <github-user> [topic-filter]}"
FILTER="${2:-react|redux|rtk|vitest|frontend|next}"

echo "=== All repos, most recently updated (top 25) ==="
gh api "users/$USER/repos" --paginate \
  -q '.[] | "\(.updated_at[:10])  \(.name)  lang=\(.language)  desc=\(.description)"' \
  | sort -r | head -25

echo
echo "=== Repos matching topic filter: $FILTER ==="
gh api "users/$USER/repos" --paginate \
  -q '.[] | "\(.updated_at[:10])  \(.name)  lang=\(.language)  desc=\(.description)"' \
  | grep -iE "$FILTER" || echo "(none — promised repos likely do not exist yet)"

# Per-repo deep inspection — run for each promising candidate:
#
#   # top-level contents (README? package.json? tests dir?)
#   gh api "repos/$USER/<repo>/contents" -q '.[].name'
#
#   # package.json — check scripts + dead dependencies
#   gh api "repos/$USER/<repo>/contents/package.json" -q '.content' | base64 -d
#
#   # README — compare promises vs reality
#   gh api "repos/$USER/<repo>/contents/README.md" -q '.content' | base64 -d
#
#   # full src tree — verify README features actually exist in code
#   gh api "repos/$USER/<repo>/git/trees/HEAD?recursive=1" -q '.tree[].path'

# Audit checklist per candidate repo:
#   [ ] README promises match the actual source tree (mismatch = credibility hit)
#   [ ] No dead dependencies (e.g., react-redux listed but never imported)
#   [ ] Tests exist — a testing claim with zero tests collapses under probing
#   [ ] CI workflow exists (.github/workflows) if the candidate preaches CI gates
#   [ ] Repo is genuinely recent and the candidate can walk through it live
