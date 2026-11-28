# v3.19 RYU: 듣기연습 소분류마다 11~12개 (lis_v319.py). usage: python3 build_v319.py app.js readings_v313.json
import json,re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import lis_v319 as C
APP=sys.argv[1];RD=json.load(open(sys.argv[2],encoding='utf-8'))
L=open(APP,encoding='utf-8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0]);D=json.loads(json.loads(m.group(1)));B=D['B']
def rd(lo):
    r=RD.get(lo);assert r and '[' not in r,('no reading',lo,r);return r
SPK={'ນ້ອຍ':'아이','ພໍ່':'아빠','ກະຕ່າຍ':'토끼','ເສືອ':'호랑이','ລູກຄ້າ':'손님','ພະນັກງານ':'직원','ເຈົ້າຂອງ':'주인','ພະຍາບານ':'간호사','ຄົນເຈັບ':'환자','ຄູ':'선생님','ນັກຮຽນ':'학생'}
NAR={'8-05':'선생님','8-06':'안내','8-07':'아나운서','8-08':'앵커'}
INTRO={'8-01':'노래처럼 짧게 반복되는 듣기예요. 0.8배속으로 먼저 들어 보세요.','8-02':'그림이 그려지는 짧은 동화예요. 0.8배속으로 먼저 들어 보세요.',
 '8-03':'라오스 옛이야기예요. 연결어(그래서·그런데)를 들어 보세요.','8-04':'두 사람의 대화예요. 1.0배속으로 들어 보세요.',
 '8-05':'학교에서 실제로 듣는 말이에요. 1.0배속으로 들어 보세요.','8-06':'안내 방송이에요. 숫자·시간·장소를 들어 보세요.',
 '8-07':'라디오에서 한 사람이 길게 말해요. 핵심 정보를 들어 보세요.','8-08':'뉴스 문장이에요. 언제·어디서·무엇을 들어 보세요. 1.0~1.2배속.'}
TAIL=' 듣는 순서: ❶ 본문 전체 듣기 → ❷ 문장별로 다시 듣기 → ❸ 확인퀴즈 → ❹ 받아쓰기(선택).'
SUB={p['id']:p for p in D['P']}['P9']['subs']
SB={'8-0'+str(i+1):s for i,s in enumerate(SUB)}
LT={}
for bid,title,lt,nar,lines,words,qz,tp in C.BUNDLES:
    assert bid not in B,bid;g=bid[:4]
    dl=[]
    for s,lo,ko in lines:
        sp=SPK[s] if s else (NAR.get(g,'') if nar else '')
        dl.append([sp,lo,rd(lo),ko])
    W=[]
    for lo,ko,note,li in words:
        assert lo in lines[li][1],(bid,lo)
        W.append([lo,ko+(' · '+note if note else ''),rd(lo),ko,[[lines[li][1],rd(lines[li][1]),lines[li][2]]]])
    Q=[list(q) for q in qz]+[[W[0][0]+' 의 뜻을 쓰세요.',W[0][3]]]
    B[bid]={'t':title,'h':' · '.join(w[0] for w in W),'i':INTRO[g]+TAIL,'w':W,'tp':list(tp),'nx':[],'pr':[],'dl':dl,'sm':None,'qz':Q,'lis':1,'nar':nar}
    SB[g]['b'].append(bid);LT[bid]=lt
for s in SUB:s['b']=sorted(s['b'])
print({s['id']:len(s['b']) for s in SUB})
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
i=next(k for k,l in enumerate(L) if l.startswith('const BLAB='))
L.insert(i+1,'/* v3.19 RYU: 듣기연습 늘리기 */Object.assign(BLAB,'+json.dumps({k:[B[k]['t'],''] for k in LT},ensure_ascii=False)+');')
open(APP,'w',encoding='utf-8').write('\n'.join(L));print('ok',len(LT))
