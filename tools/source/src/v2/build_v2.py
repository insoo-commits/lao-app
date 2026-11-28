# v2.0: 말소리(P1) rebuilt around confusable sounds (p1_spec.txt + build_p1.py),
#       말뿌리(P2) cleaned to root-family words, new root bundles, migration IDMAP7 / lao-idv 17.
# usage: python3 build_v2.py /path/to/app.js [--dry]
import json,re,sys,copy,collections,os
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
import build_p1
APP=sys.argv[1];DRY='--dry' in sys.argv
s=open(APP,encoding='utf-8').read();first,rest=s.split('\n',1)
m=re.match(r'const DATA=JSON\.parse\((".*")\)(;?)\s*$',first)
D=json.loads(json.loads(m.group(1)));B=D['B'];O=copy.deepcopy(B)
NB,psubs,ib=build_p1.build(D)
ORD=sorted(O,key=lambda b:({'5':0,'4':1,'1':2,'2':3,'3':4}[b[0]],b))
def entry(lo,src=None):
    for bid in ([src] if src else ORD):
        for w in O[bid]['w']:
            if w[0]==lo:
                w=copy.deepcopy(w);w[1]=re.sub(r' · 원래 \d-\d\d-\d\d','',w[1]);return w
    raise KeyError((lo,src))
def trip(w):return [w[0],w[2],w[3]]
def exof(w,need=True):
    c=[e for e in w[4] if e[0].count(w[0])==1] if need else list(w[4])
    return min(c,key=lambda e:len(e[0])) if c else None
def qhit(q,r):
    Q,A=q
    if A==r or A.startswith(r+' ('):return True
    if Q.startswith(r+' 의 한국어'):return True
    mm=re.search(r'① (.+?)  ② (.+)$',Q)
    return bool(mm and r in (mm.group(1).strip(),mm.group(2).strip()))
def fixqz(b,removed):
    W=b['w'];qz=[q for q in b['qz'] if not any(qhit(q,r) for r in removed)]
    have=' '.join(q[0]+q[1] for q in qz);cand=[]
    for w in W:
        if w[0] in have:continue
        e=exof(w)
        cand.append([f"‘{w[3]}’를 라오스어로 쓰세요.",f"{w[0]} ({w[2]})"])
        if e:cand.append([f"빈칸에 알맞은 말: {e[0].replace(w[0],' ____ ').strip()}  ({e[2].rstrip('.')})",w[0]])
        cand.append([f"{w[0]} 의 한국어 독음과 뜻은?",f"{w[2]}, {w[3]}"])
    for w in W:
        cand.append([f"{w[0]} 의 한국어 독음과 뜻은?",f"{w[2]}, {w[3]}"])
        cand.append([f"‘{w[3]}’를 라오스어로 쓰세요.",f"{w[0]} ({w[2]})"])
    for c in cand:
        if len(qz)>=5:break
        if c not in qz and not any(c[1]==q[1] for q in qz):qz.append(c)
    for c in cand:
        if len(qz)>=5:break
        if c not in qz:qz.append(c)
    b['qz']=qz
def autoqz(W):
    qz=[];e=exof(W[0],False);qz.append([f"{e[0]} 의 뜻을 쓰세요.",e[2].rstrip('.')])
    w=W[1];qz.append([f"‘{w[3]}’를 라오스어로 쓰세요.",f"{w[0]} ({w[2]})"])
    for w in W[2:]+W:
        e=exof(w)
        if e:qz.append([f"빈칸에 알맞은 말: {e[0].replace(w[0],' ____ ').strip()}  ({e[2].rstrip('.')})",w[0]]);break
    a,b=W[-2],W[-1];qz.append([f"‘{b[3]}’는 어느 쪽?  ① {a[0]}  ② {b[0]}","②"])
    w=W[min(3,len(W)-1)] if len(W)>3 else W[0];qz.append([f"{w[0]} 의 한국어 독음과 뜻은?",f"{w[2]}, {w[3]}"])
    return qz
