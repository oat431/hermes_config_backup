# Testing & Demo-Mode Setup — verified configs and error→fix log

Session: 2026-08-19, repo `oat431/react-ts-component-snippets` (React 19, Vite 7, TS 5.9 strict, Tailwind 4 + daisyUI 5, react-router 7). Final state: lint 0 errors · 26/26 tests · build clean · GitHub Actions green (43s).

## File inventory added

```
vitest.config.ts                 # jsdom + globals + setupFiles, '@' alias reused
src/test/setup.ts                # jest-dom + MSW server lifecycle + matchMedia polyfill
src/test/utils.tsx               # renderWithProviders (Router + Redux + Auth)
src/mocks/handlers.ts            # REST handlers mirroring types/Auth.ts envelope
src/mocks/browser.ts             # setupWorker — demo mode
src/mocks/server.ts              # setupServer — Vitest
.github/workflows/ci.yml         # npm ci → lint → build → test, Node 24, on main+dev
src/hooks/*.ts                   # 8 custom hooks, 2 with colocated tests
src/pages/*.test.tsx             # LoginPage, AuthContext tests
src/store/cartSlice.test.ts      # pure reducer tests
```

## Configs that mattered

**vitest.config.ts** — `environment: 'jsdom'`, `globals: true`, `setupFiles: ['./src/test/setup.ts']`, `include: ['src/**/*.test.{ts,tsx}']`, `css: false`, and `resolve.alias` matching vite's (`@` → src). Without the alias, `@/` imports pass in the app but fail in tests.

**tsconfig deltas** (use `sed -i`; `patch` refuses JSONC):
- tsconfig.app.json: `"types": ["vite/client", "vitest/globals"]`, `"include": ["src", "vitest.config.ts"]`
- tsconfig.node.json: `"include": ["vite.config.ts", "vitest.config.ts"]`

**main.tsx demo boot** — dynamic-import the worker behind the env flag, render in `.finally()`:
```tsx
async function enableDemoMode() {
    if (import.meta.env.RTCS_DEMO !== 'false') {
        const { worker } = await import('./mocks/browser')
        await worker.start({ onUnhandledRequest: 'bypass' })
    }
}
enableDemoMode().finally(() => createRoot(...).render(...))
```

**MSW handler contract** — mirror the API envelope from `types/Auth.ts` exactly (`{data, status: "SUCCESS"|"FAIL"|"ERROR", error}`), return real HTTP status codes (401 with the envelope body for bad creds), gate `/auth/detail` on the exact `Bearer` token so the 401→auto-logout path is testable end-to-end.

**setup.ts matchMedia polyfill** — jsdom has no `matchMedia`; pages using `useMediaQuery` crash without it. Stub `matches/media/addEventListener/removeEventListener/dispatchEvent`.

## Error → fix log (each one cost a cycle; don't repeat)

| Symptom | Root cause | Fix |
|---|---|---|
| Page tests fail: "could not find react-redux context value; please ensure the component is wrapped in a `<Provider>`" (trace: NavBar → CartBadge → useSelector) | LoginPage renders MainLayout → NavBar → CartBadge which subscribes to the Redux store; test wrapped only Router+Auth | `renderWithProviders` util wrapping Router + Redux + Auth; pass `{route}` for MemoryRouter initial entry |
| `TestingLibraryElementError: Found multiple elements with the text of: /password/i` | password show/hide toggle's `aria-label="Show password"` matched the same regex as the field label | rename auxiliary control ("Show secret"/"Hide secret"); keep aria-pressed |
| `error TS6133: 'useState' is declared but never read` / duplicate `useRef` identifier | leftover imports in hand-written hooks/pages | strict `noUnusedLocals` catches these at build; fix imports |
| `error TS2304: Cannot find name 'beforeAll'` in setup.ts | vitest globals not in tsconfig types | add `"vitest/globals"` to tsconfig.app types |
| eslint parsing error on `vitest.config.ts`: "file was not found in any of the provided project(s)" | typed-lint project service didn't include it | add to tsconfig includes (both app and node) |
| `react-hooks/set-state-in-effect` errors in AuthContext/useMediaQuery/VerifyEmailPage/HooksPage | compiler-era rule flags sync setState in effects | real fix where possible (useMediaQuery → useSyncExternalStore); documented `eslint-disable-next-line -- reason` where the pattern is intentional (session restore on mount, demo counters) |
| `react-hooks/refs` + purity errors in usePrevious/RenderCount/HeavyPanel | reading refs during render / busy-wait in render IS the demo | scoped disables with written justification comments |
| `no-misused-promises` on `setTimeout(() => navigate(...))` | navigate returns a promise passed to a void-returning callback | `setTimeout(() => { void navigate("/login"); }, 3000)` |
| "Unused eslint-disable directive" warnings after fixes | earlier disables became redundant | `npx eslint . --fix` removes them; keep directives minimal |
| `patch` tool refuses tsconfig edits: "candidate content fails .json syntax validation" | tsconfig files are JSONC (comments); validator is strict JSON | use `sed -i` for one-line edits |
| `git push origin main` → "src refspec main does not match any" | repo default branch is `dev` | check `git branch -a` first; push `dev`; ALSO write CI `branches: [main, dev]` — a main-only trigger on a dev-default repo silently never runs |
| `node` in shell is v12 (Hermes-bundled); Vite 7 needs ≥20.19 | PATH resolves to bundled node | `export PATH="/c/nvm4w/nodejs:$PATH"` (Node 24) at the start of every terminal call — PATH does not persist between calls |

## Test suite shape that worked (26 tests / 5 files)

1. `useDebounce.test.ts` — fake timers; four cases: immediate initial value, NOT updated before delay, updated after delay, timer resets on rapid changes (burst → one settled value). This last one is the money test — it proves the cleanup/return-clearTimeout behavior.
2. `useLocalStorage.test.ts` — initial fallback, write-through persistence, fresh-mount read-back, functional updates.
3. `cartSlice.test.ts` — pure reducers: add/increment/decrement-at-zero-removes/remove/clear + selectors (count, total). Use `?.` not `!` (typeChecked lint flags unnecessary assertions).
4. `LoginPage.test.tsx` — behavior-first: accessible form (labels associated), empty-submit blocked with field errors, short-password error, `aria-invalid` present, wrong-creds alert (through MSW + real axios client), success stores tokens in localStorage, password toggle.
5. `AuthContext.test.tsx` — probe component pattern for context values; session restore from storage; logout clears both; **401 event → auto-logout** (the interceptor↔context contract); useAuth-outside-provider throws.

## eslint.config.js scoping that ended at 0 errors

- `globalIgnores(["dist", "public/mockServiceWorker.js"])`
- tests + vitest.config + `src/test/**`: node+browser globals, `project: ["./tsconfig.app.json"]`, disable `no-floating-promises`, `require-await`, `unbound-method`
- teaching-snippet files (usePrevious, RenderCount): `react-hooks/refs: off`
- AuthContext.tsx: `react-refresh/only-export-components: off` (component + hook colocated by design)
- main.tsx: `no-floating-promises: off` (top-level MSW boot)
- pages + NavBar: `no-floating-promises: off` (event handlers with internal error handling)
