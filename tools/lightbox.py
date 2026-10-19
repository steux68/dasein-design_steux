"""Project pop-up viewer (lightbox) for the projects page.

A native <dialog>: the site stays visible underneath behind a very light white veil and a soft blur,
the dashed column grid of the site is drawn sharp on top, and the project sits on the same 220 px columns.
build.py imports the four pieces below; the tiles are clickable areas over the projects page.

To add real photos: put them in img/ (named after their caption, up to 1600 px), then list them under
the project's "imgs" - the first one is the photo shown on the tile.
"""
import json

TRI = 'M6.83791 0.390006C7.23821 -0.130002 8.02242 -0.130002 8.42272 0.390005L15.0512 9.00065C15.5574 9.65821 15.0886 10.6106 14.2588 10.6106H1.00184C0.172004 10.6106 -0.296761 9.65822 0.209436 9.00065L6.83791 0.390006Z'

# tile on the projects page (x, y, w, h in Figma pixels), title, text, photos - in reading order
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
for p in PROJECTS:
    p.setdefault('x', PLACEHOLDER)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')


# clickable tiles, placed inside the projects page so they scroll with it
TILES = ''.join(f'<button type="button" class="hot proj" data-p="{i}" aria-label="open project: {esc(p["t"])}" '
                f'style="left:{p["r"][0]}px;top:{p["r"][1]}px;width:{p["r"][2]}px;height:{p["r"][3]}px"></button>'
                for i, p in enumerate(PROJECTS))

CSS = '''
/* project tiles: a red frame on hover, as on the links page; a click opens the pop-up */
.hot.proj{padding:0;margin:0;border:0;background:none;cursor:zoom-in}
.hot.proj:hover,.hot.proj:focus-visible{box-shadow:inset 0 0 0 calc(1.5px / var(--s,1)) #e30613;outline:none}
/* project pop-up: the site stays visible under a very light white veil and a soft blur */
dialog.lb{position:fixed;inset:0;width:100%;height:100%;max-width:none;max-height:none;margin:0;padding:0;border:0;background:transparent;overflow:hidden;color:#000}
dialog.lb::backdrop{background:rgba(255,255,255,.32);-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px)}
dialog.lb[open]{display:flex;align-items:center;justify-content:center}
.lbh{position:relative;flex:none;width:calc(1440px * var(--s,.5));height:calc(1024px * var(--s,.5))}
.lbs{position:absolute;left:0;top:0;width:1440px;height:1024px;transform:scale(var(--s,.5));transform-origin:0 0;font-family:Calibri,Carlito,sans-serif}
dialog.lb[open] .lbs{animation:lbin .28s ease-out both}
@keyframes lbin{from{opacity:0}to{opacity:1}}
@media (prefers-reduced-motion:reduce){dialog.lb[open] .lbs{animation:none}}
/* the site's dashed column lines, kept sharp over the blur */
.lbg i{position:absolute;top:0;height:1024px;width:var(--w);pointer-events:none;
  --w:calc(1px / (var(--s,1) * var(--dpr,1)));background:repeating-linear-gradient(to bottom,#b4b4b4 0 5px,transparent 5px 7.5px)}
/* the pop-up itself: lightly see-through white on the content columns */
.lbp{position:absolute;left:235px;top:60px;width:1080px;height:940px;background:rgba(255,255,255,.9)}
.lbd::after{content:"";position:absolute;inset:0;pointer-events:none;
  --c:#c4c4c4;--d:5px;--p:7.5px;--w:calc(1px / (var(--s,1) * var(--dpr,1)));
  background:
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/100% var(--w) no-repeat,
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left bottom/100% var(--w) no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/var(--w) 100% no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) right top/var(--w) 100% no-repeat}
/* big photo on four columns */
.lbi{position:absolute;left:0;top:0;width:860px;height:940px;display:flex;align-items:center;justify-content:center;background:#fff}
.lbi img{width:100%;height:100%;object-fit:contain;display:block}
.lbi img.ld{opacity:0} .lbi img{transition:opacity .2s}
.lbn{position:absolute;top:0;width:50%;height:100%;padding:0;border:0;background:none;cursor:pointer;display:flex;align-items:center}
.lbn.prev{left:0;justify-content:flex-start;padding-left:18px}.lbn.next{right:0;justify-content:flex-end;padding-right:18px}
.lbn span{width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.85);display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .2s}
.lbn.prev svg{transform:rotate(-90deg)}.lbn.next svg{transform:rotate(90deg)}
.lbi:hover .lbn span,.lbn:focus-visible span{opacity:1}
.lbn:hover span{box-shadow:inset 0 0 0 1.5px #e30613}
.lbn:focus-visible{outline:none}
.tri{fill:rgba(205,255,62,.86);stroke:#000;stroke-width:1}
.lbn:hover .tri,.lbm button:hover .tri{stroke:#e30613}
/* right-hand column: close, number, title, text, photos of this project, previous / next project */
.lbc{position:absolute;left:880px;top:0;width:200px;height:940px;display:flex;flex-direction:column}
.lbx{flex:none;width:200px;height:25px;border:0;padding:0;background:#ebebeb;font:400 15px/25px Calibri,Carlito,sans-serif;color:#000;cursor:pointer;text-align:center}
.lbx small{font-size:10px;color:#666}
.lbx:hover,.lbx:focus-visible{color:#e30613;box-shadow:inset 0 0 0 1.5px #e30613;outline:none}
.lbk{margin-top:28px;font-size:13px;color:#666;letter-spacing:.06em}
.lbk b{color:#e30613;font-weight:400}
.lbt{margin:8px 0 0;font:700 20px/1.15 Calibri,Carlito,sans-serif;color:#e30613}
.lbtx{margin:14px 0 0;font:400 14px/1.4 Calibri,Carlito,sans-serif;color:#222}
.lbth{margin-top:24px;display:flex;flex-direction:column;gap:10px;min-height:0;overflow:hidden}
.lbth button{position:relative;flex:none;width:200px;height:120px;padding:0;border:0;background:#fff;cursor:pointer}
.lbth img{width:100%;height:100%;object-fit:cover;display:block}
.lbth button::before{content:"";position:absolute;inset:0;z-index:1}
.lbth button:hover::before,.lbth button:focus-visible::before{box-shadow:inset 0 0 0 1.5px #e30613}
.lbth button.cur::before{box-shadow:inset 0 0 0 2.5px #e30613}
.lbth button:focus-visible{outline:none}
.lbm{margin-top:auto;padding-top:12px;display:flex;justify-content:space-between}
.lbm button{display:flex;align-items:center;gap:6px;border:0;background:none;padding:0;cursor:pointer;font:400 11px/1 Calibri,Carlito,sans-serif;letter-spacing:.06em;color:#666}
.lbm button:hover,.lbm button:focus-visible{color:#e30613;outline:none}
.lbm .pp svg{transform:rotate(-90deg)}.lbm .np svg{transform:rotate(90deg)}
'''

