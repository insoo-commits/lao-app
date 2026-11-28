/* core mine v1.1 (from kor-app; copy, do not edit here). Shared by PhasaKAO, JeyCampus and PhasaLAO.
   Edit only this master, raise the version, then run  node tools/core-copy.js.
   The sums behind the 내 학습 card under the search box (KoJey v1.4, RYU 2026-11-25): the day string, days with study,
   days in a row, how many lessons were opened, today's counts and the next new lesson. Only the sums live here;
   the card itself (words, layout) and where the records are saved stay in each app, because the saved formats differ:
     PhasaKAO / JeyCampus: S.seen {code: first day}, S.days [day…], S.td {d, l: lessons opened today, q: quizzes}
     PhasaLAO: lao-seen, lao-days, lao-td {d, s: {lesson: 1}, q}
   The storage keys and formats must not change: learners' progress is in them. */
(function(){
  if (window.MINE) return;
  /* local date as "2026-11-28" */
  var day = function(d){ return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
  /* the list of days with study, with day t added once at the end (newest 400 kept); returns the same array when t was already last */
  function addDay(days, t){ days = days || []; if (days[days.length - 1] !== t){ days.push(t); days = days.slice(-400); } return days; }
  /* days in a row up to today, or up to yesterday when today has no study yet */
  function streak(days){
    var set = new Set(days || []), d = new Date(), n = 0;
    if (!set.has(day(d))) d.setDate(d.getDate() - 1);
    while (set.has(day(d))){ n++; d.setDate(d.getDate() - 1); }
    return n;
  }
  /* today's counts: td when it is from today (t, default now), else make(t) */
  function fresh(td, make, t){ t = t || day(new Date()); return td && td.d === t ? td : make(t); }
  /* L = the lessons that count (no reading pages), seen(x) = opened before; pct with one decimal, bar = the bar's width in % */
  function prog(L, seen){ var n = L.filter(seen).length, pct = L.length ? Math.round(1000 * n / L.length) / 10 : 0;
    return {n: n, all: L.length, pct: pct, bar: Math.max(pct, n ? 1.5 : 0)}; }
  /* the next lesson not yet opened after position at (wrapping round); if all are opened, simply the next one */
  function next(L, at, seen){ return L.slice(at + 1).concat(L.slice(0, at + 1)).find(function(x){ return !seen(x); }) || L[(at + 1) % L.length]; }
  /* a quiz was finished: every finished quiz counts on today's record, the 오답·별표 review too (JeyCampus way, RYU 2026-11-28, v1.1);
     make(t) = the app's empty record for day t. Returns today's record. */
  function quiz(td, make){ td = fresh(td, make); td.q = (td.q || 0) + 1; return td; }
  window.MINE = {day: day, addDay: addDay, streak: streak, fresh: fresh, prog: prog, next: next, quiz: quiz};
})();
