"""Phone preview of the dasein-design site: phone/index.html (its own address; the desktop site is untouched).

Fixed header: logo mark + wordmark, then the five tabs in two rows (3 + 2), current page in yellow-lime.
Start page: the beetle stands upright (img/m-bug-up.webp, head and antlers at the top) and arrives as
square-cut collage pieces that land apart, pause and lock - like the desktop - with the five numbered
circles beside it (tap to go). Projects: a narrow strip on the left with the vertical title, tiles in two
columns, tap opens a full-screen pop-up: swipe through the photos, title, text, details, previous / next.
The other pages are placeholders for now. Run from tools/:  python3 phone.py
"""
import json
import os
import random
from PIL import Image
import lightbox as LB
import search as SEARCH

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
OUT = os.path.join(ROOT, 'phone', 'index.html')

# ---------- upright beetle cut into square pieces (percent of its box, so it scales with the screen) ----------
bug = Image.open(os.path.join(ROOT, 'img/m-bug-up.webp')).convert('RGBA')
BW, BH = bug.size
alpha = bug.getchannel('A').load()
rnd = random.Random(7)
pieces = []


def split(x0, y0, x1, y1, d=0):
    w, h = x1 - x0, y1 - y0
    big = max(w, h)
    if big < 120 or (big < 230 and rnd.random() < .3) or d > 12:
        hits = sum(1 for x in range(int(x0), int(x1), 4) for y in range(int(y0), int(y1), 4) if alpha[min(BW - 1, x), min(BH - 1, y)] > 100)
        if hits >= 25:
            pieces.append((int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0)))
        return
    f = rnd.uniform(.3, .7)
    if w >= h:
        m = round(x0 + w * f); split(x0, y0, m, y1, d + 1); split(m, y0, x1, y1, d + 1)
    else:
        m = round(y0 + h * f); split(x0, y0, x1, m, d + 1); split(x0, m, x1, y1, d + 1)


split(0, 0, BW, BH)
CX, CY = BW / 2, BH / 2


def pc(v, tot):
    return f'{v / tot * 100:.3f}%'


PIECES = ''.join(
    f'<i class="bp" data-dx="{(x + w / 2 - CX) / BW * 2:.3f}" data-dy="{(y + h / 2 - CY) / BH * 2:.3f}" style="left:{pc(x, BW)};top:{pc(y, BH)};width:{pc(w, BW)};height:{pc(h, BH)};'
    f'background-size:{BW / w * 100:.2f}% {BH / h * 100:.2f}%;background-position:{(x / (BW - w) * 100) if BW != w else 0:.3f}% {(y / (BH - h) * 100) if BH != h else 0:.3f}%"></i>'
    for x, y, w, h in pieces)

# ---------- four sections: "us & our services" and "contact" are one page on the phone (trial, 21 Oct) ----------
TABS = [('us', 'us & contact', '01'), ('projects', 'projects', '02'), ('downloads', 'downloads & links', '03'),
        ('bits', 'bits & bats', '04')]
TABHTML = ''.join(f'<a class="tab" href="#{i}" data-pg="{i}"><span>{n}</span> <small>[{k}]</small></a>' for i, n, k in TABS)
# circles beside the beetle: left and right, top to bottom
PINS = ''.join(f'<a class="pin {"l" if k % 2 == 0 else "r"}" href="#{i}" style="top:{10 + k * 23}%"><b>{num}</b><span>{n}</span></a>'
               for k, (i, n, num) in enumerate(TABS))

P = [{'t': p['t'], 'x': p['x'], 'd': p['d'], 'imgs': ['../' + s for s in p['imgs']]} for p in LB.PROJECTS]
FIELDS = LB.FIELDS
TILES = ''.join(f'<button type="button" class="tile" data-p="{n}"><img src="../{p["imgs"][0]}" alt="" loading="lazy">'
                f'<span class="cap"><b>{LB.esc(p["t"])}</b><small>smaller text example</small></span></button>'
                for n, p in enumerate(LB.PROJECTS))
ARW, ARE = LB.compass('W', 26), LB.compass('E', 26)


def placeholder(i, name, num):
    return (f'<section class="pg" id="{i}"><div class="vt"><span><b>{name.replace("&", "<em>&amp;</em>")}</b> <i>[{num}]</i></span></div>'
            f'<div class="body"><p class="soon">The phone version of <b>{name}</b> follows. '
            f'<a href="../#{i}">Open this page on the full site</a></p></div></section>')


