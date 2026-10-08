# Customization

A map of "where do I change X?". The site is bilingual: English lives at the root, Spanish under `/es/`.

## Text and labels (EN + ES)

All UI strings are in **`src/i18n/ui.ts`** — one dictionary for `en`, one for `es`. Edit both to keep them in sync.

Key groups:

| Prefix | Used on |
| --- | --- |
| `nav.*` | Header menu labels |
| `lang.switch`, `theme.toggle` | Header controls (accessibility labels) |
| `home.*` | Homepage (title, description, hero greeting/roles/lead, "Latest") |
| `ai.*` | AI & Engineering hub and sections |
| `rides.*` | Road Trips hub and sections |
| `about.*` | About page |
| `contact.*` | Contact page, form, and thank-you page |
| `notfound.*` | 404 page |
| `footer.*`, `common.*` | Footer and shared strings |

Example — change the nav label for Road Trips:

```ts
// en
"nav.rides": "Road Trips",
// es
"nav.rides": "Viajes",
```

## Site constants

**`src/consts.ts`** (`SITE`): `name`, `jobTitle`, `email`, `location`, `ogImage`, and `sameAs` (the list of social profile URLs). The `Person` JSON-LD, the hero social icons, and the footer all derive from here.

## Home hero and the title animation

- **Markup**: `src/components/HomePage.astro` (the `.hero-photo` section).
- **Animated roles** (the typed text): `home.hero.roles` in `src/i18n/ui.ts`, a **pipe-separated** list. The first entry is the default/SEO text; the rest cycle.
  ```ts
  // en
  "home.hero.roles": "Manuel Gil|A Data Scientist|A Machine Learning Engineer|An Adventurer",
  // es
  "home.hero.roles": "Manuel Gil|Científico de Datos|Ingeniero de Machine Learning|Aventurero",
  ```
- **Greeting** ("I'm" / "Soy"): `home.hero.greeting`.
- **Speed**: the typing/deleting delays are the `setTimeout(...)` values at the bottom of `HomePage.astro` (type `70ms`, delete `40ms`, hold `1600ms`, between roles `350ms`, initial delay `1200ms`). Reduce-motion users get a static line.
- **Background image**: `src/assets/img/home-bg.webp` (rendered/optimized via `astro:assets`). Replace the file to change the photo.
- **Scrim/overlay**: `.hero-scrim` in `src/styles/global.css` controls the darkening over the photo.

## Navigation menu

- Items and paths: the `nav` array in **`src/components/Header.astro`** (`key` → label from `ui.ts`, `path` → locale-less route).
- The transparent-over-hero behaviour is also in `Header.astro` (scroll listener) + the `.site-header[data-over-hero]` rules in `global.css`.

## Social links

- **`src/consts.ts` → `sameAs`** is the single source of truth.
- Footer: `src/components/Footer.astro`.
- Hero icon row: `src/components/SocialIcons.astro` (maps each platform to an inline SVG; add/remove platforms in its `order`/`PATHS` maps).

## Branding: colors and fonts

**`src/styles/global.css`**, `:root` tokens:

- `--accent` — interactive color (links, buttons; tuned per theme for contrast)
- `--accent-brand` — decorative warm tan (`#b8a07e`)
- `--bg`, `--bg-elev`, `--fg`, `--muted`, `--border`, radii, and the type scale
- Light theme overrides live under `:root[data-theme="light"]`

Fonts are self-hosted via `@fontsource-variable/*`, imported at the top of **`src/layouts/BaseLayout.astro`** (`--font-sans`, `--font-serif` in `global.css`).

## SEO, redirects, headers

- **`src/components/Seo.astro`** — canonical, hreflang, Open Graph/Twitter, JSON-LD. Per-page `title`/`description` are passed by each page (text in `ui.ts`).
- **`public/staticwebapp.config.json`** — redirects (old URLs → new), security headers, and cache rules.
- **`public/robots.txt`**, **`public/site.webmanifest`**, favicon/OG images in **`public/assets/img/`**.

## Games

- **Hub**: `src/components/GamesHub.astro` (rendered by `src/pages/games/index.astro` + `src/pages/es/games/index.astro`) — intro, playable games, and the latest devlogs. Reached from the **Games** menu.
- **Playable games**: listed in **`src/data/games.ts`**; builds live in **`public/play/<slug>/`** (served at `/play/<slug>/`, excluded from search). The Snake build is embedded from `/play/snake/`.
- **Devlogs**: Markdown articles with `vertical: "games"`, `kind: "devlog"` → `/games/devlogs/<slug>/`. See [content](./content.md).

## AI & Engineering: Projects and MLflow

- **`src/data/projects.ts`** lists the projects shown on `/ai/projects/` (and `/es/ai/projects/`). Each entry has a `slug`, a locale-less `href`, and `title`/`description` for `en` + `es`. **To add a project:** append an entry here and create its page (e.g. `src/pages/ai/projects/<slug>.astro` + `src/pages/es/ai/projects/<slug>.astro`). Reached from the **AI & Engineering → Projects** menu.
- **MLflow server**: `src/components/MlflowProject.astro` (pages `ai/projects/mlflow.astro` + the `es/` mirror) holds the project copy and the **Get access** dialog, which posts to `/api/mlflow_server`. See [configuration](./configuration.md) for the required environment variables.
- **YouTube playlists**: `src/components/Playlists.astro`, injected into the AI hub via the `<slot />` in `PillarHub.astro` (only the AI page passes it).

## Contact form

- Fields/markup and submit logic: **`src/components/ContactForm.astro`**.
- Messages (labels, success/error): `contact.form.*` in `ui.ts`.
- Recipient and SMTP: environment variables (see [configuration](./configuration.md)).

## Pages and 404

Route files live in `src/pages/` (English) and `src/pages/es/` (Spanish): `index`, `about`, `contact/index`, `contact/thanks`, `ai/**`, `rides/**`, `404`. The 404 page is **`src/pages/404.astro`**.