# ---------------- P2 clean-up ----------------
RM={'4-01-04':'ເມົາ','4-01-09':'ແກ້ວ','4-01-21':'ສ້ອມແປງ','4-01-24':'ຫາຍ','4-02-07':'ເຮືອນ','4-03-09':'ໄຮ່','4-03-10':'ຄວາຍ ງົວ ໝູ ໄກ່','4-04-02':'ອາຍຸ','4-05-06':'ອ້າຍ ເອື້ອຍ','4-06-03':'ເຮືອນ','4-06-05':'ປະຊາຊົນ','4-07-04':'ເຝີ ເຂົ້າປຸ້ນ ໝີ່','4-07-05':'ຕ່ຳຫູກ','4-08-01':'ຢ່າງໜ້ອຍ','4-08-08':'ແຂ່ງ ແຂ່ງຂັນ','4-09-02':'ອາຈານ','4-09-09':'ປຶ້ມ ໜັງ','4-09-12':'ນາມສະກຸນ','4-10-05':'ເກີບ','4-10-07':'ຖືພາ','4-11-02':'ສຸຂະພາບ','4-11-05':'ຄວາມຊົງຈຳ','4-12-06':'ຮົ່ມ ນ້ຳຖ້ວມ','4-13-02':'ນັກຮ້ອງ','4-13-03':'ເຕັ້ນ ສະແດງ','4-13-05':'ສາລາ'}
DEL=['4-03-12','4-03-13','4-05-09','4-13-01']
# (destination, word, source bundle or None, hint override or None)
ADD=[
('3-08-02','ນິດໜ່ອຍ',None,None),('3-08-02','ເລັກນ້ອຍ',None,None),('3-08-02','ຢ່າງໜ້ອຍ',None,None),
('4-05-07','ໜຸ່ມສາວ',None,None),('4-05-09x','ໝໍແຂ້ວ',None,None),('4-03-03','ໝໍ້ຫຸງເຂົ້າ',None,None),
('4-06-09','ຂ້າງນອກ',None,None),('4-06-09','ຂ້າງໃນ',None,None),
('1-12-03','ກຳນົດ',None,'정하다, 일정 · 날짜와 시간을 정할 때'),('1-12-03','ເຊື້ອເຊີນ',None,None),('1-12-03','ສະແດງ',None,'공연하다, 보여 주다 · ການສະແດງ = 공연'),
('1-01-03','ຄອບຄົວ',None,'가족 · ຄອບ(돌보다) + ຄົວ(살림)'),('1-01-03','ນາມສະກຸນ',None,None),
('4-06-10','ກາງວັນ',None,None),('1-06-02','ຂັ້ນໄດ',None,None),
('1-10-02','ສື່ສານ',None,'소통하다, 통신 · ສື່(매체) + ສານ(소식)'),('3-13-07','ສີແຂ້ວ',None,None),('2-04-14','ສົມຄວນ',None,None),
('1-06-03','ຊົມເຊີຍ',None,None),('1-09-01','ຊົງຜົມ',None,None),('4-09-01','ຊັ້ນຮຽນ',None,None),
('3-14-04','ສັນຍາ',None,'약속(하다), 계약 · 꼭 지키겠다는 말'),
('1-08-02','ບັນຫາ',None,'문제 · 곤란한 일'),('1-08-02','ສ້ອມແປງ',None,None),
('4-03-01','ບໍ່ນ້ຳ',None,'우물 · ບໍ່(샘·구덩이) + ນ້ຳ(물)'),('4-03-01','ນ້ຳຖ້ວມ',None,None),
('1-07-09','ໃສ່ບາດ',None,None),('1-07-09','ຕ່ຳຫູກ',None,None),('1-07-09','ສາລາ',None,'정자, 법당 회관 · 절이나 마을의 쉼터'),
('1-07-11','ຫຼວງພະບາງ',None,None),('3-01-04','ປານໃດ',None,None),('3-02-06','ແບ່ງປັນ',None,None),
('4-11-01','ພໍໃຈ',None,None),('4-11-01','ທັນໃຈ',None,None),('2-01-01','ຕົນເອງ',None,None),
('4-04-06','ຕອນທ່ຽງ',None,None),('3-12-01','ແຕ່ງດອງ',None,'결혼하다 · ແຕ່ງ(꾸미다) + ດອງ(혼인으로 맺다)'),
('3-04-02','ດູແລ',None,None),('3-08-06','ໂດ່ງດັງ',None,None),('2-03-01','ພາກໃຕ້',None,None),('3-04-05','ໄຕ່ຖາມ',None,None),
('1-07-10','ຮີດຄອງ',None,None),('3-12-03','ເລກທີ',None,None),('4-07-01','ຫໍ່ເຄື່ອງ',None,None),
('4-02-01','ຢຸດລົດ',None,None),('4-01-23','ຢຸດພັກ',None,None),
('4-05-06','ຍາດພີ່ນ້ອງ',None,None),('4-05-06','ຍາດ',None,'친척 · ‘빼앗다’와 같은 글자'),
('1-03-05','ເມົາ',None,'취하다 · 멀미에도 써요'),('4-14-03','ປະຊາຊົນ',None,None),('1-09-05','ຖືພາ',None,'임신하다 · 공손한 말'),
('4-14-01','ຄວາມຊົງຈຳ',None,None),('2-05-04','ແຂ່ງຂັນ',None,None),('1-03-04','ຂົ້ວ',None,'볶다 · 기름에 볶는 조리법'),
('2-04-09','ລົດຊາດ',None,None),('1-07-18','ບານເຕະ',None,None),('1-07-18','ເປຕັງ',None,None),('1-07-16','ລອຍນ້ຳ',None,None),
('4-03-10','ສວນສັດ','4-03-09',None),
('4-06-05','ເພງຊາດ','4-13-02',None),('4-06-05','ທຸງຊາດ','1-07-07',None),
('4-13-03','ລຳວົງ','1-12-01',None),
]
ADD=[(('4-05-10' if d=='4-05-09x' else d),lo,src,h) for d,lo,src,h in ADD]
HINT={('4-06-05','ຊາດ'):'민족, 국가 · 나라를 이루는 겨레'}
TITLE={'4-06-05':'ປະເທດ·ຊາດ 나라·민족','4-05-06':'ພີ່·ນ້ອງ 형제·친척','4-13-03':'ຟ້ອນ·ລຳ 춤·노래'}
INTRO={'4-03-10':'ສັດ(싿)은 ‘동물’입니다.','4-13-03':'라오스 전통 춤 ຟ້ອນ(펀)과 전통 노래 ລຳ(람)입니다.','4-06-05':'나라 ປະເທດ(빠텓)과 민족·국가 ຊາດ(싿)이 들어간 말입니다.'}
TPSET={'4-03-10':(1,'• ສັດລ້ຽງ(기르는 동물 → 가축·반려동물), ສວນສັດ(동물의 정원 → 동물원).'),
 '4-07-04':(0,'• 국수 이름은 주제별 ‘국수 종류’ 묶음에 있어요: ເຝີ(쌀국수), ເຂົ້າປຸ້ນ(카오뿐), ໝີ່(밀국수).'),
 '4-13-03':(0,'• 전통 춤 ຟ້ອນ ↔ 현대 춤 ເຕັ້ນ. 둥글게 돌며 추는 춤이 ລຳວົງ입니다.')}
