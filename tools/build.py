"""Assemble the single-page site from the split Figma pages."""
import json
import lightbox as LB   # project pop-up viewer
import bug as BUG   # start page: the beetle flies in as a collage
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
            extra += f'<a class="hot pin" href="#{target}" style="left:{x}px;top:{y}px">{num}<span class="pl {sd}">{nm}</span></a>'
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
    if pid == 'projects':   # each project tile opens the pop-up viewer
        extra += LB.TILES
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
hot += '<a class="hot" href="#intro" style="left:115px;top:0;width:110px;height:365px" aria-label="dasein-design home"></a>'

html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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

.stage[data-hover="0"] .chrome.on [class*="w-[190px]"][class*="left-[335px]"]{{color:#e30613!important}}
.stage[data-hover="1"] .chrome.on [class*="w-[190px]"][class*="left-[555px]"]{{color:#e30613!important}}
.stage[data-hover="2"] .chrome.on [class*="w-[190px]"][class*="left-[775px]"]{{color:#e30613!important}}
.stage[data-hover="3"] .chrome.on [class*="w-[190px]"][class*="left-[995px]"]{{color:#e30613!important}}
.stage[data-hover="4"] .chrome.on [class*="w-[190px]"][class*="left-[1215px]"]{{color:#e30613!important}}

.hot.pin{{width:30px;height:30px;box-sizing:border-box;border-radius:50%;border:calc(1px / var(--s,1)) solid #000;background:#bfbfbf;
  display:flex;align-items:center;justify-content:center;font:400 18px/1 Calibri,Carlito,sans-serif;color:#000;text-decoration:none;z-index:6;transition:background .15s}}
.pin .pl{{position:absolute;top:50%;transform:translateY(-50%);white-space:nowrap;font:400 15px/1 Calibri,Carlito,sans-serif;color:#000;padding:4px 0}}
.pin .pl.r{{left:calc(100% + 9px)}} .pin .pl.l{{right:calc(100% + 9px)}}
.hot.pin:hover .pl,.hot.pin:focus-visible .pl{{color:#e30613}}
.hot.pin:hover,.hot.pin:focus-visible,.hot.pin:active{{background:#d4fb4d;font-weight:700;z-index:7;border:calc(1px / var(--s,1)) solid #e30613;outline:none}}
.hot:focus-visible{{outline:2px solid red;outline-offset:2px}}
/* social links: current brand marks in their own colours (Figma's old icons are hidden) */
.chrome [data-name="Facebook"],.chrome [data-name="Instagram"],.chrome [data-name="Twitter Squared"]{{display:none}}
.social{{display:flex;align-items:center;justify-content:center;border-radius:4px}}
.social:hover{{box-shadow:inset 0 0 0 calc(1px / var(--s,1)) #e30613}}
/* vertical section titles: the light "&" and the number in red; a quiet slide-in when you arrive on a page */
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
/* frames around images: light dotted, one and a quarter screen pixels; only the main grid lines are dashed */
.frame .border-dashed.border-black{{border-width:0!important}}
.frame .border-dashed.border-black::after{{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;
  --c:#cbcbcb;--d:var(--w);--p:calc(var(--w) * 3);--w:calc(1.25px / (var(--s,1) * var(--dpr,1)));
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
.mz button{{padding:0;margin:0;border:1.25px dotted #cbcbcb;background:#fff;cursor:pointer;display:block}}
.mz button img{{display:block;width:100%;height:100%}}
.mz button:hover{{border:1px solid #e30613}}
.pin42{{position:relative;text-align:center;font-family:Calibri,Carlito,sans-serif;font-weight:700;color:#000}}
.pin42 img{{display:block;margin:0 auto}}
.leaflet-container .leaflet-control-attribution{{font:10px/1.3 Calibri,Carlito,sans-serif;background:rgba(255,255,255,.7)}}
{LB.CSS}{BUG.CSS}</style>
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
<div class="mz" id="mz"><button id="zin" aria-label="Zoom in"><img src="{M['imgZoomIn']}" alt=""></button><button id="zout" aria-label="Zoom out"><img src="{M['imgZoomOut']}" alt=""></button></div></div></div>
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
    const mz=document.getElementById('mz'); mz.style.cssText=`left:${{835*s}}px;top:${{252*s}}px`;
    mz.querySelectorAll('button').forEach(b=>{{b.style.width=b.style.height=(25*s)+'px';}});
  }}
  const VIEW=[48.211114,16.337330], VIEW_ZOOM=17;   // default view chosen by Steuart
  function homeView(z){{ map.invalidateSize(); map.setView(VIEW,z||VIEW_ZOOM,{{animate:false}}); }}
  function marker(){{
    const s=S;
    return L.divIcon({{className:'',iconSize:[25*s,52*s],iconAnchor:[12.5*s,35*s],
      html:`<div class="pin42" style="width:${{25*s}}px;font-size:${{12*s}}px"><img src="img/contact-imgVector.svg" alt="" style="width:${{25*s}}px;height:${{35*s}}px">42/6</div>`}});
  }}
  let pin=null;
  /* page first: scale it, show the menus and side bars; the map is added afterwards so it can never stop the page */
  fit(); addEventListener('resize',()=>{{fit(); try{{ if(map){{placeMap(); homeView(map.getZoom()); pin.setIcon(marker());}} }}catch(err){{console.warn(err);}} }});
  if(location.hash) go(location.hash.slice(1),true);
  update();
  try{{ {LB.JS} }}catch(err){{ console.warn('project viewer not available',err); }}
{BUG.JS}
  try{{
    if(window.L){{
      clip.hidden=false; placeMap();
      map=L.map('livemap',{{zoomControl:false,scrollWheelZoom:false,attributionControl:true}});
      L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}}).addTo(map);
      map.attributionControl.setPrefix(false);
      placeMap(); homeView();
      pin=L.marker(HOME,{{icon:marker(),keyboard:false}}).addTo(map);
      document.getElementById('zin').onclick=()=>map.zoomIn();
      document.getElementById('zout').onclick=()=>map.zoomOut();
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
open('site/index.html', 'w').write(html)
print(len(html))
