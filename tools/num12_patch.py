# Tab-Nummern "[01]" von 10 auf 12 px (kleinste Stufe der Skala). Idempotent. Aufruf im Repo-Stamm: python3 -I <script> <datei> <version>
import re, sys
f, ver = sys.argv[1], sys.argv[2]
s = open(f, encoding='utf-8').read()
if 'id="num12-css"' in s: sys.exit('schon angewendet')
css = '<style id="num12-css">small.n,.seg button small.n,nav .tab small,.pbar small,.wbt small{font-size:12px!important}</style>'
i = s.rindex('</style>') + len('</style>'); s = s[:i] + css + s[i:]
if ver != '-':
    s = re.sub(r'(<meta name="app-version" content=")([^"]*)(")', lambda m: m.group(1)+ver+m.group(3), s, count=1)
open(f, 'w', encoding='utf-8').write(s); print('ok', f)
