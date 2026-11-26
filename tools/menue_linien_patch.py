# 26.11.2026: Menuebalken unten (phone/index.html) ohne gepunktete Trennlinien; der Farbkontrast genuegt. Idempotent.
# Aufruf im Hauptordner: python3 tools/menue_linien_patch.py   Zurueck: git revert dieses Commit.
import re, sys, json
f = 'phone/index.html'
s = open(f, encoding='utf-8').read()
if 'id="menue-linien-css"' in s: sys.exit('schon angewendet')
css = ('<style id="menue-linien-css">.pbar.hb[data-pc]{background-image:none!important}'
       '.pbar.hb[data-pc]::before,.pbar.hb[data-pc]::after{display:none!important}</style>')
assert s.count('</head>') == 1
s = s.replace('</head>', css + '</head>')
v = '20261126140000'
assert s.count('const V="20261125153800";') == 1
s = s.replace('const V="20261125153800";', 'const V="%s";' % v)
open(f, 'w', encoding='utf-8').write(s)
open('phone/version.json', 'w').write(json.dumps({"v": v}))
open('phone/version.txt', 'w').write(v)
print('ok')
