# v2.85 RYU: rest of the GPT review moves: 5-10-05 ຖືກ -> 단어가족 6-08-12, 5-17-01 문장 끝말 -> 문장규칙 3-02-04 (sub P3-Z removed)
import json,re,sys
APP=sys.argv[1];L=open(APP,encoding='utf-8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0])
MAP={'5-10-05':'6-08-12','5-17-01':'3-02-04'}
for i in range(6,9):MAP['5-10-%02d'%i]='5-10-%02d'%(i-1)
new=lambda x:MAP.get(x,x)
rx=re.compile(r'(?<![\d-])(\d-\d\d-\d\d)(?![\d])')
sub_=lambda s:rx.sub(lambda mm:new(mm.group(1)),s)
n0=len(json.loads(json.loads(m.group(1)))['B'])
D=json.loads(sub_(json.loads(m.group(1))));B=D['B'];assert len(B)==n0
subs={x['id']:x for p in D['P'] for x in p['subs']}
subs['P3-J']['b']=[b for b in subs['P3-J']['b'] if b!='6-08-12']
subs['P2-L']['b'].append('6-08-12');subs['P7-B']['b'].append('3-02-04')
for p in D['P']:p['subs']=[x for x in p['subs'] if x['id']!='P3-Z']
B['6-08-12']['t']='ຖືກ 맞다·싸다·당하다'
allb=[b for p in D['P'] for x in p['subs'] for b in x['b']];assert len(allb)==len(set(allb))==len(B),(len(allb),len(set(allb)),len(B))
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
for i,l in enumerate(L):
    if l.startswith('const BLAB=') or l.startswith('/* v2.82 RYU: sub/bundle titles') or '(id==="1-13-01"||id==="1-13-02")' in l:
        L[i]=sub_(l)
k=next(i for i,l in enumerate(L) if 'store.set("lao-idv",20)}' in l)
L.insert(k+1,'/* v2.85 RYU: 5-10-05 -> 6-08-12, 5-17-01 -> 3-02-04, 5-10-06..08 -> 05..07 */const IDMAP11='+json.dumps(MAP)+';if(store.get("lao-idv",0)<21){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);k2[m&&IDMAP11[m[1]]?IDMAP11[m[1]]+k.slice(m[1].length):k]=known[k]}known=k2;store.set("lao-known",known);if(saved.bun)for(const k in saved.bun)if(IDMAP11[saved.bun[k]])saved.bun[k]=IDMAP11[saved.bun[k]];if(saved.sub==="P3-Z"){saved.sub="P7-B";saved.part="P7"}if(saved.lastSub&&saved.lastSub.P3==="P3-Z")delete saved.lastSub.P3;store.set("lao-sel",saved);store.set("lao-idv",21)}')
open(APP,'w',encoding='utf-8').write('\n'.join(L))
print('ok',len(B))
