# v2.83 RYU: bundle moves from the GPT menu review. usage: python3 build_v283.py app.js
import json,re,sys
APP=sys.argv[1];L=open(APP,encoding='utf-8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0])
MAP={}
# colours -> new 핵심회화 sub 1-13 색깔
MAP['4-04-10']='1-13-01';MAP['4-04-11']='1-13-02'
# 4-04: 12..16 shift -2, then add three moved bundles
for i in range(12,17):MAP['4-04-%02d'%i]='4-04-%02d'%(i-2)
MAP['5-09-01']='4-04-15';MAP['5-15-05']='4-04-16';MAP['5-16-04']='4-04-17'
MAP['5-11-03']='4-06-08'
for i in range(2,7):MAP['5-09-%02d'%i]='5-09-%02d'%(i-1)
new=lambda x:MAP.get(x,x)
rx=re.compile(r'(?<![\d-])(\d-\d\d-\d\d)(?![\d])')
sub_=lambda s:rx.sub(lambda mm:new(mm.group(1)),s)
n0=len(json.loads(json.loads(m.group(1)))['B'])
D=json.loads(sub_(json.loads(m.group(1))));B=D['B'];assert len(B)==n0
subs={x['id']:x for p in D['P'] for x in p['subs']}
c=subs['P4-C']['b'];c=[b for b in c if not b.startswith('1-13')]+['4-04-15','4-04-16','4-04-17'];subs['P4-C']['b']=sorted(c)
subs['P4-F']['b']=subs['P4-F']['b']+['4-06-08']
for sid,old in [('P3-K','4-04-15'),('P3-F','4-04-16'),('P3-N','4-04-17'),('P3-P','4-06-08')]:subs[sid]['b']=[b for b in subs[sid]['b'] if b!=old]
subs['P3-P']['name']='끝·잃음'
for k in ('4-04-15','4-04-16','4-04-17'):B[k]['t']=B[k]['t'].strip("'")
D['P'][0]['subs'].append({'id':'P5-M','name':'색깔','b':['1-13-01','1-13-02']})
for x in subs.values():
    for b in x['b']:assert b in B,b
allb=[b for p in D['P'] for x in p['subs'] for b in x['b']];assert len(allb)==len(set(allb))==len(B),(len(allb),len(set(allb)),len(B))
js=json.dumps(D,ensure_ascii=False,separators=(',',':'))
L[0]='const DATA=JSON.parse('+json.dumps(js,ensure_ascii=False)+')'+m.group(2)
for i,l in enumerate(L):
    if l.startswith('const BLAB=') or l.startswith('/* v2.82 RYU: sub/bundle titles') or '(id==="4-04-10"||id==="4-04-11")' in l:
        L[i]=sub_(l)
    if l.startswith('const BLAB='):
        bl=json.loads(L[i][len('const BLAB='):].rstrip(';'));bl['5-09-05']  # sanity
idm=json.dumps(MAP,ensure_ascii=False)
k=next(i for i,l in enumerate(L) if 'store.set("lao-idv",19)}' in l)
L.insert(k+1,'/* v2.83 RYU: bundles moved (colours -> 1-13 색깔, 한가·부자·넓다 -> 4-04, 예의 -> 4-06) */const IDMAP10='+idm+';if(store.get("lao-idv",0)<20){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);k2[m&&IDMAP10[m[1]]?IDMAP10[m[1]]+k.slice(m[1].length):k]=known[k]}known=k2;store.set("lao-known",known);if(saved.bun)for(const k in saved.bun)if(IDMAP10[saved.bun[k]])saved.bun[k]=IDMAP10[saved.bun[k]];store.set("lao-sel",saved);store.set("lao-idv",20)}')
open(APP,'w',encoding='utf-8').write('\n'.join(L))
print(json.dumps(MAP,ensure_ascii=False))
