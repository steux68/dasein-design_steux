# 18.11.2026: dasein-design phone wie DOCH!/PASSAGE: vier Balken in voller Breite (je eine Zeile, 25 px, Grossbuchstaben), Text buendig,
# gepunktete Linie unter jedem Balken, Einrasten am Balken. Idempotent. Mit --preview wird phone/stack.html geschrieben (phone/index.html bleibt).
# Aufruf im Hauptordner: python3 tools/stackbars_patch.py [--preview]. Zurueck: git revert dieses Commit.
import re, sys, json
f = 'phone/index.html'
s = open(f, encoding='utf-8').read()
if 'id="stack-css"' in s:
    print('schon vorhanden'); sys.exit(0)
H = 25; HB = H - 1
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a)); s = s.replace(a, b)
rep("const H=22, bars=[...document.querySelectorAll('.pg .pbar')], secs=bars.map(b=>b.closest('.pg')), ROWS=Math.ceil(bars.length/2);",
    "const H=%d, bars=[...document.querySelectorAll('.pg .pbar')], secs=bars.map(b=>b.closest('.pg')), ROWS=bars.length;" % HB)
rep("const r=k>>1, right=k&1, sec=secs[k];", "const r=k, right=k&1, sec=secs[k];")
rep("sec.style.scrollMarginTop=(r*H+22)+'px';   /* lands", "sec.style.scrollMarginTop=(r*H+%d)+'px';   /* lands" % HB)
css = '''<style id="stack-css">
/* Balken: volle Breite, 25 px, Grossbuchstaben */
.stack main > .hb{height:%dpx!important;font-size:13px!important}
.stack main > .hb b{text-transform:uppercase;letter-spacing:1.6px;font-size:12.5px}
.stack main > .hb small{font-size:9.5px!important;margin-left:6px!important;letter-spacing:.5px}
.stack main > .hb.hl,.stack main > .hb.hr{margin:%dpx 10px -1px 10px!important}
.stack main > #start + .hb{margin-top:14px!important}
.stack main > .hb::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;pointer-events:none;background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px)}
/* Einrasten am Balken */
html{scroll-snap-type:y proximity}
main > section.pg{scroll-snap-align:start}
</style>
</head>''' % (H, HB)
rep('</head>', css)
if '--preview' in sys.argv:
    s = re.sub(r'<title>[^<]*</title>', '<title>dasein-design TEST volle Balken</title>', s, count=1)
    open('phone/stack.html', 'w', encoding='utf-8').write(s); print('ok phone/stack.html')
else:
    v = '20261118101500'
    assert s.count('const V="20261118094500";') == 1
    s = s.replace('const V="20261118094500";', 'const V="%s";' % v)
    open('phone/version.json', 'w').write(json.dumps({"v": v}))
    open(f, 'w', encoding='utf-8').write(s); print('ok', f)
