/* core menu v1.0 (from kor-app; copy, do not edit here). Shared by PhasaKAO, JeyCampus, PhasaLAO.
   Edit only this master, raise the version, then run  node tools/core-copy.js  to copy it to the other apps.
   Helpers for the sideways menu rows #groups, #subs and the sticky bar's #stickG, on a computer with a mouse only
   (hotel English app v1.55-v1.57, RYU 2026-11-24):
   - glide: a soft pill with a line under it slides along #groups / #stickG after the mouse;
   - arrows: a row that does not fit gets a round arrow button at the end that has more (wrapped in div.hs), and the
     mouse wheel moves the row sideways too.
   The look is each app's own CSS (.glide, .hs, .hsb). Per-app values from window.APPCFG.menu (app-config.js):
     follow  true = when the pressed menu button changes, the row scrolls just enough to show it
     stop    true = a tap on an arrow does not reach the page's other click handlers */
(function(){
  if (window.__menu) return; window.__menu = 1;
  if (!matchMedia("(hover:hover) and (pointer:fine)").matches) return;
  var C = (window.APPCFG && window.APPCFG.menu) || {}, $ = function(id){ return document.getElementById(id); };
  var mk = function(tag, cls){ var e = document.createElement(tag); e.className = cls; return e; };
  ["groups", "stickG"].forEach(function(id){ var nav = $(id); if (!nav) return;
    var gl = function(){ var e = nav.querySelector(".glide"); if (!e){ e = mk("span", "glide"); e.setAttribute("aria-hidden", "true"); nav.appendChild(e); } return e; };
    var at = function(e, t){ e.style.left = t.offsetLeft + "px"; e.style.width = t.offsetWidth + "px"; e.style.top = t.offsetTop + "px"; e.style.height = t.offsetHeight + "px"; };
    nav.addEventListener("mouseover", function(ev){ var t = ev.target.closest(".group"); if (!t || !nav.contains(t)) return; var e = gl();
      if (e.style.opacity !== "1"){ e.style.transition = "none"; at(e, t); e.offsetWidth; e.style.transition = ""; }
      at(e, t); e.style.opacity = "1"; });
    nav.addEventListener("mouseleave", function(){ var e = nav.querySelector(".glide"); if (e) e.style.opacity = "0"; });
  });
  var chev = function(d){ var b = mk("button", "hsb " + (d < 0 ? "l" : "r")); b.type = "button"; b.setAttribute("aria-label", d < 0 ? "왼쪽 메뉴 보기" : "오른쪽 메뉴 보기"); b.hidden = true;
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + (d < 0 ? "m15 5-7 7 7 7" : "m9 5 7 7-7 7") + '"/></svg>'; return b; };
  ["groups", "subs", "stickG"].forEach(function(id){ var nav = $(id); if (!nav) return;
    var w = mk("div", "hs"); nav.parentNode.insertBefore(w, nav); w.appendChild(nav);
    var l = chev(-1), r = chev(1); w.append(l, r);
    var upd = function(){ var m = nav.scrollWidth - nav.clientWidth, x = nav.scrollLeft; l.hidden = !(m > 2 && x > 2); r.hidden = !(m > 2 && x < m - 2); w.classList.toggle("ml", !l.hidden); w.classList.toggle("mr", !r.hidden); };
    var mv = function(d){ nav.scrollBy({left: d * Math.max(120, nav.clientWidth * .6), behavior: "smooth"}); };
    l.addEventListener("click", function(e){ if (C.stop) e.stopPropagation(); mv(-1); }); r.addEventListener("click", function(e){ if (C.stop) e.stopPropagation(); mv(1); });
    nav.addEventListener("scroll", upd, {passive: true});
    nav.addEventListener("wheel", function(e){ if (nav.scrollWidth - nav.clientWidth < 3 || Math.abs(e.deltaY) <= Math.abs(e.deltaX)) return; e.preventDefault(); nav.scrollLeft += e.deltaY; }, {passive: false});
    addEventListener("resize", upd);
    var show = !C.follow ? upd : function(){ var t = nav.querySelector('[aria-pressed="true"],[aria-selected="true"]');
      if (t){ var a = t.offsetLeft - 40, z = t.offsetLeft + t.offsetWidth + 40 - nav.clientWidth; if (nav.scrollLeft > a) nav.scrollLeft = Math.max(0, a); else if (nav.scrollLeft < z) nav.scrollLeft = z; } upd(); };
    new MutationObserver(function(){ requestAnimationFrame(show); }).observe(nav, {childList: true, subtree: true, attributes: true, attributeFilter: ["aria-pressed", "aria-selected"]});
    if (C.follow) requestAnimationFrame(show);
    if ("ResizeObserver" in window) new ResizeObserver(upd).observe(nav);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(upd);
    upd();
  });
})();
