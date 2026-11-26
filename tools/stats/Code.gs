/**
 * Study Lao (lao-app) usage statistics: receives the app's anonymous events and writes them to this Google Sheet.
 * Setup (once): paste this file into Extensions > Apps Script, run setup(), then Deploy > New deployment >
 * Web app (Execute as: Me, Who has access: Anyone). Put the web app URL into STATS_URL in app.js (v4.0 block).
 *
 * Sheet "events": one row per event.
 *   received (server time) | device time | device id | event | lesson | value 1 | value 2 | device | OS | app version | language | installed
 *   events: open (value 1 = phone/tablet/computer, value 2 = installed/browser) · lesson (lesson opened)
 *           speak (value 1 = % match of a spoken sentence, v1.13)
 *           quiz (value 1 = right, value 2 = questions) · topik (same, TOPIK practice set) · play (value 1 = lesson/all)
 * Sheet "summary": totals and tables made with formulas from "events".
 * Sheet "survey" (v1.11): one row per answer of the in-app satisfaction survey.
 *   received | device id | stars (1-5) | most helpful menu | recommend (yes/maybe/no) | comment | app version | device | OS | language
 * After changing this file: Deploy > Manage deployments > edit (pencil) > Version: New version > Deploy (the URL stays the same).
 */
var EVENTS = 'events', SUMMARY = 'summary';
var HEAD = ['received', 'device time', 'device id', 'event', 'lesson', 'value 1', 'value 2', 'device', 'OS', 'app version', 'language', 'installed'];
var OK_EVENTS = {open: 1, lesson: 1, quiz: 1, topik: 1, play: 1, speak: 1};
var SURVEY = 'survey', SHEAD = ['received', 'device id', 'stars', 'most helpful menu', 'recommend', 'comment', 'app version', 'device', 'OS', 'language'];

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var d = JSON.parse(e.postData.contents);
    var id = clean_(d.id, 40), now = new Date(), rows = [];
    (d.ev || []).slice(0, 200).forEach(function (x) {
      if (!x || !OK_EVENTS[x[1]]) return;
      rows.push([now, clean_(x[0], 30), id, x[1], clean_(x[2], 20), num_(x[3]), num_(x[4]),
        clean_(d.dev, 12), clean_(d.os, 12), clean_(d.v, 30), clean_(d.lang, 12), d.pwa ? 'yes' : '']);
    });
    if (rows.length) {
      var sh = sheet_(EVENTS);
      sh.getRange(sh.getLastRow() + 1, 1, rows.length, HEAD.length).setValues(rows);
    }
    var sv = d.survey;
    if (sv && sv.stars >= 1 && sv.stars <= 5) {
      var ss = sheet_(SURVEY);
      if (ss.getLastRow() === 0) ss.getRange(1, 1, 1, SHEAD.length).setValues([SHEAD]).setFontWeight('bold');
      ss.appendRow([now, id, Math.round(sv.stars), clean_(sv.menu, 10), clean_(sv.rec, 10), clean_(sv.text, 300), clean_(d.v, 30), clean_(d.dev, 12), clean_(d.os, 12), clean_(d.lang, 12)]);
      CacheService.getScriptCache().remove('stats');
    }
    return ContentService.createTextOutput('ok ' + rows.length);
  } catch (err) {
    return ContentService.createTextOutput('error');
  } finally {
    lock.releaseLock();
  }
}

/** GET ?stats=1: totals only (no device ids, no single scores) for the app's public 학습 통계 page. Cached 10 minutes. */
function doGet(e) {
  if (!e || !e.parameter || !e.parameter.stats) return ContentService.createTextOutput('Study Lao stats endpoint is working.');
  var cache = CacheService.getScriptCache(), hit = cache.get('stats');
  var json = hit || JSON.stringify(stats_());
  if (!hit) cache.put('stats', json, 600);
  return ContentService.createTextOutput(json).setMimeType(ContentService.MimeType.JSON);
}

