"""Project pop-up viewer (lightbox) for the projects page.

A native <dialog>. Only the main content area gets a very light white veil and a soft blur, so the side bars,
the vertical title and the menu stay sharp; the dashed column lines are redrawn sharp over the veil.
The pop-up sits centred in the main area: the photo, the title and text beside it with the project
details underneath, and a strip of the project's photos below for quick navigation.
build.py imports TILES, CSS, HTML and JS from here.

To add real photos: put them in img/ (named after their caption, up to 1600 px), then list them under
the project's "imgs" - the first one is the photo shown on the tile.
To fill in the details: set "d" for the project, e.g. d={'place': 'Wien 7', 'date': '2024', 'client': '...'}.
"""
import json

TRI = 'M6.83791 0.390006C7.23821 -0.130002 8.02242 -0.130002 8.42272 0.390005L15.0512 9.00065C15.5574 9.65821 15.0886 10.6106 14.2588 10.6106H1.00184C0.172004 10.6106 -0.296761 9.65822 0.209436 9.00065L6.83791 0.390006Z'

# tile on the projects page (x, y, w, h in Figma pixels), title, text, details, photos - in reading order
PROJECTS = [
    dict(r=(235, 60, 200, 370), t='dd - NEW LOGO & IDENTITY', imgs=['img/projects-imgDdLogoWithTextFinal13.webp', 'img/p-fly-drawing.webp', 'img/p-spiky-drawing.webp', 'img/p-tower-drawing-frame.webp', 'img/p-tower-drawing-up.webp', 'img/p-sketchbooks-colour.webp', 'img/p-overlay-drawing-render.webp', 'img/p-map-decon-cluster.webp']),
    dict(r=(455, 60, 200, 180), t='SKI SLOPES IN SUMMER', imgs=['img/projects-imgDdLogoWithTextFinal14.webp', 'img/p-motorway-gantry.webp', 'img/p-horse-rider.webp', 'img/p-render-twin-towers.webp', 'img/p-section-sky-pen.webp', 'img/p-render-x-towers.webp', 'img/p-section-warehouse-blue.webp']),
    dict(r=(455, 250, 200, 180), t='AIDA - THE BEST COFFEE CHAIN', imgs=['img/projects-imgImage6.webp', 'img/p-coffee-stain.webp', 'img/p-coffee-stain-paper.webp', 'img/p-milk-glass.webp', 'img/p-crates-black.webp', 'img/p-render-spiky-harbour.webp', 'img/p-section-masters.webp']),
    dict(r=(675, 60, 420, 370), t='MUSEUMS QUARTIER', imgs=['img/projects-imgImage5.webp', 'img/p-banana-tape.webp', 'img/p-triple-head.webp', 'img/p-tower-drawing-grey.webp', 'img/p-render-three-towers.webp', 'img/p-render-crystal.webp', 'img/p-render-crystal-street.webp', 'img/p-render-glass-dock.webp']),
    dict(r=(1115, 60, 200, 370), t='dd - NEW BUSINESS CARDS', imgs=['img/intro-imgImage.webp', 'img/p-paper-shreds.webp', 'img/p-graffiti-nieder.webp', 'img/p-sketchbook-wall.webp', 'img/p-sketchbook-hermit-crab.webp', 'img/p-section-warehouse-2.webp']),
    # the tile shows Steuart's line portrait (the ID card stays on the services page only)
    dict(r=(235, 440, 420, 370), t='WHO IS THIS GUY?', imgs=['img/p-straw-drawing.webp', 'img/p-haircut.webp', 'img/p-boy-sunlight.webp', 'img/p-letter-pappi.webp', 'img/p-face-lines.webp', 'img/p-section-boat.webp']),
    dict(r=(895, 440, 420, 370), t='LIGHT AT THE END OF THE TUNNEL', imgs=['img/projects-imgImage8.webp', 'img/p-light-hole.webp', 'img/p-streaks-green-yellow.webp', 'img/p-motion-blur-grey.webp', 'img/p-render-motorway-loop.webp', 'img/p-render-towers-blue.webp', 'img/p-drawing-river-tower.webp']),
    dict(r=(675, 630, 200, 370), t='Hr. KARL SCHWANZER', imgs=['img/projects-imgImage3.webp', 'img/p-section-trees.webp', 'img/p-section-wide.webp', 'img/p-section-blue.webp', 'img/p-render-spiky-tower.webp', 'img/p-render-concrete-tower.webp', 'img/p-model-dock-top.webp', 'img/p-model-dock-side.webp']),
    dict(r=(235, 820, 200, 180), t='MIRROR BALL & DISCO HALLS', imgs=['img/projects-imgImage1.webp', 'img/p-carrots-plate.webp', 'img/p-wasp-red.webp', 'img/p-render-harbour-bridge.webp', 'img/p-plan-vertical.webp', 'img/p-render-warehouse-figures.webp']),
    dict(r=(455, 820, 200, 180), t='dd - OUR OLD LOGO', imgs=['img/projects-imgImage2.webp', 'img/p-torn-strips-drawing.webp', 'img/p-torn-strips-photo.webp', 'img/p-plan-horizontal.webp', 'img/p-folded-houses.webp', 'img/p-map-river-grid.webp', 'img/p-map-river-blocks.webp']),
    dict(r=(895, 820, 200, 180), t='INTERIOR COURTYARDS', imgs=['img/projects-imgImage7.webp', 'img/p-light-switch.webp', 'img/p-yellow-dots-box.webp', 'img/p-plastic-sheet-2.webp', 'img/p-flower-shadows.webp', 'img/p-drawing-cranes.webp', 'img/p-render-three-pink.webp', 'img/p-render-three-hazy.webp']),
]
PLACEHOLDER = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore '
               'et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.',
               'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore. '
               'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt.']
