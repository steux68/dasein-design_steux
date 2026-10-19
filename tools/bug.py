"""Start page: the beetle flies in as a collage of square-cut pieces and puts itself together (about 3.6 s).

The beetle image (transparent background) is cut with straight, right-angled cuts into rectangles of
mixed sizes (a recursive split, like cutting card); only pieces that contain some beetle are kept.
Each piece flies in from outside, turned and slightly larger, and lands squarely but still apart,
so white gaps of different widths show between the pieces; after a pause they all lock together
and the real image takes over. On the start page a small pulsing dot follows the pointer with a hint
("click the menu or a number on the beetle") that switches sides near the edges.
When the pointer is over the beetle its pieces ease slightly apart and close again when it leaves.
It plays every time you arrive on the start page, never with "reduce motion" switched on.
build.py imports HTML (placed in the intro page), CSS and JS. Run from tools/ (reads ../img/).
"""
import os
import random
from PIL import Image

SRC = 'img/intro-bug-cut.webp'           # the beetle with its white background made transparent (from intro-imgRectangle307.webp)
X0, Y0, W, H = 225, 60, 1100, 940          # where the beetle sits on the intro page (Figma pixels)
COLS, ROWS = 8, 6                          # grid over the beetle's own outline

rnd = random.Random(42)                    # fixed seed: the same pieces every build
im = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', SRC)).convert('RGBA')
k = im.width / W
alpha = im.getchannel('A').resize((W, H))
bx0, by0, bx1, by1 = alpha.getbbox()

# recursive straight cuts: split the longer side at a random point until pieces are small enough
pieces = []
apx = alpha.load()


def split(x0, y0, x1, y1, depth=0):
    w, h = x1 - x0, y1 - y0
    big = max(w, h)
    if big < 72 or (big < 140 and rnd.random() < .3) or depth > 12:
        hits = sum(1 for x in range(int(x0), int(x1), 3) for y in range(int(y0), int(y1), 3) if apx[min(W - 1, x), min(H - 1, y)] > 100)
        if hits >= 40:
            pieces.append(dict(b=[int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0)]))
        return
    f = rnd.uniform(.3, .7)
    if w >= h:
        m = round(x0 + w * f); split(x0, y0, m, y1, depth + 1); split(m, y0, x1, y1, depth + 1)
    else:
        m = round(y0 + h * f); split(x0, y0, x1, m, depth + 1); split(x0, m, x1, y1, depth + 1)


split(bx0, by0, bx1, by1)
CX, CY = (bx0 + bx1) / 2, (by0 + by1) / 2

HTML = ('<div class="pcur ihint" id="ihint" aria-hidden="true"><b></b><span class="ilab">click the menu or a number on the beetle</span></div>'
        + f'<div class="bug" id="bug" aria-hidden="true" style="left:{X0}px;top:{Y0}px;width:{W}px;height:{H}px">'
        + ''.join(f'<div class="bp" data-dx="{(p["b"][0] + p["b"][2] / 2 - CX) / 550:.3f}" data-dy="{(p["b"][1] + p["b"][3] / 2 - CY) / 470:.3f}" '
                  f'style="left:{p["b"][0]}px;top:{p["b"][1]}px;width:{p["b"][2]}px;height:{p["b"][3]}px">'
                  f'<i style="background-position:{-p["b"][0]}px {-p["b"][1]}px"></i></div>'
                  for p in pieces)
        + '</div>')

CSS = f'''
/* start page: the beetle arrives as a collage and puts itself together */
.bug{{position:absolute;pointer-events:none;display:none;z-index:1;clip-path:inset({32 - Y0}px 0 {Y0 + H - 1024}px 0)}}   /* fly only inside the main area */
.bugplay .bug{{display:block}}
.bugplay [data-node-id="1:144"]{{visibility:hidden}}
.bp{{position:absolute;opacity:0;will-change:transform}}
.bp i{{position:absolute;inset:0;background:url({SRC}) no-repeat;background-size:{W}px {H}px}}
/* start page hint: a small pulsing dot follows the pointer over the main area, with a note that switches sides near the edges */
.ihint .ilab{{position:absolute;left:14px;bottom:8px;white-space:nowrap;background:rgba(255,255,255,.92);color:#000;
  font:400 13px/1.25 Calibri,Carlito,sans-serif;padding:4px 8px}}
.ihint.l .ilab{{left:auto;right:14px}}
.ihint.b .ilab{{bottom:auto;top:10px}}
.ihoff,.ihoff *{{cursor:none!important}}
'''

