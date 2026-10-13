import type { Lang } from "../i18n/ui";

/**
 * Format an article date for display.
 *
 * Dates are authored as plain `YYYY-MM-DD` in frontmatter and coerced by the
 * content schema to a `Date` at UTC midnight. Formatting them in UTC keeps the
 * rendered day aligned with the authored date regardless of the build machine's
 * timezone (otherwise a machine behind UTC shows the previous day).
 */
export function formatDate(lang: Lang, date: Date, style: "medium" | "long" = "medium"): string {
  return new Intl.DateTimeFormat(lang === "es" ? "es-CO" : "en-US", {
    dateStyle: style,
    timeZone: "UTC",
  }).format(date);
}
