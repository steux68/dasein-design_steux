# Aufruf im Hauptordner: python3 tools/skala_patch.py   Zurueck: git revert dieses Commit.
# Schriftstufe .pcs (13px -> 12px, Skala 12/14/16). Idempotent.
import re, json
f='phone/index.html'; s=open(f,encoding='utf-8').read()
a='.pcs{margin:12px 0 0;font-size:min(13px,3.4vw);line-height:1.4}'
if a not in s: raise SystemExit('schon angewendet')
s=s.replace(a,'.pcs{margin:12px 0 0;font-size:12px;line-height:1.4}')
old=re.search(r'const V="(\d+)";',s).group(0); v='20261126150000'
s=s.replace(old,'const V="%s";'%v); open(f,'w',encoding='utf-8').write(s)
open('phone/version.json','w').write(json.dumps({"v":v})); open('phone/version.txt','w').write(v); print('ok')
