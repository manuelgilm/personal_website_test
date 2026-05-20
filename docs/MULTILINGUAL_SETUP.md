# YouWiki Multilingual Setup Guide

This documentation site now supports multiple languages: **English** and **Spanish**.

## 📁 Directory Structure

```
docs/
├── en/                    # English content
│   ├── index.md
│   └── engineering_channel/
│       └── index.md
├── es/                    # Spanish content
│   ├── index.md
│   └── engineering_channel/
│       └── index.md
└── mkdocs.yml            # Configuration file
```

## 🚀 Building & Serving

### Option 1: Using the Build Script (Recommended)

Make the script executable:
```bash
chmod +x build_language.sh
```

Then use it to build or serve:

```bash
# Serve English version locally
./build_language.sh serve en

# Serve Spanish version locally
./build_language.sh serve es

# Build English version
./build_language.sh en

# Build Spanish version
./build_language.sh es
```

### Option 2: Manual Build

Edit `mkdocs.yml` and change the `docs_dir` line:

**For English:**
```yaml
docs_dir: docs/en
```

**For Spanish:**
```yaml
docs_dir: docs/es
```

Then run:
```bash
mkdocs serve    # For local development
mkdocs build    # For production build
```

## 📝 Adding New Content

When you create new pages:

1. **Create the file in English** under `docs/en/`
2. **Duplicate and translate** to `docs/es/`
3. **Update both** `mkdocs.yml` nav entries if needed (they're shared)

Example:
```
docs/en/engineering_channel/my_new_page.md
docs/es/engineering_channel/my_new_page.md
```

## 🌐 Deployment Strategy

For your personal website integration, you can:

1. **Deploy both versions** to separate subpaths:
   - `yourdomain.com/docs/en/` (English)
   - `yourdomain.com/docs/es/` (Spanish)

2. **Add a language switcher** in your main website to link between versions

3. **Build both** before deployment using a script or CI/CD pipeline

## 🔄 Future Enhancements

Once you're comfortable with the setup, consider:
- Adding a language switcher plugin
- Automating builds for both languages in CI/CD
- Adding more languages to the structure

## ✅ Current Status

- ✅ English version: Ready
- ✅ Spanish version: Ready
- ✅ Navigation configured for both

**Start building content in your preferred language!**
