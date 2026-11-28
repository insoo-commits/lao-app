/* core ptr v1.0 (from kor-app; copy, do not edit here). Shared by PhasaKAO, JeyCampus, PhasaLAO.
   Edit only this master, raise the version, then run  node tools/core-copy.js  to copy it to the other apps.
   Pull to refresh (RYU 2026-11-27): on phones and tablets, pull down from the very top of the page and let go to reload
   (also in the installed home-screen app). The service worker is asked for an update first (at most 1.5 s).
   Per-app values from window.APPCFG.ptr (app-config.js): bg = the round button's colour, go = its colour once pulled far enough. */
(function(){
  if(window.__ptr)return;window.__ptr=1;
  var C=(window.APPCFG&&window.APPCFG.ptr)||{};
  if(!("ontouchstart" in window)&&!(navigator.maxTouchPoints>0))return;
  var TH=70,MAX=110,de=document.documentElement;
  var css=document.createElement("style");
  css.textContent="html,body{overscroll-behavior-y:contain}"+
   "#ptr{position:fixed;left:50%;top:0;z-index:2147483000;width:40px;height:40px;margin-left:-20px;border-radius:50%;"+
   "background:"+C.bg+";color:#fff;display:flex;align-items:center;justify-content:center;"+
   "box-shadow:0 2px 10px rgba(0,0,0,.25);transform:translateY(-52px);opacity:0;pointer-events:none}"+
   "#ptr svg{width:22px;height:22px;transition:transform .15s}#ptr.go{background:"+C.go+"}"+
   "#ptr.spin svg{animation:ptrs .8s linear infinite}@keyframes ptrs{to{transform:rotate(360deg)}}";
  (document.head||de).appendChild(css);
  var el=null;
  function mk(){if(el)return el;el=document.createElement("div");el.id="ptr";el.setAttribute("aria-hidden","true");
   el.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12a8 8 0 1 1-2.34-5.66"/><path d="M20 4v5h-5"/></svg>';
   document.body.appendChild(el);return el}
  function top0(){return (window.scrollY||de.scrollTop||0)<=0}
  function blocked(t){
    if(!t||!t.closest)return false;
    if(t.closest("input,select,textarea,[contenteditable=''],[contenteditable=true],#player,.player,[role=slider]"))return true;
    for(var n=t;n&&n!==document.body&&n!==de;n=n.parentElement){
      if(n.scrollTop>0){var oy=getComputedStyle(n).overflowY;if(oy==="auto"||oy==="scroll")return true}
    }
    return false}
  var sx=0,sy=0,on=false,pull=false,d=0,busy=false;
  function show(){var e=mk(),y=Math.min(d,MAX);e.style.transition="none";e.style.opacity=Math.min(1,y/40);
    e.style.transform="translateY("+(y-46)+"px)";e.querySelector("svg").style.transform="rotate("+(y/TH*270)+"deg)";
    e.classList.toggle("go",y>=TH)}
  function hide(){if(!el)return;el.style.transition="transform .2s,opacity .2s";el.style.transform="translateY(-52px)";el.style.opacity="0";el.classList.remove("go")}
  function refresh(){busy=true;var e=mk();e.classList.add("spin");e.style.transition="transform .2s";e.style.transform="translateY("+(TH-46)+"px)";
    var go=function(){location.reload()};
    try{var sw=navigator.serviceWorker;if(sw&&sw.getRegistration){
      Promise.race([sw.getRegistration().then(function(r){return r&&r.update()}),new Promise(function(r){setTimeout(r,1500)})]).then(go,go);return}}catch(_){}
    setTimeout(go,150)}
  document.addEventListener("touchstart",function(e){on=pull=false;d=0;
    if(busy||e.touches.length!==1||!top0()||blocked(e.target))return;
    try{var s=getSelection();if(s&&String(s).length)return}catch(_){}
    sx=e.touches[0].clientX;sy=e.touches[0].clientY;on=true},{passive:true});
  document.addEventListener("touchmove",function(e){if(!on)return;
    if(e.touches.length!==1){on=false;if(pull){pull=false;hide()}return}
    var dx=e.touches[0].clientX-sx,dy=e.touches[0].clientY-sy;
    if(!pull){if(dy<=0||!top0()){on=false;return}
      if(dy<12)return;
      if(Math.abs(dx)>dy*0.7){on=false;return}
      pull=true;sy=e.touches[0].clientY}
    dy=e.touches[0].clientY-sy;
    if(dy<=0){d=0;show();return}
    if(e.cancelable)e.preventDefault();
    d=dy*0.5;show()},{passive:false});
  function end(){if(!on)return;on=false;if(!pull)return;pull=false;if(d>=TH)refresh();else hide();d=0}
  document.addEventListener("touchend",end,{passive:true});
  document.addEventListener("touchcancel",function(){on=false;if(pull){pull=false;hide()}d=0},{passive:true});
})();
