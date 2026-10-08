import { getRelativeLocaleUrl } from "astro:i18n";
import { defaultLang, ui, type Lang, type UIKey } from "./ui";

export function getLangFromUrl(url: URL): Lang {
  const [, maybeLang] = url.pathname.split("/");
  if (maybeLang && maybeLang in ui) return maybeLang as Lang;
  return defaultLang;
}

export function useTranslations(lang: Lang) {
  return function t(key: UIKey): string {
    return (ui[lang] as Record<string, string>)[key] ?? ui[defaultLang][key];
  };
}

export function stripLocale(pathname: string, lang: Lang): string {
  if (lang === defaultLang) return pathname;
  const stripped = pathname.replace(new RegExp(`^/${lang}(?=/|$)`), "");
  return stripped === "" ? "/" : stripped;
}

export function localizePath(locale: Lang, path: string): string {
  const clean = path.replace(/^\/+/, "");
  const url = getRelativeLocaleUrl(locale, clean);
  return url === "" ? "/" : url;
}
