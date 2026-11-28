# 라오스어 앱: mp3 + 아이폰 설치(PWA)

RYU chose Azure Speech (official) for Lao mp3 and a PWA on GitHub Pages for iPhone install.

## Needs from RYU (asked 2026-11-12)
- Cloud environment with env vars AZURE_SPEECH_KEY, AZURE_SPEECH_REGION and allowed domain <region>.tts.speech.microsoft.com
- An empty GitHub repo + GitHub connected (Pages host)

## Steps (from this src folder, copy to a work dir first)
1. python3 build.py            # app html + offline html (tpl.html already supports mp3: window.AUDIO_INDEX)
2. node pwa_gen_list.js lao-app.html tts/list.json   # ~11,448 clips, ~233k chars (fits Azure F0 0.5M/month)
3. cd tts && python3 azure_tts.py list.json audio 20   # try 20 first, listen, then run without the limit (resumable)
4. python3 pwa/build_pwa.py <offline.html> tts/audio pwa/out
5. push pwa/out to the repo root, enable Pages (main, /root). iPhone: Safari > 공유 > 홈 화면에 추가. In-app button "음성 전체 저장" caches all mp3 for offline.

Audio key = FNV-1a(base36) of rep(text) with whitespace collapsed (same as akey() in tpl.html). ໆ is expanded before keying and synthesis.
Tested with fake mp3s in headless Chromium: playback 2x per item, SW offline reload OK. Not yet tested on a real iPhone.

## 2026-11-13
From v10.4 the repo app.js (insoo-commits/lao-app) is the source of truth; src/build.py output would revert ~1,100 edited word hints. Audio: src/tts/edge_tts_gen.py (24 kbps), lists via pwa_gen_list*.js.
