#!/bin/bash
# Local development build script for versioned documentation
# Creates dev versions without versioning for quicker iteration

set -e

cd docs

echo "=== Building MLflow Documentation (Development) ==="
mkdocs build -f mkdocs-mlflow.yml

echo "=== Building YouTube Bot Series Documentation (Development) ==="
mkdocs build -f mkdocs-yt-bot.yml

echo "=== Build Complete ==="
echo "Documentation available at:"
echo "  MLflow: open build/mlflow/index.html"
echo "  Bot:    open build/bot/index.html"
