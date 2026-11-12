const SHELL="lao-shell-v9.11",AUD="lao-audio-v1";
const FILES=["./","index.html","app.js","manifest.webmanifest","audio/index.js","icon-180.png","icon-192.png","icon-512.png","audio/_gap450.mp3","audio/_gap900.mp3"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(SHELL).then(c=>Promise.all(FILES.map(f=>fetch(new Request(f,{cache:"reload"})).then(r=>{if(r.ok)return c.put(f,r)}).catch(()=>{})))).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith("lao-shell-")&&k!==SHELL).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET")return;
  if(u.pathname.includes("/audio/")&&u.pathname.endsWith(".mp3")){e.respondWith(caches.open(AUD).then(async c=>{const m=await c.match(u.pathname.split("/").slice(-2).join("/"))||await c.match(e.request);if(m)return m;const r=await fetch(e.request);if(r.ok)c.put(e.request,r.clone());return r}));return}
  if(u.origin!==location.origin)return;
  // app files: network first (so updates show right away), cache when offline
  e.respondWith(fetch(e.request,{cache:"no-cache"}).then(r=>{if(r.ok){const cl=r.clone();caches.open(SHELL).then(c=>c.put(e.request.mode==="navigate"?"index.html":e.request,cl))}return r})
    .catch(()=>caches.match(e.request,{ignoreSearch:true}).then(m=>m||caches.match("index.html"))))});
