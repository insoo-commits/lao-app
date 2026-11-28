"""Lao mp3 via Edge online neural voice (edge-tts). Usage: python3 edge_tts_gen.py list.json audio [voice] [limit]
Resumable. Output is re-encoded to 24 kbps mono (RYU's choice). Through the agent proxy: uses HTTPS_PROXY and /root/.ccr/ca-bundle.crt if present."""
import asyncio,json,os,ssl,subprocess,sys,time,edge_tts,edge_tts.communicate as C
if os.path.exists('/root/.ccr/ca-bundle.crt'): C._SSL_CTX=ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
src,out=sys.argv[1],sys.argv[2]; V=sys.argv[3] if len(sys.argv)>3 else 'lo-LA-KeomanyNeural'
os.makedirs(out,exist_ok=True); L=json.load(open(src))
todo=[(k,t) for k,t in L.items() if not os.path.exists(f'{out}/{k}.mp3')]
if len(sys.argv)>4: todo=todo[:int(sys.argv[4])]
P=os.environ.get('HTTPS_PROXY'); fails=[]; done=0; t0=time.time(); print('todo',len(todo),flush=True)
async def one(k,t):
    for a in range(6):
        try:
            await edge_tts.Communicate(t,V,proxy=P).save(f'{out}/{k}.part')
            if os.path.getsize(f'{out}/{k}.part')<500: raise RuntimeError('short')
            # RYU 2026-11-13: store as 24 kbps mono 24 kHz
            subprocess.run(['ffmpeg','-loglevel','error','-y','-f','mp3','-i',f'{out}/{k}.part','-ar','16000','-ac','1','-b:a','16k','-f','mp3',f'{out}/{k}.p24'],check=True)
            os.remove(f'{out}/{k}.part'); os.replace(f'{out}/{k}.p24',f'{out}/{k}.mp3'); return True
        except Exception as e: await asyncio.sleep(2**a)
    return False
async def worker(q):
    global done
    while q:
        k,t=q.pop()
        if not await one(k,t): fails.append(k)
        done+=1
        if done%200==0: print(done,'done',int(time.time()-t0),'s',flush=True)
async def main():
    q=todo[::-1]; await asyncio.gather(*[worker(q) for _ in range(int(os.environ.get('TTS_THREADS','4')))])
asyncio.run(main()); print('failed',len(fails),'time',int(time.time()-t0)); json.dump(fails,open('failed.json','w'))
