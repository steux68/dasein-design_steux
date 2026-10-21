"""Desktop site: the changes first made on the phone version (21 Oct 2026), applied to index.html.

Run from tools/:  python3 fromphone.py   (patches ../index.html in place; safe to run again)
build.py also calls patch() before writing, so a full rebuild keeps them.

- texts instead of the Latin placeholders (shared with the phone through texts.py)
- "dasein-design" in text always in the logo red; phone numbers green, e-mail links blue
- beetle: dotted leader lines redrawn, white in "difference" (they show over the dark beetle),
  ending in yellow dots with a black ring on legs, jaw and mouth; the circles light up yellow-lime in turn
  and send out coloured rings
- project pop-up: close drawn like the compass signs; the counter sits between previous and next at the bottom
- link logos trimmed to their edges (img/m-lg-*), with a small margin in their boxes
- menu: "about us [01]" and "contact [05]" are half tabs at the two ends
"""
import re
from texts import INTRO, BIO, INFO_TXT, LINKS_TXT, CONTACT_TXT

MARK = '<!--fromphone-->'
RED = '#e30613'


def _sub1(pat, rep, s, flags=0):
    s2, n = re.subn(pat, rep, s, count=1, flags=flags)
    assert n == 1, pat
    return s2


def _rep(a, b, s, n=1):
    assert s.count(a) >= n, a[:80]
    return s.replace(a, b)


# ---------- the beetle's leader lines: circle centre -> elbow -> end on the beetle (desktop page pixels)
LEADS = [((335, 377), (335, 420), (580, 420)),     # 01 about us -> back leg
         ((555, 744), (555, 652), (648, 652)),     # 02 projects -> back foot
         ((775, 328), None, (775, 432)),           # 03 downloads & links -> middle leg
         ((995, 692), (995, 671), (1086, 671)),    # 04 bits & bats -> lower jaw
         ((1215, 287), (1215, 524), (1005, 524))]  # 05 contact -> mouth
R = 4.5
FIGMA_LINES = ['1:225', '1:228', '26:180', '30:639', '26:181', '30:640', '26:186', '26:187']


def _leads():
    paths, dots = '', ''
    for a, m, b in LEADS:
        pts = [a] + ([m] if m else []) + [b]
        (x1, y1), (x2, y2) = pts[-2], pts[-1]   # stop the line at the dot's edge
        if x1 == x2:
            y2 = y2 - R if y2 > y1 else y2 + R
        else:
            x2 = x2 - R if x2 > x1 else x2 + R
        pts[-1] = (x2, y2)
        paths += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in pts) + '"/>'
        dots += f'<circle cx="{b[0]}" cy="{b[1]}" r="{R}"/>'
    return (f'<svg class="dlead" viewBox="0 0 1440 1024" aria-hidden="true">{paths}</svg>'
            f'<svg class="dlead dots" viewBox="0 0 1440 1024" aria-hidden="true">{dots}</svg>')


CSS = '''
/* ---- from the phone version (fromphone.py) ---- */
.dd{color:#e30613}
a[href^="tel:"]{color:#1e8e3e;text-decoration:none} a[href^="mailto:"]{color:#1a5fd0}
.plab b{color:#e30613}
/* beetle: new leader lines (the Figma ones are hidden) */
''' + ','.join(f'[data-node-id="{n}"]' for n in FIGMA_LINES) + '''{display:none!important}
.dlead{position:absolute;left:0;top:0;width:1440px;height:1024px;pointer-events:none;z-index:4;overflow:visible;mix-blend-mode:difference}
.dlead path{fill:none;stroke:#fff;stroke-width:1.2;stroke-dasharray:1.2 2.2}
.dlead.dots{mix-blend-mode:normal}
.dlead circle{fill:#ffd400;stroke:#000;stroke-width:1.2}
/* the circles light up yellow-lime in turn (01 ... 05), each sending out its two coloured rings, then turn grey again */
.hot.pin{animation:pinon 7.5s ease-in-out infinite;animation-delay:calc(var(--k) * 1.5s)}
@keyframes pinon{0%{background:#bfbfbf}3%{background:#cdff3e}17%{background:#cdff3e}20%{background:#bfbfbf}100%{background:#bfbfbf}}
.pin .cr{position:absolute;inset:-1px;border-radius:50%;border:1.6px solid var(--c1);opacity:0;pointer-events:none;
  animation:pinturn 7.5s ease-out infinite;animation-delay:calc(var(--k) * 1.5s + .3s)}
.pin .cr.c2{border-color:var(--c2);animation-delay:calc(var(--k) * 1.5s + .6s)}
@keyframes pinturn{0%{transform:scale(1);opacity:.9}15%{transform:scale(2.3);opacity:0}100%{transform:scale(2.3);opacity:0}}
.hot.pin:hover,.hot.pin:focus-visible,.hot.pin.near{animation:none}
.hot.pin.near{animation:pinpulse 1.5s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){.hot.pin,.pin .cr{animation:none}}
/* texts */
.ptx{position:absolute;font:400 12px/1.4 Calibri,Carlito,sans-serif;color:#222;margin:0}
.ptx p{margin:0 0 6px} .ptx .lab2{font-weight:700;font-size:11px;letter-spacing:.12em;color:#e30613;margin-bottom:4px}
.ptx.bio{font-size:11px;line-height:1.35} .ptx.bio p{margin-bottom:4px}
.ptx.end{font-style:italic;font-size:13px;line-height:1.45}
.ptx.end .hd{font-style:normal;margin:0 .35em}
.ptx.end .hd:first-child{margin-left:0}
/* pop-up: close like the compass signs; the counter between previous and next */
.lbx{width:24px;height:24px}
.lbx svg{width:22px;height:22px;stroke:none}
.lbx .rg{fill:none;stroke:#3a3c37;stroke-width:var(--hp)} .lbx .xx{fill:none;stroke:#1a1a1a;stroke-width:1.15;stroke-linecap:round;transition:stroke .2s}
.lbx:hover .rg,.lbx:focus-visible .rg{stroke:#e30613} .lbx:hover .xx,.lbx:focus-visible .xx{stroke:#e30613}
.lbk{display:none}
.lbm{align-items:center}
.lbm .lbkc{font:400 13px/25px Calibri,Carlito,sans-serif;color:#666;letter-spacing:.06em}
.lbm .lbkc b{color:#e30613;font-weight:400}
/* half tabs: positions not in figma.css */
.left-\\[285px\\]{left:285px} .left-\\[1265px\\]{left:1265px} .w-\\[96px\\]{width:96px}
/* link logos trimmed to their edges, with a small margin in their boxes */
img[src^="img/m-lg-"]{box-sizing:border-box;padding:6px 12px}
'''

