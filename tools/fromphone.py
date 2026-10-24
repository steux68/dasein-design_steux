"""Desktop site: the changes first made on the phone version (21 Oct 2026), applied to index.html.

Run from tools/:  python3 fromphone.py   (patches ../index.html in place; safe to run again)
build.py also calls patch() before writing, so a full rebuild keeps them.

- texts instead of the Latin placeholders (shared with the phone through texts.py)
- "dasein-design" in text always in the logo red; phone numbers green, e-mail links blue
- beetle: dotted leader lines redrawn, white in "difference" (they show over the dark beetle),
  ending in yellow dots with a black ring on legs, jaw and mouth; the circles light up yellow-lime in turn
  and send out coloured rings
- project pop-up: close drawn like the compass signs; the counter sits between previous and next at the bottom
- link logos trimmed to their edges (img/m-lg-*), with a small margin in their boxes
- the two long CVs fold to just over half the page, with a "full CV" opener
- IT, PROJEKTE and SKILLS icons drawn in the compass style (img/ic-*.svg)
- one job per line: no white dashed edges on the tabs, no --- text dividers, no e-mail underlines
- synchronised with the phone: vertical title "about us", no placeholder captions on the ID cards, one address and phone format, red client subtitles
- three quick clicks on the beetle: the red heart, as on the phone
- menu: the first tab reads "about us [01]" (half tabs were tried and dropped)
"""
import re
from texts import INTRO, BIO, INFO_TXT, LINKS_TXT, CONTACT_TXT, LEGAL_BODY, BITS, CARDS, CARD_AT
import json
import os
from lightbox import compass

MARK = '<!--fromphone-->'
RED = '#e30613'


def _sub1(pat, rep, s, flags=0):
    s2, n = re.subn(pat, rep, s, count=1, flags=flags)
    assert n == 1, pat
    return s2


def _rep(a, b, s, n=1):
    assert s.count(a) >= n, a[:80]
    return s.replace(a, b)


# ---------- the beetle's leader lines: circle centre -> elbow -> end on the beetle (desktop page pixels)
LEADS = [((1215, 800), (1215, 703), (1152, 703)),   # i impressum -> tip of the lower antler
         ((335, 377), (335, 420), (580, 420)),     # 01 about us -> back leg
         ((555, 744), (555, 652), (648, 652)),     # 02 projects -> back foot
         ((775, 328), None, (775, 432)),           # 03 downloads & links -> middle leg
         ((1215, 287), (1215, 524), (1005, 524))]  # 05 contact -> mouth
R = 4.5
FIGMA_LINES = ['1:225', '1:228', '26:180', '30:639', '26:181', '30:640', '26:186', '26:187']


def _leads():
    paths, dots = '', ''
    for a, m, b in LEADS:
        pts = [a] + ([m] if m else []) + [b]
        (x1, y1), (x2, y2) = pts[-2], pts[-1]   # stop the line at the dot's edge
        if x1 == x2:
            y2 = y2 - R if y2 > y1 else y2 + R
        else:
            x2 = x2 - R if x2 > x1 else x2 + R
        pts[-1] = (x2, y2)
        paths += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in pts) + '"/>'
        dots += f'<circle cx="{b[0]}" cy="{b[1]}" r="{R}"/>'
    return (f'<svg class="dlead" viewBox="0 0 1440 1024" aria-hidden="true">{paths}</svg>'
            f'<svg class="dlead dots" viewBox="0 0 1440 1024" aria-hidden="true">{dots}</svg>')


CSS = '''
/* ---- from the phone version (fromphone.py) ---- */
.dd{color:#e30613}
a[href^="tel:"]{color:#1e8e3e;text-decoration:none} a[href^="mailto:"]{color:#1a5fd0}
.plab b{color:#e30613}
/* beetle: new leader lines (the Figma ones are hidden) */
''' + ','.join(f'[data-node-id="{n}"]' for n in FIGMA_LINES) + '''{display:none!important}
.dlead{position:absolute;left:0;top:0;width:1440px;height:1024px;pointer-events:none;z-index:4;overflow:visible;mix-blend-mode:difference}
.dlead path{fill:none;stroke:#fff;stroke-width:1.2;stroke-dasharray:1.2 2.2}
.dlead.dots{mix-blend-mode:normal}
.dlead circle{fill:#ffd400;stroke:#000;stroke-width:1.2}
/* the circles light up yellow-lime in turn (01 ... 05), each sending out its two coloured rings, then turn grey again */
.hot.pin{animation:pinon 9s ease-in-out infinite;animation-delay:calc(var(--k) * 1.5s)}
@keyframes pinon{0%{background:#bfbfbf}2.5%{background:#cdff3e}14%{background:#cdff3e}16.7%{background:#bfbfbf}100%{background:#bfbfbf}}
.pin .cr{position:absolute;inset:-1px;border-radius:50%;border:1.6px solid var(--c1);opacity:0;pointer-events:none;
  animation:pinturn 9s ease-out infinite;animation-delay:calc(var(--k) * 1.5s + .3s)}
.pin .cr.c2{border-color:var(--c2);animation-delay:calc(var(--k) * 1.5s + .6s)}
@keyframes pinturn{0%{transform:scale(1);opacity:.9}12.5%{transform:scale(2.3);opacity:0}100%{transform:scale(2.3);opacity:0}}
.hot.pin:hover,.hot.pin:focus-visible,.hot.pin.near{animation:none}
.hot.pin.near{animation:pinpulse 1.5s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){.hot.pin,.pin .cr{animation:none}}
/* texts */
.ptx{position:absolute;font:400 12px/1.4 Calibri,Carlito,sans-serif;color:#222;margin:0}
.ptx p{margin:0 0 6px} .ptx .lab2{font-weight:700;font-size:11px;letter-spacing:.12em;color:#e30613;margin-bottom:4px}
.ptx.bio{font-size:11px;line-height:1.35} .ptx.bio p{margin-bottom:4px}
.ptx.end{font-family:Calibri,Carlito,sans-serif;font-weight:700;font-size:12px;line-height:normal;color:#000}   /* in the contact address type */
.ptx.end .hd{font-style:normal;font-weight:700;margin:0 .35em}
.ptx.end .hd:first-child{margin-left:0}
/* pop-up: close like the compass signs; the counter between previous and next */
.lbx{width:24px;height:24px}
.lbx svg{width:22px;height:22px;stroke:none}
.lbx .rg{fill:none;stroke:#3a3c37;stroke-width:var(--hp)} .lbx .xx{fill:none;stroke:#1a1a1a;stroke-width:1.15;stroke-linecap:round;transition:stroke .2s}
.lbx:hover .rg,.lbx:focus-visible .rg{stroke:#e30613} .lbx:hover .xx,.lbx:focus-visible .xx{stroke:#e30613}
/* project counter at the top, centred on the pop-up and level with the close cross, the previous / next project arrows either side (23 Oct) */
.lbk{left:50%;right:auto;top:30px;transform:translateX(-50%);gap:10px;z-index:4}
.lbk .ar{width:22px;height:22px}
.lbk .lbkc{display:inline-block;min-width:13.5em;text-align:center;white-space:nowrap;font:400 13px/25px Calibri,Carlito,sans-serif;color:#666;letter-spacing:.06em;font-variant-numeric:tabular-nums}   /* room for three-figure numbers (100+) so the arrows never shift */
.lbk .lbkc b{color:#e30613;font-weight:400}
/* the two long CVs on the us & our services page end just over half way down, faded, with a "full CV" opener; open, they run to the foot as designed */
[data-node-id="1:622"],[data-node-id="1:623"]{max-height:165px;overflow:hidden;overscroll-behavior:contain;transition:max-height .45s ease;
  -webkit-mask-image:linear-gradient(#000 62%,transparent);mask-image:linear-gradient(#000 62%,transparent)}
.frame.cvo1 [data-node-id="1:623"],.frame.cvo2 [data-node-id="1:622"]{max-height:335px;overflow-y:auto;-webkit-mask-image:none;mask-image:none}
.dcv{position:absolute;z-index:6;display:flex;align-items:center;gap:6px;border:0;background:none;padding:0;cursor:pointer;font:400 13px/1 Calibri,Carlito,sans-serif;letter-spacing:.04em;color:#000}
.dcv b{color:#e30613;font-weight:700;font-size:14px;margin-left:-2px} .dcv .cvt{font-weight:300}
.dcv svg{width:20px;height:20px;overflow:visible}
.dcv .c{fill:#fff;stroke:#e30613;stroke-width:1.5} .dcv path{stroke:#e30613;stroke-width:1.6;stroke-linecap:round}
.dcv .r1,.dcv .r2{fill:none;stroke:#cdff3e;stroke-width:2.2;transform-box:fill-box;transform-origin:center;animation:cvp 1.8s ease-out infinite}
.dcv .r2{animation-delay:.9s}
@keyframes cvp{0%{transform:scale(1);opacity:.95}100%{transform:scale(1.9);opacity:0}}
.dcv[aria-expanded=true] .v,.dcv[aria-expanded=true] .r1,.dcv[aria-expanded=true] .r2{display:none}
.dcv .cl{display:none} .dcv[aria-expanded=true] .cl{display:inline} .dcv[aria-expanded=true] .op{display:none}
.dcv:hover .cvt,.dcv:focus-visible .cvt{color:#e30613} .dcv:focus-visible{outline:none}
/* open: the opener moves up beside the top of its CV and reads "close CV" */
.frame.cvo1 .dcv1,.frame.cvo2 .dcv2{top:596px!important;left:var(--xo)!important}
@media (prefers-reduced-motion:reduce){.dcv .r1,.dcv .r2{display:none} [data-node-id="1:622"],[data-node-id="1:623"]{transition:none}}
/* the four service icons, drawn in the compass style, a touch smaller (90 %) */
img[src^="img/ic-"]{transform:scale(.9)}
/* one job per line (22 Oct, as on the phone): dashed = page structure, dotted = round pictures only.
   No white dashed edge on the menu tabs, no underlines under e-mail addresses */
.border-dashed.border-white{border-color:transparent!important}
a[href^="mailto:"],a[href^="mailto:"] span{text-decoration:none!important}
/* services: a dotted line across each partner's column at the tick y 440, in place of the red bars above the names */
.pline{position:absolute;top:620px;width:420px;height:1px;z-index:3;background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px)}
.sub2{color:#e30613;font-size:11px;letter-spacing:.12em;margin-bottom:3px!important}
.rs{display:inline-block;width:2.5px;height:.9em;margin:0 6px;vertical-align:-.08em;background:#3a3c37}
/* impressum: a small dot above the copyright in the right-hand bar; it opens a pop-up */
/* impressum: written upwards above the copyright like it - a circled i (like the ©) that flashes now and then; red on hover */
.hot.imp{display:flex;justify-content:center;text-decoration:none}
.hot.imp span{writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;font:400 11px Calibri,Carlito,sans-serif;letter-spacing:.03em;color:#777;transition:color .2s}
.hot.imp b{font-weight:700;font-size:12px;color:#000;transition:color .2s}
.hot.imp .ii{display:inline-block;width:13px;height:13px;line-height:11px;text-align:center;border:1.2px solid #000;border-radius:50%;font:700 9px/11px Calibri,Carlito,sans-serif;font-style:normal;color:#000;box-sizing:border-box;animation:iiflash 3.2s ease-in-out infinite}
@keyframes iiflash{0%,70%,100%{border-color:#000;color:#000;background:transparent}80%{border-color:#e30613;color:#e30613;background:#cdff3e}}
.hot.imp.cur span,.hot.imp.cur b,.hot.imp:hover span,.hot.imp:hover b,.hot.imp:focus-visible span,.hot.imp:focus-visible b{color:#e30613}
.hot.imp:hover .ii{animation:none;border-color:#e30613;color:#e30613;background:#cdff3e} .hot.imp:focus-visible{outline:none}
@media (prefers-reduced-motion:reduce){.hot.imp .ii{animation:none}}
.impc{position:absolute;column-count:2;column-gap:20px;font:400 12px/1.5 Calibri,Carlito,sans-serif;color:#222}
.impc .lab2{margin:0 0 6px;font-weight:700;font-size:11px;letter-spacing:.14em;color:#e30613;column-span:all}
.impc .lp{color:#666;font-size:11.5px;margin:0 0 4px;column-span:all}
.impc h4{margin:12px 0 2px;font-size:12px;font-weight:700;color:#000;break-after:avoid} .impc p{margin:0;break-inside:avoid}
.impc .ib{break-inside:avoid;-webkit-column-break-inside:avoid;display:block;overflow:hidden}
.impc a{color:#1a5fd0;text-decoration:none} .impc a[href^="tel:"]{color:#1e8e3e} .impc .todo{color:#e30613}
.ci{display:inline-block;font-style:normal;width:.95em;height:.95em;line-height:.85em;text-align:center;border:.07em solid currentColor;border-radius:50%;font-size:.8em;vertical-align:.05em}
.impl{pointer-events:auto;color:#000;text-decoration:none;font-weight:400;transition:color .2s}
.impl:hover,.impl:focus-visible,.impl.cur{color:#e30613;font-weight:700;outline:none}
/* three clicks on the beetle: the heart */
.heartfx{position:fixed;inset:0;z-index:9999;pointer-events:none;overflow:hidden}
.heartfx svg{position:absolute;left:0;top:0;width:60px;height:60px;margin:-30px 0 0 -30px;fill:#e30613;will-change:transform,opacity}
.heartfx .sm{width:16px;height:16px;margin:-8px 0 0 -8px}
/* link logos trimmed to their edges, with a small margin in their boxes */
img[src^="img/m-lg-"]{box-sizing:border-box;padding:6px 12px;background:#fff}   /* white ground in every logo box: three logos (zt:, …) are cut out, and the grey showed through (24 Oct) */
'''