function stats_() {
  var TZ = 'Asia/Seoul', sh = sheet_(EVENTS), n = sh.getLastRow() - 1;
  var rows = n > 0 ? sh.getRange(2, 1, n, HEAD.length).getValues() : [];
  var dev = {}, days = {}, months = {}, lessons = {}, areas = {}, hours = [], hist = [0, 0, 0, 0, 0];
  for (var i = 0; i < 24; i++) hours.push(0);
  var t = {devices: 0, returning: 0, lessons: 0, quizzes: 0, quizAvg: null, topik: 0, topikAvg: null, plays: 0, opens: 0, installed: 0, perLearner: null};
  var qR = 0, qN = 0, tR = 0, tN = 0, spS = 0, first = null;
  rows.forEach(function (r) {
    var when = r[0] instanceof Date ? r[0] : new Date(r[0]); if (isNaN(when)) return;
    var id = String(r[2]), ev = r[3], code = String(r[4] || ''), day = Utilities.formatDate(when, TZ, 'yyyy-MM-dd'), mon = day.slice(0, 7);
    if (!first || when < first) first = when;
    var d = dev[id] || (dev[id] = {days: {}, dev: '', os: '', pwa: false});
    d.days[day] = 1; if (r[7]) d.dev = r[7]; if (r[8]) d.os = r[8]; if (r[11] === 'yes') d.pwa = true;
    var D = days[day] || (days[day] = {ids: {}, lessons: 0}); D.ids[id] = 1;
    var M = months[mon] || (months[mon] = {ids: {}, lessons: 0}); M.ids[id] = 1;
    hours[+Utilities.formatDate(when, TZ, 'H')]++;
    if (ev === 'open') t.opens++;
    else if (ev === 'lesson') { t.lessons++; D.lessons++; M.lessons++; lessons[code] = (lessons[code] || 0) + 1; var a = code.split('-')[0]; areas[a] = (areas[a] || 0) + 1; }
    else if (ev === 'quiz') { var R = +r[5], N = +r[6]; if (N > 0) { t.quizzes++; qR += R; qN += N; hist[Math.min(4, Math.floor(5 * R / N))]++; } }
    else if (ev === 'topik') { var R2 = +r[5], N2 = +r[6]; if (N2 > 0) { t.topik++; tR += R2; tN += N2; } }
    else if (ev === 'play') t.plays++;
    else if (ev === 'speak') { var sp = +r[5]; if (sp >= 0) { t.speaks = (t.speaks || 0) + 1; spS += sp; } }
  });
  var devs = {}, oss = {};
  Object.keys(dev).forEach(function (id) {
    var d = dev[id]; t.devices++; if (Object.keys(d.days).length > 1) t.returning++; if (d.pwa) t.installed++;
    var dv = d.dev || 'other', os = d.os || 'other'; devs[dv] = (devs[dv] || 0) + 1; oss[os] = (oss[os] || 0) + 1;
  });
  if (qN) t.quizAvg = Math.round(1000 * qR / qN) / 10;
  if (tN) t.topikAvg = Math.round(1000 * tR / tN) / 10;
  if (t.speaks) t.speakAvg = Math.round(spS / t.speaks);
  if (t.devices) t.perLearner = Math.round(10 * t.lessons / t.devices) / 10;
  var pairs = function (o) { return Object.keys(o).map(function (k) { return [k, o[k]]; }).sort(function (a, b) { return b[1] - a[1]; }); };
  var dayList = Object.keys(days).sort().slice(-60).map(function (k) { return [k, Object.keys(days[k].ids).length, days[k].lessons]; });
  var monList = Object.keys(months).sort().map(function (k) { return [k, Object.keys(months[k].ids).length, months[k].lessons]; });
  return {updated: Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm') + ' KST', first: first ? Utilities.formatDate(first, TZ, 'yyyy-MM-dd') : '',
    survey: survey_(), totals: t, daily: dayList, monthly: monList, top: pairs(lessons).slice(0, 15), areas: pairs(areas), devices: pairs(devs), os: pairs(oss), quizHist: hist, hours: hours};
}

