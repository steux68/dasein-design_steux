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

# ---------- five pages: about us · projects · downloads & links · bits & bats · contact (contact moved to the end, 21 Oct) ----------
TABS = [('us', 'about us', '01'), ('projects', 'projects', '02'), ('downloads', 'downloads & links', '03'),
        ('bits', 'bits & bats', '04'), ('contact', 'contact', '05')]
# about us (top) and contact (bottom) are half tabs (Steuart, 21 Oct): together they take one tab's height
TABHTML = ''.join(f'<a class="tab{" half" if i in ("us", "contact") else ""}" href="#{i}" data-pg="{i}"><span>{n.replace("&", "&amp;")}</span> <small>[{k}]</small></a>' for i, n, k in TABS)
# circles beside the beetle: left and right, top to bottom (five, 21 Oct)
# where each circle's dotted line ends on the upright beetle (fractions of its box): mouth, right front leg (claw), left middle leg, right back leg
AIM = [(.51, .245), (.715, .365), (.258, .53), (.80, .605), (.31, .905)]
PINS = ''.join(f'<a class="pin {"l" if k % 2 == 0 else "r"}" href="#{i}" data-fx="{AIM[k][0]}" data-fy="{AIM[k][1]}" style="top:{10.5 + k * 17.6}%;--k:{k}"><b>{num}</b><span>{n.replace("&", "&amp;")}</span></a>'
               for k, (i, n, num) in enumerate(TABS))

P = [{'t': p['t'], 'x': p['x'], 'd': p['d'], 'imgs': ['../' + s for s in p['imgs']]} for p in LB.PROJECTS]
FIELDS = LB.FIELDS
TILES = ''.join(f'<button type="button" class="tile" data-p="{n}"><img src="../{p["imgs"][0]}" alt="" loading="lazy">'
                f'<span class="cap"><b>{LB.esc(p["t"])}</b><small>smaller text example</small></span></button>'
                for n, p in enumerate(LB.PROJECTS))
ARW, ARE = LB.compass('W', 26), LB.compass('E', 26)
# close: drawn like the compass signs (thin open circle), with a small cross in place of the arrow
XC = '<svg viewBox="-12 -12 24 24" aria-hidden="true"><circle class="rg" r="9.5"/><path class="xx" d="M-3.6 -3.6L3.6 3.6M3.6 -3.6L-3.6 3.6"/></svg>'


def section(i, name, num, body):
    """a page; it opens with a muted yellow-lime bar across, in the tab style, naming it (scrolls away with the page)"""
    return (f'<section class="pg" id="{i}" aria-label="{name} [{num}]"><div class="sbar"><b>{name.replace("&", "&amp;")}</b> <small>[{num}]</small></div>'
            f'<div class="body">{body}</div></section>')


ARN, ARS = LB.compass('N', 24), LB.compass('S', 24)
ARW2, ARE2 = LB.compass('W', 34, 'pulse'), LB.compass('E', 34, 'pulse')


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
             + ''.join(f'<a class="lk" href="{u}" target="_blank" rel="noopener"><span class="lg"><img src="../img/m-lg-{im.replace('downloads-img', '')}" alt="" loading="lazy"></span>'
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
    dict(role='Architekt', first='Cuong', last='TRAN-VIET', q='BArch DipArch', idimg='m-id-cuong.webp', idalt='Personalausweis Cuong Tran-Viet', tel='+43 (0)676 4822 464', mail='cuong@dasein-design.net', extra='',
         cv=[('Professional', ['2010 ZT: Arch+Ing, Bundeskammer der ZiviltechnikerInnen, Österreich [EU]',
                               '2005 ARB: Architects Registration Board of the United Kingdom [UK]']),
             ('Academic', ['Sep.’00 – Jun.’02 » Bartlett School of Architecture, UCL, London – Dip. Arch',
                           '2002 RIBA Part II · 1998 RIBA Part I',
                           'Okt.’96 – Jun.’98 » Mackintosh School of Architecture, Glasgow – B. Arch',
                           'Okt.’90 – Dez.’95 » Technische Universität Wien, Fakultät Architektur']),
             ('Berufliche Tätigkeiten', ['Jan.’21 – Mai.’21 » Franz und Sue Architekten, Wien',
                                         'Sep.’19 – Mai.’20 » BWM Architekten, Wien',
                                         'Mar.’10 – Aug.’19 » BEHF Architects, Wien',
                                         'Jun.’99 – Feb.’10 » Aedas, Ian Simpson, David Morley, Arthur Collin &amp; Gregory Phillips, London'])]),
    dict(role='Architect', first='Steuart', last='J Mackenzie HARRISON', q='BArch MArch ARB', idimg='m-id-steuart.webp', idalt='Führerschein Steuart J Mackenzie Harrison', tel='+43 (0)699 1941 9240', mail='steuart@dasein-design.net',
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
             ('Berufliche Tätigkeiten', ['1989 – 2005 Mitarbeit in diversen Architekturbüros in Wien, London &amp; Glasgow, darunter Atelier Ernst Hoffmann, Büro Geiswinkler, Atelier Artec, Büro Hagmüller, Tim Bushe Associates, E.C. Riach Architects'])])]


PLUS = ('<svg class="cvx" viewBox="-12 -12 24 24" aria-hidden="true"><circle class="r1" r="8"/><circle class="r2" r="8"/>'
        '<circle class="c" r="8"/><path class="v" d="M0 -4.2V4.2"/><path d="M-4.2 0H4.2"/></svg>')
# short text about the practice (draft, to be replaced by Steuart's) and the full bio (placeholder)
INTRO = ('<b class="dd">dasein-design</b> is an architecture and design partnership in Vienna, founded in 2003. '
         'We work at every scale – houses, courtyards, interiors, exhibitions, furniture and identity – looking for the simple idea that makes a place work for the people who use it.')
BIO = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
       'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
       'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.']