# ---------- us & contact: the partnership, the two partners (CV folds open), the office with the map ----------
PARTNERS = [
    dict(role='Architect', first='Steuart', last='J Mackenzie HARRISON', q='BArch MArch ARB', tel='+43 (0)699 1941 9240', mail='steuart@dasein-design.net',
         extra='Sprachen: Englisch [Muttersprache] &amp; Deutsch [B2]',
         cv=[('Professional', ['2019 ZT: Arch+Ing, Bundeskammer der ZiviltechnikerInnen, Österreich [EU]',
                               '2004 ARB: Architects Registration Board of the United Kingdom [UK]',
                               '2004 RIAS: Royal Incorporation of Architects in Scotland [SCO]']),
             ('Academic', ['Mackintosh School of Architecture, Glasgow School of Art &amp; Glasgow University',
                           '1994 Master of Architecture [M. Arch]', '1993 Diploma of Architecture [Dip. Arch]',
                           '1992 RIBA Part II · 1989 RIBA Part I', '1989 Bachelor of Architecture [B. Arch]']),
             ('Akademische Tätigkeit', ['Mär.’02 – Aug.’17 » TU Wien, Institut für Architektur &amp; Entwerfen [E253/1]: Universitätslektor, Studio &amp; MA/BA Tutor',
                                        'Sep.’06 – Aug.’12 &amp; Mar.’14 – Sep.’14 » New Design University, St. Pölten: co-Leiter, Major Project Tutor, Leiter des Internationalen Büros',
                                        'Gastkritiker: Universität Belgrad (Jul.’09), Ryerson University, Toronto (Dez.’08)',
                                        'Berater: NDU St. Pölten – Curricula / Akkreditierung (2003–04, Jun.’19)']),
             ('Berufliche Tätigkeiten', ['1989 – 2005 Mitarbeit in diversen Architekturbüros in Wien, London &amp; Glasgow, darunter Atelier Ernst Hoffmann, Büro Geiswinkler, Atelier Artec, Büro Hagmüller, Tim Bushe Associates, E.C. Riach Architects'])]),
    dict(role='Architekt', first='Cuong', last='TRAN-VIET', q='BArch DipArch', tel='+43 (0)676 4822 464', mail='cuong@dasein-design.net', extra='',
         cv=[('Professional', ['2010 ZT: Arch+Ing, Bundeskammer der ZiviltechnikerInnen, Österreich [EU]',
                               '2005 ARB: Architects Registration Board of the United Kingdom [UK]']),
             ('Academic', ['Sep.’00 – Jun.’02 » Bartlett School of Architecture, UCL, London – Dip. Arch',
                           '2002 RIBA Part II · 1998 RIBA Part I',
                           'Okt.’96 – Jun.’98 » Mackintosh School of Architecture, Glasgow – B. Arch',
                           'Okt.’90 – Dez.’95 » Technische Universität Wien, Fakultät Architektur']),
             ('Berufliche Tätigkeiten', ['Jan.’21 – Mai.’21 » Franz und Sue Architekten, Wien',
                                         'Sep.’19 – Mai.’20 » BWM Architekten, Wien',
                                         'Mar.’10 – Aug.’19 » BEHF Architects, Wien',
                                         'Jun.’99 – Feb.’10 » Aedas, Ian Simpson, David Morley, Arthur Collin &amp; Gregory Phillips, London'])])]


def partner(p):
    cv = ''.join(f'<h4>{h}</h4><ul>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>' for h, xs in p['cv'])
    tel = p['tel'].replace(' ', '').replace('(0)', '')
    return (f'<article class="who"><p class="role">» {p["role"]}</p><h3>{p["first"]} <b>{p["last"]}</b></h3><p class="q">{p["q"]}</p>'
            f'<p class="kt"><a href="tel:{tel}">{p["tel"]}</a><br><a href="mailto:{p["mail"]}">{p["mail"]}</a></p>'
            + (f'<p class="ex">{p["extra"]}</p>' if p['extra'] else '')
            + f'<details><summary>CV</summary>{cv}</details></article>')


