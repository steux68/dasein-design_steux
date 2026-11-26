/* common.js – gemeinsames Modul für DOCH!, PASSAGE a–x und dasein-design. In allen drei Repos derselbe Inhalt.
   Stand 2026-11-26 (Audit 27.11., Punkte 7 und 8). Später kommen hierher auch Bildladen, Versions-Check und Start-Regel.

   AppBack – Zurück-Taste (Android) nach einer Regel für alle Apps:
     1. zuerst ein offenes Pop-up schließen, 2. dann eine Ebene zurück, 3. dann zum Start (Titelseite oben),
     4. am Start verlässt Zurück die App.
   Die App meldet ihre „Ebenen“ mit AppBack.add({open:()=>bool, close:()=>void}), oberste (Pop-up) zuerst.
   Für jede offene Ebene liegt genau ein Eintrag im Verlauf (state.cj = 1, 2, …). Einträge entstehen nur direkt
   nach einem Tippen (sonst überspringt Chrome sie), und wenn eine Ebene in der App geschlossen wird (✕, Start-Knopf),
   wird der überzählige Eintrag wieder entfernt. So bleibt der Verlauf immer so lang wie die offenen Ebenen.
   Apps mit eigener Seiten-Navigation (PASSAGE: #r1, #wissen …) melden nur ihre Pop-ups an; der Rest läuft wie bisher.

   AppSwipe – waagrechtes Wischen auf Lernkarten, wie im Theorie-Pop-up von DOCH (#pb):
     mehr als 60 px waagrecht und 1,5-mal mehr waagrecht als senkrecht, innerhalb von 0,8 s.
     Senkrechtes Scrollen, Zeichnen, Schieberegler und waagrecht scrollende Leisten bleiben unberührt. */
(function(w,d){"use strict";
if(w.AppBack)return;

var AppBack=(function(){
  var L=[],skip=0,skipT=0,busy=false,armed=false;
  function dep(){try{var s=w.history.state;return s&&typeof s.cj==="number"?s.cj:0;}catch(e){return 0;}}
  function isOpen(l){try{return !!l.open();}catch(e){return false;}}
  function count(){var n=0;for(var i=0;i<L.length;i++)if(isOpen(L[i]))n++;return n;}
  function top(){for(var i=0;i<L.length;i++)if(isOpen(L[i]))return L[i];return null;}
  function st(k){var s={};try{var o=w.history.state;if(o&&typeof o==="object")for(var x in o)if(x!=="cj")s[x]=o[x];}catch(e){}s.cj=k;return s;}
  function noSkip(){skip=0;clearTimeout(skipT);}
  /* Verlauf an die offenen Ebenen anpassen */
  function sync(){if(!armed||busy||skip)return;var n=count(),k=dep();
    if(n>k){for(;k<n;k++){try{w.history.pushState(st(k+1),"");}catch(e){return;}}}
    else if(n<k){skip=1;clearTimeout(skipT);skipT=setTimeout(noSkip,800);try{w.history.go(n-k);}catch(e){noSkip();}}}
  function later(){setTimeout(sync,0);setTimeout(sync,450);}
  /* Zurück-Taste: so viele Ebenen schließen, bis es zur Tiefe des Eintrags passt (in der Regel genau eine) */
  function pop(e){
    if(skip){noSkip();if(e&&e.stopImmediatePropagation)e.stopImmediatePropagation();return;}
    if(!armed)return;
    var k=dep(),n=count();if(n<=k)return;            /* nichts von uns offen: die App selbst ist dran (PASSAGE-Navigation) */
    if(e&&e.stopImmediatePropagation)e.stopImmediatePropagation();
    busy=true;
    try{for(var g=0;g<12&&n>k;g++){var l=top();if(!l)break;l.close();var m=count();if(m>=n)break;n=m;}}catch(x){}
    busy=false;setTimeout(sync,0);}
  w.addEventListener("popstate",pop);
  return{
    add:function(o){if(o&&o.open&&o.close)L.push(o);return this;},
    init:function(){if(armed)return this;armed=true;
      try{if(typeof (w.history.state&&w.history.state.cj)!=="number")w.history.replaceState(st(0),"");}catch(e){}
      ["click","keyup","touchend","change"].forEach(function(t){d.addEventListener(t,later,true);});
      later();return this;},
    sync:later,depth:dep,count:count};
})();

/* Elemente, auf denen ein Wischer etwas anderes bedeutet */
var NOSW="input,textarea,select,button[role=slider],[role=slider],[contenteditable],[data-noswipe],.noswipe";
function scrollsX(t,root){for(var x=t;x&&x!==root&&x.nodeType===1;x=x.parentElement){
  if(x.scrollWidth>x.clientWidth+2){var o=getComputedStyle(x).overflowX;if(o==="auto"||o==="scroll")return true;}}return false;}
function AppSwipe(el,o){if(!el||!o)return;o=o||{};
  var MIN=o.min||60,R=o.ratio||1.5,x0=null,y0=0,t0=0;
  el.addEventListener("touchstart",function(e){x0=null;if(e.touches.length!==1)return;
    var t=e.target;if(t&&t.closest&&(t.closest(NOSW)||(o.ignore&&t.closest(o.ignore))))return;
    if(o.when&&!o.when())return;if(scrollsX(t,el))return;
    var p=e.touches[0];x0=p.clientX;y0=p.clientY;t0=Date.now();},{passive:true});
  el.addEventListener("touchmove",function(e){if(e.touches.length!==1)x0=null;},{passive:true});
  el.addEventListener("touchcancel",function(){x0=null;},{passive:true});
  el.addEventListener("touchend",function(e){if(x0==null)return;var p=e.changedTouches[0],dx=p.clientX-x0,dy=p.clientY-y0;x0=null;
    if(Date.now()-t0>800)return;
    if(Math.abs(dx)>MIN&&Math.abs(dx)>Math.abs(dy)*R){if(o.when&&!o.when())return;var f=dx<0?o.next:o.prev;if(f)f();}},{passive:true});}
/* einen (versteckten) Knopf drücken, falls es ihn gibt und er nicht gesperrt ist */
function press(id){var b=typeof id==="string"?d.getElementById(id):id;if(b&&!b.disabled&&b.getAttribute("aria-disabled")!=="true"){b.click();return true;}return false;}

w.AppBack=AppBack;w.AppSwipe=AppSwipe;w.AppCommon={version:"2026-11-26",press:press};
})(window,document);
