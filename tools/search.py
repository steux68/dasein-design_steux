"""Site search: a thin red magnifier top right; a click opens a small pop-up between the grid lines
(x 1105-1325, under the menu) with "search site" in red. Typing lists the matching text from every page
(page name + snippet, accents ignored); a click on a result goes to that page and briefly marks the text.
Also the map zoom buttons in the same style: white circles with a thin red + / -.
build.py imports CSS, BUTTON (hot layer), JS and ZOOM_IN / ZOOM_OUT.
"""

LENS = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6.6"/>'
        '<path d="M14.8 14.8L20.6 20.6"/></svg>')
BUTTON = ('<button type="button" class="hot sbtn" id="sbtn" aria-label="search the site" aria-expanded="false" '
          f'style="left:1333px;top:0;width:25px;height:25px">{LENS}</button>'
          '<div class="spop" id="spop" hidden style="left:1105px;top:32px;width:220px">'
          '<input id="sq" type="search" placeholder="search site" autocomplete="off" spellcheck="false" aria-label="search site">'
          '<div id="sres" role="list"></div></div>')

ZOOM_IN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10.5"/><path d="M7.5 12H16.5M12 7.5V16.5"/></svg>'
ZOOM_OUT = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10.5"/><path d="M7.5 12H16.5"/></svg>'

CSS = '''
/* site search: the Figma magnifier is replaced by a red one, a little sturdier than the hairline arrows (like the map pin) */
.chrome [data-name="Search"]{display:none}
.sbtn{padding:0;margin:0;border:0;background:none;cursor:pointer;display:flex;align-items:center;justify-content:center}
.sbtn svg{width:21px;height:21px;fill:none;stroke:#e30613;stroke-width:2;stroke-linecap:round;overflow:visible}
.sbtn:hover svg,.sbtn:focus-visible svg,.sbtn[aria-expanded="true"] svg{animation:lbxp 1.4s ease-in-out infinite}
.sbtn:focus-visible{outline:none}
@media (prefers-reduced-motion:reduce){.sbtn svg{animation:none!important}}
.spop{position:absolute;z-index:40;box-sizing:border-box;padding:10px 12px 12px;background:rgba(255,255,255,.9);
  -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);box-shadow:0 8px 28px rgba(0,0,0,.10);font-family:Calibri,Carlito,sans-serif}
.spop input{display:block;width:100%;box-sizing:border-box;margin:0;padding:4px 0;border:0;border-bottom:var(--hp) dotted #b8b8b8;border-radius:0;
  background:none;font:400 15px/1.2 Calibri,Carlito,sans-serif;color:#000;outline:none;-webkit-appearance:none;appearance:none}
.spop input::placeholder{color:#e30613;opacity:1}
.spop input::-webkit-search-cancel-button{-webkit-appearance:none}
#sres{max-height:520px;overflow-y:auto;scrollbar-width:thin}
.sr{display:block;width:100%;box-sizing:border-box;text-align:left;margin:0;padding:6px 0;border:0;border-bottom:var(--hp) dotted #d6d6d6;background:none;cursor:pointer;
  font:400 12.5px/1.3 Calibri,Carlito,sans-serif;color:#222}
.sr .sp{display:block;color:#e30613;font-size:10.5px;letter-spacing:.06em}
.sr mark{background:#d4fb4d;color:inherit;padding:0 1px}
.sr:hover .st,.sr:focus-visible .st{color:#e30613}
.sr:focus-visible{outline:none}
.snone{padding-top:7px;font-size:12px;color:#888}
.sflash{background:rgba(212,251,77,.9)!important;box-shadow:0 0 0 3px rgba(212,251,77,.9)}
/* map zoom: white circles with a thin red + / -, like the search magnifier */
.mz{gap:4px!important}
.mz button{border:0!important;border-radius:50%;background:none!important;padding:0}
.mz button svg{display:block;width:100%;height:100%;overflow:visible}
.mz button circle{fill:rgba(255,255,255,.9);stroke:#e30613;stroke-width:2;vector-effect:non-scaling-stroke}
.mz button path{fill:none;stroke:#e30613;stroke-width:2;vector-effect:non-scaling-stroke;stroke-linecap:round}
.mz button:hover circle,.mz button:focus-visible circle{fill:rgba(212,251,77,.92)}
.mz button:focus-visible{outline:none}
'''

