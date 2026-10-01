// Copy the videos (and their poster stills) out of content/<slug>/ into public/media/<slug>/
// so the built site can serve them by URL. Runs before every build; public/media is not in git.
import { cpSync, existsSync, mkdirSync, readdirSync, rmSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const site = dirname(dirname(fileURLToPath(import.meta.url)));
const content = join(site, 'content');
const out = join(site, 'public', 'media');
rmSync(out, { recursive: true, force: true });
let n = 0;
for (const slug of readdirSync(content)) {
	const dir = join(content, slug);
	if (!statSync(dir).isDirectory()) continue;
	const files = readdirSync(dir);
	const stems = new Set(files.filter((f) => f.endsWith('.mp4')).map((f) => f.slice(0, -4)));
	for (const f of files) {
		const stem = f.replace(/\.(mp4|jpg)$/, '');
		if (!f.endsWith('.mp4') && !(f.endsWith('.jpg') && stems.has(stem))) continue;
		mkdirSync(join(out, slug), { recursive: true });
		cpSync(join(dir, f), join(out, slug, f));
		n++;
	}
}
console.log(`sync-media: ${n} files -> public/media`);
