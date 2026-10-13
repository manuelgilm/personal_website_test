# Adding content

Content is plain Markdown in **Astro content collections**. There is no CMS: create a file, rebuild, and the route, listing entry, sitemap entry, and RSS item are generated automatically. Articles can also be **`.mdx`** when you want to embed interactive components (see [Interactive components](#interactive-components-mdx)).

## Where content lives

```
src/content/
  articles/
    en/ai/<slug>.md          # AI & Engineering articles
    en/ai/<slug>.mdx         # …or .mdx to embed components (see below)
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

## Interactive components (MDX)

Articles are Markdown by default, but the content loader also accepts **`.mdx`**. Rename the file to `.mdx` and you can import and embed Astro components in the body. Keep the `en/` and `es/` twins at the same relative path so they stay paired.

```mdx
---
title: "My interactive article"
description: "One or two sentences for search results and listings."
date: 2026-10-07
lang: "en"
vertical: "ai"
kind: "article"
---

import IdeaFeedback from "../../../../components/IdeaFeedback.astro";

Some prose…

<IdeaFeedback persona="optimist" label="Try it" />
```

The import is four levels up from `src/content/articles/<lang>/<vertical>/`.

### `IdeaFeedback` widget

Lets the reader submit an idea and get a model review through `POST /api/openai` (see [configuration](./configuration.md)). Props:

| Prop | Type | Notes |
| --- | --- | --- |
| `persona` | string | One persona id (see below). |
| `personas` | string[] | Query several personas. |
| `all` | boolean | Query every persona (reviewers capped at 4). |
| `plain` | boolean | Send the idea with **no** system prompt, for a plain baseline answer. |
| `sync` | boolean | Share the typed idea across every widget on the page (default `true`). |
| `label` | string | Optional heading shown above the form. |
| `model` | string | Optional gateway endpoint name; defaults to the server's `MLFLOW_GATEWAY_DEFAULT_MODEL`. |

Personas (in **`src/data/personas.ts`**) come in two roles:

- **Reviewers** — `optimist`, `skeptic`, `pragmatist`. Each gets the idea and replies independently, in parallel.
- **Synthesizer** — `synthesizer`. It runs **after** the reviewers: it receives the idea plus their replies and returns an overall view with a 1–10 score. A synthesizer on its own automatically pulls in the reviewers as inputs.

So `<IdeaFeedback all />` runs the three reviewers, then the synthesizer (up to 4 calls: three in parallel, one after).

- Persona names and system prompts live in **`src/data/personas.ts`** — edit them there.
- The widget is bilingual automatically (it follows the page locale). Only an authored `label` string needs translating by hand in each language's `.mdx`.
- Drop it multiple times in one article: each instance works independently, but by default they **share one idea** (kept in `sessionStorage`), so the reader types it once and every section reuses it. Set `sync={false}` to opt out.
- Use `plain` for a no-persona baseline (e.g. in the intro) to show how the answer changes once a system prompt is added.
- Guardrail blocks come back from the API as `{ success: false, code: "guardrail" }`; the widget shows the localized `idea.blocked` message instead of a generic error.
- It needs JavaScript and a working `/api/openai` (use the SWA CLI locally — see [configuration](./configuration.md)). Write the article so it still reads well without the widget.

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
