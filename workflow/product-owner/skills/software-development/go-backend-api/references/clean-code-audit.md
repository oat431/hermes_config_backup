# Clean-code audit — the user's checklist (distilled)

Source: `F:\obsidian_note\swe-knowledge\computing-foundation-note\Clean Code Simplify\` — three notes: `01 Naming & Functions.md`, `02 Code Smells & Refactoring.md`, `03 Comments & Documentation.md` (overview in `Clean Code Overview.md`). When the user asks "is the code clean?" or "check against my notes", READ the notes first, then audit.

## Core rules

- **Names**: intention-revealing, pronounceable, searchable; no Hungarian, no `data`/`temp`/`flag`; classes=nouns, methods=verbs.
- **Functions**: under 20 lines (ideal 3–10); do ONE thing; one level of abstraction; **0–3 params** (4+ → parameter object); no boolean params.
- **Smells**: long method, large class, duplicated code (rule of three), dead code, speculative generality (YAGNI), long parameter list, magic numbers → named constants.
- **Comments**: explain WHY not WHAT; no commented-out code, no journal comments, no restatements; exported symbols get one-line docs; rationale (security, race, design decisions) is the good kind.
- **Refactor hygiene**: tests green before/after every step; refactor commit separate from features; message `refactor: ...`.

## Go-specific smells this checklist surfaces (all hit in a real audit)

1. **Dead claims plumbing** — auth middleware stores claims in context but nothing reads them → remove (speculative generality). Grep for the accessor before keeping.
2. **Rule-of-three duplication** — email normalization `strings.ToLower(strings.TrimSpace(...))` in 3 places → `domain.NormalizeEmail`. Grep for repeated expression fragments.
3. **4-param methods** — `Update(ctx, id, name, email)` → `UpdateUserInput{Name, Email *string}`; `Issue(ctx, sub, email, ttl)` → move TTL into the JWT manager (signing policy owns its own config), `Issue(ctx, claims)`.
4. **Long composition root** — 150-line `main()` → `connectMongo`, `ensureIndexes`, `serveHTTP`, `serveGRPC`, `shutdown` helpers; main becomes a ~50-line orchestrator. Timeouts/layouts become named consts.
5. **Adapter read-back duplication** — `FindOne+Decode` in `FindByID` and `Update` → one `getByObjectID(ctx, oid)` helper.

## Audit procedure (fast greps)

```bash
# longest functions (production)
for f in $(find cmd internal -name '*.go' ! -name '*_test.go'); do awk -v file="$f" '/^func /{if(name) print file": "n" lines"; name=$0; n=0; next} {n++} END{if(name) print file": "n" lines"}' "$f"; done | awk -F'lines' '{gsub(/[^0-9]/,"",$2); if ($2+0>15) print}' | sort -rn

# 4+ param functions
grep -rn "^func .*(" cmd internal --include='*.go' | grep -v _test | awk -F'(' '{n=split($2,a,","); if (n>=4) print $0}'

# duplicated fragments (candidates)
grep -rn "strings.ToLower(strings.TrimSpace" internal/ | grep -v _test
```

## Acceptable exceptions (do not force-churn)

- Composition root `main()` and sequential shutdown functions: one abstraction level, orchestration only.
- Adapter methods 20–30 lines of linear error translation (driver error → domain sentinel): one thing, verbose but not split-worthy.
- Error-mapping `switch` on error types at the transport boundary: idiomatic Go, not smell #10 (switch-on-type) — it IS the translation layer.
- Constructors with 3 deps after the TTL move; DI constructors are conventionally exempt beyond that.
