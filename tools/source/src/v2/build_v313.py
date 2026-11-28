# v3.13 RYU: 핵심회화 -> 기초회화 (01 인사·기본 표현), 숙소·집 / 은행·통신·관공서 / 축제·경조사 보강, 새 소분류 직장생활,
#  문장규칙 04 부탁·조건·전하기, 문자학습 04 숫자·기호 + 05 간판 읽기.
# usage: python3 build_v313.py app.js readings.json      (readings.json = {lao: korean reading})
import json,re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import content_v313_p5 as C5, content_v313_p76 as C7
APP=sys.argv[1];RD=json.load(open(sys.argv[2],encoding='utf-8'))
L=open(APP,encoding='utf-8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0])
D0=json.loads(json.loads(m.group(1)));B0=D0['B']
MAP=dict(C5.MOVE)
for a,b in MAP.items():assert a in B0 and b not in B0,(a,b)
rx=re.compile(r'(?<![\d-])(\d-\d\d-\d\d)(?![\d])')
sub_=lambda s:rx.sub(lambda mm:MAP.get(mm.group(1),mm.group(1)),s)
D=json.loads(sub_(json.loads(m.group(1))));B=D['B']
P={p['id']:p for p in D['P']};SUBS={x['id']:x for p in D['P'] for x in p['subs']}
def rd(lo):
    if '…' in lo:
        parts=lo.split('…');toks=iter(RD[lo.replace('…',' ')].split());assert len(RD[lo.replace('…',' ')].split())==len([x for x in parts if x]),lo
        return '…'.join(next(toks) if x else '' for x in parts)
    r=RD.get(lo) or RD.get(lo.replace('…',' '))
    assert r and '[' not in r,('no reading',lo,r);return r
head={}
for k,b in B.items():
    for w in b['w']:head.setdefault(w[0],[]).append(k)
NX={'3-04-03':['접속사 → 3-03-04'],'3-04-01':['말투·끝말 → 3-02-03'],'2-04-01':['숫자 → 1-02-01'],'2-05-02':['교통 → 1-05-01'],'2-05-03':['식당 → 1-03-01']}
def build(t):
    bid,title,intro,words,tips,dl,sm=t
    W=[]
    for lo,ko,note,ex in words:
        if lo in head and not all(k.startswith('8-') for k in head[lo]):print('  dup headword',bid,lo,head[lo])
        W.append([lo,ko+(' · '+note if note else ''),rd(lo),ko,[[e,rd(e),k] for e,k in ex]])
    plain=[w for w in W if '…' not in w[0] and not re.search('[໐-໙]',w[0])] or W
    qz=[[W[0][4][0][0]+' 의 뜻을 쓰세요.',W[0][4][0][2]],
        ['‘'+plain[1%len(plain)][3]+'’를 라오스어로 쓰세요.',plain[1%len(plain)][0]+' ('+plain[1%len(plain)][2]+')']]
    for w in plain[2:]:
        e=next((e for e in w[4] if w[0] in e[0] and e[0]!=w[0]),None)
        if e:qz.append(['빈칸에 알맞은 말: '+e[0].replace(w[0],'____',1)+'  ('+e[2]+')',w[0]]);break
    a,b=plain[3%len(plain)],plain[4%len(plain)]
    if a is not b:
        opts=[a[0],b[0]] if len(bid)%2==0 and int(bid[-1])%2 else [b[0],a[0]]
        qz.append(['‘'+a[3]+'’는 어느 쪽?  ① '+opts[0]+'  ② '+opts[1],'①' if opts[0]==a[0] else '②'])
    z=plain[-1];qz.append([z[0]+' 의 한국어 독음과 뜻은?',z[2]+', '+z[3]])
    return {'t':title,'h':' · '.join(w[0] for w in W),'i':intro,'w':W,'tp':list(tips),'nx':NX.get(bid,[]),'pr':[],
            'dl':[[s,lo,rd(lo),ko] for s,lo,ko in dl],'sm':[sm[0],rd(sm[0]),sm[1]],'qz':qz}
NB={}
for t in C5.BUNDLES+C7.BUNDLES:
    assert t[0] not in B and t[0] not in NB,t[0];NB[t[0]]=build(t)
B.update(NB)
# subs
for sid,(name,ids) in C5.SUBS.items():SUBS[sid]['name']=name;SUBS[sid]['b']+=ids
SUBS['P5-K']['name']='인사·기본 표현';P['P5']['ko']='기초회화'
sid,name,ids=C5.NEWSUB;assert sid not in SUBS;P['P5']['subs'].append({'id':sid,'name':name,'b':ids})
for pid,sid,name,ids in C7.NEWSUBS:assert sid not in SUBS;P[pid]['subs'].append({'id':sid,'name':name,'b':ids})
for p in D['P']:
    for x in p['subs']:
        x['b'].sort();assert len({b[:4] for b in x['b']})==1,x['id']
allb=[b for p in D['P'] for x in p['subs'] for b in x['b']];assert len(allb)==len(set(allb))==len(B),(len(allb),len(set(allb)),len(B))
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
for i,l in enumerate(L):
    if i==0 or 'const IDMAP' in l:continue
    if rx.search(l):L[i]=sub_(l)
# menu name
i=next(i for i,l in enumerate(L) if '/* v2.81 RYU: menu names */' in l);assert 'P5:"핵심회화"' in L[i];L[i]=L[i].replace('P5:"핵심회화"','P5:"기초회화"')
# BLAB
LT={'1-08-05':'ພາຍໃນເຮືອນ','1-08-06':'ຊອກເຊົ່າເຮືອນ','1-08-07':'ເຄື່ອງຄົວ','1-08-08':'ແຕ່ງກິນ','1-10-05':'ວີຊາ ແລະ ເອກະສານ','1-10-06':'ສະຖານີຕຳຫຼວດ',
    '1-10-07':'ໄປສະນີ ແລະ ພັດສະດຸ','1-12-04':'ງານແຕ່ງດອງ','1-12-05':'ງານສົບ','1-12-06':'ເກີດລູກ ແລະ ວັນເກີດ','1-12-07':'ຄຳອວຍພອນ ແລະ ຄຳປອບໃຈ',
    '1-13-01':'ບໍລິສັດ ແລະ ການໄປວຽກ','1-13-02':'ກອງປະຊຸມ','1-13-03':'ຕາຕະລາງ ແລະ ນັດໝາຍ','1-13-04':'ຂໍຮ້ອງ ແລະ ລາຍງານ','1-13-05':'ລົມກັບເພື່ອນຮ່ວມງານ',
    '3-04-01':'ການຊວນ ແລະ ຂໍຮ້ອງ','3-04-02':'ຫ້າມ ຕ້ອງ ແລະ ອະນຸຍາດ','3-04-03':'ເງື່ອນໄຂ','3-04-04':'ການເລົ່າຄຳເວົ້າ',
    '2-04-01':'ຕົວເລກລາວ','2-04-02':'ເຄື່ອງໝາຍ ແລະ ຕົວຫຍໍ້','2-05-01':'ປ້າຍຮ້ານ','2-05-02':'ປ້າຍທາງ','2-05-03':'ປ້າຍແຈ້ງການ'}
assert set(LT)==set(NB)
i=next(k for k,l in enumerate(L) if l.startswith('const BLAB='))
L.insert(i+1,'/* v3.13 RYU: new bundles */Object.assign(BLAB,'+json.dumps({k:[NB[k]['t'],LT[k]] for k in NB},ensure_ascii=False)+');')
# NDICT / NRD for the ※ notes
nm=re.search(r'const NDICT=(\{.*?\}),NRD=','\n'.join(L));ND=json.loads(nm.group(1)) if nm else {}
nd={};nr={}
for k,b in NB.items():
    for w in b['w']:
        lo=w[0]
        if len(lo)>=2 and '…' not in lo and not re.search('[໐-໙.]',lo) and lo not in ND and lo not in head:
            nd[lo]=re.split('[,(]',w[3])[0].strip();nr[lo]=w[2]
j=next(k for k,l in enumerate(L) if l.startswith('/* v2.60 RYU: more whole compounds'))
L.insert(j+1,'/* v3.13 RYU: new words */Object.assign(NDICT,'+json.dumps(nd,ensure_ascii=False)+');Object.assign(NRD,'+json.dumps(nr,ensure_ascii=False)+');')
# saved progress: moved bundle ids (known, 선택, 완료, 틀린 단어, 별표)
k=next(i for i,l in enumerate(L) if l.startswith('/* v3.02 RYU: 학습 기록'))
L.insert(k+1,'/* v3.13 RYU: 같이 쓰는 말 1-08-05 -> 1-08-09, 1-10-05 -> 1-10-08, 1-12-04 -> 1-12-08 */const IDMAP13='+json.dumps(MAP)+';if(store.get("lao-idv",0)<23){const mv=o=>{const r={};for(const k in o){const m=/^(\\d-\\d{2}-\\d{2})(.*)$/.exec(k);r[m&&IDMAP13[m[1]]?IDMAP13[m[1]]+m[2]:k]=o[k]}return r};known=mv(known);store.set("lao-known",known);DONE=mv(DONE);store.set("lao-done",DONE);WRONG=mv(WRONG);store.set("lao-wrong",WRONG);STAR=mv(STAR);store.set("lao-star",STAR);if(saved.bun){for(const k in saved.bun)if(IDMAP13[saved.bun[k]])saved.bun[k]=IDMAP13[saved.bun[k]];store.set("lao-sel",saved)}store.set("lao-idv",23)}')
open(APP,'w',encoding='utf-8').write('\n'.join(L))
print('ok bundles',len(B),'new',len(NB),'ndict',len(nd))
