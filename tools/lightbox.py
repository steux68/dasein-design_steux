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
    dict(r=(235, 60, 200, 370), t='dd - NEW LOGO & IDENTITY', imgs=['img/projects-imgDdLogoWithTextFinal13.webp']),
    dict(r=(455, 60, 200, 180), t='SKI SLOPES IN SUMMER', imgs=['img/projects-imgDdLogoWithTextFinal14.webp']),
    dict(r=(455, 250, 200, 180), t='AIDA - THE BEST COFFEE CHAIN', imgs=['img/projects-imgImage6.webp']),
    dict(r=(675, 60, 420, 370), t='MUSEUMS QUARTIER', imgs=['img/projects-imgImage5.webp']),
    dict(r=(1115, 60, 200, 370), t='dd - NEW BUSINESS CARDS', imgs=['img/intro-imgImage.webp']),
    dict(r=(235, 440, 420, 370), t='WHO IS THIS GUY?', imgs=['img/services-imgImage1.webp']),
    dict(r=(895, 440, 420, 370), t='LIGHT AT THE END OF THE TUNNEL', imgs=['img/projects-imgImage8.webp']),
    dict(r=(675, 630, 200, 370), t='Hr. KARL SCHWANZER', imgs=['img/projects-imgImage3.webp']),
    dict(r=(235, 820, 200, 180), t='MIRROR BALL & DISCO HALLS', imgs=['img/projects-imgImage1.webp']),
    dict(r=(455, 820, 200, 180), t='dd - OUR OLD LOGO', imgs=['img/projects-imgImage2.webp']),
    dict(r=(895, 820, 200, 180), t='INTERIOR COURTYARDS', imgs=['img/projects-imgImage7.webp']),
]
PLACEHOLDER = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore '
               'et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.')
