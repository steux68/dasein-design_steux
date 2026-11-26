# 26.11.2026: Titelband einheitlich wie in PASSAGE und DOCH! (phone/index.html): Band 58 px hoch ab 8 px, Logo 42 px hoch mit Luft, Schalter mittig. Idempotent.
# Aufruf im Hauptordner: python3 tools/header_einheit_patch.py   Zurueck: git revert dieses Commit.
import re, sys, json
f = 'phone/index.html'
s = open(f, encoding='utf-8').read()
if 'id="header-einheit-css"' in s: sys.exit('schon angewendet')
css = ('<style id="header-einheit-css">header{padding-top:8px!important;padding-bottom:0!important}'
       '.row1{height:54px!important}.logo{height:38px!important;gap:calc(2.41vw - .7px)!important}.logo img{width:calc(9.07vw - 2.6px)!important;height:calc(9.07vw - 2.6px)!important}.logo span{font-size:calc(8.16vw - 2.35px)!important}</style>')
assert s.count('</head>') == 1
s = s.replace('</head>', css + '</head>')
old = re.search(r'const V="(\d+)";', s).group(0)
v = '20261126143000'
s = s.replace(old, 'const V="%s";' % v)
open(f, 'w', encoding='utf-8').write(s)
open('phone/version.json', 'w').write(json.dumps({"v": v})); open('phone/version.txt', 'w').write(v)
print('ok')