# imaginary placeholder details, in project order, until the real ones are written
DETAILS = [
    dict(place='Wien 16, Ottakring', date='2024', client='dasein-design (own work)', type='corporate identity, logo', status='completed'),
    dict(place='Hinterstoder, Upper Austria', date='2019', client='regional tourism board', type='landscape study', status='study'),
    dict(place='Wien 7, Neubau', date='2021', client='café chain', type='interior refurbishment', status='completed'),
    dict(place='Wien 7, Museumsplatz', date='2018', client='cultural institution', type='exhibition design', status='completed'),
    dict(place='Wien 16, Ottakring', date='2025', client='dasein-design (own work)', type='graphic design, print', status='completed'),
    dict(place='Wien', date='2026', client='–', type='portrait, about us', status='ongoing'),
    dict(place='Wien 10, Favoriten', date='2022', client='public client', type='lighting concept, underpass', status='competition entry'),
    dict(place='Wien 3, Landstraße', date='2020', client='research', type='architectural history, documentation', status='published'),
    dict(place='Wien 2, Prater', date='2017', client='private client', type='event space, interior', status='completed'),
    dict(place='Wien', date='2008', client='dasein-design (own work)', type='corporate identity', status='archived'),
    dict(place='Wien 16, Ottakring', date='2023', client='housing cooperative', type='courtyard greening', status='under construction'),
]
for p, d in zip(PROJECTS, DETAILS):
    p.setdefault('d', dict(d))
# the details shown under the text, in this order; a missing entry shows a dash
FIELDS = [('name', 'project'), ('place', 'place'), ('date', 'date'), ('client', 'client'), ('type', 'type'), ('status', 'status')]
# coloured placeholder photos in mixed shapes (img/ph-01.svg ... ph-10.svg) until the real photos arrive:
# each project gets nine of them after its tile photo, starting at a different one so the strips differ
PH = [f'img/ph-{i:02d}.svg' for i in range(1, 11)]
# placeholders retired 19 Oct: every project now shows only real photos, each used once on the whole site
for p in PROJECTS:
    p.setdefault('x', PLACEHOLDER)
    p.setdefault('d', {})
    p['d'].setdefault('name', p['t'])


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')


