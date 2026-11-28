# v12.2: insert 컴퓨터 조작 as 1-07-16; 1-07-16→17, 1-07-17→18; migration lao-idv 13
import json,re,sys
APP=sys.argv[1]
src=open('/mnt/project-files/lao-app/src/build_v12.py',encoding='utf-8').read()
ns={};exec(src[src.find('def jong'):src.find('# id map old -> new')],ns)
exec(open('/mnt/project-files/lao-app/src/new_subs_v12.py',encoding='utf-8').read(),ns)
s=open(APP,encoding='utf-8').read()
i=s.find('const DATA=');j=s.find('\n',i);lit=s[i+11:j].rstrip(';')
d=json.loads(json.loads(lit[11:-1]));B=d['B']
assert B['1-07-15']['t']=='컴퓨터 기본' and B['1-07-16']['t']=='인터넷·파일' and B['1-07-17']['t']=='숙제·평가' and '1-07-18' not in B
C=ns['CTRL'];w=C['w']
nb={"t":C['t'],"h":" · ".join(x[0] for x in w),"i":", ".join(re.sub(r'\(.*?\)','',x[3]).split(',')[0].strip() for x in w)+".",
    "w":w,"tp":C['tp'],"nx":[],"pr":C['pr'],"dl":C['dl'],"sm":C['sm'],"qz":ns['mkq'](C)}
M={'1-07-16':'1-07-17','1-07-17':'1-07-18'}
pat=re.compile(r'(?<![\d-])(\d-\d{2}-\d{2})(?![\d-])')
def fix(o):
    if isinstance(o,str): return pat.sub(lambda m:M.get(m.group(1),m.group(1)),o)
    if isinstance(o,list): return [fix(x) for x in o]
    if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
    return o
newB={M.get(k,k):fix(v) for k,v in B.items()};newB['1-07-16']=nb
for p in d['P']:
    for sb in p['subs']:
        sb['b']=[M.get(x,x) for x in sb['b']]
        if sb['id']=='P5-L': sb['b']=[f"1-07-{n:02d}" for n in range(1,19)]
allids=[x for p in d['P'] for sb in p['subs'] for x in sb['b']]
d['B']={k:newB[k] for k in allids};assert len(d['B'])==len(newB)
new='const DATA=JSON.parse('+json.dumps(json.dumps(d,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+');'
s=s[:i]+new+s[j:]
a='const IDV=store.get("lao-idv",0);'
assert s.count(a)==1
s=s.replace(a,'const IDMAP3='+json.dumps(M)+';for(const k in IDMAP){if(IDMAP3[IDMAP[k]])IDMAP[k]=IDMAP3[IDMAP[k]]}\n'+a)
a='if(IDV<12){store.set("lao-sel",saved);store.set("lao-idv",12)}'
assert s.count(a)==1
s=s.replace(a,'if(IDV<13){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);k2[m&&IDMAP3[m[1]]?IDMAP3[m[1]]+k.slice(m[1].length):k]=known[k]}known=k2;store.set("lao-known",known);if(saved.bun)for(const k in saved.bun)if(IDMAP3[saved.bun[k]])saved.bun[k]=IDMAP3[saved.bun[k]];store.set("lao-sel",saved);store.set("lao-idv",13)}')
open(APP,'w',encoding='utf-8').write(s);print('ok',len(d['B']))