TPADD={'4-05-06':'• ຍາດພີ່ນ້ອງ(친척)은 ຍາດ(친족)과 ພີ່ນ້ອງ(형제)을 합친 말입니다.',
 '4-06-05':'• ຊາດ(민족·국가)가 붙은 말: ທຸງຊາດ(국기), ເພງຊາດ(국가).',
 '3-08-02':'• ‘조금’은 말할 때 ນິດໜ່ອຍ, 글이나 격식 있는 자리에서는 ເລັກນ້ອຍ. ຢ່າງໜ້ອຍ는 ‘적어도’입니다.',
 '4-06-09':'• 안팎 짝: ຂ້າງນອກ(바깥쪽) ↔ ຂ້າງໃນ(안쪽).'}
PRSET={'4-05-06':('ພີ່','ນ້ອງ'),'4-03-10':('ສັດລ້ຽງ','ສວນສັດ'),'4-07-04':('ເສັ້ນທາງ','ເສັ້ນຜົມ'),'4-08-08':('ແຂງແຮງ','ນ້ຳແຂງ'),'4-13-03':('ຟ້ອນລຳວົງ','ໝໍລຳ')}
NEW=[
dict(sub='P2-K',t='ເສຍ 잃다·상하다',i='ເສຍ(씨야)는 ‘잃다, 상하다, 고장 나다’입니다. 뒤에 잃은 것을 붙여 말을 만듭니다.',
 w=[('ເສຍ','5-07-10','잃다, 고장 나다 · 뒤에 잃은 것을 붙여요'),('ເສຍເວລາ',None,None),('ເສຍເງິນ','4-07-02',None),('ເສຍໃຈ','4-11-01',None),('ເສຍດາຍ',None,'아깝다, 아쉽다 · 잃어서 아까운 마음'),('ທ້ອງເສຍ','4-10-07',None)],
 tp=['• ເສຍ + 잃은 것: ເສຍເວລາ(시간을 잃다 → 낭비하다), ເສຍເງິນ(돈을 쓰다), ເສຍໃຈ(마음이 상하다 → 슬프다).','• 물건이 고장 났을 때도 ເສຍ: ໂທລະສັບເສຍ(전화기가 고장 났어요). 배탈은 ທ້ອງເສຍ(배가 상하다).'],
 pr=('ເສຍເວລາ','ເສຍເງິນ'),sm=['ລົດເສຍ ເສຍເວລາຫຼາຍ ເສຍດາຍແທ້','롣 씨야 씨야웨라 라이 씨야다이 태','차가 고장 나서 시간을 많이 버렸어요. 정말 아까워요.']),
dict(sub='P2-H',t='ທ່ຽງ 한가운데 때',i='ທ່ຽງ(티앙)은 ‘한가운데 때’입니다. 낮의 한가운데는 정오, 밤의 한가운데는 자정입니다.',
 w=[('ທ່ຽງ','5-05-08','정오, 낮 12시 · 하루의 한가운데'),('ຕອນທ່ຽງ',None,None),('ທ່ຽງຄືນ',None,None)],
 tp=['• ທ່ຽງ만 쓰면 정오입니다. ຕອນທ່ຽງ(정오 무렵 → 점심때), ທ່ຽງຄືນ(밤의 한가운데 → 자정).','• 점심밥은 ເຂົ້າທ່ຽງ(정오의 밥)이라고 합니다.'],
 pr=('ຕອນທ່ຽງ','ທ່ຽງຄືນ'),sm=['ຕອນທ່ຽງກິນເຂົ້າ ທ່ຽງຄືນນອນ','떤 티앙 낀 카오 티앙큰 넌','정오에는 밥을 먹고 자정에는 자요.']),
dict(sub='P2-B',t='ເຈົ້າ·ນາຍ 주인·우두머리',i='ເຈົ້າ(짜오)와 ນາຍ(나이)는 둘 다 ‘주인, 높은 사람’입니다. 뒤에 맡은 것을 붙입니다.',
 w=[('ເຈົ້າ','2-01-02','너, 당신 · 본뜻은 ‘주인, 님’'),('ເຈົ້າຂອງ','4-07-07',None),('ເຈົ້າເມືອງ','4-06-04',None),('ເຈົ້າບ່າວ','4-05-07',None),('ເຈົ້າສາວ','4-05-07',None),('ນາຍ','5-01-10','우두머리, 주인 · 남자를 높여 ‘~씨’로도 써요'),('ນາຍຈ້າງ',None,None)],
 tp=['• ເຈົ້າ는 ‘너, 당신’으로 가장 많이 쓰지만 본뜻은 ‘주인, 님’입니다: ເຈົ້າຂອງ(물건의 주인), ເຈົ້າເມືອງ(고을의 주인 → 군수).','• 결혼식의 두 주인공: ເຈົ້າບ່າວ(신랑)·ເຈົ້າສາວ(신부).','• ນາຍ + 맡은 곳: ນາຍຈ້າງ(고용주), ນາຍບ້ານ(촌장), ນາຍຄູ(선생님, 높임).'],
 pr=('ເຈົ້າບ່າວ','ເຈົ້າສາວ'),sm=['ນາຍຈ້າງເປັນເຈົ້າຂອງຮ້ານນີ້','나이짱 뻰 짜오컹 한 니','사장님이 이 가게의 주인이에요.']),
dict(sub='P2-F',t='ຫໍ 큰 건물',i='ຫໍ(허)는 여럿이 쓰는 큰 건물입니다. 뒤에 쓰임을 붙입니다.',
 w=[('ຫໍ','5-06-20','건물, ~관 · 여럿이 쓰는 큰 집'),('ຫໍສະໝຸດ',None,None),('ຫໍພັກ',None,None)],
 tp=['• ຫໍ + 쓰임: ຫໍສະໝຸດ(책의 집 → 도서관), ຫໍພັກ(쉬는 집 → 기숙사), ຫໍພິພິທະພັນ(박물관).','• ຫໍ(허, 건물)와 ຫໍ່(허, 싸다)는 성조 부호 ◌່ 하나 차이입니다.'],
 pr=('ຫໍສະໝຸດ','ຫໍພັກ'),sm=['ຂ້ອຍພັກຢູ່ຫໍພັກ ໃກ້ຫໍສະໝຸດ','커이 팍 유 허팍 까이 허싸묻','나는 도서관 가까운 기숙사에 살아요.']),
dict(sub='P2-F',t='ນອກ 밖',i='ນອກ(넉)은 ‘밖’입니다. 앞에 붙은 말의 바깥을 나타냅니다.',
 w=[('ນອກ','5-01-15','밖 · 안은 ໃນ'),('ຂ້າງນອກ',None,None),('ເມືອງນອກ','4-06-04',None),('ນອກຈາກ',None,None)],
 tp=['• 밖 ນອກ ↔ 안 ໃນ: ຂ້າງນອກ(바깥쪽) ↔ ຂ້າງໃນ(안쪽).','• ເມືອງນອກ(바깥 나라 → 외국), ນອກຈາກ(~의 밖에서 → ~외에, ~말고).'],
 pr=('ຂ້າງນອກ','ເມືອງນອກ'),sm=['ຂ້າງນອກຮ້ອນ ເຂົ້າມາຂ້າງໃນເດີ','캉넉 헌 카오 마 캉나이 더','밖은 더우니 안으로 들어오세요.']),
dict(sub='P2-L',t='ຂີ້ 찌꺼기·버릇',i='ຂີ້(키)는 본래 ‘똥, 찌꺼기’입니다. 더러운 것의 이름과 나쁜 버릇을 나타내는 말을 만듭니다.',
 w=[('ຂີ້','5-02-10','똥, 찌꺼기 · 나쁜 버릇에도 붙어요'),('ຂີ້ຝຸ່ນ',None,None),('ຂີ້ຕົມ',None,None),('ຂີ້ເຫຍື້ອ','1-08-04','쓰레기 · ຂີ້(찌꺼기) + ເຫຍື້ອ(쓰레기)'),('ຂີ້ຄ້ານ','3-15-03','게으르다 · ຂີ້(~하는 버릇) + ຄ້ານ(게으르다)'),('ຂີ້ອາຍ','3-07-07','수줍음을 타다 · ຂີ້(~하는 버릇) + ອາຍ(부끄럽다)')],
 tp=['• 찌꺼기·더러운 것: ຂີ້ຝຸ່ນ(먼지), ຂີ້ຕົມ(진흙), ຂີ້ເຫຍື້ອ(쓰레기).','• ຂີ້ + 동사·형용사 = ‘~하는 버릇이 있다’: ຂີ້ຄ້ານ(게으르다), ຂີ້ອາຍ(수줍음을 타다), ຂີ້ລືມ(잘 잊다).'],
 pr=('ຂີ້ຝຸ່ນ','ຂີ້ຕົມ'),sm=['ຢ່າຂີ້ຄ້ານ ກວາດຂີ້ຝຸ່ນ ແລະ ຖິ້ມຂີ້ເຫຍື້ອ','야 키칸 꽈앋 키푼 래 팀 키느아','게으름 피우지 말고 먼지를 쓸고 쓰레기를 버려요.']),
dict(sub='P2-J',t='ລາຍ 줄·목록',i='ລາຍ(라이)는 ‘줄, 무늬’입니다. 줄지어 적은 것, 곧 ‘목록’을 만듭니다.',
 w=[('ລາຍ','5-06-06','무늬, 줄 · 줄지어 적으면 목록'),('ລາຍການ',None,None),('ລາຍຊື່',None,None)],
 tp=['• ລາຍ + 적는 것: ລາຍຊື່(이름 목록 → 명단), ລາຍການ(항목 목록 → 메뉴·프로그램).','• 식당 메뉴판은 ລາຍການອາຫານ, 방송 프로그램도 ລາຍການ이라고 합니다.'],
 pr=('ລາຍການ','ລາຍຊື່'),sm=['ຄູອ່ານລາຍຊື່ ແລ້ວແຈກລາຍການອາຫານ','쿠 안 라이쓰 래우 짹 라이깐 아한','선생님이 명단을 읽고 나서 식단표를 나눠 줘요.']),
dict(sub='P2-C',t='ຕົວ 몸·자신·글자',i='ຕົວ(뚜아)는 ‘몸, 자신’이고, 글자 한 자를 가리키기도 합니다.',
 w=[('ຕົວ','5-05-15','몸, 자신 · 글자 한 자도 ຕົວ'),('ຕົວໜັງສື',None,'글자, 문자 · ຕົວ(낱자) + ໜັງສື(글)'),('ຕົວອັກສອນ','1-07-03','글자, 문자 · ຕົວ(낱자) + ອັກສອນ(글자)'),('ຕົວຢ່າງ',None,'예, 보기 · ຕົວ(본보기) + ຢ່າງ(종류)'),('ຕົວເມືອງ','4-06-04',None),('ແຕ່ງຕົວ','3-02-03',None),('ບັດປະຈຳຕົວ',None,None)],
 tp=['• 글자: ຕົວໜັງສື와 ຕົວອັກສອນ은 둘 다 ‘글자’입니다. ຕົວໜັງສື가 더 일상적인 말입니다.','• ‘본체, 중심’ 뜻: ຕົວເມືອງ(도시의 몸 → 시내), ຕົວຢ່າງ(본보기 → 예).','• ຕົວ(뚜아, 몸)와 ຕົວະ(뚜아, 거짓말하다)는 끝의 ◌ະ로 구별합니다.'],
 pr=('ຕົວໜັງສື','ຕົວຢ່າງ'),sm=['ແຕ່ງຕົວແລ້ວ ຢ່າລືມບັດປະຈຳຕົວ','땡뚜아 래우 야 름 받빠짬뚜아','옷을 차려입고 신분증을 잊지 마세요.']),
dict(sub='P2-N',t="ບໍລິ- 접두 '버리'",i='ບໍລິ-(버리)는 팔리어에서 온 앞말로 ‘두루, 온전히’라는 뜻을 더합니다. 격식 있는 낱말에 나옵니다.',
 w=[('ບໍລິການ',None,'서비스, 봉사 · ບໍລິ(두루) + ການ(일)'),('ບໍລິສັດ',None,'회사 · ບໍລິ(두루) + ສັດ(모임)'),('ບໍລິຈາກ','3-02-06','기부하다 · ບໍລິ(두루) + ຈາກ(내놓다)')],
 tp=['• ບໍລິ는 ‘버리’로 읽습니다. ㄹ받침을 넣지 않아요: 버리깐, 버리삳, 버리짝.','• ບໍລິການ(서비스)는 식당·호텔에서, ບໍລິສັດ(회사)는 자기소개에서, ບໍລິຈາກ(기부)는 절이나 학교 행사에서 자주 듣습니다.'],
 pr=('ບໍລິການ','ບໍລິສັດ'),sm=['ບໍລິສັດນີ້ບໍລິການດີ ແລະ ບໍລິຈາກເງິນໃຫ້ໂຮງຮຽນ','버리삳 니 버리깐 디 래 버리짝 응은 하이 홍히안','이 회사는 서비스가 좋고 학교에 돈을 기부해요.']),
]
touched=collections.defaultdict(list)
for bid,ws in RM.items():
    ws=ws.split();b=B[bid]
    for lo in ws:assert any(w[0]==lo for w in b['w']),(bid,lo)
    b['w']=[w for w in b['w'] if w[0] not in ws];touched[bid]+=ws
