# Schriftgroessen-Skala, zweiter Durchgang (25.11.2026): Nachzuegler der Stufen 12 / 14 / 16 px einfangen.
#   10.5 bis <13  -> 12     13 bis <15 -> 14     15 bis <19 -> 16     8 bis <10.5 -> 10 (kleine Marken, z. B. [01])
#   Titel ab 19 px, Logos und Werte unter 8 px bleiben. Nur CSS-Angaben "font-size:" in px/rem. Idempotent.
# Aufruf: python3 -I src/skala2_patch.py [Datei=index.html] [--noversion] [--ver=NAME]
import re, sys
args = [a for a in sys.argv[1:] if not a.startswith('--')]
path = args[0] if args else 'index.html'
s = open(path, encoding='utf-8').read()
if '<!--skala2-->' in s:
    print('schon angewendet'); sys.exit(0)
n = 0
def snap(px):
    if px >= 19 or px < 8: return None
    if px < 10.5: return 10
    if px < 13: return 12
    if px < 15: return 14
    return 16
def f(m):
    global n
    v = float(m.group(1)); px = v * 16 if m.group(2) == 'rem' else v
    t = snap(px)
    if t is None or abs(t - px) < 0.01: return m.group(0)
    n += 1
    return 'font-size:%dpx' % t
s = re.sub(r'font-size:(\d*\.?\d+)(rem|px)(?![\w.%])', f, s)
print('ersetzt', n)
s = s.replace('</head>', '<!--skala2--></head>', 1)
ver = [a[6:] for a in sys.argv[1:] if a.startswith('--ver=')]
if '--noversion' not in sys.argv and ver:
    s = re.sub(r'(<meta name="app-version" content=")([^"]*)(")', lambda m: m.group(1) + ver[0] + m.group(3), s, count=1)
open(path, 'w', encoding='utf-8').write(s)
