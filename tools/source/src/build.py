import json,base64,os,sys
os.chdir('/tmp/claude-0/-home-claude/5cb58977-2588-5b11-be03-6cb784340bba/scratchpad')
B=json.load(open('doc/bundles.json')); T=json.load(open('/mnt/project-files/lao-app/taxonomy.json')); toc=dict(json.load(open('doc/toc.json')))
toc['P5-047']='요일'
for p in T:
    for sb in p['subcategories']:
        if sb['id']=='P3-F': sb['name']='성격·외모·형편'
        if sb['id']=='P5-K': sb['name']='기초 회화'
EX=json.load(open('extra_bundles.json')) if os.path.exists('extra_bundles.json') else {}
for bid,x in EX.items():
    B[bid]={"head":x['head'],"intro":x['intro'],"words":x['words'],"tip":x['tip'],"next":x.get('next',[]),"pairs":x['pairs'],"dlg":x['dlg'],"sum":x['sum'],"quiz":x['quiz']}
    toc[bid]=x['title']
    for p in T:
        for sb in p['subcategories']:
            if sb['id']==x['sub'] and bid not in [q['id'] for q in sb['bundles']]:
                AFTER={'P5-052':'P5-047','P5-053':'P5-051','P4-061':'P4-022','P5-054':'P5-022'}
                ids=[q['id'] for q in sb['bundles']]
                pos=ids.index(AFTER[bid])+1 if bid in AFTER and AFTER[bid] in ids else x['pos']
                sb['bundles'].insert(pos,{"id":bid,"title":x['title']})
n3=nf=0
for c in ([] if os.environ.get('NOEX3') else ['P1','P2a','P2b','P3','P4','P5']):
    p=f'ex3/out_{c}.json'
    if not os.path.exists(p): continue
    O=json.load(open(p))
    for bid,o in O.items():
        ws=B[bid]['words']
        if len(o.get('ex3',[]))!=len(ws): continue
        for f in o.get('fix',[]):
            try: ws[f['i']]['ex'][f['n']-1]=f['ex']; nf+=1
            except Exception: pass
        for w,e in zip(ws,o['ex3']):
            if len(w['ex'])==2: w['ex'].append(e); n3+=1
ns=0
for c in ([] if os.environ.get('NOEX3') else ['P1','P2a','P2b','P3','P4','P5']):
    p=f'ex3/short_out_{c}.json'
    if os.environ.get('SKIPSHORT') or not os.path.exists(p): continue
    SO=json.load(open(p))
    if len(SO)<len(json.load(open(f'ex3/short_in_{c}.json'))): print('skip incomplete',c); continue
    for key,e in SO.items():
        bid,i,n=key.split('|'); B[bid]['words'][int(i)]['ex'][int(n)-1]=e; ns+=1
for v in B.values():
    for w in v['words']:
        if w['lo']=='ວັນພຸດ' and w['rd']=='완풀': w['rd']='완푿'
print('short replaced',ns)
def norm(r):
    o=[]
    for ch in r:
        x=ord(ch)-0xAC00
        if 0<=x<11172:
            L,V,T=x//588,(x%588)//28,x%28
            if L==9: L=10   # ㅅ -> ㅆ
            if T==19: T=7   # final ㅅ -> ㄷ
            ch=chr(0xAC00+L*588+V*28+T)
        o.append(ch)
    return ''.join(o).replace('퐝','팡').replace('완풀','완푿').replace('할타깜','핟타깜')
nn=0
for v in B.values():
    for w in v['words']:
        for e in w['ex']:
            r=norm(e[1])
            if r!=e[1]: nn+=1; e[1]=r
print('readings normalized',nn)
for v in B.values():
    for w in v['words']:
        if 'ຊາວ' in w['lo']: w['rd']=w['rd'].replace('싸우','싸오')
        for e in w['ex']:
            if 'ຊາວ' in e[0]: e[1]=e[1].replace('싸우','싸오')
    for d in v['dlg']:
        if 'ຊາວ' in d[1]: d[2]=d[2].replace('싸우','싸오')
# reorder words per ord/order.json (pairs adjacent, base before negative/question)
ORDER=json.load(open('ord/order.json'))
ORDER.pop('P5-055',None); ORDER.pop('P5-067',None); ORDER.pop('P4-062',None)  # hand-ordered in extra_bundles.json
nre=0
for k,v in B.items():
    if k not in ORDER: continue
    pool={}
    for w in v['words']: pool.setdefault(w['lo'],[]).append(w)
    nw=[pool[lo].pop(0) for lo in ORDER[k] if pool.get(lo)]
    nw+=[w for ws in pool.values() for w in ws]
    assert len(nw)==len(v['words']),k
    if [w['lo'] for w in nw]!=[w['lo'] for w in v['words']]: nre+=1
    v['words']=nw
print('bundles reordered',nre)
# P5-050 수료식·작별 lives in P5-A 학교 (end, before its cross bundle P5-061)
for p in T:
    for sb in p['subcategories']:
        if sb['id']=='P5-K': mv=[q for q in sb['bundles'] if q['id']=='P5-050']; sb['bundles']=[q for q in sb['bundles'] if q['id']!='P5-050']
for p in T:
    for sb in p['subcategories']:
        if sb['id']=='P5-A' and mv and 'P5-050' not in [q['id'] for q in sb['bundles']]: sb['bundles']+=mv
