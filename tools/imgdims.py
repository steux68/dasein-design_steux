"""Adds explicit width / height (the picture file's own size) to every <img> that has none,
so the browser reserves the space before the picture loads (Lighthouse: "Image elements do not have explicit width and height").
CSS still decides the size on screen; the attributes only give the proportions.
apply(html, base_dir) - base_dir is the folder the page's relative img/ paths start from."""
import os, re
from PIL import Image

_cache = {}

def _size(path):
    if path in _cache: return _cache[path]
    r = None
    try:
        if path.lower().endswith('.svg'):
            t = open(path, encoding='utf-8', errors='ignore').read(2000)
            m = re.search(r'<svg[^>]*>', t, re.S); tag = m.group(0) if m else ''
            vb = re.search(r'viewBox="([-\d.\s,]+)"', tag)
            w = re.search(r'\swidth="([\d.]+)(?:px)?"', tag); h = re.search(r'\sheight="([\d.]+)(?:px)?"', tag)
            if w and h: r = (float(w.group(1)), float(h.group(1)))
            elif vb:
                v = [float(x) for x in re.split(r'[\s,]+', vb.group(1).strip())]; r = (v[2], v[3])
        else:
            with Image.open(path) as im: r = im.size
    except Exception:
        r = None
    _cache[path] = r
    return r

def _num(v): return str(int(v)) if float(v).is_integer() else ('%g' % v)

def apply(html, base_dir):
    def fix(m):
        tag = m.group(0)
        if re.search(r'\swidth=', tag) and re.search(r'\sheight=', tag): return tag
        s = re.search(r'\ssrc="([^"#?]+)"', tag)
        if not s or s.group(1).startswith(('http', 'data:')): return tag
        if s.group(1).endswith('steux.png'): return tag   # sized by max-height only: a width attribute would stretch it
        wh = _size(os.path.normpath(os.path.join(base_dir, s.group(1))))
        if not wh or not wh[0] or not wh[1]: return tag
        add = ''
        if not re.search(r'\swidth=', tag): add += ' width="%s"' % _num(wh[0])
        if not re.search(r'\sheight=', tag): add += ' height="%s"' % _num(wh[1])
        return tag[:-1].rstrip('/').rstrip() + add + '>'
    return re.sub(r'<img\b[^>]*>', fix, html)

if __name__ == '__main__':
    import sys
    for f in sys.argv[1:]:
        h = open(f).read(); n = apply(h, os.path.dirname(os.path.abspath(f))); open(f, 'w').write(n)
        print(f, 'changed' if n != h else 'unchanged')
