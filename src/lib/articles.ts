import { getCollection, type CollectionEntry } from "astro:content";
import { type Lang } from "../i18n/ui";
import { localizePath } from "../i18n/utils";

export type ArticleEntry = CollectionEntry<"articles">;

const KIND_SEGMENT: Record<ArticleEntry["data"]["kind"], string> = {
  article: "articles",
  route: "routes",
  story: "stories",
  devlog: "devlogs",
};

/** Slug within a vertical, without locale prefix, vertical folder or extension. */
export function entryPath(entry: ArticleEntry): string {
  const parts = entry.id.split("/");
  if (parts[0] === entry.data.lang) parts.shift();
  if (parts[0] === entry.data.vertical) parts.shift();
  return parts.filter((part) => part !== "index").join("/");
}

/** Locale-less canonical path for an article. */
export function articlePath(entry: ArticleEntry): string {
  const slug = entryPath(entry);
  if (entry.data.vertical === "ai") return `ai/articles/${slug}`;
  if (entry.data.vertical === "games") return `games/devlogs/${slug}`;
  return `rides/${KIND_SEGMENT[entry.data.kind]}/${slug}`;
}

export function articleHref(lang: Lang, entry: ArticleEntry): string {
  return localizePath(lang, articlePath(entry));
}

/** Locale-less listing path for a vertical + kind. */
export function listPath(
  vertical: "ai" | "rides" | "games",
  kind: ArticleEntry["data"]["kind"],
): string {
  if (vertical === "ai") return "ai/articles";
  if (vertical === "games") return "games/devlogs";
  return `rides/${KIND_SEGMENT[kind]}`;
}

export interface ArticleFilter {
  vertical?: "ai" | "rides" | "games";
  kind?: ArticleEntry["data"]["kind"];
}

export async function getArticles(lang: Lang, filter: ArticleFilter = {}): Promise<ArticleEntry[]> {
  const entries = await getCollection(
    "articles",
    (entry) =>
      entry.data.lang === lang &&
      !entry.data.draft &&
      (filter.vertical === undefined || entry.data.vertical === filter.vertical) &&
      (filter.kind === undefined || entry.data.kind === filter.kind),
  );
  return entries.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export async function getArticleByPath(
  lang: Lang,
  path: string,
): Promise<ArticleEntry | undefined> {
  const entries = await getCollection(
    "articles",
    (entry) => entry.data.lang === lang && !entry.data.draft,
  );
  return entries.find((entry) => articlePath(entry) === path);
}

export async function getAvailableLocales(path: string): Promise<Lang[]> {
  const entries = await getCollection("articles", (entry) => !entry.data.draft);
  const langs = new Set(entries.filter((e) => articlePath(e) === path).map((e) => e.data.lang));
  return (["en", "es"] as Lang[]).filter((lang) => langs.has(lang));
}