HEART_JS = r"""<script>
/* the two CVs: "full CV" opens one, "close CV" folds it again; both fold when you leave the page */
(function(){
  const fr=document.querySelector('#services .frame'); if(!fr) return;
  const bs=[...fr.querySelectorAll('.dcv')];
  bs.forEach(b=>b.addEventListener('click',()=>{ const k=b.dataset.k, on=!fr.classList.contains('cvo'+k);
    fr.classList.toggle('cvo'+k,on); b.setAttribute('aria-expanded',String(on)); }));
  document.addEventListener('pagechange',e=>{ if(e.detail!=='services'){ fr.classList.remove('cvo1','cvo2'); bs.forEach(b=>b.setAttribute('aria-expanded','false')); } });
})();
</script><script>
/* three quick clicks on the beetle (within 0.9 s): a red heart pops out, zooms up until the screen is red and bursts into little hearts (as on the phone) */
(function(){
  const bug=document.getElementById('bug'); if(!bug||!document.body.animate) return;
  const fr=bug.parentElement, X0=parseFloat(bug.style.left), Y0=parseFloat(bug.style.top);
  const RECTS=[...bug.querySelectorAll('.bp')].map(p=>[X0+parseFloat(p.style.left),Y0+parseFloat(p.style.top),parseFloat(p.style.width),parseFloat(p.style.height)]);
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches, R=(a,b)=>a+Math.random()*(b-a);
  const HEART='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21.3s-7.6-4.7-10.1-9.4C.3 8.6 1.9 4.6 5.6 4.2c2.4-.3 4 1.1 6.4 3.5 2.4-2.4 4-3.8 6.4-3.5 3.7.4 5.3 4.4 3.7 7.7C19.6 16.6 12 21.3 12 21.3z"/></svg>';
  const onBug=e=>{ const r=fr.getBoundingClientRect(), s=r.width/1440, x=(e.clientX-r.left)/s, y=(e.clientY-r.top)/s;
    return RECTS.some(q=>x>=q[0]&&x<q[0]+q[2]&&y>=q[1]&&y<q[1]+q[3]); };
  let hearting=false, taps=[];
  function heart(cx,cy){
    if(hearting) return; hearting=true;
    const fx=document.createElement('div'); fx.className='heartfx'; fx.innerHTML=HEART; document.body.appendChild(fx);
    const h=fx.firstChild, big=Math.hypot(innerWidth,innerHeight)/60*2.8, at=`translate(${cx}px,${cy}px)`;
    const zoom=h.animate([
      {transform:at+' scale(0)',opacity:1},
      {transform:at+' scale(1.3)',opacity:1,offset:.16,easing:'ease-out'},
      {transform:at+' scale(1)',opacity:1,offset:.24},
      {transform:at+' scale(1.12)',opacity:1,offset:.32},
      {transform:at+' scale(1)',opacity:1,offset:.4,easing:'cubic-bezier(.5,0,.9,.6)'},
      {transform:`translate(${innerWidth/2}px,${innerHeight*.6}px) scale(${big})`,opacity:1,offset:1}],{duration:reduce?600:1500,fill:'forwards'});
    fx.animate([{background:'rgba(227,6,19,0)',offset:0},{background:'rgba(227,6,19,0)',offset:.8},{background:'rgba(227,6,19,1)',offset:1}],{duration:reduce?600:1500,fill:'forwards'});
    zoom.finished.then(()=>{
      fx.animate([{background:'rgba(227,6,19,1)'},{background:'rgba(227,6,19,0)'}],{duration:reduce?300:420,easing:'ease-in',fill:'forwards'});
      h.animate([{opacity:1},{opacity:0}],{duration:reduce?300:420,easing:'ease-in',fill:'forwards'});
      const n=reduce?0:60, mx=innerWidth/2, my=innerHeight/2, bits=[];
      for(let i=0;i<n;i++){ const d=document.createElement('div'); d.innerHTML=HEART; const sv=d.firstChild; sv.classList.add('sm'); fx.appendChild(sv);
        const a=R(0,Math.PI*2), r=R(.35,.8)*Math.max(innerWidth,innerHeight), sc=R(.6,1.6), rot=R(-90,90);
        bits.push(sv.animate([{transform:`translate(${mx}px,${my}px) scale(${sc*2}) rotate(0deg)`,opacity:1},
          {transform:`translate(${mx+Math.cos(a)*r}px,${my+Math.sin(a)*r}px) scale(${sc}) rotate(${rot}deg)`,opacity:0}],{duration:R(700,1200),easing:'cubic-bezier(.1,.8,.3,1)',fill:'forwards'}).finished); }
      return Promise.all(bits);
    }).catch(()=>{}).then(()=>{ fx.remove(); hearting=false; });
  }
  document.addEventListener('click',e=>{
    if(e.target.closest('a,button,dialog')||!onBug(e)) return;
    const t=performance.now(); taps=taps.filter(x=>t-x<900); taps.push(t);
    if(taps.length>=3){ taps=[]; heart(e.clientX,e.clientY); }
  });
})();
</script>"""

XC = ('<svg viewBox="-12 -12 24 24" aria-hidden="true"><circle class="rg" r="9.5"/>'
      '<path class="xx" d="M-3.6 -3.6L3.6 3.6M3.6 -3.6L-3.6 3.6"/></svg>')
RINGS = [('#ffd400', '#2f8cff'), ('#2fbf4a', '#ffd400'), ('#2f8cff', '#cdff3e'), ('#e30613', '#2fbf4a'), ('#cdff3e', '#e30613')]


def _tab_names(s):
    """in every page's menu the first tab reads "about us [01]" (full-size tabs; half tabs were tried and dropped, 21 Oct)"""
    def lab(m):
        spans = re.findall(r'<span class="([^"]*)">([^<]*)</span>', m.group(2))
        first = next(c for c, t in spans if t.strip() and t.strip() != '&amp;')
        return f'{m.group(1)}<span class="{first}">about us </span><span class="{spans[-1][0]}">[01]</span></p>'
    s, n = re.subn(r'(left-\[335px\][^"]*?w-\[190px\]" data-node-id="[^"]+"><p[^>]*>)(.*?)</p>', lab, s, flags=re.S)
    assert n == 6, n
    return _rep('aria-label="us &amp; our services"', 'aria-label="about us"', s)


