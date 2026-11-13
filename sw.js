const SHELL="lao-shell-v10.9",AUD="lao-audio-v2";
const FILES=["./","index.html","app.js","manifest.webmanifest","audio/index.js","icon-180.png","icon-192.png","icon-512.png","header.svg","header-day.svg","audio/_gap450.mp3","audio/_gap900.mp3"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(SHELL).then(c=>Promise.all(FILES.map(f=>fetch(new Request(f,{cache:"reload"})).then(r=>{if(r.ok)return c.put(f,r)}).catch(()=>{})))).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>(k.startsWith("lao-shell-")&&k!==SHELL)||(k.startsWith("lao-audio-")&&k!==AUD)).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET")return;
  if(u.pathname.includes("/audio/")&&u.pathname.endsWith(".mp3")){e.respondWith(caches.open(AUD).then(async c=>{const m=await c.match(u.pathname.split("/").slice(-2).join("/"))||await c.match(e.request);if(m)return m;const p=u.pathname.split("/").slice(-2).join("/");const sm=await caches.open(SHELL).then(s=>s.match(p));if(sm)return sm;if(self.navigator&&self.navigator.onLine===false)return Response.error();const r=await fetch(e.request);if(r.ok)c.put(e.request,r.clone());return r}));return}
  if(u.origin!==location.origin)return;
  // app files: show the saved copy at once (never wait for the network), refresh the saved copy in the background.
  // New versions therefore appear on the next launch. Only the small SHELL cache is searched (the 16k-clip audio cache is slow on iOS).
  const key=e.request.mode==="navigate"?"index.html":e.request;
  const net=fetch(e.request,{cache:"no-cache"}).then(r=>{if(r.ok){const cl=r.clone();return caches.open(SHELL).then(c=>c.put(key,cl)).then(()=>r,()=>r)}return r});
  e.respondWith(caches.open(SHELL).then(c=>c.match(key,{ignoreSearch:true}).then(m=>m||(e.request.mode==="navigate"?c.match("index.html"):undefined))).then(m=>{
    if(m){e.waitUntil(net.catch(()=>{}));return m}
    return net.catch(()=>caches.open(SHELL).then(c=>c.match("index.html")))}))});
