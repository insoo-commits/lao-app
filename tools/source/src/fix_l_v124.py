# v12.4 (RYU): intervocalic ລ/ຫຼ inside a word gets ㄹ받침 in the Korean reading (까올리, 쌀라)
import json,re,sys
R=[("ເກົາຫຼີ",[("까오리","까올리"),("까오 리","까올리"),("까오리","까올리")]),
   ("ສະຫຼະ",[("싸라","쌀라")]),("ພະລະສຶກສາ",[("파라쓱싸","팔라쓱싸"),("파라 쓱싸","팔라쓱싸")]),
   ("ກໍລະກົດ",[("꺼라꼳","껄라꼳"),("꺼라 꼳","껄라꼳")]),("ກິລາ",[("끼라","낄라"),("끼 라","낄라")]),
   ("ໂທລະສັບ",[("토라쌉","톨라쌉"),("토라 쌉","톨라쌉")]),("ໂທລະທັດ",[("토라탇","톨라탇"),("토라 탇","톨라탇")]),
   ("ອັນຕະລາຍ",[("안따라이","안딸라이"),("안따 라이","안딸라이")]),
   ("ກະລຸນາ",[("까루나","깔루나"),("까 루나","깔루나"),("꺼루나","깔루나")]),
   ("ຜະລິດ",[("파릳","팔릳")]),("ສະຫຼາດ",[("싸랃","쌀랃")]),("ສະຫຼັດ",[("싸랃","쌀랃")]),
   ("ຕະຫຼາດ",[("따랃","딸랃")]),("ຕະຫຼອດ",[("따럳","딸럳"),("따 럳","딸럳")]),
   ("ຕາຕະລາງ",[("따따랑","따딸랑")]),("ສາລາ",[("싸라","쌀라")])]
APP=sys.argv[1];s=open(APP,encoding='utf-8').read()
i=s.find('const DATA=');j=s.find('\n',i);lit=s[i+11:j].rstrip(';')
d=json.loads(json.loads(lit[11:-1]));cnt={}
def fx(lo,rd):
    for w,subs in R:
        if w in lo:
            for a,b in subs:
                if a in rd: rd=rd.replace(a,b);cnt[w]=cnt.get(w,0)+1
    return rd
for k,b in d['B'].items():
    for w in b['w']:
        w[2]=fx(w[0],w[2])
        for e in w[4]: e[1]=fx(e[0],e[1])
    for p in b['pr']:
        for x in p: x[1]=fx(x[0],x[1])
    for x in b['dl']: x[2]=fx(x[1],x[2])
    if b.get('sm') and b['sm'][0]: b['sm'][1]=fx(b['sm'][0],b['sm'][1])
    for q in b.get('qz',[]):
        q[1]=fx(q[1],q[1])
        m=re.match(r'^(\S+) 의 한국어 독음',q[0])
        if m: q[1]=fx(m.group(1),q[1])
    b['tp']=[fx(t,t) for t in b['tp']]
new='const DATA=JSON.parse('+json.dumps(json.dumps(d,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+');'
s=s[:i]+new+s[j:]
m=re.search(r'NRD=(\{.*?\}),NFREQ=',s)
if m:
    nrd=json.loads(m.group(1));nrd={k:fx(k,v) for k,v in nrd.items()}
    s=s[:m.start(1)]+json.dumps(nrd,ensure_ascii=False,separators=(',',':'))+s[m.end(1):]
else: print('NRD not found')
open(APP,'w',encoding='utf-8').write(s);print(cnt)
