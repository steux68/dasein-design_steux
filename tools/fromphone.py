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
from texts import INTRO, BIO, INFO_TXT, LINKS_TXT, CONTACT_TXT, LEGAL_BODY

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
LEADS = [((335, 377), (335, 420), (580, 420)),     # 01 about us -> back leg
         ((555, 744), (555, 652), (648, 652)),     # 02 projects -> back foot
         ((775, 328), None, (775, 432)),           # 03 downloads & links -> middle leg
         ((995, 692), (995, 671), (1086, 671)),    # 04 bits & bats -> lower jaw
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
.hot.pin{animation:pinon 7.5s ease-in-out infinite;animation-delay:calc(var(--k) * 1.5s)}
@keyframes pinon{0%{background:#bfbfbf}3%{background:#cdff3e}17%{background:#cdff3e}20%{background:#bfbfbf}100%{background:#bfbfbf}}
.pin .cr{position:absolute;inset:-1px;border-radius:50%;border:1.6px solid var(--c1);opacity:0;pointer-events:none;
  animation:pinturn 7.5s ease-out infinite;animation-delay:calc(var(--k) * 1.5s + .3s)}
.pin .cr.c2{border-color:var(--c2);animation-delay:calc(var(--k) * 1.5s + .6s)}
@keyframes pinturn{0%{transform:scale(1);opacity:.9}15%{transform:scale(2.3);opacity:0}100%{transform:scale(2.3);opacity:0}}
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
.lbk{display:none}
.lbm{align-items:center}
.lbm .lbkc{font:400 13px/25px Calibri,Carlito,sans-serif;color:#666;letter-spacing:.06em}
.lbm .lbkc b{color:#e30613;font-weight:400}
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
.hot.imp:hover span,.hot.imp:hover b,.hot.imp:focus-visible span,.hot.imp:focus-visible b{color:#e30613}
.hot.imp:hover .ii{animation:none;border-color:#e30613;color:#e30613;background:#cdff3e} .hot.imp:focus-visible{outline:none}
@media (prefers-reduced-motion:reduce){.hot.imp .ii{animation:none}}
/* three clicks on the beetle: the heart */
.heartfx{position:fixed;inset:0;z-index:9999;pointer-events:none;overflow:hidden}
.heartfx svg{position:absolute;left:0;top:0;width:60px;height:60px;margin:-30px 0 0 -30px;fill:#e30613;will-change:transform,opacity}
.heartfx .sm{width:16px;height:16px;margin:-8px 0 0 -8px}
/* link logos trimmed to their edges, with a small margin in their boxes */
img[src^="img/m-lg-"]{box-sizing:border-box;padding:6px 12px}
'''


IMP_JS = r"""<script>
(function(){ const d=document.getElementById('impd'); if(!d) return;
  document.querySelectorAll('a.imp').forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); d.showModal(); }));
  document.getElementById('impx').onclick=()=>d.close();
  d.addEventListener('click',e=>{ if(e.target===d) d.close(); });
})();
</script>"""

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
    s = _rep('<span class="pl r">us &amp; our services</span>', '<span class="pl r">about us</span>', s)
    # ---- pop-up
    s = _sub1(r'(<button type="button" class="lbx" id="lbx"[^>]*>)<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 2L14 14M14 2L2 14"/></svg>', r'\1' + XC, s)
    s = _rep('<span id="lbk"></span>', '', s)
    s = _sub1(r'(<div class="lbm"><button type="button" class="pp" id="lbpp">.*?</button>)', r'\1<span class="lbkc" id="lbk"></span>', s, re.S)
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
    s = _rep('<a class="hot social" href="#" data-pending="1" aria-label="Facebook"',
             '<a class="hot imp" href="#impressum" aria-label="impressum - click to open" title="click to open the full impressum" style="left:1330px;top:552px;width:26px;height:210px">'
             '<span><i class="ii">i</i> <b>impressum</b> · click for the full text</span></a>'
             '<a class="hot social" href="#" data-pending="1" aria-label="Facebook"', s)
    s = s.replace('</body>', '<dialog class="impd" id="impd" aria-label="impressum"><button type="button" class="lbx" id="impx" aria-label="close (Esc)">' + XC + '</button>'
                  '<div class="impc"><p class="lab2">IMPRESSUM</p>' + LEGAL_BODY + '</div></dialog>' + IMP_JS + '</body>', 1)
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
    s = _rep('</style>', CSS + '</style>', s)
    return s.replace('</body>', HEART_JS + MARK + '</body>', 1)


if __name__ == '__main__':
    p = '../index.html'
    html = patch(open(p).read())
    open(p, 'w').write(html)
    print('patched', p)
