import { readFileSync } from "node:fs";

const HOST = process.env.SITE_HOST || "gilmanuel.com";
const KEY = process.env.INDEXNOW_KEY || "5258853dcab540a5bb1ad5e7e19e04ab";
const SITEMAP = process.env.SITEMAP || "dist/sitemap-0.xml";
const SITEMAP_URL = process.env.SITEMAP_URL;

let xml;
if (SITEMAP_URL) {
  const response = await fetch(SITEMAP_URL);
  if (!response.ok) {
    console.error(`Failed to fetch sitemap ${SITEMAP_URL}: HTTP ${response.status}`);
    process.exit(1);
  }
  xml = await response.text();
} else {
  xml = readFileSync(SITEMAP, "utf8");
}

const urlList = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);

if (urlList.length === 0) {
  console.error("No URLs found in sitemap");
  process.exit(1);
}

const response = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST",
  headers: { "Content-Type": "application/json; charset=utf-8" },
  body: JSON.stringify({
    host: HOST,
    key: KEY,
    keyLocation: `https://${HOST}/${KEY}.txt`,
    urlList,
  }),
});

console.log(`IndexNow: submitted ${urlList.length} URLs -> HTTP ${response.status}`);
