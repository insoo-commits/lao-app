/* app-config (PhasaLAO): the values that differ between apps. The shared parts in tools/core/ read only this.
   They come from kor-app (PhasaKAO): run  node tools/core-copy.js ../lao-app  there; it also puts them into app.js. */
window.APPCFG = {
  app: "PhasaLAO",
  store: "lao-",                /* this app's storage prefix (lao-snap …); core parts that save new things use it */
  ptr: { bg: "rgba(40,44,52,.88)", go: "rgba(26,115,232,.95)" },   /* core ptr: pull-to-refresh button colour, and once far enough */
  vol: { sub: "작게 · 크게" }   /* core vol: small Korean label under the volume slider's title */
};
