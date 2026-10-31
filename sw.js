/* Mini-Service-Worker: macht die Seite für Chrome als App installierbar. Er speichert nichts und reicht alles unverändert durch. */
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(fetch(e.request));});
