"""One-off importer: rebuild Selected case studies from the old kaizhang.io (Adobe Portfolio) pages.

Reads the saved page HTML + match report produced during the asset sync, resolves every image/video
to a file in ../asset (original if the library had it, otherwise the "From kaizhang.io" copy), writes
web-sized media into the site, and emits src/data/case-studies/<slug>.json with the page's blocks
in their original order.

Usage: python3 scripts/import-legacy.py <crawl_dir> [selected|archive]
"""
import html as htmllib, json, os, re, shutil, subprocess, sys
from bs4 import BeautifulSoup, NavigableString, Tag
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
CRAWL = sys.argv[1]
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET = os.path.join(os.path.dirname(SITE), 'asset')
IMG_OUT = os.path.join(SITE, 'src', 'assets', 'work')
MEDIA_OUT = os.path.join(SITE, 'public', 'media')
DATA_OUT = os.path.join(SITE, 'src', 'data', 'case-studies')
MAX_EDGE = 2400

# old URL slug -> new slug (matches src/data/projects.ts)
SELECTED = {
    'at-opt-industries': 'eyelash', 'inflatable-generator': 'inflatable-patterner', 'os-11': 'os-11',
    'large-language-objects': 'large-language-objects', 'pupas': 'imago',
    'sound-x-2021-light-effect-design': 'sound-x', 'hyperslice': 'hyperslice', 'prismo': 'prismo',
    'zhang-zhoujie-digital-lab-internship': 'tables', 'mind-bridge': 'mind-bridge', 'seesaw': 'seesaw',
    'wind': 'telewind', 'yotabyte': 'yottabyte',
}
ARCHIVE = {
    'transform': 'transform', 'vitalization': 'vitalization', 'drawing': 'ink-on-paper',
    'marble-fall': 'marble-fall', 'made-in-gh': 'made-in-gh', 'briota-iospro': 'briota-iospro',
    'give-light-a-hug': 'hug', 'invertebot': 'invertebot', 'neurodynamic': 'neurodynamic',
    'practice': 'dynamic-valley', 'homovirus': 'homovirus',
    'providence-station-seat-redesign': 'providence-seat', 'mix-musuem-guide': 'mix-museum-guide',
    'donut': 'donut-in-half', 'intersect': 'intersect', 'barnacle-lamp': 'barnacle-lamp',
    'rib-stool': 'rib-stool', 'metal': 'folded-volume', 'wood-ii': 'wood-ii', 'wood': 'wood-i',
    'being-contained': 'being-contained', 'mix-headset': 'mix-headset', 'mirrored-river': 'mirrored-river',
}
FOLDER = {  # same mapping used when placing "From kaizhang.io" downloads
    'inflatable-generator': 'Pneuhaus', 'os-11': 'Operating System 1.1', 'large-language-objects': 'LLO',
    'pupas': 'Pupas', 'sound-x-2021-light-effect-design': 'Huawei', 'hyperslice': 'HyperSlice',
    'prismo': 'Prismo', 'zhang-zhoujie-digital-lab-internship': 'Tables', 'mind-bridge': 'Mind Bridge',
    'seesaw': 'See X Saw', 'wind': 'Telewind', 'yotabyte': 'Yottabyte', 'at-opt-industries': 'Eyelash', '_covers_work': 'Thumbnail',
    '_covers_archive': 'Thumbnail',
    'barnacle-lamp': 'Barnacle Lamp', 'being-contained': 'Being Contained', 'briota-iospro': 'Briota IOSPro',
    'donut': 'Donut in haft', 'drawing': 'Drawings', 'give-light-a-hug': 'H U G', 'homovirus': 'Homovirus',
    'intersect': 'Intersect', 'invertebot': 'InverteBot', 'made-in-gh': 'GH?', 'marble-fall': 'MarbleFall',
    'metal': 'Metal I', 'mirrored-river': 'Mirrored River', 'mix-headset': 'MIX Headset',
    'mix-musuem-guide': 'MIX Museum Guide', 'neurodynamic': 'Neurodynamic', 'practice': 'Dynamic Valley',
    'providence-station-seat-redesign': 'Providence Station Seat', 'rib-stool': 'Rib Stool',
    'transform': 'Transform', 'vitalization': 'Vitalization', 'wood-ii': 'Wood II', 'wood': 'Wood I',
}
GROUP = sys.argv[2] if len(sys.argv) > 2 else 'selected'
ONLY = sys.argv[3] if len(sys.argv) > 3 else None  # optional: a single new slug to (re)import
PAGES = ARCHIVE if GROUP == 'archive' else SELECTED
COVER_KEY = '_covers_archive' if GROUP == 'archive' else '_covers_work'
INDEX_HTML = 'archive.html' if GROUP == 'archive' else 'work.html'
UUID = re.compile(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})')