US = ('<section class="pg" id="us"><div class="vt"><span><b>us <em>&amp;</em> contact</b> <i>[01]</i></span></div><div class="body">'
      '<p class="lab">PARTNERSHIP</p><p class="firm"><b>dasein-design</b> [architecture+design] [Wien]<br><span>» Jan.’03 – bis dato</span></p>'
      + ''.join(partner(p) for p in PARTNERS)
      + '<p class="lab">OFFICE</p><p class="addr"><b>dasein-design</b><br>Neulerchenfelderstrasse 42/6<br>A-1160 Wien · Austria · EU</p>'
      '<div class="mapw"><div class="map" id="map"></div><div class="mz"><button type="button" id="zin" aria-label="zoom in">' + SEARCH.ZOOM_IN + '</button><button type="button" id="zout" aria-label="zoom out">' + SEARCH.ZOOM_OUT + '</button><button type="button" id="zhome" aria-label="back to the start view">' + SEARCH.ZOOM_HOME + '</button></div></div>'
      '<p class="mapl"><a href="https://www.openstreetmap.org/?mlat=48.211431&amp;mlon=16.333964#map=18/48.211431/16.333964">open the map</a></p>'
      '</div></section>')

HTML = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>dasein-design · phone preview</title>
<link rel="stylesheet" href="../fonts.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<style>
:root{{--red:#e30613;--lime:rgba(205,255,62,.86);--green:#a5e35a;--grey:#ebebeb;--line:#c4c4c4;--dot:#b8b8b8;--hp:1px;--head:118px}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth;scroll-padding-top:var(--head)}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:#fff;color:#000;font:400 15px/1.35 Calibri,Carlito,sans-serif;-webkit-text-size-adjust:100%}}
a{{color:inherit}}
/* header: logo, then the five tabs in two rows (3 + 2) */
header{{position:fixed;left:0;right:0;top:0;z-index:20;background:#fff;padding:calc(env(safe-area-inset-top,0px) + 8px) max(10px,env(safe-area-inset-right,0px)) 8px max(10px,env(safe-area-inset-left,0px));
  border-bottom:1px dashed var(--line)}}
.row1{{display:flex;align-items:center}}
.logo{{display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--red);height:34px}}
.logo img{{width:30px;height:30px}}
.logo span{{font-size:27px;line-height:1;letter-spacing:-.01em}}
.logo b{{font-weight:700}}
nav{{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:8px}}
.tab{{display:flex;align-items:center;justify-content:center;gap:3px;height:28px;padding:0 4px;background:var(--grey);text-decoration:none;
  font-size:13.5px;white-space:nowrap;outline:1px dashed #fff;outline-offset:-1px;-webkit-tap-highlight-color:transparent;transition:background .15s}}
.tab small{{font-size:9px}}
.tab:active{{background:var(--green)}}
.tab.cur{{background:var(--lime);font-weight:700}}
.tab.cur small{{font-weight:400}}
main{{padding-top:var(--head)}}
/* every page: a narrow strip on the left with the vertical title, the content beside it */
.pg{{position:relative;display:flex;min-height:calc(100svh - var(--head));border-bottom:1px dashed var(--line)}}
.vt{{flex:none;width:44px;border-right:1px dashed var(--line);position:relative}}
.vt span{{position:sticky;top:calc(var(--head) + 12px);display:block;writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;
  font-size:30px;line-height:44px;height:max-content;margin-top:12px;color:rgba(0,0,0,.8)}}
.vt b{{font-weight:700}} .vt em{{font-style:normal;font-weight:300;color:var(--red)}} .vt i{{font-style:normal;color:var(--red);font-size:24px}}
.body{{flex:1;min-width:0;padding:12px 10px 28px}}
/* start page: the upright beetle with the five circles beside it */
#start{{display:block;min-height:calc(100svh - var(--head));overflow:clip}}
html,body{{overflow-x:clip}}
.stage{{position:relative;height:calc(100svh - var(--head) - 34px);min-height:430px;margin:0 auto}}
.beetle{{position:absolute;left:50%;top:10px;bottom:10px;aspect-ratio:{BW}/{BH};transform:translateX(-50%);max-width:52vw}}
.beetle .whole{{position:absolute;inset:0;background:url(../img/m-bug-up.webp) center/100% 100% no-repeat}}
.bp{{position:absolute;display:none;background-image:url(../img/m-bug-up.webp);background-repeat:no-repeat;will-change:transform}}
.play .bp{{display:block}} .play .whole{{visibility:hidden}}
.pin{{position:absolute;display:flex;flex-direction:column;align-items:center;gap:3px;width:25vw;max-width:110px;text-decoration:none;text-align:center;-webkit-tap-highlight-color:transparent}}
.pin.l{{left:6px}} .pin.r{{right:6px}}
.pin b{{display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:#bfbfbf;font-weight:400;font-size:19px;
  box-shadow:inset 0 0 0 1px #000;transition:background .15s}}
.pin span{{font-size:13px;line-height:1.15;background:rgba(255,255,255,.85);padding:1px 3px}}
.pin:active b{{background:var(--green);box-shadow:inset 0 0 0 1px var(--red)}}
.pin:active span{{color:var(--red)}}
.hint{{text-align:center;font-size:12px;color:#666;letter-spacing:.06em;margin:0;padding:4px 0 10px}}
/* projects: tiles in two columns */
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.tile{{position:relative;display:block;font:inherit;color:inherit;aspect-ratio:1/1;padding:0;border:0;background:#f4f4f4;overflow:hidden;cursor:pointer;-webkit-tap-highlight-color:transparent}}
.tile img{{width:100%;height:100%;object-fit:cover;display:block}}
.tile::after{{content:"";position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(to right,var(--dot) 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,repeating-linear-gradient(to right,var(--dot) 0 1px,transparent 1px 3px) left bottom/100% 1px no-repeat,
  repeating-linear-gradient(to bottom,var(--dot) 0 1px,transparent 1px 3px) left top/1px 100% no-repeat,repeating-linear-gradient(to bottom,var(--dot) 0 1px,transparent 1px 3px) right top/1px 100% no-repeat}}
.cap{{position:absolute;left:0;right:0;bottom:0;padding:4px 6px 5px;background:rgba(68,68,68,.7);color:#fff;text-align:left;line-height:1.15}}
.cap b{{display:block;font-size:11.5px}} .cap small{{font-size:10px}}
.tile:active{{outline:1px solid var(--red);outline-offset:-1px}}
.soon{{margin:20px 4px;color:#555}}
/* us & contact */
.lab{{margin:6px 0 4px;font-size:11px;letter-spacing:.12em;color:var(--red)}}
.firm{{margin:0 0 6px;font-size:16px}} .firm span{{font-size:13px;color:#666}}
.who{{margin:14px 0 0;padding:12px 0 0;border-top:1px dotted var(--dot)}}
.who .role{{margin:0;font-size:12px;color:#666}}
.who h3{{margin:2px 0 0;font-weight:400;font-size:21px;line-height:1.15;color:var(--red)}} .who h3 b{{font-weight:700}}
.who .q{{margin:2px 0 0;font-size:13px;color:#444}}
.who .kt{{margin:8px 0 0;font-size:15px;line-height:1.5}} .who .kt a{{text-decoration:none;border-bottom:1px dotted var(--dot)}}
.who .ex{{margin:6px 0 0;font-size:12.5px;color:#555}}
details{{margin:8px 0 0}}
summary{{display:inline-flex;align-items:center;gap:6px;cursor:pointer;list-style:none;font-size:13px;letter-spacing:.06em;padding:5px 12px;background:var(--grey);outline:1px dashed #fff;outline-offset:-1px}}
summary::-webkit-details-marker{{display:none}}
summary::after{{content:"+";color:var(--red)}} details[open] summary::after{{content:"–"}}
details[open] summary{{background:var(--lime)}}
details h4{{margin:12px 0 2px;font-size:13px;color:var(--red);font-weight:700}}
details ul{{margin:0;padding:0 0 0 14px;font-size:13px;line-height:1.4;color:#222}} details li{{margin:2px 0}}
.addr{{margin:0;font-size:15px;line-height:1.45}}
p.lab:not(:first-child){{margin-top:22px;padding-top:12px;border-top:1px dotted var(--dot)}}
.mapw{{position:relative;margin:10px 0 0}}
.map{{height:56svh;min-height:300px;background:#eee}}
.mz{{position:absolute;right:9px;top:9px;z-index:500;display:flex;flex-direction:column;gap:5px}}
.mz button{{width:36px;height:36px;border:0;border-radius:50%;background:none;padding:0;-webkit-tap-highlight-color:transparent}}
.mz #zhome{{margin-top:9px}}
.mz svg{{display:block;width:100%;height:100%;overflow:visible}}
.mz circle{{fill:rgba(255,255,255,.9);stroke:#e30613;stroke-width:2}}
.mz path{{fill:none;stroke:#e30613;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.mz button:active circle{{fill:var(--green)}}
.mapl{{margin:6px 0 0;font-size:12px}} .mapl a{{color:var(--red)}}
.pinH{{position:relative;width:34px;height:44px;font-size:12px}}
.pinsvg{{display:block;width:100%;height:100%;overflow:visible}}
.pinsvg .pb{{fill:#3a3c37}} .pinsvg .pw{{fill:#fff}}
.pinsvg .pr{{fill:none;stroke:#3a3c37;stroke-width:1;vector-effect:non-scaling-stroke}}
.pinsvg .pa{{fill:#4d4f4a;stroke:#1a1a1a;stroke-width:1;vector-effect:non-scaling-stroke;stroke-linejoin:round}}
.pinsvg text{{fill:#3a3c37;font:700 6.4px Calibri,Carlito,sans-serif;text-anchor:middle;dominant-baseline:central}}
.plab{{position:absolute;left:calc(100% + .35em);bottom:62%;white-space:nowrap;background:rgba(255,255,255,.92);color:#000;font:400 12px/1.25 Calibri,Carlito,sans-serif;padding:.3em .55em}}
.plab b{{font-weight:700}}
.leaflet-container{{font-family:Calibri,Carlito,sans-serif}} .leaflet-control-attribution{{font-size:10px!important}} .soon a{{color:var(--red)}}
/* project pop-up: full screen, swipe through the photos */
dialog{{position:fixed;inset:0;width:100%;height:100%;max-width:none;max-height:none;margin:0;padding:0;border:0;background:rgba(255,255,255,.96);overflow-y:auto;color:#000}}
dialog::backdrop{{background:rgba(255,255,255,.4);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}}
.top{{position:sticky;top:0;z-index:2;display:flex;align-items:center;justify-content:space-between;padding:calc(env(safe-area-inset-top,0px) + 8px) 10px 8px;background:rgba(255,255,255,.94)}}
.cnt{{display:flex;align-items:center;gap:6px;font-size:13px;color:#666;letter-spacing:.06em}}
.cnt b{{color:var(--red);font-weight:400}}
.cnt button,.x{{border:0;background:none;padding:6px;margin:-6px;display:flex}}
.x svg{{width:22px;height:22px;stroke:#000;stroke-width:1.3}}
.ar{{overflow:visible}} .ar .rg{{fill:none;stroke:#3a3c37;stroke-width:var(--hp)}} .ar .dt{{fill:#4d4f4a;stroke:#1a1a1a;stroke-width:var(--hp);stroke-linejoin:round}}
.ar text{{fill:#3a3c37;font:700 6.4px Calibri,Carlito,sans-serif;text-anchor:middle;dominant-baseline:central}} .ar .tr{{display:none}}
.photos{{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;background:#f6f6f6}}
.photos::-webkit-scrollbar{{display:none}}
.photos img{{flex:none;width:100%;height:62svh;object-fit:contain;scroll-snap-align:center}}
.pcount{{font-size:11px;color:#888;letter-spacing:.06em;padding:6px 12px 0}}
.dots{{display:flex;gap:5px;justify-content:center;padding:6px 0 0}}
.dots i{{width:6px;height:6px;border-radius:50%;background:#ccc}} .dots i.on{{background:var(--red)}}
.txt{{padding:8px 14px 30px}}
.txt h2{{margin:6px 0 0;color:var(--red);font-size:21px;line-height:1.15}}
.txt p{{margin:10px 0 0;font-size:15px;line-height:1.45;color:#222}}
.txt dl{{margin:16px 0 0;padding-top:10px;border-top:1px dotted var(--dot);display:grid;grid-template-columns:70px 1fr;gap:5px 10px;font-size:14px}}
.txt dt{{color:#888}} .txt dd{{margin:0}}
.nav2{{display:flex;justify-content:space-between;padding:6px 14px 26px}}
.nav2 button{{display:flex;align-items:center;gap:6px;border:0;background:none;font:400 12px Calibri,Carlito,sans-serif;letter-spacing:.06em;color:#666;padding:6px 0}}
.note{{margin-left:auto;align-self:flex-start;font-size:10.5px;color:#888;letter-spacing:.04em;white-space:nowrap}}
.note a{{color:var(--red)}}
</style>
</head>
<body>
<header>
<div class="row1"><a class="logo" href="#start" aria-label="dasein-design, start"><img src="../img/m-mark.png" alt=""><span>dasein<b>-design</b></span></a><span class="note">phone preview · <a href="../">full site</a></span></div>
<nav>{TABHTML}</nav>
</header>
<main>
<section class="pg" id="start"><div class="stage"><div class="beetle" id="beetle"><div class="whole"></div>{PIECES}</div>{PINS}</div>
<p class="hint">tap a number or the menu</p></section>
{US}
<section class="pg" id="projects"><div class="vt"><span><b>projects</b> <i>[02]</i></span></div><div class="body"><div class="grid">{TILES}</div></div></section>
{placeholder("downloads", "downloads & links", "03")}
{placeholder("bits", "bits & bats", "04")}
</main>
<dialog id="lb" aria-labelledby="lt">
<div class="top"><div class="cnt"><button type="button" id="pp" aria-label="previous project">{ARW}</button><span id="lk"></span><button type="button" id="np" aria-label="next project">{ARE}</button></div>
<button type="button" class="x" id="lx" aria-label="close"><svg viewBox="0 0 16 16" fill="none"><path d="M2 2L14 14M14 2L2 14"/></svg></button></div>
<div class="photos" id="ph"></div><div class="dots" id="dots"></div>
<div class="txt"><h2 id="lt"></h2><div id="tx"></div><dl id="dl"></dl></div>
<div class="nav2"><button type="button" id="pp2">{ARW}previous project</button><button type="button" id="np2">next project{ARE}</button></div>
</dialog>
<script>
(function(){{
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* current page: tab in yellow-lime, as on the desktop */
  const tabs=[...document.querySelectorAll('.tab')];
  const secs=[...document.querySelectorAll('.pg')];
  function mark(){{ const y=innerHeight*.45; let id='start'; secs.forEach(s=>{{ if(s.getBoundingClientRect().top<=y) id=s.id; }});
    tabs.forEach(t=>t.classList.toggle('cur',t.dataset.pg===id)); }}
  addEventListener('scroll',mark,{{passive:true}}); addEventListener('resize',mark); mark();
  /* the upright beetle arrives as square-cut pieces, lands apart, pauses, locks */
  const bug=document.getElementById('beetle'), ps=[...bug.querySelectorAll('.bp')], R=(a,b)=>a+Math.random()*(b-a);
  let anims=[], run=0;
  function play(){{
    if(reduce||!bug.animate) return; anims.forEach(a=>a.cancel()); const me=++run; bug.classList.add('play');
    const W=bug.offsetWidth, T=3600, LOCK=3150, SNAP=260;
    anims=ps.map(p=>{{
      const ang=R(0,Math.PI*2), dist=R(1.6,2.6)*W, r=R(-160,160), d=R(0,750), fly=R(1500,1850);
      const dx=+p.dataset.dx, dy=+p.dataset.dy, n=Math.hypot(dx,dy)||1, g=R(.025,.08)*W, k=Math.max(.55,Math.min(1,n*1.4));
      const ax=dx/n*g*k, ay=dy/n*g*k;
      return p.animate([
        {{offset:0,transform:`translate(${{Math.cos(ang)*dist}}px,${{Math.sin(ang)*dist}}px) rotate(${{r}}deg) scale(1.25)`,opacity:0,easing:'step-end'}},
        {{offset:d/T,transform:`translate(${{Math.cos(ang)*dist}}px,${{Math.sin(ang)*dist}}px) rotate(${{r}}deg) scale(1.25)`,opacity:0,easing:'cubic-bezier(.2,.7,.3,1)'}},
        {{offset:(d+fly*.15)/T,opacity:1}},
        {{offset:(d+fly)/T,transform:`translate(${{ax}}px,${{ay}}px)`,opacity:1}},
        {{offset:LOCK/T,transform:`translate(${{ax}}px,${{ay}}px)`,opacity:1,easing:'cubic-bezier(.6,0,.4,1.4)'}},
        {{offset:(LOCK+SNAP)/T,transform:'none',opacity:1}},{{offset:1,transform:'none',opacity:1}}],{{duration:T,fill:'both'}});
    }});
    Promise.all(anims.map(a=>a.finished)).then(()=>{{ if(me===run) bug.classList.remove('play'); }}).catch(()=>{{}});
  }}
  play();
  let away=false; new IntersectionObserver(es=>es.forEach(e=>{{ if(!e.isIntersecting) away=true; else if(away){{ away=false; play(); }} }}),{{threshold:.6}}).observe(document.getElementById('start'));
  /* project pop-up */
  const P={json.dumps(P)}, F={json.dumps(FIELDS)};
  const lb=document.getElementById('lb'), $=id=>document.getElementById(id), ph=$('ph'), dots=$('dots');
  const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;'), two=n=>String(n).padStart(2,'0');
  let pi=0;
  function show(n){{
    pi=(n+P.length)%P.length; const p=P[pi];
    $('lk').innerHTML='projects <b>'+two(pi+1)+'</b> / '+two(P.length);
    ph.innerHTML=p.imgs.map(s=>'<img src="'+s+'" alt="" loading="lazy">').join(''); ph.scrollLeft=0;
    dots.innerHTML=p.imgs.map((s,k)=>'<i class="'+(k?'':'on')+'"></i>').join('');
    $('lt').textContent=p.t; $('tx').innerHTML=(Array.isArray(p.x)?p.x:[p.x]).map(t=>'<p>'+esc(t)+'</p>').join('');
    $('dl').innerHTML=F.map(([k,l])=>'<dt>'+l+'</dt><dd>'+esc(p.d[k]||'–')+'</dd>').join('');
    lb.scrollTop=0;
  }}
  ph.addEventListener('scroll',()=>{{ const k=Math.round(ph.scrollLeft/ph.clientWidth); [...dots.children].forEach((d,i)=>d.classList.toggle('on',i===k)); }},{{passive:true}});
  document.querySelectorAll('.tile').forEach(t=>t.addEventListener('click',()=>{{ show(+t.dataset.p); lb.showModal(); }}));
  $('lx').onclick=()=>lb.close();
  $('pp').onclick=$('pp2').onclick=()=>show(pi-1); $('np').onclick=$('np2').onclick=()=>show(pi+1);
}})();
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" defer></script>
<script>
/* live map with the H pin; loaded last so it can never stop the page */
addEventListener('load',()=>{{ try{{
  const HOME=[48.211431,16.333964], el=document.getElementById('map');
  const map=L.map(el,{{zoomControl:false,scrollWheelZoom:false,dragging:!L.Browser.mobile,tap:false,attributionControl:true}});
  const home=a=>{{ map.setView(HOME,17,{{animate:false}}); map.panBy([Math.min(110,el.clientWidth*.28),-30],{{animate:false}}); }}; home();   /* pin left of centre so its address label fits */
  document.getElementById('zin').onclick=()=>map.zoomIn(); document.getElementById('zout').onclick=()=>map.zoomOut(); document.getElementById('zhome').onclick=()=>home();
  L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}}).addTo(map);
  map.attributionControl.setPrefix(false);
  L.marker(HOME,{{icon:L.divIcon({{className:'',iconSize:[34,44],iconAnchor:[17,44],html:'<div class="pinH"><svg class="pinsvg" viewBox="0 0 40 52" aria-hidden="true"><path class="pb" d="M20 51C14.5 40.5 2 31 2 19A18 18 0 0 1 38 19C38 31 25.5 40.5 20 51Z"/><circle class="pw" cx="20" cy="19" r="14.5"/><g transform="translate(20 19) scale(1.12)"><path class="pr" d="M-5.31 7.88A9.5 9.5 0 1 1 5.31 7.88"/><path class="pa" transform="rotate(90)" d="M5.4 0L-4.6 -4.9L-2.2 0L-4.6 4.9Z"/><text x="0" y="9.5">H</text></g></svg><div class="plab"><b>dasein-design</b><br>Neulerchenfelderstrasse 42/6<br>A-1160 Wien</div></div>'}})}}).addTo(map);
}}catch(err){{ console.warn('map not available',err); }} }});
</script>
</body>
</html>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w').write(HTML)
if __name__ == '__main__':
    print(len(pieces), 'pieces,', len(HTML) // 1024, 'KB ->', OUT)