ARROW = f'<svg width="20" height="15" viewBox="-0.5 -0.5 16.26 11.61" aria-hidden="true"><path class="tri" d="{TRI}"/></svg>'
LINES = ''.join(f'<i style="left:{x}px"></i>' for x in (115, 225, 445, 665, 885, 1105, 1325))

HTML = f'''<dialog class="lb" id="lb" aria-labelledby="lbt"><div class="lbh"><div class="lbs" id="lbs">
<div class="lbg">{LINES}</div>
<div class="lbp lbd" id="lbp">
<div class="lbi lbd"><img id="lbimg" alt="">
<button type="button" class="lbn prev" id="lbprev" aria-label="previous photo"><span>{ARROW}</span></button>
<button type="button" class="lbn next" id="lbnext" aria-label="next photo"><span>{ARROW}</span></button></div>
<div class="lbc">
<button type="button" class="lbx" id="lbx">close &#x2715; <small>[esc]</small></button>
<div class="lbk" id="lbk"></div>
<h2 class="lbt" id="lbt"></h2>
<p class="lbtx" id="lbtx"></p>
<div class="lbth" id="lbth"></div>
<div class="lbm"><button type="button" class="pp" id="lbpp">{ARROW}previous</button><button type="button" class="np" id="lbnp">next{ARROW}</button></div>
</div></div></div></div></dialog>'''

JS = '''
  /* project pop-up */
  const P=''' + json.dumps([{'t': p['t'], 'x': p['x'], 'imgs': p['imgs']} for p in PROJECTS]) + ''';
  const lb=document.getElementById('lb'), $=id=>document.getElementById(id);
  let pi=0, ph=0;
  const two=n=>String(n).padStart(2,'0');
  function show(p,f){
    pi=(p+P.length)%P.length; const pr=P[pi]; ph=Math.max(0,Math.min(pr.imgs.length-1,f||0));
    const im=$('lbimg'); im.classList.add('ld'); im.onload=()=>im.classList.remove('ld'); im.src=pr.imgs[ph]; im.alt=pr.t;
    $('lbk').innerHTML='projects <b>'+two(pi+1)+'</b> / '+two(P.length)+(pr.imgs.length>1?' &middot; photo '+(ph+1)+' / '+pr.imgs.length:'');
    $('lbt').textContent=pr.t; $('lbtx').textContent=pr.x;
    $('lbth').innerHTML=pr.imgs.length>1?pr.imgs.map((s,k)=>'<button type="button" data-k="'+k+'" class="'+(k===ph?'cur':'')+'" aria-label="photo '+(k+1)+'"><img src="'+s+'" alt=""></button>').join(''):'';
  }
  /* left / right arrows walk through every photo, moving on to the next project at the end */
  function step(d){ const pr=P[pi], f=ph+d; if(f>=0&&f<pr.imgs.length) show(pi,f); else if(d>0) show(pi+1,0); else { const q=(pi-1+P.length)%P.length; show(q,P[q].imgs.length-1); } }
  document.querySelectorAll('.hot.proj').forEach(b=>b.addEventListener('click',()=>{ show(+b.dataset.p,0); lb.showModal(); }));
  $('lbx').onclick=()=>lb.close();
  $('lbprev').onclick=()=>step(-1); $('lbnext').onclick=()=>step(1);
  $('lbpp').onclick=()=>show(pi-1,0); $('lbnp').onclick=()=>show(pi+1,0);
  $('lbth').addEventListener('click',e=>{ const b=e.target.closest('button'); if(b) show(pi,+b.dataset.k); });
  /* a click beside the pop-up closes it */
  lb.addEventListener('click',e=>{ if(!e.target.closest('#lbp')) lb.close(); });
  lb.addEventListener('keydown',e=>{
    const d={ArrowRight:1,ArrowDown:1,PageDown:1,ArrowLeft:-1,ArrowUp:-1,PageUp:-1}[e.key]; if(!d) return;
    e.preventDefault(); e.stopPropagation(); step(d);
  });
  lb.addEventListener('wheel',e=>e.preventDefault(),{passive:false});
'''
