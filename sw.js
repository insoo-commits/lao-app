const SHELL="lao-shell-v10.10",AUD="lao-audio-v2";
const FILES=["./","index.html","app.js","manifest.webmanifest","audio/index.js","icon-180.png","icon-192.png","icon-512.png","header.svg","header-day.svg","audio/_gap450.mp3","audio/_gap900.mp3"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(SHELL).then(c=>Promise.all(FILES.map(f=>fetch(new Request(f,{cache:"reload"})).then(r=>{if(r.ok)return c.put(f,r)}).catch(()=>{})))).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>(k.startsWith("lao-shell-")&&k!==SHELL)||(k.startsWith("lao-audio-")&&k!==AUD)).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET")return;
  if(u.pathname.includes("/audio/")&&u.pathname.endsWith(".mp3")){e.respondWith(caches.open(AUD).then(async c=>{const m=await c.match(u.pathname.split("/").slice(-2).join("/"))||await c.match(e.request);if(m)return m;if(/_gap\d+\.mp3$/.test(u.pathname)){const sm=await caches.open(SHELL).then(s=>s.match("audio/"+u.pathname.split("/").pop()));if(sm)return sm}const r=await fetch(e.request);if(r.ok)c.put(e.request,r.clone());return r}));return}
  if(u.origin!==location.origin)return;
  // app files: network first (so updates show right away), cache when offline.
  // Offline fallback looks ONLY in the small SHELL cache: a global caches.match over the 16k-clip audio cache takes 10-15 s on iPhone.
  e.respondWith(fetch(e.request,{cache:"no-cache"}).then(r=>{if(r.ok){const cl=r.clone();caches.open(SHELL).then(c=>c.put(e.request.mode==="navigate"?"index.html":e.request,cl))}return r})
    .catch(()=>caches.open(SHELL).then(c=>c.match(e.request.mode==="navigate"?"index.html":e.request,{ignoreSearch:true}).then(m=>m||c.match("index.html")))))});
