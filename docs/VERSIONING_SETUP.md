# Topic-Level Documentation Versioning Setup

This documentation uses **Mike** for independent versioning of each topic within the wiki.

## Structure

- **MLflow For ML Dev**: Versioned at `/mlflow/` on your site
- **YouTube Bot Series**: Versioned at `/bot/` on your site

Each topic maintains its own version history independently.

## Files Overview

### Configuration Files
- `mkdocs-mlflow.yml` - MLflow documentation configuration
- `mkdocs-yt-bot.yml` - YouTube Bot Series documentation configuration
- `staticwebapp.json` - Azure Static Web Apps routing configuration

### Build Scripts
- `build-versioned-docs.sh` - Production build with mike versioning (runs on Azure deployment)
- `build-docs-dev.sh` - Local development build (quick iteration without versioning)

## Local Development

### Quick Build (Development)
```bash
cd docs
./build-docs-dev.sh
```
This builds both documentation sites without versioning, useful for testing changes.

### Open Documentation Locally
```bash
# MLflow docs
open build/mlflow/index.html

# YouTube Bot docs
open build/bot/index.html
```

## Production Deployment

The Azure Static Web Apps workflow automatically:

1. Installs Python dependencies (mkdocs, mike)
2. Runs `build-versioned-docs.sh` to build both topics
3. Deploys versioned docs to:
   - `https://yourdomain.com/mlflow/` (with version selector)
   - `https://yourdomain.com/bot/` (with version selector)

## Adding New Versions

When you want to release a new version:

```bash
cd docs
mike deploy -c -m mkdocs-mlflow.yml 1.1 latest
mike deploy -c -m mkdocs-yt-bot.yml 1.1 latest
```

Then push to your main branch to trigger Azure deployment.

## Modifying Documentation Structure

### Add a new page to MLflow:
1. Create markdown file in `docs/en/engineering_channel/mlflow_for_ml_dev/`
2. Add entry to `nav` section in `mkdocs-mlflow.yml`

### Add a new page to YouTube Bot:
1. Create markdown file in `docs/en/engineering_channel/yt_bot_series/`
2. Add entry to `nav` section in `mkdocs-yt-bot.yml`

## Directory Layout

```
docs/
├── mkdocs.yml                    # Main site config
├── mkdocs-mlflow.yml             # MLflow versioned docs config
├── mkdocs-yt-bot.yml             # YouTube Bot versioned docs config
├── build-versioned-docs.sh       # Production build script
├── build-docs-dev.sh             # Development build script
├── build/                         # Output directory (auto-generated)
│   ├── mlflow/                   # MLflow versioned output
│   └── bot/                      # YouTube Bot versioned output
└── docs/
    └── en/
        └── engineering_channel/
            ├── mlflow_for_ml_dev/
            └── yt_bot_series/
```

## Deployment Path Mapping

- `build/mlflow/*` → `src/mlflow/*` → `https://domain.com/mlflow/`
- `build/bot/*` → `src/bot/*` → `https://domain.com/bot/`

The `staticwebapp.json` routes all requests properly to each documentation site's index.html for client-side routing.

## Troubleshooting

### Docs not updating on Azure?
1. Check GitHub Actions logs
2. Ensure `build-versioned-docs.sh` has execute permissions: `chmod +x docs/build-versioned-docs.sh`
3. Verify mkdocs YAML syntax in config files

### Version selector not appearing?
- Ensure `mike` versions are deployed (check `docs/build/mlflow/versions.json` and `docs/build/bot/versions.json`)
- Version selector only shows if multiple versions exist

### 404 errors on versioned routes?
- Check `staticwebapp.json` routing rules
- Verify files are in correct directories (`src/mlflow/`, `src/bot/`)