JS = '''
  /* start page: the beetle flies in as square-cut pieces, lands still apart with white gaps,
     pauses, then locks together - about 3.6 seconds, every time you arrive on the start page */
  try{
    const bug=document.getElementById('bug'), fr=bug&&bug.parentElement;
    if(bug && bug.animate && !reduce){
      const ps=[...bug.children], R=(a,b)=>a+Math.random()*(b-a);
      const T=3600, LOCK=3150, SNAP=260;   /* whole run, moment the pieces lock, how long the lock takes */
      let anims=[], run=0, playing=false, hov=[], isOpen=false;
      const play=()=>{
        anims.forEach(a=>a.cancel()); hov.forEach(a=>a.cancel()); hov=[]; isOpen=false; playing=true; const me=++run;
        fr.classList.add('bugplay');
        anims=ps.map(p=>{
          const ang=R(0,Math.PI*2), dist=R(700,1100), r=R(-160,160), d=R(0,750), fly=R(1500,1850);
          /* resting place before the lock: pushed outwards from the beetle's middle by a different amount each */
          const dx=+p.dataset.dx, dy=+p.dataset.dy, n=Math.hypot(dx,dy)||1, g=R(9,32);
          const k=Math.max(.55,Math.min(1,n*1.6)), ax=dx/n*g*k+R(-5,5), ay=dy/n*g*k+R(-5,5);
          const land=(d+fly)/T, hold=LOCK/T;
          return p.animate([
            {offset:0,transform:`translate(${Math.cos(ang)*dist}px,${Math.sin(ang)*dist}px) rotate(${r}deg) scale(1.25)`,opacity:0,easing:'step-end'},
            {offset:d/T,transform:`translate(${Math.cos(ang)*dist}px,${Math.sin(ang)*dist}px) rotate(${r}deg) scale(1.25)`,opacity:0,easing:'cubic-bezier(.2,.7,.3,1)'},
            {offset:(d+fly*.15)/T,opacity:1},
            {offset:land,transform:`translate(${ax}px,${ay}px)`,opacity:1},
            {offset:hold,transform:`translate(${ax}px,${ay}px)`,opacity:1,easing:'cubic-bezier(.6,0,.4,1.4)'},
            {offset:(LOCK+SNAP)/T,transform:'none',opacity:1},
            {offset:1,transform:'none',opacity:1}],
            {duration:T,fill:'both'});
        });
        /* all pieces locked: the real beetle takes over */
        Promise.all(anims.map(a=>a.finished)).then(()=>{ if(me===run){ playing=false; if(!isOpen) fr.classList.remove('bugplay'); } }).catch(()=>{});
      };
      /* pointer over the beetle: the pieces ease slightly apart, as just before they lock; they close again when it leaves */
      const X0=parseFloat(bug.style.left), Y0=parseFloat(bug.style.top), st=document.getElementById('stage'), intro=document.getElementById('intro');
      const RECTS=ps.map(p=>[X0+parseFloat(p.style.left), Y0+parseFloat(p.style.top), parseFloat(p.style.width), parseFloat(p.style.height)]);
      const OPEN=ps.map(p=>{ const dx=+p.dataset.dx, dy=+p.dataset.dy, n=Math.hypot(dx,dy)||1, g=R(5,15), k=Math.max(.55,Math.min(1,n*1.6));
        return `translate(${dx/n*g*k+R(-3,3)}px,${dy/n*g*k+R(-3,3)}px)`; });
      function setOpen(o){
        if(o===isOpen||playing) return; isOpen=o;
        const from=ps.map(p=>getComputedStyle(p).transform);
        hov.forEach(a=>a.cancel()); if(o) fr.classList.add('bugplay');
        hov=ps.map((p,i)=>p.animate([{transform:from[i]==='none'?'none':from[i],opacity:1},{transform:o?OPEN[i]:'none',opacity:1}],
          {duration:o?380:300,easing:o?'cubic-bezier(.2,.7,.3,1)':'cubic-bezier(.6,0,.4,1.3)',fill:'forwards'}));
        if(!o) Promise.all(hov.map(a=>a.finished)).then(()=>{ if(!isOpen&&!playing) fr.classList.remove('bugplay'); }).catch(()=>{});
      }
      addEventListener('mousemove',e=>{
        if(cur!=='intro'||playing){ if(isOpen&&!playing) setOpen(false); return; }
        const r=st.getBoundingClientRect(), s=r.width/1440, x=(e.clientX-r.left)/s, y=(e.clientY-r.top)/s+sc.scrollTop-intro.offsetTop;
        setOpen(RECTS.some(q=>x>=q[0]&&x<q[0]+q[2]&&y>=q[1]&&y<q[1]+q[3]));
      },{passive:true});
      document.addEventListener('mouseleave',()=>setOpen(false));
      document.addEventListener('pagechange',e=>{ if(e.detail==='intro') play(); });
      if(cur==='intro') play();
    }
  }catch(err){ console.warn('beetle animation skipped',err); }
  /* start page hint: pulsing dot that follows the pointer over the main area, with a note */
  try{
    const ih=document.getElementById('ihint'), st=document.getElementById('stage'), lab=ih&&ih.querySelector('.ilab');
    if(ih && matchMedia('(hover:hover)').matches){
      document.body.appendChild(ih);   /* outside the scaled page, so it sits exactly on the pointer */
      const hide=()=>{ ih.classList.remove('on'); document.body.classList.remove('ihoff'); };
      addEventListener('mousemove',e=>{
        const r=st.getBoundingClientRect(), s=r.width/1440, x=(e.clientX-r.left)/s, y=(e.clientY-r.top)/s;
        const lbOpen=document.getElementById('lb')&&document.getElementById('lb').open;
        const inMain=x>225&&x<1325&&y>32&&y<1024, onLink=e.target.closest('a,button');
        if(cur!=='intro'||lbOpen||!inMain||onLink){ hide(); return; }
        ih.style.transform=`translate(${e.clientX}px,${e.clientY}px)`; ih.classList.add('on'); document.body.classList.add('ihoff');
        const lw=lab.offsetWidth, lh=lab.offsetHeight, right=r.left+1325*s, top=r.top+32*s;
        ih.classList.toggle('l', e.clientX+14+lw+6>right);
        ih.classList.toggle('b', e.clientY-8-lh-6<top);
      },{passive:true});
      document.addEventListener('mouseleave',hide); document.addEventListener('pagechange',hide);
    }
  }catch(err){ console.warn('start page hint skipped',err); }
'''

if __name__ == '__main__':
    print(len(pieces), 'pieces', len(HTML), 'bytes')
