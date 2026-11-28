# v12 restructure: new 상황 sub "수업" (1-07) after 학교; later subs shift +1. Run from repo root: python3 build_v12.py app.js
import json,re,sys
APP=sys.argv[1]
exec(open('/mnt/project-files/lao-app/src/new_subs_v12.py',encoding='utf-8').read())
NEW={b['t']:b for s in SUBS for b in s['b']}
s=open(APP,encoding='utf-8').read()
i=s.find('const DATA=');j=s.find('\n',i);lit=s[i+11:j].rstrip(';')
d=json.loads(json.loads(lit[11:-1]))
B=d['B']
assert B['1-06-03']['t']=='과목' and B['1-06-08']['t']=='체육·놀이' and B['1-06-07']['t']=='숙제·평가' and B['1-06-02']['t']=='수업 명령어'
def jong(w):
    c=w.rstrip(' )?.!')[-1:]
    return bool(c) and '가'<=c<='힣' and (ord(c)-0xAC00)%28!=0
def obj(w): return '을' if jong(w) else '를'
def top(w): return '은' if jong(w) else '는'
def mkq(b):
    W=b['w'];q=[]
    e=W[0][4][0];q.append([f"{e[0]} 의 뜻을 쓰세요.",e[2].rstrip('.')])
    k=W[1][3];q.append([f"‘{k}’{obj(k)} 라오스어로 쓰세요.",f"{W[1][0]} ({W[1][2]})"])
    e=W[2][4][0]
    if W[2][0] in e[0]: q.append([f"빈칸에 알맞은 말: {e[0].replace(W[2][0],'____',1)}  ({e[2].rstrip('.')})",W[2][0]])
    k=W[4][3];q.append([f"‘{k}’{top(k)} 어느 쪽?  ① {W[3][0]}  ② {W[4][0]}","②"])
    q.append([f"{W[5][0]} 의 한국어 독음과 뜻은?",f"{W[5][2]}, {W[5][3]}"])
    return q
def mk(t):
    b=NEW[t];w=b['w']
    return {"t":t,"h":" · ".join(x[0] for x in w),"i":", ".join(re.sub(r'\(.*?\)','',x[3]).split(',')[0].strip() for x in w)+".",
            "w":w,"tp":b['tp'],"nx":[],"pr":b['pr'],"dl":b['dl'],"sm":b['sm'],"qz":mkq(b)}
# id map old -> new
M={}
school=[('1-06-01','1-06-01'),('1-06-04','1-06-02'),('1-06-05','1-06-03'),('1-06-06','1-06-04'),('1-06-09','1-06-05'),('1-06-10','1-06-06'),
        ('1-06-03','1-07-01'),('1-06-02','1-07-02'),('1-06-08','1-07-12'),('1-06-07','1-07-17')]
for a,b in school: M[a]=b
P5=[p for p in d['P'] if p['id']=='P5'][0]
idx=[x['id'] for x in P5['subs']].index('P5-A')
for sb in P5['subs'][idx+1:]:
    for bid in sb['b']:
        a,n,c=bid.split('-');M[bid]=f"{a}-{int(n)+1:02d}-{c}"
order=['한글 배우기','수업 중 표현','말하기 연습','한국 소개','K-팝·드라마','라오스 문화','예절·명절','음악','미술·만들기']
newB={}
for k,v in B.items(): newB[M.get(k,k)]=v
for n,t in enumerate(order): newB[f"1-07-{n+3:02d}"]=mk(t)
for n,t in zip((13,14,15,16),['운동·구령','과학 실험','컴퓨터 기본','인터넷·파일']): newB[f"1-07-{n:02d}"]=mk(t)
for sb in P5['subs']: sb['b']=[M.get(x,x) for x in sb['b']]
P5['subs'][idx]['b']=[f"1-06-{n:02d}" for n in range(1,7)]
P5['subs'].insert(idx+1,{"id":"P5-L","name":"수업","b":[f"1-07-{n:02d}" for n in range(1,18)]})
assert all(x in newB for sb in P5['subs'] for x in sb['b'])
# text refs
pat=re.compile(r'(?<![\d-])(\d-\d{2}-\d{2})(?![\d-])')
def fix(o):
    if isinstance(o,str): return pat.sub(lambda m:M.get(m.group(1),m.group(1)),o)
    if isinstance(o,list): return [fix(x) for x in o]
    if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
    return o
newB=fix(newB)
# keep key order by sub listing
allids=[x for p in d['P'] for sb in p['subs'] for x in sb['b']]
d['B']={k:newB[k] for k in allids}
assert len(d['B'])==len(newB),(len(d['B']),len(newB))
new='const DATA=JSON.parse('+json.dumps(json.dumps(d,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+');'
s=s[:i]+new+s[j:]
# migration (one time, flag lao-idv=12)
anchor='const saved=store.get("lao-sel",{});'
assert s.count(anchor)==1
mig=('const IDMAP2='+json.dumps(M,separators=(',',':'))+';for(const k in IDMAP)if(IDMAP2[IDMAP[k]])IDMAP[k]=IDMAP2[IDMAP[k]];\n'
 'const IDV=store.get("lao-idv",0);if(IDV<12){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);k2[m&&IDMAP2[m[1]]?IDMAP2[m[1]]+k.slice(m[1].length):k]=known[k]}known=k2;store.set("lao-known",known)}\n')
s=s.replace(anchor,mig+anchor)
a2='if(IDMAP[saved.bun[k]])saved.bun[k]=IDMAP[saved.bun[k]];'
assert s.count(a2)==1
s=s.replace(a2,a2+'if(IDV<12&&saved.bun)for(const k in saved.bun)if(IDMAP2[saved.bun[k]])saved.bun[k]=IDMAP2[saved.bun[k]];if(IDV<12)store.set("lao-idv",12);')
open(APP,'w',encoding='utf-8').write(s)
json.dump(M,open('/mnt/project-files/lao-app/src/id_map_v12.json','w'),ensure_ascii=False,indent=0)
print('mapped',len(M),'bundles',len(d['B']))