# clickable tiles, placed inside the projects page so they scroll with it
TILES = ''.join(f'<button type="button" class="hot proj" data-p="{i}" aria-label="open project: {esc(p["t"])}" '
                f'style="left:{p["r"][0]}px;top:{p["r"][1]}px;width:{p["r"][2]}px;height:{p["r"][3]}px"></button>'
                for i, p in enumerate(PROJECTS))

# pop-up box in the main area (Figma pixels): main area is x 225-1325, y 32-1024
BX, BY, BW, BH = 315, 168, 920, 720

CSS = '''
/* project tiles: a red frame on hover, as on the links page; a click opens the pop-up */
.hot.proj{padding:0;margin:0;border:0;background:none;cursor:none}
.hot.proj:hover,.hot.proj:focus-visible{box-shadow:inset 0 0 0 calc(1px / var(--s,1)) #e30613;outline:none}
/* over a project tile the pointer becomes a small pulsing circle sending out thin red rings */
.pcur{position:fixed;left:0;top:0;width:0;height:0;pointer-events:none;z-index:2147483000;display:none}
.pcur.on{display:block}
.pcur b,.pcur::before,.pcur::after{content:"";position:absolute;left:0;top:0;border-radius:50%;transform:translate(-50%,-50%)}
.pcur b{width:9px;height:9px;background:#d4fb4d;box-shadow:inset 0 0 0 .5px #e30613;animation:pcdot 1.4s ease-in-out infinite}
.pcur::before,.pcur::after{width:9px;height:9px;border:.6px solid #e30613;box-sizing:border-box;animation:pcring 1.4s ease-out infinite}
.pcur::after{animation-delay:.7s}
@keyframes pcdot{50%{transform:translate(-50%,-50%) scale(.75)}}
@keyframes pcring{from{width:9px;height:9px;opacity:.8}to{width:45px;height:45px;opacity:0}}
@media (prefers-reduced-motion:reduce){.pcur b,.pcur::before,.pcur::after{animation:none}.pcur::after{display:none}.pcur::before{width:18px;height:18px}}
/* over the photo the pointer becomes a small yellow arrow, pulsing and sending out thin red rings like the circle */
.pcar{position:fixed;left:0;top:0;width:0;height:0;pointer-events:none;z-index:10;display:none}
.pcar.on{display:block}
.pcar{--hp:calc(.86px / var(--dpr,1))}
.pcar svg{position:absolute;left:-14px;top:-14px;display:none}
.pcar.l .cw,.pcar.r .ce{display:block}
.pcar .tr{animation:arring 1.4s ease-out infinite}
.pcar .dt{transform-box:fill-box;transform-origin:center}
/* project pop-up: only the main area is veiled and blurred; side bars, title and menu stay sharp */
dialog.lb{position:fixed;inset:0;width:100%;height:100%;max-width:none;max-height:none;margin:0;padding:0;border:0;background:transparent;overflow:hidden;color:#000}
dialog.lb::backdrop{background:transparent}
dialog.lb[open]{display:flex;align-items:center;justify-content:center}
.lbh{position:relative;flex:none;width:calc(1440px * var(--s,.5));height:calc(1024px * var(--s,.5))}
.lbs{position:absolute;left:0;top:0;width:1440px;height:1024px;transform:scale(var(--s,.5));transform-origin:0 0;font-family:Calibri,Carlito,sans-serif}
.lbv{position:absolute;left:225px;top:32px;width:1100px;height:992px;background:rgba(255,255,255,.35);-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px)}
dialog.lb[open] .lbv{animation:lbveil .3s ease-out both}
@keyframes lbveil{from{background:rgba(255,255,255,0);-webkit-backdrop-filter:blur(0);backdrop-filter:blur(0)}}
dialog.lb[open] .lbp{animation:lbin .3s ease-out both}
@keyframes lbin{from{opacity:0;transform:translateY(14px)}}
@media (prefers-reduced-motion:reduce){dialog.lb[open] .lbv,dialog.lb[open] .lbp{animation:none}}
/* the site's dashed column lines, kept sharp over the veil */
.lbg i{position:absolute;top:32px;height:992px;width:var(--w);pointer-events:none;
  --w:calc(1px / (var(--s,1) * var(--dpr,1)));background:repeating-linear-gradient(to bottom,#b4b4b4 0 5px,transparent 5px 7.5px)}
/* the pop-up itself, centred in the main area */
.lbp{position:absolute;outline:none;background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);box-shadow:0 12px 40px rgba(0,0,0,.10)}
.lbd::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;
  --c:#b8b8b8;--d:var(--w);--p:calc(var(--w) * 3);--w:calc(1px / (var(--s,1) * var(--dpr,1)));
  background:
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/100% var(--w) no-repeat,
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left bottom/100% var(--w) no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/var(--w) 100% no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) right top/var(--w) 100% no-repeat}
/* top line: counter on the left, close on the right */
.lbk{position:absolute;left:26px;top:30px;height:25px;display:flex;align-items:center;gap:8px;font:400 13px/25px Calibri,Carlito,sans-serif;color:#666;letter-spacing:.06em}
.lbkb{display:flex;align-items:center;border:0;background:none;padding:0;cursor:pointer}
.lbkb:focus-visible{outline:none}
.lbk b{color:#e30613;font-weight:400}
.lbx{position:absolute;right:26px;top:31px;width:24px;height:24px;border:0;padding:0;background:none;cursor:pointer;display:flex;align-items:center;justify-content:center}
.lbx svg{width:16px;height:16px;stroke:#000;stroke-width:1;transition:stroke .2s}
.lbx:hover svg,.lbx:focus-visible svg{stroke:#e30613;animation:lbxp 1.4s ease-in-out infinite}
.lbx:focus-visible{outline:none}
@keyframes lbxp{50%{transform:scale(1.3)}}
@media (prefers-reduced-motion:reduce){.lbx:hover svg,.lbx:focus-visible svg{animation:none}}
/* main photo */
.lbi{position:absolute;left:30px;top:75px;width:520px;height:390px;display:flex;align-items:center;justify-content:center;background:rgba(240,240,240,.55)}
.lbi img{width:100%;height:100%;object-fit:contain;display:block;transition:opacity .2s}
.lbi img.ld{opacity:0}
.lbn{position:absolute;top:0;width:50%;height:100%;padding:0;border:0;background:none;cursor:none;display:flex;align-items:center;z-index:3}
.lbn.prev{left:0;justify-content:flex-start;padding-left:12px}.lbn.next{right:0;justify-content:flex-end;padding-right:12px}
.lbn span{width:40px;height:40px;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .2s}
.lbn:focus-visible span{opacity:1}
.lbn:focus-visible{outline:none}
/* all arrows are compass arrows (north = top of the screen): a dark grey notched arrowhead in an open circle,
   with N, E, S or W in the gap; every line as thin as the dashed guide lines (one screen pixel).
   Pointed at, they send out thin dark rings, like the pulsing pointers */
:root{--hp:calc(.92px / (var(--s,1) * var(--dpr,1)))}
.ar{overflow:visible;flex:none}
.ar .rg{fill:none;stroke:#3a3c37;stroke-width:var(--hp)}
.ar .dt{fill:#4d4f4a;stroke:#1a1a1a;stroke-width:var(--hp);stroke-linejoin:round}
.ar text{fill:#3a3c37;font:700 6.4px Calibri,Carlito,sans-serif;text-anchor:middle;dominant-baseline:central}
.tr{fill:none;stroke:#3a3c37;stroke-width:var(--hp);opacity:0;transform-box:fill-box;transform-origin:center}
.lbm button:hover .tr,.lbm button:focus-visible .tr,.lbkb:hover .tr,.lbkb:focus-visible .tr,.lbsa:not(:disabled):hover .tr,.nextp:hover .tr,.nextp:focus-visible .tr,.nextp.hint .tr{animation:arring 1.4s ease-out infinite}
.tr2{animation-delay:.7s!important}
@keyframes arring{from{transform:scale(1);opacity:.75}to{transform:scale(1.8);opacity:0;stroke-width:calc(var(--hp) / 1.8)}}
@media (prefers-reduced-motion:reduce){.tr{animation:none!important}}
/* beside the photo: title, text, then the project details */
.lbc{position:absolute;left:580px;top:75px;width:310px;height:390px;overflow-y:auto;scrollbar-width:thin}
.lbt{margin:0;font:700 20px/1.15 Calibri,Carlito,sans-serif;color:#e30613}
.lbtx{margin:12px 0 0;font:400 14px/1.4 Calibri,Carlito,sans-serif;color:#222;display:flex;flex-direction:column;gap:8px}
.lbtx p{margin:0}
.lbdt{margin:18px 0 0;padding-top:12px;border-top:calc(1px / (var(--s,1) * var(--dpr,1))) dotted #b8b8b8;display:grid;grid-template-columns:62px 1fr;gap:5px 10px;font:400 13px/1.3 Calibri,Carlito,sans-serif}
.lbdt dt{color:#888;letter-spacing:.04em}
.lbdt dd{margin:0;color:#000}
/* photo strip of this project, for quick navigation */
.lbsl{position:absolute;left:30px;top:490px;font:400 11px/1 Calibri,Carlito,sans-serif;color:#888;letter-spacing:.06em}
.lbsw{position:absolute;left:30px;top:508px;width:860px;height:120px;display:flex;align-items:center;gap:8px}
.lbsa{flex:none;width:22px;height:120px;border:0;padding:0;background:none;cursor:pointer;display:flex;align-items:center;justify-content:center}
.lbsa:disabled{opacity:.25;cursor:default}
.lbsa:focus-visible{outline:1px solid #e30613}
.lbst{flex:1;height:120px;display:flex;align-items:flex-end;gap:10px;overflow-x:auto;scroll-behavior:smooth;scrollbar-width:none}
.lbst::-webkit-scrollbar{display:none}
.lbst button{position:relative;flex:none;padding:0;border:0;background:none;cursor:pointer;line-height:0}
.lbst img{display:block;width:auto;height:auto;max-width:150px;max-height:120px}
.lbst img{opacity:.4;transition:opacity .25s}
.lbst button:hover img,.lbst button:focus-visible img{opacity:.8}
.lbst button.cur img{opacity:1}
.lbst button::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:1;
  --c:#b8b8b8;--d:var(--w);--p:calc(var(--w) * 3);--w:calc(1px / (var(--s,1) * var(--dpr,1)));
  background:
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/100% var(--w) no-repeat,
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left bottom/100% var(--w) no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/var(--w) 100% no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) right top/var(--w) 100% no-repeat}
.lbst button::after{content:"";position:absolute;left:0;right:0;bottom:0;height:4px;background:#d4fb4d;transform:scaleX(0);transition:transform .25s}
.lbst button.cur::after{transform:none}
.lbst button:focus-visible{outline:none}
/* bottom line: previous / next project */
.lbm{position:absolute;left:30px;right:30px;bottom:30px;display:flex;justify-content:space-between}
.lbm button{display:flex;align-items:center;gap:6px;border:0;background:none;padding:0;cursor:pointer;font:400 11px/1 Calibri,Carlito,sans-serif;letter-spacing:.06em;color:#666}
.lbm button:hover,.lbm button:focus-visible{color:#e30613;outline:none}
'''

