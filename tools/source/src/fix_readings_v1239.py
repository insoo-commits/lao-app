# v12.38: reading fixes found by the spelling-vs-reading checker (scratch rev/tr.py). Run: python3 fix_readings_v1238.py app.js
import json,re,sys
APP=sys.argv[1]
s=open(APP,encoding='utf-8').read()
i=s.find('const DATA=');j=s.find('\n',i);lit=s[i+11:j].rstrip(';');d=json.loads(json.loads(lit[11:-1]))
PROT=['버리삳','안녕하세요','안뇽하세요','감사합니다','추석','시프트','펫북','윷놀이','민주','민준']
def norm(t):
    out=[]
    for tok in re.split(r'(\s+)',t):
        if any(p in tok for p in PROT):out.append(tok);continue
        o=''
        for c in tok:
            if '가'<=c<='힣':
                v=ord(c)-0xAC00;L,V,T=v//588,(v%588)//28,v%28
                if L==9:L=10
                if T==19:T=7
                c=chr(0xAC00+L*588+V*28+T)
            o+=c
        out.append(o)
    return ''.join(out)
# (lao key, wrong, right, [lao that must NOT be present])
M=[('ເກັບ','깹','껩','ແກັບ|ແຄບ'),('ເສັງ','쌩','쎙','ແສງ|ແຊງ'),('ເກັ່ງ','깽','껭','ແກງ|ແກ່ງ|ແກ້ງ'),('ຍົກ','녹','뇩','ນົກ|ໂນກ'),
 ('ຍອມ','넘','념','ນອມ|ໜອມ'),('ຍ້ອມ','넘','념','ນອມ|ໜອມ'),('ໂຍນ','욘','뇬'),('ຍ່ອຍ','너이','녀이','ນ້ອຍ|ໜ້ອຍ|ນ່ອຍ|ໜ່ອຍ')]
CH=[]
def fx(lo,rd):
    o=rd;rd=norm(rd)
    for m in M:
        k,a,b=m[:3]
        if k in lo and a in rd and not(len(m)>3 and re.search(m[3],lo)):rd=rd.replace(a,b)
    if rd!=o:CH.append((lo,o,rd))
    return rd
for b in d['B'].values():
    for w in b['w']:
        w[2]=fx(w[0],w[2])
        for e in w[4]:e[1]=fx(e[0],e[1])
    for p in b['pr']:
        for x in p:x[1]=fx(x[0],x[1])
    for dd in b['dl']:dd[2]=fx(dd[1],dd[2])
    if b.get('sm') and len(b['sm'])>1:b['sm'][1]=fx(b['sm'][0],b['sm'][1])
RDTOK=set();KOS=set()
for b in d['B'].values():
    for w in b['w']:
        RDTOK.update(w[2].split());KOS.add(w[3])
        for e in w[4]:RDTOK.update(e[1].split())
def isrd(t):
    t=t.strip()
    return t and t not in KOS and all(x.strip(',') in RDTOK for x in t.split())
pp=re.compile(r'([\u0e80-\u0eff][\u0e80-\u0eff ]*)(\s?\()([가-힣 ]+)\)')
def inl(t):return pp.sub(lambda m:m.group(1)+m.group(2)+(fx(m.group(1),m.group(3)) if isrd(m.group(3)) else m.group(3))+')',t)
for b in d['B'].values():
    b['tp']=[inl(t) for t in b['tp']];b['i']=inl(b['i'])
    for q in b['qz']:
        q[0]=inl(q[0])
        if re.search('[\u0e80-\u0eff]',q[1]):q[1]=inl(q[1])
        elif '독음' in q[0] and ',' in q[1]:
            h,t=q[1].split(',',1);q[1]=fx(''.join(re.findall('[\u0e80-\u0eff]+',q[0])),h)+','+t
m=re.search(r'NRD=(\{.*?\}),NFREQ',s);R=json.loads(m.group(1))
for k in R:R[k]=fx(k,R[k])
new='const DATA=JSON.parse('+json.dumps(json.dumps(d,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+');'
s=s[:i]+new+s[j:]
m=re.search(r'NRD=(\{.*?\}),NFREQ',s)
s=s[:m.start(1)]+json.dumps(R,ensure_ascii=False,separators=(',',':'))+s[m.end(1):]
open(APP,'w',encoding='utf-8').write(s)
print(len(CH))
open('/tmp/fixlog.txt','w',encoding='utf-8').write('\n'.join(a+' | '+b+' → '+c for a,b,c in CH))
