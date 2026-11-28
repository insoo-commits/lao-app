# v14: merge small bundles in 2-02 분류사·단위 (15 -> 10); migration lao-idv 15 (IDMAP5)
# usage: python3 build_v14.py /path/to/app.js
import json,re,sys
APP=sys.argv[1]
s=open(APP,encoding='utf-8').read()
first,rest=s.split('\n',1)
m=re.match(r'const DATA=JSON\.parse\((".*")\)(;?)\s*$',first)
d=json.loads(json.loads(m.group(1)));B=d['B']
SUB=[sb for p in d['P'] for sb in p['subs'] if sb['id']=='P4-D'][0]
old=SUB['b'][:];assert len(old)==15,old
BL=dict((k,json.loads('['+v+']')) for k,v in re.findall(r'"(2-02-\d\d)":\[([^\]]*)\]',rest))
PLAN=[
 (['2-02-01'],None),
 (['2-02-02','2-02-04','2-02-05'],dict(t="ໂຕ·ໜ່ວຍ·ຄັນ",lab=["ໂຕ·ໜ່ວຍ·ຄັນ",""],i="한 글자로 여러 물건을 세는 말 셋이에요. ໂຕ(동물·옷·글자·가구), ໜ່ວຍ(둥근 것·과일·기기), ຄັນ(손잡이나 몸체가 긴 것).")),
 (['2-02-03'],None),
 (['2-02-06','2-02-14'],dict(t="모양으로 세기",lab=["모양으로 세기","ນັບຕາມຮູບຮ່າງ"],i="모양에 따라 세는 말: 개, 조각, 덩어리, 자루, 가닥, 줄, 장(천), 척.")),
 (['2-02-07'],None),
 (['2-02-13','2-02-08'],dict(t="식물·알",lab=["식물·알","ພືດ·ເມັດ"],i="나무의 부분(그루, 가지, 잎, 송이, 열매)과 알·알뿌리를 세는 말.")),
 (['2-02-09'],None),
 (['2-02-10','2-02-11'],dict(t="묶음·세트",lab=["묶음·세트","ມັດ·ຊຸດ"],i="봉지, 상자, 다발, 팩, 켤레, 벌, 세트, 다스.")),
 (['2-02-12'],None),
 (['2-02-15'],None),
]
M={};newB={k:v for k,v in B.items() if k not in old};ids=[];LAB={}
for n,(src,meta) in enumerate(PLAN):
    nid=f"2-02-{n+1:02d}";ids.append(nid)
    for x in src:
        if x!=nid:M[x]=nid
    if meta is None:
        newB[nid]=B[src[0]];LAB[nid]=BL[src[0]];continue
    bs=[B[x] for x in src];w=[];seen=set()
    for b in bs:
        for x in b['w']:
            if x[0] in seen: continue
            seen.add(x[0]);w.append(x)
    qz=[];mx=max(len(b.get('qz',[])) for b in bs)
    for j in range(mx):
        for b in bs:
            q=b.get('qz',[])
            if j<len(q) and len(qz)<6 and q[j] not in qz: qz.append(q[j])
    sms=[b['sm'] for b in bs if b.get('sm') and b['sm'][0]]
    nb={"t":meta['t'],"h":" · ".join(x[0] for x in w),"i":meta['i'],"w":w,
        "tp":[t for b in bs for t in b.get('tp',[])],
        "nx":[x for b in bs for x in b.get('nx',[])],
        "pr":[x for b in bs for x in b.get('pr',[])],
        "dl":[x for b in bs for x in b.get('dl',[])],
        "sm":[" ".join(x[0] for x in sms)," ".join(x[1] for x in sms)," ".join(x[2] for x in sms)] if sms else [],
        "qz":qz}
    newB[nid]=nb;LAB[nid]=meta['lab']
pat=re.compile(r'(?<![\d-])(\d-\d{2}-\d{2})(?![\d-])')
def fix(o):
    if isinstance(o,str): return pat.sub(lambda mm:M.get(mm.group(1),mm.group(1)),o)
    if isinstance(o,list): return [fix(x) for x in o]
    if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
    return o
newB=fix(newB);SUB['b']=ids
allids=[x for p in d['P'] for sb in p['subs'] for x in sb['b']]
d['B']={k:newB[k] for k in allids};assert len(d['B'])==len(newB),(len(d['B']),len(newB))
# a quiz/tip must not point at a word that is no longer in the merged bundle: checked by the caller
# BLAB labels
a=rest.index('"2-02-01":[');e=rest.index(']',rest.index('"2-02-15":['))+1
rest=rest[:a]+",".join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(LAB[k],ensure_ascii=False,separators=(',',':')) for k in ids)+rest[e:]
x='const IDV=store.get("lao-idv",0);';assert rest.count(x)==1
rest=rest.replace(x,'const IDMAP5='+json.dumps(M)+';for(const k in IDMAP){if(IDMAP5[IDMAP[k]])IDMAP[k]=IDMAP5[IDMAP[k]]}\n'+x)
x='store.set("lao-idv",14)}';assert rest.count(x)==1
rest=rest.replace(x,x+'if(IDV<15){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);k2[m&&IDMAP5[m[1]]?IDMAP5[m[1]]+k.slice(m[1].length):k]=known[k]}known=k2;store.set("lao-known",known);if(saved.bun)for(const k in saved.bun)if(IDMAP5[saved.bun[k]])saved.bun[k]=IDMAP5[saved.bun[k]];store.set("lao-sel",saved);store.set("lao-idv",15)}')
lit=json.dumps(json.dumps(d,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)
open(APP,'w',encoding='utf-8').write('const DATA=JSON.parse('+lit+')'+m.group(2)+'\n'+rest)
for k in ids: print(k,LAB[k],len(d['B'][k]['w']),d['B'][k]['h'])
print(M)