def partner(n, p):
    """one architect: a column of the two-column block (ID card on its grey tile, name, letters, phone, e-mail, CV button)"""
    tel = p['tel'].replace(' ', '').replace('(0)', '')
    return (f'<article class="who"><span class="idw"><img class="idc" src="../img/{p["idimg"]}" alt="{p["idalt"]} (Nummer, Geburtsdatum und Unterschrift unkenntlich)" loading="lazy"></span>'
            f'<p class="role">» {p["role"]}</p><h3>{p["first"]}<br><b>{p["last"]}</b></h3><p class="q">{p["q"]}</p>'
            f'<p class="kt"><a href="tel:{tel}">{p["tel"]}</a><a href="mailto:{p["mail"]}">{p["mail"]}</a></p>'
            f'<button type="button" class="cvb" aria-expanded="false" aria-controls="cv{n}">{PLUS}<span class="cvt">full</span><b>CV</b></button></article>')


def cvpanel(n, p):
    """the CV, opened under both columns, full width"""
    secs = p['cv'] + ([('Sprachen', [p['extra'].replace('Sprachen: ', '')])] if p['extra'] else [])
    cv = ''.join(f'<h4>{h}</h4><ul>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>' for h, xs in secs)
    return (f'<details class="cvp" id="cv{n}"><summary></summary><div class="box"><p class="lab first">CV</p>'
            f'<h3 class="cvn">{p["first"]} <b>{p["last"]}</b> <span class="q">{p["q"]}</span></h3>{cv}'
            f'<button type="button" class="cvb" aria-expanded="true" aria-controls="cv{n}">{PLUS}<span class="cvt">full</span><b>CV</b></button></div></details>')


US = ('<div class="box"><p class="lab first">PARTNERSHIP</p><p class="firm"><b class="dd">dasein-design</b> [architecture+design] [Wien]<br><span>» Jan.’03 – bis dato</span></p>'
      f'<p class="intro2">{INTRO}</p>'
      '<details class="bio"><summary>' + PLUS + '<span class="cvt">full</span><b>bio</b></summary>' + ''.join(f'<p>{t}</p>' for t in BIO) + '</details></div>'
      '<div class="duo">' + ''.join(partner(n, p) for n, p in enumerate(PARTNERS)) + '</div>'
      + ''.join(cvpanel(n, p) for n, p in enumerate(PARTNERS)))
CONTACT = ('<div class="box"><p class="lab first">OFFICE</p><p class="addr"><b class="dd">dasein-design</b><br>Neulerchenfelderstrasse 42/6<br>A-1160 Wien · Austria · EU</p>'
      '<div class="mapw"><div class="map" id="map"></div><div class="mz"><button type="button" id="zin" aria-label="zoom in">' + SEARCH.ZOOM_IN + '</button><button type="button" id="zout" aria-label="zoom out">' + SEARCH.ZOOM_OUT + '</button><button type="button" id="zhome" aria-label="back to the start view">' + SEARCH.ZOOM_HOME + '</button></div></div>'
      '<p class="mapl"><a href="https://www.openstreetmap.org/?mlat=48.211431&amp;mlon=16.333964#map=18/48.211431/16.333964">open the map</a></p></div>')

