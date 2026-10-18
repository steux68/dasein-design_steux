"""Convert the Figma React+Tailwind exports into plain HTML fragments + optimised assets."""
import re, os, json, html, shutil
from PIL import Image, ImageDraw, ImageOps

PAGES = {'intro': 'LIntro', 'services': 'LUsOurServices01', 'projects': 'LProjects02',
         'downloads': 'LDownloadsLinks03', 'bits': 'LBitsBats04', 'contact': 'LContact05'}
# Images that are real identity documents: never published, replaced by a neutral placeholder
PRIVATE = set()  # ID-card images are now shown, at the owner's request
# ...but with document numbers, dates of birth/issue and signatures made unreadable (original pixel coordinates)
LIC = [(425, 352, 725, 394), (400, 394, 785, 424), (430, 452, 600, 494), (495, 505, 705, 598), (935, 155, 1075, 315)]
REDACT = {('services', 'imgImage'): [(350, 222, 500, 264), (350, 508, 540, 552), (390, 592, 690, 672)],
          ('services', 'imgImage1'): LIC, ('projects', 'imgImage'): LIC, ('bits', 'imgImage18'): LIC}

def redact(im, boxes):
    from PIL import ImageFilter
    im = im.copy()
    for b in boxes:
        reg = im.crop(b)
        w, h = reg.size
        reg = reg.resize((max(1, w // 14), max(1, h // 14)), Image.BILINEAR).resize((w, h), Image.BILINEAR)
        im.paste(reg.filter(ImageFilter.GaussianBlur(6)), b[:2])
    return im

OUT = 'site'
os.makedirs(f'{OUT}/img', exist_ok=True)
os.makedirs('frag', exist_ok=True)

FONT = {
    "font-['Calibri:Regular']": 'fcal-r',
    "font-['Calibri:Bold']": 'fcal-b',
    "font-['Calibri:Light']": 'fcal-l',
    "font-['Inter:Semi_Bold']": 'finter',
}

import hashlib
_SEEN = {}   # identical pictures used on several pages are stored once

def optimise(pid, name, src):
    """Return the published path for an asset: photos resized to max 1600 px and saved as WebP, duplicates shared."""
    ext = src.rsplit('.', 1)[1]
    if ext == 'svg':
        key = hashlib.md5(open(src, 'rb').read()).hexdigest()
        if key in _SEEN: return _SEEN[key]
        out = f'{OUT}/img/{pid}-{name}.svg'; shutil.copy(src, out); _SEEN[key] = out; return out
    key = hashlib.md5(open(src, 'rb').read() + repr(REDACT.get((pid, name))).encode()).hexdigest()
    if key in _SEEN: return _SEEN[key]
    im = ImageOps.exif_transpose(Image.open(src))
    if (pid, name) in REDACT:
        im = redact(im, REDACT[(pid, name)])
    if name == 'imgPdf':   # PDF download symbols in dasein-design red
        im = im.convert('RGBA'); red = Image.new('RGBA', im.size, (227, 6, 19, 255)); red.putalpha(im.getchannel('A')); im = red
    if max(im.size) > 1600:
        im.thumbnail((1600, 1600), Image.LANCZOS)
    out = f'{OUT}/img/{pid}-{name}.webp'
    if im.mode in ('RGBA', 'LA', 'P') and im.convert('RGBA').getextrema()[3][0] < 255:
        im.convert('RGBA').save(out, 'WEBP', quality=86, method=6)
    else:
        im.convert('RGB').save(out, 'WEBP', quality=82, method=6)
    _SEEN[key] = out
    return out

def jsx_to_html(t, pid):
    consts = dict(re.findall(r'const (\w+) = "(https://www\.figma\.com/api/mcp/asset/[^"]+)";', t))
    paths = {}
    for name, url in consts.items():
        ext = url.rsplit('.', 1)[1]
        paths[name] = optimise(pid, name, f'assets/{pid}/{name}.{ext}').replace(f'{OUT}/', '')
    body = t[t.index('return (') + len('return ('): t.rindex(');')]
    body = re.sub(r'\{`([^`]*)`\}', lambda m: html.escape(m.group(1), quote=False), body)
    body = re.sub(r'src=\{(\w+)\}', lambda m: f'src="{paths[m.group(1)]}"', body)
    body = body.replace('style={{ containerType: "size" }}', 'style="container-type:size"')
    body = body.replace('className=', 'class=')
    body = re.sub(r'<(div|span|p|a)(\s[^<>]*?)?\s*/>', lambda m: f'<{m.group(1)}{m.group(2) or ""}></{m.group(1)}>', body)
    for k, v in FONT.items():
        body = body.replace(k, v)
    # JSX whitespace rules: line breaks + indentation between/around tags are not text
    body = re.sub(r'>\s*\n\s*', '>', body)
    body = re.sub(r'\s*\n\s*<', '<', body)
    def unrotate(m):
        pre, h, w, rest = m.group(1), m.group(2), m.group(3), m.group(4)
        src = re.search(r'src="([^"]+)"', rest)
        if src:
            iw, ih = Image.open(f'{OUT}/{src.group(1)}').size
            if ih / iw > 3:
                return f'<div class="flex-none"><div class="{pre}h-[{w}px] relative w-[{h}px]"{rest}'
        return m.group(0)
    body = re.sub(r'<div class="-rotate-90 flex-none"><div class="([^"]*?)h-\[(\d+)px\] relative w-\[(\d+)px\]"([^>]*><img[^>]*>)', unrotate, body)
    # side-bar texture: Figma rotates the fill back, so show it upright in its 90x570 slot
    body = re.sub(r'<div class="-rotate-90 flex-none"><div class="border-\[0\.5px\] border-solid border-white h-\[90px\] relative w-\[570px\]"',
                  '<div class="flex-none"><div class="border-[0.5px] border-solid border-white h-[570px] relative w-[90px]"', body)
    # unify Figma's two blacks/greys? no: keep values exactly
    return body.strip(), paths

manifest = {}
for pid, fn in PAGES.items():
    h, paths = jsx_to_html(open(fn + '.jsx').read(), pid)
    if pid == 'services':
        # personal data kept off the public site
        h = re.sub(r'<p class="mb-0">\s*<span class="leading-\[normal\]">Geburts(datum|ort): </span>\s*<span[^>]*>[^<]*</span>\s*</p>', '', h)
        # Figma links pointed to a placeholder address; link the address that is shown
        parts = h.split('href="mailto:steux@steux.com"')
        # each address appears on an <a> and its inner <span>: 4 occurrences, Steuart's first
        addrs = ['steuart@dasein-design.net'] * 2 + ['cuong@dasein-design.net'] * 2
        h = parts[0] + ''.join(f'href="mailto:{addrs[i]}"' + p for i, p in enumerate(parts[1:]))
    if pid == 'projects':
        # "who is this guy?" spans two columns: 235-655 (420 wide), not 430, so it stops at the column edge like the rest
        for old, new in [
            ('h-[35px] left-[235px] top-[775px] w-[430px]" data-node-id="1:262"', 'h-[35px] left-[235px] top-[775px] w-[420px]" data-node-id="1:262"'),
            ('top-[792.5px] w-[427px]" data-node-id="1:263"', 'top-[792.5px] w-[417px]" data-node-id="1:263"')]:
            assert old in h, old[:40]
            h = h.replace(old, new)
    # the ID-card photos fill their frames (upright where the frame is landscape, turned where it is tall)
    def boxed(h, nid, x, y, w, hh, src):
        pat = re.compile(r'<div[^>]*data-node-id="' + re.escape(nid) + r'"[^>]*>(?:<div[^>]*>)*<img[^>]*>(?:</div>)+')
        m = pat.search(h); assert m, nid
        depth = m.group(0).count('<div')
        whole = re.match(r'(?:<div[^>]*>)+<img[^>]*>' + '</div>' * depth, m.group(0)).group(0)
        new = (f'<div class="absolute border-[0.5px] border-black border-dashed overflow-hidden" data-node-id="{nid}" data-name="IMAGE" '
               f'style="left:{x}px;top:{y}px;width:{w}px;height:{hh}px"><img alt="" class="absolute inset-0 max-w-none object-cover pointer-events-none size-full" src="{src}"></div>')
        return h.replace(whole, new, 1)
    if pid == 'services':
        h = boxed(h, '1:555', 235, 290, 200, 150, paths['imgImage'])
        h = boxed(h, '1:600', 895, 290, 200, 150, paths['imgImage1'])
    if pid == 'projects':
        h = boxed(h, '1:248', 235, 440, 420, 370, paths['imgImage'])
    if pid == 'bits':
        im = Image.open(f"{OUT}/{paths['imgImage18']}")
        rot = paths['imgImage18'].rsplit('.', 1)[0] + '-tall.' + paths['imgImage18'].rsplit('.', 1)[1]
        im.rotate(90, expand=True).save(f'{OUT}/{rot}')
        h = boxed(h, '1:78', 455, 250, 200, 370, rot)
    open(f'frag/{pid}.html', 'w').write(h)
    manifest[pid] = paths
json.dump(manifest, open('frag/manifest.json', 'w'), indent=1)
print('ok', {k: len(v) for k, v in manifest.items()})
