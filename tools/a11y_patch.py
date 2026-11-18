# 18.11.2026: Zugaenglichkeit, unsichtbar (phone/index.html und index.html): role=main, unsichtbare h1, Namen fuer die CV-/Bio-Schalter,
# groessere Beruehrungsflaeche fuer die Karten-Links. Aussehen unveraendert. Idempotent. Aufruf im Hauptordner: python3 tools/a11y_patch.py
# Nach einem Neubau mit phone.py einmal erneut ausfuehren. Zurueck: git revert dieses Commit.
import re, sys, json
CSS = '<style id="a11y-css">a[href*="openstreetmap"]{position:relative}a[href*="openstreetmap"]::after{content:"";position:absolute;left:-8px;right:-8px;top:50%;height:44px;transform:translateY(-50%)}</style>\n'
JS = '''<script id="a11y-js">(function(){var m=document.querySelector("main")||document.querySelector(".strip");
if(m&&m.tagName!=="MAIN"&&!m.getAttribute("role"))m.setAttribute("role","main");
if(!document.querySelector("h1")){var h=document.createElement("h1");h.textContent="dasein-design \\u00b7 architecture + design \\u00b7 Wien";h.style.cssText="position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0";var t=m||document.body;t.insertBefore(h,t.firstChild);}
document.querySelectorAll("button.cvb").forEach(function(b){if(!(b.innerText||"").trim()&&!b.getAttribute("aria-label"))b.setAttribute("aria-label","show or hide the full text");});})();</script>
'''
for f in ('phone/index.html', 'index.html'):
    s = open(f, encoding='utf-8').read()
    if 'id="a11y-js"' in s:
        print(f, 'schon vorhanden'); continue
    assert s.count('</body>') == 1 and s.count('</head>') == 1, f
    s = s.replace('</head>', CSS + '</head>').replace('</body>', JS + '</body>')
    if f.startswith('phone'):
        v = '20261118094500'
        assert s.count('const V="20261118003658";') == 1
        s = s.replace('const V="20261118003658";', 'const V="%s";' % v)
        open('phone/version.json', 'w').write(json.dumps({"v": v}))
    open(f, 'w', encoding='utf-8').write(s)
    print(f, 'ok')
