# v14.19: new bundle 1-02-04 계산 in 숫자·시간; old 1-02-04..07 shift +1; migration lao-idv 16 (IDMAP6)
# usage: python3 build_v1419.py /path/to/app.js
import json,re,sys
APP=sys.argv[1]
s=open(APP,encoding='utf-8').read()
first,rest=s.split('\n',1)
m=re.match(r'const DATA=JSON\.parse\((".*")\)(;?)\s*$',first)
d=json.loads(json.loads(m.group(1)));B=d['B']
SUB=[sb for p in d['P'] for sb in p['subs'] if sb['id']=='P5-J'][0]
old=SUB['b'][:];assert old==['1-02-0%d'%i for i in range(1,8)],old
M={'1-02-0%d'%i:'1-02-0%d'%(i+1) for i in range(4,8)}
BL=dict((k,json.loads('['+v+']')) for k,v in re.findall(r'"(1-02-\d\d)":\[([^\]]*)\]',rest))
pat=re.compile(r'(?<![\d-])(\d-\d{2}-\d{2})(?![\d-])')
def fix(o):
    if isinstance(o,str): return pat.sub(lambda mm:M.get(mm.group(1),mm.group(1)),o)
    if isinstance(o,list): return [fix(x) for x in o]
    if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
    return o
newB={}
for k,v in B.items(): newB[M.get(k,k)]=fix(v)
kl=[w for w in B['4-09-04']['w'] if w[0]=='ຄິດໄລ່'][0]
W=[
 ["ບວກ","더하다 · 더하기(+)","부악","더하다",[["ໜຶ່ງບວກສອງ","능 부악 썽","1 더하기 2"],["ສອງບວກສາມເທົ່າກັບຫ້າ","썽 부악 쌈 타오깝 하","2 더하기 3은 5예요."],["ບວກຄ່າສົ່ງແລ້ວ ທັງໝົດເທົ່າໃດ?","부악 카 쏭 래우 탕몯 타오다이?","배송비를 더하면 모두 얼마예요?"]]],
 ["ລົບ","빼다 · 빼기(−), ລຶບ(릅, 지우다)과 구별","롭","빼다",[["ສິບລົບສີ່","씹 롭 씨","10 빼기 4"],["ສິບລົບສີ່ເທົ່າກັບຫົກ","씹 롭 씨 타오깝 혹","10 빼기 4는 6이에요."],["ລົບສ່ວນຫຼຸດແລ້ວ ຈ່າຍເທົ່າໃດ?","롭 쑤안룯 래우 짜이 타오다이?","할인을 빼면 얼마 내요?"]]],
 ["ຄູນ","곱하다 · 곱하기(×)","쿤","곱하다",[["ສອງຄູນສາມ","썽 쿤 쌈","2 곱하기 3"],["ສອງຄູນສາມເທົ່າກັບຫົກ","썽 쿤 쌈 타오깝 혹","2 곱하기 3은 6이에요."],["ຊື້ສອງອັນ ລາຄາກໍຄູນສອງ","쓰 썽 안 라카 꺼 쿤 썽","두 개 사면 값도 2를 곱해요."]]],
 ["ຫານ","나누다 · 나누기(÷)","한","나누다",[["ສິບຫານສອງ","씹 한 썽","10 나누기 2"],["ສິບຫານສອງເທົ່າກັບຫ້າ","씹 한 썽 타오깝 하","10 나누기 2는 5예요."],["ຄ່າອາຫານຫານສີ່ຄົນ ຄົນລະເທົ່າໃດ?","카 아한 한 씨 콘 콘 라 타오다이?","밥값을 네 명으로 나누면 한 사람에 얼마예요?"]]],
 ["ເທົ່າກັບ","~와 같다, 는(=) · ເທົ່າ(만큼) + ກັບ(~와)","타오깝","~와 같다, 는(=)",[["ເທົ່າກັບສິບ","타오깝 씹","10과 같아요."],["ຫ້າບວກຫ້າເທົ່າກັບສິບ","하 부악 하 타오깝 씹","5 더하기 5는 10이에요."],["ສາມຄູນສີ່ເທົ່າກັບເທົ່າໃດ?","쌈 쿤 씨 타오깝 타오다이?","3 곱하기 4는 얼마예요?"]]],
 ["ຄິດໄລ່","계산하다 · ຄິດ(생각하다) + ໄລ່(셈하다)","킫라이","계산하다",kl[4]],
 ["ເຄື່ອງຄິດເລກ","계산기 · ເຄື່ອງ(기계) + ຄິດ(생각하다) + ເລກ(숫자)","크앙 킫 렉","계산기",[["ມີເຄື່ອງຄິດເລກບໍ?","미 크앙 킫 렉 버?","계산기 있어요?"],["ໃຊ້ເຄື່ອງຄິດເລກ","싸이 크앙 킫 렉","계산기를 써요."],["ແມ່ຄ້າກົດເຄື່ອງຄິດເລກໃຫ້ເບິ່ງລາຄາ","매카 꼳 크앙 킫 렉 하이 븡 라카","상인이 계산기를 눌러서 값을 보여 줘요."]]],
]
NB={"t":"계산","h":" · ".join(w[0] for w in W),"i":"더하기, 빼기, 곱하기, 나누기와 ‘=’, 계산하다, 계산기.","w":W,
 "tp":["• 식 읽기: 2 + 3 = 5 → ສອງບວກສາມເທົ່າກັບຫ້າ. 기호 자리에 ບວກ(+)·ລົບ(−)·ຄູນ(×)·ຫານ(÷)을, ‘=’ 자리에 ເທົ່າກັບ을 넣어 순서대로 읽어요.",
       "• ລົບ(롭, 빼다)과 ລຶບ(릅, 지우다)은 모음이 달라요.",
       "• 시장·식당에서: ທັງໝົດເທົ່າໃດ?(모두 얼마예요?), ຄິດໄລ່ຜິດ(계산이 틀렸어요)."],
 "nx":["숫자 0~10 → 1-02-01","큰 수 → 1-02-03"],
 "pr":[[["ບວກ","부악","더하다"],["ລົບ","롭","빼다"]],[["ຄູນ","쿤","곱하다"],["ຫານ","한","나누다"]]],
 "dl":[["봉사자","ສາມຄູນສີ່ເທົ່າກັບເທົ່າໃດ?","쌈 쿤 씨 타오깝 타오다이?","3 곱하기 4는 얼마예요?"],["학생","ເທົ່າກັບສິບສອງ.","타오깝 씹썽.","12예요."],["봉사자","ຖືກຕ້ອງ! ສິບສອງຫານສາມເດ?","특떵! 씹썽 한 쌈 데?","맞아요! 12 나누기 3은요?"],["학생","ເທົ່າກັບສີ່.","타오깝 씨.","4예요."]],
 "sm":["ຖົງລະຫ້າພັນກີບ ຊື້ສາມຖົງ ຫ້າພັນຄູນສາມເທົ່າກັບສິບຫ້າພັນກີບ","통 라 하 판 낍 쓰 쌈 통 하 판 쿤 쌈 타오깝 씹하 판 낍","한 봉지에 5,000낍인데 세 봉지를 사요. 5,000 곱하기 3은 15,000낍이에요."],
 "qz":[["ສອງບວກສາມເທົ່າກັບຫ້າ 의 뜻을 쓰세요.","2 더하기 3은 5"],["‘곱하다’를 라오스어로 쓰세요.","ຄູນ (쿤)"],["빈칸에 알맞은 말: ສິບ ____ ສີ່ເທົ່າກັບຫົກ  (10 빼기 4는 6)","ລົບ"],["‘나누다’는 어느 쪽?  ① ຫານ  ② ບວກ","①"],["ເທົ່າກັບ 의 한국어 독음과 뜻은?","타오깝, ~와 같다(=)"]]}
