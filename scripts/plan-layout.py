"""Assign a magazine layout to every block of the Selected case studies.

Pass 1 classifies media (photo / white-background diagram or render / logo strip / small
thumbnail) by looking at the pixels. Pass 2 applies per-project decisions made by eye
(see PLAN below). The result is written into each block as `layout` (a cell class that
src/components/Blocks.astro understands) plus `kind` for reference. Blocks without a
`layout` fall back to the automatic rules in Blocks.astro.

Cell vocabulary (12-column grid):
  full | wide-l wide-r | half-l half-r | narrow-l narrow-r | third-l third-r
  small-l small-c small-r | tri-a tri-b tri-c | text-l text-r | beside-l beside-r
  quote | section | credits | skip           (+ ' stagger' modifier; ' pull' = render before the previous cell)
Gallery layouts: grid2 grid3 grid4 grid5 strip.   Row layouts: stagger (offset 2nd column).

Usage: python3 scripts/plan-layout.py
"""
import json, os, re, glob
from PIL import Image, ImageOps

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(SITE, 'src', 'data', 'case-studies')
IMG = os.path.join(SITE, 'src', 'assets', 'work')
CREDITS = re.compile(r'^\s*(course|for:|instructor|project team|team members?|my role|special thanks|thanks:|all the works|harvard graduate|realized)', re.I)


def whiteness(block):
    """Mean brightness of the image border: high values mean a diagram/render on white."""
    if block['type'] != 'image':
        return 0
    im = Image.open(os.path.join(IMG, block['src']))
    im.draft('L', (400, 400))
    im = ImageOps.exif_transpose(im.convert('L')).resize((200, 200))
    px = im.load()
    edge = [px[x, y] for x in range(200) for y in (0, 1, 198, 199)] + [px[x, y] for y in range(200) for x in (0, 1, 198, 199)]
    return sum(edge) / len(edge)


def kind_of(block):
    if block['type'] not in ('image', 'loop'):
        return block['type']
    r = block['width'] / block['height']
    if r > 3.2:
        return 'logo'
    if max(block['width'], block['height']) <= 700:
        return 'small'
    if block['type'] == 'image' and whiteness(block) >= 232:
        return 'white'
    return 'photo'


def text_of(html):
    return re.sub(r'<[^>]+>', ' ', html).strip()


def tag(bs):
    """Annotate kinds recursively; galleries/rows get sensible inner layouts."""
    for b in bs:
        if b['type'] == 'text':
            b['html'] = re.sub(r'(?<![.:!?\u2026\u2014)\]])\s*<br>\s*(?=[a-z(])', ' ', b['html'])
            t = text_of(b['html'])
            if CREDITS.match(t):
                b['kind'] = 'credits'
            elif re.search(r'<h[23]>', b['html']) and not re.search(r'<p>|<ul>|<ol>', b['html']):
                # short = section label, medium = pull quote, long = it's really a paragraph in heading clothes
                if len(t) < 36:
                    b['kind'] = 'section'
                elif len(t) < 200 and '<h2>' in b['html'] and '<a ' not in b['html']:
                    b['kind'] = 'quote'  # the old site's big statements (links mean a call-to-action, not a quote)
                elif len(t) < 200:
                    b['kind'] = 'text'  # a note between pictures: keep it modest
                    b['html'] = b['html'].replace('<h2>', '<h3>').replace('</h2>', '</h3>')
                else:
                    b['kind'] = 'text'
                    b['html'] = re.sub(r'</?h[23]>', lambda m: '<p>' if m.group(0) == '<h2>' or m.group(0) == '<h3>' else '</p>', b['html'])
            else:
                b['kind'] = 'text'
        elif b['type'] == 'gallery':
            for it in b['items']:
                it['kind'] = kind_of(it)
            b['kind'] = 'gallery'
        elif b['type'] == 'row':
            for c in b['columns']:
                tag(c['blocks'])
                for g in c['blocks']:
                    if g['type'] == 'gallery' and len(g['items']) >= 4:
                        g['layout'] = 'grid3' if len(g['items']) >= 7 else 'grid2'
                    elif g['type'] == 'gallery' and all(it['width'] / it['height'] > 1.6 for it in g['items']):
                        g['layout'] = 'stack'  # wide drawings side by side would be tiny
            b['kind'] = 'row'  # rows are top-aligned; set layout 'stagger' in PLAN to offset the second column
        else:
            b['kind'] = kind_of(b)


