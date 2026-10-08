import { getCollection, type CollectionEntry } from "astro:content";
import { defaultLang, type Lang } from "../i18n/ui";
import { localizePath } from "../i18n/utils";

export type TutorialEntry = CollectionEntry<"tutorials">;

export interface TutorialItem {
  title: string;
  path: string;
  group: string;
  groupOrder: number;
  order: number;
}

export interface SidebarGroup {
  name: string;
  order: number;
  items: TutorialItem[];
}

/** Path within the tutorials section, without the locale prefix or extension. */
export function entryPath(entry: TutorialEntry): string {
  const parts = entry.id.split("/");
  if (parts[0] === entry.data.lang) parts.shift();
  const path = parts.filter((part) => part !== "index").join("/");
  return path;
}

export function tutorialHref(lang: Lang, path: string): string {
  const base = path === "" ? "ai/tutorials" : `ai/tutorials/${path}`;
  return localizePath(lang, base);
}

export async function getTutorials(lang: Lang): Promise<TutorialEntry[]> {
  return getCollection(
    "tutorials",
    (entry) => entry.data.lang === lang && !entry.data.draft,
  );
}

export async function getTutorialByPath(
  lang: Lang,
  path: string,
): Promise<TutorialEntry | undefined> {
  const entries = await getTutorials(lang);
  return entries.find((entry) => entryPath(entry) === path);
}

export async function getSidebar(lang: Lang): Promise<SidebarGroup[]> {
  const entries = await getTutorials(lang);
  const groups = new Map<string, SidebarGroup>();

  for (const entry of entries) {
    const path = entryPath(entry);
    if (path === "") continue;
    const { group, groupOrder, order, title } = entry.data;
    if (!groups.has(group)) {
      groups.set(group, { name: group, order: groupOrder, items: [] });
    }
    groups.get(group)!.items.push({ title, path, group, groupOrder, order });
  }

  const result = [...groups.values()].sort((a, b) => a.order - b.order);
  for (const group of result) group.items.sort((a, b) => a.order - b.order);
  return result;
}

export async function getAvailableLocales(path: string): Promise<Lang[]> {
  const entries = await getCollection("tutorials", (entry) => !entry.data.draft);
  const langs = new Set(entries.filter((e) => entryPath(e) === path).map((e) => e.data.lang));
  return (["en", "es"] as Lang[]).filter((lang) => langs.has(lang));
}

export const fallbackLang = defaultLang;
