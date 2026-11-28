// Korean meaning list (word playback ×2: Lao, Korean, Lao); files are audio/k_<akey>.mp3
const fs=require('fs');const h=fs.readFileSync(process.argv[2],'utf8');
const i=h.indexOf('const DATA=')+11;let d=0,j=i;for(;;j++){const c=h[j];if(c=='{')d++;else if(c=='}'){d--;if(!d)break}}
const D=JSON.parse(h.slice(i,j+1));
const s0=h.indexOf('let SEG=null;'),s1=h.indexOf('function utterOf');eval(h.slice(s0,s1).replace('let SEG','var SEG'));
function akey(t){t=rep(String(t)).replace(/\s+/g," ").trim();let h=0x811c9dc5;for(let i=0;i<t.length;i++){h^=t.charCodeAt(i);h=Math.imul(h,0x01000193)>>>0}return h.toString(36)}
const out={};for(const b of Object.values(D.B))b.w.forEach(w=>{if(w[3])out['k_'+akey(w[3])]=String(w[3]).replace(/[\u2460-\u2473]/g,'').replace(/\s*\([^)]*\)/g,'').replace(/[;·]/g,',').replace(/\s+/g,' ').trim()||String(w[3])});
fs.writeFileSync(process.argv[3],JSON.stringify(out));console.log('ko clips',Object.keys(out).length);
