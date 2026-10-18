import json
from playwright.sync_api import sync_playwright
css=open('site/figma.css').read()
res={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':1024})
    for pid in ['intro','services','projects','downloads','bits','contact']:
        frag=open(f'frag/{pid}.html').read()
        pg.set_content(f'<html><head><base href="file:///home/claude/figma/site/"><style>{css} body{{margin:0}}</style></head><body><div id="F" style="position:relative;width:1440px;height:1024px">{frag}</div></body></html>')
        pg.wait_for_timeout(200)
        out=pg.evaluate('''()=>{
          const root=document.querySelector('#F > div');
          const r0=root.getBoundingClientRect();
          const rectOf=el=>{ if(getComputedStyle(el).display==='contents'){ let rs=[...el.children].map(rectOf).filter(Boolean); if(!rs.length) return null;
               return {left:Math.min(...rs.map(r=>r.left)),top:Math.min(...rs.map(r=>r.top)),right:Math.max(...rs.map(r=>r.right)),bottom:Math.max(...rs.map(r=>r.bottom))}; }
             const r=el.getBoundingClientRect(); return {left:r.left-r0.left,top:r.top-r0.top,right:r.right-r0.left,bottom:r.bottom-r0.top}; };
          const chrome=[],content=[],dropped=[];
          for(const el of [...root.children]){
            const r=rectOf(el); const id=el.dataset.nodeId;
            if(!r){dropped.push(id);continue;}
            const w=r.right-r.left,h=r.bottom-r.top;
            if(r.bottom<=0||r.top>=1024){dropped.push(id);continue;}
            if(h>1000&&w<4){dropped.push(id);continue;}          // full-height grid lines: replaced by the site's own overlay lines
            if(r.right<=226||r.left>=1324||(r.top<2&&r.bottom<=27)) chrome.push(el.outerHTML); else content.push(el.outerHTML);
          }
          return {chrome,content,dropped,rootClass:root.className};
        }''')
        res[pid]=out; print(pid,len(out['chrome']),len(out['content']),len(out['dropped']))
    b.close()
json.dump(res,open('frag/split.json','w'))