def _closing_div(s, i):
    """index just after the </div> that closes the <div ...> starting at i"""
    depth = 0
    for m in re.finditer(r'<(/?)div\b[^>]*>', s[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return i + m.end()
    raise ValueError


def _impressum_page(s):
    """a page after contact, like it: the impressum written out, vertical title "impressum [§]"; no tab of its own (reached by the (i) above the copyright)"""
    # each heading travels with its text, so a column never ends on a lone heading (22 Oct)
    legal = re.sub(r'(<h4>.*?</h4>)(<p[^>]*>.*?</p>)', r'<div class="ib">\1\2</div>', LEGAL_BODY, flags=re.S)
    body = f'<div class="impc" style="left:235px;top:60px;width:860px"><p class="lab2">IMPRESSUM</p>{legal}</div>'
    i = s.index('<section class="pg" id="contact"'); j = s.index('</section>', i) + len('</section>')
    s = s[:j] + f'<section class="pg" id="impressum"><div class="bg-white relative frame">{body}</div></section>' + s[j:]
    i = s.index('<div class="chrome" data-pg="contact">'); j = _closing_div(s, i)
    ch = s[i:j].replace('data-pg="contact"', 'data-pg="impressum"', 1)
    ch = ch.replace('<span class="fcal-b leading-[normal] text-[50px]">contact </span><span class="fcal-r leading-[normal] text-[20px]">[05]</span>',
                    '<span class="fcal-b leading-[normal] text-[50px]">impressum </span><span class="fcal-r leading-[normal] text-[20px]">[§]</span>')
    ch = ch.replace('bg-[rgba(205,255,62,0.86)]', 'bg-[rgba(0,0,0,0.05)]').replace('<span class="fcal-b leading-[normal] text-[18px]">contact </span>', '<span class="fcal-r leading-[normal] text-[15px]">contact </span>')
    s = s[:j] + ch + s[j:]
    # while on the impressum page its (i) link in the right-hand bar stays red
    return s.replace('</body>', '<script>document.addEventListener("pagechange",e=>document.querySelectorAll("a.impl").forEach(a=>a.classList.toggle("cur",e.detail==="impressum")));</script></body>', 1)


# ---------- bits & bats (22 Oct): every tile opens a pop-up; six tiles become notes / links (as on the phone);
# the pop-up steps through all 33 photos and 10 cards in the phone's order
BITS_CELLS = [((895, 60), 0), ((675, 440), 1), ((235, 820), 6), ((455, 630), 4), ((1115, 630), 7), ((1115, 250), 9)]


def _bits_items():
    items = []
    for k, (im, t, c) in enumerate(BITS):
        if k in CARD_AT:
            kind, src, head, txt, url = CARDS[CARD_AT[k]]
            items.append({'t': kind, 'c': CARD_AT[k], 'src': src, 'head': head, 'txt': txt, 'url': url})
        items.append({'t': 'img', 'im': 'img/' + im, 'cap': c})
    return items


def _bits_card(x, y, k):
    kind, src, head, txt, url = CARDS[k]
    plain = re.sub(r'<[^>]+>', '', txt)
    if kind == 'news':
        body, lab, sub = f'<small>{src}</small><b>{head}</b><em>{plain}</em>', f'LINK · {src}', 'read the article ↗'
    else:
        body = f'<i class="qm">“</i><b>{head}</b>'
        lab, sub = ('STUDIO NOTE', 'dasein-design') if src == 'studio note' else ('QUOTE', src)
    return (f'<button type="button" class="bcard {kind}" data-c="{k}" style="left:{x}px;top:{y}px"><span class="bct">{body}</span>'
            f'<span class="bcap"><b>{lab}</b><span>{sub}</span></span></button>')


BITS_CSS = """
/* bits & bats: cards among the photos and the pop-up */
#bits .bhit{position:absolute;z-index:4;padding:0;border:0;background:none;cursor:pointer}
#bits .bhit:hover{outline:1px solid #e30613;outline-offset:-1px}
#bits .bcard{position:absolute;z-index:5;width:200px;height:180px;padding:0;border:0;text-align:left;font:inherit;color:#222;cursor:pointer;overflow:hidden;font-family:Calibri,Carlito,sans-serif}
#bits .bcard::after{content:"";position:absolute;inset:0;pointer-events:none;border:1px dotted #b8b8b8}
#bits .bcard.news{background:#f4f4f4} #bits .bcard.note{background:#fffbd6}
#bits .bcard:hover{outline:1px solid #e30613;outline-offset:-1px}
#bits .bct{position:absolute;inset:0 0 35px;display:flex;flex-direction:column;gap:4px;padding:10px 10px 6px;overflow:hidden}
#bits .bct small{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#e30613;font-weight:700}
#bits .bct b{font-size:14px;line-height:1.2;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;flex:none}
#bits .bct em{font-style:normal;font-size:11px;line-height:1.35;color:#555;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
#bits .bcard.note .qm{font-style:normal;font-size:36px;line-height:.6;height:14px;color:#e30613}
#bits .bcard.note .bct b{font-weight:400;font-style:italic;font-size:14px;line-height:1.3;-webkit-line-clamp:5}
#bits .bcap{position:absolute;left:0;right:0;bottom:0;height:35px;padding:0 3px;display:flex;flex-direction:column;justify-content:center;background:rgba(68,68,68,.7);color:#fff;font-size:12px;line-height:normal}
#bits .bcap b{font-weight:700} #bits .bcap span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
dialog.bv{position:fixed;inset:0;width:100vw;height:100vh;max-width:none;max-height:none;margin:0;padding:0;border:0;background:#fff;font-family:Calibri,Carlito,sans-serif;color:#000}
dialog.bv::backdrop{background:transparent}
.bv .bvp{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:min(980px,88vw);height:min(820px,90vh);display:flex;flex-direction:column}
.bv .bvt{display:flex;justify-content:flex-end;align-items:center;height:34px;flex:none}
.bv .bvx{border:0;background:none;padding:4px;cursor:pointer} .bv .bvx svg{width:26px;height:26px} .bv .bvx .rg{fill:none;stroke:#3a3c37;stroke-width:.6} .bv .bvx .xx{fill:none;stroke:#1a1a1a;stroke-width:1.15;stroke-linecap:round}
.bv .bvx:hover .rg{stroke:#e30613}
.bv button:focus:not(:focus-visible){outline:none}
.bv .bvm{flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center}
.bv .bvm img{max-width:100%;max-height:100%;object-fit:contain;outline:1px dotted #b8b8b8;outline-offset:3px}
.bv .bvc{max-width:620px;padding:0 20px} .bv .bvc .lab{font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:#222;margin:0 0 10px}
.bv .bvc h2{margin:0 0 14px;font-size:30px;line-height:1.15;color:#e30613} .bv .bvc p{margin:0;font-size:18px;line-height:1.55;color:#222}
.bv .bvc .q{font-size:26px;line-height:1.45;font-style:italic} .bv .bvc .qm{display:block;font-style:normal;font-size:80px;line-height:.5;height:36px;color:#e30613}
.bv .bvc .todo{color:#e30613} .bv .bvc a.open{display:inline-block;margin-top:20px;font-size:17px;color:#1a5fd0;text-decoration:none;border-bottom:1px dotted #b8b8b8;padding-bottom:3px}
.bv .bvc a.open:hover{color:#e30613}
.bv .bvcap{flex:none;text-align:center;margin:14px 0 4px;font-size:16px;font-weight:700;color:#e30613;min-height:20px}
.bv .bvn{flex:none;display:flex;justify-content:center;align-items:center;gap:18px;height:44px;font-size:14px;color:#666;letter-spacing:.06em}
.bv .bvn button{display:flex;align-items:center;gap:8px;border:0;background:none;font:inherit;color:#000;cursor:pointer;padding:4px}
.bv .bvn button:hover{color:#e30613}
"""

BITS_JS = """
  const fr=document.querySelector('#bits .frame'), bv=document.getElementById('bv'); if(!fr||!bv) return; let cur=0;
  const n=IT.length, $=id=>document.getElementById(id), p2=k=>String(k).padStart(2,'0');
  function show(k){ cur=(k+n)%n; const it=IT[cur], m=$('bvm');
    if(it.t==='img'){ m.innerHTML='<img alt="" src="'+it.im+'">'; $('bvcap').innerHTML=it.cap; }
    else if(it.t==='news'){ m.innerHTML='<div class="bvc"><p class="lab">'+it.src+'</p><h2>'+it.head+'</h2><p>'+it.txt+'</p><a class="open" href="'+it.url+'" target="_blank" rel="noopener">read the article on '+it.src+' \\u2197</a></div>'; $('bvcap').innerHTML='link'; }
    else { m.innerHTML='<div class="bvc"><i class="qm">\\u201c</i><p class="lab">'+it.src+'</p><p class="q">'+it.txt+'</p></div>'; $('bvcap').innerHTML=it.src==='studio note'?'studio note':'quote'; }
    $('bvk').textContent='bits & bats '+p2(cur+1)+' / '+n; }
  function open(k){ show(k); if(!bv.open) bv.showModal(); }
  /* every photo on the page gets a clear button on top of it */
  const mk=()=>{ fr.querySelectorAll('.bhit').forEach(b=>b.remove()); const f=fr.getBoundingClientRect(), sc=(f.width/fr.offsetWidth)||1;
    fr.querySelectorAll('img').forEach(im=>{ const src=im.getAttribute('src'), k=IT.findIndex(x=>x.im===src); if(k<0) return;
      const t=im.parentElement.closest('[data-node-id]')||im.parentElement, r=t.getBoundingClientRect();
      const b=document.createElement('button'); b.type='button'; b.className='bhit'; b.setAttribute('aria-label','open photo');
      Object.assign(b.style,{left:(r.left-f.left)/sc+'px',top:(r.top-f.top)/sc+'px',width:r.width/sc+'px',height:r.height/sc+'px'});
      b.addEventListener('click',()=>open(k)); fr.appendChild(b); }); };
  if(document.readyState==='complete') mk(); else addEventListener('load',mk);
  fr.querySelectorAll('.bcard').forEach(c=>c.addEventListener('click',()=>open(IT.findIndex(x=>x.c===+c.dataset.c))));
  $('bvx').onclick=()=>bv.close(); $('bvprev').onclick=()=>show(cur-1); $('bvnext').onclick=()=>show(cur+1);
  bv.addEventListener('click',e=>{ if(e.target===bv) bv.close(); });
  bv.addEventListener('wheel',e=>{ e.preventDefault(); e.stopPropagation(); },{passive:false});
  bv.addEventListener('keydown',e=>{ e.stopPropagation(); if(e.key==='ArrowLeft') show(cur-1); else if(e.key==='ArrowRight') show(cur+1); });
"""


def _bits(s):
    i = s.index('id="bits"'); j = s.index('<section', i + 10)
    k = s.index('<div class="bg-white relative frame">', i) + len('<div class="bg-white relative frame">')
    assert k < j
    s = s[:k] + ''.join(_bits_card(x, y, c) for (x, y), c in BITS_CELLS) + s[k:]
    W, E = compass('W', 22), compass('E', 22)
    dlg = ('<dialog class="bv" id="bv" aria-label="bits &amp; bats"><div class="bvp">'
           f'<div class="bvt"><button type="button" class="bvx" id="bvx" aria-label="close (Esc)" title="close (Esc)">{XC}</button></div>'
           '<div class="bvm" id="bvm"></div><div class="bvcap" id="bvcap"></div>'
           f'<div class="bvn"><button type="button" id="bvprev">{W}<span>previous</span></button><span id="bvk"></span>'
           f'<button type="button" id="bvnext"><span>next</span>{E}</button></div></div></dialog>')
    js = '<script>(function(){ const IT=' + json.dumps(_bits_items()) + ';' + BITS_JS + '})();</script>'
    return s.replace('</body>', dlg + js + '</body>', 1)


EXT_JS = r'''<script>/* every link to another site opens in a new tab / window, so this site stays open behind it */
(function(){ const ext=a=>a&&/^https?:/i.test(a.getAttribute('href')||'')&&a.host!==location.host;
  const mark=a=>{ a.target='_blank'; a.rel='noopener'; };
  document.querySelectorAll('a[href]').forEach(a=>{ if(ext(a)) mark(a); });
  document.addEventListener('click',e=>{ const a=e.target.closest&&e.target.closest('a[href]'); if(ext(a)) mark(a); },true); })();</script>'''


# ---------- the beetle game (22 Oct, evening; ported from the phone): a pulsing dot with "press me" at the foot of the impressum page
# opens it full screen. Four foods - red dot 1, red ring 2, blue diamond 5, yellow star 10 - first to 100 wins.
# On the desktop the dot follows the mouse once the game has started (no need to hold the button down)
GAME_CSS = """
.pgo{position:absolute;z-index:6;display:flex;align-items:center;border:0;background:none;padding:0;font:inherit;cursor:pointer;font-family:Calibri,Carlito,sans-serif}
.pgo .pme{font-size:14px;letter-spacing:.08em;color:#666;white-space:nowrap} .pgo:hover .pme{color:#e30613}
.pgo .pld{width:34px;height:1px;margin:0 2px 0 7px;background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px)}
.pdot{position:absolute;left:0;top:0;width:44px;height:44px;margin:-22px 0 0 -22px;display:flex;align-items:center;justify-content:center;cursor:grab}
.pgo .pdot{position:relative;margin:0}
.pdot b{width:12px;height:12px;border-radius:50%;background:#cdff3e;box-shadow:0 0 0 1px #3a3c37;animation:pdp 1.4s ease-in-out infinite}
.pdot::before,.pdot::after{content:"";position:absolute;left:50%;top:50%;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;border:1px solid #e30613;opacity:0;animation:pdr 1.8s ease-out infinite}
.pdot::after{animation-delay:.9s}
@keyframes pdp{50%{transform:scale(1.25)}} @keyframes pdr{0%{transform:scale(1);opacity:.8}100%{transform:scale(4.2);opacity:0}}
dialog.game{position:fixed;inset:0;width:100vw;height:100vh;max-width:none;max-height:none;margin:0;padding:0;border:0;background:#fff;overflow:hidden;font-family:Calibri,Carlito,sans-serif}
dialog.game::backdrop{background:transparent}
.play{position:absolute;inset:0;overflow:hidden;touch-action:none;user-select:none;-webkit-user-select:none;cursor:default}
.play.go{cursor:none}
.ptrail{position:absolute;inset:0;width:100%;height:100%}
.gx{position:absolute;right:22px;top:20px;z-index:4;border:0;background:none;padding:4px;cursor:pointer} .gx svg{width:28px;height:28px} .gx .rg{fill:none;stroke:#3a3c37;stroke-width:.6} .gx .xx{fill:none;stroke:#1a1a1a;stroke-width:1.15;stroke-linecap:round} .gx:hover .rg{stroke:#e30613}
.pscore{position:absolute;left:30px;right:80px;top:26px;display:flex;justify-content:space-between;font-size:15px;letter-spacing:.06em;color:#555;pointer-events:none;z-index:2}
.pscore b{color:#e30613;font-size:20px;margin-left:5px}
.phint{position:absolute;left:0;right:0;top:30%;display:flex;flex-direction:column;align-items:center;gap:5px;text-align:center;pointer-events:none;transition:opacity .5s;z-index:2}
.phint b{font-size:34px;color:#e30613} .phint span{font-size:19px;color:#222} .phint small{margin-top:10px;font-size:14px;letter-spacing:.08em;color:#888}
.play.go .phint{opacity:0}
.pkey{display:flex;align-items:center;gap:6px;margin-top:14px;font-size:17px;color:#222}
.pf{position:absolute;left:0;top:0;display:block;pointer-events:none}
.pf.f1{width:10px;height:10px;margin:-5px 0 0 -5px;border-radius:50%;background:#e30613}
.pf.f2{width:15px;height:15px;margin:-7.5px 0 0 -7.5px;border-radius:50%;border:3px solid #e30613;box-sizing:border-box}
.pf.f5{width:15px;height:15px;margin:-7.5px 0 0 -7.5px;background:#2f8cff;transform:rotate(45deg)}
.pf.f10{width:24px;height:24px;margin:-12px 0 0 -12px;background:#ffd400;clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);filter:drop-shadow(0 0 .5px #3a3c37)}
.pkey .pf.pf{position:relative;left:auto;top:auto;display:inline-block;flex:none;margin:0 1px 0 16px} .pkey .pf.pf:first-child{margin-left:0} .pkey .pf.f5{transform:rotate(45deg) scale(.85)}
.pbug{position:absolute;left:0;top:0;width:46px;height:101px;margin:-50px 0 0 -23px;pointer-events:none;will-change:transform}
.pplus{position:absolute;left:0;top:0;font-weight:700;font-size:20px;color:#e30613;pointer-events:none;z-index:3}
.pdd{position:absolute;left:0;top:0;width:40px;height:40px;margin:-20px 0 0 -20px;pointer-events:none}
.pmsg{position:absolute;left:0;right:0;top:44%;text-align:center;font-size:34px;font-weight:700;color:#e30613;pointer-events:none;z-index:3}
.pend{position:absolute;left:0;right:0;bottom:22px;display:flex;flex-direction:column;align-items:center;gap:2px;pointer-events:none;z-index:2}
.pend img{width:32px;height:32px} .pend span{font-size:21px;color:#e30613} .pend b{font-weight:700}
"""

GAME_JS = r"""<script>(function(){ const gd=document.getElementById('game'), pl=document.getElementById('play'), go=document.getElementById('pgo'); if(!gd||!pl||!go) return;
  const dot=pl.querySelector('.pdot'), bug=pl.querySelector('.pbug'), cv=pl.querySelector('.ptrail'), tc=cv.getContext('2d'), R2=(a,b)=>a+Math.random()*(b-a);
  const sy=document.getElementById('sy'), sb=document.getElementById('sb');
  const KINDS=[[1,'f1',.5],[2,'f2',.28],[5,'f5',.15],[10,'f10',.07]], GOAL=100;
  let W=0,H=0,N=10, d={x:0,y:0}, g={x:30,y:200,a:0}, run=false, last=0, walked=0, food=[], you=0, them=0, over=false, playing=false;
  const size=()=>{ W=pl.clientWidth; H=pl.clientHeight; N=Math.max(8,Math.min(16,Math.round(W*H/90000))); const r=devicePixelRatio||1; cv.width=Math.round(W*r); cv.height=Math.round(H*r); tc.setTransform(r,0,0,r,0,0); tc.fillStyle='rgba(58,60,55,.55)'; };
  const DD='<svg class="pdd" viewBox="-20 -20 40 40"><circle r="19" fill="#e30613"/><circle r="15.5" fill="none" stroke="#fff" stroke-width="1" stroke-dasharray="1 2.2"/>'
    +'<text y="1" fill="#fff" font-family="Calibri,Carlito,sans-serif" font-weight="700" font-size="17" text-anchor="middle" dominant-baseline="central">dd</text></svg>';
  function fly(e,x,y){ e.animate([{transform:`translate(${x}px,${y}px) scale(.3)`,opacity:1},{transform:`translate(${x}px,${y-28}px) scale(1.1)`,opacity:1,offset:.35},
      {transform:`translate(${x}px,${y-70}px) scale(.9)`,opacity:0}],{duration:1100,easing:'cubic-bezier(.2,.8,.3,1)'}).finished.then(()=>e.remove()).catch(()=>e.remove()); }
  function pop(x,y,v,byYou){ let e; if(byYou){ e=document.createElement('b'); e.className='pplus'; e.textContent='+'+v; } else { const w=document.createElement('div'); w.innerHTML=DD; e=w.firstChild; } pl.appendChild(e); fly(e,x,y); }
  function addFood(){ if(!W||!gd.open) return; let r=Math.random(), k=KINDS[0]; for(const q of KINDS){ if(r<q[2]){ k=q; break; } r-=q[2]; }
    const el=document.createElement('i'); el.className='pf '+k[1]; const f={x:R2(40,W-40),y:R2(110,H-120),v:k[0],el}; el.style.left=f.x+'px'; el.style.top=f.y+'px'; pl.appendChild(el); food.push(f); }
  function reset(){ you=them=0; sy.textContent=sb.textContent='0'; tc.clearRect(0,0,W,H); food.forEach(x=>x.el.remove()); food=[]; for(let i=0;i<N;i++) addFood();
    playing=false; over=false; pl.classList.remove('go'); d={x:W*.5,y:H*.72}; g={x:W*.2,y:H*.35,a:0}; }
  function eat(f,byYou){ food=food.filter(x=>x!==f); f.el.remove(); pop(f.x,f.y,f.v,byYou);
    if(byYou){ you+=f.v; sy.textContent=you; } else { them+=f.v; sb.textContent=them; }
    if(you>=GOAL||them>=GOAL){ over=true; const m=document.createElement('p'); m.className='pmsg'; m.textContent=you>=GOAL?'you win!':'the beetle wins!'; pl.appendChild(m);
      setTimeout(()=>{ m.remove(); reset(); },2800); }
    else setTimeout(addFood,R2(250,900)); }
  function step(t){ if(!run) return; const dt=Math.min(.05,(t-last)/1000||0); last=t;
    if(!over){ let tgt=null, best=1e9;
      if(playing){ food.slice().forEach(f=>{ if(Math.hypot(f.x-d.x,f.y-d.y)<20) eat(f,true); });
        let bs=-1; food.forEach(f=>{ const q=Math.hypot(f.x-g.x,f.y-g.y), sc=Math.sqrt(f.v)/(q+40); if(sc>bs){ bs=sc; best=q; tgt=f; } });
      } else { tgt={x:W/2+Math.cos(t/1300)*W*.3, y:H*.55+Math.sin(t/1300)*H*.2}; }
      if(tgt){ const dx=tgt.x-g.x, dy=tgt.y-g.y; const want=Math.atan2(dy,dx)*180/Math.PI+90+Math.sin(t/260)*20; let da=((want-g.a+540)%360)-180;
        g.a+=Math.max(-280*dt,Math.min(280*dt,da)); const sp=(playing?Math.max(150,W*.13):90)*dt, h=(g.a-90)*Math.PI/180;
        g.x=Math.max(10,Math.min(W-10,g.x+Math.cos(h)*sp)); g.y=Math.max(10,Math.min(H-10,g.y+Math.sin(h)*sp));
        walked+=sp; if(walked>3.4){ walked=0; tc.fillRect(g.x-.7,g.y-.7,1.4,1.4); }
        if(playing&&best<24) eat(tgt,false); } }
    dot.style.transform=`translate(${d.x}px,${d.y}px)`; bug.style.transform=`translate(${g.x}px,${g.y}px) rotate(${g.a}deg)`;
    requestAnimationFrame(step); }
  const at=e=>{ const r=pl.getBoundingClientRect(); d.x=Math.max(8,Math.min(W-8,e.clientX-r.left)); d.y=Math.max(8,Math.min(H-8,e.clientY-r.top)); };
  dot.addEventListener('pointerdown',e=>{ e.preventDefault(); at(e); if(!playing&&!over){ playing=true; pl.classList.add('go'); } });
  pl.addEventListener('pointermove',e=>{ if(playing) at(e); });
  go.addEventListener('click',()=>{ gd.showModal(); requestAnimationFrame(()=>{ size(); reset(); run=true; last=performance.now(); requestAnimationFrame(step); }); });
  document.getElementById('gx').addEventListener('click',()=>gd.close());
  gd.addEventListener('close',()=>{ run=false; });
  gd.addEventListener('wheel',e=>{ e.preventDefault(); e.stopPropagation(); },{passive:false});
  gd.addEventListener('keydown',e=>{ if(e.key!=='Escape') e.stopPropagation(); });
  addEventListener('resize',()=>{ if(gd.open) size(); });
})();</script>"""


def _game(s):
    i = s.index('<section class="pg" id="impressum"><div class="bg-white relative frame">') + len('<section class="pg" id="impressum"><div class="bg-white relative frame">')
    trig = ('<button type="button" class="pgo" id="pgo" style="left:1000px;top:930px" aria-label="play the beetle game">'
            '<span class="pme">press me</span><i class="pld"></i><i class="pdot"><b></b></i></button>')
    s = s[:i] + trig + s[i:]
    dlg = ('<dialog class="game" id="game" aria-label="beetle game"><div class="play" id="play"><canvas class="ptrail"></canvas>'
           f'<button type="button" class="gx" id="gx" aria-label="close the game (Esc)" title="close (Esc)">{XC}</button>'
           '<div class="pscore"><span>you <b id="sy">0</b></span><span>beetle <b id="sb">0</b></span></div>'
           '<div class="phint"><b>collect the dots!</b><span>whoever gets to 100 first wins</span>'
           '<span class="pkey"><i class="pf f1"></i> 1 <i class="pf f2"></i> 2 <i class="pf f5"></i> 5 <i class="pf f10"></i> 10</span>'
           '<small>click the yellow dot to start – then it follows your mouse</small></div>'
           '<i class="pdot"><b></b></i><img class="pbug" src="img/m-bug-up.webp" alt="">'
           '<div class="pend"><img src="img/m-mark.png" alt=""><span>dasein<b>-design</b></span></div></div></dialog>')
    return s.replace('</body>', dlg + GAME_JS + '</body>', 1)


# ---------- 23 Oct, 02:10 - the desktop catches up with the phone: bits & bats leaves (its photos live in "wonder"), contact becomes [04],
# the fifth tab slot holds the "work ○ wonder" switch, no game, no social marks, no closing contact line
def _wonder_tiles():
    import datetime, html as H
    from texts import WCATS, WCAT_OF
    items = [(im, c, WCAT_OF.get(k, 0)) for k, (im, t, c) in enumerate(BITS)][::-1]   # newest first
    t, steps = datetime.datetime(2026, 10, 22, 19, 40), [3.2, 5.1, 16.4, 4.3, 2.7, 15.9, 6.2, 18.1, 3.6, 4.8, 14.7]
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    out = []
    for n, (im, c, cat) in enumerate(items):
        when = f'{days[t.weekday()]} {t.day} {t.strftime("%b")} · {t.strftime("%H:%M")}'
        line = H.unescape(c).replace('dd - ', '').strip().capitalize().rstrip('.!?') + '.'
        from PIL import Image as _I
        with _I.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img', im)) as I: ar = round(I.width / I.height, 3)
        out.append(f'<button type="button" class="dwg" data-cat="{cat}" data-ar="{ar}" data-when="{when}" data-line="{H.escape(line)}" data-img="img/{im}">'
                   f'<img src="img/{im}" alt="" loading="lazy"></button>')
        t -= datetime.timedelta(hours=steps[n % len(steps)])
    return ''.join(out), WCATS


WONDER_CSS = """
/* work ○ wonder on the desktop (23 Oct) */
.dwsw{position:absolute;left:1115px;top:0;width:200px;height:25px;z-index:46;display:flex;align-items:center;justify-content:center;gap:7px;border:.5px dashed #fff;background:rgba(0,0,0,.05);
  font-family:Calibri,Carlito,sans-serif;font-size:15px;color:#666;cursor:pointer;padding:0}
.dwsw .wk{color:#000;font-weight:700} .dwsw[aria-pressed=true] .wk{color:#666;font-weight:400} .dwsw[aria-pressed=true] .wo{color:#e30613;font-weight:700}
.dwsw .tg{position:relative;width:30px;height:15px;border-radius:8px;border:1px solid #3a3c37;background:#fff;transition:background .25s}
.dwsw .tg b{position:absolute;left:2px;top:2px;width:9px;height:9px;border-radius:50%;background:#cdff3e;box-shadow:0 0 0 1px #3a3c37;transition:transform .25s}
.dwsw .tg b::after{content:"";position:absolute;inset:-1px;border-radius:50%;border:1px solid #e30613;opacity:0;animation:dwp 3.2s ease-out infinite}
@keyframes dwp{0%{transform:scale(1);opacity:.8}100%{transform:scale(4);opacity:0}}
.dwsw[aria-pressed=true] .tg{background:#eaffae} .dwsw[aria-pressed=true] .tg b{transform:translateX(15px);background:#e30613} .dwsw[aria-pressed=true] .tg b::after{animation:none}
.dwsw:hover .wo{color:#e30613}
.dwon{position:absolute;left:225px;top:30px;width:1100px;height:966px;z-index:45;background:#fff}   /* ends above the scroll arrow (y 998), which stays, as on every page */   /* above the map (20) and the guide lines */
.dwon[hidden]{display:none}
.dwtrail{position:absolute;left:0;top:0;width:1100px;height:216px;z-index:2;pointer-events:none}
.dwbug{position:absolute;left:0;top:0;width:29px;height:65px;margin:-32px 0 0 -15px;z-index:2;pointer-events:none;will-change:transform;
}   /* no outline: it walks on white */
[data-node-id="1:600"]{width:150px!important}   /* Steuart's portrait square (three photos and one empty) in place of his card, as tall as Cuong's card (23 Oct) */
.dwopen #ihint{display:none!important}   /* no start-page hint over wonder (23 Oct) */
.dwopen #mapclip{visibility:hidden}   /* the live map sits above the page: hidden while wonder is open (the dashed columns stay) */
.dwsc{position:absolute;inset:0;overflow-y:auto;overscroll-behavior:contain;touch-action:pan-y;scrollbar-width:none;padding:30px 10px 30px} .dwsc::-webkit-scrollbar{display:none}
.dwgrid{position:relative;width:1080px}   /* each column of the projects grid split in two (95 + 10 + 95), rows of 85 + 10 */   /* the projects page's module: columns on the dashed lines, rows of 180 from y 60 */
.dwg{position:absolute;padding:0;border:0;background:#f4f4f4;overflow:hidden;cursor:pointer}
.dwg img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s} .dwg:hover img{transform:scale(1.04)}
.dwempty{position:absolute}
.dwtitle{position:absolute;left:0;top:0;width:1440px;height:1024px;z-index:45;pointer-events:none}
.dwtitle .dwtw{position:absolute;left:110px;top:380px;width:112px;height:644px;background:#fff}
.dwtitle [class*="h-[560px]"][class*="w-[84px]"]{height:570px!important} .dwtitle [class*="w-[560px]"]{width:570px!important}
.dwtitle [class*="w-[560px]"] > p{display:flex;align-items:baseline;white-space:pre;margin:0}
.dwtitle [class*="w-[560px]"] > p > span[class*="text-[20px]"]{font-size:40px!important;margin-left:auto;color:#e30613}   /* [w] like the pages' [01]-[04] */
.dwtitle[hidden]{display:none}
.dwfloat{position:absolute;left:10px;top:220px;width:1080px;height:22px;z-index:2}   /* ten categories, two to each column, in a row under the tabs, level with the dd mark */
.dwsc{top:246px!important;padding-top:6px!important}   /* the category row sits on the tick at y 250 (by the i of dasein), the photos start 10 px under it */
.dwfb{position:absolute;top:0;width:95px;height:22px;display:flex;align-items:center;justify-content:center;gap:4px;padding:0 4px;border:0;font:13px Calibri,Carlito,sans-serif;color:#000;white-space:nowrap;overflow:hidden;cursor:pointer}
.dwfb b{font-weight:700} .dwfb small{font-size:9px;opacity:.7} .dwfb:hover{filter:brightness(1.08)}
.dwfb:nth-child(1){background:#d4f06a} .dwfb:nth-child(2){background:#f2cf3a} .dwfb:nth-child(3){background:#4a8fe0;color:#fff} .dwfb:nth-child(4){background:#f2bccf}
.dwfb:nth-child(5){background:#d03a3a;color:#fff} .dwfb:nth-child(6){background:#45ad5c;color:#fff} .dwfb:nth-child(7){background:#ee9233} .dwfb:nth-child(8){background:#9a7ee6;color:#fff} .dwfb:nth-child(9){background:#26a69c;color:#fff} .dwfb:nth-child(10){background:#2e3a72;color:#fff}
.dwfb.on{box-shadow:inset 0 0 0 2px #111}
.dwfb.on small{display:none} .dwfb.on::after{content:"× all";margin-left:4px;font-size:11px;font-weight:700;opacity:.85}   /* the chosen category offers the way back to all photos */
.dwpop{position:absolute;inset:0;z-index:3;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.62);backdrop-filter:blur(1.5px)}
.dwpop[hidden]{display:none}
.dwcard{width:560px;background:#fff;box-shadow:0 2px 18px rgba(0,0,0,.18);border:1px dotted #b8b8b8;font-family:Calibri,Carlito,sans-serif}
.dwtop{display:flex;justify-content:space-between;align-items:center;padding:10px 14px 6px;font-size:13px;color:#666;letter-spacing:.06em} .dwtop b{color:#e30613;font-weight:400}
.dwx{border:0;background:none;padding:2px;cursor:pointer} .dwx svg{width:24px;height:24px} .dwx .rg{fill:none;stroke:#3a3c37;stroke-width:.6} .dwx .xx{fill:none;stroke:#1a1a1a;stroke-width:1.15;stroke-linecap:round} .dwx:hover .rg,.dwx:focus-visible .rg{stroke:#e30613} .dwx .xx{transition:stroke .2s} .dwx:hover .xx,.dwx:focus-visible .xx{stroke:#e30613}
.dwx:hover svg,.dwx:focus-visible svg{animation:lbxp 1.4s ease-in-out infinite} .dwx:focus-visible{outline:none}   /* the close pulses on hover, like the project pop-up's (23 Oct) */
@media (prefers-reduced-motion:reduce){.dwx:hover svg,.dwx:focus-visible svg{animation:none}}
.dwbody{padding:0 14px 8px} .dwbody img{display:block;width:100%;aspect-ratio:1/1;object-fit:contain;background:#f6f6f6;outline:1px dotted #b8b8b8;outline-offset:-1px}
.dwbody img{cursor:none}   /* the floating W / E arrow takes over (23 Oct) */
.dwbody .d{margin:10px 0 2px;font-size:13px;letter-spacing:.06em;color:#888} .dwbody .l{margin:0 0 4px;font-size:18px;color:#222}
.dwnav{display:flex;justify-content:space-between;padding:8px 12px 10px;border-top:1px dashed #c4c4c4}
.dwnav button{display:flex;align-items:center;gap:7px;border:0;background:none;font:14px Calibri,Carlito,sans-serif;cursor:pointer;padding:3px} .dwnav button:hover{color:#e30613}
"""

WONDER_JS = r"""<script>(function(){ const sw=document.getElementById('dwsw'), wo=document.getElementById('dwon'), ti=document.getElementById('dwtitle'); if(!sw||!wo) return;
  const sc=wo.querySelector('.dwsc'), grid=document.getElementById('dwgrid'), tiles=[...grid.querySelectorAll('.dwg')], pop=document.getElementById('dwpop'), body=document.getElementById('dwbody');
  const CATS=JSON.parse(wo.dataset.cats); let only=null, cur=0;
  const set=on=>{ document.documentElement.classList.toggle('dwopen',on); sw.setAttribute('aria-pressed',String(on)); wo.hidden=!on; ti.hidden=!on; if(!on) pop.hidden=true; else { carpet(); sc.scrollTop=0; requestAnimationFrame(nxl); } };
  sw.addEventListener('click',()=>set(sw.getAttribute('aria-pressed')!=='true'));
  document.querySelectorAll('.hot.tab,.hot.pin').forEach(a=>a.addEventListener('click',()=>set(false)));
  addEventListener('wheel',e=>{ if(wo.hidden||!pop.hidden&&false) return; if(!e.target.closest||!e.target.closest('#dwon')) return; e.stopImmediatePropagation(); e.preventDefault(); sc.scrollTop+=e.deltaY; },{passive:false,capture:true});
  /* the scroll arrow at the foot works on wonder too: a screen further down, at the end "top" */
  const nx=document.getElementById('nextp');
  const nxl=()=>{ if(!nx||wo.hidden) return; const end=sc.scrollTop+sc.clientHeight>=sc.scrollHeight-4; nx.classList.toggle('up',end); nx.classList.remove('hint'); nx.style.width='90px'; nx.lastChild.textContent=end?'top':'scroll'; };
  sc.addEventListener('scroll',nxl,{passive:true});
  if(nx) addEventListener('click',e=>{ if(wo.hidden||!e.target.closest||!e.target.closest('#nextp')) return; e.preventDefault(); e.stopImmediatePropagation();
    const end=sc.scrollTop+sc.clientHeight>=sc.scrollHeight-4; sc.scrollTo({top:end?0:sc.scrollTop+sc.clientHeight-95,behavior:'smooth'}); },true);
  addEventListener('keydown',e=>{ if(wo.hidden) return; if(e.key==='Escape'){ if(!pop.hidden) pop.hidden=true; else set(false); e.stopImmediatePropagation(); }
    else if(!pop.hidden&&(e.key==='ArrowLeft'||e.key==='ArrowRight')){ step(e.key==='ArrowLeft'?-1:1); e.stopImmediatePropagation(); } else e.stopImmediatePropagation(); },true);
  function lay(items,W){ const out=[]; let y=0, row=[];
    const worst=(r,h)=>Math.max(...r.map(o=>{ const w=o.a/h; return Math.max(w/h,h/w); }));
    const flush=()=>{ const sa=row.reduce((a,o)=>a+o.a,0), h=sa/W; let x=0; row.forEach(o=>{ const w=o.a/h; out.push({...o,x,y,w,h}); x+=w; }); y+=h; row=[]; };
    items.forEach(o=>{ if(!row.length){ row.push(o); return; } const h0=row.reduce((a,q)=>a+q.a,0)/W, r1=row.concat(o), h1=r1.reduce((a,q)=>a+q.a,0)/W;
      if(worst(r1,h1)<=worst(row,h0)) row.push(o); else { flush(); row.push(o); } }); if(row.length) flush(); return {out,h:y}; }
  function sq(items,x,y,w,h,out){ items=items.slice(); const tot=items.reduce((a,b)=>a+b.a,0), f=w*h/tot; items.forEach(o=>o.s=o.a*f);
    const worst=(r,len)=>{ const s=r.reduce((a,b)=>a+b.s,0); return Math.max(...r.map(o=>Math.max(len*len*o.s/(s*s), s*s/(len*len*o.s)))); };
    while(items.length){ const len=Math.min(w,h); let row=[items.shift()];
      while(items.length&&worst(row.concat(items[0]),len)<=worst(row,len)) row.push(items.shift());
      const s=row.reduce((a,b)=>a+b.s,0);
      if(w>=h){ const cw=s/h; let yy=y; row.forEach(o=>{ const ch=o.s/cw; out.push({...o,x,y:yy,w:cw,h:ch}); yy+=ch; }); x+=cw; w-=cw; }
      else { const rh=s/w; let xx=x; row.forEach(o=>{ const rw=o.s/rh; out.push({...o,x:xx,y,w:rw,h:rh}); xx+=rw; }); y+=rh; h-=rh; } } }
  /* the carpet: a treemap of many sizes, newest first, in runs that form blocks, the blocks laid row by row; a few white rests */
  /* the carpet (02:30): ten half-columns - two in each column of the site, 10 px apart, 20 px between columns - and rows of 85 + 10, so two rows
     make one row of the projects page; photos take 1 x 1, 2 x 1 (a whole column), 1 x 2, 2 x 2 or now and then 4 x 4, packed in order */
  function carpet(){ const ph=tiles.filter(t=>only===null||t.dataset.cat===only);
    tiles.forEach(t=>t.hidden=true); grid.querySelectorAll('.dwempty,.again').forEach(e=>e.remove());
    const COLS=5, CW=200, CG=20, G=7, RATIO=.9, EMPTY='dwempty';
    /* (08:10) each column of the page split in THREE, rows to match: mostly small pieces - squares, upright and wide rectangles - with the odd bigger one;
       a piece never straddles the gap between two columns unless it fills whole columns */
    const K=3, NC=COLS*K, SW=(CW-2*G)/K, PITCH=SW*RATIO+G;
    const X=c=>Math.floor(c/K)*(CW+CG)+(c%K)*(SW+G), WD=(c,w)=>w%K===0?(w/K)*CW+(w/K-1)*CG:w*SW+(w-1)*G, HT=h=>h*PITCH-G;
    const ok=(c,w)=>c+w<=NC&&(Math.floor(c/K)===Math.floor((c+w-1)/K)||(w%K===0&&c%K===0));
    const SZ=[[1,1],[2,1],[1,1],[1,2],[1,1],[2,2],[1,1],[2,1],[1,1],[1,1],[1,2],[3,2],[1,1],[2,1],[1,1],[1,1],[2,2],[1,2],[1,1],[2,1],[1,1],[3,3],[1,1],[1,2],[2,1]];
    const occ=[], free=(c,r,w,h)=>{ for(let y=r;y<r+h;y++) for(let x=c;x<c+w;x++){ if(occ[y]&&occ[y][x]) return false; } return true; };
    const take=(c,r,w,h)=>{ for(let y=r;y<r+h;y++){ occ[y]=occ[y]||[]; for(let x=c;x<c+w;x++) occ[y][x]=1; } };
    let bottom=0;
    const place=(e,w,h)=>{ if(w>NC) w=NC; for(let r=0;;r++) for(let c=0;c<NC;c++){ if(!ok(c,w)||!free(c,r,w,h)) continue; take(c,r,w,h);
      e.style.cssText=''; Object.assign(e.style,{position:'absolute',left:X(c)+'px',top:(r*PITCH)+'px',width:WD(c,w)+'px',height:HT(h)+'px'}); grid.appendChild(e); bottom=Math.max(bottom,r+h); return; } };
    let n=0;
    ph.forEach((t,k)=>{ if(k%5===3){ const e=document.createElement('i'); e.className=EMPTY; place(e,1,1); }
      let [w,h]=SZ[n%SZ.length]; n++; t.hidden=false; place(t,w,h); });
    /* fill the screen: with all categories on, the photos come round again (repeats open the same post) until the carpet is well over a screen deep */
    if(only===null&&ph.length) for(let k=0; k<ph.length*3 && bottom*PITCH<sc.clientHeight*1.6; k++){ const t=ph[(k*7+3)%ph.length], e=t.cloneNode(true); e.classList.add('again'); e.hidden=false;
      e.addEventListener('click',()=>show(t)); if(k%5===3){ const x=document.createElement('i'); x.className=EMPTY; place(x,1,1); } let [w,h]=SZ[n%SZ.length]; n++; place(e,w,h); }
    grid.style.height=(bottom*PITCH)+'px'; }
  /* the beetle wanders over wonder in curves, quick but not frantic, leaving a dotted trail that slowly fades; it stays put while the photos scroll */
  /* (02:58) only in the white band between the tabs and the category row, slowly, in spaghetti loops from left to right and back */
  (function(){ const bug=document.getElementById('dwbug'), cv=document.getElementById('dwtrail'), tc=cv.getContext('2d'); const W=1100, H=216;
    cv.width=W*2; cv.height=H*2; tc.setTransform(2,0,0,2,0,0);
    let g={x:60,y:108,a:90}, tgt={x:600,y:500}, last=0, walked=0, fade=0, run=0;
    let dir=1; const R=(a,b)=>a+Math.random()*(b-a), pick=()=>{ let x=g.x+dir*R(70,160); if(x>W-50){ x=W-50; dir=-1; } if(x<50){ x=50; dir=1; } tgt={x,y:R(55,H-55)}; };
    function step(t){ if(wo.hidden){ run=0; return; } const dt=Math.min(.05,(t-last)/1000||0); last=t;
      const dx=tgt.x-g.x, dy=tgt.y-g.y; if(Math.hypot(dx,dy)<40) pick();
      const want=Math.atan2(dy,dx)*180/Math.PI+90+Math.sin(t/420)*55; let da=((want-g.a+540)%360)-180;
      g.a+=Math.max(-140*dt,Math.min(140*dt,da)); const sp=70*dt, h=(g.a-90)*Math.PI/180;
      g.x=Math.max(30,Math.min(W-30,g.x+Math.cos(h)*sp)); g.y=Math.max(40,Math.min(H-40,g.y+Math.sin(h)*sp));
      walked+=sp; if(walked>4){ walked=0; tc.fillStyle='rgba(58,60,55,.6)'; tc.beginPath(); tc.arc(g.x,g.y,1,0,7); tc.fill(); }
      fade+=dt; if(fade>.12){ fade=0; tc.globalCompositeOperation='destination-out'; tc.fillStyle='rgba(0,0,0,.025)'; tc.fillRect(0,0,W,H); tc.globalCompositeOperation='source-over'; }
      bug.style.transform=`translate(${g.x}px,${g.y}px) rotate(${g.a}deg)`; run=requestAnimationFrame(step); }
    sw.addEventListener('click',()=>{ if(!wo.hidden&&!run){ tc.clearRect(0,0,W,H); pick(); last=performance.now(); run=requestAnimationFrame(step); } });
  })();
  /* the categories: a row of half-column labels */
  const fl=wo.querySelector('.dwfloat');
  const fb=CATS.map((c,k)=>{ const b=document.createElement('button'); b.type='button'; b.className='dwfb'; b.innerHTML='<b>'+c+'</b><small>['+String(k+1).padStart(2,'0')+']</small>';
    b.addEventListener('click',()=>{ only=only===String(k)?null:String(k); fb.forEach((x,j)=>x.el.classList.toggle('on',only===String(j))); carpet(); sc.scrollTop=0; });
    b.style.left=(Math.floor(k/2)*220+(k%2)*105)+'px'; fl.appendChild(b); return {el:b,x:Math.random(),y:Math.random(),vx:(Math.random()-.5)*.02,vy:(Math.random()-.5)*.02}; });
  let fla=0, flt=0;
  function drift(t){ if(wo.hidden){ fla=0; return; } const dt=Math.min(.05,(t-flt)/1000||0); flt=t; const FW=fl.clientWidth, FH=fl.clientHeight;
    if(pop.hidden) fb.forEach(o=>{ o.vx+=(Math.random()-.5)*.004*dt*60; o.vy+=(Math.random()-.5)*.004*dt*60; const sp=Math.hypot(o.vx,o.vy), mx=.03;
      if(sp>mx){ o.vx*=mx/sp; o.vy*=mx/sp; } o.x+=o.vx*dt; o.y+=o.vy*dt;
      if(o.x<0||o.x>1){ o.vx*=-1; o.x=Math.max(0,Math.min(1,o.x)); } if(o.y<0||o.y>1){ o.vy*=-1; o.y=Math.max(0,Math.min(1,o.y)); }
      o.el.style.transform=`translate(${o.x*(FW-o.el.offsetWidth)}px,${o.y*(FH-o.el.offsetHeight)}px)`; });
    fla=requestAnimationFrame(drift); }
  /* the pop-up: a square card, the photo whole, date and one sentence; previous / next; a click beside it goes back */
  const vis=()=>tiles.filter(t=>!t.hidden);
  function show(t){ const v=vis(); cur=v.indexOf(t); const d=t.dataset;
    body.innerHTML='<img src="'+d.img+'" alt=""><p class="d">'+d.when+'</p><p class="l">'+d.line+'</p>';
    document.getElementById('dwk').innerHTML='wonder <b>'+String(cur+1).padStart(2,'0')+'</b> / '+v.length; pop.hidden=false; }
  const step=k=>{ const v=vis(); show(v[(cur+k+v.length)%v.length]); };
  tiles.forEach(t=>t.addEventListener('click',()=>show(t)));
  /* with a category chosen, a click anywhere outside the photos and labels brings all photos back */
  wo.addEventListener('click',e=>{ if(only===null||!pop.hidden) return; if(e.target.closest('.dwg,.dwfb,.dwpop,a,button')) return;
    only=null; wo.querySelectorAll('.dwfb').forEach(x=>x.classList.remove('on')); carpet(); });
  document.getElementById('dwprev').onclick=()=>step(-1); document.getElementById('dwnext').onclick=()=>step(1);
  document.getElementById('dwx').onclick=()=>{ pop.hidden=true; }; pop.addEventListener('click',e=>{ if(e.target===pop) pop.hidden=true; });
  /* over the photo: the floating W / E arrow of the project pop-up; a click on the left half goes back, on the right half on (23 Oct) */
  const ar=document.createElement('div'); ar.className='pcar'; ar.setAttribute('aria-hidden','true'); ar.innerHTML=__DWAR__; document.body.appendChild(ar);
  const half=(e,im)=>{ const r=im.getBoundingClientRect(); return e.clientX<r.left+r.width/2?'l':'r'; };
  body.addEventListener('mousemove',e=>{ const im=e.target.closest('img'); if(!im){ ar.className='pcar'; return; }
    ar.style.transform=`translate(${e.clientX}px,${e.clientY}px)`; ar.className='pcar on '+half(e,im); });
  body.addEventListener('mouseleave',()=>ar.className='pcar');
  body.addEventListener('click',e=>{ const im=e.target.closest('img'); if(!im) return; step(half(e,im)==='l'?-1:1);
    requestAnimationFrame(()=>{ ar.className='pcar on '+half(e,body.querySelector('img')); }); });
  new MutationObserver(()=>{ if(pop.hidden) ar.className='pcar'; }).observe(pop,{attributes:true,attributeFilter:['hidden']});
  /* a swipe on a touch screen steps too (23 Oct) */
  let sx=null, sy=0;
  body.addEventListener('touchstart',e=>{ const t=e.touches[0]; sx=t.clientX; sy=t.clientY; },{passive:true});
  body.addEventListener('touchend',e=>{ if(sx===null) return; const t=e.changedTouches[0], dx=t.clientX-sx, dy=t.clientY-sy; sx=null;
    if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy)*1.3){ e.preventDefault(); step(dx<0?1:-1); } });
})();</script>"""


def _tab_pat(label):
    """a top tab: its dashed box and its words (with or without a wrapper), found by its label"""
    return (r'<div class="absolute bg-[^"]*h-\[25px\] left-\[\d+px\] top-0 w-\[200px\]"[^>]*></div>'
            r'<div class="[^"]*"[^>]*><p[^>]*>(?:(?!</p>).)*?' + re.escape(label) + r'(?:(?!</p>).)*</p></div>')


def _drop_group(s, label):
    return re.subn(_tab_pat(label), '', s, flags=re.S)


def _desk_catchup(s):
    # bits & bats: page, its chrome, its tab (in every chrome), its hot tab, its beetle circle
    i = s.index('<section class="pg" id="bits">'); j = s.index('<section', i + 10)
    s = s[:i] + s[j:]
    i = s.index('<div class="chrome" data-pg="bits">'); s = s[:i] + s[_closing_div(s, i):]
    s, n = _drop_group(s, 'bits &amp; bats </span>'); assert n >= 4, n
    s, n2 = _drop_group(s, '>bits</span>')   # the contact page's tab spells it in three spans
    s = re.sub(r'<a class="hot tab" href="#bits"[^>]*></a>', '', s)
    s = re.sub(r'<a class="hot pin" href="#bits".*?</a>', '', s, count=1, flags=re.S)
    # contact moves into the fourth slot and becomes [04]
    def mv(m):
        g = m.group(0)
        return g.replace('left-[1115px]', 'left-[895px]').replace('left-[1215px]', 'left-[995px]').replace('[05]', '[04]')
    s, n = re.subn(_tab_pat('contact </span>'), mv, s, flags=re.S)
    s = s.replace('<div class="absolute contents left-[1115px] top-0"', '<div class="absolute contents left-[895px] top-0"')
    assert n >= 4, n
    s = s.replace('<a class="hot tab" href="#contact" style="left:1115px;', '<a class="hot tab" href="#contact" style="left:895px;')
    s = s.replace('contact </span><span class="fcal-r leading-[normal] text-[20px]">[05]</span>', 'contact </span><span class="fcal-r leading-[normal] text-[20px]">[04]</span>')
    s = re.sub(r'(<a class="hot pin" href="#contact" style="[^"]*?)--k:4;([^"]*">)05', r'\1--k:3;\g<2>04', s)
    s = re.sub(r'(<a class="hot pin" href="#impressum" style="[^"]*?)--k:5;([^"]*">)i<', r'\1--k:4;\2§<', s)
    # no social marks, no closing contact line
    s = re.sub(r'<div class="absolute left-\[1335px\] size-\[25px\] top-\[\d+px\]" data-node-id="[^"]+" data-name="(?:Twitter Squared|Facebook|Instagram)"><img[^>]*></div>', '', s)
    s = re.sub(r'<a class="hot social"[^>]*>(?:</a>)?', '', s)
    s = re.sub(r'<div class="ptx end"[^>]*>(?:(?!</div>).)*Write, call(?:(?!</div>).)*</div>', '', s, flags=re.S)
    # the switch in the fifth slot, and wonder itself over the five columns
    tiles, cats = _wonder_tiles()
    W, E = compass('W', 22), compass('E', 22)
    sw = ('<button type="button" class="dwsw" id="dwsw" aria-pressed="false" aria-label="switch between work and wonder">'
          '<span class="wk">work</span><i class="tg"><b></b></i><span class="wo">wonder</span></button>')
    # the vertical title in exactly the markup and position of the other pages' titles, over the same grey text strip (23 Oct, 02:50)
    title = ('<i class="dwtw"></i>'
             '<div class="absolute flex h-[570px] items-center justify-center left-[125px] top-[430px] w-[90px]"><div class="flex-none"><div class="border-[0.5px] border-solid border-white h-[570px] relative w-[90px]">'
             '<img alt="" class="absolute inset-0 max-w-none object-contain pointer-events-none size-full" src="img/intro-imgImage.webp"></div></div></div>'
             '<div class="-translate-y-full absolute flex h-[560px] items-center justify-center left-[125px] top-[1000px] w-[84px]"><div class="-rotate-90 flex-none">'
             '<div class="[word-break:break-word] flex flex-col finter font-semibold h-[84px] justify-end leading-[0] not-italic relative text-[0px] text-[rgba(0,0,0,0.8)] w-[560px]">'
             '<p><span class="fcal-b leading-[normal] text-[50px]">wonder </span><span class="fcal-r leading-[normal] text-[20px]">[w]</span></p></div></div></div>')
    wo = (f'<div class="dwtitle" id="dwtitle" hidden>{title}</div>'
          f'<div class="dwon" id="dwon" hidden data-cats=\'{json.dumps(cats)}\'><div class="dwsc"><div class="dwgrid" id="dwgrid">{tiles}</div></div><div class="dwfloat"></div><canvas class="dwtrail" id="dwtrail"></canvas><img class="dwbug" id="dwbug" src="img/m-bug-up.webp" alt="">'
          f'<div class="dwpop" id="dwpop" hidden><div class="dwcard"><div class="dwtop"><span id="dwk"></span><button type="button" class="dwx" id="dwx" aria-label="close">{XC}</button></div>'
          f'<div class="dwbody" id="dwbody"></div><div class="dwnav"><button type="button" id="dwprev">{W}<span>previous</span></button><button type="button" id="dwnext"><span>next</span>{E}</button></div></div></div></div>')
    i = s.index('<a class="hot tab" href="#contact"')
    s = s[:i] + sw + wo + s[i:]
    return s.replace('</body>', WONDER_JS.replace('__DWAR__', json.dumps(compass('W', 28, 'cw') + compass('E', 28, 'ce'))) + '</body>', 1)


def _tint(s):
    """23 Oct, 08:15 - like the phone: a pale grey ground on every other page, starting with about us (about us, downloads & links, impressum),
    inside the five columns (x 235-1315), from under the tabs to above the scroll arrow"""
    for pid in ('services', 'downloads', 'impressum'):
        a = f'<section class="pg" id="{pid}"><div class="bg-white relative frame">'
        assert a in s, pid
        s = s.replace(a, a + '<div class="pgtint" aria-hidden="true"></div>', 1)
    return s


# ---------- contact + impressum on one page (23 Oct, 13:04, Steuart): contact details at the top, the map in the middle,
# the impressum basics under the map and "(+) full impressum" right at the bottom; the impressum page goes
IMP_CSS = """
/* contact + impressum (23 Oct) */
#contact [data-node-id="1:539"],#contact [data-node-id="8:3"],#contact [data-node-id="104:17"],#contact [data-node-id="104:18"]{display:none}
.impb{position:absolute;font:400 11.5px/1.5 Calibri,Carlito,sans-serif;color:#222}
.impb .lab2{margin:0 0 4px;font-weight:700;font-size:11px;letter-spacing:.14em;color:#e30613}
.impb .lp{color:#666;font-size:11px;margin:0}
.impb h4{margin:0 0 2px;font-size:11.5px;font-weight:700;color:#000} .impb p{margin:0} .impb .lp+h4{margin-top:8px}
.impb a,.impfull a{color:#1a5fd0;text-decoration:none} .impb a[href^="tel:"],.impfull a[href^="tel:"]{color:#1e8e3e}
.impfull{z-index:7;display:none;column-count:5;column-gap:20px;font-size:11px;line-height:1.42} .impfull h4{font-size:11px;margin-top:8px} .impfull .lp{font-size:10.5px} .impo .impfull{display:block} .impo .impb{visibility:hidden}
.imptint{position:absolute;left:235px;top:815px;width:1080px;height:178px;background:#f4f4f2;transition:top .45s ease,height .45s ease}   /* the short impressum on a pale grey band from the tick mark above "contact" to the foot, a whole tick clear of the map (23 Oct, 13:31) */
.impo .imptint{top:630px;height:363px}   /* "full impressum" grows the band up to just under the map, with the whole text */
.impo .impfull{animation:impin .35s .15s ease-out both} @keyframes impin{from{opacity:0}to{opacity:1}}
@media (prefers-reduced-motion:reduce){.imptint{transition:none}.impo .impfull{animation:none}}
.dimp{left:235px;top:960px;width:1080px;height:28px;padding:0 0 0 2px;
  background:repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left top/100% 1px no-repeat,
             repeating-linear-gradient(to right,#b8b8b8 0 1px,transparent 1px 3px) left bottom/100% 1px no-repeat}
"""
IMP_JS = """<script>/* contact + impressum (23 Oct): "full impressum" opens the whole text over the map; the § links open it from anywhere */
(function(){
  const fr=document.querySelector('#contact .frame'), b=document.getElementById('dimp'); if(!fr||!b) return;
  let here='', want=false;
  const set=on=>{ fr.classList.toggle('impo',on); document.documentElement.classList.toggle('impopen',on); b.setAttribute('aria-expanded',String(on));
    document.querySelectorAll('a.impl').forEach(a=>a.classList.toggle('cur',on)); };
  b.addEventListener('click',()=>set(!fr.classList.contains('impo')));
  document.addEventListener('pagechange',e=>{ here=e.detail; if(here==='contact'){ if(want){ want=false; set(true); } } else set(false); });
  document.addEventListener('click',e=>{ if(e.target.closest('[data-imp]')){ if(here==='contact') set(true); else want=true; } },true);
  if(window.ddImp) set(true);
})();</script>"""

LBSW_JS = """<script>/* 23 Oct: with the project pop-up open, a click on the work / wonder switch or a tab closes it and does that too */
(function(){ const lb=document.getElementById('lb'); if(!lb) return;
  lb.addEventListener('click',e=>{ if(e.target.closest('#lbp')) return; const x=e.clientX, y=e.clientY;
    requestAnimationFrame(()=>{ if(lb.open) return; const el=document.elementFromPoint(x,y), t=el&&el.closest('#dwsw,.hot.tab'); if(t) t.click(); }); });
})();</script>"""


def _contact_imp(s):
    # the impressum page and its chrome go
    i = s.index('<section class="pg" id="impressum"'); j = s.index('</section>', i) + len('</section>')
    s = s[:i] + s[j:]
    i = s.index('<div class="chrome" data-pg="impressum">'); s = s[:i] + s[_closing_div(s, i):]
    s = _rep('<script>document.addEventListener("pagechange",e=>document.querySelectorAll("a.impl").forEach(a=>a.classList.toggle("cur",e.detail==="impressum")));</script>', '', s)
    # every § link now opens contact with the impressum unfolded; an old #impressum address too
    s = s.replace('<a class="impl" href="#impressum">', '<a class="impl" href="#contact" data-imp="1">')
    s = s.replace('<a class="hot pin" href="#impressum"', '<a class="hot pin" href="#contact" data-imp="1"')
    assert '#impressum"' not in s
    s = s.replace('<head>', '<head><script>if(location.hash==="#impressum"){ history.replaceState(null,"",location.pathname+location.search+"#contact"); window.ddImp=1; }</script>', 1)
    # contact details to the top of the first column, a touch smaller; the map from y 60 to 800
    s = _rep('top-[445px] w-[200px] whitespace-pre-wrap" style="top:440px" data-node-id="1:474"', 'top-[445px] w-[200px] whitespace-pre-wrap" style="top:60px;font-size:11px" data-node-id="1:474"', s)
    s = _rep('<div class="absolute h-[560px] left-[455px] top-[440px] w-[860px]" data-node-id="4:2"', '<div class="absolute h-[560px] left-[455px] top-[440px] w-[860px]" style="top:60px;height:560px" data-node-id="4:2"', s)
    s = _rep('contact.offsetTop-sc.scrollTop+440-32', 'contact.offsetTop-sc.scrollTop+60-32', s)
    s = _rep('height:${560*s}px`;', 'height:${560*s}px`;', s)
    s = _rep('top:${240*s}px`;', 'top:${240*s}px`;', s)
    # under the map: the basics; at the bottom the bar; the full text over the map when open
    PLUS = ('<svg viewBox="-12 -12 24 24" aria-hidden="true"><circle class="r1" r="8"/><circle class="r2" r="8"/><circle class="c" r="8"/>'
            '<path class="v" d="M0 -4.2V4.2"/><path d="M-4.2 0H4.2"/></svg>')
    parts = re.findall(r'(<h4>.*?</h4>)(<p[^>]*>.*?</p>)', LEGAL_BODY, re.S)
    get = {re.sub('<.*?>', '', h): h + t for h, t in parts}
    lp = re.search(r'<p class="lp">.*?</p>', LEGAL_BODY).group(0)
    legal = re.sub(r'(<h4>.*?</h4>)(<p[^>]*>.*?</p>)', r'<div class="ib">\1\2</div>', LEGAL_BODY, flags=re.S)
    add = (f'<div class="imptint" aria-hidden="true"></div><div class="impb" style="left:235px;top:825px;width:420px"><p class="lab2">IMPRESSUM</p>{lp}{get["Unternehmensgegenstand"]}</div>'
           f'<div class="impb" style="left:675px;top:825px;width:420px">{get["Medieninhaber, Herausgeber und Diensteanbieter"]}</div>'
           f'<div class="impc impfull" style="left:235px;top:640px;width:1080px;height:312px"><p class="lab2">IMPRESSUM</p>{legal}</div>'
           f'<button type="button" class="dcv dimp" id="dimp" aria-expanded="false">{PLUS}<span class="cvt"><span class="op">full</span><span class="cl">close</span></span><b>impressum</b></button>')
    a = '<section class="pg" id="contact"><div class="bg-white relative frame">'
    s = _rep(a, a + add, s)
    s = s.replace('</style>', IMP_CSS + '</style>', 1)
    s = s.replace('</body>', LBSW_JS + '</body>', 1)
    return s.replace('</body>', IMP_JS + '</body>', 1)


NOCOPY = '<style>/* photos are harder to copy (24 Oct): no dragging, no selecting, no long-press "save image" on phones */\nimg{-webkit-user-drag:none;user-drag:none;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}</style>\n<script>/* no right-click / long-press menu and no dragging on pictures (24 Oct) - the link logos keep their menu */\n(function(){ const ph=e=>{ const im=e.target.closest&&e.target.closest(\'img\'); return im&&!im.closest(\'a[href^="http"]\'); };\n  document.addEventListener(\'contextmenu\',e=>{ if(ph(e)) e.preventDefault(); },true);\n  document.addEventListener(\'dragstart\',e=>{ if(e.target.closest&&e.target.closest(\'img\')) e.preventDefault(); },true); })();</script>\n'


def _links_board(s):
    """24 Oct (Steuart, after the phone): the 15 links for clients on a draughts board - each link (logo, red name, grey line) on its own square,
    white and grey taking turns, so it is clear which text belongs to which logo. Squares 220 x 110 on the three right-hand columns
    (x 665 / 885 / 1105, from one dashed column line to the next), rows from y 428; the grey squares are the page's own grey"""
    sq = ''.join(f'<i style="left:{665 + c * 220}px;top:{428 + r * 110}px;width:220px"></i>'
                 for r in range(5) for c in range(3) if (r + c) % 2)
    a = '<section class="pg" id="downloads"><div class="bg-white relative frame"><div class="pgtint" aria-hidden="true"></div>'
    s = _rep(a, a + f'<div class="lboard" aria-hidden="true">{sq}</div>', s)
    return s.replace('</style>', '.lboard i{position:absolute;height:110px;background:#fff;pointer-events:none}   /* links on a draughts board (24 Oct) */\n</style>', 1)


def patch(s):
    if MARK in s:
        return s
    # ---- texts
    s = _sub1(r'(<p class="leading-\[normal\] mb-0">INFORMATION FOR CLIENTS</p><p class="fcal-r leading-\[normal\] mb-0">)Saepissime.*?(</p>)', r'\g<1>' + INFO_TXT + r'\2', s, re.S)
    s = _sub1(r'(<p class="leading-\[normal\] mb-0">LINKS FOR CLIENTS</p><p class="fcal-r leading-\[normal\] mb-0">)Saepissime.*?</p><p class="leading-\[normal\] mb-0">​</p><p class="fcal-r leading-\[normal\] mb-0">Amor enim.*?</p><p class="fcal-r leading-\[normal\] mb-0">Inter quos.*?(</p>)',
              r'\g<1>' + LINKS_TXT + r'\2', s, re.S)
    about = (f'<div class="ptx" style="left:235px;top:60px;width:420px"><p class="lab2">ABOUT US</p><p>{INTRO}</p></div>'
             f'<div class="ptx bio" style="left:895px;top:60px;width:420px"><p class="lab2">BIO</p>' + ''.join(f'<p>{t}</p>' for t in BIO) + '</div>')
    s = _rep('<section class="pg" id="services"><div class="bg-white relative frame">', '<section class="pg" id="services"><div class="bg-white relative frame">' + about, s)
    PLUS = ('<svg viewBox="-12 -12 24 24" aria-hidden="true"><circle class="r1" r="8"/><circle class="r2" r="8"/><circle class="c" r="8"/>'
            '<path class="v" d="M0 -4.2V4.2"/><path d="M-4.2 0H4.2"/></svg>')
    cvb = ''.join(f'<button type="button" class="dcv dcv{k}" data-k="{k}" aria-expanded="false" style="left:{x}px;top:803px;--xo:{x + 330}px">{PLUS}'
                  f'<span class="cvt"><span class="op">full</span><span class="cl">close</span></span><b>CV</b></button>' for k, x in ((1, 236), (2, 896)))
    s = _rep('<section class="pg" id="services"><div class="bg-white relative frame">', '<section class="pg" id="services"><div class="bg-white relative frame">' + cvb, s)
    end = f'<div class="ptx end" style="left:235px;top:930px;width:205px">{CONTACT_TXT}</div>'
    s = _rep('<section class="pg" id="contact"><div class="bg-white relative frame">', '<section class="pg" id="contact"><div class="bg-white relative frame">' + end, s)
    # ---- dasein-design in red, phone / e-mail links
    s = _rep('<p class="fcal-r leading-[normal] mb-0 text-[10px]">dasein-design [architecture+design] [Wien]</p>',
             '<p class="fcal-r leading-[normal] mb-0 text-[10px]"><b class="dd">dasein-design</b> [architecture+design] [Wien]</p>', s)
    for num, tel in (('+43 [0] 699 1941 9240', '+436991941 9240'), ('+43 [0] 676 4822 464', '+436764822464')):
        tel = tel.replace(' ', '')
        s = s.replace(f'not-italic"> {num} </span>', f'not-italic"> <a href="tel:{tel}">{num}</a> </span>')
    s = _rep('not-italic">+43 [0] 676 4822 464</span>', 'not-italic"><a href="tel:+436764822464">+43 [0] 676 4822 464</a></span>', s)
    s = _sub1(r'not-italic"> cuong</span>(<a [^>]*href="mailto:cuong@dasein-design.net"[^>]*>)<span ([^>]*)>@dasein-design.net</span></a>',
              r'not-italic"> </span>\1<span \2>cuong@dasein-design.net</span></a>', s)   # one link for the whole address
    for num, tel, mail in (('+43 (0)676 4822 464', '+436764822464', 'cuong@dasein-design.net'), ('+43 (0)699 1941 9240', '+4369919419240', 'steuart@dasein-design.net')):
        s = _rep(f'<p class="fcal-r leading-[normal] mb-0">{num}</p><p class="fcal-r leading-[normal] mb-0">{mail}</p>',
                 f'<p class="fcal-r leading-[normal] mb-0"><a href="tel:{tel}">{num}</a></p><p class="fcal-r leading-[normal] mb-0"><a href="mailto:{mail}">{mail}</a></p>', s)
    # ---- beetle: new leader lines, circles take turns
    s = _rep('<a class="hot pin" href="#services"', _leads() + '<a class="hot pin" href="#services"', s)
    k = [0]

    def pin(m):
        c1, c2 = RINGS[k[0]]
        out = f'<a class="hot pin" href="{m.group(1)}" style="{m.group(2)};--k:{k[0]};--c1:{c1};--c2:{c2}">{m.group(3)}<i class="cr"></i><i class="cr c2"></i>'
        k[0] += 1
        return out
    s = re.sub(r'<a class="hot pin" href="([^"]+)" style="([^"]+)">(\d\d)', pin, s)
    assert k[0] == 5
    s = _sub1(r'(<a class="hot pin" href="#contact".*?</a>)', lambda m: m.group(1) +
              '<a class="hot pin" href="#impressum" style="left:1200px;top:800px;--k:5;--c1:#3a3c37;--c2:#ffd400">i<i class="cr"></i><i class="cr c2"></i>'
              '<svg class="pring" viewBox="0 0 30 30" aria-hidden="true"><circle cx="15" cy="15" r="14.5"/></svg><span class="pl l">impressum</span></a>', s, re.S)
    s = _rep('<span class="pl r">us &amp; our services</span>', '<span class="pl r">about us</span>', s)
    # ---- pop-up
    s = _sub1(r'(<button type="button" class="lbx" id="lbx"[^>]*>)<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 2L14 14M14 2L2 14"/></svg>', r'\1' + XC, s)
    # ---- logos
    import os
    for n in sorted(os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img'))):
        if n.startswith('m-lg-'):
            s = s.replace('src="img/downloads-img' + n[5:] + '"', 'src="img/' + n + '"')
    # ---- menu: first tab renamed
    s = _tab_names(s)
    # ---- service icons: drawn in the compass style (img/ic-*.svg) instead of the red Figma pictograms
    for old, new in (('services-imgWorkstation.webp', 'ic-it.svg'), ('services-imgExterior.webp', 'ic-projekte.svg'), ('services-imgBrainstormSkill.webp', 'ic-skills.svg'), ('services-imgGroups.svg', 'ic-partnership.svg')):
        s = _rep('src="img/' + old + '"', 'src="img/' + new + '"', s)
    # ---- one job per line (22 Oct): the "---" text dividers become empty lines (spacing kept, no line)
    s = s.replace('>---</p>', '>\u200b</p>')
    # ---- red bars (22 Oct): gone on downloads (x2) and contact, with the "dasein-design" heading under them on downloads
    #      (contact keeps it as the first line of the address); on services the two bars above the partners become a dotted line
    #      across each partner's column, moved down to the tick at y 440, between the ID card / contact block and the CV
    for n in ('9:93', '16:360', '9:92'):
        s = _sub1(r'<div class="[^"]*" data-node-id="' + n + r'"></div>', '', s)
    for n in ('9:91', '16:359'):
        s = _sub1(r'(data-node-id="' + n + r'"><p class="leading-\[normal\] mb-0 text-\[red\]">dasein-design</p><p class="leading-\[normal\] mb-0">\u200b</p>)',
                  lambda m: m.group(0).split('>', 1)[0] + '>', s)
    s = _sub1(r'<div class="[^"]*" data-node-id="9:94"></div>', '', s)
    s = _sub1(r'<div class="[^"]*" data-node-id="9:95"><img[^>]*></div>', '', s)
    s = _rep('<section class="pg" id="services"><div class="bg-white relative frame">',
             '<section class="pg" id="services"><div class="bg-white relative frame"><i class="pline" style="left:235px"></i><i class="pline" style="left:895px"></i>', s)
    # ---- snap to the side-bar ticks (22 Oct): a block's top sits on the lower tick of the pair above it (y 60, 250, 440, 630, 820, 1010)
    SNAP = [('services', 'top-[255px] w-[420px]', 421), ('services', 'top-[254px] w-[200px]', 250), ('services', 'top-[57px] w-[200px]', 60),
            ('downloads', 'top-[65px] w-[420px]', 60), ('downloads', 'top-[445px] w-[420px]', 440), ('contact', 'top-[445px] w-[200px]', 440)]
    for sec, cls, y in SNAP:
        i = s.index('<section class="pg" id="' + sec + '"'); j = s.index('</section>', i); t = s[i:j]
        n = t.count(cls); assert n >= 1, (sec, cls)
        t = re.sub(r'class="([^"]*' + re.escape(cls) + r'[^"]*)"', lambda m: f'class="{m.group(1)}" style="top:{y}px"', t)
        s = s[:i] + t + s[j:]
    # ---- services (22 Oct): more white under the names - the ID cards with their captions and the contact details move down to the tick y 440,
    #      the CVs to the tick y 630 (the dotted line between them on the tick y 620)
    for nid in ('1:555', '1:600'):
        s = _sub1(r'(data-node-id="' + nid + r'" data-name="IMAGE" style="left:\d+px;)top:290px', r'\1top:455px', s)
    for nid, y in (('1:601', 558), ('1:603', 558), ('1:602', 574), ('1:604', 574), ('1:626', 455), ('1:627', 455), ('1:622', 630), ('1:623', 630)):
        s = _sub1(r'class="([^"]*)" data-node-id="' + nid + '"', lambda m: f'class="{m.group(1)}" data-node-id="{nid}" style="top:{y}px"', s)
    # ---- synchronised with the phone (22 Oct)
    # the big vertical title of page 01 reads "about us", like its tab and circle
    s, n = re.subn(r'<span class="fcal-b leading-\[normal\] text-\[50px\]">us </span><span class="fcal-l leading-\[normal\] text-\[50px\]">&amp;</span><span class="fcal-b leading-\[normal\] text-\[50px\]"> our services </span>',
                   '<span class="fcal-b leading-[normal] text-[50px]">about us </span>', s)
    assert n >= 1, n
    # no placeholder caption over the two ID cards
    for nid in ('1:601', '1:602', '1:603', '1:604'):
        s = _sub1(r'<div class="[^"]*" data-node-id="' + nid + r'"[^>]*>(?:(?!<div).)*?</div>' if nid in ('1:601', '1:603') else
                  r'<div class="[^"]*" data-node-id="' + nid + r'"[^>]*>.*?</p></div>', '', s, re.S)
    # one way of writing the address and the phone numbers
    s = _rep('<p class="leading-[normal] mb-0">NEULERCHENFELDERSTRASSE 42/6</p><p class="leading-[normal] mb-0">VIENNA. A-1160</p><p class="leading-[normal] mb-0">AUSTRIA </p><p class="leading-[normal] mb-0">EUROPE (EU)</p>',
             '<p class="leading-[normal] mb-0">Neulerchenfelderstrasse 42/6</p><p class="leading-[normal] mb-0">A-1160 Wien · Austria · EU</p>', s)
    s = _rep('>TRAN-VIET CUONG</p>', '>Cuong TRAN-VIET</p>', s)
    s = _rep('>STEUART J. MACKENZIE HARRISON</p>', '>Steuart J Mackenzie HARRISON</p>', s)
    s = s.replace('+43 [0] 699 1941 9240', '+43 (0)699 1941 9240').replace('+43 [0] 676 4822 464', '+43 (0)676 4822 464')
    # Figma typo
    s = s.replace('Ausfuhrungsplannung', 'Ausführungsplanung')
    # client subtitles in the small bold red capitals used everywhere else
    for t in ('INFORMATION FOR CLIENTS', 'LINKS FOR CLIENTS'):
        s = _rep(f'<p class="leading-[normal] mb-0">{t}</p>', f'<p class="leading-[normal] mb-0 sub2">{t}</p>', s)
    # Cuong is the owner: "» Architekt | Inhaber" (22 Oct)
    s = _rep('<span class="leading-[normal] text-[14px]">Architekt</span>',
             '<span class="leading-[normal] text-[14px]">Architekt<i class="rs"></i>Inhaber</span>', s)
    # ---- impressum (22 Oct): no extra page or tab on the desktop - a small dot above the copyright opens it in a pop-up
    # the copyright line reads "© 2026 [ dasein-design & steux ] · impressum" - the last word goes to the impressum page
    s, n = re.subn(r'(<div class="-translate-x-1/2 -translate-y-1/2 absolute flex )h-\[252px\]( items-center justify-center left-\[1343px\] )top-\[898px\]( w-\[36px\]" data-node-id="[^"]+")(><div class="-rotate-90 flex-none"><div class="[^"]*?) w-\[252px\]"><p class="whitespace-pre-wrap">(<span class="leading-\[normal\]">© 2026</span><span class="[^"]*">\s*\[ dasein-design &amp; steux \]</span>)</p>',
                   r'\1\2\3 style="height:330px;top:884px"\4" style="width:330px"><p class="whitespace-pre-wrap">\5<span class="fcal-r"> · </span><a class="impl" href="#impressum">§ impressum</a></p>', s)
    assert n >= 4, n
    s = _impressum_page(s)
    s = _tint(s)
    s = s.replace('src="img/services-imgImage.webp"', 'src="img/services-id-cuong-line.webp"')
    s = s.replace('src="img/services-imgImage1.webp"', 'src="img/services-portrait-steuart.webp"')   # 23 Oct: a black-and-white line drawing of the card, no personal numbers
    s = s.replace('<head>', '<head><script>/* phones go to the phone site (23 Oct); ?desktop=1 stays here and is remembered */ (function(){ try{ const q=new URLSearchParams(location.search);'
                  ' if(q.get("desktop")==="1") localStorage.setItem("dd-desktop","1"); if(q.get("desktop")==="0") localStorage.removeItem("dd-desktop");'
                  ' const narrow=Math.min(screen.width,screen.height)<=600||(innerWidth<=760&&matchMedia("(pointer:coarse)").matches);'
                  ' if(narrow&&localStorage.getItem("dd-desktop")!=="1") location.replace("phone/index.html"+location.hash); }catch(e){} })();</script>', 1)
    s = _desk_catchup(s)   # 23 Oct: bits & bats and the game gone, wonder in the fifth slot
    # ---- map + / - / home (22 Oct): finer lines, like the compass arrows
    s = _rep('.mz button circle{fill:rgba(255,255,255,.9);stroke:#e30613;stroke-width:2;', '.mz button circle{fill:rgba(255,255,255,.9);stroke:#e30613;stroke-width:1;', s)
    s = _rep('.mz button path{fill:none;stroke:#e30613;stroke-width:2;', '.mz button path{fill:none;stroke:#e30613;stroke-width:1.2;', s)
    # ---- project pop-up (22 Oct): the arrows beside the photo strip step to the previous / next photo instead of scrolling the strip
    s = _rep("$('lbsl0').onclick=()=>{ st.scrollLeft-=st.clientWidth*.8; }; $('lbsr0').onclick=()=>{ st.scrollLeft+=st.clientWidth*.8; };",
             "$('lbsl0').onclick=()=>step(-1); $('lbsr0').onclick=()=>step(1);", s)
    s = _rep("function arrows(){ $('lbsl0').disabled=st.scrollLeft<=1; $('lbsr0').disabled=st.scrollLeft+st.clientWidth>=st.scrollWidth-1; }",
             "function arrows(){}", s)
    # ---- project pop-up (22 Oct): the strip shows five thumbnails (two before and two after the current photo); a row of dots underneath shows how many there are in all
    s = _rep("st.querySelectorAll('button').forEach((b,k)=>b.classList.toggle('cur',k===ph));",
             "st.querySelectorAll('button').forEach((b,k)=>b.classList.toggle('cur',k===ph)); "
             "{ const n=pr.imgs.length, lo=Math.max(0,Math.min(ph-2,n-5)); st.querySelectorAll('button').forEach((b,k)=>{ b.hidden=k<lo||k>lo+4; }); "
             "const dd=$('lbdots'); if(dd.children.length!==n) dd.innerHTML=pr.imgs.map((s,k)=>'<i data-k=\"'+k+'\"></i>').join(''); "
             "[...dd.children].forEach((x,k)=>{ x.classList.toggle('on',k===ph); x.classList.toggle('vis',k>=lo&&k<=lo+4); }); }", s)
    s = _sub1(r'(<button type="button" class="lbsa r" id="lbsr0".*?</button></div>)', r'\1<div class="lbdots" id="lbdots"></div>', s, re.S)
    s = s.replace('</body>', '<script>document.getElementById("lbdots")&&document.getElementById("lbdots").addEventListener("click",e=>{ const i=e.target.closest("i"); if(i){ const b=document.querySelector("#lbst button[data-k=\'"+i.dataset.k+"\']"); if(b) b.click(); } });</script></body>', 1)
    # ---- styles
    s = _rep('</style>', CSS + WONDER_CSS + '.pgtint{position:absolute;left:235px;top:35px;width:1080px;height:958px;background:#f4f4f2;pointer-events:none}\n</style>', s)
    s = _contact_imp(s)   # 23 Oct, 13:04: contact + impressum on one page
    s = _links_board(s)   # 24 Oct: links for clients on a draughts board
    s = s.replace('</body>', NOCOPY + '</body>', 1)   # 24 Oct: photos harder to copy
    return s.replace('</body>', HEART_JS + EXT_JS + MARK + '</body>', 1)


if __name__ == '__main__':
    p = '../index.html'
    html = patch(open(p).read())
    open(p, 'w').write(html)
    print('patched', p)
