import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const articles = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/articles" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    lang: z.enum(["en", "es"]),
    vertical: z.enum(["ai", "rides", "games"]).default("ai"),
    kind: z.enum(["article", "route", "story", "devlog"]).default("article"),
    youtubeId: z.string().optional(),
    cover: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const tutorials = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/tutorials" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    lang: z.enum(["en", "es"]),
    order: z.number().default(0),
    group: z.string().default(""),
    groupOrder: z.number().default(0),
    draft: z.boolean().default(false),
  }),
});

export const collections = { articles, tutorials };
