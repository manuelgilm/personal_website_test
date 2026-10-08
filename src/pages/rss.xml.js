import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import { SITE } from "../consts";
import { articlePath } from "../lib/articles";

export async function GET(context) {
  const entries = await getCollection(
    "articles",
    ({ data }) => data.lang === "en" && !data.draft,
  );
  const posts = entries.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  return rss({
    title: SITE.name,
    description: "Technical articles and road trips by Manuel Gil.",
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.date,
      link: `/${articlePath(post)}/`,
    })),
  });
}
