"""Assemble the single-page site from the split Figma pages."""
import json
S = json.load(open('frag/split.json'))
ORDER = ['intro', 'services', 'projects', 'downloads', 'bits', 'contact']
ROOT = 'bg-white relative'  # each frame keeps Figma's root styling

sections = []
# Figma's pointer circles + numbers on the intro are redrawn as clean, clickable circles (same size, place and colours)
PIN_NODES = {'1:190', '1:212', '1:215', '1:218', '1:221', '1:210', '1:213', '1:216', '1:219', '1:222'}
for pid in ORDER:
    extra = ''
    items = S[pid]["content"]
    if pid == 'intro':
        items = [h for h in items if not any(f'data-node-id="{n}"' in h[:400] for n in PIN_NODES)]
        for (x, y), target, num in zip([(320, 347), (540, 744), (760, 298), (980, 692), (1200, 257)], ORDER[1:], ['01', '02', '03', '04', '05']):
            cls = 'pin'
            extra += f'<a class="hot {cls}" href="#{target}" style="left:{x}px;top:{y}px" aria-label="{target}">{num}</a>'
    sections.append(f'<section class="pg" id="{pid}"><div class="{ROOT} frame">{"".join(items)}{extra}</div></section>')

chromes = ''.join(f'<div class="chrome" data-pg="{pid}">{"".join(S[pid]["chrome"])}</div>' for pid in ORDER)
labels = ['us &amp; our services', 'projects', 'downloads &amp; links', 'bits &amp; bats', 'contact']
hot = ''.join(f'<a class="hot tab" href="#{pid}" style="left:{235 + 220 * i}px;top:0;width:200px;height:25px" aria-label="{labels[i]}"></a>' for i, pid in enumerate(ORDER[1:]))
hot += '<a class="hot" href="#intro" style="left:115px;top:0;width:110px;height:365px" aria-label="dasein-design home"></a>'

html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>dasein-design Big Stripes</title>
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="figma.css">
<style>
html,body{{margin:0;height:100%;overflow:hidden;background:#fff}}
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
.chrome [class*="h-[25px]"][class*="w-[190px]"]{{text-shadow:none!important}}
.hot.tab:hover,.hot.tab:focus-visible{{box-shadow:inset 0 0 0 calc(1.5px / var(--s,1)) #e30613;outline:none}}
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
.hot.pin:hover,.hot.pin:focus-visible,.hot.pin:active{{background:#d4fb4d;font-weight:700;z-index:7;border:calc(2.5px / var(--s,1)) solid #e30613;outline:none}}
.hot:focus-visible{{outline:2px solid red;outline-offset:2px}}
.gl{{position:absolute;left:0;top:0;pointer-events:none;z-index:30}}
/* dashed frames around images: same thin light-grey dash as the guide lines */
.frame .border-dashed.border-black{{border-width:0!important}}
.frame .border-dashed.border-black::after{{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;
  --c:#c4c4c4;--d:5px;--p:7.5px;--w:calc(1px / (var(--s,1) * var(--dpr,1)));
  background:
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/100% var(--w) no-repeat,
   repeating-linear-gradient(to right,var(--c) 0 var(--d),transparent var(--d) var(--p)) left bottom/100% var(--w) no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) left top/var(--w) 100% no-repeat,
   repeating-linear-gradient(to bottom,var(--c) 0 var(--d),transparent var(--d) var(--p)) right top/var(--w) 100% no-repeat}}
.gl i{{position:absolute;display:block}}
</style>
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
</div></div>
<script>
(function(){{
  const sc=document.getElementById('scroller'), pgs=[...sc.children];
  const chromes=[...document.querySelectorAll('.chrome')];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function go(id,instant){{const el=document.getElementById(id); if(el) sc.scrollTo({{top:el.offsetTop,behavior:(instant||reduce)?'auto':'smooth'}});}}
  document.addEventListener('click',e=>{{const a=e.target.closest('a[href^="#"]'); if(!a) return; e.preventDefault(); go(a.getAttribute('href').slice(1)); history.replaceState(null,'',a.getAttribute('href'));}});
  let cur='';
  const stage=document.getElementById('stage');
  document.querySelectorAll('.hot.tab').forEach((t,i)=>{{
    const on=()=>stage.dataset.hover=i, off=()=>delete stage.dataset.hover;
    t.addEventListener('mouseenter',on); t.addEventListener('mouseleave',off); t.addEventListener('focus',on); t.addEventListener('blur',off);
  }});
  function update(){{
    const i=Math.max(0,Math.min(pgs.length-1,Math.round(sc.scrollTop/1024))), id=pgs[i].id;
    if(id===cur) return; cur=id; chromes.forEach(c=>c.classList.toggle('on',c.dataset.pg===id)); document.querySelectorAll('.hot.tab').forEach(t=>t.classList.toggle('cur',t.getAttribute('href')==='#'+id));
  }}
  sc.addEventListener('scroll',update,{{passive:true}});
  addEventListener('keydown',e=>{{
    const d={{ArrowDown:1,PageDown:1,ArrowRight:1,' ':1,ArrowUp:-1,PageUp:-1,ArrowLeft:-1}}[e.key]; if(!d) return;
    e.preventDefault(); const i=Math.round(sc.scrollTop/1024)+d; go(pgs[Math.max(0,Math.min(pgs.length-1,i))].id);
  }});
  function fit(){{
    const s=Math.min(innerWidth/1440,innerHeight/1024);
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
  fit(); addEventListener('resize',fit);
  if(location.hash) go(location.hash.slice(1),true);
  update();
}})();
</script>
</body>
</html>
'''
open('site/index.html', 'w').write(html)
print(len(html))
