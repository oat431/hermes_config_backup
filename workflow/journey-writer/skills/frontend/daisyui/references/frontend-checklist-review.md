# Frontend Checklist Review (Vite/SPA)

When building a React frontend with Vite (not Next.js), apply the React checklist with these adjustments:

## Skip (Next.js-specific)
- Server Components, `loading.tsx`, `error.tsx` per route
- `next/image`, `next/font`, `next/dynamic`
- `middleware.ts` for auth guards
- File-based routing from Next.js

## Apply (Vite/SPA)
- **Data Fetching:** TanStack Query for async data, staleTime tuning, optimistic updates
- **State:** URL params for pagination/filters (shareable, back-button works), Zustand for client state
- **Styling:** Tailwind + DaisyUI (already handled by daisyui skill)
- **Accessibility:** Semantic HTML, heading hierarchy, keyboard nav, color contrast
- **Security:** No `dangerouslySetInnerHTML`, no secrets in `VITE_*` env vars, HTTP-only cookies for auth
- **Testing:** Vitest + React Testing Library, MSW for API mocking
- **Deployment:** Custom 404 page, unique `<title>` per page, error boundary

## PR Grouping for Frontend

| PR | Theme | Items |
|----|-------|-------|
| #1 | MVP Polish | Error handling, 404 page, page titles |
| #2 | URL State | Pagination params, filter params, debounce |
| #3 | Data Fetching | TanStack Query, optimistic updates, prefetch |
| #4 | Tests | Vitest, RTL, MSW |
| #5 | Accessibility | Semantic HTML, keyboard nav, contrast |
