# phone: weisse "scroll"-Leisten oben/unten entfernt; stattdessen ein kleiner Chevron unten rechts zurueck nach oben. 06.11.2026.
import sys
p='phone/index.html'; s=open(p,encoding='utf-8').read()
if '/* totop */' in s: print('schon angewendet'); sys.exit(0)
CSS='''
/* totop */
html{--bar:0px!important}
.bar{border:0!important;background:none!important;pointer-events:none}.bar::after{display:none!important}.bar button{display:none!important}
#toTop{position:fixed;right:10px;bottom:calc(10px + env(safe-area-inset-bottom,0px));z-index:40;width:34px;height:34px;padding:0;display:flex;align-items:center;justify-content:center;
 background:rgba(255,255,255,.94);border:1px dotted #b8b8b8;border-radius:0;opacity:0;pointer-events:none;transition:opacity .25s;-webkit-tap-highlight-color:transparent}
#toTop.on{opacity:1;pointer-events:auto}
#toTop svg{width:20px;height:20px;fill:none;stroke:#3a3c37;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
'''
HTML='<button type="button" id="toTop" aria-label="back to the top"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 15L12 8L19 15"/></svg></button>'
JS='''<script id="totop-js">(function(){var b=document.getElementById('toTop');if(!b)return;
function upd(){var y=innerHeight-10;document.querySelectorAll('.pbar').forEach(function(p){var r=p.getBoundingClientRect(),bt=parseFloat(getComputedStyle(p).bottom);if(!isNaN(bt)&&r.height&&r.bottom>=innerHeight-bt-3&&r.top<y)y=r.top;});
 b.style.bottom=Math.max(10,innerHeight-y+8)+'px';b.classList.toggle('on',scrollY>260);}
b.onclick=function(){scrollTo({top:0,behavior:'smooth'});};addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();})();</script>'''
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
j=s.rindex('</body>') if '</body>' in s else len(s)
s=s[:j]+HTML+JS+s[j:]
s=s.replace('const V="20261101094842"','const V="20261106200000"')
open(p,'w',encoding='utf-8').write(s)
open('phone/version.json','w').write('{"v":"20261106200000"}')
print('ok')
