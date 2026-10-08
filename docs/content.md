# Adding content

Content is plain Markdown in **Astro content collections**. There is no CMS: create a file, rebuild, and the route, listing entry, sitemap entry, and RSS item are generated automatically.

## Where content lives

```
src/content/
  articles/
    en/ai/<slug>.md          # AI & Engineering articles
    en/rides/<slug>.md       # Road Trips (kind: route | story)
    es/ai/<slug>.md          # same, Spanish
    es/rides/<slug>.md
  tutorials/
    en/index.md              # tutorials landing page
    en/<group>/<slug>.md     # structured tutorials
    es/index.md
    es/<group>/<slug>.md
```

## Bilingual pairing

Keep the **same relative path** under `en/` and `es/` (e.g. `en/ai/foo.md` ↔ `es/ai/foo.md`). Pages that exist in both languages get `hreflang` + a working language switch; pages that exist in only one language hide the switch for the other.

## Article frontmatter

Defined in `src/content.config.ts`:

| Field | Required | Notes |
| --- | --- | --- |
| `title` | Yes | Page `<h1>` and card title |
| `description` | Yes | Meta description and listing blurb |
| `date` | Yes | `YYYY-MM-DD`; drives ordering and "Latest" |
| `lang` | Yes | `en` or `es` (must match the folder) |
| `vertical` | No | `ai` (default) or `rides` |
| `kind` | No | `article` (default), `route`, or `story` |
| `youtubeId` | No | YouTube ID → embedded video + `VideoObject` schema |
| `cover` | No | Image path (e.g. `/assets/img/foo.jpg`) shown as a header image |
| `draft` | No | `true` hides it from build/listings |

### URL mapping

| `vertical` | `kind` | File | URL |
| --- | --- | --- | --- |
| `ai` | `article` | `en/ai/foo.md` | `/ai/articles/foo/` |
| `rides` | `route` | `en/rides/foo.md` | `/rides/routes/foo/` |
| `rides` | `story` | `en/rides/foo.md` | `/rides/stories/foo/` |
| `games` | `devlog` | `en/games/foo.md` | `/games/devlogs/foo/` |

Spanish mirrors under `/es/...`.

## Add an AI article

Create `src/content/articles/en/ai/my-post.md` and `src/content/articles/es/ai/my-post.md`:

```markdown
---
title: "My new article"
description: "One or two sentences for search results and listings."
date: 2026-10-07
lang: "en"
vertical: "ai"
kind: "article"
# youtubeId: "dQw4w9WgXcQ"     # optional: embeds the video + VideoObject schema
# cover: "/assets/img/cover.jpg" # optional: header image (put file in public/assets/img/)
---

Body in Markdown. Put the video transcript or notes here as normal text so it is
indexable.
```

## Add a route guide

`src/content/articles/en/rides/my-route.md` (and the `es/` twin) with `vertical: "rides"`, `kind: "route"`. It appears at `/rides/routes/my-route/` and in the Routes listing.

## Add a story

Same as a route but `kind: "story"` → `/rides/stories/my-story/`.

## Add a tutorial

Create `src/content/tutorials/en/<group>/<slug>.md` (and `es/` twin):

```markdown
---
title: "Series 1: Getting started"
description: "What this tutorial covers."
lang: "en"
order: 1            # position within its group
group: "My Series"  # sidebar group heading
groupOrder: 1       # position of the group
---

Tutorial body in Markdown.
```

- URL: `/ai/tutorials/<group>/<slug>/` (Spanish `/es/ai/tutorials/...`).
- The sidebar is built automatically from every tutorial's `group`/`order`.
- The tutorials landing page is `src/content/tutorials/{en,es}/index.md` (edit it to change the intro).

## Videos, transcripts, covers

- **Video**: set `youtubeId` in the frontmatter. The article layout renders a click-to-load embed and adds `VideoObject` structured data automatically.
- **Transcript**: there is no separate field — add it as a section in the Markdown body so it is crawlable.
- **Cover**: set `cover` to a path under `public/` (e.g. `/assets/img/my-cover.jpg`) and drop the file in `public/assets/img/`.

## Add a project

Projects (not articles) live in **`src/data/projects.ts`** and render on `/ai/projects/` + `/es/ai/projects/`. Append an entry with `slug`, `href` (locale-less path), and `title`/`description` for `en` + `es`, then create the project's page under `src/pages/ai/projects/` (and the `es/` mirror).

## Add a devlog (game development)

Devlogs reuse the articles collection. Create `src/content/articles/en/games/<slug>.md` (and the `es/` twin) with `vertical: "games"` and `kind: "devlog"`:

```markdown
---
title: "Building Snake in Godot"
description: "One or two sentences for search results and listings."
date: 2026-10-07
lang: "en"
vertical: "games"
kind: "devlog"
---

Devlog body in Markdown.
```

- URL: `/games/devlogs/<slug>/` (Spanish `/es/games/devlogs/<slug>/`).
- They appear on the `/games/` hub (latest 5) and at `/games/devlogs/`.

## Add a playable game

1. Drop the web export in **`public/play/<slug>/`** (served at `/play/<slug>/`).
2. Append an entry to **`src/data/games.ts`** with `slug`, `playPath: "play/<slug>/"`, and `title`/`description` for `en` + `es`.
3. The game build is excluded from search via `robots.txt` (`Disallow: /play/`) and a `noindex` meta tag in its `index.html`.

## Drafts

Add `draft: true` to the frontmatter to keep a piece out of builds, listings, sitemap, and RSS until it is ready.

## What updates automatically

- **Listing pages** (`/ai/articles/`, `/rides/routes/`, `/rides/stories/`) — newest first.
- **Homepage "Latest"** — the 3 newest articles (any vertical).
- **RSS** — English articles, newest first (`/rss.xml`).
- **Sitemap** — every non-draft page (via `@astrojs/sitemap`).

## After adding content

```bash
npm run dev      # preview locally
npm run check    # type-check
npm run build    # build + Pagefind index
```

Commit and push to `main` to deploy.
