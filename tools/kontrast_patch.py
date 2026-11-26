"""Audit Punkt 3+4: 5-s-Regel -> 30 min (nur DOCH/PASSAGE, Flag --lim), Text-Grau #8a8a86/#8a8a8a -> #6e6e6a (nur color:),
weisse Ziffern auf #777 -> #707070, Telefon-Gruen #1e8e3e -> #167a32.  Aufruf: kontrast_patch.py index.html [--lim]"""
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf8').read(); n={}
s,n['grau']=re.subn(r'(?<![-\w])color:(\s*)#8a8a8[6a]',r'color:\1#6e6e6a',s)
s,n['777']=re.subn(r'(background(?:-color)?:\s*)#777(!important)?(;color:#fff)',r'\1#707070\2\3',s)
s,n['gruen']=re.subn(r'#1e8e3e','#167a32',s)
if '--lim' in sys.argv: s,n['lim']=re.subn(r'LIM=5000','LIM=1800000',s)
open(p,'w',encoding='utf8').write(s); print(p,n)
