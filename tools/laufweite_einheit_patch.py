import re,sys
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
def m(x):
    v=float(x.group(1))
    n='0' if v<=.03 else '.06em' if v<=.08 else '.12em'
    return 'letter-spacing:'+n
t=re.sub(r'letter-spacing:\s*(\.\d+)em',lambda x:(m(x)+'' if m(x)=='letter-spacing:0' else m(x)),s)
print(f.split('/')[-3] if 'phone' in f else f.split('/')[-2], len(re.findall(r'letter-spacing:\s*\.\d+em',s)),'->',len(re.findall(r'letter-spacing:\s*(?:\.06em|\.12em|0)\b',t)))
open(f,'w',encoding='utf-8').write(t)