report = json.load(open(os.path.join(CRAWL, 'report.json')))
manifest = json.load(open(os.path.join(CRAWL, 'manifest.json')))
videos = {v['id']: v for v in json.load(open(os.path.join(CRAWL, 'videos.json')))}


def source_for(old_slug, uuid):
    """Best local file for an image uuid: library original, else the From kaizhang.io copy, else crawl cache."""
    for key in (old_slug, COVER_KEY):
        rows = {r['uuid']: r for r in report.get(key, {}).get('images', [])}
        if uuid not in rows:
            continue
        r = rows[uuid]
        if r['match'] and os.path.exists(r['match']):
            return r['match']
        order = {im['uuid']: n for n, im in enumerate(manifest[key]['images'], 1)}
        prefix = 'cover-' + key.split('_')[-1] if key.startswith('_covers') else key
        ext = os.path.splitext(r['local'])[1].lower()
        p = os.path.join(ASSET, FOLDER[key], 'From kaizhang.io', f'{prefix}_{order[uuid]:02d}{ext}')
        return p if os.path.exists(p) else r['local']
    for key, p in manifest.items():
        for im in p['images']:
            if im['uuid'] == uuid:
                return os.path.join(CRAWL, 'site', key, f"{uuid}.{im['ext']}")
    return None


class Media:
    def __init__(self, slug):
        self.slug, self.n, self.done = slug, 0, {}
        shutil.rmtree(os.path.join(IMG_OUT, slug), ignore_errors=True)
        shutil.rmtree(os.path.join(MEDIA_OUT, slug), ignore_errors=True)
        os.makedirs(os.path.join(IMG_OUT, slug))
        os.makedirs(os.path.join(MEDIA_OUT, slug))

    def image(self, src):
        """-> block for an image (or an animated GIF turned into a looping video)."""
        if src in self.done:
            return self.done[src]
        self.n += 1
        name = f'{self.n:02d}'
        im = Image.open(src)
        frames = getattr(im, 'n_frames', 1)
        if im.format == 'GIF' and frames > 1:
            out = os.path.join(MEDIA_OUT, self.slug, name + '.mp4')
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-movflags', '+faststart',
                            '-pix_fmt', 'yuv420p', '-vf', "scale='min(1600,iw)':-2:flags=lanczos,pad=ceil(iw/2)*2:ceil(ih/2)*2",
                            '-c:v', 'libx264', '-crf', '24', '-preset', 'slow', '-an', out], check=True)
            w, h = im.size
            block = {'type': 'loop', 'src': f'/media/{self.slug}/{name}.mp4', 'width': w, 'height': h}
        else:
            im = ImageOps.exif_transpose(im)
            alpha = im.mode in ('RGBA', 'LA', 'P') and 'A' in im.convert('RGBA').getbands() and \
                im.convert('RGBA').getextrema()[3][0] < 255
            im = im.convert('RGBA' if alpha else 'RGB')
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
            ext = '.png' if alpha else '.jpg'
            out = os.path.join(IMG_OUT, self.slug, name + ext)
            if alpha:
                im.save(out, optimize=True)
            else:
                im.save(out, quality=86, optimize=True, progressive=True)
            block = {'type': 'image', 'src': f'{self.slug}/{name}{ext}', 'width': im.width, 'height': im.height}
        self.done[src] = block
        return block

    def video(self, vid):
        v = videos[vid]
        src = v['match'] if v.get('match') else None
        if not src:
            n = [x for x in videos.values() if x['slug'] == v['slug'] and not x.get('match')]
            i = [x['id'] for x in n].index(vid) + 1
            src = os.path.join(ASSET, FOLDER[v['slug']], 'From kaizhang.io', f"{v['slug']}_video_{i:02d}.mp4")
        out = os.path.join(MEDIA_OUT, self.slug, f'{vid}.mp4')
        poster = os.path.join(MEDIA_OUT, self.slug, f'{vid}.jpg')
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-movflags', '+faststart',
                        '-vf', "scale='if(gt(iw,ih),min(1920,iw),-2)':'if(gt(iw,ih),-2,min(1920,ih))'",
                        '-c:v', 'libx264', '-crf', '27', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '128k', out], check=True)
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', '1', '-i', out, '-frames:v', '1',
                        '-q:v', '4', poster], check=True)
        w, h = Image.open(poster).size
        audio = bool(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries',
                                     'stream=index', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip())
        return {'type': 'video', 'src': f'/media/{self.slug}/{vid}.mp4', 'poster': f'/media/{self.slug}/{vid}.jpg',
                'width': w, 'height': h, 'audio': audio}


