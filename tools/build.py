"""Assemble the single-page site from the split Figma pages."""
import json
import lightbox as LB   # project pop-up viewer
import bug as BUG
import search as SEARCH   # site search and the map zoom buttons   # start page: the beetle flies in as a collage
ICONS = json.load(open('icons.json'))   # current brand marks (Simple Icons)
S = json.load(open('frag/split.json'))
M = json.load(open('frag/manifest.json'))['contact']   # published paths of the map buttons and marker
ORDER = ['intro', 'services', 'projects', 'downloads', 'bits', 'contact']
ROOT = 'bg-white relative'  # each frame keeps Figma's root styling

sections = []
# Figma's pointer circles + numbers on the intro are redrawn as clean, clickable circles (same size, place and colours)
PIN_NODES = {'1:190', '1:212', '1:215', '1:218', '1:221', '1:210', '1:213', '1:216', '1:219', '1:222'}
for pid in ORDER:
    extra = ''
    items = [h for h in S[pid]["content"] if not any(f'data-node-id="{n}"' in h[:400] for n in ('1:275', '1:47'))]
    if pid != 'intro':
        items = [h.replace('<img ', '<img loading="lazy" decoding="async" ') for h in items]
    if pid == 'intro':
        items = [h for h in items if not any(f'data-node-id="{n}"' in h[:400] for n in PIN_NODES)]
        names = ['us &amp; our services', 'projects', 'downloads &amp; links', 'bits &amp; bats', 'contact']
        sides = ['r', 'l', 'r', 'l', 'l']   # which side of its circle each title sits on
        for (x, y), target, num, nm, sd in zip([(320, 347), (540, 744), (760, 298), (980, 692), (1200, 257)], ORDER[1:], ['01', '02', '03', '04', '05'], names, sides):
            extra += f'<a class="hot pin" href="#{target}" style="left:{x}px;top:{y}px">{num}<svg class="pring" viewBox="0 0 30 30" aria-hidden="true"><circle cx="15" cy="15" r="14.5"/></svg><span class="pl {sd}">{nm}</span></a>'
    if pid == 'downloads':   # every logo + caption opens that organisation's website in a new tab
        LINKS = [[('Kammer der Ziviltechniker:innen W/NÖ/B', 'https://ost.zt.at/'), ('Architects Registration Board', 'https://arb.org.uk/'),
                  ('MA 37 Baupolizei', 'https://www.wien.gv.at/wohnen/baupolizei/'), ('Wiener Rauchfangkehrer', 'https://www.rauchfangkehrer.wien/'),
                  ('Architekturzentrum Wien', 'https://www.azw.at/')],
                 [('nextroom', 'https://www.nextroom.at/'), ('wohnfonds_wien', 'https://www.wohnfonds.wien.at/'),
                  ('OIB', 'https://www.oib.or.at/'), ('Austrian Standards', 'https://www.austrian-standards.at/'), ('ÖGFA', 'https://www.oegfa.at/')],
                 [('Gebietsbetreuung Stadterneuerung', 'https://www.gbstern.at/'), ('Kleingärtner', 'https://www.kleingaertner.at/'),
                  ('Bundesdenkmalamt', 'https://www.bda.gv.at/'), ('IG Architektur', 'https://www.ig-architektur.at/'),
                  ('MA 21 Flächenwidmung', 'https://www.wien.gv.at/stadtentwicklung/flaechenwidmung/')]]
        for col, x in zip(LINKS, (675, 895, 1115)):
            for i, (nm, url) in enumerate(col):
                extra += f'<a class="hot lk" href="{url}" target="_blank" rel="noopener" aria-label="{nm} (opens in a new tab)" style="left:{x}px;top:{438 + 110 * i}px"></a>'
    if pid == 'bits':   # Steuart's own photos instead of the pictures repeated from the projects and services pages
        BITS = {'projects-imgDdLogoWithTextFinal13.webp': 'p-drawing-grille.webp', 'services-imgImage1-tall.webp': 'p-akh-crate.webp', 'projects-imgImage3.webp': 'p-scaffolding.webp', 'intro-imgImage.webp': 'p-streaks-white-blue.webp', 'projects-imgImage7.webp': 'p-pocket-watch.webp', 'projects-imgImage1.webp': 'p-barriers-night.webp', 'projects-imgDdLogoWithTextFinal14.webp': 'p-cages-night.webp', 'projects-imgImage2.webp': 'p-plastic-sheet.webp', 'projects-imgImage6.webp': 'p-section-grey.webp', 'projects-imgImage5.webp': 'p-tower-drawing-blue.webp', 'projects-imgImage8.webp': 'p-streaks-orange.webp'}
        for a, c in BITS.items():
            items = [h.replace('object-contain', 'object-cover').replace('img/' + a, 'img/' + c) if 'img/' + a in h else h for h in items]
    if pid == 'projects':   # each project tile opens the pop-up viewer
        extra += LB.TILES
        # "WHO IS THIS GUY?" shows Steuart's straw drawing (the ID card appears only on the services page)
        items = [h.replace('src="img/services-imgImage1.webp"', 'src="img/p-straw-drawing.webp"') for h in items]
    if pid == 'intro':   # beetle collage pieces, over the beetle
        extra += BUG.HTML
    sections.append(f'<section class="pg" id="{pid}"><div class="{ROOT} frame">{"".join(items)}{extra}</div></section>')

