# v2.86 RYU: words from "LAO Lang 주제 묶음 추가 단어2.xlsx" (rows json /tmp/claude-0/up1/rows.json copy in src/v2/add_v286_rows.json)
import json,re,sys
APP=sys.argv[1];ROWS=json.load(open(sys.argv[2]))
L=open(APP,encoding='utf-8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0]);D=json.loads(json.loads(m.group(1)));B=D['B']
subs={x['id']:x for p in D['P'] for x in p['subs']}
head={}
for k,b in B.items():
    for w in b['w']:head.setdefault(w[0],[]).append(k)
def find(lo,src):
    if src not in head.get(lo,[]):src=next(k for k in head[lo] if k[0] in '54')
    for w in B[src]['w']:
        if w[0]==lo:
            w=json.loads(json.dumps(w));w[1]=w[1]+' · 원래 '+src;return w
    raise KeyError((lo,src))
added=[];skipped=[];nd={};nr={}
for r in ROWS:
    if r['b'].count('-')!=2:continue
    if r['lo'] in head:skipped.append(r['lo']+' '+r['ko']);continue
    b=B[r['b']];w=[r['lo'],r['ko'],r['rd'],r['ko'],[[e[0],e[1],e[2]] for e in r['ex']]]
    b['w'].append(w);b['h']=(b['h']+' · ' if b['h'] else '')+r['lo'];added.append(r['b']+' '+r['lo']);head[r['lo']]=[r['b']]
    if len(r['lo'])>=2:nd[r['lo']]=r['ko'].split(',')[0].strip();nr[r['lo']]=r['rd']
R={r['lo']:r for r in ROWS}
def new(lo,ko,rd,ex,hint=None):
    if len(lo)>=2:nd[lo]=ko;nr[lo]=rd
    return [lo,hint or ko,rd,ko,ex]
DAM=new('ດຳ','검다','담',[['ຜົມດຳ','폼 담','검은 머리'],['ກາເຟດຳ','까페 담','블랙커피'],['ໄປງານສົບໃຫ້ນຸ່ງສີດຳ ຫຼື ສີຂາວ','빠이 응안쏩 하이 눙 씨담 르 씨카오','장례식에는 검은색이나 흰색 옷을 입어요.']])
HUA=new('ຫົວ','웃다','후아',[['ຫົວມ່ວນ','후아 무안','즐겁게 웃어요.'],['ເປັນຫຍັງຫົວ?','뻰냥 후아?','왜 웃어요?'],['ໜັງເລື່ອງນີ້ທັງເຮັດໃຫ້ຫົວ ທັງເຮັດໃຫ້ໄຫ້','낭 르앙 니 탕 헫 하이 후아 탕 헫 하이 하이','이 영화는 웃기기도 하고 울리기도 해요.']],'웃다 · 머리(ຫົວ)와 같은 글자')
def pr(key):
    e=R[key]['ex'];return [[e[0][0],e[0][1],e[0][2]],[e[1][0],e[1][1],e[1][2]]]
def bun(t,i,ws,keys,tp):
    sm=R[keys[0]]['ex'][2];return {'t':t,'h':' · '.join(w[0] for w in ws),'i':i,'w':ws,'tp':tp,'nx':[],'pr':[pr(k) for k in keys],'dl':[],'sm':[sm[0],sm[1],sm[2]],
      'qz':[[ws[0][0]+' 의 뜻을 쓰세요.',ws[0][3]],["'"+ws[1][3]+"'를 라오스어로 쓰세요.",ws[1][0]+' ('+ws[1][2]+')']]}
NB={}
NB['4-04-18']=bun('새것·헌것, 길이, 무게, 빠르기','자주 쓰는 형용사를 반대말 짝으로 익혀요.',
  [find('ໃໝ່','5-10-03'),find('ເກົ່າ','5-10-04'),find('ຍາວ','5-16-02'),find('ສັ້ນ','5-08-02'),find('ໜັກ','5-16-03'),find('ເບົາ','5-16-03'),find('ໄວ','5-08-04'),find('ຊ້າ','5-08-05')],
  ['ໃໝ່ ↔ ເກົ່າ','ຍາວ ↔ ສັ້ນ','ໜັກ ↔ ເບົາ','ໄວ ↔ ຊ້າ'],['• ໃໝ່(새) ↔ ເກົ່າ(헌), ຍາວ(길다) ↔ ສັ້ນ(짧다), ໜັກ(무겁다) ↔ ເບົາ(가볍다), ໄວ(빠르다) ↔ ຊ້າ(느리다).','• ເກົ່າ(까오, 낡다)와 ເກົ້າ(까오, 9)는 부호만 달라요.'])
NB['4-04-19']=bun('쉽다·어렵다, 깨끗함, 많고 적음, 색, 참과 빔','자주 쓰는 형용사를 반대말 짝으로 익혀요.',
  [find('ງ່າຍ','5-10-05'),find('ຍາກ','5-10-06'),find('ສະອາດ','5-09-04'),find('ເປື້ອນ','5-09-04'),find('ຫຼາຍ','5-08-03'),find('ໜ້ອຍ','5-08-02'),find('ຂາວ','7-01-07'),DAM,find('ເຕັມ','5-09-01'),find('ຫວ່າງ','4-04-15')],
  ['ງ່າຍ ↔ ຍາກ','ສະອາດ ↔ ເປື້ອນ','ຫຼາຍ ↔ ໜ້ອຍ','ຂາວ ↔ ດຳ','ເຕັມ ↔ ຫວ່າງ'],['• ງ່າຍ ↔ ຍາກ, ສະອາດ ↔ ເປື້ອນ, ຫຼາຍ ↔ ໜ້ອຍ, ຂາວ ↔ ດຳ, ເຕັມ ↔ ຫວ່າງ.','• ຫວ່າງ은 ‘한가하다’와 ‘비어 있다’ 두 뜻이 있어요: ບ່ອນນັ່ງຫວ່າງ(빈자리).'])
NB['4-05-12']=bun('묻고 답하기·웃고 울기·서고 앉기','함께 기억하면 좋은 동작 반대말이에요.',
  [find('ຖາມ','5-04-05'),find('ຕອບ','5-04-05'),HUA,find('ໄຫ້','7-01-10'),find('ຢືນ','5-13-06'),find('ນັ່ງ','5-13-06')],
  ['ຖາມ ↔ ຕອບ','ຫົວ ↔ ໄຫ້','ຢືນ ↔ ນັ່ງ'],['• ຫົວ는 ‘웃다’와 ‘머리’ 두 뜻이에요. 문장을 보고 구별해요.'])
NB['4-03-06']=bun('~전·~후','때의 앞뒤를 나타내는 짝이에요.',[find('ກ່ອນ','5-05-01'),find('ຫຼັງ','5-05-02')],['ກ່ອນ ↔ ຫຼັງ'],['• ກ່ອນ/ຫຼັງ + 명사·동사: ກ່ອນອາຫານ(식전), ຫຼັງອາຫານ(식후).','• ຫຼັງຈາກ 은 ‘~한 다음에’: ຫຼັງຈາກກິນເຂົ້າ.'])
SG=R['ສົງສານ / ເຫັນໃຈ']['ex']
NB['5-07-11']={'t':'불쌍하다·공감하다','h':'ສົງສານ · ເຫັນໃຈ','i':'남의 어려움을 보고 드는 마음이에요.',
  'w':[new('ສົງສານ','불쌍히 여기다','쏭싼',[[SG[0][0],SG[0][1],SG[0][2]],['ໜ້າສົງສານຫຼາຍ','나 쏭싼 라이','정말 안됐어요.'],[SG[2][0],SG[2][1],SG[2][2]]]),
       new('ເຫັນໃຈ','공감하다, 마음을 이해하다','헨짜이',[[SG[1][0],SG[1][1],SG[1][2]],['ຂ້ອຍເຫັນໃຈເຈົ້າ','커이 헨짜이 짜오','당신 마음 이해해요.'],['ຂອບໃຈທີ່ເຫັນໃຈ','컵짜이 티 헨짜이','이해해 줘서 고마워요.']])],
  'tp':['• ສົງສານ: 불쌍하다, 안됐다(위에서 내려다보는 느낌도 있어요). ເຫັນໃຈ: 같은 마음이 되어 이해하다.'],'nx':[],'pr':[],'dl':[],'sm':None,
  'qz':[['ສົງສານ 의 뜻을 쓰세요.','불쌍히 여기다'],["'공감하다'를 라오스어로 쓰세요.",'ເຫັນໃຈ (헨짜이)']]}
for k,v in NB.items():
    assert k not in B;B[k]=v
subs['P4-C']['b']+=['4-04-18','4-04-19'];subs['P4-A']['b'].append('4-05-12');subs['P4-B']['b'].append('4-03-06');subs['P3-E']['b'].append('5-07-11')
B['1-02-01']['tp'].append('• 라오 숫자: ໐ 0, ໑ 1, ໒ 2, ໓ 3, ໔ 4, ໕ 5, ໖ 6, ໗ 7, ໘ 8, ໙ 9. 번호판이나 공문서에서 볼 수 있어요 (ປີ ໒໐໒໗ = 2027년).')
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
bl={k:[v['t'],''] for k,v in NB.items()}
bl['4-04-18'][1]='ໃໝ່·ເກົ່າ ຍາວ·ສັ້ນ ໜັກ·ເບົາ ໄວ·ຊ້າ';bl['4-04-19'][1]='ງ່າຍ·ຍາກ ສະອາດ·ເປື້ອນ ຫຼາຍ·ໜ້ອຍ ຂາວ·ດຳ ເຕັມ·ຫວ່າງ';bl['4-05-12'][1]='ຖາມ·ຕອບ ຫົວ·ໄຫ້ ຢືນ·ນັ່ງ';bl['4-03-06'][1]='ກ່ອນ·ຫຼັງ';bl['5-07-11'][1]='ສົງສານ·ເຫັນໃຈ'
i=next(k for k,l in enumerate(L) if l.startswith('const BLAB='))
L.insert(i+1,'/* v2.86 RYU: new bundles (word list 2) */Object.assign(BLAB,'+json.dumps(bl,ensure_ascii=False)+');')
j=next(k for k,l in enumerate(L) if l.startswith('/* v2.60 RYU: more whole compounds'))
L.insert(j+1,'/* v2.86 RYU: words from word list 2 */Object.assign(NDICT,'+json.dumps(nd,ensure_ascii=False)+');Object.assign(NRD,'+json.dumps(nr,ensure_ascii=False)+');')
open(APP,'w',encoding='utf-8').write('\n'.join(L))
print('added',len(added));print('skipped',skipped)