XC = ('<svg viewBox="-12 -12 24 24" aria-hidden="true"><circle class="rg" r="9.5"/>'
      '<path class="xx" d="M-3.6 -3.6L3.6 3.6M3.6 -3.6L-3.6 3.6"/></svg>')
RINGS = [('#ffd400', '#2f8cff'), ('#2fbf4a', '#ffd400'), ('#2f8cff', '#cdff3e'), ('#e30613', '#2fbf4a'), ('#cdff3e', '#e30613')]


def _half_tabs(s):
    """in every page's menu: tab 1 = "about us [01]", left half of its column; tab 5 = "contact [05]", right half of its"""
    s, n1 = re.subn(r'h-\[25px\] left-\[235px\] (top-\[?-?\d*p?x?\]?|top-0) w-\[200px\]', r'h-[25px] left-[235px] \1 w-[100px]', s)
    s, n5 = re.subn(r'h-\[25px\] left-\[1115px\] (top-\[?-?\d*p?x?\]?|top-0) w-\[200px\]', r'h-[25px] left-[1215px] \1 w-[100px]', s)
    assert n1 == 6 and n5 == 6, (n1, n5)

    def label(name, num):
        def lab(m):
            spans = re.findall(r'<span class="([^"]*)">([^<]*)</span>', m.group(3))
            first = next(c for c, t in spans if t.strip() and t.strip() != '&amp;')
            return f'{m.group(1)}w-[96px]{m.group(2)}<span class="{first}">{name} </span><span class="{spans[-1][0]}">[{num}]</span></p>'
        return lab
    s, t1 = re.subn(r'(h-\[25px\] justify-center leading-\[0\] )left-\[335px\]([^"]*?)w-\[190px\]', r'\1left-[285px]\2w-[190px]', s)
    s, t5 = re.subn(r'(h-\[25px\] justify-center leading-\[0\] )left-\[1215px\]([^"]*?)w-\[190px\]', r'\1left-[1265px]\2w-[190px]', s)
    assert t1 == 6 and t5 == 6, (t1, t5)
    s, c1 = re.subn(r'(left-\[285px\][^"]*?)w-\[190px\](" data-node-id="[^"]+"><p[^>]*>)(.*?)</p>', label('about us', '01'), s, flags=re.S)
    s, c5 = re.subn(r'(left-\[1265px\][^"]*?)w-\[190px\](" data-node-id="[^"]+"><p[^>]*>)(.*?)</p>', label('contact', '05'), s, flags=re.S)
    assert c1 == 6 and c5 == 6, (c1, c5)
    s = _rep('style="left:235px;top:0;width:200px;height:25px" aria-label="us &amp; our services"', 'style="left:235px;top:0;width:100px;height:25px" aria-label="about us"', s)
    s = _rep('style="left:1115px;top:0;width:200px;height:25px" aria-label="contact"', 'style="left:1215px;top:0;width:100px;height:25px" aria-label="contact"', s)
    return s


