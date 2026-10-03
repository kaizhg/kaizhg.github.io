// Password-protected projects: after `astro build`, the page's <article> is replaced by a
// password form, and the original markup travels inside the page encrypted (AES-GCM, key from
// PBKDF2 of the password). The browser decrypts it with WebCrypto when the right password is
// typed; nothing is sent anywhere. Pictures stay reachable by URL, so this is a soft lock.
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { pbkdf2Sync, randomBytes, createCipheriv } from 'node:crypto';

const site = dirname(dirname(fileURLToPath(import.meta.url)));
const data = join(site, 'src', 'data', 'case-studies');
const dist = join(site, 'dist');
const ITER = 200000;
let n = 0;
for (const f of readdirSync(data)) {
	if (!f.endsWith('.json')) continue;
	const d = JSON.parse(readFileSync(join(data, f), 'utf8'));
	if (!d.password) continue;
	const page = join(dist, 'work', d.slug, 'index.html');
	if (!existsSync(page)) continue;
	let html = readFileSync(page, 'utf8');
	const m = html.match(/<article[\s\S]*?<\/article>/);
	if (!m) {
		console.warn(`lock-pages: no <article> in ${d.slug}`);
		continue;
	}
	const salt = randomBytes(16), iv = randomBytes(12);
	const key = pbkdf2Sync(String(d.password).normalize('NFKC'), salt, ITER, 32, 'sha256');
	const cipher = createCipheriv('aes-256-gcm', key, iv);
	const enc = Buffer.concat([cipher.update(m[0], 'utf8'), cipher.final(), cipher.getAuthTag()]);
	const payload = Buffer.concat([salt, iv, enc]).toString('base64');
	const title = (m[0].match(/<h1[^>]*>([^<]*)<\/h1>/) || [])[1] || d.slug;
	const code = (m[0].match(/<p class="code[^"]*"[^>]*>([^<]*)<\/p>/) || [])[1] || '';
	const gate = `<article class="gate" data-lock="${d.slug}">
<div class="gate-box">
${code ? `<p class="gate-code">${code}</p>` : ''}
<h1 class="gate-title">${title}</h1>
<p class="gate-lead">This project is password protected.</p>
<form class="gate-form" autocomplete="off">
<input type="password" name="p" placeholder="Password" aria-label="Password" autofocus required>
<button type="submit">Open →</button>
</form>
<p class="gate-err" hidden>That is not it. Try again.</p>
<p class="gate-note">Write me for the password: <a href="mailto:this.kaizhang@gmail.com">this.kaizhang@gmail.com</a></p>
</div>
</article>
<style>
.gate{min-height:60vh;display:flex;align-items:center}
.gate-box{max-width:30rem}
.gate-code{font:12px var(--mono);letter-spacing:.06em;color:var(--muted);margin:0 0 10px}
.gate-title{font-size:clamp(32px,4.2vw,56px);line-height:1.05;letter-spacing:-.02em;font-weight:600;margin:0 0 18px}
.gate-lead{font-family:var(--text);font-size:17px;line-height:1.5;margin:0 0 22px}
.gate-form{display:flex;gap:12px;align-items:stretch;max-width:24rem}
.gate-form input{flex:1;min-width:0;font:16px var(--text);padding:10px 0;border:0;border-bottom:1px solid var(--fg);background:transparent;color:var(--fg);border-radius:0;outline:none}
.gate-form input:focus{border-bottom-color:var(--accent)}
.gate-form button{font:500 12px var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:10px 16px;border:1px solid var(--fg);background:transparent;color:var(--fg);cursor:pointer}
.gate-form button:hover{background:var(--fg);color:var(--bg)}
.gate-err{font:12px var(--mono);color:var(--accent);margin:12px 0 0}
.gate-note{font:12px var(--mono);color:var(--muted);margin:28px 0 0}
.gate-note a{color:inherit;text-decoration:underline;text-underline-offset:3px}
</style>
<script type="text/plain" id="lock-data">${payload}</script>
<script data-astro-rerun>
(() => {
	const art = document.querySelector('article.gate'); if (!art) return;
	const slug = art.dataset.lock;
	const bytes = Uint8Array.from(atob(document.getElementById('lock-data').textContent.trim()), (c) => c.charCodeAt(0));
	const salt = bytes.slice(0, 16), iv = bytes.slice(16, 28), body = bytes.slice(28);
	async function open(pw) {
		const km = await crypto.subtle.importKey('raw', new TextEncoder().encode(pw.normalize('NFKC')), 'PBKDF2', false, ['deriveKey']);
		const key = await crypto.subtle.deriveKey({ name: 'PBKDF2', salt, iterations: ${ITER}, hash: 'SHA-256' }, km, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
		return new TextDecoder().decode(await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, body));
	}
	async function unlock(pw, remember) {
		let html; try { html = await open(pw); } catch { return false; }
		if (remember) try { sessionStorage.setItem('lock:' + slug, pw); } catch {}
		const tpl = document.createElement('template'); tpl.innerHTML = html;
		art.replaceWith(tpl.content);
		document.dispatchEvent(new Event('astro:page-load')); // wake the page's own scripts for the new content
		return true;
	}
	let saved = null; try { saved = sessionStorage.getItem('lock:' + slug); } catch {}
	if (saved) unlock(saved, false);
	const form = art.querySelector('form');
	form.addEventListener('submit', async (e) => {
		e.preventDefault();
		if (!(await unlock(form.p.value, true))) { art.querySelector('.gate-err').hidden = false; form.p.select(); }
	});
})();
</script>`;
	html = html.replace(m[0], gate).replace('</head>', '<meta name="robots" content="noindex">\n</head>');
	writeFileSync(page, html);
	n++;
}
console.log(`lock-pages: ${n} page(s) locked`);