chromes = ''.join(f'<div class="chrome{" on" if pid == "intro" else ""}" data-pg="{pid}">{"".join(h for h in S[pid]["chrome"] if "inset-[95.7%_6.25%_2.83%_92.71%]" not in h[:300])}</div>' for pid in ORDER)
labels = ['us &amp; our services', 'projects', 'downloads &amp; links', 'bits &amp; bats', 'contact']
hot = ''.join(f'<a class="hot tab" href="#{pid}" style="left:{235 + 220 * i}px;top:0;width:200px;height:25px" aria-label="{labels[i]}"></a>' for i, pid in enumerate(ORDER[1:]))
hot += ('<a class="hot nextp" id="nextp" href="#services" style="left:745px;top:998px;width:90px;height:24px" aria-label="next page">'
        + LB.compass('S', 22, 'cs') + LB.compass('N', 22, 'cn') +
        '<span>scroll</span></a>')
SOCIAL = [('facebook', 'Facebook', 60, '#0866FF', ''), ('instagram', 'Instagram', 96, 'url(#igrad)', ''), ('x', 'X (Twitter)', 132, '#000000', '')]
hot += ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><radialGradient id="igrad" cx="30%" cy="107%" r="150%">'
        '<stop offset="0" stop-color="#fdf497"/><stop offset=".05" stop-color="#fdf497"/><stop offset=".45" stop-color="#fd5949"/>'
        '<stop offset=".6" stop-color="#d6249f"/><stop offset=".9" stop-color="#285AEB"/></radialGradient></defs></svg>')
for key, label, y, fill, url in SOCIAL:   # url: fill in the profile address when the accounts exist
    hot += (f'<a class="hot social" href="{url or "#"}" data-pending="{0 if url else 1}" aria-label="{label}" style="left:1335px;top:{y}px;width:25px;height:25px">'
            f'<svg viewBox="0 0 24 24" width="16" height="16"><path fill="{fill}" d="{ICONS[key]}"/></svg></a>')
hot += SEARCH.BUTTON   # thin red magnifier + search pop-up
hot += '<a class="hot" href="#intro" style="left:115px;top:0;width:110px;height:365px" aria-label="dasein-design home"></a>'

