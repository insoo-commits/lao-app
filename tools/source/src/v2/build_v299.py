# v2.99 RYU (점검표 1·2번): bundle numbers match the tabs, small subs merged.
#  듣기연습 9-xx-xx <-> 라오스 8-xx-xx (라오스 ids come from build_v263.py, also changed)
#  6-01-18 ຕົ້ນ -> 6-12-07 (자연·색), 6-01-19..26 -> 18..25
#  1-13 색깔 (2) -> 1-11-05/06 (날씨·자연), sub P5-M removed
#  5-16 거리·크기 재기 (3) -> 5-08-07..09, sub P3-N removed
#  5-11 끝·잃음 (2) -> 5-02-12/13 (기본 동사), sub P3-P removed; 5-12..15 -> 5-11..14
#  6-15 말뿌리 총정리 (1) -> 6-14-13, sub P2-Z removed
import json,re,sys
APP=sys.argv[1];L=open(APP,encoding='utf-8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0])
D0=json.loads(json.loads(m.group(1)));B0=D0['B']
MAP={}
for k in B0:
    if k.startswith('9-'):MAP[k]='8'+k[1:]
for x in range(1,10):
    for y in range(1,40):MAP['8-%02d-%02d'%(x,y)]='9-%02d-%02d'%(x,y)   # 라오스 (in LAOINFO, keys for saved state)
MAP['6-01-18']='6-12-07'
for i in range(19,27):MAP['6-01-%02d'%i]='6-01-%02d'%(i-1)
MAP['1-13-01']='1-11-05';MAP['1-13-02']='1-11-06'
for i in (1,2,3):MAP['5-16-%02d'%i]='5-08-%02d'%(6+i)
MAP['5-11-01']='5-02-12';MAP['5-11-02']='5-02-13'
for s in (12,13,14,15):
    for i in range(1,15):
        if '5-%02d-%02d'%(s,i) in B0:MAP['5-%02d-%02d'%(s,i)]='5-%02d-%02d'%(s-1,i)
MAP['6-15-01']='6-14-13'
for a,b in MAP.items():
    if a in B0:assert b not in B0 or b in MAP,(a,b)
rx=re.compile(r'(?<![\d-])(\d-\d\d-\d\d)(?![\d])')
sub_=lambda s:rx.sub(lambda mm:MAP.get(mm.group(1),mm.group(1)),s)
D=json.loads(sub_(json.loads(m.group(1))));B=D['B'];assert len(B)==len(B0)
subs={x['id']:(p,x) for p in D['P'] for x in p['subs']}
def mv(bid,dst):
    for p in D['P']:
        for x in p['subs']:
            if bid in x['b']:x['b'].remove(bid)
    subs[dst][1]['b'].append(bid)
mv('6-12-07','P2-I')
for b in ('1-11-05','1-11-06'):mv(b,'P5-H')
for b in ('5-08-07','5-08-08','5-08-09'):mv(b,'P3-D')
for b in ('5-02-12','5-02-13'):mv(b,'P3-B')
mv('6-14-13','P2-N')
for p in D['P']:p['subs']=[x for x in p['subs'] if x['b']]
for p in D['P']:
    for x in p['subs']:x['b'].sort()
allb=[b for p in D['P'] for x in p['subs'] for b in x['b']];assert len(allb)==len(set(allb))==len(B),(len(allb),len(set(allb)),len(B))
# each sub's bundles share one prefix
for p in D['P']:
    for x in p['subs']:
        pre={b[:4] for b in x['b']};assert len(pre)==1,(x['id'],pre)
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
for i,l in enumerate(L):
    if i==0 or l.lstrip().startswith('const IDMAP') or '*/const IDMAP' in l:continue
    if rx.search(l):L[i]=sub_(l)
k=next(i for i,l in enumerate(L) if 'store.set("lao-idv",21)}' in l)
L.insert(k+1,'/* v2.99 RYU: 듣기 9-xx <-> 라오스 8-xx, 6-01-18 -> 6-12-07, 1-13 -> 1-11-05/06, 5-16 -> 5-08-07..09, 5-11 -> 5-02-12/13, 5-12..15 -> 5-11..14, 6-15-01 -> 6-14-13 */const IDMAP12='+json.dumps(MAP)+';if(store.get("lao-idv",0)<22){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);k2[m&&IDMAP12[m[1]]?IDMAP12[m[1]]+k.slice(m[1].length):k]=known[k]}known=k2;store.set("lao-known",known);if(saved.bun)for(const k in saved.bun)if(IDMAP12[saved.bun[k]])saved.bun[k]=IDMAP12[saved.bun[k]];const GONE={"P5-M":["P5","P5-H"],"P3-N":["P3","P3-D"],"P3-P":["P3","P3-B"],"P2-Z":["P2","P2-N"]};if(GONE[saved.sub]){saved.part=GONE[saved.sub][0];saved.sub=GONE[saved.sub][1]}if(saved.lastSub)for(const p in saved.lastSub)if(GONE[saved.lastSub[p]])saved.lastSub[p]=GONE[saved.lastSub[p]][1];store.set("lao-sel",saved);store.set("lao-idv",22)}')
open(APP,'w',encoding='utf-8').write('\n'.join(L))
print('ok',len(B),len(MAP))
