# 25.11.2026: Schriftgroessen der Handy-Fassung auf 12 / 14 / 16 px (wie PASSAGE und DOCH!): 12,5 -> 12, 13 -> 14, kleine Marken -> 10.
# Aufruf im Hauptordner: python3 -I tools/skala2_phone_patch.py   (setzt danach die Versionsnummer neu). Idempotent.
import subprocess, sys, json, re
r = subprocess.run([sys.executable, '-I', 'tools/skala2_patch.py', 'phone/index.html'], capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip())
if 'schon angewendet' in r.stdout: sys.exit(0)
v = '20261125111500'
s = open('phone/index.html', encoding='utf-8').read()
m = re.search(r'const V="(\d+)";', s); assert m
s = s.replace(m.group(0), 'const V="%s";' % v, 1)
open('phone/index.html', 'w', encoding='utf-8').write(s)
open('phone/version.json', 'w').write(json.dumps({"v": v}))
open('phone/version.txt', 'w').write(v + '\n')
print('Version', v)
