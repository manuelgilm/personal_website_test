# Mike Versioning Guide

Your documentation now supports independent versioning for each topic with a version selector menu.

## How It Works

### Directory Structure
Each topic maintains its own versioned site:

```
build/mlflow/
  ├── 1.0/              # Version 1.0 content
  ├── latest/           # Alias to current version
  └── versions.json     # Version metadata

build/bot/
  ├── 1.0/              # Version 1.0 content
  ├── latest/           # Alias to current version
  └── versions.json     # Version metadata
```

### On Your Website
- **MLflow**: `https://yourdomain.com/mlflow/` → shows version selector
- **Bot**: `https://yourdomain.com/bot/` → shows version selector

The Material theme displays a version selector dropdown at the top of each page, allowing users to switch between versions.

## Adding a New Version

### Option 1: Using the Build Script (Recommended)

Edit `docs/build-versioned-docs.sh` and change the VERSION:

```bash
VERSION="1.1"  # Change from "1.0" to "1.1"
```

Then run:
```bash
cd docs
./build-versioned-docs.sh
```

This creates:
- `build/mlflow/1.1/` - new version
- `build/mlflow/latest/` - updated to 1.1
- `build/bot/1.1/` - new version
- `build/bot/latest/` - updated to 1.1

### Option 2: Using Mike CLI

If you have mike installed locally:

```bash
# Add new version for MLflow
cd build/mlflow
mike deploy 1.1 latest

# Add new version for Bot
cd ../bot
mike deploy 1.1 latest
```

## Publishing New Versions

After creating a new version:

```bash
git add docs/build-versioned-docs.sh  # if you updated VERSION
git commit -m "Release version 1.1"
git push origin main
```

GitHub Actions will automatically rebuild and deploy to Azure.

## Local Development

Test locally without versioning:

```bash
cd docs
./build-docs-dev.sh

# Then open:
open build/mlflow/index.html
open build/bot/index.html
```

## Version Metadata

The `versions.json` file in each topic contains:

```json
{
  "current": "latest",
  "releases": {
    "1.0": "/1.0/",
    "latest": "/latest/"
  }
}
```

Users see this in the version selector dropdown.

## Editing Documentation

- **MLflow docs**: `docs/en/engineering_channel/mlflow_for_ml_dev/`
- **Bot docs**: `docs/en/engineering_channel/yt_bot_series/`

Changes to these files will automatically be included in the next build.

## Troubleshooting

### Version selector not showing?
1. Check that `versions.json` exists in `build/mlflow/` and `build/bot/`
2. Verify theme version is set in mkdocs*.yml:
   ```yaml
   theme:
     version: "1.0"
   ```

### Versioning failed locally?
Ensure you're in the `docs/` directory and have execute permissions:
```bash
cd docs
chmod +x build-versioned-docs.sh build-docs-dev.sh
./build-versioned-docs.sh
```

### Azure deployment failed?
Check GitHub Actions logs and ensure:
- Python 3.11 is installed (workflow sets this up)
- mkdocs-material is installed
- All markdown files exist (no broken links)

## Future Enhancements

- **Automatic version detection**: Add git tags to automatically create versions
- **Version cleanup**: Periodically remove old versions from deployment
- **Staging**: Create a separate branch for pre-release versions
- **Redirect**: Set up redirects from old URLs to new versions