for dst,lo,src,h in ADD:
    w=entry(lo,src)
    if h:w[1]=h
    assert not any(x[0]==lo for x in B[dst]['w']),(dst,lo)
    B[dst]['w'].append(w);touched[dst]
for (bid,lo),h in HINT.items():
    [w for w in B[bid]['w'] if w[0]==lo][0][1]=h
for bid,t in TITLE.items():B[bid]['t']=t
for bid,t in INTRO.items():B[bid]['i']=t
for bid,(k,t) in TPSET.items():B[bid]['tp'][k]=t
for bid,t in TPADD.items():B[bid]['tp'].append(t)
for bid,(a,b_) in PRSET.items():
    g=lambda lo:trip([w for w in B[bid]['w'] if w[0]==lo][0])
    B[bid]['pr']=[[g(a),g(b_)]]
for bid,rm in touched.items():
    b=B[bid];b['h']=' · '.join(w[0] for w in b['w'])
    if rm:fixqz(b,rm)
P2=[p for p in D['P'] if p['id']=='P2'][0];P1=[p for p in D['P'] if p['id']=='P1'][0]
LABN={}
for k,n in enumerate(NEW):
    W=[]
    for lo,src,h in n['w']:
        w=entry(lo,src)
        if h:w[1]=h
        W.append(w)
    g=lambda lo:trip([w for w in W if w[0]==lo][0])
    tid='N%02d'%k
    B[tid]=dict(t=n['t'],h=' · '.join(w[0] for w in W),i=n['i'],w=W,tp=n['tp'],nx=[],pr=[[g(n['pr'][0]),g(n['pr'][1])]],dl=[],sm=n['sm'],qz=autoqz(W))
    [sb for sb in P2['subs'] if sb['id']==n['sub']][0]['b'].append(tid)
