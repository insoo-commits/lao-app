// male-voice list: 예문 2 (w[4][1]) of every word; files are audio/m_<akey>.mp3
const fs=require('fs');const h=fs.readFileSync(process.argv[2],'utf8');
const i=h.indexOf('const DATA=')+11;let d=0,j=i;for(;;j++){const c=h[j];if(c=='{')d++;else if(c=='}'){d--;if(!d)break}}
const D=JSON.parse(h.slice(i,j+1));
const s0=h.indexOf('let SEG=null;'),s1=h.indexOf('function utterOf');eval(h.slice(s0,s1).replace('let SEG','var SEG'));
function akey(t){t=rep(String(t)).replace(/\s+/g," ").trim();let h=0x811c9dc5;for(let i=0;i<t.length;i++){h^=t.charCodeAt(i);h=Math.imul(h,0x01000193)>>>0}return h.toString(36)}
const out={};for(const b of Object.values(D.B)){b.w.forEach(w=>{const e=w[4][1];if(e&&e[0]){out['m_'+akey(e[0])]=rep(String(e[0])).replace(/\s+/g," ").trim()}});
  (b.dl||[]).forEach((x,di)=>{if(di%2&&x[1])out['m_'+akey(x[1])]=rep(String(x[1])).replace(/\s+/g," ").trim()})}
fs.writeFileSync(process.argv[3],JSON.stringify(out));console.log('male clips',Object.keys(out).length);
