---
name: react-vite-spa
description: Use when building or testing React+Vite+TS SPAs.
version: 0.1.0
tags: [react, vite, vitest, rtl, msw, spa, frontend]
---

# React + Vite SPA: build, test, demo-mode, CI

Class-level skill for React 19 + Vite + TypeScript SPA work on this setup — adding a test suite, mocking a dead backend, wiring CI, or passing strict lint gates. Everything here was executed and verified green (lint 0 errors · 26/26 tests · build clean · CI green) on `react-ts-component-snippets`, 2026-08-19. Exact configs and the error→fix log live in `references/testing-and-demo-mode-setup.md`.

## When to use

- Adding Vitest + React Testing Library to an existing Vite React app
- Mocking a decommissioned/absent backend (MSW demo mode)
- Wiring GitHub Actions CI for a frontend repo
- Fighting `eslint-plugin-react-hooks` v7 (compiler-era) errors in teaching/demo code
- Building hooks/pages playgrounds or perf demos in a snippets/portfolio repo

## Stack conventions (follow the user's checklist, not habit)

The user maintains `F:\obsidian_note\swe-knowledge\checklist\web-checklist\react-js.md` — consult it before frontend work. Key positions it takes (verified in practice):

| Topic | Convention |
|---|---|
| Test runner | Vitest (Vite-native), not Jest |
| Queries | `getByRole`/`getByLabelText` first; `testid` is last resort |
| Interaction | `userEvent`, never `fireEvent` |
| Network mocking | MSW at the network boundary, not module mocks (`jest.mock`-style) |
| Virtualization | `@tanstack/react-virtual`, not react-window |
| External-store hooks | `useSyncExternalStore` (e.g. `useMediaQuery`), not effect+setState |
| Context vs store | Context for low-frequency global state (auth/theme); store for high-churn shared state (cart) |

## Testing setup recipe (order matters)

1. `npm i -D vitest jsdom @testing-library/react @testing-library/user-event @testing-library/jest-dom` + `msw`
2. `vitest.config.ts` — `environment: 'jsdom'`, `globals: true`, `setupFiles`, `css: false`, reuse the `@` alias
3. `src/test/setup.ts` — jest-dom, MSW `setupServer` with `beforeAll/afterEach/afterAll`, and a `matchMedia` polyfill (jsdom lacks it; any hook or page using media queries will crash tests without it)
4. `src/test/utils.tsx` — `renderWithProviders(ui, {route, store})`: Router + Redux + Auth stack in one wrapper. **Pages that render a layout/NavBar pull in store-consuming components**, so page-level tests need the full provider stack or they fail with "could not find react-redux context value"
5. `npm pkg set scripts.test="vitest run"`
6. Add `"vitest/globals"` to tsconfig `types` AND add `vitest.config.ts` to a tsconfig `include` (else: `Cannot find name 'beforeAll'` in setup, and a parser "file not found in project" lint error)

## MSW pattern: one mock layer, two uses

- `src/mocks/handlers.ts` — REST handlers mirroring the real API envelope (match the app's `types/` response shapes exactly)
- `src/mocks/browser.ts` — `setupWorker(...handlers)`; started in `main.tsx` behind an env flag (e.g. `RTCS_DEMO !== 'false'`) via dynamic import, THEN render the app (`enableDemoMode().finally(render)`)
- `src/mocks/server.ts` — `setupServer(...handlers)` for Vitest (setup.ts lifecycle)
- `npx msw init public/ --save` generates the worker script
- Demo credentials documented in the UI (e.g. a hint line on the login form)

This is also an interview/senior talking point: "the same handlers run the live demo and the test suite."

## eslint react-hooks v7 (compiler rules): fix or document

New rules (`set-state-in-effect`, `refs-in-render`/purity, `no-floating-promises` under `recommendedTypeChecked`) flag canonical patterns. Policy:

1. **Prefer a real fix** — e.g. rewrite `useMediaQuery` on `useSyncExternalStore`; type axios interceptors with `isAxiosError` narrowing instead of `any` access
2. **Where the pattern IS the point** (usePrevious reading a ref during render, render counters, session-restore-on-mount), use a scoped `// eslint-disable-next-line <rule> -- reason` with a written justification, plus a comment block in the file explaining why
3. Scoped per-file relaxations for tests (`no-floating-promises`, `require-await`) in `eslint.config.js` — not global disables
4. `globalIgnores` the generated `public/mockServiceWorker.js`

## Tooling pitfalls (durable, verified)

- **patch tool vs JSONC**: `patch` validates strict JSON and will refuse tsconfig writes (they contain `//` comments). Use `sed -i` for one-line tsconfig edits instead.
- **CI branch triggers**: check the actual default branch (`git branch -a`, `origin/HEAD`) before writing `on: push: branches:`. A workflow targeting `main` on a `dev`-default repo silently never runs.
- **Node version**: Vite 7 needs Node ≥ 20.19. The shell's default `node` may be ancient (v12) — resolve a modern one (this host: `/c/nvm4w/nodejs`, Node 24) via `export PATH` at the start of each terminal call; PATH does not persist across calls.
- **A11y label collisions in tests**: an icon toggle labeled "Show password" collides with `getByLabelText(/password/i)` — name auxiliary controls distinctly ("Show secret") so role/label queries stay unambiguous.

## Workflow with this user

- Propose the plan in the repo's README (marked PROPOSAL) → user reviews → then execute. User accepts scope pushback: fewer things done properly beat many thin ones (they explicitly chose 1 polished repo over 5 rushed ones).
- Timebox phases with a hard stop; record progress in `note/00_BUILD_MANUAL.md` inside the repo (goal → files → verification → interview/story value per phase).
- Final gate before push: `npm run lint` (0 errors) + `npm test` + `npm run build`, all three verified by actual exit status — then push and confirm CI green via `gh run list`.
- Conventional commits; commit+push only after the user has approved the plan.

## Support files

- `references/testing-and-demo-mode-setup.md` — exact file inventory, config contents, and the session error→fix log (provider-stack failures, aria-label collisions, JSONC patch refusals, unused-directive cleanup)
