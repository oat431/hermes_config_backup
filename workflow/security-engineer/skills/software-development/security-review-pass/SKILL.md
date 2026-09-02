---
name: security-review-pass
description: "Security review of a codebase: evidence, fixes, sign-off."
version: 1.0.0
author: Hermes Agent (SecEng profile)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, review, audit, govulncheck, docker, jwt, findings]
    related_skills: [requesting-code-review, github-code-review, software-specification, dogfood]
---

# Security Review Pass

Full-codebase security review with evidence and sign-off — the Security persona in a
multi-persona handoff chain (PO → Dev → QA → Security), or a standalone security audit
of a repo.

**Core principle:** Frame from the handoff/spec first; verify every claim with real tool
output; fix only in-lane items; ship a findings register + residual-risk statement, not
just a list of complaints.

## When to Use

- User asks for a security review / audit of a whole repo (interview challenge, pre-release, handoff)
- You are the Security persona receiving a QA→Security handoff with action items (e.g. ACT-S1..Sn)
- "Review the whole project" / "do the security pass" on an implemented codebase

**This skill vs requesting-code-review:** `requesting-code-review` verifies YOUR diff
pre-commit. This skill reviews a complete codebase (any author) end-to-end with live
evidence and produces sign-off docs.

## Workflow

### 1. Context first (handoff chain)
- Find the spec package (`.agents/spec/` or similar) and read `000_spec_index.md` plus the
  latest handoff INTO you (e.g. `07_pm/075_MM_qa_to_security_handoff.md`).
- Handoffs carry an evidence pack: what's already verified (do NOT re-prove), what's open
  in YOUR lane (action-item IDs), and pre-chewed findings. Structure your pass to close
  those IDs explicitly.
- Read the API spec + architecture doc for the LOCKED contract. Contract-changing fixes
  (error codes, auth model, API shape) go back to PO as decisions — never into code.

### 2. Map and statically review
- File tree (excluding `.git`), `git log --oneline` / `git status` — spot the stack and recent changes.
- Read EVERY production file: config, auth (JWT/bcrypt), handlers, middleware, DB adapter,
  worker, Dockerfile, docker-compose, `.env.example`, `.gitignore`, `go.mod`.
- Targeted greps: hardcoded secrets, `os.Exec`/`eval`/`panic`, base64-looking long strings,
  string-built queries (injection).
- Secret hygiene: `git log --all -- <secretfile>` empty; `.env` may exist locally but must
  never be committed — check presence + byte SIZE only, NEVER print contents.

### 3. Tool gates
- `govulncheck ./...` (install once: `go install golang.org/x/vuln/cmd/govulncheck@latest`).
  Distinguish REACHABLE stdlib vulns (fixed by bumping the `go.mod` `go` directive — the
  toolchain auto-downloads with `GOTOOLCHAIN=auto`) from module vulns "not called by your
  code" (informational).
- `go vet ./...` and `go test -race ./...` — baseline must be green before any claim.

### 4. Live probes (when a stack is running)
- Login timing side-channel: `scripts/login-timing-probe.sh` — unknown-email vs
  wrong-password response times; ≈10×+ delta = email-enumeration oracle.
- Response-header inspection (security headers, cache), error-envelope checks (413/404
  code correctness), auth spot checks (no-token → 401, garbage token → 401).

### 5. Container verification
- Builder layers: `docker build --target builder -t chk . && docker run --rm --entrypoint sh chk -c 'ls -la /app'`
  — assert `.env`, `.git`, `.agents` absent. Missing `.dockerignore` = the classic
  "secret in builder image" finding (final stage can still be clean — check both).
- Runtime image: contains only the binary; non-root uid (`docker exec <c> id`);
  `-ldflags "-s -w"` in Dockerfile.

### 6. Fix in-lane, verify each fix
- Fix only non-contract hardening: supply chain/toolchain, secrets hygiene, login timing,
  build config, JWT strictness. Contract changes → PO decision (document, don't implement).
- Every fix gets a re-run proof: govulncheck re-run, live re-probe with before/after
  numbers, rebuilt-image inspection, full test suite + smoke.
- Add a regression test for each code fix (e.g. dummy-compare invocation count test,
  wrong-issuer rejection test).

### 7. Deliverables (match the repo's doc conventions)
- **Security test report** (the heavyweight): numbered file in a `06_security/`-style
  folder; frontmatter + wikilinks; scope & method; controls-verified table with evidence;
  findings register (ID/severity/status); re-runnable verification commands; residual-risk
  statement; action-item closure table.
- **Handoff doc** (`07_pm/076_MM_security_to_po_handoff.md`-style): sign-off status, what
  was fixed + evidence, residual risks accepted (with owners), decisions requested
  (none from Security unless contract), what is now unblocked downstream.
- Update the defect report entries you closed and the spec index.
- Commit with an evidence-backed message (fix IDs, before/after numbers).

## Pitfalls

- **git-bash (MSYS) curl**: prints `%{time_total}` fine but exits 23 after `-w` output —
  harmless; read the printed values, ignore the exit code. Test a single call before
  looping; `for` loops with `;` separators can silently swallow output in this shell.
- **`docker compose up -d` trips the terminal long-lived-process guard** — run it with
  background=true + notify_on_complete, then poll `docker compose ps` for health in a
  separate call. Do NOT retry the same foreground form expecting a different result.
- **govulncheck wording**: "affected by N vulnerabilities from the standard library" with a
  `go 1.x.y` pin means the toolchain is stale — bump the `go` directive, don't hunt
  per-vuln workarounds. Re-run after the bump: expect "0 vulnerabilities".
- **Timing probes need a registered user** for the wrong-password case (register a
  throwaway first); the unknown-email case needs no setup. Use N=5 and compare ranges,
  not single samples.
- **Dummy bcrypt compare** must use a REAL precomputed bcrypt hash — `CompareHashAndPassword`
  fails fast on malformed input, which would recreate the timing gap. Generate via a
  throwaway `go run` file INSIDE the module (outside it can't resolve deps), then delete it.
- **Markdown table patching**: don't double the leading pipe (`||` vs `|`) when inserting
  rows — verify the diff after every doc patch.
- **Never print `.env` contents** — presence + byte size is sufficient evidence.
- **Logging secret check**: middleware must log method/path/status/duration only; if a
  unit test asserts it (e.g. `TestLoggingMiddlewareNeverLogsSecrets`), cite it rather than
  re-proving.

## Support files

- `references/go-backend-security-checklist.md` — per-layer Go security checklist + exact commands (JWT hardening, Mongo query patterns, Docker verification, error hygiene).
- `scripts/login-timing-probe.sh` — re-runnable login timing oracle probe (bash).
