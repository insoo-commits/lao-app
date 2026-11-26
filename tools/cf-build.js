/* Cloudflare Pages build (phasalao.pages.dev, was studylao.pages.dev), v3.44, 2026-11-25.
   Cloudflare settings:  Build command  node tools/cf-build.js   ·  Build output directory  cf
   Copies the site into cf/ without the ~34,600 single mp3 clips, and instead joins the clips of each bundle into one pack
   cf/audio/p/<bundle>.bin, so the site has about 1,000 files (Cloudflare Pages free plan: 20,000; RYU wants under 10-15k).
   Pack file = 4-byte little-endian header length N, N bytes of JSON [[clip, offset, length], ...], then the mp3 bytes.
   Each slice is the original mp3 file byte for byte, so the sound is unchanged. A clip used by several bundles is in each of
   their packs, so opening a bundle needs only that bundle's pack. Clips that no bundle text points to go to a few "x" packs.
   cf/audio/index.js = audio/index.js + window.AUDIO_PACKS = [[code, hash, "clip clip ..."], ...] (clips whose home is that pack).
   GitHub Pages is not touched: there AUDIO_PACKS does not exist and the app fetches the single mp3s as before.
   Run locally the same way (node tools/cf-build.js) to test; cf/ is in .gitignore. */
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const root = path.join(__dirname, ".."), out = path.join(root, "cf"), audio = path.join(root, "audio");
const skip = new Set([".git", ".github", "cf", "tools", "test", "node_modules"]);
fs.rmSync(out, {recursive: true, force: true});
let n = 0;
(function copy(rel){
  for (const e of fs.readdirSync(path.join(root, rel), {withFileTypes: true})){
    const r = path.join(rel, e.name);
    if (!rel && (skip.has(e.name) || /\.(md|py)$/.test(e.name))) continue;
    if (e.isDirectory()){ copy(r); continue; }
    if (rel === "audio" && e.name.endsWith(".mp3") && !e.name.startsWith("_")) continue;   // _gap*.mp3 stay single
    if (rel === "audio" && e.name === "index.js") continue;   // written below
    fs.mkdirSync(path.join(out, rel), {recursive: true}); fs.copyFileSync(path.join(root, r), path.join(out, r)); n++;
  }
})("");

/* the clip names of each bundle: the app names a clip akey(text) ("k_" Korean meaning, "m_" male voice), see app.js */
const L = fs.readFileSync(path.join(root, "app.js"), "utf8").split("\n");
const line = re => { const s = L.find(x => re.test(x)); if (!s) throw new Error("app.js: no line " + re); return s; };
const fnBlock = name => { const i = L.findIndex(x => x.startsWith("function " + name + "(")); let j = i + 1; while (j < L.length && /^\s/.test(L[j])) j++; return L.slice(i, j).join("\n"); };
const {DATA, akey} = new Function([line(/^const DATA=/), line(/^const NDICT=/), line(/^Object\.assign\(NDICT,/),
  "let SEG=null;try{SEG=new Intl.Segmenter('lo',{granularity:'word'})}catch(e){}", fnBlock("akey"), fnBlock("rep"), "return {DATA, akey};"].join("\n"))();
const AUDSRC = fs.readFileSync(path.join(audio, "index.js"), "utf8");
const AUD = JSON.parse(AUDSRC.trim().replace(/^window\.AUDIO_INDEX=/, "").replace(/;$/, ""));
const strs = (o, acc) => { if (typeof o === "string") acc.push(o); else if (o && typeof o === "object") for (const v of Object.values(o)) strs(v, acc); return acc; };
const lessons = [], used = new Set();
for (const code of DATA.P.flatMap(p => p.subs.flatMap(s => s.b))){
  const keys = new Set();
  for (const s of strs(DATA.B[code], [])) for (const t of [s, ...s.split(/\s*[·;\/|]\s*/)]){
    if (!t) continue; const k = akey(t);
    for (const kk of [k, "k_" + k, "m_" + k]) if (AUD[kk]) keys.add(kk);
  }
  if (keys.size){ lessons.push([code, [...keys]]); keys.forEach(k => used.add(k)); }
}
const rest = Object.keys(AUD).filter(k => !used.has(k)).sort();
for (let i = 0; i < rest.length; i += 200) lessons.push(["x" + String(i / 200 + 1).padStart(2, "0"), rest.slice(i, i + 200)]);

const dir = path.join(out, "audio", "p"); fs.mkdirSync(dir, {recursive: true});
const packs = [], home = new Set(); let bytes = 0;
for (const [code, keys] of lessons){
  const parts = [], table = []; let off = 0;
  for (const k of keys){
    const f = path.join(audio, k + ".mp3"); if (!fs.existsSync(f)) continue;
    const b = fs.readFileSync(f); table.push([k, off, b.length]); parts.push(b); off += b.length;
  }
  if (!table.length) continue;
  const head = Buffer.from(JSON.stringify(table)), len = Buffer.alloc(4); len.writeUInt32LE(head.length);
  const buf = Buffer.concat([len, head, ...parts]);
  fs.writeFileSync(path.join(dir, code + ".bin"), buf); n++; bytes += buf.length;
  const mine = table.map(t => t[0]).filter(k => !home.has(k)); mine.forEach(k => home.add(k));   // home pack = first bundle that uses the clip
  packs.push([code, crypto.createHash("sha1").update(buf).digest("hex").slice(0, 8), mine.join(" ")]);
}
fs.writeFileSync(path.join(out, "audio", "index.js"), AUDSRC.trim() + "\nwindow.AUDIO_PACKS=" + JSON.stringify(packs) + ";\n"); n++;
/* packs carry their hash in the link (?h=), so they can be kept long; app files are checked every time */
fs.writeFileSync(path.join(out, "_headers"), "/audio/p/*\n  Cache-Control: public, max-age=31536000, immutable\n/sw.js\n  Cache-Control: no-cache\n"); n++;
console.log("cf/: " + n + " files · " + packs.length + " packs, " + (bytes / 1e6).toFixed(1) + " MB · clips " + home.size + " of " + Object.keys(AUD).length + " (" + rest.length + " in x packs)");
if (home.size < Object.keys(AUD).length) console.log("missing mp3:", Object.keys(AUD).filter(k => !home.has(k)).slice(0, 20).join(" "));
if (n > 15000) throw new Error("over 15,000 files (RYU's limit; Cloudflare free plan allows 20,000)");