def patch(s):
    if MARK in s:
        return s
    # ---- texts
    s = _sub1(r'(<p class="leading-\[normal\] mb-0">INFORMATION FOR CLIENTS</p><p class="fcal-r leading-\[normal\] mb-0">)Saepissime.*?(</p>)', r'\g<1>' + INFO_TXT + r'\2', s, re.S)
    s = _sub1(r'(<p class="leading-\[normal\] mb-0">LINKS FOR CLIENTS</p><p class="fcal-r leading-\[normal\] mb-0">)Saepissime.*?</p><p class="leading-\[normal\] mb-0">​</p><p class="fcal-r leading-\[normal\] mb-0">Amor enim.*?</p><p class="fcal-r leading-\[normal\] mb-0">Inter quos.*?(</p>)',
              r'\g<1>' + LINKS_TXT + r'\2', s, re.S)
    about = (f'<div class="ptx" style="left:235px;top:57px;width:420px"><p class="lab2">ABOUT US</p><p>{INTRO}</p></div>'
             f'<div class="ptx bio" style="left:895px;top:57px;width:420px"><p class="lab2">BIO</p>' + ''.join(f'<p>{t}</p>' for t in BIO) + '</div>')
    s = _rep('<section class="pg" id="services"><div class="bg-white relative frame">', '<section class="pg" id="services"><div class="bg-white relative frame">' + about, s)
    end = f'<div class="ptx end" style="left:235px;top:930px;width:205px">{CONTACT_TXT.replace("<br>", " ")}</div>'
    s = _rep('<section class="pg" id="contact"><div class="bg-white relative frame">', '<section class="pg" id="contact"><div class="bg-white relative frame">' + end, s)
    # ---- dasein-design in red, phone / e-mail links
    s = _rep('<p class="fcal-r leading-[normal] mb-0 text-[10px]">dasein-design [architecture+design] [Wien]</p>',
             '<p class="fcal-r leading-[normal] mb-0 text-[10px]"><b class="dd">dasein-design</b> [architecture+design] [Wien]</p>', s)
    for num, tel in (('+43 [0] 699 1941 9240', '+436991941 9240'), ('+43 [0] 676 4822 464', '+436764822464')):
        tel = tel.replace(' ', '')
        s = s.replace(f'not-italic"> {num} </span>', f'not-italic"> <a href="tel:{tel}">{num}</a> </span>')
    s = _rep('not-italic">+43 [0] 676 4822 464</span>', 'not-italic"><a href="tel:+436764822464">+43 [0] 676 4822 464</a></span>', s)
    s = _sub1(r'not-italic"> cuong</span>(<a [^>]*href="mailto:cuong@dasein-design.net"[^>]*>)<span ([^>]*)>@dasein-design.net</span></a>',
              r'not-italic"> </span>\1<span \2>cuong@dasein-design.net</span></a>', s)   # one link for the whole address
    for num, tel, mail in (('+43 (0)676 4822 464', '+436764822464', 'cuong@dasein-design.net'), ('+43 (0)699 1941 9240', '+4369919419240', 'steuart@dasein-design.net')):
        s = _rep(f'<p class="fcal-r leading-[normal] mb-0">{num}</p><p class="fcal-r leading-[normal] mb-0">{mail}</p>',
                 f'<p class="fcal-r leading-[normal] mb-0"><a href="tel:{tel}">{num}</a></p><p class="fcal-r leading-[normal] mb-0"><a href="mailto:{mail}">{mail}</a></p>', s)
    # ---- beetle: new leader lines, circles take turns
    s = _rep('<a class="hot pin" href="#services"', _leads() + '<a class="hot pin" href="#services"', s)
    k = [0]

    def pin(m):
        c1, c2 = RINGS[k[0]]
        out = f'<a class="hot pin" href="{m.group(1)}" style="{m.group(2)};--k:{k[0]};--c1:{c1};--c2:{c2}">{m.group(3)}<i class="cr"></i><i class="cr c2"></i>'
        k[0] += 1
        return out
    s = re.sub(r'<a class="hot pin" href="([^"]+)" style="([^"]+)">(\d\d)', pin, s)
    assert k[0] == 5
    s = _rep('<span class="pl r">us &amp; our services</span>', '<span class="pl r">about us</span>', s)
    # ---- pop-up
    s = _sub1(r'(<button type="button" class="lbx" id="lbx"[^>]*>)<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 2L14 14M14 2L2 14"/></svg>', r'\1' + XC, s)
    s = _rep('<span id="lbk"></span>', '', s)
    s = _sub1(r'(<div class="lbm"><button type="button" class="pp" id="lbpp">.*?</button>)', r'\1<span class="lbkc" id="lbk"></span>', s, re.S)
    # ---- logos
    import os
    for n in sorted(os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img'))):
        if n.startswith('m-lg-'):
            s = s.replace('src="img/downloads-img' + n[5:] + '"', 'src="img/' + n + '"')
    # ---- menu: half tabs at both ends
    s = _half_tabs(s)
    # ---- styles
    s = _rep('</style>', CSS + '</style>', s)
    return s.replace('</body>', MARK + '</body>', 1)


if __name__ == '__main__':
    p = '../index.html'
    html = patch(open(p).read())
    open(p, 'w').write(html)
    print('patched', p)