M={};newB={};dead=[]
for si,sb in enumerate(P2['subs'],1):
    ids=[]
    for bid in sb['b']:
        if bid in DEL:dead.append(bid);continue
        nid='4-%02d-%02d'%(si,len(ids)+1);ids.append(nid)
        if bid!=nid and not bid.startswith('N'):M[bid]=nid
        newB[nid]=B[bid];newB[nid]['_old']=bid
    sb['b']=ids
for bid in O:
    if bid[0]=='5':
        if bid in ib:M[bid]=ib[bid]
        else:dead.append(bid)
for k in list(M):
    if M[k]==k:del M[k]
P1['subs']=psubs
P1['desc']='한글로 쓰면 같거나 비슷해서 헷갈리는 소리. 성조, 짧은·긴 모음, 된소리·거센소리, 비슷한 모음과 비슷한 소리 모음'
# ---------- BLAB ----------
a=rest.index('const BLAB={');e=rest.index('};',a)
BL=json.loads(rest[a+11:e+1])
LAB={}
for nid,b in list(newB.items())+list(NB.items()):
    if nid[0]=='4':
        old=b.pop('_old')
        if old in BL and old not in TITLE:LAB[nid]=BL[old]
        else:
            lo,ko=b['t'].split(' ',1);LAB[nid]=[ko.replace("'",''),lo]
    else:
        lab=b.pop('_lab',None);b.pop('_removed',None)
        LAB[nid]=lab if lab else BL['5-08-01']