# cross-listed words: each scene sub gets a bundle of words it needs from other subs
CR=json.load(open('cross.json'))
SUBOF={b['id']:s['id'] for p in T for s in p['subcategories'] for b in s['bundles']}
PRI={'P5':0,'P4':1,'P3':2,'P2':3,'P1':4}
n0=55  # cross bundles stay P5-056..066 (ids are used for saved progress)
for si,(sid,los) in enumerate(CR['sel'].items()):
    bid='P5-%03d'%(n0+1+si); nm=CR['names'][sid]; ws=[]; origin=[]
    for lo in los:
        cands=[k for k,v in B.items() if any(w['lo']==lo for w in v['words']) and SUBOF.get(k)!=sid]
        src=CR['src'].get(lo) or sorted(cands,key=lambda k:(PRI[k[:2]],k))[0]
        w=dict(next(w for w in B[src]['words'] if w['lo']==lo)); w['hint']=(w['hint']+' · ' if w['hint'] else '')+'원래 '+src
        ws.append(w); origin.append(f"{lo}({w['rd']}) → {src} {toc.get(src,'')}")
    title=nm+'에서 같이 쓰는 말'; toc[bid]=title
    B[bid]={"head":title+'  '+' · '.join(los),"intro":f"{nm} 장면에서 꼭 필요하지만 다른 묶음에 실려 있는 단어를 모았어요. 원래 묶음에도 그대로 있어요.",
      "words":ws,"tip":["• 원래 묶음: "+o for o in origin],"next":[],"pairs":[],"dlg":[],"sum":[],
      "quiz":[[f"{w['lo']} 의 독음과 뜻은?",f"{w['rd']}, {w['ko']}"] for w in ws[:5]]}
    for p in T:
        for s in p['subcategories']:
            if s['id']==sid: s['bundles'].append({"id":bid,"title":title})
print('cross bundles',len(CR['sel']))
out={}
for k,v in B.items():
    parts=v['head'].split('  ',1)
    out[k]={"t":toc[k],"h":parts[1].strip() if len(parts)>1 else '',"i":v['intro'],"w":[[w['lo'],w['hint'],w['rd'],w['ko'],w['ex']] for w in v['words']],
      "tp":v.get('tip',[]),"nx":v.get('next',[]),"pr":v['pairs'],"dl":v['dlg'],"sm":v['sum'],"qz":v['quiz']}
# RYU 2026-11-13: drop "prefix + circled number" from bundle titles, also in tp/nx link labels
import re
TREN={v['t']:re.sub(r'^.*?[\u2460-\u246e]\s*','',v['t']) for v in out.values() if re.search(r'[\u2460-\u246e]',v['t'])}
for v in out.values():
    v['t']=TREN.get(v['t'],v['t'])
    for f in ('tp','nx'):
        L=[]
        for x in v[f]:
            for o in sorted(TREN,key=len,reverse=True): x=x.replace(o,TREN[o])
            L.append(x)
        v[f]=L
print('titles renamed',len(TREN))
P=[{"id":p['id'],"ko":p['name'],"desc":p['desc'],"subs":[{"id":s['id'],"name":s['name'],"b":[b['id'] for b in s['bundles']]} for s in p['subcategories']]} for p in T]
# v10 (RYU 2026-11-13): bundle ids renumbered part-sub-order (src/id_map_v10.json); PART n -> 발음/어근/의미
import re
IDM=json.load(open('id_map_v10.json'))
PARTN={'PART 1':'발음','PART 2':'어근','PART 3':'의미'}
def v10txt(x):
    for o,n in PARTN.items(): x=x.replace(o,n)
    return re.sub(r'P[1-5]-\d{3}',lambda m:IDM.get(m.group(0),m.group(0)),x)
miss=[k for k in out if k not in IDM]; assert not miss,('no v10 id',miss[:5])
out={IDM[k]:v for k,v in out.items()}
for v in out.values():
    v['t']=v10txt(v['t']); v['tp']=[v10txt(x) for x in v['tp']]; v['nx']=[v10txt(x) for x in v['nx']]
    for w in v['w']: w[1]=v10txt(w[1])
for p in P:
    for s_ in p['subs']:
        s_['b']=[IDM[b] for b in s_['b']]; s_['name']=PARTN.get(s_['name'][:6],'')+s_['name'][6:] if s_['name'].startswith('PART ') else s_['name']
ORD={"P5":"KJBCEAFDGHI","P4":"EDBCAF","P3":"HBCAGIEDKJPOLMFNZ","P2":"KGDHBFELJCAIMNZ","P1":"EADCBFGZ"}
for p in P:
    o=ORD[p['id']]; assert sorted(o)==sorted(s['id'].split('-')[1] for s in p['subs']),p['id']
    p['subs'].sort(key=lambda s:o.index(s['id'].split('-')[1]))
P=P[::-1]
d='const DATA='+json.dumps({"P":P,"B":out},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';'
t=open('tpl.html').read()
f=base64.b64encode(open('font/lao.woff2','rb').read()).decode()
ff='@font-face{font-family:"Lao Local";src:url(data:font/woff2;base64,'+f+') format("woff2");font-weight:100 900;font-display:swap;unicode-range:U+0E81-0EDF,U+200C-200D,U+25CC}\n'
t=t.replace('&family=Noto+Sans+Lao:wght@400;500;600;700','').replace('--lao:"Noto Sans Lao",','--lao:"Lao Local","Noto Sans Lao",').replace('<style>\n/* Layout','<style>\n'+ff+'/* Layout',1).replace('/*DATA*/',d)
open('lao-app.html','w').write(t)
off='<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style>\n'
off+=t.replace('<div class="wrap"','</head><body>\n<div class="wrap"',1)+'\n</body></html>\n'
off=off.replace('예문은 학습용으로','이 파일은 인터넷 없이도 열립니다. 예문은 학습용으로')
open('/mnt/project-files/lao-app/라오스어_묶음학습_오프라인.html','w').write(off)
print('ex3 added',n3,'fixes',nf,'size',len(t.encode()))
