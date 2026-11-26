# Audit 27.11., Punkt 7: gemeinsame common.js (gleicher Inhalt wie in DOCH & PASSAGE) für die Zurück-Taste auf phone/.
# Vorher hatte die Seite keinen Verlauf: Zurück bei offenem Wonder-Pop-up verließ die Seite.
# Jetzt: Wonder-Bild-Pop-up → Projekt-Pop-up (dialog) → wonder → nach oben → Seite verlassen.
# Aufruf aus dem Repo-Ordner: python3 tools/common_phone_patch.py NEUE_VERSION (z. B. 20261126180000)
import sys,re,json
V=sys.argv[1]; p='phone/index.html'; s=open(p,encoding='utf-8').read()
if 'src="common.js' not in s:
    i=s.index('</head>'); s=s[:i]+'<script src="common.js?v=%s"></script>'%V+s[i:]
s=re.sub(r'src="common\.js\?v=[^"]*"','src="common.js?v=%s"'%V,s)
WIRE='''<script id="common-wire">/* Audit 27.11., Punkt 7 (common.js): Zurück schließt zuerst das Bild-Pop-up, dann das Projekt-Pop-up, dann wonder, dann nach oben, dann verlässt es die Seite */
(function(){if(!window.AppBack)return;const $=id=>document.getElementById(id),P=AppCommon.press,sw=$('wsw'),wp=$('wpop'),wd=$('wonder');let toTop=false;
 const dl=()=>document.querySelectorAll('dialog[open]'),won=()=>!!sw&&sw.getAttribute('aria-pressed')==='true';
 AppBack
  .add({open:()=>!!wp&&!wp.hidden,close:()=>{if(!P('wback'))wp.hidden=true;}})
  .add({open:()=>dl().length>0,close:()=>{const a=dl();a[a.length-1].close();}})
  .add({open:won,close:()=>{sw.click();}})
  .add({open:()=>{if(toTop){if(scrollY<60)toTop=false;return false;}return scrollY>=60;},
        close:()=>{toTop=true;scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}})
  .init();
 addEventListener('scroll',()=>{if(toTop&&scrollY<60)toTop=false;},{passive:true});
})();</script>'''
if 'id="common-wire"' in s: s=re.sub(r'<script id="common-wire">.*?</script>',lambda m:WIRE,s,flags=re.S)
else: s=s.rstrip('\n')+'\n'+WIRE+'\n'
s,n=re.subn(r'const V="\d+"','const V="%s"'%V,s); assert n==1
open(p,'w',encoding='utf-8').write(s)
open('phone/version.json','w').write(json.dumps({"v":V}))
open('phone/version.txt','w').write(V)
print('ok',V)
