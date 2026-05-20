#!/bin/bash
# Language management script for YouWiki

LANGUAGE=${1:-en}
SITE_DIR="site_${LANGUAGE}"

case $LANGUAGE in
  en)
    echo "Building English version..."
    sed -i "s/docs_dir: docs\/es/docs_dir: docs\/en/" mkdocs.yml
    mkdocs build -d "$SITE_DIR"
    ;;
  es)
    echo "Building Spanish version..."
    sed -i "s/docs_dir: docs\/en/docs_dir: docs\/es/" mkdocs.yml
    mkdocs build -d "$SITE_DIR"
    ;;
  serve)
    LANG=${2:-en}
    echo "Serving $LANG version on http://localhost:8000"
    if [ "$LANG" = "en" ]; then
      sed -i "s/docs_dir: docs\/es/docs_dir: docs\/en/" mkdocs.yml
    else
      sed -i "s/docs_dir: docs\/en/docs_dir: docs\/es/" mkdocs.yml
    fi
    mkdocs serve
    ;;
  *)
    echo "Usage: $0 {en|es|serve [en|es]}"
    echo ""
    echo "Examples:"
    echo "  $0 en           # Build English version"
    echo "  $0 es           # Build Spanish version"
    echo "  $0 serve en     # Serve English version locally"
    echo "  $0 serve es     # Serve Spanish version locally"
    exit 1
    ;;
esac
