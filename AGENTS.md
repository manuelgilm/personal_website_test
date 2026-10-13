# AGENTS.md

Manuel Gil's personal site (gilmanuel.com): a bilingual **Astro** static site plus **Azure Functions** (Python) in `api/`, deployed to **Azure Static Web Apps**. Content and branding matter here — when content is missing, leave a placeholder; do not invent personal details.

## Commands
- `npm install`
- `npm run dev` — Astro dev at http://localhost:4321
- `npm run build` — `astro build && pagefind --site dist` (also builds the search index)
- `npm run check` — `astro check` (types). `build` does NOT typecheck; run this before finishing.
- `npm run preview`, `npm run indexnow` (submits the live sitemap; needs a deploy)
- API syntax check: `python3 -m py_compile api/contact/__init__.py api/mlflow_server/__init__.py api/openai/__init__.py`
- No tests, lint, or formatter are configured. Keep the build and `check` clean.

## Hard requirements / local-dev gotchas
- **Node >= 22.12.0** (Astro 7). `.nvmrc` = `22`; CI sets `NODE_VERSION: "22"`. Do not lower it.
- `astro dev`/`preview` do **not** serve `/api/*`. The contact form, the MLflow form and the article `IdeaFeedback` widget only work with Azure Functions + the SWA CLI (see `docs/configuration.md`).
- **Pagefind search exists only after `npm run build`** (post-build index), not in dev.
- The Python API uses `X | None` annotations (Python >= 3.10). SWA managed Python is confirmed working.

## Architecture
- English at root, Spanish at `/es/` (`i18n.prefixDefaultLocale: false`). All UI text lives in `src/i18n/ui.ts` — add keys to **both** `en` and `es`. Components read `Astro.currentLocale` and build links with `localizePath(lang, path)` (`src/i18n/utils.ts`); never hardcode `/es/`.
- Content collections (`src/content.config.ts`):
  - `articles` → `src/content/articles/{en,es}/{ai|rides|games}/<slug>.{md,mdx}`; `vertical` = ai|rides|games, `kind` = article|route|story|devlog; optional `youtubeId`, `cover`, `draft`.
  - `tutorials` → `src/content/tutorials/{en,es}/**`.
  - Bilingual pairs share the same relative path. URL derivation is in `src/lib/articles.ts`.
  - Articles can be `.mdx` (via `@astrojs/mdx`) to embed components such as `src/components/IdeaFeedback.astro` (personas in `src/data/personas.ts`) — see `docs/content.md`.
  - Only the bilingual `ai/idea-breaker` pair exists so far; other listings still render "Content coming soon". Don't assume more posts exist.
- Data/config: `src/consts.ts` (SITE), `src/data/projects.ts`, `src/data/games.ts`, `src/data/cv.ts`, `src/data/personas.ts` (IdeaFeedback reviewers/synthesizer).
- `api/` = Azure Functions, v1 model (`function.json` + `__init__.py`): `contact`, `mlflow_server`, `openai` (proxies the MLflow gateway's OpenAI-compatible API). Required env vars per feature are in `docs/configuration.md`.
- `public/`: `staticwebapp.config.json`, `robots.txt`, `site.webmanifest`, `assets/img/*` (favicon/OG/me), `play/<slug>/` (Godot game builds), `cv/*.pdf` (CV download).
- Deploy: one workflow, `.github/workflows/azure-static-web-apps-*.yml`; Oryx runs `npm run build` → `dist`, with `app_location: "."`, `api_location: "./api"`, `output_location: "dist"`.

## Deployment gotcha (this already broke a deploy)
Azure SWA **rejects duplicate routes** in `public/staticwebapp.config.json` and treats `/foo` and `/foo/` as the same route. Never define both forms; use a trailing `*` wildcard (e.g. `/ai/projects/ai-room*`), which matches `/foo`, `/foo/`, and `/foo/index.html`. Routes are first-match-wins, so put specific rules before catch-alls. SWA validates this file at deploy and fails the build on errors.

## Code gotchas
- Arrays in `src/consts.ts` (`SITE.sameAs`, etc.) are `as const`, i.e. readonly literal unions. `.find()`/`.filter()` with a type predicate needs an explicit `string | undefined` (see `src/components/SocialIcons.astro` and `src/components/CvPage.astro`). This has caused type errors twice.
- `@astrojs/sitemap` excludes `/contact/thanks/` and `/es/contact/gracias/` via a `filter`. If you add other `noindex` pages, add them there so they don't leak into `sitemap-0.xml`.
- The CV "Download PDF" button only renders when `public/cv/manuel-gil-cv-{en,es}.pdf` exists (build-time `fs.existsSync`).
- Playable game builds (`public/play/<slug>/`) are intentionally `noindex` and robots-disallowed; the `/games/` hub is the indexable page.

## Conventions
- **Do not fabricate personal content** (experience, routes, bios); use placeholders and leave the writing to the owner.
- After changing config, UI text, SEO, or redirects, update the matching doc in `docs/` (`configuration.md`, `customization.md`, `content.md`).
- SEO is centralized in `src/components/Seo.astro` (canonical, hreflang, OG/Twitter, JSON-LD). When adding a page, pass `title`/`description` and confirm canonical + `hreflang`.
- Adding a top-level section = UI keys in `ui.ts` (en+es) + a nav entry in `src/components/Header.astro` + pages under `src/pages/<x>/` and `src/pages/es/<x>/`.