HTML = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>dasein-design · phone preview</title>
<link rel="stylesheet" href="../fonts.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<style>
:root{{--dh:repeating-linear-gradient(to right,var(--dot) 0 1px,transparent 1px 3px);--dv:repeating-linear-gradient(to bottom,var(--dot) 0 1px,transparent 1px 3px);--bar:30px;--red:#e30613;--lime:rgba(205,255,62,.86);--green:#a5e35a;--grey:#ebebeb;--line:#c4c4c4;--dot:#b8b8b8;--hp:1px;--head:118px;--side:0px;--ttl:44px}}
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
.side.rail{{--side:40px;--logoh:168px}}
/* all side: ONE narrow strip down the left - the mark and "dasein-design" (a little smaller) at the top, the four tabs below it, sharing the rest of the height */
.side.rail .sidebar{{width:var(--side);bottom:auto;height:calc(env(safe-area-inset-top,0px) + var(--logoh));padding-top:calc(env(safe-area-inset-top,0px) + 8px);padding-bottom:0;border-right:1px dashed var(--line)}}
.side.rail .sidebar img{{width:24px;height:24px}}
.side.rail .sidebar span{{margin-top:9px;font-size:20px}}
.side.rail header{{left:0;right:auto;top:calc(env(safe-area-inset-top,0px) + var(--logoh));bottom:0;width:var(--side);padding:6px 5px calc(env(safe-area-inset-bottom,0px) + 6px);border-bottom:0;border-right:1px dashed var(--line)}}
.side.rail .row1{{min-height:0;height:0}}
.side.rail nav{{display:flex;flex-direction:column;height:100%;margin:0;gap:5px}}
.side.rail .tab{{flex:1;min-height:0;height:auto;writing-mode:vertical-rl;transform:rotate(180deg);padding:3px 0;font-size:min(12.5px,1.75svh);gap:3px;overflow:hidden}}
.side.rail .tab small{{font-size:8.5px}}
/* the split first tab: two halves, 2 px apart, sharing one tab's place */
.side.rail .tab.half{{flex:.5}}   /* about us at the top and contact at the bottom are half tabs */
.side.rail .tab.half{{font-size:min(12.5px,1.6svh);gap:2px}} .side.rail .tab.half small{{font-size:min(8.5px,1.15svh)}}   /* halves keep their number: a touch smaller type on short phones */
nav .tab:last-child:nth-child(odd){{grid-column:span 2}}
.note2{{display:none}}
.side.rail .row1 .note{{display:none}}
.side.rail .note2{{display:block;text-align:center;margin:-6px 0 0;padding-bottom:8px}}
.side header{{left:var(--side)}}
.side main{{padding-left:var(--side)}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth;scroll-padding-top:calc(var(--head) + var(--bar))}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:#fff;color:#000;font:400 15px/1.35 Calibri,Carlito,sans-serif;-webkit-text-size-adjust:100%}}
a{{color:inherit}}
/* header: logo, then the five tabs in two rows (3 + 2) */
header{{position:fixed;left:0;right:0;top:0;z-index:20;background:#fff;padding:calc(env(safe-area-inset-top,0px) + 8px) max(10px,env(safe-area-inset-right,0px)) 8px max(10px,env(safe-area-inset-left,0px));
  border-bottom:1px dashed var(--line)}}
.row1{{display:flex;align-items:center}}
.side .row1{{min-height:14px}}
.logo{{flex:none;white-space:nowrap;display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--red);height:34px}}
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
main{{padding-top:calc(var(--head) + var(--bar));padding-bottom:var(--bar);padding-right:8px}}
body{{position:relative}}
/* every page */
.pg{{position:relative}}   /* pages are as tall as their content, so the white above each page bar is always the same */
/* thin white bars at the top and bottom of the screen with the N and S arrows: previous / next page */
.bar{{position:fixed;left:var(--side);right:8px;z-index:15;height:var(--bar);display:flex;align-items:center;justify-content:center;background:#fff}}
.bar.btop{{top:var(--head);border-bottom:1px dashed var(--line)}}
.bar.bbot{{bottom:0;height:calc(var(--bar) + env(safe-area-inset-bottom,0px));padding-bottom:env(safe-area-inset-bottom,0px);border-top:1px dashed var(--line)}}
.bar button{{border:0;background:none;padding:3px 24px;display:flex;-webkit-tap-highlight-color:transparent;transition:opacity .2s}}
.bar button:disabled{{opacity:.2}}
/* pulsing thin dark rings round an arrow, as on the desktop */
.ar.pulse .tr,.bar .go .tr{{display:block;fill:none;stroke:#3a3c37;stroke-width:.7;transform-box:fill-box;transform-origin:center;animation:ring 2.2s ease-out infinite}}
.ar.pulse .tr2,.bar .go .tr2{{animation-delay:1.1s}}
@keyframes ring{{0%{{transform:scale(1);opacity:.55}}100%{{transform:scale(1.7);opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.ar .tr{{animation:none!important;display:none!important}}}}
.body{{min-width:0;padding:12px 10px 0}} .pg:last-child .body{{padding-bottom:28px}}
/* guide lines down both sides, as on the desktop: a light dashed vertical line */
.rule{{position:fixed;top:0;bottom:0;width:1px;z-index:45;pointer-events:none;
  background:repeating-linear-gradient(to bottom,var(--line) 0 4px,transparent 4px 7px)}}
.rule.l{{left:calc(var(--side) - 1px)}} .rule.r{{right:7px}}
.side.rail .sidebar,.side.rail header{{border-right:0!important}}
/* section bar: same size, type and thickness as a tab in the side strip, a muted version of the lit tab's yellow-lime */
.sbar{{display:flex;align-items:center;justify-content:center;gap:4px;height:30px;margin:60px 10px 0;background:rgba(205,255,62,.42);color:rgba(0,0,0,.78);
  outline:1px dashed #fff;outline-offset:-1px;font-size:12.5px;white-space:nowrap}}
.sbar b{{font-weight:700}} .sbar small{{font-size:8.5px}}
/* start page: the upright beetle with the five circles beside it */
#start{{display:block;overflow:clip}}
html,body{{overflow-x:clip}}
.stage{{position:relative;height:calc(100svh - var(--head) - 2 * var(--bar) - 6px);min-height:430px;margin:0 auto}}
.beetle{{cursor:pointer;-webkit-tap-highlight-color:transparent;position:absolute;left:50%;top:calc(10px + 5%);bottom:0;aspect-ratio:{BW}/{BH};transform:translateX(-50%);max-width:52vw}}
.beetle .whole{{position:absolute;inset:0;background:url(../img/m-bug-up.webp) center/100% 100% no-repeat}}
.bp{{position:absolute;display:none;background-image:url(../img/m-bug-up.webp);background-repeat:no-repeat;will-change:transform}}
.play .bp{{display:block}} .play .whole{{visibility:hidden}}
/* three taps on the beetle: a red heart pops out, zooms up to fill the screen and bursts into little hearts */
.heartfx{{position:fixed;inset:0;z-index:60;pointer-events:none;overflow:hidden}}
.heartfx svg{{position:absolute;left:0;top:0;width:60px;height:60px;margin:-30px 0 0 -30px;fill:var(--red);will-change:transform,opacity}}
.heartfx .sm{{width:16px;height:16px;margin:-8px 0 0 -8px}}
.pin{{position:absolute;display:flex;flex-direction:column;align-items:center;gap:3px;width:25vw;max-width:110px;text-decoration:none;text-align:center;-webkit-tap-highlight-color:transparent}}
.pin.l{{left:6px}} .pin.r{{right:6px}}
.pin b{{display:flex;align-items:center;justify-content:center;width:23px;height:23px;border-radius:50%;background:#bfbfbf;font-weight:400;font-size:11.5px;
  box-shadow:inset 0 0 0 1px #000;transition:background .15s}}
.pin b{{position:relative}}
/* thin red rings ripple out of the circles one after another - 01, 02, 03, 04, then from the start - to show they can be tapped */
.pin b::before,.pin b::after{{content:"";position:absolute;inset:-1px;border-radius:50%;border:1.6px solid var(--c1,var(--red));opacity:0;pointer-events:none;
  animation:pinring 7.5s ease-out infinite;animation-delay:calc(var(--k) * 1.5s + .3s)}}
.pin b::after{{border-color:var(--c2,var(--red));animation-delay:calc(var(--k) * 1.5s + .6s)}}
/* in turn each circle lights up yellow-lime (as if activated), sends out its rings, then turns grey again before the next one */
.pin b{{animation:pinon 7.5s ease-in-out infinite;animation-delay:calc(var(--k) * 1.5s)}}
@keyframes pinon{{0%{{background:#bfbfbf}}3%{{background:#cdff3e}}17%{{background:#cdff3e}}20%{{background:#bfbfbf}}100%{{background:#bfbfbf}}}}
.pin:nth-of-type(1){{--c1:#ffd400;--c2:#2f8cff}} .pin:nth-of-type(2){{--c1:#2fbf4a;--c2:#ffd400}}
.pin:nth-of-type(3){{--c1:#2f8cff;--c2:#cdff3e}} .pin:nth-of-type(4){{--c1:#e30613;--c2:#2fbf4a}} .pin:nth-of-type(5){{--c1:#cdff3e;--c2:#e30613}}
@keyframes pinring{{0%{{transform:scale(1);opacity:.9}}15%{{transform:scale(2.3);opacity:0}}100%{{transform:scale(2.3);opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.pin b,.pin b::before,.pin b::after{{animation:none}}}}
.pin span{{font-size:12px;line-height:1.15;background:rgba(255,255,255,.85);padding:1px 3px}}
/* thin dotted leader lines from the circles to the beetle, as on the desktop start page */
.leads{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}}
/* the lines are white drawn in "difference": black over the white page, white where they cross the dark beetle, so they always show */
#leads{{mix-blend-mode:difference}}
.leads path{{fill:none;stroke:#fff;stroke-width:1.2;stroke-dasharray:1.2 2.2}}
/* each line ends on the beetle in a big yellow dot with a black ring */
.leads circle{{fill:#ffd400;stroke:#000;stroke-width:1.2}}
.pin:active b{{animation:none;background:var(--green);box-shadow:inset 0 0 0 1px var(--red)}}
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
/* about us & contact: every block in a dotted box, 8 px apart, like the project tiles */
.box{{margin:8px 0 0;padding:10px;background:var(--dh) left top/100% 1px no-repeat,var(--dh) left bottom/100% 1px no-repeat,var(--dv) left top/1px 100% no-repeat,var(--dv) right top/1px 100% no-repeat}}
#us .body > .box:first-child{{margin-top:0}}
.box .firm{{margin:0}}
#contact .body > .box:first-child{{margin-top:0}}
.lab{{margin:6px 0 4px;font-size:11px;font-weight:700;letter-spacing:.12em;color:var(--red)}}   /* small red subtitles, bold like the current tab */
.firm{{margin:0 0 6px;font-size:16px}} .firm span{{font-size:13px;color:#666}}
.duo{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0 0}}
.who{{min-width:0;display:flex;flex-direction:column;align-items:flex-start;padding:8px;background:var(--dh) left top/100% 1px no-repeat,var(--dh) left bottom/100% 1px no-repeat,var(--dv) left top/1px 100% no-repeat,var(--dv) right top/1px 100% no-repeat}}
/* ID card on top, filling the column (number, birth date and signature blurred) */
.who .idw{{display:block;align-self:stretch;position:relative}}   /* the ID card fills the column, no frame of its own (Steuart, 21 Oct) */
.who .idc{{display:block;width:100%;height:auto;border-radius:6px}}
.who .role{{margin:8px 0 0;font-size:11.5px;color:#666}}
.who h3,.cvn{{margin:1px 0 0;font-weight:400;font-size:15px;line-height:1.15;color:var(--red)}} .who h3 b,.cvn b{{font-weight:700}}
.who .q,.cvn .q{{margin:2px 0 0;font-size:11.5px;font-style:italic;font-weight:400;color:#555}}
.cvn .q{{margin-left:3px}}
.who .kt{{display:flex;flex-direction:column;align-items:flex-start;gap:3px;margin:auto 0 0;padding-top:7px;font-size:min(12px,3.05vw);line-height:1.35;white-space:nowrap}}
.who .kt a{{text-decoration:none;padding-bottom:1px;background:var(--dh) left bottom/100% 1px no-repeat}}
/* short text about the practice */
.intro2{{margin:8px 0 0;font-size:13.5px;line-height:1.4;color:#222}}
.bio p{{margin:8px 0 0;font-size:13.5px;line-height:1.4;color:#222}}
/* the CVs open under both columns */
.cvp > summary{{display:none}} .cvp{{margin:0}} .cvp .box{{margin-top:8px}} .cvp .cvb{{margin-top:10px}}
details,.cvb{{margin:4px 0 0}}
/* "CV (+) full CV": a red cross in a circle that sends out pulsing yellow-lime rings; open, it becomes a minus and reads "close" */
summary,.cvb{{border:0;background:none;font-family:inherit;color:inherit;display:inline-flex;align-items:center;gap:7px;cursor:pointer;list-style:none;font-size:14px;letter-spacing:.04em;padding:1px 0;-webkit-tap-highlight-color:transparent}}
summary::-webkit-details-marker{{display:none}}
summary b,.cvb b{{color:var(--red);font-weight:700;font-size:15px;margin-left:-3px}} .cvt{{color:#000;font-weight:300;font-size:13px}}
.cvx{{width:20px;height:20px;overflow:visible}}
.cvx .c{{fill:#fff;stroke:var(--red);stroke-width:1.5}} .cvx path{{stroke:var(--red);stroke-width:1.6;stroke-linecap:round}}
.cvx .r1,.cvx .r2{{fill:none;stroke:#cdff3e;stroke-width:2.2;transform-box:fill-box;transform-origin:center;animation:cvp 1.8s ease-out infinite}}
.cvx .r2{{animation-delay:.9s}}
@keyframes cvp{{0%{{transform:scale(1);opacity:.95}}100%{{transform:scale(1.9);opacity:0}}}}
details[open] > summary .cvx .v,[aria-expanded=true] .cvx .v{{display:none}} details[open] > summary .cvx .r1,details[open] > summary .cvx .r2,[aria-expanded=true] .cvx .r1,[aria-expanded=true] .cvx .r2{{display:none}}
details[open] > summary .cvt,[aria-expanded=true] .cvt{{font-size:0}} details[open] > summary .cvt::after,[aria-expanded=true] .cvt::after{{content:"close";font-size:13px}}
@media (prefers-reduced-motion:reduce){{.cvx .r1,.cvx .r2{{display:none}}}}
details h4{{margin:12px 0 2px;font-size:13px;color:var(--red);font-weight:700}}
details ul{{margin:0;padding:0 0 0 14px;font-size:13px;line-height:1.4;color:#222}} details li{{margin:2px 0}}
.addr{{margin:0;font-size:15px;line-height:1.45}}
p.lab:not(.first){{margin-top:22px;padding-top:12px;background:var(--dh) left top/100% 1px no-repeat}}
.box .lab.first{{margin-top:0}}
.mapw{{position:relative;z-index:0;isolation:isolate;margin:10px 0 0}}
.map{{height:56svh;min-height:300px;background:#eee}}
.mz{{position:absolute;right:9px;top:9px;z-index:500;display:flex;flex-direction:column;gap:5px}}
.mz button{{width:36px;height:36px;border:0;border-radius:50%;background:none;padding:0;-webkit-tap-highlight-color:transparent}}
.mz #zhome{{margin-top:9px}}
.mz svg{{display:block;width:100%;height:100%;overflow:visible}}
.mz circle{{fill:rgba(255,255,255,.9);stroke:#e30613;stroke-width:2}}
.mz path{{fill:none;stroke:#e30613;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.mz button:active circle{{fill:var(--green)}}
.mapl{{margin:6px 0 0;font-size:12px}}
/* "dasein-design" in text is always in the logo red */
.dd{{color:var(--red)}}
/* links that do something: phone numbers green (call), e-mail and web addresses blue */
a[href^="tel:"]{{color:#1e8e3e}} a[href^="mailto:"],.mapl a{{color:#1a5fd0}}
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
/* pop-ups leave the side strip (and in the other versions the header) free, so the logo and the tabs stay in reach */
dialog{{position:fixed;inset:var(--head) 8px 0 var(--side);z-index:40;width:auto;height:auto;max-width:none;max-height:none;margin:0;padding:0;border:0;background:#fff;overflow-y:auto;color:#000}}
html.dlg{{overflow:hidden}}
.top{{position:sticky;top:0;z-index:2;display:flex;align-items:center;justify-content:space-between;padding:calc(env(safe-area-inset-top,0px) + 8px) 10px 8px;background:rgba(255,255,255,.94)}}
.cnt{{display:flex;align-items:center;gap:6px;font-size:13px;color:#666;letter-spacing:.06em}}
.cnt b{{color:var(--red);font-weight:400}}
.cnt button,.x{{border:0;background:none;padding:6px;margin:-6px;display:flex}}
.x{{outline:none;-webkit-tap-highlight-color:transparent}} .x svg{{width:22px;height:22px}} .x .rg{{fill:none;stroke:#3a3c37;stroke-width:var(--hp)}} .x .xx{{fill:none;stroke:#1a1a1a;stroke-width:1.15;stroke-linecap:round}}
.ar{{overflow:visible}} .ar .rg{{fill:none;stroke:#3a3c37;stroke-width:var(--hp)}} .ar .dt{{fill:#4d4f4a;stroke:#1a1a1a;stroke-width:var(--hp);stroke-linejoin:round}}
.ar text{{fill:#3a3c37;font:700 6.4px Calibri,Carlito,sans-serif;text-anchor:middle;dominant-baseline:central}} .ar .tr{{display:none}}
.photos{{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;background:#f6f6f6}}
.phw::after{{content:"";position:absolute;inset:0;pointer-events:none;background:var(--dh) left top/100% 1px no-repeat,var(--dh) left bottom/100% 1px no-repeat,var(--dv) left top/1px 100% no-repeat,var(--dv) right top/1px 100% no-repeat}}
.photos::-webkit-scrollbar{{display:none}}
.photos img{{flex:none;width:100%;height:44svh;object-fit:contain;scroll-snap-align:center}}
/* the pop-ups fill exactly one screen; nothing scrolls up and down */
dialog[open]{{display:flex;flex-direction:column;overflow:hidden}}
dialog .top{{flex:none}}
.phw{{position:relative;flex:none;margin:0 10px}}
.phw button{{position:absolute;top:50%;margin-top:-21px;width:42px;height:42px;border:0;padding:0;border-radius:50%;background:rgba(255,255,255,.82);display:flex;align-items:center;justify-content:center;
  -webkit-tap-highlight-color:transparent;transition:opacity .2s}}
.phw .pw{{left:6px}} .phw .pe{{right:6px}}
.phw button:disabled{{opacity:0;pointer-events:none}}
.pcount{{font-size:11px;color:#888;letter-spacing:.06em;padding:6px 12px 0}}
.dots{{display:flex;gap:5px;justify-content:center;padding:6px 0 0}}
.dots i{{width:6px;height:6px;border-radius:50%;background:#ccc}} .dots i.on{{background:var(--red)}}
.txt{{flex:1;min-height:0;overflow:hidden;position:relative;padding:4px 10px 0}}
.txt::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:14px;background:linear-gradient(rgba(255,255,255,0),rgba(255,255,255,.96))}}
.txt h2{{margin:4px 0 0;color:var(--red);font-size:18px;line-height:1.15}}
.txt p{{margin:5px 0 0;font-size:13.5px;line-height:1.36;color:#222}}
.txt dl{{margin:8px 0 0;padding-top:6px;background:var(--dh) left top/100% 1px no-repeat;display:grid;grid-template-columns:auto 1fr auto 1fr;gap:2px 8px;font-size:12px;line-height:1.3}}
.txt dt{{color:#888}} .txt dd{{margin:0}}
.nav2{{flex:none;display:flex;justify-content:space-between;align-items:center;margin:0 10px;padding:4px 0 calc(env(safe-area-inset-bottom,0px) + 8px);background:var(--dh) left top/100% 1px no-repeat}}
.nav2 button{{display:flex;align-items:center;gap:6px;border:0;background:none;font:400 12px Calibri,Carlito,sans-serif;letter-spacing:.06em;color:#666;padding:6px 0}}
.note{{margin-left:auto;padding-left:8px;align-self:flex-start;text-align:right;font-size:10px;line-height:1.35;color:#888;letter-spacing:.03em}}
.note a{{color:var(--red)}}
.note button{{border:0;background:none;padding:0 2px;font:inherit;color:#888;letter-spacing:inherit}}
.note button[aria-pressed="true"]{{color:var(--red);text-decoration:underline}}
/* downloads & links */
.intro{{margin:0 0 8px;font-size:14px;line-height:1.45;color:#333}}
.pdfs{{list-style:none;margin:10px 0 0;padding:0}}
.pdfs li{{display:flex;align-items:center;gap:10px;padding:7px 0;background:var(--dh) left bottom/100% 1px no-repeat}}
.pdfs li:last-child{{background:none}}
.pdfs img{{width:26px;height:auto}}
.pdfs span{{font-size:15px}} .pdfs small{{display:block;font-size:11px;color:#999;letter-spacing:.04em}}
.links{{display:grid;grid-template-columns:1fr 1fr;gap:14px 10px;margin-top:12px}}
.lk{{display:flex;flex-direction:column;text-decoration:none;-webkit-tap-highlight-color:transparent}}
.lg{{display:flex;align-items:center;justify-content:center;height:50px;padding:9px 12px;background:#fff;position:relative}}   /* low rectangles: each logo (trimmed to its edges, m-lg-*) at most 32 px high, a small margin all round */
.lg img{{display:block;max-width:100%;max-height:32px;width:auto;height:auto;object-fit:contain}}
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
#iv .photos img{{height:70svh}}
.ivcap{{padding:10px 10px 30px;color:var(--red);font-size:17px;font-weight:700}}
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
<section class="pg" id="start"><div class="stage"><div class="beetle" id="beetle"><div class="whole"></div>{PIECES}</div><svg class="leads" id="leads" aria-hidden="true"></svg><svg class="leads" id="leadots" aria-hidden="true"></svg>{PINS}</div>
</section>
{section("us", "about us", "01", US)}
{section("projects", "projects", "02", '<div class="grid">' + TILES + '</div>')}
{section("downloads", "downloads & links", "03", DOWNLOADS)}
{section("bits", "bits & bats", "04", BITSHTML)}
{section("contact", "contact", "05", CONTACT)}
</main>
<i class="rule l" aria-hidden="true"></i><i class="rule r" aria-hidden="true"></i>
<div class="bar btop"><button type="button" id="goN" aria-label="previous page">{ARN}</button></div>
<div class="bar bbot"><button type="button" id="goS" aria-label="next page">{ARS}</button></div>
<dialog id="lb" aria-labelledby="lt">
<div class="top"><span></span>
<button type="button" class="x" id="lx" aria-label="close">{XC}</button></div>
<div class="phw"><div class="photos" id="ph"></div><button type="button" class="pw" id="phw" aria-label="previous photo">{ARW2}</button><button type="button" class="pe" id="phe" aria-label="next photo">{ARE2}</button></div><div class="dots" id="dots"></div>
<div class="txt"><h2 id="lt"></h2><div id="tx"></div><dl id="dl"></dl></div>
<div class="nav2"><button type="button" id="pp2">{ARW}previous</button><div class="cnt"><span id="lk"></span></div><button type="button" id="np2">next{ARE}</button></div>
</dialog>
<dialog id="iv" aria-label="bits &amp; bats">
<div class="top"><div class="cnt"><span id="ik"></span></div>
<button type="button" class="x" id="ix" aria-label="close">{XC}</button></div>
<div class="phw"><div class="photos" id="iph"></div><button type="button" class="pw" id="iw" aria-label="previous picture">{ARW2}</button><button type="button" class="pe" id="ie" aria-label="next picture">{ARE2}</button></div><div class="ivcap" id="icap"></div>
</dialog>
<script>
(function(){{
  /* pop-ups: opened without blocking the page, so the side strip stays usable; a tap on the logo or a tab closes them and goes there */
  function openDlg(d){{ d.show(); document.documentElement.classList.add('dlg'); }}
  function closeDlgs(){{ document.querySelectorAll('dialog[open]').forEach(d=>d.close()); document.documentElement.classList.remove('dlg'); }}
  document.querySelectorAll('dialog').forEach(d=>d.addEventListener('close',()=>{{ if(!document.querySelector('dialog[open]')) document.documentElement.classList.remove('dlg'); }}));
  document.querySelectorAll('.sidebar,.tab,.logo').forEach(a=>a.addEventListener('click',closeDlgs));
  addEventListener('keydown',e=>{{ if(e.key==='Escape') closeDlgs(); }});
  /* an open CV closes by itself when it has been scrolled out of view */
  const cvio=new IntersectionObserver(es=>es.forEach(e=>{{ const d=e.target; if(e.isIntersecting||!d.open) return;
    /* keep what is on screen where it is: measure a page that is in view before and after closing (some browsers do this by themselves) */
    const tp=parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0, anchor=document.elementFromPoint(innerWidth*.6,tp+6), y0=anchor&&anchor.getBoundingClientRect().top;
    d.open=false; if(anchor){{ const dy=anchor.getBoundingClientRect().top-y0; if(Math.abs(dy)>1) scrollBy({{top:dy,behavior:'instant'}}); }} }}));
  document.querySelectorAll('.cvp, .bio').forEach(d=>cvio.observe(d));
  document.querySelectorAll('.cvp').forEach(d=>d.addEventListener('toggle',()=>{{
    document.querySelectorAll('.cvb[aria-controls="'+d.id+'"]').forEach(b=>b.setAttribute('aria-expanded',String(d.open))); }}));
  document.querySelectorAll('.cvb').forEach(b=>b.addEventListener('click',()=>{{ const d=document.getElementById(b.getAttribute('aria-controls')), op=!d.open;
    document.querySelectorAll('.cvp[open]').forEach(x=>{{ if(x!==d) x.open=false; }});
    d.open=op; if(op) requestAnimationFrame(()=>d.scrollIntoView({{behavior:'smooth',block:'start'}}));
    else if(b.closest('.cvp')) document.getElementById('us').scrollIntoView({{behavior:'smooth'}}); }}));
  /* logo switch */
  const B=document.body;
  const setLogo=m=>{{ B.classList.toggle('side',m!=='top'); B.classList.toggle('rail',m==='rail'); try{{ localStorage.setItem('ddlogo2',m); }}catch(e){{}}
    document.querySelectorAll('[data-logo]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.logo===m))); }};
  const fitHead=()=>document.documentElement.style.setProperty('--head',(B.classList.contains('rail')?0:document.querySelector('header').offsetHeight)+'px');
  /* dotted leader lines: from the inner side of each circle across, then up or down onto the beetle, with a small arrowhead */
  const stage=document.querySelector('.stage'), leads=document.getElementById('leads'), btl=document.getElementById('beetle');
  function drawLeads(){{
    const S=stage.getBoundingClientRect(), Bt=btl.getBoundingClientRect(); let h='', g='';
    stage.querySelectorAll('.pin').forEach(p=>{{
      const c=p.querySelector('b').getBoundingClientRect(), left=p.classList.contains('l');
      const sx=(left?c.right+4:c.left-4)-S.left, sy=c.top+c.height/2-S.top;
      const tx=Bt.left+Bt.width*p.dataset.fx-S.left, ty=Bt.top+Bt.height*p.dataset.fy-S.top, d=ty>sy?1:-1, r=4.5;
      h+=`<path d="M${{sx}} ${{sy}}H${{tx}}V${{ty-d*r}}"/>`; g+=`<circle cx="${{tx}}" cy="${{ty}}" r="${{r}}"/>`;
    }});
    leads.innerHTML=h; document.getElementById('leadots').innerHTML=g;
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
  document.querySelectorAll('.bt').forEach(t=>t.addEventListener('click',()=>{{ openDlg(iv); iph.scrollLeft=+t.dataset.b*iph.clientWidth; ishow(); }}));
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
  let anims=[], run=0, flying=false;
  function play(){{
    if(reduce||!bug.animate) return; anims.forEach(a=>a.cancel()); const me=++run; flying=true; bug.classList.add('play');
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
    Promise.all(anims.map(a=>a.finished)).then(()=>{{ if(me===run){{ flying=false; bug.classList.remove('play'); }} }}).catch(()=>{{}});
  }}
  play();
  /* one tap: the beetle opens to the moment before the pieces lock - uneven white gaps - holds, then snaps shut */
  function openUp(){{
    if(flying||!bug.animate) return; anims.forEach(a=>a.cancel()); const me=++run; bug.classList.add('play'); const W=bug.offsetWidth;
    anims=ps.map(p=>{{ const dx=+p.dataset.dx, dy=+p.dataset.dy, n=Math.hypot(dx,dy)||1, g=R(.025,.075)*W, k=Math.max(.55,Math.min(1,n*1.4)), t=`translate(${{dx/n*g*k}}px,${{dy/n*g*k}}px)`;
      return p.animate([{{transform:'none',offset:0,easing:'cubic-bezier(.2,.7,.3,1)'}},{{transform:t,offset:.2}},{{transform:t,offset:.78,easing:'cubic-bezier(.6,0,.4,1.4)'}},{{transform:'none',offset:1}}],{{duration:1900,fill:'both'}}); }});
    Promise.all(anims.map(a=>a.finished)).then(()=>{{ if(me===run) bug.classList.remove('play'); }}).catch(()=>{{}});
  }}
  /* three taps: a red heart pops out of the beetle, zooms right in until it fills the screen, bursts into little hearts, and the page is back */
  const HEART='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21.3s-7.6-4.7-10.1-9.4C.3 8.6 1.9 4.6 5.6 4.2c2.4-.3 4 1.1 6.4 3.5 2.4-2.4 4-3.8 6.4-3.5 3.7.4 5.3 4.4 3.7 7.7C19.6 16.6 12 21.3 12 21.3z"/></svg>';
  let hearting=false;
  function heart(){{
    if(hearting||!document.body.animate) return; hearting=true;
    const b=bug.getBoundingClientRect(), cx=b.left+b.width/2, cy=b.top+b.height*.42;
    const fx=document.createElement('div'); fx.className='heartfx'; fx.innerHTML=HEART; document.body.appendChild(fx);
    const h=fx.firstChild, big=Math.hypot(innerWidth,innerHeight)/60*2.8, at=`translate(${{cx}}px,${{cy}}px)`;
    const zoom=h.animate([
      {{transform:at+' scale(0)',opacity:1}},
      {{transform:at+' scale(1.3)',opacity:1,offset:.16,easing:'ease-out'}},
      {{transform:at+' scale(1)',opacity:1,offset:.24}},
      {{transform:at+' scale(1.12)',opacity:1,offset:.32}},
      {{transform:at+' scale(1)',opacity:1,offset:.4,easing:'cubic-bezier(.5,0,.9,.6)'}},
      {{transform:`translate(${{innerWidth/2}}px,${{innerHeight*.6}}px) scale(${{big}})`,opacity:1,offset:1}}],{{duration:reduce?600:1500,fill:'forwards'}});
    fx.animate([{{background:'rgba(227,6,19,0)',offset:0}},{{background:'rgba(227,6,19,0)',offset:.8}},{{background:'rgba(227,6,19,1)',offset:1}}],{{duration:reduce?600:1500,fill:'forwards'}});   /* fully red at the peak */
    zoom.finished.then(()=>{{
      fx.animate([{{background:'rgba(227,6,19,1)'}},{{background:'rgba(227,6,19,0)'}}],{{duration:reduce?300:420,easing:'ease-in',fill:'forwards'}});
      h.animate([{{opacity:1}},{{opacity:0}}],{{duration:reduce?300:420,easing:'ease-in',fill:'forwards'}});   /* the big heart breaks up */
      /* the burst: little hearts fly out from the middle of the screen and fade */
      const n=reduce?0:40, mx=innerWidth/2, my=innerHeight/2, bits=[];
      for(let i=0;i<n;i++){{ const d=document.createElement('div'); d.innerHTML=HEART; const sv=d.firstChild; sv.classList.add('sm'); fx.appendChild(sv);
        const a=R(0,Math.PI*2), r=R(.35,.8)*Math.max(innerWidth,innerHeight), sc=R(.6,1.6), rot=R(-90,90);
        bits.push(sv.animate([{{transform:`translate(${{mx}}px,${{my}}px) scale(${{sc*2}}) rotate(0deg)`,opacity:1}},
          {{transform:`translate(${{mx+Math.cos(a)*r}}px,${{my+Math.sin(a)*r}}px) scale(${{sc}}) rotate(${{rot}}deg)`,opacity:0}}],{{duration:R(700,1200),easing:'cubic-bezier(.1,.8,.3,1)',fill:'forwards'}}).finished); }}
      return Promise.all(bits);
    }}).catch(()=>{{}}).then(()=>{{ fx.remove(); hearting=false; }});
  }}
  let taps=[];
  bug.addEventListener('click',()=>{{ const t=performance.now(); taps=taps.filter(x=>t-x<900); taps.push(t);
    if(taps.length>=3){{ taps=[]; heart(); }} else if(taps.length===1) openUp(); }});
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
    $('dl').innerHTML=F.filter(([k])=>k!=='name').map(([k,l])=>'<dt>'+l+'</dt><dd>'+esc(p.d[k]||'–')+'</dd>').join('');
    lb.scrollTop=0;
  }}
  /* W / E arrows on the photos: tap to slide to the previous / next photo; hidden at the first / last */
  const arrows=(box,w,e)=>{{ const upd=()=>{{ const k=Math.round(box.scrollLeft/box.clientWidth), n=box.children.length; w.disabled=k<=0; e.disabled=k>=n-1; }};
    w.onclick=()=>box.scrollBy({{left:-box.clientWidth,behavior:'smooth'}}); e.onclick=()=>box.scrollBy({{left:box.clientWidth,behavior:'smooth'}});
    box.addEventListener('scroll',upd,{{passive:true}}); return upd; }};
  const phUpd=arrows(ph,$('phw'),$('phe')), ivUpd=arrows(document.getElementById('iph'),$('iw'),$('ie'));
  ph.addEventListener('scroll',()=>{{ const k=Math.round(ph.scrollLeft/ph.clientWidth); [...dots.children].forEach((d,i)=>d.classList.toggle('on',i===k)); }},{{passive:true}});
  new MutationObserver(phUpd).observe(ph,{{childList:true}});
  document.querySelectorAll('.bt').forEach(t=>t.addEventListener('click',()=>requestAnimationFrame(ivUpd)));
  /* N / S arrows in the bars: previous / next page */
  const pages=[...document.querySelectorAll('.pg')], gN=$('goN'), gS=$('goS');
  const top0=()=>parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0;
  const curIdx=()=>{{ const y=top0()+4; let i=0; pages.forEach((p,k)=>{{ if(p.getBoundingClientRect().top<=y) i=k; }}); return i; }};
  const barUpd=()=>{{ const i=curIdx(), atTop=scrollY<4, atEnd=innerHeight+scrollY>=document.documentElement.scrollHeight-4;
    gN.disabled=atTop; gS.disabled=atEnd; gS.classList.toggle('go',i===0&&atTop); }};
  gS.onclick=()=>{{ const i=curIdx(); if(pages[i+1]) pages[i+1].scrollIntoView({{behavior:'smooth'}}); }};
  gN.onclick=()=>{{ const i=curIdx(), off=pages[i].getBoundingClientRect().top-top0(); (off<-8?pages[i]:pages[Math.max(0,i-1)]).scrollIntoView({{behavior:'smooth'}}); }};
  addEventListener('scroll',barUpd,{{passive:true}}); addEventListener('resize',barUpd); barUpd();
  document.querySelectorAll('.tile[data-p]').forEach(t=>t.addEventListener('click',()=>{{ show(+t.dataset.p); openDlg(lb); }}));
  $('lx').onclick=()=>lb.close();
  $('pp2').onclick=()=>show(pi-1); $('np2').onclick=()=>show(pi+1);
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
  L.marker(HOME,{{icon:L.divIcon({{className:'',iconSize:[34,44],iconAnchor:[17,44],html:'<div class="pinH"><svg class="pinsvg" viewBox="0 0 40 52" aria-hidden="true"><path class="pb" d="M20 51C14.5 40.5 2 31 2 19A18 18 0 0 1 38 19C38 31 25.5 40.5 20 51Z"/><circle class="pw" cx="20" cy="19" r="14.5"/><g transform="translate(20 19) scale(1.12)"><path class="pr" d="M-5.31 7.88A9.5 9.5 0 1 1 5.31 7.88"/><path class="pa" transform="rotate(90)" d="M5.4 0L-4.6 -4.9L-2.2 0L-4.6 4.9Z"/><text x="0" y="9.5">H</text></g></svg><div class="plab"><b class="dd">dasein-design</b><br>Neulerchenfelderstrasse 42/6<br>A-1160 Wien</div></div>'}})}}).addTo(map);
}}catch(err){{ console.warn('map not available',err); }} }});
</script>
</body>
</html>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w').write(HTML)
if __name__ == '__main__':
    print(len(pieces), 'pieces,', len(HTML) // 1024, 'KB ->', OUT)
