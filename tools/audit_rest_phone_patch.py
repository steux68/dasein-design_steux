"""Audit Punkt 9 + Kleinkram (phone/index.html): Platzhalter raus, Rasterlinie unter das Pop-up, Beschriftungen, Fokus-Rahmen.
Aufruf: python3 tools/audit_rest_phone_patch.py <version>"""
import sys,re,json,html
V=sys.argv[1]; p='phone/index.html'; s=open(p,encoding='utf8').read(); n={}
n['platz']=0  # Platzhalter-Texte bleiben vorerst stehen (Steuart, 26.11.)
def wg(m):
    t=m.group(0); line=re.search(r'data-line="([^"]*)"',t)
    if not line: return t
    l=line.group(1)
    t=t.replace('class="wg"','class="wg" aria-label="%s"'%l,1)
    return re.sub(r'alt=""','alt="%s"'%l,t,1)
s,n['wg']=re.subn(r'<button type="button" class="wg"[^>]*>\s*<img [^>]*>',wg,s)
def tile(m):
    t=m.group(0); b=re.search(r'<b>(.*?)</b>',m.group(0)); return t
def tl(m):
    img,cap=m.group(1),m.group(2)
    t=html.unescape(re.sub('<[^>]+>','',cap)).title() if False else re.sub('<[^>]+>','',cap)
    return img.replace('alt=""','alt="%s"'%t,1)+m.group(3)+cap
s,n['tile']=re.subn(r'(<button type="button" class="tile"[^>]*>\s*<img [^>]*>)(<span class="cap">)(.*?)(</span>)',lambda m:m.group(1).replace('alt=""','alt="%s"'%re.sub('<[^>]+>','',m.group(3)),1)+m.group(2)+m.group(3)+m.group(4),s)
css='<style id="audit-rest">#wpop{z-index:50}:focus-visible{outline:2px solid #1a1a1a;outline-offset:2px}</style>'
if 'id="audit-rest"' in s: s=re.sub(r'<style id="audit-rest">.*?</style>',css,s,flags=re.S)
else: s=s.replace('</head>',css+'</head>',1)
s,k=re.subn(r'const V="\d+"','const V="%s"'%V,s); assert k==1
open(p,'w',encoding='utf8').write(s)
open('phone/version.json','w').write(json.dumps({"v":V})); open('phone/version.txt','w').write(V)
print(n)
