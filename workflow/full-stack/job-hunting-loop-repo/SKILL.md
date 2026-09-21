---
name: job-hunting-loop-repo
description: "Use when editing F:/projects/job-hunting-loop (Bun loop)."
---

# job-hunting-loop (F:\projects\job-hunting-loop)

Scheduled loop: fetch JDs → dedup → prefilter → LLM screen/tailor/honesty-check → LaTeX build → targets/ + human-review. Bun + TS, `yaml` is the only runtime dep (AGENTS.md constraint — keep it).

## Layout (post-refactor 2026-09-17, branch refactor/ports-and-tests)
- `engine/domain/` pure types+rules (prefilter, profile gate, config validator, stage-output validators) — zero I/O
- `engine/ports.ts` — ModelGateway/JobStore/ReviewQueue/ProfileStore/Toolchain/Source/Publisher/PromptReader
- `engine/app/` — `loop.ts` orchestrator with single `dispose()` transition funnel, `stages.ts`, `report.ts` (pure renderers)
- `engine/adapters/` — llm (instance Budget, 429/5xx retry-once backoff), state (JSONL + derived human-review.md), build (patchTex reports missing anchors), sources, profile
- `engine/run.ts` — composition root / CLI only
- `tests/fakes.ts` — stage-keyed FakeGateway + mem ports; runLoop takes injectable `now`/`log`

## Commands
`bun test` (65 tests, no network), `bun run typecheck` (bundle-check), `bun run gate`, `bun run master-pdf` (master resume → master-resume.pdf via the shared toolchain; build.sh delegates to engine/master-build.ts), `bun run seed-test` (needs real LLM key — nightly CI only).

## Hermes cron wiring (live since 2026-09-17)
- Job af36b9605452, `every 2h`, no_agent watchdog → `profiles/full-stack/scripts/job-hunting-loop-tick.py` (MUST be .py — Hermes runs .sh through WSL bash, absent on this box). Script runs the one-shot loop, reads runs.jsonl tail, prints digest only on error/escalated/tailored; silent on nothing_new. Requires full gateway (hermes gateway install) running.
- The script resolves bun via shutil.which + npm-shim fallback (`~/AppData/Roaming/npm/bun.cmd`) — Python subprocess PATH on Windows may not see it.

## Pitfalls
- State in `loop/state/` is live user data — never delete records; smoke-test artifacts must be filtered out of jobs.jsonl after runs.
- `skipped_budget` is NON-terminal in dedup (deferred postings reconsider next run); all other statuses suppress.
- CI seed-test job requires repo secrets LLM_API_KEY/LLM_BASE_URL; silently skips when absent.
- Honesty red line tests: check-fail must mean zero toolchain.build calls — don't 'optimize' that path.
