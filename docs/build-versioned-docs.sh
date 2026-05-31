#!/bin/bash
# Build script for versioned documentation with mike
# Deploys MLflow and YouTube Bot series docs independently

set -e

cd docs

echo "=== Building MLflow For ML Dev Documentation ==="
mike deploy -f -c -m mkdocs-mlflow.yml 1.0 latest
mike set-default -c -m mkdocs-mlflow.yml latest

echo "=== Building YouTube Bot Series Documentation ==="
mike deploy -f -c -m mkdocs-yt-bot.yml 1.0 latest
mike set-default -c -m mkdocs-yt-bot.yml latest

echo "=== Build Complete ==="
echo "Output structure:"
echo "  build/mlflow/  -> deployed to /mlflow/ on Azure"
echo "  build/bot/     -> deployed to /bot/ on Azure"
