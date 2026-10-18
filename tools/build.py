"""Assemble the single-page site from the split Figma pages."""
import json
S = json.load(open('frag/split.json'))
ORDER = ['intro', 'services', 'projects', 'downloads', 'bits', 'contact']
ROOT = 'bg-white relative'  # each frame keeps Figma's root styling

sections = []
for pid in ORDER:
    extra = ''
    if pid == 'intro':  # the numbered pointers on the beetle jump to their pages
        for (x, y), target in zip([(320, 347), (540, 744), (760, 298), (980, 692), (1200, 257)], ORDER[1:]):
            extra += f'<a class="hot pin" href="#{target}" style="left:{x}px;top:{y}px;width:30px;height:30px" aria-label="{target}"></a>'
    sections.append(f'<section class="pg" id="{pid}"><div class="{ROOT} frame">{"".join(S[pid]["content"])}{extra}</div></section>')

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
.hot.tab:hover{{background:rgba(255,255,255,.25);outline:1px solid rgba(0,0,0,.15)}}
.hot.pin{{border-radius:50%}}
.hot.pin:hover{{background:rgba(205,255,62,.55)}}
.hot:focus-visible{{outline:2px solid red;outline-offset:2px}}
.gl{{position:absolute;inset:0;pointer-events:none;z-index:30}}
.gl i{{position:absolute;top:0;bottom:0;background:#e9e9e9;mix-blend-mode:multiply}}
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
<div class="gl" id="gl"></div>
</div></div>
<script>
(function(){{
  const sc=document.getElementById('scroller'), pgs=[...sc.children];
  const chromes=[...document.querySelectorAll('.chrome')];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function go(id,instant){{const el=document.getElementById(id); if(el) sc.scrollTo({{top:el.offsetTop,behavior:(instant||reduce)?'auto':'smooth'}});}}
  document.addEventListener('click',e=>{{const a=e.target.closest('a[href^="#"]'); if(!a) return; e.preventDefault(); go(a.getAttribute('href').slice(1)); history.replaceState(null,'',a.getAttribute('href'));}});
  let cur='';
  function update(){{
    const i=Math.max(0,Math.min(pgs.length-1,Math.round(sc.scrollTop/1024))), id=pgs[i].id;
    if(id===cur) return; cur=id; chromes.forEach(c=>c.classList.toggle('on',c.dataset.pg===id));
  }}
  sc.addEventListener('scroll',update,{{passive:true}});
  addEventListener('keydown',e=>{{
    const d={{ArrowDown:1,PageDown:1,ArrowRight:1,' ':1,ArrowUp:-1,PageUp:-1,ArrowLeft:-1}}[e.key]; if(!d) return;
    e.preventDefault(); const i=Math.round(sc.scrollTop/1024)+d; go(pgs[Math.max(0,Math.min(pgs.length-1,i))].id);
  }});
  function fit(){{
    const s=Math.min(innerWidth/1440,innerHeight/1024);
    document.documentElement.style.setProperty('--s',s);
    const dpr=devicePixelRatio||1, lw=Math.max(1,Math.round(1.6*s*dpr))/dpr;
    document.getElementById('gl').innerHTML=[115,225,445,665,885,1105,1325].map(x=>`<i style="left:${{Math.round(x*s*dpr)/dpr-lw/2}}px;width:${{lw}}px"></i>`).join('');
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