# ---------- rich text -> clean HTML ----------
INLINE_OK = {'a', 'b', 'strong', 'i', 'em', 'br', 'sup', 'sub'}


def font_px(tag):
    m = re.search(r'font-size:\s*(\d+)px', tag.get('style', '')) if isinstance(tag, Tag) else None
    return int(m.group(1)) if m else 0


def inline(node):
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            out.append(htmllib.escape(str(c), quote=False))
        elif isinstance(c, Tag):
            inner = inline(c)
            bold = 'font-weight:700' in c.get('style', '').replace(' ', '') or 'bold' in c.get('style', '')
            if c.name == 'br':
                out.append('<br>')
            elif c.name == 'a' and c.get('href'):
                out.append(f'<a href="{htmllib.escape(c["href"])}">{inner}</a>')
            elif c.name in ('b', 'strong') or bold:
                out.append(f'<strong>{inner}</strong>' if inner.strip() else inner)
            elif c.name in ('i', 'em'):
                out.append(f'<em>{inner}</em>')
            else:
                out.append(inner)
    return ''.join(out)


def max_font(node):
    sizes = [font_px(t) for t in node.find_all(True)] + [font_px(node)]
    return max(sizes) if sizes else 0


def rich_text(div):
    parts = []
    for c in div.children:
        if isinstance(c, NavigableString):
            if c.strip():
                parts.append(('p', htmllib.escape(c.strip())))
            continue
        if not isinstance(c, Tag):
            continue
        cls = ' '.join(c.get('class', []))
        if c.name in ('ul', 'ol'):
            items = ''.join(f'<li>{inline(li).strip()}</li>' for li in c.find_all('li'))
            parts.append((c.name, items))
            continue
        text = re.sub(r'(<br>\s*)+$', '', inline(c).strip())
        if not re.sub(r'<br>|\s|&nbsp;|\xa0', '', text):
            parts.append(('gap', ''))
            continue
        size = max_font(c)
        if 'title' in cls.split() or size >= 36:
            tag = 'h2'
        elif 'sub-title' in cls or size >= 24:
            tag = 'h3'
        elif 'caption' in cls:
            tag = 'caption'
        else:
            tag = 'p'
        parts.append((tag, text))
    # merge consecutive plain lines into paragraphs; blank lines split paragraphs
    html, buf = [], []
    def flush():
        if buf:
            html.append('<p>' + '<br>'.join(buf) + '</p>')
            buf.clear()
    for tag, text in parts:
        if tag == 'p':
            buf.append(text)
            continue
        flush()
        if tag == 'gap':
            continue
        if tag in ('h2', 'h3') and html and html[-1].startswith(f'<{tag}>'):
            html[-1] = html[-1][:-len(f'</{tag}>')] + '<br>' + text + f'</{tag}>'  # multi-line heading
        elif tag == 'caption':
            html.append(f'<p class="caption">{text}</p>')
        elif tag in ('ul', 'ol'):
            html.append(f'<{tag}>{text}</{tag}>')
        else:
            html.append(f'<{tag}>{text}</{tag}>')
    flush()
    return '\n'.join(html)


# ---------- module walker ----------
def best_uuid(tag):
    for attr in ('data-src', 'src'):
        for el in [tag] + tag.find_all(True):
            v = el.get(attr) if isinstance(el, Tag) else None
            if v and 'myportfolio' in v:
                m = UUID.search(v.split('/')[-1])
                if m:
                    return m.group(1)
    return None


