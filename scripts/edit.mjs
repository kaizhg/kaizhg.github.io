// Live editing: watches content/*/project.md, regenerates that project's data on save, and runs
// the Astro dev server so the browser at http://127.0.0.1:4321 reloads by itself.
//   npm run edit
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, readdirSync, statSync, writeFileSync, unlinkSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const site = dirname(dirname(fileURLToPath(import.meta.url)));
const content = join(site, 'content');
const py = 'python3';

const errFile = join(site, 'public', 'edit-errors.json');
let notes = {};
const report = () => writeFileSync(errFile, JSON.stringify(notes));
const build = (slug) => {
	const r = spawnSync(py, ['scripts/content.py', 'build', ...(slug ? [slug] : [])], { cwd: site, encoding: 'utf8' });
	const warnings = (r.stderr || '').split('\n').filter((l) => l.startsWith('! ')).map((l) => l.slice(2));
	if (r.status !== 0) {
		const msg = (r.stderr || '').trim().split('\n').pop().replace(/^\w+Error: /, '');
		console.log(`\x1b[31m✗ ${msg}\x1b[0m`);
		notes[slug ?? '*'] = { error: msg };
		report();
		return false;
	}
	for (const k of Object.keys(notes)) if (!slug || k === slug || k === '*') delete notes[k];
	if (warnings.length) notes[slug ?? '*'] = { warnings };
	report();
	console.log(`\x1b[32m✓ ${slug ?? 'all projects'} regenerated\x1b[0m` + (warnings.length ? `\n\x1b[33m${warnings.join('\n')}\x1b[0m` : ''));
	return true;
};
const syncMedia = () => spawnSync('node', ['scripts/sync-media.mjs'], { cwd: site, stdio: 'inherit' });

const snapshot = () => {
	const m = new Map();
	for (const slug of readdirSync(content)) {
		const dir = join(content, slug);
		if (!statSync(dir).isDirectory()) continue;
		const md = join(dir, 'project.md');
		if (existsSync(md)) m.set(slug, statSync(md).mtimeMs);
		m.set(slug + '/media', readdirSync(dir).filter((f) => /\.(mp4|jpe?g|png)$/i.test(f)).sort().join(','));
	}
	return m;
};

build();
syncMedia();
let last = snapshot();
console.log('\n编辑模式：改 content/<项目>/project.md 存盘，浏览器会自动刷新。Ctrl+C 退出。\n');
const dev = spawn('npx', ['astro', 'dev', '--port', '4321', '--host', '127.0.0.1'], { cwd: site, stdio: 'inherit' });

setInterval(() => {
	const now = snapshot();
	for (const [key, val] of now) {
		if (last.get(key) === val) continue;
		if (key.endsWith('/media')) {
			console.log(`media changed in ${key.replace('/media', '')}`);
			syncMedia();
			build(key.replace('/media', ''));
		} else {
			build(key);
		}
	}
	for (const key of last.keys()) if (!now.has(key)) build();
	last = now;
}, 1000);
process.on('SIGINT', () => { dev.kill('SIGINT'); try { unlinkSync(errFile); } catch {} process.exit(0); });
