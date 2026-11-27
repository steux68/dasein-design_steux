# phone: Leiste "Alle Links/Projekte": runder weisser Knopf mit Chevron und sanft pulsierendem Ring (wie das (+) der CV-Knoepfe). 27.11.2026
import sys
p='phone/index.html'; s=open(p,encoding='utf-8').read()
if '/* morebar-pulse */' in s: print('schon angewendet'); sys.exit(0)
OLD='<i class="mchev" aria-hidden="true"></i>'
NEW='<svg class="cvx mcv" viewBox="-12 -12 24 24" aria-hidden="true"><circle class="r1" r="8"/><circle class="r2" r="8"/><circle class="c" r="8"/><path d="M-3.6 -1.4L0 2.2L3.6 -1.4" fill="none"/></svg>'
assert s.count(OLD)==2; s=s.replace(OLD,NEW)
CSS='''
/* morebar-pulse */
.more.mbar{position:relative}
.more.mbar .mcv{position:absolute;left:12px;top:50%;margin-top:-10px;width:20px;height:20px}
.more.mbar[aria-expanded=true] .mcv path{transform:rotate(180deg)}
'''
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
s=s.replace('"20261127210500"','"20261127211000"'); open(p,'w',encoding='utf-8').write(s)
open('phone/version.json','w').write('{"v": "20261127211000"}\n'); print('ok')
