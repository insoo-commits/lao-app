/* PhasaLAO intro: first screen with study settings, install help and downloads (ported from PhasaKAO src/intro.js) */
(() => {
const URL_APP = "phasalao.pages.dev";
/* the app's 10 menus: [code, tile text, Korean name, what is inside] (app.js PARTS + poster) */
const MENUS = [["P5","인사","기초회화","인사·식당·시장·교통…"],["P8","ກຂ","문자학습","자음·모음·받침·성조"],["P3","어순","문장규칙","어순·부정·시제·분류사"],["P1","짝","짝말비교","반대말·짝을 이루는 말"],["P2","≈","비슷한말","뜻이 비슷해 헷갈리는 말"],
  ["P4","가족","단어가족","같은 뿌리에서 넓혀 가기"],["P6","발음","발음구별","성조·긴 모음·된소리"],["P7","듣기","듣기연습","대화·이야기 듣고 풀기"],["P9","ລາວ","라오스","나라·문화 읽을거리"],["PH","?","도움말","앱 사용법 전체"]];
const LEARN = 8;
const x = {
 hello:"ສະບາຍດີ! 싸바이디!", losub:"라오스어, 주제별로 공부하기",
 lead:"인사부터 식당·시장·교통까지 주제별 묶음으로 배워요. 원어민 라오어 음성과 한글 독음, 한국어 뜻이 함께 나오고, 짝말·비슷한말·발음·듣기 연습과 라오스 이야기까지 담았어요.",
 st:["묶음","단어","문장","학습자"], free:"무료",
 s1:"재생 설정", s1n:"공부하는 중에도 언제든 바꿀 수 있어요. 앱이 기억해요.",
 pass:"나의 학습 설정", rep:"반복", spd:"배속", vol:"음량", voice:"한국어 음성", voiceN:"라오어 → 한국어 뜻 → 라오어",
 theme:"화면", th:["자동","밝게","어둡게"], fz:"글자 크기", listen:"들어 보기",
 start:"시작하기", how:"설치 방법",
 s2:"공부 방법", s2n:"묶음마다 세 가지로 공부해요.", h3:[["예문보기","듣고 따라 말하기","main"],["단어공부","낱말카드·성조 색","happy"],["확인퀴즈","4지선다로 확인","think"]], h3k:["S","W","E"],
 inside:"메뉴", learn:"라오어 공부", live:"라오스와 도움말",
 it:"PhasaLAO를 홈 화면에 설치", itn:"앱처럼 화면 가득 열리고, 음성을 저장하면 인터넷 없이도 들을 수 있어요. 앱스토어는 필요 없어요.", det:"지금 쓰는 기기",
 dlt:"내려받기", dla:"앱 설치", dlad:"홈 화면 아이콘으로 바로 열어요.", inst:"설치", seehow:"방법 보기",
 dlv:"음성 전체 저장", dlvd:"라오어 + 한국어 뜻 음성, 약 260MB. 와이파이에서 받으세요.", save:"저장",
 dlp:"사용 안내 포스터", dlpd:"A4 한 장. 주변에 소개해 주세요.", dl:"받기",
 qr:"휴대폰으로 열기", qrd:"휴대폰 카메라로 찍으면 바로 열려요.", copy:"복사", copied:"주소를 복사했어요",
 foot:"라오스어를 배우는 모든 분께 무료로.",
 steps:{ios:["Safari로 이 페이지를 열어요.","아래쪽 공유 단추 {share} 를 눌러요.","아래로 내려 ‘홈 화면에 추가’를 골라요.","‘추가’를 누르면 홈 화면에 PhasaLAO가 생겨요."],
  android:["아래 ‘설치’를 눌러요.","안 보이면 Chrome 메뉴 {dots} 에서 ‘앱 설치’를 골라요.","‘설치’를 누르고 홈 화면에서 PhasaLAO를 열어요."],
  ipad:["Safari로 이 페이지를 열어요.","오른쪽 위 공유 단추 {share} 를 눌러요.","‘홈 화면에 추가’ → ‘추가’를 눌러요."],
  chrome:["Chrome이나 Edge 주소창 끝의 설치 아이콘 {inst} 을 눌러요.","‘설치’를 누르면 PhasaLAO가 자기 창으로 열리고 바탕화면 바로가기가 생겨요."],
  safari:["Mac의 Safari에서 ‘파일’ 메뉴를 열어요.","‘Dock에 추가’ → ‘추가’를 눌러요."]}
};
const LO = {s1:"ຕັ້ງຄ່າ",s2:"ວິທີຮຽນ",inside:"ເມນູ",it:"ຕິດຕັ້ງ",pass:"ຂອງຂ້ອຍ"};
const ICON = {
 play:'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15l13-7.5z"/></svg>',
 stop:'<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>',
 arrow:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 share:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M8 7l4-4 4 4"/><path d="M6 11H5v10h14V11h-1"/></svg>',
 inst:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M12 8v6M9 11l3 3 3-3"/></svg>',
 dots:'<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>',
 audio:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 14v-2a9 9 0 0 1 18 0v2"/><rect x="3" y="14" width="4" height="7" rx="1.5"/><rect x="17" y="14" width="4" height="7" rx="1.5"/></svg>',
 phone:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><rect x="7" y="3" width="10" height="18" rx="2.5"/></svg>',
 pc:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8"/></svg>'
};


/* the device: install steps for it are shown first */
const ua = navigator.userAgent || "";
const isIPad = /iPad/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
const REAL = isIPad ? "ipad" : /iPhone|iPod/.test(ua) ? "ios" : /Android/.test(ua) ? (/Mobile/.test(ua) ? "android" : "atab") : /Mac/.test(ua) ? "mac" : "pc";
const os = {phone: REAL === "android" ? "android" : "ios", pad: REAL === "atab" ? "atab" : "ipad", pc: REAL === "mac" ? "safari" : "chrome"};
const standalone = (window.matchMedia && matchMedia("(display-mode: standalone)").matches) || navigator.standalone === true;
let bip = null;   // Chrome/Edge/Android install prompt
window.addEventListener("beforeinstallprompt", e => { e.preventDefault(); bip = e; });

const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const kb = s => esc(s).replace(/\{(share|inst|dots)\}/g, (m, k) => '<span class="kbd">' + ICON[k] + '</span>');
/* the app's own settings (app.js globals): REP, RATE, SAYKO, PREF */
const rep = () => String(REP), rate = () => String(RATE), voice = () => !!SAYKO, theme = () => PREF.theme || "auto", fz = () => PREF.fz || 1;
function isDark(){ const th = theme(); if (th === "dark") return true; if (th === "light") return false; return !!(window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches); }
function devOf(){ const w = window.innerWidth; return w < 700 ? "phone" : w < 1100 ? "pad" : "pc"; }
/* numbers as the header shows them */
function counts(){ const n = [...document.querySelectorAll("#app header .stats b")].map(b => b.textContent.trim()); return [n[0] || "735", n[1] || "4,506", n[2] || "16,889", String(PARTS.length)]; }
function ver(){ const v = document.querySelector(".ver"), m = v && /v[\d.]+/.exec(v.textContent); return m ? m[0] : ""; }

function heroCopy(){ const c = counts(); return `
  <span class="badge"><img src="icon-192.png" alt="">PhasaLAO</span>
  <h1 lang="lo">ຮຽນ ພາສາລາວ</h1>
  <p class="losub">${esc(x.losub)}</p>
  <p class="lead">${esc(x.lead)}</p>
  <div class="stats">${c.slice(0, 3).map((n, i) => `<div><b>${esc(n)}</b><span>${x.st[i]}</span></div>`).join("")}<div><b data-learners>${learners()}</b><span>${x.st[3]}</span></div></div>`; }

/* RYU 2026-11-28: "메뉴" out, "학습자" last = devices counted by the anonymous stats (same number as 도움말 > 통계), from the saved copy at once, then refreshed once per visit */
let LRN = null, LRNF = false;
const lfmt = n => Number(n).toLocaleString("en-US");
function learners(){ if (LRN == null){ try { const d = JSON.parse(localStorage.getItem("lao-statspage") || "null"); if (d && d.totals && d.totals.devices) LRN = +d.totals.devices; } catch (e) {} getLearners(); } return LRN ? lfmt(LRN) : "–"; }
function getLearners(){ if (LRNF) return; LRNF = true; try { if (typeof STATS_URL === "undefined" || !STATS_URL || !navigator.onLine) return;
  fetch(STATS_URL + "?stats=1", {cache: "no-store"}).then(r => r.json()).then(d => { if (!d || !d.totals) return; try { localStorage.setItem("lao-statspage", JSON.stringify(d)); } catch (e) {}
    if (d.totals.devices){ LRN = +d.totals.devices; document.querySelectorAll("#intro [data-learners]").forEach(b => { b.textContent = lfmt(LRN); }); } }).catch(() => {}); } catch (e) {} }
function brand(){ return `<div class="brand"><img src="icon-192.png" alt=""><div><b>PhasaLAO</b><span class="lo">ພາສາລາວ</span></div></div>`; }
function free(long){ return `<span class="freepill"><i></i>${x.free}${long ? ` · <span class="lo">ສະບາຍດີ</span>` : ""}</span>`; }
function step(n, k, note){ return `<div class="sh">${n ? `<span class="n">${n}</span>` : ""}<div><h2>${esc(x[k])}${LO[k] ? ` <span class="kosub lo">${LO[k]}</span>` : ""}</h2>${note ? `<p>${esc(x[note])}</p>` : ""}</div></div>`; }
function seg(name, opts, cur, cls){ return `<div class="seg${cls ? " " + cls : ""}" role="group">${opts.map(([v, l]) => `<button type="button" data-${name}="${v}" class="${String(v) === String(cur) ? "on" : ""}" aria-pressed="${String(v) === String(cur)}">${esc(l)}</button>`).join("")}</div>`; }
function pass(withCta){
  return `<div class="pass">
  <div class="passhead"><span class="ph"><img src="img/ele/main.webp" alt=""></span><div><div class="pt">PHASALAO PASS</div><div class="pn">${esc(x.pass)}<small class="lo">ການຮຽນ${LO.pass}</small></div></div><div class="pid">KOR · <span class="lo">ລາວ</span><br>${new Date().getFullYear()}</div></div>
  <div class="scarf"></div>
  <div class="passbody">
   <div class="row"><div class="lab">${esc(x.rep)}<small>문장마다 몇 번 들을지</small></div>${seg("rep", [1,2,3,4,5].map(n => [n, n + "회"]), rep())}</div>
   <div class="row full"><div class="rate"><div class="lab">${esc(x.spd)}<small>느리게 · 빠르게</small></div><div class="rtrack"><input type="range" min="0.7" max="2" step="0.1" value="${rate()}" data-rate aria-label="${esc(x.spd)}"><div class="ticks" aria-hidden="true">${[0.7, 1, 1.5, 2].map(v => `<span style="left:${((v - 0.7) / 1.3 * 100).toFixed(2)}%">${v.toFixed(1)}</span>`).join("")}</div></div><output>×${(+rate()).toFixed(1)}</output></div></div>
   <div class="row full">${window.AVOL && AVOL.row ? AVOL.row(x.vol) : ""}</div>
   <div class="row"><div class="lab">${esc(x.voice)}<small>${esc(x.voiceN)}</small></div><button type="button" class="sw${voice() ? " on" : ""}" data-voice role="switch" aria-checked="${voice()}" aria-label="${esc(x.voice)}"></button></div>
   <div class="row"><div class="lab">${esc(x.theme)}<small>밝은 화면 · 어두운 화면</small></div>${seg("theme", [["auto", x.th[0]], ["light", x.th[1]], ["dark", x.th[2]]], theme(), "txt")}</div>
   <div class="row"><div class="lab">${esc(x.fz)}<small>읽기 편한 크기로</small></div>${seg("fz", [[0.9, "A−"], [1, "A"], [1.15, "A+"], [1.3, "A++"]], fz())}</div>
   <div class="sample"><button type="button" class="play" data-act="sample" aria-label="${esc(x.listen)}">${playing ? ICON.stop : ICON.play}</button><div><div class="s1 lo">${esc(SAMPLE_LO)}</div><div class="s2">${esc(SAMPLE_RD)} · ${esc(SAMPLE_KO)}</div></div><div class="s3">${rep()}회 · ×${(+rate()).toFixed(1)}<br>${esc(x.listen)}</div></div>
  </div>
  ${withCta ? `<div class="passcta">${cta()}</div>` : ""}
  <div class="passfoot">${esc(x.s1n)}</div>
 </div>`; }
function how3(){ return `<div class="how3">${x.h3.map((h, i) => `<div class="hstep"><span class="k">${x.h3k[i]}</span><img src="img/ele/${h[2]}.webp" alt=""><b>${esc(h[0])}</b><small>${esc(h[1])}</small></div>`).join("")}</div>`; }
function menus(){ const tile = (m, i) => `<button type="button" class="mt${i >= LEARN ? " live" : ""}" data-area="${m[0]}"><span class="g${/[຀-໿]/.test(m[1]) ? " lo" : ""}">${esc(m[1])}</span><span class="t"><b>${esc(m[2])}</b><small>${esc(m[3])}</small></span></button>`;
  return `<div class="menus"><div class="mgl">${esc(x.learn)}</div>${MENUS.slice(0, LEARN).map(tile).join("")}<div class="mgl">${esc(x.live)}</div>${MENUS.slice(LEARN).map((m, i) => tile(m, i + LEARN)).join("")}</div>`; }
function osTabs(dev){ const o = dev === "phone" ? [["ios","iPhone"],["android","Android"]] : dev === "pad" ? [["ipad","iPad"],["atab","Android"]] : [["chrome","Chrome · Edge"],["safari","Mac Safari"]];
  return `<div class="otabs" role="group">${o.map(([k, l]) => `<button type="button" data-os="${dev}:${k}" class="${os[dev] === k ? "on" : ""}">${l}</button>`).join("")}</div>`; }
function steps(dev){ const k = os[dev] === "atab" ? "android" : os[dev]; return `<ol class="steps">${x.steps[k].map(s => `<li><span>${kb(s)}</span></li>`).join("")}</ol>`; }
function detectChip(dev){ const name = {phone:{ios:"iPhone · Safari",android:"Android · Chrome"},pad:{ipad:"iPad · Safari",atab:"Android 태블릿"},pc:{chrome:"PC · Chrome/Edge",safari:"Mac · Safari"}}[dev][os[dev]];
  return `<span class="detect"><i>${dev === "pc" ? ICON.pc : ICON.phone}</i>${esc(x.det)}: <b>${name}</b></span>`; }
function downloads(dev){ const ios = (dev === "phone" && os.phone === "ios") || (dev === "pad" && os.pad === "ipad") || (dev === "pc" && os.pc === "safari");
  const hasAudio = !!document.querySelector(".dlp a.dla");
  return `<div class="dls">
   <div class="dl"><span class="ic"><img src="icon-192.png" alt=""></span><span class="tx"><b>${esc(x.dla)}</b><small>${esc(x.dlad)}</small></span>${standalone ? '<span class="go y">✓</span>' : `<button type="button" class="go y" data-act="${ios ? "how" : "install"}">${esc(ios ? x.seehow : x.inst)}</button>`}</div>
   ${hasAudio ? `<div class="dl"><span class="ic">${ICON.audio}</span><span class="tx"><b>${esc(x.dlv)}</b><small>${esc(x.dlvd)}</small><small class="dlmsg" data-dlmsg></small></span><button type="button" class="go" data-act="audio">${esc(x.save)}</button></div>` : ""}
   <div class="dl"><span class="ic"><img class="pst" src="img/poster.webp" alt=""></span><span class="tx"><b>${esc(x.dlp)}</b><small>${esc(x.dlpd)}</small></span><a class="go" href="img/poster.webp" download="PhasaLAO-poster.webp">${esc(x.dl)}</a></div>
  </div>`; }
function addr(){ return `<div class="addr">${URL_APP}<button type="button" data-act="copy">${esc(x.copy)}</button></div>`; }
function foot(pic){ return `<div class="foot">${pic ? `<img src="img/ele/try.webp" alt="">` : ""}<div><b>PhasaLAO</b> · <span class="lo">ຮຽນ ພາສາລາວ</span><div>${esc(x.foot)}</div><div>${URL_APP} · ${esc(ver())} · Copyleft</div></div></div>`; }
function cta(){ return `<button type="button" class="btn pri" data-act="start">${esc(x.start)} ${ICON.arrow}</button>`; }
function howBtn(cls){ return `<button type="button" class="btn ${cls}" data-act="how">${esc(x.how)}</button>`; }

/* ---- the three layouts (RYU's own photos in img/intro/) ---- */
function phone(){ return `
 <div class="hero"><img class="bg" src="img/intro/thatluang.jpg" alt="">
  <div class="top">${brand()}${free(false)}</div>
  <div class="copy">${heroCopy()}</div></div>
 <div class="sec">${step(1, "s1")}${pass(false)}</div>
 <div class="sec">${step(2, "s2", "s2n")}${how3()}</div>
 <div class="sec"><div class="sh"><div><h2>${esc(x.inside)} <span class="kosub lo">${LO.inside}</span></h2></div></div>${menus()}</div>
 <div class="inst"><img class="bg" src="img/intro/sunset.jpg" alt="">
  ${detectChip("phone")}<h2>${esc(x.it)}</h2><p style="margin:0;opacity:.85;font-size:.88em">${esc(x.itn)}</p>
  ${osTabs("phone")}${steps("phone")}${downloads("phone")}${addr()}</div>
 ${foot(true)}
 <div class="sticky">${cta()}</div>`; }
function pad(){ return `
 <div class="hero"><img class="bg" src="img/intro/nightmarket.jpg" alt="">
  <div class="top">${brand()}${free(true)}</div>
  <div class="copy">${heroCopy()}</div></div>
 <div class="wrap">
  <div class="duo">
   <div class="lcard">${step(0, "s2", "s2n")}${how3()}</div>
   ${pass(false)}
  </div>
  <div class="ctarow" style="margin-top:-8px">${howBtn("sec")}${cta()}</div>
  <div style="display:grid;gap:12px"><h2 style="font-size:1.25em">${esc(x.inside)} <span class="kosub lo">${LO.inside}</span></h2>${menus()}</div>
 </div>
 <div class="inst"><img class="bg" src="img/intro/sunset.jpg" alt="">
  <div style="display:grid;gap:14px;align-content:start">${detectChip("pad")}<h2 style="font-size:1.4em">${esc(x.it)}</h2><p style="margin:0;opacity:.85;font-size:.9em">${esc(x.itn)}</p>${osTabs("pad")}${steps("pad")}</div>
  <div style="display:grid;gap:12px;align-content:start"><h3 style="font-size:1em;opacity:.9">${esc(x.dlt)}</h3>${downloads("pad")}${addr()}</div>
 </div>
 <div class="frow">${foot(false)}<img src="img/ele/happy.webp" alt="" class="frpic"></div>`; }
function pc(){ return `
 <div class="hero"><img class="bg" src="img/intro/nongkhiaw.jpg" alt=""><span class="glow2"></span>
  <div class="nav">${brand()}${[0, 1, 8, 9].map(i => `<a href="#" data-area="${MENUS[i][0]}">${esc(MENUS[i][2])}</a>`).join("")}<span class="sp"></span>${free(true)}${cta()}</div>
  <div class="hgrid">
   <div class="copy">${heroCopy()}<div class="cta">${cta()}${howBtn("ghost")}</div></div>
   <div class="passwrap"><img class="elep" src="img/ele/main.webp" alt="">${pass(true)}</div>
  </div></div>
 <div class="band">
  <div style="display:grid;gap:14px;align-content:start"><h2>${esc(x.s2)} <span class="kosub lo">${LO.s2}</span></h2><p style="margin:0;color:var(--mm);font-size:.92em">${esc(x.s2n)} ${esc(x.s1n)}</p>${how3()}</div>
  <div><h2 style="margin-bottom:12px">${esc(x.inside)} <span class="kosub lo">${LO.inside}</span></h2>${menus()}<div class="gal"><img src="img/intro/patuxai.jpg" alt="빠뚜싸이 분수"><img src="img/intro/koreandept.jpg" alt="한국어학과"><img src="img/la/alms.jpg" alt="탁발"></div></div>
 </div>
 <div class="inst"><img class="bg" src="img/intro/sunset.jpg" alt="">
  <div style="display:grid;gap:14px;align-content:start">${detectChip("pc")}<h2 style="font-size:1.5em">${esc(x.it)}</h2><p style="margin:0;opacity:.85;font-size:.92em">${esc(x.itn)}</p>${osTabs("pc")}${steps("pc")}</div>
  <div style="display:grid;gap:12px;align-content:start;justify-items:start"><h3 style="font-size:1em">${esc(x.qr)}</h3><div class="qrbox"><img src="img/qr.svg" alt="QR ${URL_APP}"></div><p style="margin:0;opacity:.85;font-size:.85em">${esc(x.qrd)}</p>${addr()}</div>
  <div style="display:grid;gap:12px;align-content:start"><h3 style="font-size:1em;opacity:.9">${esc(x.dlt)}</h3>${downloads("pc")}</div>
 </div>
 <div class="frow">${foot(false)}<img src="img/ele/happy.webp" alt="" class="frpic"></div>`; }

/* ---- show, redraw, close ---- */
let box = null, curDev = null;
function render(){
  if (!box) return;
  const d = devOf(), y = box.scrollTop;
  box.className = "m " + (d === "phone" ? "P" : d === "pad" ? "T" : "D") + (isDark() ? " dk" : "");
  box.style.setProperty("--fz", fz());
  box.innerHTML = '<div class="wrapin">' + (d === "phone" ? phone() : d === "pad" ? pad() : pc()) + "</div>";
  box.scrollTop = d === curDev ? y : 0; curDev = d;
  mirrorDl();
}
function open(){
  if (box) return;
  try { if (P.active) stopPlay(); } catch (e) {}
  box = document.createElement("div"); box.id = "intro"; box.lang = "ko"; box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "PhasaLAO");
  document.body.appendChild(box); document.documentElement.classList.add("introon");
  render();
  try { sessionStorage.setItem("pl-intro", "open"); } catch (e) {}   // a refresh keeps the intro
}
function close(){
  stopSample();
  try { sessionStorage.setItem("pl-intro", "closed"); } catch (e) {}   // a refresh keeps the main screen
  if (box){ box.remove(); box = null; } document.documentElement.classList.remove("introon");
}
let rT = 0;
window.addEventListener("resize", () => { clearTimeout(rT); rT = setTimeout(() => { if (box && devOf() !== curDev) render(); }, 150); });
if (window.matchMedia) { const mq = matchMedia("(prefers-color-scheme: dark)"); if (mq.addEventListener) mq.addEventListener("change", () => { if (box && theme() === "auto") render(); }); }

function setRep(v){ REP = +v; store.set("lao-rep", REP); const e = document.getElementById("repSel"); if (e) e.value = String(REP); try { showPlayer(); } catch (x) {} }
function setRate(v){ RATE = +v; store.set("lao-rate", RATE); const e = document.getElementById("rateSel"); if (e) e.value = String(RATE); try { if (AEL) AEL.playbackRate = RATE; } catch (x) {} }
function setPref(k, v){ PREF[k] = v; store.set("lao-pref", PREF); applyPrefs(); }

/* sample: the first line of 1-01-01 with the app's own recordings: Lao (repeat × at the chosen speed), the Korean meaning once after the first when 한국어 음성 is on */
const SAMPLE_LO = "ສະບາຍດີ ສະບາຍດີບໍ?", SAMPLE_RD = "싸바이디, 싸바이디 버?", SAMPLE_KO = "안녕하세요, 잘 지내요?";
let RUN = 0;   // each play has its own number: a stopped play never wakes up and talks over a new one (RYU 2026-11-27, as JeyCampus v1.30.6)
let playing = false, IA = null;
function stopSample(){ RUN++; if (playing){ playing = false; try { IA && IA.pause(); } catch (e) {} } }
function playClip(text, ko){ const me = RUN; return new Promise(res => { let k = null; try { k = keyOf({text, ko}); } catch (e) {} if (!k){ res(); return; }
  blobUrl(k).then(u => { if (!playing || RUN !== me){ res(); return; } IA = IA || new Audio(); IA.src = u; IA.playbackRate = ko ? 1 : RATE; try { IA.preservesPitch = true; } catch (e) {}
    IA.onended = IA.onerror = () => res(); const p = IA.play(); if (p && p.catch) p.catch(() => res()); }, () => res()); }); }
async function sample(){
  if (playing){ stopSample(); render(); return; }
  try { if (P.active) stopPlay(); } catch (e) {}
  const me = ++RUN, on = () => playing && RUN === me;
  playing = true; render(); const n = +rep() || 1;
  for (let i = 0; i < n && on(); i++){
    await playClip(SAMPLE_LO, false);
    if (i === 0 && voice() && on()) await playClip(SAMPLE_KO, true);
    if (on()) await new Promise(r => setTimeout(r, 350));
  }
  if (RUN === me){ playing = false; render(); }
}
function toast(msg){ if (!box) return; const el = document.createElement("div"); el.className = "toast"; el.textContent = msg; box.appendChild(el); setTimeout(() => el.remove(), 2200); }
/* the app's own "음성 mp3 내려받기" link does the work; its progress text is copied here */
function mirrorDl(){ const src = document.querySelector(".dlp .dls"), dst = box && box.querySelector("[data-dlmsg]"); if (src && dst) dst.textContent = src.textContent; }
{ const src = document.querySelector(".dlp .dls"); if (src && window.MutationObserver) new MutationObserver(mirrorDl).observe(src, {childList: true, characterData: true, subtree: true}); }
function goArea(a){ const b = document.querySelector('#groups [data-g="' + a + '"]'); close(); if (b) b.click(); setTimeout(() => scrollTo(0, 0), 80); }

document.addEventListener("click", ev => {
  if (!box || !box.contains(ev.target)) return;
  const b = ev.target.closest("button,a"); if (!b || b.disabled) return;
  if (b.dataset.rep){ setRep(b.dataset.rep); render(); return; }
  if (b.dataset.theme){ setPref("theme", b.dataset.theme); render(); return; }
  if (b.dataset.fz){ setPref("fz", +b.dataset.fz); render(); return; }
  if (b.hasAttribute("data-voice")){ setSayKo(!voice()); render(); return; }
  if (b.dataset.os){ const [d, k] = b.dataset.os.split(":"); os[d] = k; render(); return; }
  if (b.dataset.area){ ev.preventDefault(); goArea(b.dataset.area); return; }
  const a = b.dataset.act; if (!a) return;
  ev.preventDefault();
  if (a === "start") close();
  else if (a === "sample") sample();
  else if (a === "copy"){ const done = () => toast(x.copied); try { navigator.clipboard.writeText("https://" + URL_APP + "/").then(done, done); } catch (e) { done(); } }
  else if (a === "install"){ if (bip){ bip.prompt(); bip.userChoice.then(() => { bip = null; }, () => {}); } else { const el = box.querySelector(".steps"); if (el) el.scrollIntoView({behavior: "smooth", block: "center"}); } }
  else if (a === "audio"){ const d = document.querySelector(".dlp a.dla"); if (d) d.click(); }
  else if (a === "how"){ const el = box.querySelector(".steps"); if (el) el.scrollIntoView({behavior: "smooth", block: "center"}); }
});
/* volume (RYU 2026-11-27): the slider row and its handler are the shared part core/vol.js (window.AVOL.row) */
document.addEventListener("input", ev => { if (box && ev.target.matches("#intro [data-rate]")){ const v = (+ev.target.value).toFixed(1).replace(/\.0$/, ""); setRate(v); const o = ev.target.closest(".rate").querySelector("output"); if (o) o.textContent = "×" + (+v).toFixed(1); } });
document.addEventListener("change", ev => { if (box && ev.target.matches("#intro [data-rate]")) render(); });
/* while the intro is open, the app's keys stay off; Esc closes it */
document.addEventListener("keydown", ev => { if (!box) return; if (ev.key === "Escape") close(); else if (!/^(Tab|Enter| )$/.test(ev.key) && !ev.target.closest("#intro input")) ev.stopImmediatePropagation(); }, true);

/* a way back: a button under the theme row (applyPrefs only refills #prefs, so the line after it stays) */
{ const pf = document.getElementById("prefs"); if (pf && !document.querySelector(".introline")){ const p = document.createElement("p"); p.className = "introline";
  const b = document.createElement("button"); b.type = "button"; b.className = "pb"; b.innerHTML = '<img src="icon-192.png" alt="" style="width:18px;height:18px;border-radius:5px;vertical-align:-4px"> PhasaLAO 첫 화면';
  b.addEventListener("click", open); p.appendChild(b); pf.after(p); } }

/* open: no bundle link in the address and not yet closed in this visit; a refresh keeps whichever screen was showing (v4.48, like PhasaKAO) */
let st = null; try { st = sessionStorage.getItem("pl-intro"); } catch (e) {}
if (st === "open" || (location.hash.length <= 1 && st !== "closed")) open();
window.PL_INTRO = open;
})();
