"""Package the offline app as an installable PWA (iPhone: Safari > Share > Add to Home Screen).
Usage: python3 build_pwa.py <offline.html> <audio_dir> <out_dir>"""
import sys, os, json, shutil, hashlib, glob
src, adir, out = sys.argv[1:4]; here=os.path.dirname(os.path.abspath(__file__))
os.makedirs(out+'/audio', exist_ok=True)
keys=sorted(os.path.basename(p)[:-4] for p in glob.glob(adir+'/*.mp3'))
for k in keys:
    d=f'{out}/audio/{k}.mp3'
    if not os.path.exists(d): shutil.copyfile(f'{adir}/{k}.mp3', d)
open(f'{out}/audio/index.js','w').write('window.AUDIO_INDEX='+json.dumps({k:1 for k in keys},separators=(',',':'))+';')
h=open(src,encoding='utf-8').read()
head='''<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#8a5a12">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="라오스어">
<link rel="apple-touch-icon" href="icon-180.png"><script src="audio/index.js"></script>'''
h=h.replace('<title>', head+'\n<title>',1)
tail='''<script>
if("serviceWorker" in navigator)navigator.serviceWorker.register("sw.js").catch(()=>{});
(function(){const n=document.getElementById("voiceNote");if(!n||!window.AUDIO_INDEX)return;
const ks=Object.keys(window.AUDIO_INDEX);const b=document.createElement("button");b.className="speak all";b.style.marginLeft="8px";
b.textContent="음성 전체 저장 (오프라인용)";n.after(b);
b.onclick=async()=>{if(!("caches" in window))return;b.disabled=true;const c=await caches.open("lao-audio-v1");let done=0;
 const q=ks.slice();async function w(){while(q.length){const k=q.shift();const u="audio/"+k+".mp3";try{if(!(await c.match(u))){const r=await fetch(u);if(r.ok)await c.put(u,r)}}catch(e){}done++;if(done%50==0||done==ks.length)b.textContent="저장 중 "+done+"/"+ks.length}}
 await Promise.all([w(),w(),w(),w(),w(),w()]);b.textContent="음성 "+ks.length+"개 저장 완료";try{localStorage.setItem("lao-audio-saved","1")}catch(e){}};
try{if(localStorage.getItem("lao-audio-saved"))b.textContent="음성 저장됨 (다시 확인)"}catch(e){}})();
</script>'''
h=h.replace('</body>', tail+'\n</body>') if '</body>' in h else h+tail
open(f'{out}/index.html','w',encoding='utf-8').write(h)
ver=hashlib.md5(h.encode()).hexdigest()[:8]
json.dump({"name":"라오스어 묶음 학습","short_name":"라오스어","start_url":"./","scope":"./","display":"standalone",
  "background_color":"#faf6ee","theme_color":"#8a5a12","lang":"ko",
  "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]},
  open(f'{out}/manifest.webmanifest','w'),ensure_ascii=False)
for n in (180,192,512): shutil.copyfile(f'{here}/icon-{n}.png', f'{out}/icon-{n}.png')
open(f'{out}/sw.js','w').write(f'''const SHELL="lao-shell-{ver}",AUD="lao-audio-v1";
const FILES=["./","index.html","manifest.webmanifest","audio/index.js","icon-180.png","icon-192.png","icon-512.png"];
self.addEventListener("install",e=>{{e.waitUntil(caches.open(SHELL).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith("lao-shell-")&&k!==SHELL).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener("fetch",e=>{{const u=new URL(e.request.url);if(e.request.method!=="GET")return;
  if(u.pathname.includes("/audio/")&&u.pathname.endsWith(".mp3")){{e.respondWith(caches.open(AUD).then(async c=>{{const m=await c.match(u.pathname.split("/").slice(-2).join("/"))||await c.match(e.request);if(m)return m;const r=await fetch(e.request);if(r.ok)c.put(e.request,r.clone());return r}}));return}}
  e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(m=>m||fetch(e.request).then(r=>{{if(r.ok&&u.origin===location.origin){{const cl=r.clone();caches.open(SHELL).then(c=>c.put(e.request,cl))}}return r}}).catch(()=>caches.match("index.html"))))}});
''')
open(f'{out}/.nojekyll','w').write('')
print('pwa ok', len(keys), 'audio files', ver)