def merge_runs(bs):
    """Runs of similar unplanned images become one gallery: slide decks (white, landscape,
    4+) as two-up grids, series of product photos (3+, same orientation) as three-up grids.
    A viewer scans a series faster as a grid than as a stack of full-width pictures."""
    out, i = [], 0
    def plain(b):
        return b['type'] == 'image' and 'layout' not in b and not b.get('caption')
    while i < len(bs):
        b = bs[i]
        if plain(b):
            j = i
            kind = b['kind']
            land = b['width'] >= b['height']
            while j < len(bs) and plain(bs[j]) and bs[j]['kind'] == kind and (bs[j]['width'] >= bs[j]['height']) == land \
                    and abs(bs[j]['width'] / bs[j]['height'] - b['width'] / b['height']) < 0.2:
                j += 1
            n = j - i
            if (kind == 'white' and land and n >= 4) or (kind == 'photo' and n >= 3):
                items = bs[i:j]
                out.append({'type': 'gallery', 'items': items, 'kind': 'gallery',
                            'layout': 'grid2' if kind == 'white' else 'grid3'})
                i = j
                continue
        out.append(b)
        i += 1
    return out


def auto(bs):
    """Default layouts for blocks the PLAN doesn't mention."""
    for b in bs:
        if 'layout' in b:
            continue
        k = b.get('kind')
        if k == 'credits':
            b['layout'] = 'credits'
        elif k == 'logo':
            b['layout'] = 'small-l'
        elif b['type'] == 'gallery' and len(b['items']) >= 2:
            n = len(b['items'])
            cols = 5 if n >= 10 else 4 if n >= 7 or n == 4 else 3 if n >= 3 else 2
            # Portrait pictures are tall: give them one more column so no row is a screen high
            if sum(1 for it in b['items'] if it['height'] > it['width']) > n / 2 and n >= 2:
                cols = min(cols + 1, 5)
            b['layout'] = f'grid{cols}'


# ---- decisions made by eye per project: block index -> layout ----
PLAN = {
    'large-language-objects': {7: 'wide-l', 11: 'wide-r', 12: 'half-l', 20: 'credits'},
    'os-11': {3: 'half-l', 4: 'half-r', 5: 'quote', 9: 'carousel', 11: 'section', 12: 'full', 13: 'half-l', 14: 'half-r stagger'},
    'hyperslice': {1: 'half-l', 2: 'beside-r', 3: 'grid4', 5: 'full', 8: 'grid4'},
    'imago': {0: 'small-l', 1: 'beside-r', 2: 'half-l', 3: 'grid3', 4: 'narrow-r', 8: 'wide-l', 9: 'text-l',
              10: 'half-l', 11: 'half-r', 12: 'text-r', 13: 'half-l', 14: 'section', 15: 'tri-a', 16: 'tri-b', 17: 'tri-c'},
    'seesaw': {2: 'full', 3: 'half-l', 4: 'half-r stagger', 5: 'section', 6: 'grid3', 7: 'grid3', 8: 'section',
               9: 'full', 14: 'half-r', 16: 'wide-l', 18: 'small-l'},
    'tables': {0: 'full', 2: 'half-l', 3: 'grid3', 4: 'wide-r'},
    'yottabyte': {2: 'quote', 3: 'full', 4: 'half-l', 5: 'half-r', 6: 'wide-l', 7: 'full', 8: 'half-l', 9: 'half-r'},
    'prismo': {2: 'quote', 4: 'text-l', 6: 'wide-r', 9: 'text-l', 10: 'half-r', 11: 'half-l', 14: 'grid3', 17: 'section',
               19: 'wide-l', 20: 'section', 21: 'full', 24: 'half-l', 25: 'half-r', 26: 'grid3'},
    'inflatable-patterner': {11: 'grid4'},
    'eyelash': {7: 'stack'},  # the ten overview slides read full width, as on the old site
    'mind-bridge': {1: 'full', 2: 'half-l', 3: 'half-r', 4: 'full'},
    # ---- archive ----
    'vitalization': {2: 'wide-l', 3: 'wide-r stagger', 5: 'wide-c'},
    'ink-on-paper': {1: 'grid3', 2: 'grid3', 3: 'grid3', 4: 'grid2', 6: 'strip', 7: 'grid4', 8: 'strip', 9: 'grid5', 10: 'text-l'},
    'marble-fall': {0: 'full', 1: 'half-l', 2: 'half-r stagger', 3: 'half-l', 4: 'narrow-r stagger'},
    'made-in-gh': {0: 'wide-l', 1: 'small-r stagger', 2: 'grid3', 3: 'half-l', 4: 'half-r stagger', 5: 'wide-c', 6: 'half-l',
                   7: 'half-r stagger', 8: 'wide-r', 9: 'half-l', 10: 'narrow-r stagger', 11: 'wide-l', 12: 'full', 13: 'wide-r'},
    'briota-iospro': {},  # slide deck: rhythm generated below
    'hug': {0: 'quote', 1: 'wide-l', 2: 'wide-r stagger', 3: 'full'},
    'invertebot': {5: 'full', 6: 'wide-r', 7: 'full', 8: 'section', 9: 'wide-l', 10: 'small-r stagger'},
    'neurodynamic': {1: 'full', 2: 'wide-r'},
    'dynamic-valley': {0: 'text-l', 2: 'grid3', 5: 'wide-c'},
    'homovirus': {0: 'full', 2: 'half-l', 3: 'half-r stagger', 4: 'wide-r', 5: 'section', 6: 'strip', 7: 'wide-l', 9: 'wide-r'},
    'providence-seat': {0: 'full', 1: 'wide-l', 2: 'wide-r stagger'},
    'mix-museum-guide': {0: 'full', 1: 'half-l', 2: 'half-r stagger', 3: 'wide-l', 4: 'half-l', 5: 'half-r stagger'},
    'donut-in-half': {0: 'full', 2: 'grid3', 3: 'wide-c'},
    'intersect': {0: 'grid5', 1: 'grid4', 2: 'grid4', 4: 'wide-l', 5: 'half-r stagger', 6: 'full'},
    'barnacle-lamp': {0: 'full', 1: 'half-l', 2: 'narrow-r stagger', 3: 'wide-l', 4: 'half-r stagger', 5: 'half-l',
                      6: 'wide-r stagger', 7: 'full', 8: 'half-l', 9: 'half-r stagger'},
    'rib-stool': {2: 'wide-l', 3: 'wide-r stagger'},
    'wood-ii': {0: 'full', 2: 'wide-l', 3: 'grid3'},
    'wood-i': {0: 'full', 1: 'half-l', 2: 'half-r stagger', 3: 'wide-l', 4: 'small-r stagger', 5: 'half-l', 6: 'half-r stagger', 7: 'grid3'},
    'mix-headset': {1: 'full', 2: 'half-l', 3: 'half-r stagger', 4: 'wide-r', 5: 'half-l', 6: 'half-r stagger'},
    'mirrored-river': {1: 'full'},
    'telewind': {1: 'full', 2: 'half-l', 3: 'half-r', 4: 'full'},
    'sound-x': {0: 'full'},
}


