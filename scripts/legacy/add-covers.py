"""Add the old site's tile covers to the Selected case studies.

Each project on kaizhang.io/work had a default cover and a rollover image (sometimes an
animated GIF). This downloads both at full size into ../asset/Thumbnail/From kaizhang.io/,
writes web copies into the site, and stores them as `cover` / `hover` blocks in
src/data/case-studies/<slug>.json. The page hero (`hero`) is left untouched.

Usage: python3 scripts/add-covers.py <crawl_dir> [selected|archive]
"""
import json, os, re, subprocess, sys
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
CRAWL = sys.argv[1]
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(os.path.dirname(SITE), 'asset', 'Thumbnail', 'From kaizhang.io')
IMG_OUT = os.path.join(SITE, 'src', 'assets', 'work')
MEDIA_OUT = os.path.join(SITE, 'public', 'media')
DATA = os.path.join(SITE, 'src', 'data', 'case-studies')
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
GROUP = sys.argv[2] if len(sys.argv) > 2 else 'selected'
PAGES = ARCHIVE if GROUP == 'archive' else SELECTED
INDEX_HTML = 'archive.html' if GROUP == 'archive' else 'work.html'


def largest(img):
    """Largest URL in an <img>'s srcset (falls back to data-src)."""
    best, size = img.get('data-src') or img.get('src'), 0
    for part in (img.get('data-srcset') or '').split(','):
        part = part.strip()
        if not part:
            continue
        url, w = part.rsplit(' ', 1)
        if int(w.rstrip('w')) > size:
            best, size = url, int(w.rstrip('w'))
    return best


def download(url, dest):
    if not os.path.exists(dest):
        subprocess.run(['curl', '-sfL', '--retry', '3', '-o', dest + '.part', url], check=True)
        os.rename(dest + '.part', dest)
    return dest


def to_web(src, slug, name):
    """Still image -> src/assets/work/<slug>/<name>.jpg; animated GIF -> public/media/<slug>/<name>.mp4."""
    im = Image.open(src)
    if im.format == 'GIF' and getattr(im, 'n_frames', 1) > 1:
        os.makedirs(os.path.join(MEDIA_OUT, slug), exist_ok=True)
        out = os.path.join(MEDIA_OUT, slug, name + '.mp4')
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-movflags', '+faststart',
                        '-pix_fmt', 'yuv420p', '-vf', "scale='min(1600,iw)':-2:flags=lanczos,pad=ceil(iw/2)*2:ceil(ih/2)*2",
                        '-c:v', 'libx264', '-crf', '24', '-preset', 'slow', '-an', out], check=True)
        return {'type': 'loop', 'src': f'/media/{slug}/{name}.mp4', 'width': im.width, 'height': im.height}
    im = ImageOps.exif_transpose(im).convert('RGB')
    im.thumbnail((2400, 2400), Image.LANCZOS)
    os.makedirs(os.path.join(IMG_OUT, slug), exist_ok=True)
    out = os.path.join(IMG_OUT, slug, name + '.jpg')
    im.save(out, quality=86, optimize=True, progressive=True)
    return {'type': 'image', 'src': f'{slug}/{name}.jpg', 'width': im.width, 'height': im.height}


os.makedirs(ASSET_DIR, exist_ok=True)
soup = BeautifulSoup(open(os.path.join(CRAWL, INDEX_HTML)).read(), 'html.parser')
for a in soup.select('a.project-cover'):
    old = a['href'].strip('/')
    slug = PAGES.get(old)
    if not slug:
        continue
    roll = a.select_one('.cover-rollover img')
    cover = next((i for i in a.select('img') if i is not roll), None)
    f = os.path.join(DATA, slug + '.json')
    d = json.load(open(f))
    for key, img in (('cover', cover), ('hover', roll)):
        if img is None:
            d[key] = None
            continue
        url = largest(img)
        ext = re.search(r'\.(\w+)(?:\?|$)', url).group(1).lower()
        local = download(url, os.path.join(ASSET_DIR, f'{key}-{slug}.{ext}'))
        d[key] = to_web(local, slug, key)
    json.dump(d, open(f, 'w'), indent=1, ensure_ascii=False)
    print(f"{slug:24s} cover={d['cover'] and d['cover']['type']:6s} hover={d['hover'] and d['hover']['type']}")
