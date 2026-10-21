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
# where each circle's dotted line ends on the upright beetle (fractions of its box): antler, front leg, body, back leg
AIM = [(.30, .16), (.72, .40), (.30, .62), (.66, .84)]
PINS = ''.join(f'<a class="pin {"l" if k % 2 == 0 else "r"}" href="#{i}" data-fx="{AIM[k][0]}" data-fy="{AIM[k][1]}" style="top:{10 + k * 23}%"><b>{num}</b><span>{n}</span></a>'
               for k, (i, n, num) in enumerate(TABS))

P = [{'t': p['t'], 'x': p['x'], 'd': p['d'], 'imgs': ['../' + s for s in p['imgs']]} for p in LB.PROJECTS]
FIELDS = LB.FIELDS
TILES = ''.join(f'<button type="button" class="tile" data-p="{n}"><img src="../{p["imgs"][0]}" alt="" loading="lazy">'
                f'<span class="cap"><b>{LB.esc(p["t"])}</b><small>smaller text example</small></span></button>'
                for n, p in enumerate(LB.PROJECTS))
ARW, ARE = LB.compass('W', 26), LB.compass('E', 26)


def section(i, name, num, body):
    """a page: its title sticks under the header while you scroll through it and is pushed up by the next page's title"""
    return (f'<section class="pg" id="{i}"><h2 class="ttl"><b>{name.replace("&", "<em>&amp;</em>")}</b> <i>[{num}]</i></h2>'
            f'<div class="body">{body}</div></section>')


# ---------- downloads & links: client information (the four PDFs) and the 15 links with their logos ----------
LATIN = ('Saepissime igitur mihi de amicitia cogitanti maxime illud considerandum videri solet, utrum propter imbecillitatem atque inopiam '
         'desiderata sit amicitia, ut dandis recipiendisque meritis quod quisque minus per se ipse posset, id acciperet ab alio vicissimque redderet.')
PDFS = ['Why use an Architect', 'From Idea to Finish', 'Costs of Building', 'Partners in the Process']
LINKS = [('https://ost.zt.at/', 'downloads-imgImage.webp', 'zt: Kammer Ost', 'Ziviltechniker:innen Wien, Niederösterreich &amp; Burgenland [Ö]'),
         ('https://arb.org.uk/', 'downloads-imgImage1.webp', 'arb', 'Architects Registration Board of the United Kingdom [UK]'),
         ('https://www.wien.gv.at/wohnen/baupolizei/', 'downloads-imgRectangle329.webp', 'MA 37 – Baupolizei', 'Baubehörde der Stadt Wien [W]'),
         ('https://www.rauchfangkehrer.wien/', 'downloads-imgRectangle332.webp', 'Rauchfangkehrer', 'Wiener Rauchfangkehrer [Ö]'),
         ('https://www.azw.at/', 'downloads-imgRectangle331.webp', 'Az W', 'Architekturzentrum Wien [Ö]'),
         ('https://www.nextroom.at/', 'downloads-imgImage2.webp', 'next room', 'Verein für Architektur, Wien [Ö]'),
         ('https://www.wohnfonds.wien.at/', 'downloads-imgImage3.webp', 'wohnfonds_wien', 'Fonds für Wohnbau und Stadterneuerung [Ö]'),
         ('https://www.oib.or.at/', 'downloads-imgRectangle333.webp', 'OIB', 'Österreichisches Institut für Bautechnik [Ö]'),
         ('https://www.austrian-standards.at/', 'downloads-imgRectangle335.webp', 'Austrian Standards', 'Österreichische Organisation für Standardisierung und Innovation [Ö]'),
         ('https://www.oegfa.at/', 'downloads-imgRectangle334.webp', 'ÖGFA', 'Österreichische Gesellschaft für Architektur [Ö]'),
         ('https://www.gbstern.at/', 'downloads-imgRectangle345.webp', 'GB* Gebietsbetreuungen', 'Service-Einrichtung der Stadt Wien [Ö]'),
         ('https://www.kleingaertner.at/', 'downloads-imgRectangle346.webp', 'Kleingärtner', 'Zentralverband der Kleingärtner und Siedler Österreichs [Ö]'),
         ('https://www.bda.gv.at/', 'downloads-imgRectangle336.webp', 'Bundesdenkmalamt', 'Bundesdenkmalamt Österreich [Ö]'),
         ('https://www.ig-architektur.at/', 'downloads-imgRectangle338.webp', 'IG Architektur', 'Interessensgemeinschaft der Architekturschaffenden [Ö]'),
         ('https://www.wien.gv.at/stadtentwicklung/flaechenwidmung/', 'downloads-imgRectangle337.webp', 'MA 21 A/B', 'Stadtteilplanung und Flächenwidmung, Wien [W]')]
