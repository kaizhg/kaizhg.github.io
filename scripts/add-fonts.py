"""Convert Neue Montreal font files to woff2 and place them where Base.astro expects them.

Usage: python3 scripts/add-fonts.py <folder with the .otf/.ttf/.woff2 files>

Looks for Light, Regular, Italic, Semibold and Extrabold (Pangram Pangram's naming) and
writes public/fonts/NeueMontreal-{Light,Regular,Italic,Semibold,Extrabold}.woff2.
Needs: pip install fonttools brotli
"""
import glob, os, re, shutil, sys
from fontTools.ttLib import TTFont

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public', 'fonts')
os.makedirs(OUT, exist_ok=True)
WANT = {
    'Light': re.compile(r'-light(?!italic)', re.I),
    'Regular': re.compile(r'-regular', re.I),
    'Italic': re.compile(r'-italic', re.I),
    'Semibold': re.compile(r'-semibold(?!italic)', re.I),
    'Extrabold': re.compile(r'-extrabold(?!italic)', re.I),
}
files = [f for f in glob.glob(os.path.join(SRC, '**', '*'), recursive=True) if f.lower().endswith(('.otf', '.ttf', '.woff2', '.woff'))]
for name, rx in WANT.items():
    match = next((f for f in files if rx.search(os.path.basename(f))), None)
    dest = os.path.join(OUT, f'NeueMontreal-{name}.woff2')
    if not match:
        print(f'{name:8s} not found')
        continue
    if match.lower().endswith('.woff2'):
        shutil.copy(match, dest)
    else:
        font = TTFont(match)
        font.flavor = 'woff2'
        font.save(dest)
    print(f'{name:8s} <- {os.path.basename(match)}  ({os.path.getsize(dest) // 1024} KB)')
