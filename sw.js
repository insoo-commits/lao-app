const SHELL="lao-shell-f811a2e2",AUD="lao-audio-v1";
const FILES=["./","index.html","manifest.webmanifest","audio/index.js","icon-180.png","icon-192.png","icon-512.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(SHELL).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith("lao-shell-")&&k!==SHELL).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET")return;
  if(u.pathname.includes("/audio/")&&u.pathname.endsWith(".mp3")){e.respondWith(caches.open(AUD).then(async c=>{const m=await c.match(u.pathname.split("/").slice(-2).join("/"))||await c.match(e.request);if(m)return m;const r=await fetch(e.request);if(r.ok)c.put(e.request,r.clone());return r}));return}
  e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(m=>m||fetch(e.request).then(r=>{if(r.ok&&u.origin===location.origin){const cl=r.clone();caches.open(SHELL).then(c=>c.put(e.request,cl))}return r}).catch(()=>caches.match("index.html"))))});