newB['1-02-04']=NB
ids=['1-02-0%d'%i for i in range(1,9)];SUB['b']=ids
allids=[x for p in d['P'] for sb in p['subs'] for x in sb['b']]
d['B']={k:newB[k] for k in allids};assert len(d['B'])==len(newB)==len(B)+1
LAB={M.get(k,k):v for k,v in BL.items()};LAB['1-02-04']=["계산","ການຄິດໄລ່"]
a=rest.index('"1-02-01":[');e=rest.index(']',rest.index('"1-02-07":['))+1
rest=rest[:a]+",".join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(LAB[k],ensure_ascii=False,separators=(',',':')) for k in ids)+rest[e:]
x='const IDV=store.get("lao-idv",0);';assert rest.count(x)==1
rest=rest.replace(x,'const IDMAP6='+json.dumps(M)+';for(const k in IDMAP){if(IDMAP6[IDMAP[k]])IDMAP[k]=IDMAP6[IDMAP[k]]}\n'+x)
x='store.set("lao-idv",15)}';assert rest.count(x)==1
rest=rest.replace(x,x+'if(IDV<16){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);k2[m&&IDMAP6[m[1]]?IDMAP6[m[1]]+k.slice(m[1].length):k]=known[k]}known=k2;store.set("lao-known",known);if(saved.bun)for(const k in saved.bun)if(IDMAP6[saved.bun[k]])saved.bun[k]=IDMAP6[saved.bun[k]];store.set("lao-sel",saved);store.set("lao-idv",16)}')
lit=json.dumps(json.dumps(d,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)
open(APP,'w',encoding='utf-8').write('const DATA=JSON.parse('+lit+')'+m.group(2)+'\n'+rest)
for k in ids: print(k,LAB[k],len(d['B'][k]['w']))
