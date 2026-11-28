/* core prefs v1.0 (from kor-app; copy, do not edit here). Shared by PhasaKAO, JeyCampus, PhasaLAO.
   Edit only this master, raise the version, then run  node tools/core-copy.js  to copy it to the other apps.
   Screen theme (auto / light / dark) and text size (A− A A+ A++), kept on this device (KoJey v1.4, RYU).
   "auto" follows the phone's setting: no data-theme on <html>. Text size = the CSS variable --fz on <html>.
   The row of buttons goes in #prefs: two groups .pseg > .pbtns > button.pb(.on); the look is each app's own CSS.
   The app keeps its own saved values and calls once:
     PREFS.init({get: () => ({theme, fz}), set: (key, value) => save it, box: () => the #prefs element or null, after: () => re-fit text})
   then PREFS.apply() whenever the values changed elsewhere (the intro page). Labels from window.APPCFG.prefs (app-config.js):
     theme  the theme group's label     themes  [auto, light, dark] button texts     fz  the size group's label
     stop   true = a tap on these buttons does not reach the page's other click handlers */
(function(){
  if (window.PREFS) return;
  var C = (window.APPCFG && window.APPCFG.prefs) || {}, O = {};
  var SIZES = [[0.9, "A−"], [1, "A"], [1.15, "A+"], [1.3, "A++"]];
  var esc = function(s){ return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;"); };
  var seg = function(k, lab, opts, cur){
    return '<div class="pseg" role="group" aria-label="' + esc(lab) + '" title="' + esc(lab) + '"><div class="pbtns">' + opts.map(function(o){
      var on = String(cur) === String(o[0]);
      return '<button type="button" class="pb' + (on ? " on" : "") + '" data-pref="' + k + '" data-v="' + o[0] + '" aria-pressed="' + on + '">' + esc(o[1]) + "</button>"; }).join("") + "</div></div>"; };
  function apply(){
    if (!O.get) return;
    var p = O.get() || {}, th = p.theme || "auto", fz = p.fz || 1, r = document.documentElement;
    if (th === "light" || th === "dark") r.setAttribute("data-theme", th); else r.removeAttribute("data-theme");
    r.style.setProperty("--fz", String(fz));
    var box = O.box && O.box(); if (!box) return;
    var t = C.themes || ["Auto", "☀ Light", "☾ Dark"];
    box.innerHTML = seg("theme", C.theme || "Theme", [["auto", t[0]], ["light", t[1]], ["dark", t[2]]], th) + seg("fz", C.fz || "Text size", SIZES, fz);
  }
  document.addEventListener("click", function(e){
    var b = e.target.closest && e.target.closest("#prefs [data-pref]"); if (!b || !O.set) return;
    if (C.stop) e.stopPropagation();
    var k = b.getAttribute("data-pref"), v = b.getAttribute("data-v");
    O.set(k, k === "fz" ? +v : v); apply(); if (O.after) try { O.after(); } catch (_) {}
  }, true);
  window.PREFS = {init: function(o){ O = o || {}; apply(); }, apply: apply};
})();
