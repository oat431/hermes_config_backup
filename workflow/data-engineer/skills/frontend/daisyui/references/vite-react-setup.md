# Vite + React + DaisyUI 5 + Tailwind CSS 4 Setup

## Install

```bash
bun add react react-dom react-router-dom
bun add -D daisyui @vitejs/plugin-react typescript vite tailwindcss postcss autoprefixer @types/react @types/react-dom
```

## CSS (src/index.css)

```css
@import "tailwindcss";
@plugin "daisyui";
```

No `tailwind.config.js` needed — Tailwind v4 uses CSS-based config.

## PostCSS (postcss.config.js)

Not needed if using Vite — Vite handles PostCSS internally.

## Vite Config

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3300,
    proxy: {
      '/api': 'http://localhost:8005',
    },
  },
})
```

## TypeScript

Need `src/vite-env.d.ts`:
```ts
/// <reference types="vite/client" />
```

Without this, CSS imports fail with `Cannot find module './index.css'`.

## Build

```bash
bun run build  # tsc -b && vite build
```
