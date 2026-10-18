import re,base64,sys
s=open('site/index.html').read()
head=re.search(r'<head>(.*)</head>',s,re.S).group(1); body=re.search(r'<body>(.*)</body>',s,re.S).group(1)
head=re.sub(r'<meta[^>]*>\n?','',head); t=re.search(r'<title>.*?</title>',head).group(0); head=head.replace(t,'')
s=t+'\n'+head.strip()+'\n'+body.strip()
s=re.sub(r'<(link|script)[^>]*data-live-map[^>]*>(</script>)?\n?','',s)  # artifact pages cannot load map tiles: keep the static map
def uri(p):
    m={'svg':'image/svg+xml','png':'image/png','jpg':'image/jpeg','woff2':'font/woff2'}[p.rsplit('.',1)[1]]
    return f'data:{m};base64,'+base64.b64encode(open('site/'+p,'rb').read()).decode()
css=re.sub(r'url\((fonts/[^)]+)\)',lambda m:f'url({uri(m.group(1))})',open('site/fonts.css').read())
faces=[f for f in re.findall(r'@font-face\s*\{[^}]*\}',css) if not re.search('cyrillic|greek|vietnamese',f)]
s=s.replace('<link rel="stylesheet" href="fonts.css">','<style>'+''.join(faces)+'</style>').replace('<link rel="stylesheet" href="figma.css">','<style>'+open('site/figma.css').read()+'</style>')
s=re.sub(r'src="(img/[^"]+)"',lambda m:f'src="{uri(m.group(1))}"',s)
open(sys.argv[1],'w').write(s)
