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
Gallery layouts: grid2 grid3 grid4 grid5 strip.   Row layouts: flat (no stagger).

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
            t = text_of(b['html'])
            if CREDITS.match(t):
                b['kind'] = 'credits'
            elif re.search(r'<h[23]>', b['html']) and not re.search(r'<p>|<ul>|<ol>', b['html']):
                b['kind'] = 'section' if len(t) < 36 else 'quote'
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
            media = [g for c in b['columns'] for g in c['blocks']]
            if len(b['columns']) == 2 and all(g['type'] in ('image', 'loop', 'video') for g in media) \
                    and any(g.get('kind') in ('white', 'small') for g in media):
                b['layout'] = 'flat'
            b['kind'] = 'row'
        else:
            b['kind'] = kind_of(b)


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
        elif b['type'] == 'gallery' and len(b['items']) >= 4:
            n = len(b['items'])
            b['layout'] = 'grid5' if n >= 10 else 'grid4' if n >= 7 or n == 4 else 'grid3'


# ---- decisions made by eye per project: block index -> layout ----
PLAN = {
    'large-language-objects': {7: 'wide-l', 11: 'wide-r', 12: 'half-l', 20: 'credits'},
    'os-11': {3: 'half-l', 4: 'half-r', 5: 'quote', 9: 'grid3', 11: 'section', 12: 'full', 13: 'half-l', 14: 'half-r stagger'},
    'hyperslice': {1: 'half-l', 2: 'beside-r', 3: 'grid4', 5: 'full', 8: 'grid4'},
    'imago': {0: 'small-l', 1: 'beside-r', 2: 'half-l', 3: 'grid3', 4: 'narrow-r', 8: 'wide-l', 9: 'text-l',
              10: 'half-l', 11: 'half-r', 12: 'text-r', 13: 'half-l', 14: 'section', 15: 'tri-a', 16: 'tri-b', 17: 'tri-c'},
    'seesaw': {2: 'full', 3: 'half-l', 4: 'half-r stagger', 5: 'section', 6: 'grid3', 7: 'grid3', 8: 'section',
               9: 'full', 14: 'half-r', 16: 'wide-l', 18: 'small-l'},
    'tables': {0: 'full', 2: 'half-l', 3: 'grid3', 4: 'wide-r'},
    'yottabyte': {2: 'quote', 3: 'full', 4: 'half-l', 5: 'half-r', 6: 'wide-l', 7: 'full', 8: 'half-l', 9: 'half-r'},
    'prismo': {2: 'quote', 4: 'text-l', 6: 'wide-r', 9: 'text-l', 10: 'half-r', 11: 'grid4', 14: 'grid3', 17: 'section',
               19: 'wide-l', 20: 'section', 21: 'full', 24: 'half-l', 25: 'half-r', 26: 'grid3'},
    'inflatable-patterner': {1: 'text-l', 2: 'wide-r', 3: 'text-l', 5: 'text-r', 6: 'grid4', 8: 'wide-l', 9: 'text-r',
                             10: 'grid5', 11: 'text-l', 12: 'half-r', 13: 'text-l', 15: 'text-r', 17: 'text-l',
                             18: 'narrow-r', 19: 'text-l', 21: 'quote', 22: 'grid4'},
    'mind-bridge': {1: 'full', 2: 'half-l', 3: 'half-r', 4: 'full'},
    'telewind': {1: 'full', 2: 'half-l', 3: 'half-r', 4: 'full'},
    'sound-x': {0: 'full'},
}


def split_credit_rows(bs):
    """A row made of two text columns (credits + intro) becomes two plain text blocks."""
    out = []
    for b in bs:
        if b['type'] == 'row' and all(len(c['blocks']) == 1 and c['blocks'][0]['type'] == 'text' for c in b['columns']):
            out += [c['blocks'][0] for c in b['columns']]
        else:
            out.append(b)
    return out


for f in sorted(glob.glob(os.path.join(DATA, '*.json'))):
    d = json.load(open(f))
    blocks = d['blocks']
    for b in blocks:  # start clean so the script is re-runnable
        b.pop('layout', None)
        b.pop('kind', None)
    blocks = split_credit_rows(blocks)
    for i, lay in PLAN.get(d['slug'], {}).items():  # indices refer to the blocks after the split
        if i < len(blocks):
            blocks[i]['layout'] = lay
    tag(blocks)
    auto(blocks)
    d['blocks'] = blocks
    json.dump(d, open(f, 'w'), indent=1, ensure_ascii=False)
    kinds = {}
    for b in blocks:
        kinds[b.get('kind')] = kinds.get(b.get('kind'), 0) + 1
    print(f"{d['slug']:24s} {len(blocks):3d} blocks  {kinds}")
