const V='ghisa-v4',CORE=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V&&x!=='ghisa-share').map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
 const r=e.request;
 /* Condividi › Ghisa: i file arrivano qui, li tengo in una cache e apro l'app sull'import */
 if(r.method==='POST'&&new URL(r.url).searchParams.has('share-target')){e.respondWith((async()=>{const fd=await r.formData(),F=fd.getAll('f').filter(f=>f&&f.name),c=await caches.open('ghisa-share');for(const k of await c.keys())await c.delete(k);let i=0;for(const f of F)await c.put('./_share/'+(i++)+'/'+encodeURIComponent(f.name),new Response(f));return Response.redirect('./?gximp='+F.length,303)})());return}
 if(r.method!=='GET')return;
 const u=new URL(r.url);
 if(u.origin===location.origin){
  /* rete per prima (così gli aggiornamenti arrivano subito), cache se offline */
  e.respondWith(fetch(r).then(x=>{if(x.ok){const c=x.clone();caches.open(V).then(h=>h.put(r,c))}return x}).catch(()=>caches.match(r).then(m=>m||caches.match('./index.html'))));
 }else if(/fonts\.(googleapis|gstatic)\.com$/.test(u.hostname)){
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(x=>{const c=x.clone();caches.open(V).then(h=>h.put(r,c));return x}).catch(()=>m)));
 }
});
/* tocco sulla notifica di fine recupero o di cambio fase: torna all'app aperta, oppure la apre */
self.addEventListener('notificationclick',e=>{e.notification.close();e.waitUntil(self.clients.matchAll({type:'window',includeUncontrolled:true}).then(L=>{const c=L.find(x=>'focus' in x);return c?c.focus():self.clients.openWindow('./')}))});