# the details shown under the text, in this order; a missing entry shows a dash
FIELDS = [('name', 'project'), ('place', 'place'), ('date', 'date'), ('client', 'client'), ('type', 'type'), ('status', 'status')]
# coloured placeholder photos in mixed shapes (img/ph-01.svg ... ph-10.svg) until the real photos arrive:
# each project gets nine of them after its tile photo, starting at a different one so the strips differ
PH = [f'img/ph-{i:02d}.svg' for i in range(1, 11)]
for n, p in enumerate(PROJECTS):
    if len(p['imgs']) == 1:
        p['imgs'] += (PH[n % 10:] + PH[:n % 10])[:9]
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
.hot.proj{padding:0;margin:0;border:0;background:none;cursor:zoom-in}
.hot.proj:hover,.hot.proj:focus-visible{box-shadow:inset 0 0 0 calc(1.5px / var(--s,1)) #e30613;outline:none}
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
  --c:#c4c4c4;--d:5px;--p:7.5px;--w:calc(1px / (var(--s,1) * var(--dpr,1)));
  background:
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/100% var(--w) no-repeat,
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left bottom/100% var(--w) no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/var(--w) 100% no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) right top/var(--w) 100% no-repeat}
/* top line: counter on the left, close on the right */
.lbk{position:absolute;left:30px;top:30px;font:400 13px/25px Calibri,Carlito,sans-serif;color:#666;letter-spacing:.06em}
.lbk b{color:#e30613;font-weight:400}
.lbx{position:absolute;right:30px;top:30px;width:200px;height:25px;border:0;padding:0;background:#ebebeb;font:400 15px/25px Calibri,Carlito,sans-serif;color:#000;cursor:pointer;text-align:center}
.lbx small{font-size:10px;color:#666}
.lbx:hover,.lbx:focus-visible{color:#e30613;box-shadow:inset 0 0 0 1.5px #e30613;outline:none}
/* main photo */
.lbi{position:absolute;left:30px;top:75px;width:520px;height:390px;display:flex;align-items:center;justify-content:center;background:rgba(240,240,240,.55)}
.lbi img{width:100%;height:100%;object-fit:contain;display:block;transition:opacity .2s}
.lbi img.ld{opacity:0}
.lbn{position:absolute;top:0;width:50%;height:100%;padding:0;border:0;background:none;cursor:pointer;display:flex;align-items:center;z-index:3}
.lbn.prev{left:0;justify-content:flex-start;padding-left:12px}.lbn.next{right:0;justify-content:flex-end;padding-right:12px}
.lbn span{width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.88);display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .2s}
.lbn.prev svg,.lbm .pp svg,.lbsa.l svg{transform:rotate(-90deg)}.lbn.next svg,.lbm .np svg,.lbsa.r svg{transform:rotate(90deg)}
.lbi:hover .lbn span,.lbn:focus-visible span{opacity:1}
.lbn:hover span{box-shadow:inset 0 0 0 1.5px #e30613}
.lbn:focus-visible{outline:none}
.tri{fill:rgba(205,255,62,.86);stroke:#000;stroke-width:1}
.lbn:hover .tri,.lbm button:hover .tri,.lbsa:hover .tri{stroke:#e30613}
/* beside the photo: title, text, then the project details */
.lbc{position:absolute;left:580px;top:75px;width:310px;height:390px;overflow-y:auto;scrollbar-width:thin}
.lbt{margin:0;font:700 20px/1.15 Calibri,Carlito,sans-serif;color:#e30613}
.lbtx{margin:12px 0 0;font:400 14px/1.4 Calibri,Carlito,sans-serif;color:#222}
.lbdt{margin:18px 0 0;padding-top:12px;border-top:1px dashed #c4c4c4;display:grid;grid-template-columns:62px 1fr;gap:5px 10px;font:400 13px/1.3 Calibri,Carlito,sans-serif}
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
.lbst button::before{content:"";position:absolute;inset:0;z-index:1}
.lbst button:hover::before,.lbst button:focus-visible::before{box-shadow:inset 0 0 0 1.5px #e30613}
.lbst button.cur::before{box-shadow:inset 0 0 0 3px #e30613,inset 0 0 0 6px #d4fb4d}
.lbst button:focus-visible{outline:none}
/* bottom line: previous / next project */
.lbm{position:absolute;left:30px;right:30px;bottom:30px;display:flex;justify-content:space-between}
.lbm button{display:flex;align-items:center;gap:6px;border:0;background:none;padding:0;cursor:pointer;font:400 11px/1 Calibri,Carlito,sans-serif;letter-spacing:.06em;color:#666}
.lbm button:hover,.lbm button:focus-visible{color:#e30613;outline:none}
'''

ARROW = f'<svg width="20" height="15" viewBox="-0.5 -0.5 16.26 11.61" aria-hidden="true"><path class="tri" d="{TRI}"/></svg>'
LINES = ''.join(f'<i style="left:{x}px"></i>' for x in (225, 445, 665, 885, 1105, 1325))

HTML = f'''<dialog class="lb" id="lb" aria-labelledby="lbt"><div class="lbh"><div class="lbs" id="lbs">
<div class="lbv"></div><div class="lbg">{LINES}</div>
<div class="lbp lbd" id="lbp" tabindex="-1" style="left:{BX}px;top:{BY}px;width:{BW}px;height:{BH}px">
<div class="lbk" id="lbk"></div>
<button type="button" class="lbx" id="lbx">close &#x2715; <small>[esc]</small></button>
<div class="lbi lbd"><img id="lbimg" alt="">
<button type="button" class="lbn prev" id="lbprev" aria-label="previous photo"><span>{ARROW}</span></button>
<button type="button" class="lbn next" id="lbnext" aria-label="next photo"><span>{ARROW}</span></button></div>
<div class="lbc"><h2 class="lbt" id="lbt"></h2><p class="lbtx" id="lbtx"></p><dl class="lbdt" id="lbdt"></dl></div>
<div class="lbsl" id="lbsl"></div>
<div class="lbsw"><button type="button" class="lbsa l" id="lbsl0" aria-label="scroll photos left">{ARROW}</button>
<div class="lbst" id="lbst"></div>
<button type="button" class="lbsa r" id="lbsr0" aria-label="scroll photos right">{ARROW}</button></div>
<div class="lbm"><button type="button" class="pp" id="lbpp">{ARROW}previous project</button><button type="button" class="np" id="lbnp">next project{ARROW}</button></div>
</div></div></div></dialog>'''

JS = '''
  /* project pop-up */
  const P=''' + json.dumps([{'t': p['t'], 'x': p['x'], 'd': p['d'], 'imgs': p['imgs']} for p in PROJECTS]) + ''';
  const F=''' + json.dumps(FIELDS) + ''';
  const lb=document.getElementById('lb'), $=id=>document.getElementById(id), st=$('lbst');
  let pi=-1, ph=0;
  const two=n=>String(n).padStart(2,'0'), esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
  function arrows(){ $('lbsl0').disabled=st.scrollLeft<=1; $('lbsr0').disabled=st.scrollLeft+st.clientWidth>=st.scrollWidth-1; }
  function show(p,f){
    const np=(p+P.length)%P.length, pr=P[np], newp=np!==pi; pi=np; ph=Math.max(0,Math.min(pr.imgs.length-1,f||0));
    const im=$('lbimg'); if(im.getAttribute('src')!==pr.imgs[ph]){ im.classList.add('ld'); im.onload=()=>im.classList.remove('ld'); im.src=pr.imgs[ph]; } im.alt=pr.t;
    $('lbk').innerHTML='projects <b>'+two(pi+1)+'</b> / '+two(P.length);
    if(newp){
      $('lbt').textContent=pr.t; $('lbtx').textContent=pr.x;
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
  $('lbpp').onclick=()=>show(pi-1,0); $('lbnp').onclick=()=>show(pi+1,0);
  st.addEventListener('click',e=>{ const b=e.target.closest('button'); if(b) show(pi,+b.dataset.k); });
  st.addEventListener('scroll',arrows,{passive:true});
  $('lbsl0').onclick=()=>{ st.scrollLeft-=st.clientWidth*.8; }; $('lbsr0').onclick=()=>{ st.scrollLeft+=st.clientWidth*.8; };
  /* a click beside the pop-up closes it */
  lb.addEventListener('click',e=>{ if(!e.target.closest('#lbp')) lb.close(); });
  lb.addEventListener('keydown',e=>{
    const d={ArrowRight:1,ArrowDown:1,PageDown:1,ArrowLeft:-1,ArrowUp:-1,PageUp:-1}[e.key]; if(!d) return;
    e.preventDefault(); e.stopPropagation(); step(d);
  });
  /* the mouse wheel scrolls the photo strip sideways (or the text), never the page underneath */
  lb.addEventListener('wheel',e=>{ e.preventDefault(); if(e.target.closest('.lbsw')) st.scrollLeft+=(e.deltaY||e.deltaX); else { const c=e.target.closest('.lbc'); if(c) c.scrollTop+=e.deltaY; } },{passive:false});
'''
