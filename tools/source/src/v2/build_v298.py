# v2.98 RYU (점검표 1번): readings 웨라·카우, Korean out of the Lao field, example = headword fixes, 확인 문제 at least 5.
# usage: python3 build_v298.py app.js   -> prints the Lao texts that need new audio
import json,re,sys
APP=sys.argv[1];L=open(APP,encoding='utf8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0]);D=json.loads(json.loads(m.group(1)));B=D['B']
NEWLO=set()
# --- 1. readings: ເວລາ = 웨라, ຂ່າວ = 카우 (ເຂົ້າ·ຂາວ·ເຂົາ stay 카오)
KAO=re.compile(r'ຂ່າວ|ເຂົ້າ|ເຂົ່າ|ຂາວ|ເຂົາ|ເຄົາ')
def fixrd(lo,rd):
    if not rd:return rd
    rd=rd.replace('웰라','웨라')
    if 'ຂ່າວ' in lo:
        ws=KAO.findall(lo);pos=[mm.start() for mm in re.finditer('카오',rd)]
        if len(ws)==len(pos):
            r=list(rd)
            for w,p in zip(ws,pos):
                if w=='ຂ່າວ':r[p+1]='우'
            rd=''.join(r)
        else:print('KAO?',lo,rd)
    return rd
for b in B.values():
    for w in b.get('w') or []:
        w[2]=fixrd(w[0],w[2])
        for e in w[4] or []:e[1]=fixrd(e[0],e[1])
    for d in b.get('dl') or []:d[2]=fixrd(d[1],d[2])
    for p in b.get('pr') or []:
        for x in p:
            if isinstance(x,list):x[1]=fixrd(x[0],x[1])
    if b.get('qz'):
        for q in b['qz']:
            if 'ຂ່າວ' in q[1]:q[1]=q[1].replace('카오','카우')
            q[1]=q[1].replace('웰라','웨라')
# --- 2. Lao field without Korean: headword -> real Lao phrase (old label kept in the hint)
HEAD={  # (bundle, old headword): (new lo, reading, meaning)
 ('4-02-02','ໂຕ (동물)'):('ໝາສອງໂຕ','마 썽 또','개 두 마리'),
 ('4-02-02','ໂຕ (옷)'):('ເສື້ອສາມໂຕ','쓰아 쌈 또','셔츠 세 벌'),
 ('4-02-02','ໂຕ (글자)'):('ຕົວອັກສອນສິບໂຕ','뚜아악썬 씹 또','글자 열 자'),
 ('4-02-02','ໂຕ (가구)'):('ຕັ່ງສີ່ໂຕ','땅 씨 또','의자 네 개'),
 ('4-02-02','ໜ່ວຍ (산)'):('ພູສາມໜ່ວຍ','푸 쌈 누아이','산 세 개'),
 ('4-02-02','ຄັນ (차)'):('ລົດສອງຄັນ','롣 썽 칸','차 두 대'),
 ('4-02-02','ຄັນ (우산)'):('ຮົ່ມສາມຄັນ','홈 쌈 칸','우산 세 개'),
 ('4-02-02','ຄັນ (숟가락)'):('ບ່ວງສອງຄັນ','부앙 썽 칸','숟가락 두 개'),
 ('4-02-05','ໃບ (서류)'):('ໃບຂັບຂີ່','바이캅키','운전면허증'),
 ('4-02-06','ຫົວ (알뿌리)'):('ຜັກບົ່ວສອງຫົວ','팍부아 썽 후아','양파 두 개'),
 ('4-02-06','ເມັດ (단추·씨)'):('ກະດຸມສາມເມັດ','까둠 쌈 멛','단추 세 개'),
 ('4-02-10','ຈັກ + 분류사'):('ຈັກຄົນ','짝 콘','몇 명?'),
 ('4-02-10','ທີ + 숫자'):('ທີໜຶ່ງ','티 능','첫 번째'),
 ('4-02-10','분류사 + ລະ'):('ຄົນລະສອງ','콘라 썽','한 사람당 두 개씩'),
 ('4-02-10','ທັງ + 숫자 + 분류사'):('ທັງສອງຄົນ','탕 썽 콘','두 사람 모두'),
 ('4-02-10','ອີກ + 숫자 + 분류사'):('ອີກສອງອັນ','익 썽 안','두 개 더'),
 ('6-08-12','ຖືກ (피동)'):('ຖືກລັກ','특락','도둑맞다'),
 ('3-03-01','ໂຕ (동물)'):('ໝາສອງໂຕ','마 썽 또','개 두 마리'),
 ('3-03-01','ຄັນ (차)'):('ລົດສອງຄັນ','롣 썽 칸','차 두 대'),
 ('3-03-02','ຖືກ (수동)'):('ຖືກ',None,None),
 ('3-03-02','ໃຫ້ (사역)'):('ໃຫ້',None,None),
 ('2-02-03','◌ວ◌ (ອົວ + 받침)'):('ສວນ','쑤안','밭, 공원'),
}
for (bid,old),(lo,rd,ko) in HEAD.items():
    w=next(w for w in B[bid]['w'] if w[0]==old)
    lab=old.split(' ',1)[1].strip('()') if ' ' in old else ''
    w[0]=lo;NEWLO.add(lo)
    if rd:w[2]=rd
    if ko:
        w[3]=ko
        if lab and lab not in w[1]:w[1]=lab+' · '+w[1]
    else:
        w[1]=w[1] if lab in w[1] else lab+' · '+w[1]
    hs=[x[0] for x in B[bid]['w']];assert len(hs)==len(set(hs)),(bid,hs)
# examples with Korean in the Lao field, and examples that only repeat the headword
EX={('1-05-02','ໄປຊື່ໆ','ຊື່ (곧다)'):('ໄປຊື່ໆ ຮອດສີ່ແຍກ','빠이 쓰쓰 헏 씨냭','곧장 가서 사거리까지 가요.'),
 ('1-07-02','ເວົ້າຕາມ','ຕາມ (따르다)'):('ເວົ້າຕາມຄູເດີ້','와오 땀 쿠 더','선생님을 따라 말해요.'),
 ('5-07-08','ຊອບ','ມັກ (라오)'):('ຂ້ອຍມັກກິນເຝີ','커이 막 낀 퍼','저는 쌀국수를 좋아해요. (라오스에서는 ມັກ을 써요)'),
 ('1-01-07','ຍັງ','ຍັງ'):('ຍັງບໍ່ທັນກິນ','냥 버탄 낀','아직 안 먹었어요.'),
 ('5-03-05','ຍັງ','ຍັງ'):('ລາວຍັງບໍ່ທັນມາ','라오 냥 버탄 마','그는 아직 안 왔어요.'),
 ('3-01-03','ຍັງ','ຍັງ'):('ຍັງບໍ່ທັນແລ້ວ','냥 버탄 래우','아직 안 끝났어요.'),
 ('7-04-08','ຍັງ','ຍັງ'):('ຍັງເຮັດວຽກຢູ່','냥 헫위악 유','아직 일하고 있어요.'),
 ('7-09-03','ຍັງ','ຍັງ'):('ຍັງບໍ່ທັນຮອດ','냥 버탄 헏','아직 도착 안 했어요.'),
 ('1-09-04','ນ້ຳມູກໄຫຼ','ນ້ຳມູກໄຫຼ'):('ຂ້ອຍເປັນຫວັດ ນ້ຳມູກໄຫຼ','커이 뻰 왇, 남묵 라이','감기에 걸려서 콧물이 나요.'),
 ('1-10-04','ສາຍບໍ່ຫວ່າງ','ສາຍບໍ່ຫວ່າງ'):('ໂທໄປແລ້ວ ແຕ່ສາຍບໍ່ຫວ່າງ','토 빠이 래우, 때 싸이 버 왕','전화했는데 통화 중이에요.'),
 ('4-05-10','ໄດ້','ໄດ້'):('ນັ່ງບ່ອນນີ້ໄດ້','낭 번 니 다이','여기 앉아도 돼요.'),
 ('5-05-04','ເຄີຍ','ເຄີຍ'):('ເຄີຍໄປຫຼວງພະບາງ','크이 빠이 루앙파방','루앙프라방에 가 본 적 있어요.'),
 ('4-06-08','ຍິນດີ','ຍິນດີ'):('ຍິນດີທີ່ໄດ້ຊ່ວຍ','닌디 티 다이 쑤아이','도울 수 있어서 기뻐요.'),
 ('2-02-03','ເອົາ','ເອົາ'):('ເອົາອັນນີ້','아오 안 니','이거 주세요.'),
}
for (bid,head,old),(lo,rd,ko) in EX.items():
    w=next(w for w in B[bid]['w'] if w[0]==head);e=next(e for e in w[4] if e[0]==old)
    e[:3]=[lo,rd,ko];NEWLO.add(lo)
# --- 3. 확인 문제: at least 5 per bundle (from the words and their examples)
for bid,b in B.items():
    if b.get('info') or b.get('lis') or not b.get('qz') or len(b['qz'])>=5:continue
    have={q[0] for q in b['qz']};add=[]
    for w in b['w']:
        for e in w[4] or []:
            if len(e[0])>3 and e[0]!=w[0]:add.append(["'%s'를 라오스어로 쓰세요."%e[2].rstrip('.'),'%s (%s)'%(e[0],e[1])])
    for w in b['w']:add.append(['%s 의 뜻을 쓰세요.'%w[0],w[3]])
    for q in add:
        if len(b['qz'])>=5:break
        J=json.dumps(b['qz'],ensure_ascii=False)
        if q[0] not in have and q[1].split(' (')[0] not in J and re.sub(r"^'|'를.*$| 의 뜻.*$",'',q[0]) not in J:b['qz'].append(q);have.add(q[0])
    print('qz',bid,len(b['qz']))
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
L=[l.replace('"ຂ່າວ":"카오"','"ຂ່າວ":"카우"') for l in L]
open(APP,'w',encoding='utf8').write('\n'.join(L));json.dump(sorted(NEWLO),open('/tmp/claude-0/up3/newlo.json','w'),ensure_ascii=False);print('newlo',len(NEWLO))
