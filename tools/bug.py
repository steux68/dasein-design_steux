"""Start page: the beetle flies in as a collage of torn pieces and puts itself together (about 3 s).

The beetle image (transparent background) is cut into an irregular grid of pieces that tile exactly;
only pieces that contain some beetle are kept. Each piece flies in from outside, turned and slightly
larger, lands a little askew and then snaps into place; at the end the real image takes over.
It plays when the site opens on the start page, never with "reduce motion" switched on.
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

# grid points, the inner ones moved about so the pieces look torn rather than cut
xs = [bx0 + (bx1 - bx0) * i / COLS for i in range(COLS + 1)]
ys = [by0 + (by1 - by0) * j / ROWS for j in range(ROWS + 1)]
cw, ch = (bx1 - bx0) / COLS, (by1 - by0) / ROWS
pt = {}
for i in range(COLS + 1):
    for j in range(ROWS + 1):
        dx = rnd.uniform(-.3, .3) * cw if 0 < i < COLS else 0
        dy = rnd.uniform(-.3, .3) * ch if 0 < j < ROWS else 0
        pt[i, j] = (xs[i] + dx, ys[j] + dy)


def edge(a, b, n=3, amp=6):
    """a ragged edge from a to b: a few small zigzags, the same for both pieces that share it"""
    key = (min(a, b), max(a, b))
    r = random.Random(hash(key) & 0xffffffff)
    out = []
    for t in range(1, n + 1):
        f = t / (n + 1)
        out.append((a[0] + (b[0] - a[0]) * f + r.uniform(-amp, amp), a[1] + (b[1] - a[1]) * f + r.uniform(-amp, amp)))
    return out if a <= b else out


pieces = []
apx = alpha.load()
for i in range(COLS):
    for j in range(ROWS):
        c = [pt[i, j], pt[i + 1, j], pt[i + 1, j + 1], pt[i, j + 1]]
        poly = []
        for q in range(4):
            a, b = c[q], c[(q + 1) % 4]
            mid = edge(min(a, b), max(a, b))
            if a > b:
                mid = mid[::-1]
            poly += [a] + mid
        px0, py0 = int(min(p[0] for p in poly)), int(min(p[1] for p in poly))
        px1, py1 = int(max(p[0] for p in poly)) + 1, int(max(p[1] for p in poly)) + 1
        # keep the piece only if there is beetle inside it
        hits = sum(1 for x in range(max(0, px0), min(W, px1), 3) for y in range(max(0, py0), min(H, py1), 3) if apx[x, y] > 100)
        if hits < 40:
            continue
        pieces.append(dict(b=[px0, py0, px1 - px0, py1 - py0],
                           c=' '.join(f'{x - px0:.1f}px {y - py0:.1f}px,' for x, y in poly).rstrip(',')))

HTML = (f'<div class="bug" id="bug" aria-hidden="true" style="left:{X0}px;top:{Y0}px;width:{W}px;height:{H}px">'
        + ''.join(f'<div class="bp" style="left:{p["b"][0]}px;top:{p["b"][1]}px;width:{p["b"][2]}px;height:{p["b"][3]}px">'
                  f'<i style="clip-path:polygon({p["c"]});background-position:{-p["b"][0]}px {-p["b"][1]}px"></i></div>'
                  for p in pieces)
        + '</div>')

CSS = f'''
/* start page: the beetle arrives as a collage and puts itself together */
.bug{{position:absolute;pointer-events:none;display:none;z-index:1;clip-path:inset({32 - Y0}px 0 {Y0 + H - 1024}px 0)}}   /* fly only inside the main area */
.bugplay .bug{{display:block}}
.bugplay [data-node-id="1:144"]{{visibility:hidden}}
.bp{{position:absolute;opacity:0;will-change:transform}}
.bp i{{position:absolute;inset:0;background:url({SRC}) no-repeat;background-size:{W}px {H}px}}
'''

JS = '''
  /* start page: the beetle flies in as torn pieces and puts itself together, about 2.5 seconds */
  try{
    const bug=document.getElementById('bug'), fr=bug&&bug.parentElement;
    if(bug && cur==='intro' && !reduce && bug.animate){
      fr.classList.add('bugplay');
      const ps=[...bug.children], R=(a,b)=>a+Math.random()*(b-a);
      const done=ps.map((p,n)=>{
        const ang=R(0,Math.PI*2), dist=R(700,1100), r=R(-140,140), d=R(0,800);
        const a=p.animate([
          {transform:`translate(${Math.cos(ang)*dist}px,${Math.sin(ang)*dist}px) rotate(${r}deg) scale(1.25)`,opacity:0,filter:'drop-shadow(0 10px 8px rgba(0,0,0,.28))'},
          {opacity:1,offset:.12},
          {transform:`translate(${R(-7,7)}px,${R(-7,7)}px) rotate(${R(-5,5)}deg) scale(1.02)`,offset:.82,filter:'drop-shadow(0 3px 3px rgba(0,0,0,.18))'},
          {transform:'none',opacity:1,filter:'drop-shadow(0 0 0 rgba(0,0,0,0))'}],
          {duration:R(1650,2050),delay:d,easing:'cubic-bezier(.22,.7,.3,1)',fill:'both'});
        return a.finished;
      });
      /* all pieces in place: the real beetle takes over */
      Promise.all(done).then(()=>setTimeout(()=>{fr.classList.remove('bugplay'); bug.remove();},120));
    }
  }catch(err){ console.warn('beetle animation skipped',err); }
'''

if __name__ == '__main__':
    print(len(pieces), 'pieces', len(HTML), 'bytes')
