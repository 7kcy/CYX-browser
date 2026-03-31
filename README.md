# CycloneX Browser v2

## Project Structure

```
CycloneX/
├── API/
│   ├── games.js      — GET /api/games?cat=&q=   (full catalogue)
│   ├── game.js       — GET /api/game/:id         (single game)
│   └── search.js     — GET /api/search?q=        (search shortcut)
│
├── public/
│   ├── index.html    — Main app (copy of public/html/index.html)
│   ├── games/
│   │   ├── games.json          — Machine-readable catalogue
│   │   ├── id1/index.html      — Subway Surfers (self-contained canvas)
│   │   ├── id2/index.html      — Slope          (self-contained canvas)
│   │   ├── id5/index.html      — Drift Hunters  (embed wrapper)
│   │   └── id{N}/index.html    — ... all 85 games
│   ├── icons/
│   │   └── *.svg               — Game icons (slug-named)
│   └── html/
│       └── index.html          — Source copy of main HTML
│
├── Vercel/
│   └── vercel.json             — Reference copy of deployment config
│
├── vercel.json                 — Active Vercel config (root)
└── package.json
```

## Why Games Weren't Loading

**Root cause:** Poki.com sets a `Content-Security-Policy: frame-ancestors` header that only
whitelists `*.poki.io` and specific localhost ports. Any other domain (including yours on Vercel)
gets blocked with:

```
Framing 'https://poki.com/' violates the following Content Security Policy directive:
"frame-ancestors https://*.poki.io http://localhost:1234 ..."
```

This is enforced by the **browser** — it cannot be bypassed by any server-side header you set.

## The Fix

All Poki iframe wrappers have been replaced with:
- **CrazyGames embed URLs** (`crazygames.com/embed/<slug>`) — these explicitly allow third-party embedding
- **Direct game sites** (`.io` games like slither.io, agar.io, bonk.io) that don't block framing
- **Self-contained canvas games** for Slope, Subway Runner, Krunker etc. — zero external dependencies

Each game lives in its own folder (`public/games/id{N}/index.html`) with a clean, minimal
wrapper iframe — no leftover game-bar chrome, no Poki URLs.

## Why Icons Weren't Showing

The icon lookup in `index.html` uses `/icons/<slug>.svg` (e.g. `/icons/drift-hunters.svg`).
Only 19 SVG icons exist in the repo. For games without a matching icon, the UI correctly
falls back to the emoji. No code change needed — icons now served from `public/icons/`.

## Deploying to Vercel

```bash
# From the CycloneX/ root:
vercel deploy
```

Or connect your GitHub repo and Vercel will auto-deploy on every push.
The `vercel.json` at the root sets `outputDirectory: "public"` so no build step is needed.
