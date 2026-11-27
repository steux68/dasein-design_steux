# phone: Leiste "Alle Links/Projekte" schlank (wie die DOCH-Zeile): grosser limettengruener Pfeil-Kreis links, Text daneben, gepunktete Linien oben/unten. 27.11.2026
import sys
p='phone/index.html'; s=open(p,encoding='utf-8').read()
if '/* morebar-v2 */' in s: print('schon angewendet'); sys.exit(0)
CSS='''
/* morebar-v2 */
.more.mbar{justify-content:flex-start;gap:10px;height:44px;margin:6px 0 12px;padding:0 2px;font-size:13px;letter-spacing:.1em;
 background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left bottom/100% 1px no-repeat}
.more.mbar[aria-expanded=true]{margin-top:8px}
.more.mbar .mcv{position:static;margin:0;width:30px;height:30px;flex:none;order:-1}
.more.mbar .mcv .c{fill:#cdff3e;stroke-width:1.6}
.more.mbar .mcv path{stroke-width:1.9}
'''
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
s=s.replace('"20261127211000"','"20261127222000"'); open(p,'w',encoding='utf-8').write(s)
open('phone/version.json','w').write('{"v": "20261127222000"}\n'); print('ok')