def module_blocks(mod, old, media):
    cls = mod.get('class', [])
    kind = next((c.split('project-module-')[1] for c in cls if c.startswith('project-module-')), None)
    if kind == 'text':
        t = mod.select_one('.rich-text')
        h = rich_text(t) if t else ''
        return [{'type': 'text', 'html': h}] if h.strip() else []
    if kind == 'image':
        u = best_uuid(mod)
        src = source_for(old, u) if u else None
        if not src:
            return []
        b = dict(media.image(src))
        cap = mod.select_one('.module-caption-container .rich-text, .module-caption-container')
        if cap and cap.get_text(strip=True):
            b['caption'] = inline(cap).strip()
        return [b]
    if kind == 'media_collection':
        items = []
        for it in mod.select('.js-grid-item-container'):
            u = best_uuid(it)
            src = source_for(old, u) if u else None
            if src:
                items.append(media.image(src))
        return [{'type': 'gallery', 'items': items}] if items else []
    if kind == 'video':
        f = mod.find('iframe')
        m = re.search(r'/(?:ccv|embeds)/([^/?]+)', f['src']) if f else None
        return [media.video(m.group(1))] if m else []
    if kind == 'embed':
        f = mod.find('iframe')
        m = re.search(r'youtube\.com/embed/([\w-]+)', f['src']) if f else None
        return [{'type': 'youtube', 'id': m.group(1)}] if m else []
    if kind == 'tree':
        cols = []
        for child in mod.select_one('.tree-wrapper').find_all('div', class_='tree-child-wrapper', recursive=False):
            flex = float(re.search(r'flex:\s*([\d.]+)', child.get('style', 'flex: 1')).group(1))
            blocks = []
            for m in child.find_all('div', class_='project-module', recursive=False):
                blocks += module_blocks(m, old, media)
            if blocks:
                cols.append({'flex': flex, 'blocks': blocks})
        if not cols:
            return []
        total = sum(c['flex'] for c in cols)
        for c in cols:
            c['flex'] = round(c['flex'] / total, 4)
        return [{'type': 'row', 'columns': cols}] if len(cols) > 1 else cols[0]['blocks']
    return []


def covers():
    """old slug -> [cover uuid, rollover uuid] from the Selected index."""
    s = BeautifulSoup(open(os.path.join(CRAWL, INDEX_HTML)).read(), 'html.parser')
    out = {}
    for a in s.select('a.project-cover'):
        uu = []
        for img in a.select('img'):
            v = img.get('data-src') or img.get('src') or ''
            m = UUID.search(v.split('/')[-1])
            if m and m.group(1) not in uu:
                uu.append(m.group(1))
        out[a['href'].strip('/').split('/')[-1]] = uu
    return out


def main():
    os.makedirs(DATA_OUT, exist_ok=True)
    cov = covers()
    for old, slug in PAGES.items():
        if ONLY and slug != ONLY:
            continue
        media = Media(slug)
        # hero: the largest of the cover / rollover images
        cands = [source_for(COVER_KEY, u) for u in cov.get(old, [])]
        cands = [c for c in cands if c and os.path.exists(c) and min(Image.open(c).size) >= 400]
        hero = None
        if cands:
            best = max(cands, key=lambda p: Image.open(p).size[0] * Image.open(p).size[1])
            hero = media.image(best)
        raw = open(os.path.join(CRAWL, 'pages', old + '.html')).read()
        soup = BeautifulSoup(raw, 'html.parser')
        first = soup.select_one('.js-project-modules div.project-module')
        root = first.parent if first else None
        blocks = []
        if root:
            for m in root.find_all('div', class_='project-module', recursive=False):
                blocks += module_blocks(m, old, media)
        if not hero:  # fall back to the first still image on the page
            hero = next((b for b in blocks if b['type'] == 'image'), None)
        data = {'slug': slug, 'legacy': f'https://kaizhang.io/{old}', 'hero': hero,
                'locked': root is None, 'blocks': blocks}
        json.dump(data, open(os.path.join(DATA_OUT, slug + '.json'), 'w'), indent=1, ensure_ascii=False)
        print(f'{slug:24s} blocks={len(blocks):3d} media={media.n:3d} hero={"yes" if hero else "no"}')


if __name__ == '__main__':
    main()