def compass(d, size=22, cls=''):
    """compass arrow: a notched arrowhead in an open circle, with N, E, S or W in the gap it points to"""
    import math
    a = {'E': 0, 'S': 90, 'W': 180, 'N': 270}[d]
    r, gap = 9.5, 34
    p = lambda deg: (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))
    (x0, y0), (x1, y1), (lx, ly) = p(a + gap), p(a - gap), p(a)
    return (f'<svg class="ar {cls}" width="{size}" height="{size}" viewBox="-12 -12 24 24" aria-hidden="true">'
            f'<circle class="tr" r="{r}"/><circle class="tr tr2" r="{r}"/>'
            f'<path class="rg" d="M{x0:.2f} {y0:.2f}A{r} {r} 0 1 1 {x1:.2f} {y1:.2f}"/>'
            f'<path class="dt" transform="rotate({a})" d="M5.4 0L-4.6 -4.9L-2.2 0L-4.6 4.9Z"/>'
            f'<text x="{lx:.2f}" y="{ly:.2f}">{d}</text></svg>')


ARROW_W, ARROW_E = compass('W'), compass('E')
LINES = ''.join(f'<i style="left:{x}px"></i>' for x in (225, 445, 665, 885, 1105, 1325))

HTML = '<div class="pcur" id="pcur" aria-hidden="true"><b></b></div>' + f'''<dialog class="lb" id="lb" aria-labelledby="lbt"><div class="pcar" id="pcar" aria-hidden="true">{compass("W", 28, "cw")}{compass("E", 28, "ce")}</div><div class="lbh"><div class="lbs" id="lbs">
<div class="lbv"></div><div class="lbg">{LINES}</div>
<div class="lbp" id="lbp" tabindex="-1" style="left:{BX}px;top:{BY}px;width:{BW}px;height:{BH}px">
<div class="lbk"><button type="button" class="lbkb" id="lbkp" aria-label="previous project">{compass("W", 18)}</button><span id="lbk"></span><button type="button" class="lbkb" id="lbkn" aria-label="next project">{compass("E", 18)}</button></div>
<button type="button" class="lbx" id="lbx" aria-label="close (Esc)" title="close (Esc)"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 2L14 14M14 2L2 14"/></svg></button>
<div class="lbi lbd"><img id="lbimg" alt="">
<button type="button" class="lbn prev" id="lbprev" aria-label="previous photo"><span>{ARROW_W}</span></button>
<button type="button" class="lbn next" id="lbnext" aria-label="next photo"><span>{ARROW_E}</span></button></div>
<div class="lbc"><h2 class="lbt" id="lbt"></h2><div class="lbtx" id="lbtx"></div><dl class="lbdt" id="lbdt"></dl></div>
<div class="lbsl" id="lbsl"></div>
<div class="lbsw"><button type="button" class="lbsa l" id="lbsl0" aria-label="scroll photos left">{ARROW_W}</button>
<div class="lbst" id="lbst"></div>
<button type="button" class="lbsa r" id="lbsr0" aria-label="scroll photos right">{ARROW_E}</button></div>
<div class="lbm"><button type="button" class="pp" id="lbpp">{ARROW_W}previous project</button><button type="button" class="np" id="lbnp">next project{ARROW_E}</button></div>
</div></div></div></dialog>'''