# ---------- assemble + remap references ----------
final={}
for p in D['P']:
    for sb in p['subs']:
        for bid in sb['b']:
            final[bid]=NB[bid] if bid[0]=='5' else (newB[bid] if bid[0]=='4' else B[bid])
pat=re.compile(r'(?<![\d-])(\d-\d{2}-\d{2})(?![\d-])')
loc=collections.defaultdict(list)
for bid,b in final.items():
    for w in b['w']:loc[w[0]].append(bid)
log=[]
def fixhint(bid,w):
    def rp(mm):
        x=mm.group(1)
        if x[0] not in '45':return mm.group(0)
        t=M.get(x,x)
        if x in dead or w[0] not in [y[0] for y in final.get(t,{'w':[]})['w']]:
            c=[y for y in loc[w[0]] if y!=bid and '같이 쓰는 말' not in final[y]['t']]
            c.sort(key=lambda y:(y[0]!=x[0],y))
            if not c:log.append(('orig dropped',bid,w[0],x));return ''
            t=c[0]
        if t!=x:log.append(('orig',bid,w[0],x,t))
        return ' · 원래 '+t
    w[1]=re.sub(r' · 원래 (\d-\d{2}-\d{2})',rp,w[1])
def fix(o):
    if isinstance(o,str):
        def r(mm):
            x=mm.group(1)
            if x in dead:log.append(('DEAD REF',x,o[:80]))
            return M.get(x,x)
        return pat.sub(r,o)
    if isinstance(o,list):return [fix(x) for x in o]
    return o
