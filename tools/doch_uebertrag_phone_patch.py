#!/usr/bin/env python3
"""Uebertrag DOCH!-Regeln (23.11.2026) auf die dasein-design-Phone-Seite - nur was passt, kein Inhalt.
Der "nach oben"-Knopf (#toTop) hatte noch CSS `border: 1px dotted` (dichter als die feine Linie 1 px Punkt / 2 px Luecke);
jetzt der Verlauf (--dh / --dv) wie ueberall. Gleiche Aenderung in tools/phone.py und phone/index.html; Version zusammen erhoeht.
Aufruf: python3 tools/doch_uebertrag_phone_patch.py <version>   (idempotent)"""
import sys, re
ver = sys.argv[1]
OLD = 'background:rgba(255,255,255,.94);border:1px dotted #b8b8b8;border-radius:0;'
NEW = ('border:0;border-radius:0;'
       'background:var(--dh) left top/100% 1px no-repeat,var(--dh) left bottom/100% 1px no-repeat,'
       'var(--dv) left top/1px 100% no-repeat,var(--dv) right top/1px 100% no-repeat,rgba(255,255,255,.94);')
done = False
for p in ('tools/phone.py', 'phone/index.html'):
    s = open(p, encoding='utf-8').read()
    if OLD in s:
        assert s.count(OLD) == 1, (p, s.count(OLD))
        s = s.replace(OLD, NEW)
        done = True
    elif NEW in s:
        print(p, 'schon angewendet')
    else:
        raise SystemExit(p + ': Muster nicht gefunden')
    if p == 'phone/index.html':
        m = re.search(r'const V="(\d+)"', s); assert m
        s = s[:m.start(1)] + ver + s[m.end(1):]
    open(p, 'w', encoding='utf-8').write(s)
open('phone/version.json', 'w').write('{"v": "%s"}' % ver)
print('ok', ver, 'geaendert' if done else 'nur Version')
