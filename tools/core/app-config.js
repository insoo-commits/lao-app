/* app-config (PhasaLAO): the values that differ between apps. The shared parts in tools/core/ read only this.
   They come from kor-app (PhasaKAO): run  node tools/core-copy.js ../lao-app  there; it also puts them into app.js. */
window.APPCFG = {
  app: "PhasaLAO",
  store: "lao-",                /* this app's storage prefix (lao-snap …); core parts that save new things use it */
  prefs: { theme: "화면", themes: ["자동", "☀ 밝게", "☾ 어둡게"], fz: "글자 크기", stop: true },   /* core prefs: labels of the theme / text size buttons */
  ptr: { bg: "rgba(40,44,52,.88)", go: "rgba(26,115,232,.95)" },   /* core ptr: pull-to-refresh button colour, and once far enough */
  stick: { title: function(){ var o = document.querySelector("#bsel option:checked"); return o ? (o.dataset.ko || o.textContent || "").trim() : ""; },
           watch: ["band"], strip: ["data-part"], stop: true },   /* core stick: lesson line from the lesson select; the band refreshes it */
  vol: { sub: "작게 · 크게" }   /* core vol: small Korean label under the volume slider's title */
};
