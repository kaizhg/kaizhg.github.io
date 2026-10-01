#!/usr/bin/env python3
"""The site's content lives in content/<slug>/project.md next to that project's pictures.
This script turns those files into what the site builds from (src/data/case-studies/*.json
and src/data/projects.json), and once did the reverse to create them.

  python3 scripts/content.py build            # content/*/project.md -> src/data/...
  python3 scripts/content.py build <slug>     # one project
  python3 scripts/content.py export           # (one-off) old JSON + media -> content/

project.md syntax: see docs/submitting-a-project.md
"""
import glob, html as htmllib, json, os, re, shutil, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(SITE, 'content')
DATA = os.path.join(SITE, 'src', 'data', 'case-studies')
PROJECTS_JSON = os.path.join(SITE, 'src', 'data', 'projects.json')
IMG_EXT = ('.jpg', '.jpeg', '.png')
CREDIT_KEYS = [  # label -> how it is written in the credits block (the page parses these back)
    ('Course', r'^course$'), ('Instructor', r'^instructors?$'), ('Duration', r'^(project )?duration$'),
    ('Team', r'^(team( members?)?|project team)$'), ('Role', r'^(my )?role$'),
    ('Thanks', r'^(spe(?:a)?cial )?thanks$'), ('For', r'^(for|client)$'),
    ('With', r'^(advisors?|collaborators?|contributors?)$'),
]
KEY_RE = re.compile(r'(Course|Instructors?|Project Duration|Duration|Team members?|Project team|Team|My Role|Role|Spe(?:a)?cial Thanks|Thanks|For|Client|Advisors?|Collaborators?|Contributors?)\s*:')


# ---------------------------------------------------------------- html <-> markdown-ish
def inline_to_md(s):
    s = re.sub(r'^\s*<br\s*/?>', '', s)  # a break at the very start says nothing
    s = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f'[{m.group(2)}]({m.group(1)})', s, flags=re.S)
    s = re.sub(r'<strong>(.*?)</strong>', r'**\1**', s, flags=re.S)
    s = re.sub(r'\s*<br\s*/?>\s*', '\\\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    return htmllib.unescape(s).strip()


def md_to_inline(s):
    s = htmllib.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s, flags=re.S)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\\\n\s*', '<br>', s)
    return s.strip()


def html_to_md(h):
    """A text block's html -> lines of markdown (headings and paragraphs)."""
    out = []
    for tag, body in re.findall(r'<(h2|h3|p)>(.*?)</\1>', h, flags=re.S):
        t = inline_to_md(body)
        if not t:
            continue
        out.append(('## ' if tag == 'h2' else '### ' if tag == 'h3' else '') + t)
    if not out and inline_to_md(h):
        out.append(inline_to_md(h))
    return out


def md_to_html(lines):
    parts = []
    for line in lines:
        if line.startswith('## '):
            parts.append(f'<h2>{md_to_inline(line[3:])}</h2>')
        elif line.startswith('### '):
            parts.append(f'<h3>{md_to_inline(line[4:])}</h3>')
        else:
            parts.append(f'<p>{md_to_inline(line)}</p>')
    return ''.join(parts)


# ---------------------------------------------------------------- credits
def parse_credits(h):
    """credits block html -> ({label: [values]}, [other lines])"""
    text = re.sub(r'<[^>]+>', '\n', h.replace('</p><p>', '\n').replace('<br>', '\n'))
    text = htmllib.unescape(text)
    text = KEY_RE.sub(lambda m: '\n' + m.group(0), text)
    facts, rest, cur = {}, [], None
    for raw in text.split('\n'):
        line = raw.strip()
        if not line:
            continue
        m = re.match(r'^([A-Za-z][A-Za-z ]{1,20}?)\s*:\s*(.*)$', line)
        key = next((lab for lab, rx in CREDIT_KEYS if m and re.match(rx, m.group(1).strip(), re.I)), None)
        if key:
            cur = facts.setdefault(key, [])
            if m.group(2).strip():
                cur.append(m.group(2).strip())
        elif cur is not None:
            cur.append(line)
        else:
            rest.append(line)
    return facts, rest


def credits_html(facts, rest):
    ps = [f'<p>{htmllib.escape(l, quote=False)}</p>' for l in rest]
    for key, vals in facts.items():
        ps.append('<p>' + htmllib.escape(f'{key}: ' + '<br>'.join(vals), quote=False).replace('&lt;br&gt;', '<br>') + '</p>')
    return ''.join(ps)


