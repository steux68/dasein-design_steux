/* Mini-Service-Worker: macht die Seite für Chrome als App installierbar. Er speichert nichts.
   Bei jedem Öffnen wird beim Server nachgefragt, ob es eine neuere Fassung gibt (cache:'no-cache' = prüfen, nur bei Änderung neu laden),
   damit nach einem Update nicht die alte Seite aus dem Zwischenspeicher kommt. */
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);
  e.respondWith(u.origin===location.origin?fetch(e.request,{cache:'no-cache'}):fetch(e.request));});
