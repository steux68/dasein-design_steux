# phone: "mehr"-Knopf der langen Raster (Projekte, Links) wird eine Leiste ueber die ganze Breite unten (Steuart, 27.11.2026).
# Statt rundem (+) im Rauschen: blasse Leiste in der Farbe des aktuellen Abschnitts, gepunktete Oberkante, "ALLE LINKS (n) v" / "WENIGER ^".
# Einmal anwenden: python3 tools/more_band_patch.py   (aus dem Repo-Stamm)
import re, sys
p = 'phone/index.html'
s = open(p, encoding='utf-8').read()
if '/* morebar */' in s:
    print('schon angewendet'); sys.exit(0)

BANDS = {  # data-g: (EN, DE, Farbe)
    'g-proj':  ('all projects', 'Alle Projekte', '#fdf3bf'),   # blasses Gelb wie die Leiste PROJEKTE
    'g-links': ('all links',    'Alle Links',     '#dfe9fb'),   # blasses Blau wie die Leiste DOWNLOADS & LINKS
}
n = 0
for g, (en, de, col) in BANDS.items():
    pat = re.compile(r'<button type="button" class="cvb more" aria-expanded="false" data-g="%s">.*?</button>' % g, re.S)
    new = ('<button type="button" class="cvb more mbar" aria-expanded="false" data-g="%s" style="--bt:%s">'
           '<span class="mo"><span class="en">%s</span><span class="de">%s</span> <i class="mn"></i></span>'
           '<span class="mc"><span class="en">fewer</span><span class="de">Weniger</span></span><i class="mchev" aria-hidden="true"></i></button>') % (g, col, en, de)
    s, k = pat.subn(new, s, count=1); n += k
assert n == 2, n

CSS = '''
/* morebar */
.more.mbar{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;height:36px;margin:0 0 14px;padding:0 10px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#222;
 background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,var(--bt,#f2f2f2)}
.more.mbar[aria-expanded=true]{margin-top:8px}
.more.mbar .mn{font-style:normal;font-weight:400;letter-spacing:.04em}
.more.mbar .mc{display:none} .more.mbar[aria-expanded=true] .mc{display:inline} .more.mbar[aria-expanded=true] .mo{display:none}
.more.mbar .de{display:none} html[lang=de] .more.mbar .de{display:inline} html[lang=de] .more.mbar .en{display:none}
.more.mbar .mchev{width:8px;height:8px;border-right:1.8px solid #222;border-bottom:1.8px solid #222;transform:translateY(-2px) rotate(45deg);transition:transform .2s}
.more.mbar[aria-expanded=true] .mchev{transform:translateY(2px) rotate(-135deg)}
.cut.shut[data-extra="0"],.cut.shut#g-proj,.cut.shut#g-links{-webkit-mask-image:linear-gradient(#000 calc(100% - 44px),rgba(0,0,0,.22));mask-image:linear-gradient(#000 calc(100% - 44px),rgba(0,0,0,.22))}
.more.mbar:focus-visible{outline:2px solid var(--red);outline-offset:-2px}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]

JS = '''<script id="morebar-js">(function(){document.querySelectorAll('.more.mbar').forEach(function(b){var g=document.getElementById(b.dataset.g),n=b.querySelector('.mn');if(g&&n)n.textContent='('+g.children.length+')';});})();</script>'''
j = s.rindex('</body>') if '</body>' in s else len(s)
s = s[:j] + JS + s[j:]

s = s.replace('"20261127170000"', '"20261127210500"')
open(p, 'w', encoding='utf-8').write(s)
open('phone/version.json', 'w').write('{"v": "20261127210500"}\n')
print('ok')