for bid,b in final.items():
    for w in b['w']:fixhint(bid,w)
    if bid[0]=='5':
        for k in('i','tp'):
            for mm in pat.finditer(json.dumps(b[k],ensure_ascii=False)):log.append(('P1 text ref',bid,mm.group(1)))
        continue
    b['i']=fix(b['i']);b['tp']=fix(b['tp'])
    nx=[]
    for x in b['nx']:
        ids=pat.findall(x)
        if any(i in dead for i in ids):log.append(('nx dropped',bid,x));continue
        nx.append(fix(x))
    b['nx']=nx
D['B']=final
allids=list(final);assert len(set(allids))==len(allids)
rest=rest[:a]+'const BLAB={'+','.join(json.dumps(k)+':'+json.dumps(LAB.get(k) or BL[k],ensure_ascii=False,separators=(',',':')) for k in allids)+rest[e:]
x='const IDV=store.get("lao-idv",0);';assert rest.count(x)==1
rest=rest.replace(x,'const IDMAP7='+json.dumps(M)+',IDDEAD7='+json.dumps(sorted(dead))+';for(const k in IDMAP){if(IDMAP7[IDMAP[k]])IDMAP[k]=IDMAP7[IDMAP[k]];else if(IDDEAD7.includes(IDMAP[k]))delete IDMAP[k]}\n'+x)
x='store.set("lao-idv",16)}';assert rest.count(x)==1
rest=rest.replace(x,x+'if(IDV<17){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);if(m&&IDMAP7[m[1]])k2[IDMAP7[m[1]]+k.slice(m[1].length)]=known[k];else if(!(m&&IDDEAD7.includes(m[1])))k2[k]=known[k]}known=k2;store.set("lao-known",known);if(saved.bun)for(const k in saved.bun){const v=saved.bun[k];if(IDMAP7[v])saved.bun[k]=IDMAP7[v];else if(IDDEAD7.includes(v))delete saved.bun[k]}store.set("lao-sel",saved);store.set("lao-idv",17)}')
# ---------- report ----------
for l in log:print(*l)
olds={w[0] for b in O.values() for w in b['w']};news={w[0] for b in final.values() for w in b['w']}
print('LOST words:',sorted(olds-news))
print('NEW words:',sorted(news-olds))
nw=sum(len(b['w']) for b in final.values())
ns=sum(sum(len(w[4]) for w in b['w'])+len(b['pr'])*2+len(b['dl'])+(1 if b['sm'] and b['sm'][0] else 0) for b in final.values())
print('bundles',len(final),'cards',nw,'unique',len(news),'sentences',ns)
for p in D['P']:print(p['id'],p['ko'],len(p['subs']),sum(len(sb['b']) for sb in p['subs']),sum(len(final[b]['w']) for sb in p['subs'] for b in sb['b']))
for bid,b in final.items():
    assert all(k in b for k in('t','h','i','w','tp','nx','pr','dl','sm','qz')),bid
    assert len(b['qz'])>=5 or bid[0] not in '45',(bid,len(b['qz']));assert len(b['w'])>=2,bid
json.dump({'M':M,'dead':sorted(dead),'touched':sorted(set(M.get(k,k) for k in touched)|{k for k,b in final.items() if k[0]=='5'}|{k for k in final if k[0]=='4' and final[k]['dl']==[]})},open(os.path.join(HERE,'v2_map.json'),'w'),ensure_ascii=False)
if not DRY:
    lit=json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)
    open(APP,'w',encoding='utf-8').write('const DATA=JSON.parse('+lit+')'+m.group(2)+'\n'+rest)
    print('written')
