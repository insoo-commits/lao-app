const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const dir=__dirname;const art=fs.readFileSync(dir+'/art.svg','utf8');const base=fs.readFileSync(dir+'/base.css','utf8');
const b=await chromium.launch();
for(const v of process.argv.slice(2)){const css=base+fs.readFileSync(`${dir}/${v}.css`,'utf8');
for(const [w,h,m,n,dark] of [[1280,860,false,'pc',false],[390,800,true,'ph',false],[390,800,true,'phd',true]]){
const c=await b.newContext({viewport:{width:w,height:h},isMobile:m,hasTouch:m,deviceScaleFactor:2,colorScheme:dark?'dark':'light'});const p=await c.newPage();
await p.route('**/index.html',async r=>{const res=await r.fetch();let t=await res.text();t=t.replace(/<\/head>/i,`<style id="skin">${css}</style></head>`).replace(/<header>/,'<header>'+art);r.fulfill({response:res,body:t,headers:{...res.headers(),'content-type':'text/html; charset=utf-8'}})});
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(2500);await p.screenshot({path:`${dir}/${v}_${n}.png`});await c.close()}}
await b.close()})();
