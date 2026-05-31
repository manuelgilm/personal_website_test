#!/bin/bash
# Build script for versioned documentation with mike
# Builds MLflow and YouTube Bot series docs with version support

set -e

VERSION="1.0"
LATEST_ALIAS="latest"

echo "=== Building MLflow For ML Dev Documentation ==="
mkdocs build -f mkdocs-mlflow.yml -d temp_mlflow

echo "=== Building YouTube Bot Series Documentation ==="
mkdocs build -f mkdocs-yt-bot.yml -d temp_bot

echo "=== Setting up versioning with mike ==="
python3 << 'PYTHON_SCRIPT'
import os
import json
import shutil
from pathlib import Path

def setup_versioned_site(temp_dir, final_dir, version, alias):
    """Setup a versioned site structure with mike-compatible layout"""
    
    # Clean and create final directory
    if os.path.exists(final_dir):
        shutil.rmtree(final_dir)
    os.makedirs(final_dir, exist_ok=True)
    
    # Create version directory
    version_dir = os.path.join(final_dir, version)
    shutil.copytree(temp_dir, version_dir)
    
    # Create alias (e.g., latest -> 1.0)
    alias_dir = os.path.join(final_dir, alias)
    if os.path.exists(alias_dir):
        shutil.rmtree(alias_dir)
    shutil.copytree(version_dir, alias_dir)
    
    # Create versions.json for version selector
    versions_data = {
        "current": alias,
        "releases": {
            version: f"/{version}/",
            alias: f"/{alias}/"
        }
    }
    
    with open(os.path.join(final_dir, "versions.json"), "w") as f:
        json.dump(versions_data, f, indent=2)
    
    print(f"✓ Versioned site setup: {final_dir}")
    print(f"  - Version: {version_dir}")
    print(f"  - Alias: {alias_dir}")
    print(f"  - Version selector: {final_dir}/versions.json")

# Setup MLflow versioning
setup_versioned_site("temp_mlflow", "build/mlflow", "1.0", "latest")

# Setup Bot versioning
setup_versioned_site("temp_bot", "build/bot", "1.0", "latest")

PYTHON_SCRIPT

# Cleanup temporary directories
rm -rf temp_mlflow temp_bot

echo "=== Build Complete ==="
echo "Output structure:"
echo "  build/mlflow/1.0/  -> version 1.0"
echo "  build/mlflow/latest/ -> alias to latest version"
echo "  build/mlflow/versions.json -> version metadata"
echo ""
echo "  build/bot/1.0/     -> version 1.0"
echo "  build/bot/latest/  -> alias to latest version"
echo "  build/bot/versions.json -> version metadata"