DOWNLOADS = ('<p class="lab first">INFORMATION FOR CLIENTS</p><p class="intro">' + LATIN + '</p><ul class="pdfs">'
             + ''.join(f'<li><img src="../img/pdf.svg" alt="PDF"><span>dd – {t}<small>PDF follows</small></span></li>' for t in PDFS)
             + '</ul><p class="lab">LINKS FOR CLIENTS</p><p class="intro">' + LATIN + '</p><div class="links">'
             + ''.join(f'<a class="lk" href="{u}" target="_blank" rel="noopener"><span class="lg"><img src="../img/{im}" alt="" loading="lazy"></span>'
                       f'<b>{n}</b><small>{d}</small></a>' for u, im, n, d in LINKS)
             + '</div>')

# ---------- bits & bats: the 21 pictures with their captions (tall ones span two rows); a tap opens them full screen ----------
BITS = [('bits-imgImage.webp', 0, 'The DILLON Shelf Plans'), ('p-drawing-grille.webp', 1, 'dd - NEW LOGO &amp; IDENTITY'),
        ('p-pocket-watch.webp', 0, 'INTERIOR COURTYARDS'), ('p-barriers-night.webp', 0, 'MIRROR BALL &amp; DISCO HALLS'),
        ('p-cages-night.webp', 0, 'SKI SLOPES IN SUMMER'), ('bits-imgImage3.webp', 0, 'PAPPI IN THE MIRROR'),
        ('p-plastic-sheet.webp', 0, 'dd - OUR OLD LOGO'), ('p-section-grey.webp', 0, 'AIDA - THE BEST COFFEE CHAIN'),
        ('bits-imgImage6.webp', 0, 'PAINT IT BLACK'), ('bits-imgImage7.webp', 0, 'CAFE PRÜCKEL...THE GHOSTS OF'),
        ('p-scaffolding.webp', 1, 'Hr. KARL SCHWANZER'), ('bits-imgImage9.webp', 0, 'BOLLOCKS BOLLOCKS!...Goat*'),
        ('p-streaks-white-blue.webp', 1, 'dd - NEW BUSINESS CARDS'), ('bits-imgImage11.webp', 0, 'VERTICAL ACCESS or STAIRS'),
        ('p-tower-drawing-blue.webp', 0, 'MUSEUMS QUARTIER'), ('bits-imgImage13.webp', 0, 'MMEEELLLAAA'),
        ('bits-imgImage14.webp', 0, 'MEESHHHA'), ('bits-imgImage15.webp', 0, 'THE “DUDE” IN VENICE'),
        ('bits-imgImage16.webp', 0, 'A. N. HARKESS'), ('p-streaks-orange.webp', 0, 'LIGHT AT THE END OF THE TUNNEL'),
        ('p-akh-crate.webp', 1, 'WHO IS THIS GUY?')]
BITSHTML = ('<div class="bgrid">' + ''.join(
    f'<button type="button" class="tile bt{" tall" if t else ""}" data-b="{k}"><img src="../img/{im}" alt="" loading="lazy">'
    f'<span class="cap"><b>{c}</b><small>smaller text example</small></span></button>' for k, (im, t, c) in enumerate(BITS)) + '</div>')
BIMGS = ['../img/' + im for im, t, c in BITS]
BCAPS = [c.replace('&amp;', '&') for im, t, c in BITS]


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


US = ('<p class="lab first">PARTNERSHIP</p><p class="firm"><b>dasein-design</b> [architecture+design] [Wien]<br><span>» Jan.’03 – bis dato</span></p>'
      + ''.join(partner(p) for p in PARTNERS)
      + '<p class="lab">OFFICE</p><p class="addr"><b>dasein-design</b><br>Neulerchenfelderstrasse 42/6<br>A-1160 Wien · Austria · EU</p>'
      '<div class="mapw"><div class="map" id="map"></div><div class="mz"><button type="button" id="zin" aria-label="zoom in">' + SEARCH.ZOOM_IN + '</button><button type="button" id="zout" aria-label="zoom out">' + SEARCH.ZOOM_OUT + '</button><button type="button" id="zhome" aria-label="back to the start view">' + SEARCH.ZOOM_HOME + '</button></div></div>'
      '<p class="mapl"><a href="https://www.openstreetmap.org/?mlat=48.211431&amp;mlon=16.333964#map=18/48.211431/16.333964">open the map</a></p>')

