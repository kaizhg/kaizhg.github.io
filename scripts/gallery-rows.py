"""Copy the old site's 'max images per row' onto gallery blocks as `cols`, where the
imported galleries line up one-to-one with the crawled grids. Run after plan-layout.py:
python3 scripts/gallery-rows.py <crawl-dir>"""
import sys, re, json, os
C = sys.argv[1]
src = open('src/data/projects.ts').read()
for slug, legacy in re.findall(r"slug:\s*'([^']+)'.*?legacyUrl:\s*'([^']+)'", src, re.S):
    page = os.path.join(C, 'pages', legacy.rstrip('/').split('/')[-1] + '.html')
    f = f'src/data/case-studies/{slug}.json'
    if not os.path.exists(page) or not os.path.exists(f): continue
    s = open(page).read()
    grids = []
    for g in re.split(r'<div class="grid--main', s)[1:]:
        mx = re.search(r'data-grid-max-images="([^"]*)"', g)
        mx = re.sub(r'\s', '', mx.group(1)) if mx else ''
        grids.append((int(mx) if mx.isdigit() else None, len(re.findall(r'data-width="\d+" data-height="\d+"', g))))
    d = json.load(open(f))
    gal = [b for b in d['blocks'] if b['type'] == 'gallery']
    if [n for _, n in grids] != [len(b['items']) for b in gal]: continue
    changed = False
    for (mx, _), b in zip(grids, gal):
        if mx and b.get('cols') != mx: b['cols'] = mx; changed = True
    if changed:
        json.dump(d, open(f, 'w'), indent=1, ensure_ascii=False)
        print(slug, [b.get('cols') for b in gal])
