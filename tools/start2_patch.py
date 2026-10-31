# Startseite erzwingen (robuster als start_patch.py): Herzschlag in sessionStorage, Prüfung bei jedem Zurückkehren
# (visibilitychange, pageshow, focus, resume); Neustart ohne #-Anhang, wenn die letzte Aktivität > 30 s her ist.
# Aufruf im Repo-Hauptordner: python3 -I src/start2_patch.py <datei> [<datei> ...]
import re,sys
JS=('<script id="start-top">(function(){try{if("scrollRestoration" in history)history.scrollRestoration="manual";'
'var K="start-seen",LIM=30000,base=location.pathname+location.search;'
'function get(){try{return +sessionStorage.getItem(K)||0}catch(e){return 0}}'
'function put(){try{sessionStorage.setItem(K,String(Date.now()))}catch(e){}}'
'function stale(){var p=get();return p&&Date.now()-p>LIM}'
'function reset(){try{sessionStorage.removeItem(K)}catch(e){}location.replace(base)}'
'if(stale()&&location.hash){reset();return}put();'
'function back(){if(stale())reset();else put()}'
'setInterval(function(){if(document.visibilityState==="visible")put()},3000);'
'document.addEventListener("visibilitychange",function(){if(document.visibilityState==="hidden")put();else back()});'
'addEventListener("pageshow",function(e){if(e.persisted)location.reload();else back()});'
'addEventListener("focus",back);document.addEventListener("resume",back);addEventListener("pagehide",put);'
'}catch(e){}})();</script>')
for p in sys.argv[1:]:
    s=open(p,encoding='utf-8').read()
    n,c=re.subn(r'<script id="start-top">.*?</script>',lambda m:JS,s,count=1,flags=re.S)
    print(p,'ok' if c else 'KEIN start-top gefunden')
    open(p,'w',encoding='utf-8').write(n)
