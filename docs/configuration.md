# Configuration

Everything that must be set for each feature to work, and where to set it.

The site is a **static frontend** (Astro) plus **Azure Functions** in `api/`, deployed together as an **Azure Static Web App**. The Functions run as SWA *managed functions*, so their settings live on the Static Web App resource.

## Where settings go

| Setting | Where | Used by |
| --- | --- | --- |
| Function environment variables | Azure Portal → Static Web App → **Settings → Environment variables** | `api/contact`, `api/mlflow_server` at runtime |
| `AZURE_STATIC_WEB_APPS_API_TOKEN_...` | GitHub repo → **Settings → Secrets and variables → Actions → Secrets** | Deployment (created automatically when you connect the repo) |
| `PUBLIC_GA4_ID`, `PUBLIC_PLAUSIBLE_DOMAIN` | GitHub repo → **Settings → Secrets and variables → Actions → Variables** | Build-time analytics (injected via `app_build_command`) |

Changes to environment variables require the Functions to pick them up (a redeploy or app restart).

## Feature: Contact form (`POST /api/contact`)

Powers `/contact/` and `/es/contact/`. Without these, submissions return *"Server configuration incomplete"*.

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `NAMECHEAP_EMAIL` | Yes | — | SMTP account/user |
| `NAMECHEAP_PASSWORD` | Yes | — | SMTP password (use an app password) |
| `ADMIN_EMAIL` | Yes | `NAMECHEAP_EMAIL` | Recipient of contact messages |
| `FROM_EMAIL` | No | `NAMECHEAP_EMAIL` | "From" address |
| `NAMECHEAP_SMTP_SERVER` | No | `smtp.namecheap.com` | SMTP host |
| `NAMECHEAP_SMTP_PORT` | No | `587` | SMTP port |
| `CONTACT_RATE_LIMIT_SECONDS` | No | `60` | Per-sender cooldown |
| `CONTACT_HONEYPOT_FIELD` | No | `website` | Hidden anti-spam field name |

## Feature: MLflow server (`POST /api/mlflow_server`)

Powers the "Get access" request on `/ai/projects/mlflow/`. It creates an MLflow user + workspace and emails credentials.

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `MLFLOW_SERVER_URL` | Yes | — | MLflow instance base URL |
| `MLFLOW_ADMIN_USER` | Yes | — | MLflow admin username |
| `MLFLOW_ADMIN_PASSWORD` | Yes | — | MLflow admin password |
| `NAMECHEAP_EMAIL` | Yes | — | SMTP account/user |
| `NAMECHEAP_PASSWORD` | Yes | — | SMTP password (use an app password) |
| `FROM_EMAIL` | No | `NAMECHEAP_EMAIL` | "From" address |
| `ADMIN_EMAIL` | No | — | Admin address used by the function |
| `NAMECHEAP_SMTP_SERVER` | No | `smtp.namecheap.com` | SMTP host |
| `NAMECHEAP_SMTP_PORT` | No | `587` | SMTP port |

> `NAMECHEAP_*` variables are shared by both functions.

## Namecheap SMTP

1. Namecheap → Account → Email → your mailbox → *Mail Client Configuration* for server/port/username.
2. Recommended: Account Settings → Security → generate an **App Password** and use it as `NAMECHEAP_PASSWORD`.

## Analytics (optional)

If both variables are empty, **no analytics script is emitted**. Set them as GitHub **Variables**:

- `PUBLIC_GA4_ID` — Google Analytics 4 measurement ID (e.g. `G-XXXXXXX`)
- `PUBLIC_PLAUSIBLE_DOMAIN` — Plausible domain (e.g. `gilmanuel.com`)

They are injected into the build by the workflow's `app_build_command`.

## IndexNow

The workflow submits `https://gilmanuel.com/sitemap-0.xml` to IndexNow after each production deploy. The key file lives at `public/<key>.txt` and the script at `scripts/indexnow.mjs` (run locally with `npm run indexnow`).

## Local development

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # astro build + Pagefind index
npm run preview    # serve the built dist/
npm run check      # astro check (types)
```

`npm run dev` / `npm run preview` do **not** serve `/api/*`. To test the Functions end to end, run [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local) and the SWA CLI:

```bash
# terminal 1 — the API (needs its env vars in api/local.settings.json or the shell)
cd api && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
func start                                   # http://localhost:7071

# terminal 2 — static frontend + API proxy on http://localhost:4280
npx @azure/static-web-apps-cli start http://localhost:4321 --api-location api
```