html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="icon" type="image/png" href="icon-192.png"><meta name="theme-color" content="#ffffff"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="dasein-design">
<title>dasein-design Big Stripes</title>
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="figma.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" data-live-map>
<style>
html,body{{margin:0;height:100%;overflow:hidden;background:#fff}}
html,body,button,input,select,textarea,dialog{{font-family:Calibri,Carlito,sans-serif}}   /* one font everywhere, buttons included */
.strip{{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}}
.holder{{position:relative;flex:none;width:calc(1440px * var(--s,.5));height:calc(1024px * var(--s,.5))}}
.stage{{position:absolute;left:0;top:0;width:1440px;height:1024px;transform:scale(var(--s,.5));transform-origin:0 0;background:#fff;overflow:hidden}}
.scroller{{position:absolute;inset:0;overflow-y:auto;overflow-x:hidden;scroll-snap-type:y mandatory;scrollbar-width:none;overscroll-behavior:contain}}
.scroller::-webkit-scrollbar{{display:none}}
.pg{{position:relative;width:1440px;height:1024px;scroll-snap-align:start;scroll-snap-stop:always;overflow:hidden}}
.frame{{position:absolute;inset:0;width:1440px;height:1024px}}
.mask{{position:absolute;background:#fff;pointer-events:none}}
.chrome{{position:absolute;inset:0;pointer-events:none;visibility:hidden}}
.chrome.on{{visibility:visible}}
.hot{{position:absolute;display:block;z-index:5}}
/* menu bar: no drop shadow under the labels; the tab under the mouse gets a red label and a red frame */
[class*="text-shadow-"]{{text-shadow:none!important}}   /* no blurred Figma drop shadows anywhere */
.hot.tab:hover,.hot.tab:focus-visible{{box-shadow:inset 0 0 0 calc(1px / var(--s,1)) #e30613;outline:none}}
.hot.tab.cur:hover,.hot.tab.cur:focus-visible{{box-shadow:none}}
/* the tab of the page you are on: bold label in red, no frame */
.chrome[data-pg="services"] [class*="w-[190px]"][class*="left-[335px]"]{{color:#e30613!important}}
.chrome[data-pg="projects"] [class*="w-[190px]"][class*="left-[555px]"]{{color:#e30613!important}}
.chrome[data-pg="downloads"] [class*="w-[190px]"][class*="left-[775px]"]{{color:#e30613!important}}
.chrome[data-pg="bits"] [class*="w-[190px]"][class*="left-[995px]"]{{color:#e30613!important}}
.chrome[data-pg="contact"] [class*="w-[190px]"][class*="left-[1215px]"]{{color:#e30613!important}}


.hot.pin{{width:30px;height:30px;box-sizing:border-box;border-radius:50%;border:calc(1px / var(--s,1)) solid #000;background:#bfbfbf;
  display:flex;align-items:center;justify-content:center;font:400 18px/1 Calibri,Carlito,sans-serif;color:#000;text-decoration:none;z-index:6;transition:background .15s}}
.pin .pl{{position:absolute;top:50%;transform:translateY(-50%);white-space:nowrap;font:400 15px/1 Calibri,Carlito,sans-serif;color:#000;padding:4px 0}}
.pin .pl.r{{left:calc(100% + 9px)}} .pin .pl.l{{right:calc(100% + 9px)}}
.hot.pin:hover .pl,.hot.pin:focus-visible .pl{{color:#e30613}}
/* numbered circles: the ring is a vector circle (even in every browser, unlike a border on the scaled page);
   when the pointer comes near, the circle sends out thin red rings */
.hot.pin{{border:0!important}}
.pin .pring{{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}}
.pin .pring circle{{fill:none;stroke:#000;stroke-width:1;vector-effect:non-scaling-stroke}}
.hot.pin:hover .pring circle,.hot.pin:focus-visible .pring circle,.hot.pin:active .pring circle{{stroke:#e30613}}
.hot.pin::before,.hot.pin::after{{content:"";position:absolute;inset:0;border-radius:50%;pointer-events:none;opacity:0;
  border:calc(1px / (var(--s,1) * var(--dpr,1))) solid #e30613}}
.hot.pin.near::before,.hot.pin.near::after{{animation:pinring 1.5s ease-out infinite}}
.hot.pin.near::after{{animation-delay:.75s}}
.hot.pin.near{{animation:pinpulse 1.5s ease-in-out infinite}}
@keyframes pinring{{from{{transform:scale(1);opacity:.8}}to{{transform:scale(2.1);opacity:0}}}}
@keyframes pinpulse{{50%{{transform:scale(1.07)}}}}
/* menu tabs: on hover, or with the pointer close below, the tab (grey box and label) bobs gently down a little;
   the top edge stays where it is; not the current page's tab */
.stage[data-bob="0"] .chrome.on [class*="left-[235px]"][class*="h-[25px]"][class*="bg-"],.stage[data-bob="0"] .chrome.on [class*="w-[190px]"][class*="left-[335px]"],.stage[data-bob="0"] .hot.tab[href]:nth-of-type(1),
.stage[data-bob="1"] .chrome.on [class*="left-[455px]"][class*="h-[25px]"][class*="bg-"],.stage[data-bob="1"] .chrome.on [class*="w-[190px]"][class*="left-[555px]"],.stage[data-bob="1"] .hot.tab[href]:nth-of-type(2),
.stage[data-bob="2"] .chrome.on [class*="left-[675px]"][class*="h-[25px]"][class*="bg-"],.stage[data-bob="2"] .chrome.on [class*="w-[190px]"][class*="left-[775px]"],.stage[data-bob="2"] .hot.tab[href]:nth-of-type(3),
.stage[data-bob="3"] .chrome.on [class*="left-[895px]"][class*="h-[25px]"][class*="bg-"],.stage[data-bob="3"] .chrome.on [class*="w-[190px]"][class*="left-[995px]"],.stage[data-bob="3"] .hot.tab[href]:nth-of-type(4),
.stage[data-bob="4"] .chrome.on [class*="left-[1115px]"][class*="h-[25px]"][class*="bg-"],.stage[data-bob="4"] .chrome.on [class*="w-[190px]"][class*="left-[1215px]"],.stage[data-bob="4"] .hot.tab[href]:nth-of-type(5){{animation:tabbob 1.1s ease-in-out infinite}}
@keyframes tabbob{{0%,100%{{transform:translateY(0)}}45%{{transform:translateY(3px)}}65%{{transform:translateY(1.5px)}}}}
/* hover is a passing state: the tab box (and a numbered circle) turns lime green; the current page keeps its yellow-lime; the label stays as it is */
.stage[data-bob="0"] .chrome.on [class*="left-[235px]"][class*="h-[25px]"][class*="bg-"],
.stage[data-bob="1"] .chrome.on [class*="left-[455px]"][class*="h-[25px]"][class*="bg-"],
.stage[data-bob="2"] .chrome.on [class*="left-[675px]"][class*="h-[25px]"][class*="bg-"],
.stage[data-bob="3"] .chrome.on [class*="left-[895px]"][class*="h-[25px]"][class*="bg-"],
.stage[data-bob="4"] .chrome.on [class*="left-[1115px]"][class*="h-[25px]"][class*="bg-"]{{background:#a5e35a!important;transition:background .15s}}
@media (prefers-reduced-motion:reduce){{.stage[data-bob] *{{animation-name:none!important}}}}
.pinnear .ihint .ilab{{display:none}}
@media (prefers-reduced-motion:reduce){{.hot.pin.near,.hot.pin.near::before,.hot.pin.near::after{{animation:none}}}}
.hot.pin:hover,.hot.pin:focus-visible,.hot.pin:active{{background:#a5e35a;font-weight:700;z-index:7;border:calc(1px / var(--s,1)) solid #e30613;outline:none}}
.hot:focus-visible{{outline:2px solid red;outline-offset:2px}}
/* social links: current brand marks in their own colours (Figma's old icons are hidden) */
.chrome [data-name="Facebook"],.chrome [data-name="Instagram"],.chrome [data-name="Twitter Squared"]{{display:none}}
.social{{display:flex;align-items:center;justify-content:center;border-radius:4px}}
.social:hover{{box-shadow:inset 0 0 0 calc(1px / var(--s,1)) #e30613}}
/* vertical section titles: the light "&" and the number in red; a quiet slide-in when you arrive on a page */
/* vertical titles run from the foot of the side bar up to the top of the grey text block (y 430); the [number] is as big as the words and ends level with it */
.chrome [class*="h-[560px]"][class*="w-[84px]"][class*="top-[1000px]"]{{height:570px!important}}
.chrome [class*="h-[560px]"][class*="w-[84px]"][class*="top-[1003px]"]{{height:573px!important}}
.chrome [class*="h-[560px]"][class*="w-[84px]"][class*="top-[1000px]"] [class*="w-[560px]"]{{width:570px!important}}
.chrome [class*="h-[560px]"][class*="w-[84px]"][class*="top-[1003px]"] [class*="w-[560px]"]{{width:573px!important}}
.chrome [class*="w-[560px]"] > p{{display:flex;align-items:baseline;white-space:pre;margin:0}}
.chrome [class*="w-[560px]"] > p > span[class*="text-[20px]"]{{font-size:40px!important;margin-left:auto}}
/* start page: the projects tab grey like the others (Figma had it lime) */
.chrome[data-pg="intro"] [class*="left-[455px]"][class*="h-[25px]"][class*="bg-"]{{background:rgba(0,0,0,.05)!important}}
.chrome[data-pg="intro"] [class*="w-[190px]"][class*="left-[555px]"] .fcal-b{{font-weight:400!important;font-size:15px!important}}

/* bits & bats: the tall AKH 1 photo sits underneath its caption bar */
#bits img[src="img/p-akh-crate.webp"]{{z-index:-1}}
#bits .frame{{isolation:isolate}}
.chrome [class*="w-[560px]"] .fcal-l,.chrome [class*="w-[560px]"] span[class*="text-[20px]"]{{color:#e30613}}
.chrome.arrive [class*="h-[560px]"][class*="w-[84px]"]{{animation:arrive .9s cubic-bezier(.2,.7,.2,1) both}}
@keyframes arrive{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{.chrome.arrive [class*="h-[560px]"][class*="w-[84px]"]{{animation:none}}}}
.hot.lk{{width:200px;height:100px}}
.hot.lk::before{{content:"";position:absolute;left:0;top:0;width:200px;height:50px}}
.hot.lk:hover::before,.hot.lk:focus-visible::before{{box-shadow:inset 0 0 0 calc(1px / var(--s,1)) #e30613}}
/* services: section headings in red, to match their red symbols */
[data-node-id="1:554"] > p:first-child,[data-node-id="1:628"] > p:first-child,[data-node-id="1:633"] > p:first-child,[data-node-id="1:634"] > p:first-child{{color:#e30613}}
/* arrow to the next page, with its label; on the last page it points up and leads back to the start */
.nextp{{display:flex;align-items:center;gap:6px;text-decoration:none;color:#666;font:400 11px/1 Calibri,Carlito,sans-serif;letter-spacing:.06em;padding-left:20px}}
.nextp:hover{{color:#e30613}}
.nextp .cn,.nextp.up .cs{{display:none}} .nextp.up .cn{{display:block}}   /* S: on to the next page; N on the last page: back to the top */
/* first visit to the intro: the arrow nudges downwards and the label invites you in, until you first move on */
.nextp.hint svg{{animation:nudge 1.3s ease-in-out infinite}}
.nextp.hint span{{color:#e30613;animation:glow 1.3s ease-in-out infinite}}
@keyframes nudge{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(4px)}}}}
@keyframes glow{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
@media (prefers-reduced-motion:reduce){{.nextp.hint svg,.nextp.hint span{{animation:none}}}}
.gl{{position:absolute;left:0;top:0;pointer-events:none;z-index:30}}
/* frames around images: light dotted, one screen pixel; only the main grid lines are dashed */
.frame .border-dashed.border-black{{border-width:0!important}}
.frame .border-dashed.border-black::after{{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;
  --c:#b8b8b8;--d:var(--w);--p:calc(var(--w) * 3);--w:calc(1px / (var(--s,1) * var(--dpr,1)));
  background:
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/100% var(--w) no-repeat,
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left bottom/100% var(--w) no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/var(--w) 100% no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) right top/var(--w) 100% no-repeat}}
.gl i{{position:absolute;display:block}}
/* live map on the contact page: OpenStreetMap, zoomable, with the dasein-design marker */
.mapclip{{position:absolute;overflow:hidden;z-index:20;pointer-events:none}}
.mapwrap{{position:absolute;pointer-events:auto;background:#e8e4dc}}
#livemap{{position:absolute;inset:0;background:#e8e4dc}}
.mz{{position:absolute;z-index:500;display:flex;flex-direction:column;gap:1px}}
.mz button{{padding:0;margin:0;border:1px dotted #b8b8b8;background:#fff;cursor:pointer;display:block}}
.mz button img{{display:block;width:100%;height:100%}}
.mz button:hover{{border:1px solid #e30613}}
.pinH{{position:relative}}
.pinsvg{{display:block;width:100%;height:100%;overflow:visible}}
.pinsvg .pb{{fill:#3a3c37}}
.pinsvg .pw{{fill:#fff}}
.pinsvg .pr{{fill:none;stroke:#3a3c37;stroke-width:1;vector-effect:non-scaling-stroke}}
.pinsvg .pa{{fill:#4d4f4a;stroke:#1a1a1a;stroke-width:1;vector-effect:non-scaling-stroke;stroke-linejoin:round}}
.pinsvg text{{fill:#3a3c37;font:700 6.4px Calibri,Carlito,sans-serif;text-anchor:middle;dominant-baseline:central}}
/* address label: top right of the pin; it moves to the other side or below as the pin nears the map's edges */
.plab{{position:absolute;left:calc(100% + .35em);bottom:62%;white-space:nowrap;background:rgba(255,255,255,.92);color:#000;
  font-family:Calibri,Carlito,sans-serif;font-weight:400;line-height:1.25;padding:.3em .55em;text-align:left}}
.plab b{{font-weight:700}}
.pinH.l .plab{{left:auto;right:calc(100% + .35em)}}
.pinH.b .plab{{bottom:auto;top:30%}}
.leaflet-container .leaflet-control-attribution{{font:10px/1.3 Calibri,Carlito,sans-serif;background:rgba(255,255,255,.7)}}
{LB.CSS}{BUG.CSS}{SEARCH.CSS}</style>
</head>
<body>
<div class="strip"><div class="holder" id="holder">
<div class="stage" id="stage">
<div class="scroller" id="scroller">{"".join(sections)}</div>
<div class="mask" style="left:0;top:0;width:225px;height:1024px"></div>
<div class="mask" style="left:1325px;top:0;width:115px;height:1024px"></div>
<div class="mask" style="left:225px;top:0;width:1100px;height:32px"></div>
{chromes}
<div class="hotlayer">{hot}</div>
</div>
<canvas class="gl" id="gl"></canvas>
<div class="mapclip" id="mapclip" hidden><div class="mapwrap" id="mapwrap"><div id="livemap"></div>
<div class="mz" id="mz"><button id="zin" aria-label="Zoom in">{SEARCH.ZOOM_IN}</button><button id="zout" aria-label="Zoom out">{SEARCH.ZOOM_OUT}</button><button id="zhome" aria-label="Back to the start view" title="back to the start view">{SEARCH.ZOOM_HOME}</button></div></div></div>
</div></div>
{LB.HTML}
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" data-live-map></script>
<script>
(function(){{
  const sc=document.getElementById('scroller'), pgs=[...sc.children];
  const chromes=[...document.querySelectorAll('.chrome')];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function go(id,instant){{const el=document.getElementById(id); if(el) sc.scrollTo({{top:el.offsetTop,behavior:(instant||reduce)?'auto':'smooth'}});}}
  document.addEventListener('click',e=>{{const a=e.target.closest('a[href^="#"]'); if(!a) return; e.preventDefault(); if(a.dataset.pending==='1') return; go(a.getAttribute('href').slice(1)); history.replaceState(null,'',a.getAttribute('href'));}});
  let cur='', moved=false;
  const stage=document.getElementById('stage');
  document.querySelectorAll('.hot.tab').forEach((t,i)=>{{
    const on=()=>stage.dataset.hover=i, off=()=>delete stage.dataset.hover;
    t.addEventListener('mouseenter',on); t.addEventListener('mouseleave',off); t.addEventListener('focus',on); t.addEventListener('blur',off);
  }});
  function update(){{
    const i=Math.max(0,Math.min(pgs.length-1,Math.round(sc.scrollTop/1024))), id=pgs[i].id;
    if(id===cur) return; if(cur==='contact'&&map) homeView(); /* leaving the contact page resets the map */ cur=id; document.dispatchEvent(new CustomEvent('pagechange',{{detail:id}})); chromes.forEach(c=>{{c.classList.toggle('on',c.dataset.pg===id); c.classList.remove('arrive');}}); const ch=chromes.find(c=>c.dataset.pg===id); void ch.offsetWidth; ch.classList.add('arrive'); const nx=document.getElementById('nextp'), k=pgs.findIndex(p=>p.id===id), last=k===pgs.length-1; nx.setAttribute('href','#'+(last?pgs[0].id:pgs[k+1].id)); nx.classList.toggle('up',last); if(id!=='intro') moved=true; const hint=id==='intro'&&!moved; nx.classList.toggle('hint',hint); nx.style.width=hint?'200px':'90px'; nx.lastChild.textContent=last?'top':(hint?'scroll or click the menu':'scroll'); document.querySelectorAll('.hot.tab').forEach(t=>t.classList.toggle('cur',t.getAttribute('href')==='#'+id));
  }}
  sc.addEventListener('scroll',update,{{passive:true}});
  /* the page always scales itself to fit the window, so block browser zoom (Ctrl/Cmd + wheel, Ctrl/Cmd + plus/minus) */
  addEventListener('wheel',e=>{{ if(e.ctrlKey||e.metaKey) e.preventDefault(); }},{{passive:false}});
  addEventListener('keydown',e=>{{ if((e.ctrlKey||e.metaKey)&&['+','-','=','_'].includes(e.key)) e.preventDefault(); }});
  addEventListener('keydown',e=>{{
    if(document.getElementById('lb').open) return;   /* the project pop-up has its own keys */
    const d={{ArrowDown:1,PageDown:1,ArrowRight:1,' ':1,ArrowUp:-1,PageUp:-1,ArrowLeft:-1}}[e.key]; if(!d) return;
    e.preventDefault(); const i=Math.round(sc.scrollTop/1024)+d; go(pgs[Math.max(0,Math.min(pgs.length-1,i))].id);
  }});
  let S=1, map=null;
  function fit(){{
    const s=Math.min(innerWidth/1440,innerHeight/1024); S=s;
    document.documentElement.style.setProperty('--s',s);
    /* light grey dashed guide lines and tick marks, drawn on a canvas over everything in whole screen pixels,
       so every line is exactly one pixel thin and every dash is the same length */
    const dpr=devicePixelRatio||1, cv=document.getElementById('gl');
    document.documentElement.style.setProperty('--dpr',dpr);
    const W=Math.round(1440*s*dpr), H=Math.round(1024*s*dpr);
    cv.width=W; cv.height=H; cv.style.width=(W/dpr)+'px'; cv.style.height=(H/dpr)+'px';
    const g=cv.getContext('2d'); g.clearRect(0,0,W,H); g.fillStyle='#c4c4c4';
    const k=s*dpr, dash=Math.max(2,Math.round(5*k)), gap=Math.max(1,Math.round(2.5*k));
    [115,225,445,665,885,1105,1325].forEach(x=>{{const X=Math.round(x*k); for(let y=0;y<H;y+=dash+gap) g.fillRect(X,y,1,Math.min(dash,H-y));}});
    [25,50,60,240,250,430,440,620,630,810,820,1000,1010].forEach(y=>[105,1325].forEach(x=>{{
      const Y=Math.round(y*k), X0=Math.round(x*k), X1=Math.round((x+10)*k);
      for(let X=X0;X<X1;X+=dash+gap) g.fillRect(X,Y,Math.min(dash,X1-X),1);}}));
  }}
  /* live map: positioned over the contact page's map area, scrolling with it, clipped to the content area */
  const HOME=[48.211431,16.333964], clip=document.getElementById('mapclip'), wrap=document.getElementById('mapwrap'), contact=document.getElementById('contact');
  function placeMap(){{
    if(!map) return;
    const s=S, y=(contact.offsetTop-sc.scrollTop+440-32)*s;
    clip.style.cssText=`left:${{225*s}}px;top:${{32*s}}px;width:${{1100*s}}px;height:${{992*s}}px`;
    wrap.style.cssText=`left:${{230*s}}px;top:${{y}}px;width:${{860*s}}px;height:${{560*s}}px`;
    const mz=document.getElementById('mz'); mz.style.cssText=`left:${{826*s}}px;top:${{240*s}}px`;   /* a little in from the map's right edge */
    mz.querySelectorAll('button').forEach(b=>{{b.style.width=b.style.height=(25*s)+'px';}});
  }}
  const VIEW=[48.211114,16.337330], VIEW_ZOOM=17;   // default view chosen by Steuart
  function homeView(z){{ map.invalidateSize(); map.setView(VIEW,z||VIEW_ZOOM,{{animate:false}}); }}
  function marker(){{
    const s=S, W=34*s, H=44*s;
    return L.divIcon({{className:'',iconSize:[W,H],iconAnchor:[W/2,H],
      html:`<div class="pinH" style="width:${{W}}px;height:${{H}}px;font-size:${{12*s}}px"><svg class="pinsvg" viewBox="0 0 40 52" aria-hidden="true"><path class="pb" d="M20 51C14.5 40.5 2 31 2 19A18 18 0 0 1 38 19C38 31 25.5 40.5 20 51Z"/><circle class="pw" cx="20" cy="19" r="14.5"/><g transform="translate(20 19) scale(1.12)"><path class="pr" d="M-5.31 7.88A9.5 9.5 0 1 1 5.31 7.88"/><path class="pa" transform="rotate(90)" d="M5.4 0L-4.6 -4.9L-2.2 0L-4.6 4.9Z"/><text x="0.00" y="9.50">H</text></g></svg><div class="plab"><b>dasein-design</b><br>Neulerchenfelderstrasse 42/6<br>A-1160 Wien</div></div>`}});
  }}
  /* keep the address label inside the map: right of the pin by default, left near the right edge, below near the top */
  function flipLabel(){{
    const el=pin&&pin.getElement(); if(!el) return; const box=el.querySelector('.pinH'), lab=el.querySelector('.plab'); if(!box||!lab) return;
    const pt=map.latLngToContainerPoint(HOME), sz=map.getSize(), W=box.offsetWidth, H=box.offsetHeight, lw=lab.offsetWidth, lh=lab.offsetHeight, m=6;
    box.classList.toggle('l', pt.x+W/2+lw+m>sz.x && pt.x-W/2-lw-m>0);
    box.classList.toggle('b', pt.y-H*.62-lh-m<0);
  }}
  let pin=null;
  /* page first: scale it, show the menus and side bars; the map is added afterwards so it can never stop the page */
  fit(); addEventListener('resize',()=>{{fit(); try{{ if(map){{placeMap(); homeView(map.getZoom()); pin.setIcon(marker()); flipLabel();}} }}catch(err){{console.warn(err);}} }});
  if(location.hash) go(location.hash.slice(1),true);
  update();
  try{{ {LB.JS} }}catch(err){{ console.warn('project viewer not available',err); }}
{BUG.JS}

  /* numbered circles pulse when the pointer comes within about 80 px */
  try{{
    const pins=[...document.querySelectorAll('.hot.pin')], st=document.getElementById('stage'), intro=document.getElementById('intro');
    if(pins.length && !reduce){{
      const C=pins.map(a=>[a.offsetLeft+15,a.offsetTop+15]);
      addEventListener('mousemove',e=>{{
        if(cur!=='intro'){{ pins.forEach(a=>a.classList.remove('near')); return; }}
        const r=st.getBoundingClientRect(), s=r.width/1440, x=(e.clientX-r.left)/s, y=(e.clientY-r.top)/s+sc.scrollTop-intro.offsetTop;
        let any=false; pins.forEach((a,i)=>{{ const n=Math.hypot(x-C[i][0],y-C[i][1])<80; a.classList.toggle('near',n); any=any||n; }});
        document.body.classList.toggle('pinnear',any);   /* near a circle its own label says it all: the hint note steps aside */
      }},{{passive:true}});
      document.addEventListener('mouseleave',()=>pins.forEach(a=>a.classList.remove('near')));
    }}
  }}catch(err){{ console.warn('pin pulse skipped',err); }}

  /* menu tabs bob down a little on hover or when the pointer comes close below them (within about 45 px) */
  try{{
    const tabs=[...document.querySelectorAll('.hot.tab')], st=document.getElementById('stage');
    if(tabs.length && !reduce){{
      const T=tabs.map(a=>[a.offsetLeft,a.offsetLeft+a.offsetWidth,a.offsetTop+a.offsetHeight]);
      addEventListener('mousemove',e=>{{
        const lbo=document.getElementById('lb'); if(lbo&&lbo.open){{ delete st.dataset.bob; return; }}
        const r=st.getBoundingClientRect(), s=r.width/1440, x=(e.clientX-r.left)/s, y=(e.clientY-r.top)/s;
        const k=tabs.findIndex((a,i)=>!a.classList.contains('cur')&&x>T[i][0]-20&&x<T[i][1]+20&&y>=0&&y<T[i][2]+45);
        if(k<0) delete st.dataset.bob; else st.dataset.bob=k;
      }},{{passive:true}});
      document.addEventListener('mouseleave',()=>{{ delete st.dataset.bob; }});
    }}
  }}catch(err){{ console.warn('tab ripple skipped',err); }}
{SEARCH.JS}
  try{{
    if(window.L){{
      clip.hidden=false; placeMap();
      map=L.map('livemap',{{zoomControl:false,scrollWheelZoom:false,attributionControl:true}});
      L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}}).addTo(map);
      map.attributionControl.setPrefix(false);
      placeMap(); homeView();
      pin=L.marker(HOME,{{icon:marker(),keyboard:false}}).addTo(map); map.on('move zoom resize',flipLabel); flipLabel();
      document.getElementById('zin').onclick=()=>map.zoomIn();
      document.getElementById('zout').onclick=()=>map.zoomOut();
      document.getElementById('zhome').onclick=()=>map.flyTo(VIEW,VIEW_ZOOM,{duration:reduce?0:.6});   /* back to the start view */
      sc.addEventListener('scroll',placeMap,{{passive:true}});
      /* the map sits above the pages, so pass mouse-wheel scrolling on to the pages underneath */
      wrap.addEventListener('wheel',e=>{{e.preventDefault(); sc.scrollBy({{top:e.deltaY/S}});}},{{passive:false}});
    }}
  }}catch(err){{ console.warn('map not available',err); clip.hidden=true; map=null; }}
}})();
</script>
</body>
</html>
'''
html = html.replace('img/services-imgPdf.webp', 'img/pdf.svg')   # Steuart's PDF symbol, redrawn without the shadow
html = html.replace('> 2022<', '>© 2026<')   # copyright year, with © as real text instead of Figma's little picture
import fromphone   # the changes first made on the phone version (21 Oct 2026)
html = fromphone.patch(html)
open('site/index.html', 'w').write(html)
print(len(html))
