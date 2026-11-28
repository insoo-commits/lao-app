# v12.3: one extra bundle per subject inside 수업 (1-07), placed after that subject; migration lao-idv 14
import json,re,sys
APP=sys.argv[1]
src=open('/mnt/project-files/lao-app/src/build_v12.py',encoding='utf-8').read()
ns={};exec(src[src.find('def jong'):src.find('# id map old -> new')],ns)
exec(open('/mnt/project-files/lao-app/src/new_subs_v12.py',encoding='utf-8').read(),ns)
def mkq5(b):
    W=b['w'];q=[];obj,top=ns['obj'],ns['top']
    e=W[0][4][0];q.append([f"{e[0]} 의 뜻을 쓰세요.",e[2].rstrip('.')])
    k=W[1][3];q.append([f"‘{k}’{obj(k)} 라오스어로 쓰세요.",f"{W[1][0]} ({W[1][2]})"])
    e=W[2][4][0]
    if W[2][0] in e[0]: q.append([f"빈칸에 알맞은 말: {e[0].replace(W[2][0],'____',1)}  ({e[2].rstrip('.')})",W[2][0]])
    k=W[4][3];q.append([f"‘{k}’{top(k)} 어느 쪽?  ① {W[3][0]}  ② {W[4][0]}","②"])
    q.append([f"{W[3][0]} 의 한국어 독음과 뜻은?",f"{W[3][2]}, {W[3][3]}"])
    return q
s=open(APP,encoding='utf-8').read()
i=s.find('const DATA=');j=s.find('\n',i);lit=s[i+11:j].rstrip(';')
d=json.loads(json.loads(lit[11:-1]));B=d['B']
L=[sb for p in d['P'] for sb in p['subs'] if sb['id']=='P5-L'][0]
old=L['b'][:];assert len(old)==18
seq=[('old',x) for x in old]
for after,C in ns['MORE']:
    titles=after.split('|');pos=max(k for k,(t,x) in enumerate(seq) if t=='old' and B[x]['t'] in titles)
    w=C['w'];nb={"t":C['t'],"h":" · ".join(x[0] for x in w),"i":", ".join(re.sub(r'\(.*?\)','',x[3]).split(',')[0].strip() for x in w)+".",
        "w":w,"tp":C['tp'],"nx":[],"pr":C['pr'],"dl":C['dl'],"sm":C['sm'],"qz":mkq5(C)}
    seq.insert(pos+1,('new',nb))
M={};newB={k:v for k,v in B.items() if k not in old};ids=[]
for n,(t,x) in enumerate(seq):
    nid=f"1-07-{n+1:02d}";ids.append(nid)
    if t=='old':
        if x!=nid:M[x]=nid
        newB[nid]=B[x]
    else: newB[nid]=x
pat=re.compile(r'(?<![\d-])(\d-\d{2}-\d{2})(?![\d-])')
def fix(o):
    if isinstance(o,str): return pat.sub(lambda m:M.get(m.group(1),m.group(1)),o)
    if isinstance(o,list): return [fix(x) for x in o]
    if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
    return o
newB=fix(newB);L['b']=ids
allids=[x for p in d['P'] for sb in p['subs'] for x in sb['b']]
d['B']={k:newB[k] for k in allids};assert len(d['B'])==len(newB)
new='const DATA=JSON.parse('+json.dumps(json.dumps(d,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+');'
s=s[:i]+new+s[j:]
a='const IDV=store.get("lao-idv",0);'
s=s.replace(a,'const IDMAP4='+json.dumps(M)+';for(const k in IDMAP){if(IDMAP4[IDMAP[k]])IDMAP[k]=IDMAP4[IDMAP[k]]}\n'+a)
a='store.set("lao-idv",13)}'
assert s.count(a)==1
s=s.replace(a,a+'if(IDV<14){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);k2[m&&IDMAP4[m[1]]?IDMAP4[m[1]]+k.slice(m[1].length):k]=known[k]}known=k2;store.set("lao-known",known);if(saved.bun)for(const k in saved.bun)if(IDMAP4[saved.bun[k]])saved.bun[k]=IDMAP4[saved.bun[k]];store.set("lao-sel",saved);store.set("lao-idv",14)}')
open(APP,'w',encoding='utf-8').write(s)
for n,(t,x) in enumerate(seq): print(f"1-07-{n+1:02d}",'NEW' if t=='new' else x,(x['t'] if t=='new' else B[x]['t']))
print(M)