# ---------------------------------------------------------------- front matter (tiny YAML subset)
def dump_fm(d):
    lines = []
    for k, v in d.items():
        if v is None or v == '' or v == [] or v == {}:
            continue
        if isinstance(v, dict):
            lines.append(f'{k}:')
            for kk, vv in v.items():
                if isinstance(vv, list):
                    if len(vv) == 1:
                        lines.append(f'  {kk}: {q(vv[0])}')
                    else:
                        lines.append(f'  {kk}:')
                        lines += [f'    - {q(x)}' for x in vv]
                else:
                    lines.append(f'  {kk}: {q(vv)}')
        elif isinstance(v, list):
            lines.append(f'{k}:')
            lines += [f'  - {q(x)}' for x in v]
        else:
            lines.append(f'{k}: {q(v)}')
    return '---\n' + '\n'.join(lines) + '\n---\n'


def q(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    return json.dumps(s, ensure_ascii=False) if re.search(r'^[\s\[\]{}#&*!|>\'"%@`]|: |#|^-|^\d+$|^(true|false|null)$|\s$', s) else s


def parse_fm(text):
    """The small YAML subset dump_fm writes: scalars, one level of nested keys, and lists."""
    m = re.match(r'^---\n(.*?)\n---\n?', text, re.S)
    if not m:
        return {}, text
    d = {}
    section = None  # name of the open nested key (dict or list)
    subkey = None   # name of the open key inside the nested dict (for its list)
    for raw in m.group(1).split('\n'):
        if not raw.strip() or raw.strip().startswith('#'):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if indent == 0:
            k, _, v = line.partition(':')
            k, v = k.strip(), v.strip()
            if v == '':
                d[k] = {}
                section, subkey = k, None
            else:
                d[k] = unq(v)
                section = subkey = None
        elif indent == 2:
            if line.startswith('- '):
                if not isinstance(d[section], list):
                    d[section] = []
                d[section].append(unq(line[2:]))
            else:
                k, _, v = line.partition(':')
                k, v = k.strip(), v.strip()
                d[section][k] = unq(v) if v != '' else []
                subkey = k
        else:  # indent 4: list under a nested key
            if line.startswith('- '):
                d[section][subkey].append(unq(line[2:]))
    return d, text[m.end():]


def unq(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        return json.loads(s)
    if s in ('true', 'false'):
        return s == 'true'
    if re.fullmatch(r'-?\d+', s):
        return int(s)
    return s


# ---------------------------------------------------------------- export (old JSON -> content/)
def export():
    from PIL import Image
    src_ts = open(os.path.join(SITE, 'src', 'data', 'projects.ts')).read()
    cut = src_ts.index('export const archive')
    pat = r"\{\s*slug: '([^']+)',\s*title: '([^']+)',\s*year: (\d+),\s*discipline: '(\w+)',\s*summary: '([^']*)'(?:,\s*context: '([^']*)')?,\s*legacyUrl: '([^']+)'"
    entries = [(*e, '') for e in re.findall(pat, src_ts[:cut])] + [(*e, 'true') for e in re.findall(pat, src_ts[cut:])]
    pos = {'selected': 0, 'archive': 0}
    for slug, title, year, disc, summary, context, legacy, arch in entries:
        group = 'archive' if arch else 'selected'
        pos[group] += 1
        d = json.load(open(os.path.join(DATA, slug + '.json')))
        folder = os.path.join(CONTENT, slug)
        os.makedirs(folder, exist_ok=True)
        n = [0]
        renamed = {}

        def take(block, name=None):
            """copy a media file into the folder under its new name; return the new file name"""
            old = block['src']
            if old in renamed:
                return renamed[old]
            if old.startswith('/media/'):
                path = os.path.join(SITE, 'public', old.lstrip('/'))
            else:
                path = os.path.join(SITE, 'src', 'assets', 'work', old)
            ext = os.path.splitext(path)[1].lower().replace('.jpeg', '.jpg')
            if name is None:
                n[0] += 1
                name = f'{slug}_{n[0]:02d}'
            new = name + ext
            shutil.copy2(path, os.path.join(folder, new))
            if block['type'] == 'video' and block.get('poster'):
                shutil.copy2(os.path.join(SITE, 'public', block['poster'].lstrip('/')), os.path.join(folder, name + '.jpg'))
            renamed[old] = new
            return new

        def same_image(a, b):
            if not a or not b or a['type'] != 'image' or b['type'] != 'image':
                return False
            if (a['width'], a['height']) != (b['width'], b['height']):
                return False
            pa = os.path.join(SITE, 'src', 'assets', 'work', a['src']); pb = os.path.join(SITE, 'src', 'assets', 'work', b['src'])
            ia = Image.open(pa).convert('L').resize((32, 32)); ib = Image.open(pb).convert('L').resize((32, 32))
            diff = sum(abs(x - y) for x, y in zip(ia.getdata(), ib.getdata())) / 1024
            return diff < 4

        fm = {'title': title, 'year': int(year), 'summary': summary, 'context': context or None,
              'group': group, 'position': pos[group], 'discipline': disc, 'legacy': legacy}
        if d.get('cover'):
            fm['cover'] = take(d['cover'], f'{slug}_cover')
        if d.get('hover'):
            fm['hover'] = take(d['hover'], f'{slug}_hover')
        if d.get('heroInline'):
            fm['hero'] = 'inline'
        elif d.get('hero') and not same_image(d['hero'], d.get('cover')):
            fm['hero'] = take(d['hero'], f'{slug}_hero')
        if slug == 'briota-iospro':
            fm['deck'] = True
        body = []
        blocks = d['blocks']
        prev_text = False
        leading = True  # credits are lifted into the front matter only while they open the page
        for b in blocks:
            is_text = b['type'] == 'text'
            if is_text and b.get('kind') == 'credits' and leading:
                facts, rest = parse_credits(b['html'])
                fm.setdefault('credits', {}).update(facts)
                if rest:
                    fm['credits_notes'] = fm.get('credits_notes', []) + rest
                prev_text = False
                continue
            leading = False
            lines = block_to_md(b, take)
            if is_text and prev_text and not lines[0].startswith(('#', '[')):
                body.append('...')
            body += lines + ['']
            prev_text = is_text
        md = dump_fm(fm) + '\n' + '\n'.join(body).rstrip() + '\n'
        open(os.path.join(folder, 'project.md'), 'w').write(md)
        print(f'{slug:24s} {len(blocks):3d} blocks  media {n[0]:3d}')


def hint(b):
    return (' ' + b['layout']) if b.get('layout') else ''


def media_md(b, take):
    name = take(b)
    cap = f' "{b["caption"]}"' if b.get('caption') else ''
    return f'![]({name}{cap})'


def block_to_md(b, take):
    t = b['type']
    if t == 'text':
        lines = html_to_md(b['html'])
        lay = b.get('layout') or b.get('kind')
        first = re.sub(r'^#+ ', '', lines[0])
        if lay == 'quote':
            return ['# ' + first]
        if lay == 'section':
            return ['[section] ' + first]
        out = []
        for l in lines:  # one paragraph per entry, blank lines between
            out += [l, '']
        out.pop()
        if b.get('layout'):
            out[-1] += ' {' + b['layout'] + '}'
        return out
    if t in ('image', 'loop'):
        return [media_md(b, take) + hint(b)]
    if t == 'video':
        name = take(b)
        return [f'[video{" audio" if b.get("audio") else ""}{hint(b)}] {name}']
    if t == 'youtube':
        return [f'[youtube{(" start=" + str(b["start"])) if b.get("start") else ""}] https://www.youtube.com/watch?v={b["id"]}']
    if t == 'gallery':
        head = '[gallery' + hint(b) + (f' cols={b["cols"]}' if b.get('cols') else '') + ']'
        items = []
        for it in b['items']:
            name = take(it)
            items.append(name + (f' "{it["caption"]}"' if it.get('caption') else ''))
        return [head + ' ' + ' '.join(items)]
    if t == 'row':
        cols = b['columns']
        simple = all(len(c['blocks']) == 1 and c['blocks'][0]['type'] in ('image', 'loop') for c in cols) and \
            all(abs(c['flex'] - cols[0]['flex']) < 0.03 for c in cols) and not b.get('layout')
        if simple:
            return [' | '.join(block_to_md(c['blocks'][0], take)[0] for c in cols)]
        head = '[row' + hint(b) + (' ' + ' '.join(f'{c["flex"]:g}' for c in cols) if any(abs(c['flex'] - 1 / len(cols)) > 0.03 for c in cols) else '') + ']'
        out = [head]
        for c in cols:
            for k, g in enumerate(c['blocks']):
                if k:
                    out.append('')
                out += block_to_md(g, take)
            out.append('|')
        out[-1] = '[/row]'
        return out
    raise ValueError(t)


# ---------------------------------------------------------------- build (content/ -> src/data)
def media_block(folder, slug, name, caption=None):
    from PIL import Image
    path = os.path.join(folder, name)
    if not os.path.exists(path):
        raise FileNotFoundError(f'{slug}: {name} is referenced in project.md but not in content/{slug}/')
    ext = os.path.splitext(name)[1].lower()
    if ext in IMG_EXT:
        w, h = Image.open(path).size
        b = {'type': 'image', 'src': f'{slug}/{name}', 'width': w, 'height': h}
    elif ext == '.mp4':
        w, h = video_size(path)
        b = {'type': 'loop', 'src': f'/media/{slug}/{name}', 'width': w, 'height': h}
    else:
        raise ValueError(f'{slug}: unsupported media {name}')
    if caption:
        b['caption'] = caption
    return b


def video_size(path):
    import subprocess
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                          '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    w, h = out.split(',')[:2]
    return int(w), int(h)


def has_audio(path):
    import subprocess
    return bool(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index',
                                '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip())


MEDIA_RE = re.compile(r'!\[\]\(([^\s)"]+)(?:\s+"([^"]*)")?\)')
LAYOUT_WORDS = r'(?:full|wide-[lrc]|half-[lr]|narrow-[lrc]|third-[lr]|small-[lcr]|tri-[abc]|text-[lr]|beside-[lr]|intro|quote|section|credits|grid[2-5]|strip|stack|carousel|flow|justified|stagger|pull)'
HINT_RE = re.compile(r'\s+((?:' + LAYOUT_WORDS + r')(?:\s+' + LAYOUT_WORDS + r')*)$')


def parse_media_line(line, folder, slug):
    """'![](a.jpg "cap") half-l' -> block"""
    m = MEDIA_RE.match(line.strip())
    if not m:
        return None
    rest = line.strip()[m.end():]
    b = media_block(folder, slug, m.group(1), m.group(2))
    hm = HINT_RE.match(' ' + rest.strip()) if rest.strip() else None
    if rest.strip() and not hm:
        raise ValueError(f'{slug}: cannot read "{rest.strip()}" after {m.group(1)}')
    if hm:
        b['layout'] = hm.group(1)
    return b


def parse_items(s, folder, slug):
    items = []
    for name, cap in re.findall(r'(\S+?\.(?:jpg|jpeg|png|mp4))(?:\s+"([^"]*)")?', s):
        items.append(media_block(folder, slug, name, cap or None))
    return items


DIRECTIVE_RE = re.compile(r'\[(gallery|video|youtube|row|/row|section)\b')


def parse_lines(lines, folder, slug, allow_rows=True):
    """Lines of project.md body (or of one row column) -> blocks.
    A text block is a heading plus the paragraphs after it (blank line = new paragraph);
    '...' or any picture / directive ends it."""
    blocks, block, para = [], [], None

    def end_para():
        nonlocal para
        if para:
            block.append('\n'.join(para))
        para = None

    def flush():
        nonlocal block
        end_para()
        if block:
            blocks.append(text_block(block))
        block = []

    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            end_para(); i += 1; continue
        if s == '...':
            flush(); i += 1; continue
        if s.startswith('[row'):
            if not allow_rows:
                raise ValueError(f'{slug}: a row inside a row')
            flush()
            m = re.match(r'\[row((?:\s+' + LAYOUT_WORDS + r')*)((?:\s+[\d.]+)*)\]$', s)
            if not m:
                raise ValueError(f'{slug}: bad row line: {s}')
            cols, cur = [], []
            i += 1
            while i < len(lines) and lines[i].strip() != '[/row]':
                if lines[i].strip() == '|':
                    cols.append(cur); cur = []
                else:
                    cur.append(lines[i])
                i += 1
            cols.append(cur)
            i += 1
            flex = [float(x) for x in m.group(2).split()] if m.group(2).strip() else [1 / len(cols)] * len(cols)
            row = {'type': 'row', 'columns': [{'flex': round(f, 4), 'blocks': parse_lines(c, folder, slug, False)} for f, c in zip(flex, cols)]}
            if m.group(1).strip():
                row['layout'] = m.group(1).strip()
            blocks.append(row)
            continue
        if MEDIA_RE.match(s) and ' | ' in s:
            flush()
            parts = [p.strip() for p in s.split(' | ')]
            blocks.append({'type': 'row', 'columns': [{'flex': round(1 / len(parts), 4), 'blocks': [parse_media_line(p, folder, slug)]} for p in parts]})
            i += 1
            continue
        if MEDIA_RE.match(s) or DIRECTIVE_RE.match(s) and not s.startswith('[section'):
            flush()
            blocks.append(parse_block_line(s, folder, slug))
            i += 1
            continue
        if s.startswith('[section] '):
            flush()
            blocks.append({'type': 'text', 'kind': 'section', 'layout': 'section', 'html': f'<h2>{md_to_inline(strip_hint(s[10:]))}</h2>'})
            i += 1
            continue
        if s.startswith('# '):
            flush()
            blocks.append({'type': 'text', 'kind': 'quote', 'layout': 'quote', 'html': f'<h2>{md_to_inline(strip_hint(s[2:]))}</h2>'})
            i += 1
            continue
        if s.startswith(('## ', '### ')):
            end_para()
            if any(not p.startswith('#') for p in block):  # a heading after paragraphs opens a new block
                flush()
            para = [s]
            i += 1
            continue
        if para is None:
            para = [s]
        else:
            para.append(s)
        i += 1
    flush()
    return blocks


def strip_hint(s):
    return re.sub(r'\s*\{[^}]*\}\s*$', '', s)


def build_one(slug):
    folder = os.path.join(CONTENT, slug)
    text = open(os.path.join(folder, 'project.md')).read()
    fm, body = parse_fm(text)
    blocks = parse_lines(body.split('\n'), folder, slug)

    data = {'slug': slug, 'legacy': fm.get('legacy', ''), 'hero': None, 'locked': False, 'blocks': blocks}
    if fm.get('cover'):
        data['cover'] = media_block(folder, slug, fm['cover'])
    if fm.get('hover'):
        data['hover'] = media_block(folder, slug, fm['hover'])
    if fm.get('hero') == 'inline':
        data['heroInline'] = True
    elif fm.get('hero'):
        data['hero'] = media_block(folder, slug, fm['hero'])
    elif data.get('cover'):
        data['hero'] = dict(data['cover'])
    if fm.get('credits') or fm.get('credits_notes'):
        facts = {k: (v if isinstance(v, list) else [v]) for k, v in (fm.get('credits') or {}).items()}
        notes = fm.get('credits_notes') or []
        data['blocks'].insert(0, {'type': 'text', 'kind': 'credits', 'html': credits_html(facts, notes if isinstance(notes, list) else [notes])})
    project = {'slug': slug, 'title': fm['title'], 'year': int(fm['year']), 'discipline': fm.get('discipline', 'ID'),
               'summary': fm.get('summary', ''), 'context': fm.get('context'), 'archive': fm.get('group') == 'archive',
               'position': int(fm.get('position', 999)), 'legacyUrl': fm.get('legacy', '')}
    return data, project, bool(fm.get('deck'))


def text_block(parts):
    lines = []
    for p in parts:
        p = re.sub(r'(?<!\\)\n', ' ', p)  # soft-wrapped lines join; a trailing backslash keeps a line break
        m = re.match(r'(.*?)\s*\{(' + LAYOUT_WORDS + r'(?:\s+' + LAYOUT_WORDS + r')*)\}$', p, re.S)
        if m:
            p, lay = m.group(1), m.group(2)
        else:
            lay = None
        lines.append((p, lay))
    layout = next((l for _, l in reversed(lines) if l), None)
    b = {'type': 'text', 'html': md_to_html([p for p, _ in lines])}
    if layout:
        b['layout'] = layout
    return b


def parse_block_line(s, folder, slug):
    s = s.strip()
    if MEDIA_RE.match(s):
        return parse_media_line(s, folder, slug)
    m = re.match(r'\[gallery((?:\s+' + LAYOUT_WORDS + r')*)(?:\s+cols=(\d))?\]\s*(.*)$', s)
    if m:
        g = {'type': 'gallery', 'items': parse_items(m.group(3), folder, slug)}
        if m.group(1).strip():
            g['layout'] = m.group(1).strip()
        if m.group(2):
            g['cols'] = int(m.group(2))
        return g
    m = re.match(r'\[video(\s+audio)?((?:\s+' + LAYOUT_WORDS + r')*)\]\s*(\S+)$', s)
    if m:
        name = m.group(3)
        path = os.path.join(folder, name)
        w, h = video_size(path)
        stem = os.path.splitext(name)[0]
        b = {'type': 'video', 'src': f'/media/{slug}/{name}', 'poster': f'/media/{slug}/{stem}.jpg', 'width': w, 'height': h,
             'audio': bool(m.group(1)) or has_audio(path)}
        if m.group(2).strip():
            b['layout'] = m.group(2).strip()
        return b
    m = re.match(r'\[youtube(?:\s+start=(\d+))?\]\s*(\S+)$', s)
    if m:
        vid = re.search(r'(?:v=|youtu\.be/|embed/)([\w-]{6,})', m.group(2))
        b = {'type': 'youtube', 'id': vid.group(1) if vid else m.group(2)}
        if m.group(1):
            b['start'] = int(m.group(1))
        return b
    raise ValueError(f'{slug}: cannot read line: {s}')


def build(only=None):
    sys.path.insert(0, os.path.join(SITE, 'scripts'))
    import plan_layout as pl  # kinds (photo / white / logo / small) and automatic layouts
    projects = []
    for folder in sorted(glob.glob(os.path.join(CONTENT, '*'))):
        slug = os.path.basename(folder)
        if not os.path.exists(os.path.join(folder, 'project.md')):
            continue
        data, project, deck = build_one(slug)
        if only is None or slug == only:
            blocks = data['blocks']
            pl.tag(blocks)
            if deck:
                for b in blocks:
                    if b['type'] == 'image':
                        b['kind'] = 'white'
            blocks = pl.merge_runs(blocks)
            pl.auto(blocks)
            data['blocks'] = blocks
            json.dump(data, open(os.path.join(DATA, slug + '.json'), 'w'), indent=1, ensure_ascii=False)
            print(f'{slug:24s} {len(blocks):3d} blocks')
        projects.append(project)
    projects.sort(key=lambda p: (p['archive'], p['position'], p['year'] * -1))
    for p in projects:
        p.pop('position')
        if not p['context']:
            p.pop('context')
        if not p['archive']:
            p.pop('archive')
    json.dump(projects, open(PROJECTS_JSON, 'w'), indent=1, ensure_ascii=False)
    print(f'{len(projects)} projects -> src/data/projects.json')


def sheets(only=None):
    """content/<slug>/_sheet.jpg: every picture and clip of the project with its file name,
    so a project can be discussed by name without opening the files."""
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    import subprocess
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 13)
    except Exception:
        font = ImageFont.load_default()
    cell, pad, cols = 220, 14, 5
    for folder in sorted(glob.glob(os.path.join(CONTENT, '*'))):
        slug = os.path.basename(folder)
        if only and slug != only:
            continue
        names = os.listdir(folder)
        stems = {f[:-4] for f in names if f.endswith('.mp4')}
        files = sorted(f for f in names if f.lower().endswith(IMG_EXT + ('.mp4',)) and not f.startswith('_')
                       and not (f.endswith('.jpg') and f[:-4] in stems))  # a video's poster still is not a picture of its own
        if not files:
            continue
        rows = (len(files) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * (cell + pad) + pad, rows * (cell + 34 + pad) + pad), '#f4f4f2')
        draw = ImageDraw.Draw(sheet)
        for k, f in enumerate(files):
            x = pad + (k % cols) * (cell + pad); y = pad + (k // cols) * (cell + 34 + pad)
            path = os.path.join(folder, f)
            try:
                if f.endswith('.mp4'):
                    tmp = '/tmp/_sheet_frame.jpg'
                    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', '0.5', '-i', path, '-frames:v', '1', '-vf', 'scale=440:-2', tmp], check=True)
                    im = Image.open(tmp).convert('RGB')
                else:
                    im = Image.open(path); im.draft('RGB', (cell * 2, cell * 2)); im = ImageOps.exif_transpose(im).convert('RGBA')
                    bg = Image.new('RGBA', im.size, '#ffffff'); im = Image.alpha_composite(bg, im).convert('RGB')
                im.thumbnail((cell, cell))
                sheet.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
            except Exception as e:
                draw.text((x, y), f'? {e}'[:30], fill='#c00', font=font)
            draw.rectangle([x - 1, y - 1, x + cell, y + cell], outline='#d6d6d2')
            label = f + ('  ▶' if f.endswith('.mp4') else '')
            draw.text((x, y + cell + 8), label, fill='#111', font=font)
        sheet.save(os.path.join(folder, '_sheet.jpg'), quality=82)
        print(f'{slug:24s} {len(files):3d} files -> _sheet.jpg')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'build'
    if cmd == 'export':
        export()
    elif cmd == 'sheets':
        sheets(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        build(sys.argv[2] if len(sys.argv) > 2 else None)
