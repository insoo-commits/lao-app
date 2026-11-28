/* core stick v1.0 (from kor-app; copy, do not edit here). Shared by PhasaKAO, JeyCampus, PhasaLAO.
   Edit only this master, raise the version, then run  node tools/core-copy.js  to copy it to the other apps.
   The menu bar that stays at the top while reading down (design A, RYU 2026-11-24; first in the hotel English app v1.51).
   Needs in the page: #stick (hidden) > … #stickG (empty nav), #stickT, #stickQ, and the page menu .menubox > #groups, .search, #q.
   It takes over exactly when the page menu row reaches the bar's menu row, in both directions (JeyCampus v1.31.23, RYU),
   checked on scroll once per frame. A tap on the bar's menu presses the same button in the page menu.
   The look (position, size, colour, no blur on iPad) is each app's own CSS, because the apps zoom the page differently.
   Per-app values from window.APPCFG.stick (app-config.js):
     title()  text for the bar's lesson line (#stickT)       watch  ids of more elements whose change refreshes the bar
     strip    attributes removed from the copied buttons      stop   true = taps on the bar do not reach the page's click handlers */
(function(){
  if (window.__stick) return; window.__stick = 1;
  var C = (window.APPCFG && window.APPCFG.stick) || {}, $ = function(id){ return document.getElementById(id); };
  var st = $("stick"), mb = document.querySelector(".menubox"), sg = $("stickG"), g = $("groups");
  if (!st || !mb || !sg || !g) return;
  var sync = function(){
    sg.innerHTML = g.innerHTML;
    sg.querySelectorAll(".glide").forEach(function(x){ x.remove(); });
    (C.strip || []).forEach(function(a){ sg.querySelectorAll("[" + a + "]").forEach(function(b){ b.removeAttribute(a); }); });
    var t = $("stickT"); if (t && C.title) t.textContent = C.title();
    var on = sg.querySelector('[aria-pressed="true"]'); if (on && !st.hidden) on.scrollIntoView({block: "nearest", inline: "center"});
  };
  var T = 8, raf = 0;
  var check = function(){ raf = 0; var show = g.getBoundingClientRect().top <= T + 0.5; if (show === !st.hidden) return; st.hidden = !show;
    if (show){ sync(); var r = st.querySelector(".groups"); if (r){ var t = r.getBoundingClientRect().top; if (t > 0 && t < 80) T = t; } } };
  addEventListener("scroll", function(){ if (!raf) raf = requestAnimationFrame(check); }, {passive: true});
  addEventListener("resize", function(){ st.hidden = true; T = 8; check(); });
  check();
  var re = function(){ if (!st.hidden) sync(); };
  new MutationObserver(re).observe(g, {childList: true, subtree: true, attributes: true});
  (C.watch || []).forEach(function(id){ var e = $(id); if (e) new MutationObserver(re).observe(e, {childList: true, subtree: true, characterData: true}); });
  sg.addEventListener("click", function(e){ var t = e.target.closest(".group"); if (!t) return; if (C.stop) e.stopPropagation();
    var i = [].indexOf.call(sg.querySelectorAll(".group"), t), o = g.querySelectorAll(".group")[i]; if (o) o.click();
    document.querySelector(".search").scrollIntoView({block: "start"}); });
  var q = $("stickQ"); if (q) q.addEventListener("click", function(e){ if (C.stop) e.stopPropagation(); window.scrollTo(0, 0); $("q").focus(); });
})();
