# gilmanuel.com

Personal site of Manuel Gil — AI Platform Developer and MLOps Engineer, and motorbike traveller. Bilingual (English at `/`, Spanish at `/es/`), built with [Astro](https://astro.build) and deployed on **Azure Static Web Apps**.

## Stack

- **Astro** — static output to `dist/`
- **Content collections** — articles and tutorials in Markdown, bilingual by folder
- **Pagefind** — site search (indexed after `astro build`)
- **Azure Functions** (`api/`) — contact form and MLflow access provisioning
- **Self-hosted fonts** — Inter + Newsreader

## Quick start

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # astro build + Pagefind index
npm run preview    # serve the built dist/
npm run check      # astro check (types)
```

## Repository map

```
src/
  pages/           routes (English at root, Spanish under pages/es/)
  components/      Header, Footer, HomePage hero, ContactForm, MlflowProject, GamesHub, Seo, ...
  layouts/         BaseLayout, ArticleLayout, DocsLayout
  content/         articles + tutorials (Markdown)
  i18n/ui.ts       all UI text (en + es)
  consts.ts        site name, email, location, social links
  content.config.ts  content schemas
  styles/global.css  design tokens + component styles
api/               Azure Functions (contact, mlflow_server)
public/            static assets, robots.txt, staticwebapp.config.json, games
scripts/           indexnow.mjs
.github/workflows/ build & deploy
```

## Documentation

- **[docs/configuration.md](docs/configuration.md)** — environment variables per feature, where to set them in Azure, analytics, and local API testing.
- **[docs/customization.md](docs/customization.md)** — where to change text (EN/ES), the hero/title animation, nav, social links, colors, SEO, and more.
- **[docs/content.md](docs/content.md)** — how to add articles, route guides, stories, and tutorials.

## Deploy

Push to `main` → GitHub Actions builds the Astro site and deploys it together with `api/` to Azure Static Web Apps (`.github/workflows/azure-static-web-apps-*.yml`). After a production deploy the workflow submits the sitemap to IndexNow. See [configuration](docs/configuration.md) for the required settings.