JS = '''
  /* site search */
  try{
    const sb=document.getElementById('sbtn'), pop=document.getElementById('spop'), q=document.getElementById('sq'), res=document.getElementById('sres');
    const NAMES={intro:'start',services:'us & our services',projects:'projects',downloads:'downloads & links',bits:'bits & bats',contact:'contact'};
    const norm=t=>t.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
    const esc=t=>t.replace(/&/g,'&amp;').replace(/</g,'&lt;');
    let IDX=null, hits=[];
    function index(){ IDX=[]; pgs.forEach(pg=>pg.querySelectorAll('p').forEach(p=>{
      const t=p.textContent.replace(/[\\s\\u200b]+/g,' ').trim(); if(t.length>1) IDX.push({pg:pg.id,el:p,t,n:norm(t)}); })); }
    function find(s){ s=norm(s.trim()); if(s.length<2) return []; const out=[], seen=new Set(), per={};   /* at most 3 hits per page, 12 in all, so every page gets a say */
      for(const r of IDX){ const i=r.n.indexOf(s); if(i<0) continue; const k=r.pg+'|'+r.n; if(seen.has(k)||(per[r.pg]||0)>=3) continue; seen.add(k); per[r.pg]=(per[r.pg]||0)+1; out.push({r,i,len:s.length}); if(out.length>=12) break; }
      return out; }
    function show(){
      if(!IDX) index(); hits=find(q.value);
      if(q.value.trim().length<2){ res.innerHTML=''; return; }
      if(!hits.length){ res.innerHTML='<div class="snone">nothing found</div>'; return; }
      res.innerHTML=hits.map((h,k)=>{ const t=h.r.t, a=Math.max(0,h.i-28), b=Math.min(t.length,h.i+h.len+40);
        return '<button type="button" class="sr" role="listitem" data-k="'+k+'"><span class="sp">'+NAMES[h.r.pg]+'</span><span class="st">'+(a>0?'… ':'')+esc(t.slice(a,h.i))+'<mark>'+esc(t.slice(h.i,h.i+h.len))+'</mark>'+esc(t.slice(h.i+h.len,b))+(b<t.length?' …':'')+'</span></button>'; }).join('');
    }
    function open(){ pop.hidden=false; sb.setAttribute('aria-expanded','true'); q.focus(); q.select(); }
    function close(){ pop.hidden=true; sb.setAttribute('aria-expanded','false'); }
    function pick(k){ const h=hits[k]; if(!h) return; close(); go(h.r.pg);
      setTimeout(()=>{ h.r.el.classList.add('sflash'); setTimeout(()=>h.r.el.classList.remove('sflash'),1800); },650); }
    sb.addEventListener('click',e=>{ e.stopPropagation(); pop.hidden?open():close(); });
    q.addEventListener('input',show);
    q.addEventListener('keydown',e=>{ e.stopPropagation();
      if(e.key==='Escape'){ close(); sb.focus(); } else if(e.key==='Enter'){ pick(0); }
      else if(e.key==='ArrowDown'){ e.preventDefault(); const f=res.querySelector('.sr'); if(f) f.focus(); } });
    res.addEventListener('click',e=>{ const b=e.target.closest('.sr'); if(b) pick(+b.dataset.k); });
    res.addEventListener('keydown',e=>{ e.stopPropagation(); const b=e.target.closest('.sr'); if(!b) return;
      if(e.key==='ArrowDown'){ e.preventDefault(); (b.nextElementSibling||b).focus(); }
      else if(e.key==='ArrowUp'){ e.preventDefault(); (b.previousElementSibling||q).focus(); }
      else if(e.key==='Escape'){ close(); sb.focus(); } });
    pop.addEventListener('wheel',e=>e.stopPropagation(),{passive:true});
    document.addEventListener('click',e=>{ if(!pop.hidden&&!e.target.closest('#spop,#sbtn')) close(); });
    document.addEventListener('pagechange',()=>{ if(document.activeElement!==q) close(); });
  }catch(err){ console.warn('search not available',err); }
'''
