const SHELL="lao-shell-v2.50",AUD="lao-audio-v2";
const JS="lao-js";/* versioned app.js?v=… lives here, kept across versions, only newest entry kept */
const FILES=["./","index.html","manifest.webmanifest","audio/index.js","icon-180.png","icon-192.png","icon-512.png","header.svg","header-day.svg"];
/* Audio clips live in IndexedDB ("lao-audio" / store "c", key = clip name, value = ArrayBuffer).
   They used to live in CacheStorage, but with 16k entries iPhone needs 10-15 s just to open CacheStorage,
   which blocked offline launches. CacheStorage now only holds the ~10 app files. */
let _db;const ADB=()=>_db||(_db=new Promise((res,rej)=>{const r=indexedDB.open("lao-audio",1);r.onupgradeneeded=()=>r.result.createObjectStore("c");r.onsuccess=()=>res(r.result);r.onerror=()=>{_db=null;rej(r.error)}}));
const aget=k=>ADB().then(db=>new Promise(res=>{const q=db.transaction("c").objectStore("c").get(k);q.onsuccess=()=>res(q.result||null);q.onerror=()=>res(null)})).catch(()=>null);
const aput=(k,v)=>ADB().then(db=>new Promise(res=>{const tx=db.transaction("c","readwrite");tx.objectStore("c").put(v,k);tx.oncomplete=()=>res(true);tx.onerror=tx.onabort=()=>res(false)})).catch(()=>false);
const mp3=b=>new Response(b,{headers:{"Content-Type":"audio/mpeg","Content-Length":String(b.byteLength)}});

self.addEventListener("install",e=>{e.waitUntil(caches.open(SHELL).then(c=>Promise.all(
  FILES.map(f=>fetch(new Request(f,{cache:"reload"})).then(r=>{if(r.ok)return c.put(f,r)}).catch(()=>{}))
  .concat(["_gap450","_gap900"].map(k=>fetch("audio/"+k+".mp3",{cache:"reload"}).then(r=>r.ok?r.arrayBuffer().then(b=>aput(k,b)):0).catch(()=>{})))
)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>(k.startsWith("lao-shell-")&&k!==SHELL)||(k.startsWith("lao-audio-")&&k!==AUD)).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET")return;
  if(u.pathname.includes("/audio/")&&u.pathname.endsWith(".mp3")){const v=u.searchParams.get("v"),k=u.pathname.split("/").pop().slice(0,-4)+(v?"@"+v:"");
    e.respondWith(aget(k).then(b=>{if(b)return mp3(b);
      return fetch(e.request).then(r=>{if(r.ok){const cl=r.clone();e.waitUntil(cl.arrayBuffer().then(b=>aput(k,b)).catch(()=>{}))}return r})
        // offline and not in IndexedDB yet: last try the old audio cache (only until the page has moved it over)
        .catch(()=>caches.has(AUD).then(h=>h?caches.open(AUD).then(c=>c.match("audio/"+k+".mp3")):null).then(m=>m||Response.error()))}));return}
  if(u.origin!==location.origin)return;
  // app.js?v=…: the version in the URL never changes content, so cache first; downloaded once per version
  if(u.pathname.endsWith("/app.js")&&u.searchParams.has("v")){
    e.respondWith(caches.open(JS).then(c=>c.match(e.request).then(m=>m||fetch(e.request).then(r=>{if(r.ok){const cl=r.clone();e.waitUntil(c.put(e.request,cl).then(()=>c.keys()).then(ks=>Promise.all(ks.filter(q=>q.url!==e.request.url).map(q=>c.delete(q)))))}return r})
      .catch(()=>c.match(e.request,{ignoreSearch:true}).then(m=>m||Response.error())))));return}
  // other app files: network first (so updates show right away), but after 4 s on a slow network use the saved copy
  const key=e.request.mode==="navigate"?"index.html":e.request;
  const cached=()=>caches.open(SHELL).then(c=>c.match(key,{ignoreSearch:true}).then(m=>m||(e.request.mode==="navigate"?c.match("index.html"):null)));
  const net=fetch(e.request,{cache:"no-cache"}).then(r=>{if(r.ok){const cl=r.clone();e.waitUntil(caches.open(SHELL).then(c=>c.put(key,cl)))}return r});
  e.respondWith(new Promise(res=>{let done=false;const go=r=>{if(!done&&r){done=true;res(r)}};
    const t=setTimeout(()=>cached().then(go),4000);
    net.then(r=>{clearTimeout(t);go(r)}).catch(()=>{clearTimeout(t);cached().then(m=>{go(m||Response.error())})})}))});