def split_gallery_rows(bs):
    """A row that squeezes a gallery of 4+ pictures into one column becomes sequential blocks:
    the pictures get a full-width grid instead of thumbnails nobody can read."""
    out = []
    for b in bs:
        if b['type'] == 'row' and 'layout' not in b and any(g['type'] == 'gallery' and len(g['items']) >= 4 for c in b['columns'] for g in c['blocks']):
            for c in b['columns']:
                out += c['blocks']
        else:
            out.append(b)
    return out


def split_credit_rows(bs):
    """A row made of two text columns (credits + intro) becomes two plain text blocks."""
    out = []
    for b in bs:
        if b['type'] == 'row' and all(len(c['blocks']) == 1 and c['blocks'][0]['type'] == 'text' for c in b['columns']):
            out += [c['blocks'][0] for c in b['columns']]
        else:
            out.append(b)
    return out


# Pages that open with two pictures close together instead of a lone hero: the hero becomes
# the first block (left) and the next image sits beside it, dropped down a little.
HERO_INLINE = {'folded-volume': ('wide-l', 'small-r stagger'), 'being-contained': ('wide-l', 'small-r stagger')}
# Slide decks: title slides go full width as section breaks; the rest are read two-up (merge_runs)
DECKS = {'briota-iospro': {0, 22, 29}}  # indices of title slides

for f in sorted(glob.glob(os.path.join(DATA, '*.json'))):
    d = json.load(open(f))
    blocks = d['blocks']
    if d['slug'] in HERO_INLINE and d.get('hero') and not d.get('heroInline'):
        blocks.insert(0, dict(d['hero']))
        d['hero'] = None
        d['heroInline'] = True
    if d['slug'] in HERO_INLINE:
        for i, lay in zip(range(2), HERO_INLINE[d['slug']]):
            PLAN.setdefault(d['slug'], {})[i] = lay
    if d['slug'] in DECKS:
        for i in DECKS[d['slug']]:
            PLAN.setdefault(d['slug'], {})[i] = 'full'
    if d.get('heroInline'):
        d['hero'] = None  # the hero lives in the blocks on these pages
    for b in blocks:  # start clean so the script is re-runnable
        b.pop('layout', None)
        b.pop('kind', None)
    blocks = split_credit_rows(blocks)
    for i, lay in PLAN.get(d['slug'], {}).items():  # indices refer to the credit-split blocks
        if i < len(blocks):
            blocks[i]['layout'] = lay
    blocks = split_gallery_rows(blocks)  # only rows without a planned layout are split
    tag(blocks)
    if d['slug'] in DECKS:  # every board in a deck is a slide, photos included
        for b in blocks:
            if b['type'] == 'image':
                b['kind'] = 'white'
    blocks = merge_runs(blocks)
    auto(blocks)
    d['blocks'] = blocks
    json.dump(d, open(f, 'w'), indent=1, ensure_ascii=False)
    kinds = {}
    for b in blocks:
        kinds[b.get('kind')] = kinds.get(b.get('kind'), 0) + 1
    print(f"{d['slug']:24s} {len(blocks):3d} blocks  {kinds}")