JS = '''
  /* project pop-up */
  const P=''' + json.dumps([{'t': p['t'], 'x': p['x'], 'd': p['d'], 'imgs': p['imgs']} for p in PROJECTS]) + ''';
  const F=''' + json.dumps(FIELDS) + ''';
  const lb=document.getElementById('lb'), $=id=>document.getElementById(id), st=$('lbst');
  let pi=-1, ph=0;
  const two=n=>String(n).padStart(2,'0'), esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
  function arrows(){}   /* the strip arrows step through the photos, so they are never switched off */
  function show(p,f){
    const np=(p+P.length)%P.length, pr=P[np], newp=np!==pi; pi=np; ph=Math.max(0,Math.min(pr.imgs.length-1,f||0));
    const im=$('lbimg'); if(im.getAttribute('src')!==pr.imgs[ph]){ im.classList.add('ld'); im.onload=()=>im.classList.remove('ld'); im.src=pr.imgs[ph]; } im.alt=pr.t;
    $('lbk').innerHTML='projects <b>'+two(pi+1)+'</b> / '+two(P.length);
    if(newp){
      $('lbt').textContent=pr.t; $('lbtx').innerHTML=(Array.isArray(pr.x)?pr.x:[pr.x]).map(t=>'<p>'+esc(t)+'</p>').join('');
      $('lbdt').innerHTML=F.map(([k,l])=>'<dt>'+l+'</dt><dd>'+esc(pr.d[k]||'–')+'</dd>').join('');
      st.innerHTML=pr.imgs.map((s,k)=>'<button type="button" data-k="'+k+'" aria-label="photo '+(k+1)+'"><img src="'+s+'" alt=""></button>').join('');
      st.querySelectorAll('img').forEach(i=>i.addEventListener('load',arrows));
      st.scrollLeft=0;
    }
    $('lbsl').textContent='photos '+(ph+1)+' / '+pr.imgs.length;
    st.querySelectorAll('button').forEach((b,k)=>b.classList.toggle('cur',k===ph));
    const c=st.children[ph]; if(c&&lb.open){ const l=c.offsetLeft-st.offsetLeft; if(l<st.scrollLeft||l+c.offsetWidth>st.scrollLeft+st.clientWidth) st.scrollLeft=l-(st.clientWidth-c.offsetWidth)/2; }
    requestAnimationFrame(arrows);
  }
  /* left / right arrows walk through every photo, moving on to the next project at the end */
  function step(d){ const pr=P[pi], f=ph+d; if(f>=0&&f<pr.imgs.length) show(pi,f); else if(d>0) show(pi+1,0); else { const q=(pi-1+P.length)%P.length; show(q,P[q].imgs.length-1); } }
  document.querySelectorAll('.hot.proj').forEach(b=>b.addEventListener('click',()=>{ pi=-1; lb.showModal(); show(+b.dataset.p,0); $('lbp').focus({preventScroll:true}); }));
  $('lbx').onclick=()=>lb.close();
  $('lbprev').onclick=()=>step(-1); $('lbnext').onclick=()=>step(1);
  $('lbpp').onclick=$('lbkp').onclick=()=>show(pi-1,0); $('lbnp').onclick=$('lbkn').onclick=()=>show(pi+1,0);
  st.addEventListener('click',e=>{ const b=e.target.closest('button'); if(b) show(pi,+b.dataset.k); });
  st.addEventListener('scroll',arrows,{passive:true});
  /* the W / E arrows beside the strip step to the previous / next photo (and on into the next project), like the arrow keys */
  $('lbsl0').onclick=()=>step(-1); $('lbsr0').onclick=()=>step(1);
  /* pulsing pointer over the project tiles */
  const pc=$('pcur');
  document.querySelectorAll('.hot.proj').forEach(b=>{
    b.addEventListener('mousemove',e=>{ pc.style.transform=`translate(${e.clientX}px,${e.clientY}px)`; pc.classList.add('on'); });
    b.addEventListener('mouseleave',()=>pc.classList.remove('on'));
    b.addEventListener('click',()=>pc.classList.remove('on'));
  });
  /* over the photo: pulsing arrow pointer, pointing the way the click will go */
  const pa=$('pcar');
  [['lbprev','l'],['lbnext','r']].forEach(([id,d])=>{ const b=$(id);
    b.addEventListener('mousemove',e=>{ pa.style.transform=`translate(${e.clientX}px,${e.clientY}px)`; pa.className='pcar on '+d; });
    b.addEventListener('mouseleave',()=>pa.className='pcar');
  });
  lb.addEventListener('close',()=>pa.className='pcar');
  /* a click beside the pop-up closes it */
  lb.addEventListener('click',e=>{ if(!e.target.closest('#lbp')) lb.close(); });
  lb.addEventListener('keydown',e=>{
    const d={ArrowRight:1,ArrowDown:1,PageDown:1,ArrowLeft:-1,ArrowUp:-1,PageUp:-1}[e.key]; if(!d) return;
    e.preventDefault(); e.stopPropagation(); step(d);
  });
  /* the mouse wheel scrolls the photo strip sideways (or the text), never the page underneath */
  lb.addEventListener('wheel',e=>{ e.preventDefault(); if(e.target.closest('.lbsw')) st.scrollLeft+=(e.deltaY||e.deltaX); else { const c=e.target.closest('.lbc'); if(c) c.scrollTop+=e.deltaY; } },{passive:false});
'''
