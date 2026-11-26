// 도움말 화면 캡처 (v4.6, KoJey·한국어배우기 tools/help_shots.js 방식): img/help/<name>.jpg + <name>-d.jpg (어두운 화면).
// 사용: 저장소 폴더에서 python3 -m http.server 8811 을 켜 두고 node tools/help_shots.js
// 앱의 HELPSHOTS(app.js v4.6 블록)가 이 그림들을 도움말 쪽에 넣음.
const {chromium} = require("playwright"), fs = require("fs"), path = require("path");
const OUT = path.join(__dirname, "../img/help/"); fs.mkdirSync(OUT, {recursive: true});
const URL = process.env.URL || "http://localhost:8811/";
const ymd = d => d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
const badge = (p, list) => p.evaluate(list => { document.querySelectorAll(".hsbx").forEach(e => e.remove());
  list.forEach(([sel, n, dx, dy]) => { const e = document.querySelector(sel); if (!e) return; const r = e.getBoundingClientRect();
    const d = document.createElement("div"); d.className = "hsbx"; d.textContent = n;
    Object.assign(d.style, {position: "absolute", left: (r.left + scrollX + (dx == null ? -6 : dx)) + "px", top: (r.top + scrollY + (dy == null ? -8 : dy)) + "px", width: "22px", height: "22px", borderRadius: "50%", background: "#E0312B", color: "#fff", font: "700 13px/22px system-ui,sans-serif", textAlign: "center", zIndex: 99999, boxShadow: "0 1px 3px rgba(0,0,0,.35)"});
    document.documentElement.appendChild(d); const o = d.getBoundingClientRect(); d.style.top = (parseFloat(d.style.top) - (o.top - (r.top + (dy == null ? -8 : dy)))) + "px"; d.style.left = (parseFloat(d.style.left) - (o.left - (r.left + (dx == null ? -6 : dx)))) + "px"; }); }, list);
const rect = (p, sel, sel2, pad) => p.evaluate(([s, s2, pd]) => { const a = document.querySelector(s).getBoundingClientRect(), b = s2 ? document.querySelector(s2).getBoundingClientRect() : a;
  return {x: 0, y: Math.max(0, a.top + scrollY - pd), width: innerWidth, height: (b.bottom - a.top) + 2 * pd}; }, [sel, sel2, pad == null ? 10 : pad]);
async function shot(p, name, sfx, clip, maxH){ await p.waitForTimeout(500); if (maxH) clip.height = Math.min(clip.height, maxH);
  await p.screenshot({path: OUT + name + sfx, type: "jpeg", quality: 80, clip, fullPage: true}); console.log(name + sfx, Math.round(clip.height)); }
(async () => {
  const b = await chromium.launch();
  for (const theme of ["light", "dark"]){
    const sfx = theme === "dark" ? "-d.jpg" : ".jpg", t = new Date(), d = n => { const x = new Date(t); x.setDate(t.getDate() - n); return ymd(x); };
    const seed = {sel: {part: "P5", sub: "P5-K", mode: "dlg", bun: {"P5-K": "1-01-01"}, lastSub: {}},
      seen: {"1-01-01": d(2), "1-01-02": d(2), "1-01-03": d(1), "1-01-04": d(1), "1-01-05": d(0), "2-01-01": d(0), "2-01-02": d(0)}, days: [d(2), d(1), d(0)], td: {d: d(0), s: {"1-01-05": 1, "2-01-01": 1, "2-01-02": 1}, q: 1},
      wrong: {"1-01-01::ຂໍໂທດ": 1, "1-01-01::ຂອບໃຈ": 1}, star: {"1-01-01::ສະບາຍດີ": 1}, theme};
    const c = await b.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: theme});
    await c.route(/script\.google/, r => r.abort());
    await c.addInitScript(s => { try { if (sessionStorage.getItem("hs")) return; sessionStorage.setItem("hs", "1"); const L = localStorage;
      L.setItem("lao-sel", JSON.stringify(s.sel)); L.setItem("lao-seen", JSON.stringify(s.seen)); L.setItem("lao-days", JSON.stringify(s.days)); L.setItem("lao-td", JSON.stringify(s.td));
      L.setItem("lao-wrong", JSON.stringify(s.wrong)); L.setItem("lao-star", JSON.stringify(s.star)); L.setItem("lao-pref", JSON.stringify({theme: s.theme, fz: 1})); L.setItem("lao-survey", JSON.stringify({later: "2999-01-01"})); L.setItem("lao-snap", "null"); } catch (e) {} }, seed);
    const p = await c.newPage(); p.on("pageerror", e => console.log("ERR", e.message));
    await p.goto(URL); await p.waitForTimeout(3000);
    await p.addStyleTag({content: "#kbinfo,kbd.kc,#audwait,.stick{display:none!important}"});
    await shot(p, "mine", sfx, await rect(p, "#mine"));
    await badge(p, [["#groups .group[aria-pressed=true]", "1", -4, -6], ["#subs .sub[aria-selected=true]", "2", -4, -6]]);
    await shot(p, "menu", sfx, await rect(p, ".menubox"));
    await badge(p, [["#bsel", "3", -4, -6], [".tiptog", "4", -6, -8]]);
    await shot(p, "band", sfx, await rect(p, "#band"));
    await badge(p, []);
    await shot(p, "controls", sfx, await rect(p, "#controls"));
    await shot(p, "dlg", sfx, await rect(p, "#view .entry"), 520);
    await p.click("#m-cards"); await p.waitForTimeout(600);
    await shot(p, "cards", sfx, await rect(p, "#view .card"), 420);
    await p.click("#m-quiz"); await p.waitForTimeout(500);
    for (let i = 0; i < 12; i++){ const os = await p.$$("[data-opt]:not([disabled])"); if (!os.length) break;
      const right = await p.evaluate(() => { const q = S.quiz.qs[S.quiz.i]; return q.opts.indexOf(q.answer); }); await os[i % 3 === 2 ? (right + 1) % os.length : right].click(); await p.waitForTimeout(80);
      const n = await p.$("#next"); if (n) await n.click(); await p.waitForTimeout(80); }
    await p.waitForTimeout(900);
    await shot(p, "quizres", sfx, await rect(p, ".qend", ".qbtns"));
    await p.evaluate(() => { S.qkind = "rev"; S.quiz = null; S.wbOpen = true; render(); }); await p.waitForTimeout(500);
    await shot(p, "wbook", sfx, await rect(p, ".wbook"));
    await p.evaluate(() => document.getElementById("prefs").scrollIntoView({block: "center"}));
    await shot(p, "prefs", sfx, await rect(p, "#prefs", null, 5));
    await c.close();
  }
  await b.close();
})();
