import re
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
from texts import INTRO, BIO, INFO_TXT, LINKS_TXT, CONTACT_TXT, SERVICES, SERVICES_SHORT, LEGAL_BODY, BITS, CARDS, CARD_AT   # shared with the desktop site
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
        ('bits', 'bits & bats', '04'), ('contact', 'contact', '05'), ('legal', 'impressum', '§')]
# about us (top) and contact (bottom) are half tabs (Steuart, 21 Oct): together they take one tab's height
TABHTML = ''.join(f'<a class="tab{" half" if i in ("us", "contact", "legal") else ""}" href="#{i}" data-pg="{i}"><span>{n.replace("&", "&amp;")}</span> <small>[{k}]</small></a>' for i, n, k in TABS)
# circles beside the beetle: left and right, top to bottom (five, 21 Oct)
# where each circle's dotted line ends on the upright beetle (fractions of its box): mouth, right front leg (claw), left middle leg, right back leg
AIM = [(.51, .245), (.715, .365), (.258, .53), (.80, .605), (.31, .905), (.69, .80)]   # ... 06 impressum: right back leg
PINS = ''.join(f'<a class="pin {"l" if k % 2 == 0 else "r"}" href="#{i}" data-fx="{AIM[k][0]}" data-fy="{AIM[k][1]}" style="top:{8 + k * 15.2}%;--k:{k}"><b>{num}</b><span>{n.replace("&", "&amp;")}</span></a>'
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
    return (f'<section class="pg" id="{i}" aria-label="{name} [{num}]"><div class="sbar" aria-hidden="true"></div><div class="pbar"><b>{name.replace("&", "&amp;")}</b><small>[{num}]</small></div>'
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
PLUS = ('<svg class="cvx" viewBox="-12 -12 24 24" aria-hidden="true"><circle class="r1" r="8"/><circle class="r2" r="8"/>'
        '<circle class="c" r="8"/><path class="v" d="M0 -4.2V4.2"/><path d="M-4.2 0H4.2"/></svg>')
DOWNLOADS = ('<p class="lab first">INFORMATION FOR CLIENTS</p><p class="intro">' + INFO_TXT + '</p><ul class="pdfs">'
             + ''.join(f'<li><img src="../img/pdf.svg" alt="PDF"><span>dd – {t}<small>PDF follows</small></span></li>' for t in PDFS)
             + '</ul><p class="lab">LINKS FOR CLIENTS</p><p class="intro">' + LINKS_TXT + '</p><div class="links cut" id="g-links" data-show="8">'
             + ''.join(f'<a class="lk" href="{u}" target="_blank" rel="noopener"><span class="lg"><img src="../img/m-lg-{im.replace('downloads-img', '')}" alt="" loading="lazy"></span>'
                       f'<b>{n}</b><small>{d}</small></a>' for u, im, n, d in LINKS)
             + '</div>' + '<button type="button" class="cvb more" aria-expanded="false" data-g="g-links">' + PLUS + '<span class="cvt"><span class="op">more</span><span class="cl">fewer</span></span><b>links</b></button>')

# ---------- bits & bats: the 21 pictures with their captions (tall ones span two rows); a tap opens them full screen ----------
def card(k):
    kind, src, head, txt, url = CARDS[k]
    if kind == 'news':
        return (f'<button type="button" class="tile card news" data-c="{k}"><span class="ct"><small>{src}</small><b>{head}</b><em class="ex">{re.sub(r"<[^>]+>", "", txt).replace("&amp;", "&")}</em></span>'
                f'<span class="cap"><b>LINK · {src}</b><small>read the article ↗</small></span></button>')
    ex = re.sub(r'<[^>]+>', '', txt.split('<br><br>')[-1] if '<br><br>' in txt else txt.replace(head, '', 1))
    return (f'<button type="button" class="tile card note" data-c="{k}"><span class="ct"><i class="qm">“</i><b>{head}</b><em class="ex">{ex}</em></span>'
            f'<span class="cap"><b>{"STUDIO NOTE" if src == "studio note" else "QUOTE"}</b><small>{"dasein-design" if src == "studio note" else src}</small></span></button>')


BITSHTML = ('<div class="bgrid cut" id="g-bits">' + ''.join(
    (card(CARD_AT[k]) if k in CARD_AT else '') +
    f'<button type="button" class="tile bt{" tall" if t else ""}" data-b="{k}"><img src="../img/{im}" alt="" loading="lazy">'
    f'<span class="cap"><b>{c}</b><small>smaller text example</small></span></button>' for k, (im, t, c) in enumerate(BITS)) + '</div>' + '<button type="button" class="cvb more" aria-expanded="false" data-g="g-bits">' + PLUS + '<span class="cvt"><span class="op">more</span><span class="cl">fewer</span></span><b>bits &amp; bats</b></button>')
BIMGS = ['../img/' + im for im, t, c in BITS]
BCAPS = [c.replace('&amp;', '&') for im, t, c in BITS]


# ---------- us & contact: the partnership, the two partners (CV folds open), the office with the map ----------
PARTNERS = [
    dict(role='Architekt<i class="rs"></i>Inhaber', first='Cuong', last='TRAN-VIET', q='BArch DipArch', idimg='m-id-cuong.webp', idalt='Personalausweis Cuong Tran-Viet', tel='+43 (0)676 4822 464', mail='cuong@dasein-design.net', extra='', nat='Österreich [EU]', lang='Deutsch &amp; Vietnamesisch [Muttersprache], English [verhandlungssicher]',
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
    dict(role='Architect', first='Steuart', last='J Mackenzie HARRISON', q='BArch MArch ARB', idimg='m-id-steuart.webp', idalt='Führerschein Steuart J Mackenzie Harrison', tel='+43 (0)699 1941 9240', mail='steuart@dasein-design.net', nat='Schottland [Europäisch!]', lang='Englisch [Muttersprache], Deutsch [B2]',
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


# short text about the practice (draft, to be replaced by Steuart's) and the full bio (placeholder)


def partner(n, p):
    """one architect: a column of the two-column block (ID card on its grey tile, name, letters, phone, e-mail, CV button)"""
    tel = p['tel'].replace(' ', '').replace('(0)', '')
    return (f'<article class="who"><span class="idw"><img class="idc" src="../img/{p["idimg"]}" alt="{p["idalt"]} (Nummer, Geburtsdatum und Unterschrift unkenntlich)" loading="lazy"></span>'
            f'<p class="role">» {p["role"]}</p><h3>{p["first"]}<br><b>{p["last"]}</b></h3><p class="q">{p["q"]}</p>'
            f'<p class="fx"><b>Staatsbürgerschaft:</b> {p["nat"]}<br><b>Sprachen:</b> {p["lang"]}</p>'
            f'<p class="kt"><a href="tel:{tel}">{p["tel"]}</a><a href="mailto:{p["mail"]}">{p["mail"]}</a></p>'
            f'<button type="button" class="cvb" aria-expanded="false" aria-controls="cv{n}">{PLUS}<span class="cvt">full</span><b>CV</b></button></article>')


def cvpanel(n, p):
    """the CV, opened under both columns, full width"""
    secs = p['cv'] + ([('Sprachen', [p['extra'].replace('Sprachen: ', '')])] if p['extra'] else [])
    cv = ''.join(f'<h4>{h}</h4><ul>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>' for h, xs in secs)
    return (f'<details class="cvp" id="cv{n}"><summary></summary><div class="box"><p class="lab first">CV</p>'
            f'<p class="role cvr">» {p["role"]}</p><h3 class="cvn">{p["first"]} <b>{p["last"]}</b> <span class="q">{p["q"]}</span></h3>{cv}'
            f'<button type="button" class="cvb" aria-expanded="true" aria-controls="cv{n}">{PLUS}<span class="cvt">full</span><b>CV</b></button></div></details>')


def morebtn(g, word, op='full', cl='close'):
    """the white bar with dotted lines that sits over the faded end of a folded block; opened it drops below the block"""
    return (f'<button type="button" class="cvb more" aria-expanded="false" data-g="{g}">' + PLUS
            + f'<span class="cvt"><span class="op">{op}</span><span class="cl">{cl}</span></span><b>{word}</b></button>')


US = ('<div class="box"><p class="lab first">PARTNERSHIP</p><p class="firm"><b class="dd">dasein-design</b> [architecture+design] [Wien]<br><span>» Jan.’03 – bis dato</span></p>'
      f'<div class="cut" id="g-bio" data-show="1" data-extra="30"><p class="intro2">{INTRO}</p>' + ''.join(f'<p class="bt">{t}</p>' for t in BIO) + '</div>'
      + morebtn('g-bio', 'bio') + '</div>'
      '<div class="duo">' + ''.join(partner(n, p) for n, p in enumerate(PARTNERS)) + '</div>'
      + ''.join(cvpanel(n, p) for n, p in enumerate(PARTNERS))
      # OUR SERVICES: the three blocks side by side in short; the white bar "full services" unfolds the whole text
      + '<div class="box"><p class="lab first">OUR SERVICES</p><div class="cut" id="g-svc" data-show="1" data-extra="30"><div class="sv3">' + ''.join(
          f'<div><img src="../img/{ic}" alt=""><b>{h}</b><span>{SERVICES_SHORT[h]}</span></div>' for h, ic, xs in SERVICES) + '</div>'
      + ''.join(f'<h4 class="sh"><img src="../img/{ic}" alt="">{h}</h4>' + ''.join(f'<p class="sp">» {x}</p>' for x in xs) for h, ic, xs in SERVICES) + '</div>'
      + morebtn('g-svc', 'services') + '</div>')
CONTACT = ('<div class="box"><p class="lab first">OFFICE</p><p class="addr"><b class="dd">dasein-design</b> · Neulerchenfelderstrasse 42/6<br>A-1160 Wien · Austria · EU</p>'
      + '<div class="pcs">' + ''.join(f'<p><b>{p["first"]} {p["last"]}</b><br><a href="tel:{p["tel"].replace(" ", "").replace("(0)", "")}">{p["tel"]}</a> · <a href="mailto:{p["mail"]}">{p["mail"]}</a></p>' for p in PARTNERS) + '</div>'
      '<div class="mapw"><div class="map" id="map"></div><div class="mz"><button type="button" id="zin" aria-label="zoom in">' + SEARCH.ZOOM_IN + '</button><button type="button" id="zout" aria-label="zoom out">' + SEARCH.ZOOM_OUT + '</button><button type="button" id="zhome" aria-label="back to the start view">' + SEARCH.ZOOM_HOME + '</button></div></div>'
      '<p class="mapl"><a href="https://www.openstreetmap.org/?mlat=48.211431&amp;mlon=16.333964#map=18/48.211431/16.333964">open the map</a></p></div>'
           '<p class="ctx">' + CONTACT_TXT + '</p>')   # the closing line of the site, after the map

MOREP = ('<button type="button" class="cvb more" aria-expanded="false" data-g="g-proj">' + PLUS
         + '<span class="cvt"><span class="op">more</span><span class="cl">fewer</span></span><b>projects</b></button>')

# Facebook, Instagram, X: the same marks as the desktop (profile addresses still to come)
SOCIAL = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><radialGradient id="igradm" cx="30%" cy="107%" r="150%"><stop offset="0" stop-color="#fdf497"/><stop offset=".05" stop-color="#fdf497"/><stop offset=".45" stop-color="#fd5949"/><stop offset=".6" stop-color="#d6249f"/><stop offset=".9" stop-color="#285AEB"/></radialGradient></defs></svg><span class="socs"><a class="soc" href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" width="18" height="18"><path fill="#0866FF" d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/></svg></a><a class="soc" href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" width="18" height="18"><path fill="url(#igradm)" d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></svg></a><a class="soc" href="#" aria-label="X (Twitter)"><svg viewBox="0 0 24 24" width="18" height="18"><path fill="#000000" d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg></a></span>'

# ---------- impressum [§] (draft by Claude, 22 Oct 2026 - to be checked by the office / the Kammer before going live) ----------
LEGAL = ('<div class="box legal cut" id="g-legal" data-show="4" data-extra="30"><p class="lab first">IMPRESSUM</p>' + LEGAL_BODY + '</div>'
         + morebtn('g-legal', 'impressum')
         # the end: one white screen for a little game - catch the red food before the beetle does; the site's mark and copyright at the foot
         + '<div class="play" id="play"><canvas class="ptrail"></canvas>'
           '<div class="pscore"><span>you <b id="sy">0</b></span><span>beetle <b id="sb">0</b></span></div>'
           '<div class="phint" id="phint"><b>collect the red dots!</b><span>whoever gets to 10 first wins</span><small>touch the dot to start</small></div>'
           '<i class="pdot"><b></b></i><img class="pbug" src="../img/m-bug-up.webp" alt="">'
           '<div class="pend"><img src="../img/m-mark.png" alt=""><span>dasein<b>-design</b></span>' + '<p class="copy">© 2026 [ dasein-design &amp; steux ]</p></div></div>')


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
  font-size:13.5px;white-space:nowrap;-webkit-tap-highlight-color:transparent;transition:background .15s}}
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
#goS .up{{display:none!important;align-items:center;gap:6px}} #goS.top .dn{{display:none}} #goS.top .up{{display:flex!important}}
.bar button span{{display:flex}} #goS .su,#goN .ns{{display:none}}
/* stack trial: the pages rise from the bottom as you swipe up, so the bottom arrow points up (N) and the top one down (S) */
.stack #goS .dn,.stack #goN .nn{{display:none}} .stack #goS .su,.stack #goN .ns{{display:flex}} .stack #goS.top .su{{display:none}}
.bar button{{align-items:center;gap:6px}} .bar .sc{{font-style:normal;font-size:11px;letter-spacing:.06em;color:#666}} #goS.top .sc{{display:none}}
.socs{{display:none;margin-left:auto;gap:12px;align-items:center}} .soc{{display:flex}} .soc svg{{display:block}}
body:not(.side) .socs{{display:flex}}   /* in the top layouts (and the stack trials) the three marks sit at the right of the logo */
.pend .socs{{display:flex;margin:4px 0 0;pointer-events:auto}}
#goS .up i{{font-style:normal;font-size:12px;letter-spacing:.06em;color:#3a3c37}}
/* the round arrow itself sits exactly in the middle (where the half bars meet); its words hang off to the right */
.bar button{{position:relative}} .bar .sc,#goS .up i{{position:absolute;left:calc(50% + 17px);top:50%;transform:translateY(-50%);white-space:nowrap}} #goS .up{{position:static}}
/* pulsing thin dark rings round an arrow, as on the desktop */
.ar.pulse .tr,.bar .go .tr{{display:block;fill:none;stroke:#3a3c37;stroke-width:.7;transform-box:fill-box;transform-origin:center;animation:ring 2.2s ease-out infinite}}
.ar.pulse .tr2,.bar .go .tr2{{animation-delay:1.1s}}
@keyframes ring{{0%{{transform:scale(1);opacity:.55}}100%{{transform:scale(1.7);opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.ar .tr{{animation:none!important;display:none!important}}}}
.body{{min-width:0;padding:0 10px}} .pg:last-child .body{{padding-bottom:28px}}
/* the last page (contact) is at least one screen tall, so the S arrow and the tab can bring its bar right to the top (largest viewport, for phones whose toolbar hides) */
.pg:last-child{{min-height:calc(100lvh - var(--head) - 2 * var(--bar))}}
/* guide lines down both sides, as on the desktop: a light dashed vertical line */
.rule{{position:fixed;top:0;bottom:0;width:1px;z-index:45;pointer-events:none;
  background:repeating-linear-gradient(to bottom,var(--line) 0 4px,transparent 4px 7px)}}
.rule.l{{left:calc(var(--side) - 1px)}} .rule.r{{right:7px}}
.side.rail .sidebar,.side.rail header{{border-right:0!important}}
/* section bar: same size, type and thickness as a tab in the side strip, a muted version of the lit tab's yellow-lime */
.pbar{{display:flex;align-items:center;justify-content:center;height:30px;margin:0 10px 10px;background:#eaffae;
  font-size:12.5px;color:rgba(0,0,0,.78);white-space:nowrap}}   /* page name in yellow-lime, as thick as the side tabs; the dotted line runs flush across its top edge */
.pbar b{{font-weight:700}} .pbar small{{font-size:8.5px;margin-left:4px}}
/* ?stack=1 (trial, 22 Oct): logo across the top, no side strip; the five page bars are thinner and stack up at the top of the screen as you pass
   their pages and wait at the bottom for the pages still to come - always all five on screen, a tap goes there */
.stack header nav,.stack header .note{{display:none}}
.stack main{{padding-left:8px}} .stack .rule.l{{left:7px}} .stack .bar{{left:8px}}
.stack .sbar{{display:none}}
.stack main > .pbar{{position:sticky;z-index:14;margin:0 10px;font-size:12px;cursor:pointer;-webkit-tap-highlight-color:transparent;transition:background-color .15s;
  justify-content:flex-start;padding:0 10px;height:23px;margin-bottom:-1px;color:#000;
  background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left bottom/100% 1px no-repeat,#fff}}
/* white bars with a thin dotted line between them (each overlaps the one before by 1 px, so the lines never double); only the page you are in is yellow-lime */
.stack main > .pbar{{margin-top:46px}}   /* a little air between a page and the next page's bar (only while it flows; stacked bars sit tight) */
/* inside the pages the waiting bars are a pale grey, so they read apart from the content; on the start page all white */
.stack.inpg main > .pbar{{background-color:#f2f2f2}}
.stack main > .pbar.on{{background-color:#eaffae!important}}
/* a tap shows first: the bar, tab or circle lights up, then the page moves (tapGo) */
.stack main > .pbar.hit,.tab.hit{{background-color:#cdff3e!important}}
.pin.hit b{{animation:none!important;background:#cdff3e!important;box-shadow:inset 0 0 0 1px var(--red)}} .pin.hit span{{color:var(--red)}}
.stack .body{{padding-top:10px}}
.stack .stage{{height:calc(100svh - var(--head) - 2 * var(--bar) - 104px);min-height:330px}}
/* the start page fills the whole screen (largest viewport), so all five bars wait together at the bottom however the phone's toolbar is showing */
.stack #start{{min-height:calc(100lvh - var(--head) - 2 * var(--bar) - 147px)}}
.stack.pairs #start{{min-height:calc(100lvh - var(--head) - 2 * var(--bar) - 81px)}}   /* just tall enough that all bars wait together at the bottom */
/* ?stack=2: half bars - each half moves on its own and locks in beside its partner */
.stack main > .hb{{position:sticky;z-index:14;display:flex;align-items:center;height:23px;padding:0 10px;font-size:12px;color:#000;cursor:pointer;-webkit-tap-highlight-color:transparent;
  transition:background-color .15s;
  background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left bottom/100% 1px no-repeat,#fff}}
/* trials (22 Oct): make each section read as one piece - ?sec=1 pale ground on every other section, ?sec=2 a dotted frame round each, ?sec=3 the section you are in turns pale lime */
.sec1 main > section.pg:not(#start):nth-of-type(even){{background:#f4f4f2}}   /* about us, downloads, contact (start is the first section) */
.sec1 main > section.pg:not(#start):nth-of-type(even) .cvb{{background-color:#f4f4f2}}   /* the full CV / bio / services bars take the same grey */
.sec1 main > section.pg:not(#start),.sec2 main > section.pg:not(#start),.sec3 main > section.pg:not(#start){{padding-top:12px;padding-bottom:16px}}
.sec1 main > section.pg:not(#start){{margin-left:10px;margin-right:10px;padding-left:0;padding-right:0}}   /* the grey ends where the title bars end */
.sec1:not(.stack) main > section.pg:not(#start){{padding-top:0}} .sec1:not(.stack) main > section.pg > .pbar{{margin-left:0;margin-right:0}}
.sec2 main > section.pg:not(#start){{margin-left:10px;margin-right:10px;padding-left:0;padding-right:0;background:var(--dh) left top/100% 1px no-repeat,var(--dh) left bottom/100% 1px no-repeat,var(--dv) left top/1px 100% no-repeat,var(--dv) right top/1px 100% no-repeat}}
.sec3 main > section.pg:not(#start){{transition:background-color .35s}} .sec3 main > section.pg.cur{{background-color:#f6ffde}}
.stack main > .hb.hl{{margin:39px 50% -1px 10px}}
.stack main > .hb.hr{{margin:39px 10px -1px 50%;
  background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left bottom/100% 1px no-repeat,
    repeating-linear-gradient(to bottom,#b8b8b8 0 1px,transparent 1px 3px) left top/1px 100% no-repeat,#fff}}
.stack.tstk .bar.btop{{border-bottom-color:transparent}} .stack.bstk .bar.bbot{{border-top-color:transparent}}   /* the bars' own dotted edge is enough where they meet the arrow bars */
.sback{{position:fixed;left:18px;right:18px;z-index:13;background:#fff;pointer-events:none}}
.stack.inpg main > .hb{{background-color:#f2f2f2}}
.stack main > .hb.on{{background-color:#eaffae!important}} .stack main > .hb.hit{{background-color:#cdff3e!important}}
.stack .stage{{height:calc(100svh - var(--head) - 2 * var(--bar) - 126px)}}
.stack.pairs .stage{{height:calc(100svh - var(--head) - 2 * var(--bar) - 70px)}}
.stack .pg:last-child{{min-height:calc(100lvh - var(--head) - 2 * var(--bar) - 132px)}}
.stack.pairs .pg:last-child{{min-height:calc(100lvh - var(--head) - 2 * var(--bar) - 66px)}}   /* the last page can always scroll up into place */
.sbar{{position:relative;z-index:1;height:1px;margin:10px 10px -1px}}   /* one line between two pages, 10 px clear each side (the same as from the side lines to the content) */
/* page boundary (21 Oct): the desktop's double edge ticks, pointing inwards from both guide lines, each running on as a dotted line right across;
   the two lines are the old title bar's height apart */
.sbar::before,.sbar::after{{content:"";position:absolute;left:-10px;right:-11px;height:1px;
  background:repeating-linear-gradient(to right,#b8b8b8 0 4px,transparent 4px 6px) left top/18px 1px no-repeat,
    repeating-linear-gradient(to right,#b8b8b8 0 4px,transparent 4px 6px) right top/18px 1px no-repeat,
    repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) 18px top/calc(100% - 36px) 1px no-repeat}}
.sbar::before{{top:0}} .sbar::after{{content:none}}

/* start page: the upright beetle with the five circles beside it */
#start{{display:block;overflow:clip}}
html,body{{overflow-x:clip}}
.stage{{position:relative;height:calc(100svh - var(--head) - 2 * var(--bar) - 6px);min-height:430px;margin:0 auto}}
.beetle{{cursor:pointer;-webkit-tap-highlight-color:transparent;position:absolute;left:50%;top:calc(10px + 5%);bottom:0;aspect-ratio:{BW}/{BH};transform:translateX(-50%);max-width:52vw}}
.beetle .whole{{position:absolute;inset:0;background:url(../img/m-bug-up.webp) center/100% 100% no-repeat}}
.bp{{position:absolute;display:none;background-image:url(../img/m-bug-up.webp);background-repeat:no-repeat;will-change:transform}}
.beetle.fly .bp{{display:block}} .beetle.fly .whole{{visibility:hidden}}   /* not .play - that is the game's box at the end and gave the beetle a jump */
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
  animation:pinring 9s ease-out infinite;animation-delay:calc(var(--k) * 1.5s + .3s)}}
.pin b::after{{border-color:var(--c2,var(--red));animation-delay:calc(var(--k) * 1.5s + .6s)}}
/* in turn each circle lights up yellow-lime (as if activated), sends out its rings, then turns grey again before the next one */
.pin b{{animation:pinon 9s ease-in-out infinite;animation-delay:calc(var(--k) * 1.5s)}}
@keyframes pinon{{0%{{background:#bfbfbf}}2.5%{{background:#cdff3e}}14%{{background:#cdff3e}}16.7%{{background:#bfbfbf}}100%{{background:#bfbfbf}}}}
.pin:nth-of-type(1){{--c1:#ffd400;--c2:#2f8cff}} .pin:nth-of-type(2){{--c1:#2fbf4a;--c2:#ffd400}}
.pin:nth-of-type(3){{--c1:#2f8cff;--c2:#cdff3e}} .pin:nth-of-type(4){{--c1:#e30613;--c2:#2fbf4a}} .pin:nth-of-type(5){{--c1:#cdff3e;--c2:#e30613}} .pin:nth-of-type(6){{--c1:#3a3c37;--c2:#ffd400}}
@keyframes pinring{{0%{{transform:scale(1);opacity:.9}}12.5%{{transform:scale(2.3);opacity:0}}100%{{transform:scale(2.3);opacity:0}}}}
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
/* one job per line (22 Oct): dashed = page structure, dotted = round pictures only; text blocks are never boxed - their red subtitle and the space hold them together */
.box{{margin:26px 0 0}}
.body > .box:first-child{{margin-top:4px}}
.box .firm{{margin:0}}
#contact .body > .box:first-child{{margin-top:0}}
.lab{{margin:6px 0 6px;font-size:11px;font-weight:700;letter-spacing:.12em;color:var(--red)}}   /* small red subtitles, bold like the current tab */
.firm{{margin:0 0 6px;font-size:16px}} .firm span{{font-size:13px;color:#666}}
.duo{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:26px 0 0}}
.who{{min-width:0;display:flex;flex-direction:column;align-items:flex-start}}
/* ID card on top, filling the column (number, birth date and signature blurred) */
.who .idw{{display:block;align-self:stretch;position:relative}}   /* the ID card fills the column, no frame of its own (Steuart, 21 Oct) */
.who .idc{{display:block;width:100%;height:auto;border-radius:6px}}
.cvr{{margin:0;font-size:11.5px;color:#666}}
.who .role .rs,.cvr .rs{{display:inline-block;width:2.5px;height:.95em;margin:0 6px;vertical-align:-.1em;background:#3a3c37}}
.who .role{{margin:8px 0 0;font-size:11.5px;color:#666}}
.who h3,.cvn{{margin:1px 0 0;font-weight:400;font-size:15px;line-height:1.15;color:var(--red)}} .who h3 b,.cvn b{{font-weight:700}}
.who .q,.cvn .q{{margin:2px 0 0;font-size:11.5px;font-style:italic;font-weight:400;color:#555}}
.cvn .q{{margin-left:3px}}
.who .fx{{margin:6px 0 0;font-size:11px;line-height:1.3;color:#444}} .who .fx b{{font-weight:700;color:#222}}
.who .kt{{display:flex;flex-direction:column;align-items:flex-start;gap:2px;margin:auto 0 0;padding-top:7px;font-size:min(12px,3.05vw);line-height:1.35;white-space:nowrap}}
.who .kt a{{text-decoration:none}}
/* short text about the practice */
.intro2{{margin:8px 0 0;font-size:13.5px;line-height:1.4;color:#222}}
p.bt,.sp{{margin:8px 0 0;font-size:13.5px;line-height:1.4;color:#222}} .sp{{margin-top:3px;font-size:13px}}
.sh{{display:flex;align-items:center;gap:7px;margin:12px 0 2px;font-size:14px;font-weight:700;color:var(--red);letter-spacing:.02em}} .sh img{{width:18px;height:18px}}
.bio p{{margin:8px 0 0;font-size:13.5px;line-height:1.4;color:#222}}
/* full bio and our services: two openers side by side, each unfolding underneath (one at a time) */
.opn{{display:flex;gap:18px;flex-wrap:wrap}}
/* openers (full bio, full services) sit on their subtitle's line, at the right */
.lh{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 0 6px}} .lh .lab{{margin:0}} .lh .cvb{{margin:0;padding:0}}
.fold > summary{{display:none}} .fold{{margin:0}}
.svc h4{{display:flex;align-items:center;gap:7px;margin:12px 0 2px;font-size:14px;font-weight:700;color:var(--red);letter-spacing:.02em}}
.svc h4 img{{width:18px;height:18px}}
.sv3{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:6px 0 6px}}
#us .cvp + .box{{margin-top:26px}}
.sv3 div{{display:flex;flex-direction:column;align-items:center;text-align:center;gap:3px}}
.sv3 img{{width:25px;height:25px}} .sv3 b{{font-size:13px;color:var(--red);letter-spacing:.03em}}
.sv3 span{{font-size:11.5px;line-height:1.3;color:#444}}
.svc p{{margin:3px 0 0;font-size:13px;line-height:1.4;color:#222}}
/* the CVs open under both columns */
.cvp > summary{{display:none}} .cvp{{margin:0}} .cvp .box{{margin-top:26px}} .cvp .cvb{{margin-top:10px}}
/* full CV: the same white bar as the other openers, one per column, the gap between the columns showing they are two */
.who .cvb,.cvp .cvb{{display:flex;align-self:stretch;width:100%;height:30px;margin-top:8px;padding:0 2px;
  background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left bottom/100% 1px no-repeat,#fff}}
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
.addr{{margin:0;font-size:13.5px;line-height:1.35}}   /* compact: two short lines */
.ctx{{margin:22px 0 0;text-align:center;font-size:min(13.5px,3.6vw);line-height:1.35;color:#000;white-space:nowrap}}   /* closing line, in the address type (not italic) */   /* closing line, like a full stop: two centred lines, a dash before and after */
.ctx .hd{{font-style:normal;margin:0 .4em}}
/* the partners on the contact page too (as on the desktop), compact */
.pcs{{margin:12px 0 0;font-size:min(13px,3.4vw);line-height:1.4}} .pcs p{{margin:0 0 8px}} .pcs b{{font-weight:700}} .pcs a{{text-decoration:none}}
/* copyright, as at the foot of the desktop side bar */
.legal h4{{margin:12px 0 2px;font-size:12px;font-weight:700;color:#000}} .legal p{{margin:0;font-size:12.5px;line-height:1.45;color:#222}} .legal .lp{{color:#666;font-size:11.5px}}
.legal a{{color:#1a5fd0;text-decoration:none}} .legal a[href^="tel:"]{{color:#1e8e3e}} .legal .todo{{color:#e30613}}
.ptrail{{position:absolute;inset:0;width:100%;height:100%}}
.play{{position:relative;height:calc(100svh - var(--head) - 2 * var(--bar) - var(--stk,0px) - 20px);min-height:360px;margin:20px -10px 0;overflow:hidden;touch-action:pan-y;-webkit-user-select:none;user-select:none}}   /* the page still scrolls; the dot itself is dragged */
.play .pdot{{touch-action:none;width:56px;height:56px;margin:-28px 0 0 -28px}}
.pdot{{position:absolute;left:0;top:0;width:44px;height:44px;margin:-22px 0 0 -22px;display:flex;align-items:center;justify-content:center;cursor:grab}}
.pdot b{{width:10px;height:10px;border-radius:50%;background:#cdff3e;box-shadow:0 0 0 1px #3a3c37;animation:pdp 1.4s ease-in-out infinite}}
.pdot::before,.pdot::after{{content:"";position:absolute;left:50%;top:50%;width:10px;height:10px;margin:-5px 0 0 -5px;border-radius:50%;border:1px solid var(--red);opacity:0;animation:pdr 1.8s ease-out infinite}}
.pdot::after{{animation-delay:.9s}}
@keyframes pdp{{50%{{transform:scale(1.25)}}}} @keyframes pdr{{0%{{transform:scale(1);opacity:.8}}100%{{transform:scale(4.2);opacity:0}}}}
.pbug{{position:absolute;left:0;top:0;width:38px;height:84px;margin:-42px 0 0 -19px;pointer-events:none;will-change:transform}}
.stack{{--stk:132px}} .stack.pairs{{--stk:66px}}
.pscore{{position:absolute;left:12px;right:12px;top:8px;display:flex;justify-content:space-between;font-size:12px;letter-spacing:.06em;color:#555;pointer-events:none;z-index:2}}
.pscore b{{color:var(--red);font-size:15px;margin-left:4px}}
.phint{{position:absolute;left:0;right:0;top:30%;display:flex;flex-direction:column;align-items:center;gap:3px;text-align:center;pointer-events:none;transition:opacity .5s;z-index:2}}
.phint b{{font-size:21px;color:var(--red)}} .phint span{{font-size:14px;color:#222}} .phint small{{margin-top:6px;font-size:11.5px;letter-spacing:.08em;color:#888}}
.play.go .phint{{opacity:0}}
.pfood{{position:absolute;left:0;top:0;width:10px;height:10px;margin:-5px 0 0 -5px;border-radius:50%;background:var(--red);box-shadow:0 0 0 2px #fff,0 0 0 3px rgba(227,6,19,.35);pointer-events:none}}
.pend{{position:absolute;left:0;right:0;bottom:10px;display:flex;flex-direction:column;align-items:center;gap:2px;pointer-events:none;z-index:2}}
.pend img{{width:26px;height:26px}} .pend span{{font-size:17px;color:var(--red)}} .pend b{{font-weight:700}} .pend .copy{{margin:4px 0 0}}
.pmsg{{position:absolute;left:0;right:0;top:44%;text-align:center;font-size:22px;font-weight:700;color:var(--red);pointer-events:none;z-index:3}}
.pdd{{position:absolute;left:0;top:0;width:34px;height:34px;margin:-17px 0 0 -17px;pointer-events:none}}   /* the round dd badge the beetle sends out when it catches the dot */
.copy{{margin:18px 0 0;text-align:center;font-size:10.5px;letter-spacing:.06em;color:#888}}   /* closing line, like a full stop */
p.lab:not(.first){{margin-top:26px}}
.box .lab.first{{margin-top:0}}
.mapw{{position:relative;z-index:0;isolation:isolate;margin:10px 0 0}}
.map{{height:56svh;min-height:300px;background:#eee}}
.mz{{position:absolute;right:9px;top:9px;z-index:500;display:flex;flex-direction:column;gap:5px}}
.mz button{{width:36px;height:36px;border:0;border-radius:50%;background:none;padding:0;-webkit-tap-highlight-color:transparent}}
.mz #zhome{{margin-top:9px}}
.mz svg{{display:block;width:100%;height:100%;overflow:visible}}
.mz circle{{fill:rgba(255,255,255,.9);stroke:#e30613;stroke-width:.7}}
.mz path{{fill:none;stroke:#e30613;stroke-width:.85;stroke-linecap:round;stroke-linejoin:round}}
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
.pdfs{{display:grid;grid-template-columns:1fr 1fr;gap:6px 12px}}   /* the four PDFs in two rows of two */
.pdfs li{{display:flex;align-items:center;gap:8px;padding:4px 0}} .pdfs span{{font-size:13.5px!important;line-height:1.25}}
.pdfs li:last-child{{background:none}}
.pdfs img{{width:26px;height:auto}}
.pdfs span{{font-size:15px}} .pdfs small{{display:block;font-size:11px;color:#999;letter-spacing:.04em}}
.links{{display:grid;grid-template-columns:1fr 1fr;gap:14px 10px;margin-top:12px}}
/* long grids (links, bits & bats) show about six at first, fading out greyed; "more …" shows the rest */
.cut{{overflow:hidden;transition:max-height .45s ease}}
.cut[data-extra].shut{{-webkit-mask-image:linear-gradient(#000 calc(100% - 34px),rgba(0,0,0,.15));mask-image:linear-gradient(#000 calc(100% - 34px),rgba(0,0,0,.15))}}
.cut.shut{{-webkit-mask-image:linear-gradient(#000 55%,rgba(0,0,0,.18));mask-image:linear-gradient(#000 55%,rgba(0,0,0,.18))}}
.more{{position:relative;z-index:2;display:flex;width:100%;height:30px;margin:-30px 0 0;padding:0 2px;background:
  repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left bottom/100% 1px no-repeat,rgba(255,255,255,.94)}}
/* open: the bar drops back under the grid */
.more[aria-expanded=true]{{margin-top:8px}}
.more .cl{{display:none}} .more[aria-expanded=true] .cl{{display:inline}} .more[aria-expanded=true] .op{{display:none}}
.more[aria-expanded=true] .cvt::after{{content:none}} .more[aria-expanded=true] .cvt{{font-size:13px}}
@media (prefers-reduced-motion:reduce){{.cut{{transition:none}}}}
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
/* notes and links among the photos: a box of their own (dotted frame, grey bar underneath, like the photo tiles), type instead of a picture */
.bgrid .card{{display:block;width:100%;text-align:left;color:#222}}
.card.news{{background:#f4f4f4}} .card.note{{background:#fffbd6}}
.card .ct{{position:absolute;inset:0 0 34px;display:flex;flex-direction:column;gap:4px;padding:9px 9px 6px;overflow:hidden}}
.card .ct small{{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--red);font-weight:700}}
.card .ct b{{font-size:14px;line-height:1.2;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;flex:none}}
.card.note .qm{{font-style:normal;font-size:36px;line-height:.6;color:var(--red);height:14px;flex:none}}
.card .ex{{font-style:normal;font-size:11.5px;line-height:1.35;color:#555;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}} .card .mo{{font-size:12px;color:var(--red);flex:none}}
.card.note .ex{{display:none}}
.card.note .ct b{{font-weight:400;font-style:italic;font-size:14px;line-height:1.3;-webkit-line-clamp:4}}
.cwc{{padding:6px 14px 30px;overflow:auto}} .cwc .lab{{margin-top:10px}} .cwc h2{{margin:6px 0 10px;font-size:20px;line-height:1.2;color:var(--red)}}
.cwc p{{margin:0;font-size:15px;line-height:1.5;color:#222}} .cwc .q{{font-size:19px;line-height:1.45}} .cwc .todo{{color:var(--red)}}
.cwc .qm{{display:block;font-style:normal;font-size:64px;line-height:.5;height:30px;margin-top:22px;color:var(--red)}}
.cwc .open{{display:inline-block;margin-top:16px;font-size:14px;color:#1a5fd0;text-decoration:none;padding:6px 0;background:var(--dh) left bottom/100% 1px no-repeat}}
/* one picture full screen, swipe to the next */
#iv .photos img{{height:70svh}}
.ivcap{{padding:10px 10px 30px;color:var(--red);font-size:17px;font-weight:700}}
.ivcap small{{display:block;margin-top:4px;color:#888;font-weight:400;font-size:12px;letter-spacing:.06em}}
</style>
</head>
<body>
<script>/* three versions: logo and tabs all down the side (default) · logo on the side, tabs on top · logo and tabs across the top
   ?logo=rail / side / top, remembered on this phone */
(function(){{ let m='rail'; try{{ m=new URLSearchParams(location.search).get('logo')||localStorage.getItem('ddlogo2')||'rail';
    const sk=new URLSearchParams(location.search).get('stack'); if(sk==='1'||sk==='2'){{ document.body.classList.add('stack'); m='top'; }} if(sk==='2') document.body.classList.add('pairs'); const sc=new URLSearchParams(location.search).get('sec'); document.body.classList.add('sec'+(['0','1','2','3'].includes(sc)?sc:'1'));   /* pale grey (sec1) is the standard since 22 Oct; ?sec=0 turns it off */ }}catch(e){{}}
  if(m!=='top') document.body.classList.add('side'); if(m==='rail') document.body.classList.add('rail'); }})();</script>
<a class="sidebar" href="#start" aria-label="dasein-design, start"><img src="../img/m-mark.png" alt=""><span>dasein<b>-design</b></span></a>
<header>
<div class="row1"><a class="logo" href="#start" aria-label="dasein-design, start"><img src="../img/m-mark.png" alt=""><span>dasein<b>-design</b></span></a>{SOCIAL}<span class="note">preview · <button type="button" data-logo="rail">all side</button>/<button type="button" data-logo="side">logo side</button>/<button type="button" data-logo="top">top</button> · <a href="../">full site</a></span></div>
<nav>{TABHTML}</nav>
</header>
<main>
<section class="pg" id="start"><div class="stage"><div class="beetle" id="beetle"><div class="whole"></div>{PIECES}</div><svg class="leads" id="leads" aria-hidden="true"></svg><svg class="leads" id="leadots" aria-hidden="true"></svg>{PINS}</div>
</section>
{section("us", "about us", "01", US)}
{section("projects", "projects", "02", '<div class="grid cut" id="g-proj" data-show="8">' + TILES + '</div>' + MOREP)}
{section("downloads", "downloads & links", "03", DOWNLOADS)}
{section("bits", "bits & bats", "04", BITSHTML)}
{section("contact", "contact", "05", CONTACT)}
{section("legal", "impressum", "§", LEGAL)}
</main>
<i class="rule l" aria-hidden="true"></i><i class="rule r" aria-hidden="true"></i>
<div class="bar btop"><button type="button" id="goN" aria-label="previous page"><span class="nn">{ARN}</span><span class="ns">{ARS}</span><i class="sc">scroll</i></button></div>
<div class="bar bbot"><button type="button" id="goS" aria-label="next page"><span class="dn">{ARS}</span><span class="su">{ARN}</span><i class="sc">scroll</i><span class="up">{ARN}<i>back to the top</i></span></button></div>
<dialog id="lb" aria-labelledby="lt">
<div class="top"><span></span>
<button type="button" class="x" id="lx" aria-label="close">{XC}</button></div>
<div class="phw"><div class="photos" id="ph"></div><button type="button" class="pw" id="phw" aria-label="previous photo">{ARW2}</button><button type="button" class="pe" id="phe" aria-label="next photo">{ARE2}</button></div><div class="dots" id="dots"></div>
<div class="txt"><h2 id="lt"></h2><div id="tx"></div><dl id="dl"></dl></div>
<div class="nav2"><button type="button" id="pp2">{ARW}previous</button><div class="cnt"><span id="lk"></span></div><button type="button" id="np2">next{ARE}</button></div>
</dialog>
<dialog id="cw" aria-label="bits &amp; bats">
<div class="top"><div class="cnt"><span id="ck"></span></div><button type="button" class="x" id="cx" aria-label="close">{XC}</button></div>
<div class="cwc" id="cwc"></div>
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
  document.querySelectorAll('.cvp, .fold').forEach(d=>cvio.observe(d));
  document.querySelectorAll('.cvp, .fold').forEach(d=>d.addEventListener('toggle',()=>{{
    document.querySelectorAll('.cvb[aria-controls="'+d.id+'"]').forEach(b=>b.setAttribute('aria-expanded',String(d.open))); }}));
  document.querySelectorAll('.cvb[aria-controls]').forEach(b=>b.addEventListener('click',e=>{{ if(!realTap(e)) return; const d=document.getElementById(b.getAttribute('aria-controls')), op=!d.open;
    document.querySelectorAll(d.classList.contains('fold')?'.fold[open]:not(#'+d.id+')':'.cvp[open]').forEach(x=>{{ if(x!==d) x.open=false; }});
    d.open=op; if(op&&!d.classList.contains('fold')) requestAnimationFrame(()=>d.scrollIntoView({{behavior:'smooth',block:'start'}}));
    else if(b.closest('.cvp')) document.getElementById('us').scrollIntoView({{behavior:'smooth'}}); }}));
  /* long grids: cut after the first six, with "more links" / "more bits & bats" */
  const cuts=[...document.querySelectorAll('.cut')];
  const cutH=g=>{{ const top=g.getBoundingClientRect().top, n=+g.dataset.show||6, ex=+g.dataset.extra||0; let b=0; [...g.children].slice(0,n).forEach(c=>{{ b=Math.max(b,c.getBoundingClientRect().bottom); }}); return b-top+ex; }};
  const setCut=(g,open)=>{{ g.classList.toggle('shut',!open); g.style.maxHeight=open?g.scrollHeight+'px':cutH(g)+'px';
    const b=document.querySelector('.more[data-g="'+g.id+'"]'); if(b) b.setAttribute('aria-expanded',String(open)); }};
  cuts.forEach(g=>setCut(g,false));
  addEventListener('resize',()=>cuts.forEach(g=>setCut(g,!g.classList.contains('shut'))));
  let lastScroll=0, tap=null; addEventListener('scroll',()=>{{ lastScroll=performance.now(); }},{{passive:true}});
  addEventListener('pointerdown',e=>{{ tap={{x:e.clientX,y:e.clientY,t:performance.now(),moving:performance.now()-lastScroll<300}}; }},{{passive:true,capture:true}});
  const realTap=e=>{{ if(!tap) return e.detail===0; return !tap.moving && Math.hypot(e.clientX-tap.x,e.clientY-tap.y)<12 && performance.now()-tap.t<800; }};
  const reCut=()=>cuts.forEach(g=>{{ if(g.classList.contains('shut')) setCut(g,false); }});
  if(document.fonts) document.fonts.ready.then(reCut); addEventListener('load',reCut);
  document.querySelectorAll('.more').forEach(b=>b.addEventListener('click',e=>{{ if(!realTap(e)) return; const g=document.getElementById(b.dataset.g), op=g.classList.contains('shut');
    setCut(g,op); if(!op) g.scrollIntoView({{behavior:'smooth',block:'start'}}); }}));

  /* the end of the site: a little game. Red food dots lie about; drag the pulsing dot to eat them before the beetle does.
     The beetle walks in curves to the nearest food, leaving a dotted trail. First to 10 wins; a dd badge pops for every bite */
  (function(){{ const pl=document.getElementById('play'); if(!pl) return;
    const dot=pl.querySelector('.pdot'), bug=pl.querySelector('.pbug'), cv=pl.querySelector('.ptrail'), tc=cv.getContext('2d'), R2=(a,b)=>a+Math.random()*(b-a);
    const sy=document.getElementById('sy'), sb=document.getElementById('sb'), hint=document.getElementById('phint');
    let W=0,H=0, d={{x:0,y:0}}, g={{x:30,y:200,a:0}}, held=false, run=false, last=0, walked=0, food=[], you=0, them=0, over=false, playing=false;
    const size=()=>{{ W=pl.clientWidth; H=pl.clientHeight; const r=devicePixelRatio||1; if(cv.width!==Math.round(W*r)){{ cv.width=Math.round(W*r); cv.height=Math.round(H*r); tc.setTransform(r,0,0,r,0,0); tc.fillStyle='rgba(58,60,55,.55)'; }} }};
    const DD='<svg class="pdd" viewBox="-20 -20 40 40"><circle r="19" fill="#e30613"/><circle r="15.5" fill="none" stroke="#fff" stroke-width="1" stroke-dasharray="1 2.2"/>'
      +'<text y="1" fill="#fff" font-family="Calibri,Carlito,sans-serif" font-weight="700" font-size="17" text-anchor="middle" dominant-baseline="central">dd</text></svg>';
    function pop(x,y){{ const w=document.createElement('div'); w.innerHTML=DD; const e=w.firstChild; pl.appendChild(e);
      e.animate([{{transform:`translate(${{x}}px,${{y}}px) scale(.2)`,opacity:1}},{{transform:`translate(${{x}}px,${{y-24}}px) scale(1.1)`,opacity:1,offset:.35}},
        {{transform:`translate(${{x}}px,${{y-60}}px) scale(.9)`,opacity:0}}],{{duration:1100,easing:'cubic-bezier(.2,.8,.3,1)'}}).finished.then(()=>e.remove()).catch(()=>e.remove()); }}
    function addFood(){{ const el=document.createElement('i'); el.className='pfood'; const f={{x:R2(24,W-24),y:R2(60,H-90),el}}; el.style.transform=`translate(${{f.x}}px,${{f.y}}px)`; pl.appendChild(el); food.push(f); }}
    function eat(f,byYou){{ food=food.filter(x=>x!==f); f.el.remove(); pop(f.x,f.y);
      if(byYou){{ you++; sy.textContent=you; }} else {{ them++; sb.textContent=them; }}
      if(you>=10||them>=10){{ over=true; const m=document.createElement('p'); m.className='pmsg'; m.textContent=you>=10?'you win!':'the beetle wins!'; pl.appendChild(m);
        setTimeout(()=>{{ m.remove(); playing=false; pl.classList.remove('go'); you=them=0; sy.textContent=sb.textContent='0'; tc.clearRect(0,0,W,H); food.forEach(x=>x.el.remove()); food=[]; for(let i=0;i<5;i++) addFood(); over=false; }},2600); }}
      else setTimeout(addFood,R2(400,1400)); }}
    function step(t){{ if(!run) return; const dt=Math.min(.05,(t-last)/1000||0); last=t;
      if(!over){{
        let tgt=null, best=1e9;
        if(playing){{
          /* you: the dot eats what it touches */
          food.slice().forEach(f=>{{ if(Math.hypot(f.x-d.x,f.y-d.y)<16) eat(f,true); }});
          /* the beetle: to the nearest food, bug-like in curves */
          food.forEach(f=>{{ const q=Math.hypot(f.x-g.x,f.y-g.y); if(q<best){{ best=q; tgt=f; }} }});
        }} else {{ /* waiting to start: the beetle strolls round in loops and leaves the food alone */
          tgt={{x:W/2+Math.cos(t/1300)*W*.3, y:H*.62+Math.sin(t/1300)*H*.18}}; }}
        if(tgt){{ const dx=tgt.x-g.x, dy=tgt.y-g.y;
          const want=Math.atan2(dy,dx)*180/Math.PI+90+Math.sin(t/260)*20; let da=((want-g.a+540)%360)-180;
          g.a+=Math.max(-170*dt,Math.min(170*dt,da)); const sp=78*dt, h=(g.a-90)*Math.PI/180;
          g.x=Math.max(10,Math.min(W-10,g.x+Math.cos(h)*sp)); g.y=Math.max(10,Math.min(H-10,g.y+Math.sin(h)*sp));
          walked+=sp; if(walked>3.2){{ walked=0; tc.fillRect(g.x-.6,g.y-.6,1.2,1.2); }}
          if(playing&&best<20) eat(tgt,false); }}
      }}
      dot.style.transform=`translate(${{d.x}}px,${{d.y}}px)`; bug.style.transform=`translate(${{g.x}}px,${{g.y}}px) rotate(${{g.a}}deg)`;
      requestAnimationFrame(step); }}
    const at=e=>{{ const r=pl.getBoundingClientRect(); d.x=Math.max(8,Math.min(W-8,e.clientX-r.left)); d.y=Math.max(8,Math.min(H-8,e.clientY-r.top)); }};
    dot.addEventListener('pointerdown',e=>{{ held=true; pl.setPointerCapture(e.pointerId); at(e); if(!playing&&!over){{ playing=true; pl.classList.add('go'); }} }});
    pl.addEventListener('pointermove',e=>{{ if(held) at(e); }});
    const up=()=>{{ held=false; }}; pl.addEventListener('pointerup',up); pl.addEventListener('pointercancel',up);
    let started=false;
    new IntersectionObserver(es=>es.forEach(e=>{{ if(e.isIntersecting&&!matchMedia('(prefers-reduced-motion: reduce)').matches){{
      if(!run){{ run=true; size(); if(!started){{ started=true; d={{x:W*.7,y:H*.55}}; for(let i=0;i<5;i++) addFood(); }} last=performance.now(); requestAnimationFrame(step); }} }} else run=false; }}),{{threshold:.3}}).observe(pl);
    addEventListener('resize',size); }})();
  /* logo switch */
  const B=document.body;
  const setLogo=m=>{{ B.classList.toggle('side',m!=='top'); B.classList.toggle('rail',m==='rail'); try{{ if(!B.classList.contains('stack')) localStorage.setItem('ddlogo2',m); }}catch(e){{}}
    document.querySelectorAll('[data-logo]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.logo===m))); }};
  /* the arrow bar tucks 1px under the header (never a hairline gap where the page shows through); re-measured when fonts arrive or the header changes */
  const fitHead=()=>document.documentElement.style.setProperty('--head',(B.classList.contains('rail')?0:Math.max(0,Math.floor(document.querySelector('header').getBoundingClientRect().height)-1))+'px');
  if(document.fonts) document.fonts.ready.then(fitHead); if(window.ResizeObserver) new ResizeObserver(()=>fitHead()).observe(document.querySelector('header'));
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
  document.querySelectorAll('.tile.bt').forEach(t=>t.addEventListener('click',()=>{{ openDlg(iv); iph.scrollLeft=+t.dataset.b*iph.clientWidth; ishow(); }}));
  document.getElementById('ix').onclick=()=>iv.close();
  /* notes and links: their own small pop-up */
  const CA={json.dumps([list(c) for c in CARDS])}, cw=document.getElementById('cw');
  document.querySelectorAll('.card').forEach(b=>b.addEventListener('click',()=>{{ const [kind,src,head,txt,url]=CA[+b.dataset.c];
    document.getElementById('ck').innerHTML='bits &amp; bats · '+(kind==='news'?'link':'note');
    document.getElementById('cwc').innerHTML=kind==='news'
      ? '<p class="lab first">'+src+'</p><h2>'+head+'</h2><p>'+txt+'</p><a class="open" href="'+url+'" target="_blank" rel="noopener">read the article on '+src+' ↗</a>'
      : '<i class="qm">“</i><p class="lab first">'+src+'</p><p class="q">'+txt+'</p>';
    openDlg(cw); }}));
  document.getElementById('cx').onclick=()=>cw.close();
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* current page: tab in yellow-lime, as on the desktop */
  const tabs=[...document.querySelectorAll('.tab')];
  const secs=[...document.querySelectorAll('.pg')];
  function mark(){{ const y=innerHeight*.45; let id='start'; secs.forEach(s=>{{ if(s.getBoundingClientRect().top<=y) id=s.id; }});
    tabs.forEach(t=>t.classList.toggle('cur',t.dataset.pg===id)); rotTabs(id); }}
  /* the tabs take turns: the current page's tab moves to the top and the rest follow in order (03, 04, 05, 01, 02);
     back on the start page they return to 01 … 05. They slide to their new places */
  let rotFor='start';
  function rotTabs(id){{
    if(id===rotFor) return; rotFor=id;
    const n=tabs.length, c=Math.max(0,tabs.findIndex(t=>t.dataset.pg===id));
    const before=tabs.map(t=>t.getBoundingClientRect());
    tabs.forEach((t,k)=>{{ t.style.order=id==='start'?k:(k-c+n)%n; }});
    if(reduce) return;
    tabs.forEach((t,k)=>{{ const a=t.getBoundingClientRect(), dx=before[k].left-a.left, dy=before[k].top-a.top;
      if(dx||dy) t.animate([{{transform:`translate(${{dx}}px,${{dy}}px)`}},{{transform:'none'}}],{{duration:450,easing:'cubic-bezier(.3,.7,.3,1)'}}); }});
  }}
  addEventListener('scroll',mark,{{passive:true}}); addEventListener('resize',mark); mark();
  /* the upright beetle arrives as square-cut pieces, lands apart, pauses, locks */
  const bug=document.getElementById('beetle'), ps=[...bug.querySelectorAll('.bp')], R=(a,b)=>a+Math.random()*(b-a);
  let anims=[], run=0, flying=false;
  function play(){{
    if(reduce||!bug.animate) return; anims.forEach(a=>a.cancel()); const me=++run; flying=true; bug.classList.add('fly');
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
    Promise.all(anims.map(a=>a.finished)).then(()=>{{ if(me===run){{ flying=false; bug.classList.remove('fly'); }} }}).catch(()=>{{}});
  }}
  play();
  /* one tap: the beetle opens to the moment before the pieces lock - uneven white gaps - holds, then snaps shut */
  function openUp(){{
    if(flying||!bug.animate) return; anims.forEach(a=>a.cancel()); const me=++run; bug.classList.add('fly'); const W=bug.offsetWidth;
    anims=ps.map(p=>{{ const dx=+p.dataset.dx, dy=+p.dataset.dy, n=Math.hypot(dx,dy)||1, g=R(.025,.075)*W, k=Math.max(.55,Math.min(1,n*1.4)), t=`translate(${{dx/n*g*k}}px,${{dy/n*g*k}}px)`;
      return p.animate([{{transform:'none',offset:0,easing:'cubic-bezier(.2,.7,.3,1)'}},{{transform:t,offset:.2}},{{transform:t,offset:.78,easing:'cubic-bezier(.6,0,.4,1.4)'}},{{transform:'none',offset:1}}],{{duration:1900,fill:'both'}}); }});
    Promise.all(anims.map(a=>a.finished)).then(()=>{{ if(me===run) bug.classList.remove('fly'); }}).catch(()=>{{}});
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
  document.querySelectorAll('.tile.bt').forEach(t=>t.addEventListener('click',()=>requestAnimationFrame(ivUpd)));
  /* N / S arrows in the bars: previous / next page */
  /* a tap on a circle, tab or page bar shows first: it lights up for a moment (0.28 s), then the page moves there */
  function tapGo(el,target){{ el.classList.add('hit'); setTimeout(()=>{{ target.scrollIntoView({{behavior:'smooth'}}); setTimeout(()=>el.classList.remove('hit'),500); }},reduce?60:280); }}
  document.querySelectorAll('.pin, .tab').forEach(a=>a.addEventListener('click',e=>{{ const t=document.querySelector(a.getAttribute('href')); if(!t) return; e.preventDefault(); tapGo(a,t); }}));
  /* ?stack=1: the page bars stack - passed pages at the top, pages still to come at the bottom; a tap on a bar goes to its page */
  if(document.body.classList.contains('pairs')){{
    /* ?stack=2: half bars in three rows (about us | projects, downloads & links | bits & bats, contact | start). Each half rises on its own
       when its page arrives and locks in beside its partner like a jigsaw piece; pages still to come wait in their places at the bottom */
    const H=22, bars=[...document.querySelectorAll('.pg .pbar')], secs=bars.map(b=>b.closest('.pg'));
    bars.forEach((b,k)=>{{ const r=k>>1, right=k&1, sec=secs[k];
      sec.before(b);
      b.classList.add('hb', right?'hr':'hl');
      b.style.top=`calc(var(--head) + var(--bar) + ${{r*H}}px)`; b.style.bottom=`calc(var(--bar) + env(safe-area-inset-bottom,0px) + ${{(2-r)*H}}px)`;
      sec.style.scrollMarginTop=(r*H+22)+'px';   /* lands with its own half bar exactly in its place at the top */
      b.setAttribute('role','link'); b.tabIndex=0; b.addEventListener('click',()=>tapGo(b,sec)); }});
    const up=b=>{{ const r=b.getBoundingClientRect(); return r.bottom < innerHeight-parseFloat(getComputedStyle(b).bottom)-3; }};   /* has left the bottom stack */
    const cur=()=>{{ let c=-1; bars.forEach((b,k)=>{{ if(up(b)) c=k; }});
      bars.forEach((b,k)=>b.classList.toggle('on',k===c)); document.body.classList.toggle('inpg',c>=0); }};
    /* white backing behind the stacks, so no page shows through the empty half of a row */
    const bt=document.createElement('div'), bb=document.createElement('div'); bt.className='sback t'; bb.className='sback b'; document.body.append(bt,bb);
    const back=()=>{{ const t0=document.querySelector('.bar.btop').getBoundingClientRect().bottom, b0=document.querySelector('.bar.bbot').getBoundingClientRect().top;
      let tb=t0, bt0=b0;
      bars.forEach(b=>{{ const r=b.getBoundingClientRect(), top=parseFloat(getComputedStyle(b).top), bot=parseFloat(getComputedStyle(b).bottom);
        if(r.top<=top+.5) tb=Math.max(tb,r.bottom); if(r.bottom>=innerHeight-bot-.5) bt0=Math.min(bt0,r.top); }});
      bt.style.top=t0+'px'; bt.style.height=Math.max(0,tb-t0)+'px'; bb.style.top=bt0+'px'; bb.style.height=Math.max(0,b0-bt0)+'px';
      document.body.classList.toggle('tstk',tb>t0+1); document.body.classList.toggle('bstk',bt0<b0-1); }};
    addEventListener('scroll',back,{{passive:true}}); addEventListener('resize',back); back();
    addEventListener('scroll',cur,{{passive:true}}); cur();
  }} else if(document.body.classList.contains('stack')){{
    const H=22, bars=[...document.querySelectorAll('.pg .pbar')], n=bars.length;
    bars.forEach((b,k)=>{{ const sec=b.closest('.pg'); sec.before(b);
      b.style.top=`calc(var(--head) + var(--bar) + ${{k*H}}px)`; b.style.bottom=`calc(var(--bar) + env(safe-area-inset-bottom,0px) + ${{(n-1-k)*H}}px)`;
      sec.style.scrollMarginTop=(k*H+22)+'px'; b.setAttribute('role','link'); b.tabIndex=0;
      b.addEventListener('click',()=>tapGo(b,sec)); }});
    const up=b=>{{ const r=b.getBoundingClientRect(); return r.bottom < innerHeight-parseFloat(getComputedStyle(b).bottom)-3; }};   /* has left the bottom stack */
    const cur=()=>{{ let c=-1; bars.forEach((b,k)=>{{ if(up(b)) c=k; }});
      bars.forEach((b,k)=>b.classList.toggle('on',k===c)); document.body.classList.toggle('inpg',c>=0); }};
    addEventListener('scroll',cur,{{passive:true}}); cur();
  }}
  if(document.body.classList.contains('sec3')){{ const secs=[...document.querySelectorAll('main > section.pg:not(#start)')];
    const mark=()=>{{ const y=innerHeight*.45; let c=null; secs.forEach(x=>{{ if(x.getBoundingClientRect().top<y) c=x; }}); secs.forEach(x=>x.classList.toggle('cur',x===c)); }};
    addEventListener('scroll',mark,{{passive:true}}); mark(); }}
  const pages=[...document.querySelectorAll('.pg')], gN=$('goN'), gS=$('goS');
  const top0=()=>parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0;
  const sm=p=>parseFloat(getComputedStyle(p).scrollMarginTop)||0;
  const curIdx=()=>{{ let i=0; pages.forEach((p,k)=>{{ if(p.getBoundingClientRect().top<=top0()+sm(p)+4) i=k; }}); return i; }};
  const barUpd=()=>{{ const i=curIdx(), atTop=scrollY<4, atEnd=innerHeight+scrollY>=document.documentElement.scrollHeight-4;
    gN.disabled=atTop; gS.classList.toggle('top',atEnd); gS.setAttribute('aria-label',atEnd?'back to the top':'next page'); gS.classList.toggle('go',i===0&&atTop); }};
  gS.onclick=()=>{{ if(gS.classList.contains('top')){{ scrollTo({{top:0,behavior:'smooth'}}); return; }} const i=curIdx(); if(pages[i+1]) pages[i+1].scrollIntoView({{behavior:'smooth'}}); }};
  gN.onclick=()=>{{ const i=curIdx(), off=pages[i].getBoundingClientRect().top-top0()-sm(pages[i]); (off<-8?pages[i]:pages[Math.max(0,i-1)]).scrollIntoView({{behavior:'smooth'}}); }};
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
<script>/* every link to another site opens in a new tab / window, so this site stays open behind it */
(function(){{ const ext=a=>a&&/^https?:/i.test(a.getAttribute('href')||'')&&a.host!==location.host;
  const mark=a=>{{ a.target='_blank'; a.rel='noopener'; }};
  document.querySelectorAll('a[href]').forEach(a=>{{ if(ext(a)) mark(a); }});
  document.addEventListener('click',e=>{{ const a=e.target.closest&&e.target.closest('a[href]'); if(ext(a)) mark(a); }},true); }})();</script>
</body>
</html>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w').write(HTML)
if __name__ == '__main__':
    print(len(pieces), 'pieces,', len(HTML) // 1024, 'KB ->', OUT)
