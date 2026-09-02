# TanStack Query (React Query) Setup

## Install

```bash
bun add @tanstack/react-query
```

## Provider (main.tsx)

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,  // 30s before refetch
      retry: 1,
    },
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
)
```

## Query Hooks Pattern

```ts
// hooks/useTodolists.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import * as api from '../api/client'

export function useTodolists(page: number) {
  return useQuery({
    queryKey: ['todolists', page],
    queryFn: () => api.listTodolists(page),
    staleTime: 30_000,
  })
}

export function useCreateTodolist() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body) => api.createTodolist(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['todolists'] }),
  })
}
```

## Key Rules

- `queryKey` must include all variables that affect the query (page, filters, id)
- Mutations should `invalidateQueries` on related query keys
- Use `enabled: !!id` to skip queries when id is null/undefined
- Pages use `useSearchParams` from react-router-dom for URL state (not useState)
