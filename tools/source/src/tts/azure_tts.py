"""Generate one mp3 per Lao text with Azure Speech (lo-LA neural voice).
Env: AZURE_SPEECH_KEY, AZURE_SPEECH_REGION. Input: list.json {key: text}. Output: audio/<key>.mp3.
Skips files that already exist, so it can be rerun after an interruption."""
import json, os, sys, time, html, concurrent.futures as cf, urllib.request, urllib.error
KEY=os.environ['AZURE_SPEECH_KEY']; REG=os.environ['AZURE_SPEECH_REGION']
VOICE=os.environ.get('LAO_VOICE','lo-LA-KeomanyNeural')
src=sys.argv[1] if len(sys.argv)>1 else 'list.json'; out=sys.argv[2] if len(sys.argv)>2 else 'audio'
os.makedirs(out,exist_ok=True)
L=json.load(open(src)); todo=[(k,t) for k,t in L.items() if not os.path.exists(f'{out}/{k}.mp3')]
if len(sys.argv)>3: todo=todo[:int(sys.argv[3])]
URL=f'https://{REG}.tts.speech.microsoft.com/cognitiveservices/v1'
def one(kt):
    k,t=kt
    ssml=f"<speak version='1.0' xml:lang='lo-LA'><voice name='{VOICE}'>{html.escape(t)}</voice></speak>".encode()
    for a in range(6):
        req=urllib.request.Request(URL,data=ssml,method='POST',headers={'Ocp-Apim-Subscription-Key':KEY,'Content-Type':'application/ssml+xml',
            'X-Microsoft-OutputFormat':'audio-24khz-48kbitrate-mono-mp3','User-Agent':'lao-app-tts'})
        try:
            b=urllib.request.urlopen(req,timeout=60).read()
            if len(b)<500: raise RuntimeError('short audio')
            open(f'{out}/{k}.mp3.part','wb').write(b); os.replace(f'{out}/{k}.mp3.part',f'{out}/{k}.mp3'); return None
        except urllib.error.HTTPError as e:
            if e.code in (401,403): raise SystemExit(f'auth error {e.code}: check key/region')
            time.sleep(2**a*(3 if e.code==429 else 1))
        except Exception: time.sleep(2**a)
    return k
print('todo',len(todo)); fails=[]; t0=time.time()
with cf.ThreadPoolExecutor(int(os.environ.get('TTS_THREADS','4'))) as ex:
    for n,r in enumerate(ex.map(one,todo),1):
        if r: fails.append(r)
        if n%200==0: print(n,'done',int(time.time()-t0),'s',flush=True)
print('failed',len(fails)); json.dump(fails,open('failed.json','w'))
