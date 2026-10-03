// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { readdirSync, readFileSync } from 'node:fs';

// Password-protected projects (front-matter `password`) are left out of the sitemap
const locked = readdirSync('src/data/case-studies')
	.filter((f) => f.endsWith('.json'))
	.map((f) => JSON.parse(readFileSync(`src/data/case-studies/${f}`, 'utf8')))
	.filter((d) => d.password)
	.map((d) => `/work/${d.slug}/`);

// https://astro.build/config
export default defineConfig({
	site: 'https://kaizhang.io',
	integrations: [sitemap({ filter: (page) => !/\/(404)\/?$/.test(page) && !locked.some((p) => page.endsWith(p)) })],
});