/** survey totals for the public page: no comments, no device ids */
function survey_() {
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SURVEY), out = {n: 0, avg: null, dist: [0, 0, 0, 0, 0], recPct: null};
  if (!sh || sh.getLastRow() < 2) return out;
  var rows = sh.getRange(2, 1, sh.getLastRow() - 1, 5).getValues(), sum = 0, rec = 0, recN = 0;
  rows.forEach(function (r) { var st = Number(r[2]); if (!(st >= 1 && st <= 5)) return; out.n++; sum += st; out.dist[st - 1]++;
    if (r[4]) { recN++; if (r[4] === 'yes') rec++; } });
  if (out.n) out.avg = Math.round(10 * sum / out.n) / 10;
  if (recN) out.recPct = Math.round(100 * rec / recN);
  return out;
}

/** Run once from the editor: makes the two sheets with headers and summary formulas. */
function setup() {
  var ev = sheet_(EVENTS);
  ev.getRange(1, 1, 1, HEAD.length).setValues([HEAD]).setFontWeight('bold');
  ev.setFrozenRows(1);
  var s = sheet_(SUMMARY);
  s.clear();
  var E = EVENTS + '!';
  var rows = [
    ['Study Lao usage', ''],
    ['Devices (users)', '=COUNTUNIQUE(' + E + 'C2:C)'],
    ['App opens', '=COUNTIF(' + E + 'D2:D,"open")'],
    ['Lessons opened', '=COUNTIF(' + E + 'D2:D,"lesson")'],
    ['Quizzes finished', '=COUNTIF(' + E + 'D2:D,"quiz")'],
    ['Quiz average (%)', '=IFERROR(ROUND(100*SUMIF(' + E + 'D2:D,"quiz",' + E + 'F2:F)/SUMIF(' + E + 'D2:D,"quiz",' + E + 'G2:G),1),"")'],
    ['TOPIK sets finished', '=COUNTIF(' + E + 'D2:D,"topik")'],
    ['TOPIK average (%)', '=IFERROR(ROUND(100*SUMIF(' + E + 'D2:D,"topik",' + E + 'F2:F)/SUMIF(' + E + 'D2:D,"topik",' + E + 'G2:G),1),"")'],
    ['Audio plays', '=COUNTIF(' + E + 'D2:D,"play")'],
    ['First event', '=IFERROR(MIN(' + E + 'A2:A),"")'],
    ['Last event', '=IFERROR(MAX(' + E + 'A2:A),"")']
  ];
  s.getRange(1, 1, rows.length, 2).setValues(rows);
  s.getRange('A1').setFontWeight('bold').setFontSize(13);
  s.getRange('B10:B11').setNumberFormat('yyyy-mm-dd hh:mm');
  s.getRange('D1').setValue('By day').setFontWeight('bold');
  s.getRange('D2').setFormula('=IFERROR(QUERY(' + E + 'A2:D,"select toDate(A), count(D) where A is not null group by toDate(A) order by toDate(A) desc label toDate(A) \'day\', count(D) \'events\'",0),"")');
  s.getRange('G1').setValue('Lessons opened most').setFontWeight('bold');
  s.getRange('G2').setFormula('=IFERROR(QUERY(' + E + 'D2:E,"select E, count(D) where D = \'lesson\' group by E order by count(D) desc limit 30 label E \'lesson\', count(D) \'opens\'",0),"")');
  s.getRange('J1').setValue('Devices').setFontWeight('bold');
  s.getRange('J2').setFormula('=IFERROR(QUERY(' + E + 'D2:I,"select H, I, count(D) where D = \'open\' group by H, I order by count(D) desc label H \'device\', I \'OS\', count(D) \'opens\'",0),"")');
  s.setColumnWidth(1, 170);
}

function sheet_(name) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  return ss.getSheetByName(name) || ss.insertSheet(name);
}
function clean_(v, max) {  // plain short text; a leading = + - @ would make a formula
  var s = String(v == null ? '' : v).slice(0, max);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}
function num_(v) {
  if (typeof v === 'number' && isFinite(v)) return v;
  return clean_(v, 12);
}