HTML = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>dasein-design · phone preview</title>
<link rel="stylesheet" href="../fonts.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<style>
:root{{--red:#e30613;--lime:rgba(205,255,62,.86);--green:#a5e35a;--grey:#ebebeb;--line:#c4c4c4;--dot:#b8b8b8;--hp:1px;--head:118px;--side:0px;--ttl:44px}}
/* logo on the side: a narrow strip down the left with the mark and the name, the header only holds the tabs */
.side{{--side:42px}}
.sidebar{{display:none}}
.side .sidebar{{display:flex;position:fixed;left:0;top:0;bottom:0;width:var(--side);z-index:21;background:#fff;border-right:1px dashed var(--line);
  flex-direction:column;align-items:center;padding:calc(env(safe-area-inset-top,0px) + 10px) 0 14px;text-decoration:none;color:var(--red)}}
.sidebar img{{width:28px;height:28px;flex:none}}
.sidebar span{{margin-top:14px;writing-mode:vertical-rl;transform:rotate(180deg);font-size:27px;line-height:1;white-space:nowrap}}
.sidebar b{{font-weight:700}}
.side .row1 .logo{{display:none}}
/* all on the side: the mark and name in one narrow column, the four tabs running down a second one; no bar across the top */
.side.rail{{--side:78px}}
.side.rail .sidebar{{width:40px}}
.side.rail .sidebar span{{font-size:25px}}
.side.rail header{{left:40px;right:auto;top:0;bottom:0;width:38px;padding:calc(env(safe-area-inset-top,0px) + 6px) 4px 6px;border-bottom:0;border-right:1px dashed var(--line)}}
.side.rail .row1{{min-height:0;height:0}}
.side.rail nav{{display:flex;flex-direction:column;height:100%;margin:0;gap:6px}}
.side.rail .tab{{flex:1;height:auto;writing-mode:vertical-rl;transform:rotate(180deg);padding:4px 0;font-size:14px;gap:4px}}
.side.rail .stage{{height:calc(100svh - 64px)}}
.side.rail .hint{{padding-bottom:30px}}
.side.rail .note{{position:fixed;right:6px;bottom:calc(env(safe-area-inset-bottom,0px) + 6px);z-index:30;background:rgba(255,255,255,.94);padding:2px 6px;border:1px dotted var(--dot)}}
.side header{{left:var(--side)}}
.side main{{padding-left:var(--side)}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth;scroll-padding-top:var(--head)}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:#fff;color:#000;font:400 15px/1.35 Calibri,Carlito,sans-serif;-webkit-text-size-adjust:100%}}
a{{color:inherit}}
/* header: logo, then the five tabs in two rows (3 + 2) */
header{{position:fixed;left:0;right:0;top:0;z-index:20;background:#fff;padding:calc(env(safe-area-inset-top,0px) + 8px) max(10px,env(safe-area-inset-right,0px)) 8px max(10px,env(safe-area-inset-left,0px));
  border-bottom:1px dashed var(--line)}}
.row1{{display:flex;align-items:center}}
.side .row1{{min-height:14px}}
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
/* every page: its title sticks just under the header and is pushed up by the next page's title as that one arrives */
.pg{{position:relative;min-height:calc(100svh - var(--head));border-bottom:1px dashed var(--line)}}
.ttl{{position:sticky;top:var(--head);z-index:10;margin:0;height:var(--ttl);display:flex;align-items:center;gap:6px;padding:0 10px;background:#fff;
  border-bottom:1px dashed var(--line);font-weight:400;font-size:27px;line-height:1;white-space:nowrap;color:rgba(0,0,0,.8)}}
.ttl b{{font-weight:700}} .ttl em{{font-style:normal;font-weight:300;color:var(--red)}} .ttl i{{font-style:normal;color:var(--red);font-size:21px}}
.body{{min-width:0;padding:12px 10px 28px}}
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
.pin b{{display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:#bfbfbf;font-weight:400;font-size:13.5px;
  box-shadow:inset 0 0 0 1px #000;transition:background .15s}}
.pin span{{font-size:12px;line-height:1.15;background:rgba(255,255,255,.85);padding:1px 3px}}
/* thin dotted leader lines from the circles to the beetle, as on the desktop start page */
.leads{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}}
.leads path{{fill:none;stroke:#3a3c37;stroke-width:1;stroke-dasharray:1 2.2}}
.leads .tip{{stroke-dasharray:none;stroke-linecap:round;stroke-linejoin:round}}
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
p.lab:not(.first){{margin-top:22px;padding-top:12px;border-top:1px dotted var(--dot)}}
.mapw{{position:relative;z-index:0;isolation:isolate;margin:10px 0 0}}
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
.note button{{border:0;background:none;padding:0 2px;font:inherit;color:#888;letter-spacing:inherit}}
.note button[aria-pressed="true"]{{color:var(--red);text-decoration:underline}}
/* downloads & links */
.intro{{margin:0 0 8px;font-size:14px;line-height:1.45;color:#333}}
.pdfs{{list-style:none;margin:10px 0 0;padding:0}}
.pdfs li{{display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px dotted var(--dot)}}
.pdfs img{{width:26px;height:auto}}
.pdfs span{{font-size:15px}} .pdfs small{{display:block;font-size:11px;color:#999;letter-spacing:.04em}}
.links{{display:grid;grid-template-columns:1fr 1fr;gap:14px 10px;margin-top:12px}}
.lk{{display:flex;flex-direction:column;text-decoration:none;-webkit-tap-highlight-color:transparent}}
.lg{{display:flex;align-items:center;justify-content:center;aspect-ratio:3/2;background:#fff;position:relative}}
.lg img{{max-width:80%;max-height:70%;object-fit:contain}}
.lg::after{{content:"";position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(to right,var(--dot) 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,repeating-linear-gradient(to right,var(--dot) 0 1px,transparent 1px 3px) left bottom/100% 1px no-repeat,
  repeating-linear-gradient(to bottom,var(--dot) 0 1px,transparent 1px 3px) left top/1px 100% no-repeat,repeating-linear-gradient(to bottom,var(--dot) 0 1px,transparent 1px 3px) right top/1px 100% no-repeat}}
.lk b{{margin-top:5px;font-size:13.5px;color:var(--red)}} .lk small{{font-size:11.5px;line-height:1.25;color:#555}}
.lk:active .lg{{background:var(--green)}}
/* bits & bats: two columns, the tall pictures over two rows */
.bgrid{{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:calc((100vw - var(--side) - 28px) / 2 * .9);grid-auto-flow:dense;gap:8px}}
.bgrid .tile{{aspect-ratio:auto;height:100%}}
.bgrid .tall{{grid-row:span 2}}
/* one picture full screen, swipe to the next */
#iv .photos img{{height:72svh}}
.ivcap{{padding:10px 14px 30px;color:var(--red);font-size:17px;font-weight:700}}
.ivcap small{{display:block;margin-top:4px;color:#888;font-weight:400;font-size:12px;letter-spacing:.06em}}
</style>
</head>
<body>
<script>/* three versions: logo and tabs all down the side (default) · logo on the side, tabs on top · logo and tabs across the top
   ?logo=rail / side / top, remembered on this phone */
(function(){{ let m='rail'; try{{ m=new URLSearchParams(location.search).get('logo')||localStorage.getItem('ddlogo2')||'rail'; }}catch(e){{}}
  if(m!=='top') document.body.classList.add('side'); if(m==='rail') document.body.classList.add('rail'); }})();</script>
<a class="sidebar" href="#start" aria-label="dasein-design, start"><img src="../img/m-mark.png" alt=""><span>dasein<b>-design</b></span></a>
<header>
<div class="row1"><a class="logo" href="#start" aria-label="dasein-design, start"><img src="../img/m-mark.png" alt=""><span>dasein<b>-design</b></span></a><span class="note">preview · <button type="button" data-logo="rail">all side</button>/<button type="button" data-logo="side">logo side</button>/<button type="button" data-logo="top">top</button> · <a href="../">full site</a></span></div>
<nav>{TABHTML}</nav>
</header>
<main>
<section class="pg" id="start"><div class="stage"><div class="beetle" id="beetle"><div class="whole"></div>{PIECES}</div><svg class="leads" id="leads" aria-hidden="true"></svg>{PINS}</div>
<p class="hint">tap a number or the menu</p></section>
{section("us", "us & contact", "01", US)}
{section("projects", "projects", "02", '<div class="grid">' + TILES + '</div>')}
{section("downloads", "downloads & links", "03", DOWNLOADS)}
{section("bits", "bits & bats", "04", BITSHTML)}
</main>
<dialog id="lb" aria-labelledby="lt">
<div class="top"><div class="cnt"><button type="button" id="pp" aria-label="previous project">{ARW}</button><span id="lk"></span><button type="button" id="np" aria-label="next project">{ARE}</button></div>
<button type="button" class="x" id="lx" aria-label="close"><svg viewBox="0 0 16 16" fill="none"><path d="M2 2L14 14M14 2L2 14"/></svg></button></div>
<div class="photos" id="ph"></div><div class="dots" id="dots"></div>
<div class="txt"><h2 id="lt"></h2><div id="tx"></div><dl id="dl"></dl></div>
<div class="nav2"><button type="button" id="pp2">{ARW}previous project</button><button type="button" id="np2">next project{ARE}</button></div>
</dialog>
<dialog id="iv" aria-label="bits &amp; bats">
<div class="top"><div class="cnt"><span id="ik"></span></div>
<button type="button" class="x" id="ix" aria-label="close"><svg viewBox="0 0 16 16" fill="none"><path d="M2 2L14 14M14 2L2 14"/></svg></button></div>
<div class="photos" id="iph"></div><div class="ivcap" id="icap"></div>
</dialog>
<script>
(function(){{
  /* logo switch */
  const B=document.body;
  const setLogo=m=>{{ B.classList.toggle('side',m!=='top'); B.classList.toggle('rail',m==='rail'); try{{ localStorage.setItem('ddlogo2',m); }}catch(e){{}}
    document.querySelectorAll('[data-logo]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.logo===m))); }};
  const fitHead=()=>document.documentElement.style.setProperty('--head',(B.classList.contains('rail')?0:document.querySelector('header').offsetHeight)+'px');
  /* dotted leader lines: from the inner side of each circle across, then up or down onto the beetle, with a small arrowhead */
  const stage=document.querySelector('.stage'), leads=document.getElementById('leads'), btl=document.getElementById('beetle');
  function drawLeads(){{
    const S=stage.getBoundingClientRect(), Bt=btl.getBoundingClientRect(); let h='';
    stage.querySelectorAll('.pin').forEach(p=>{{
      const c=p.querySelector('b').getBoundingClientRect(), left=p.classList.contains('l');
      const sx=(left?c.right+4:c.left-4)-S.left, sy=c.top+c.height/2-S.top;
      const tx=Bt.left+Bt.width*p.dataset.fx-S.left, ty=Bt.top+Bt.height*p.dataset.fy-S.top, d=ty>sy?1:-1, a=4;
      h+=`<path d="M${{sx}} ${{sy}}H${{tx}}V${{ty-d*1}}"/><path class="tip" d="M${{tx-a*.8}} ${{ty-d*a}}L${{tx}} ${{ty}}L${{tx+a*.8}} ${{ty-d*a}}"/>`;
    }});
    leads.innerHTML=h;
  }}
  const relayout=()=>{{ fitHead(); requestAnimationFrame(drawLeads); }};
  addEventListener('resize',relayout);
  document.querySelectorAll('[data-logo]').forEach(b=>b.addEventListener('click',()=>{{ setLogo(b.dataset.logo); relayout(); }}));
  setLogo(B.classList.contains('rail')?'rail':B.classList.contains('side')?'side':'top'); relayout();
  /* bits & bats: one picture full screen, swipe to the next */
  const BI={json.dumps(BIMGS)}, BC={json.dumps(BCAPS)}, iv=document.getElementById('iv'), iph=document.getElementById('iph');
  const tw=n=>String(n).padStart(2,'0');
  iph.innerHTML=BI.map(s=>'<img src="'+s+'" alt="" loading="lazy">').join('');
  const ishow=()=>{{ const k=Math.round(iph.scrollLeft/iph.clientWidth); document.getElementById('ik').innerHTML='bits &amp; bats <b>'+tw(k+1)+'</b> / '+tw(BI.length);
    document.getElementById('icap').innerHTML=BC[k].replace(/&/g,'&amp;')+'<small>smaller text example</small>'; }};
  iph.addEventListener('scroll',ishow,{{passive:true}});
  document.querySelectorAll('.bt').forEach(t=>t.addEventListener('click',()=>{{ iv.showModal(); iph.scrollLeft=+t.dataset.b*iph.clientWidth; ishow(); }}));
  document.getElementById('ix').onclick=()=>iv.close();
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
  document.querySelectorAll('.tile[data-p]').forEach(t=>t.addEventListener('click',()=>{{ show(+t.dataset.p); lb.showModal(); }}));
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
