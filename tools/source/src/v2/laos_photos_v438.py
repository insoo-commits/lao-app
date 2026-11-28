# v4.38: 라오스 탭에서 사진이 없던 쪽에 Wikimedia Commons 사진을 넣는다.
# 사진은 img/la/<key>.jpg (640px, 3:2), 출처는 laos_credits.json에도 추가.
# usage: python3 laos_photos_v438.py /path/to/lao-app
import sys,json,os,re
R=sys.argv[1];H=os.path.dirname(os.path.abspath(__file__))
CRF=os.path.join(H,'laos_credits.json');CR=json.load(open(CRF))
# bundle id, photo key, caption (the same caption the page script laos_0x.py gives for that key)
NEW=[
 ('9-02-03','central','캄무안의 석회암 산'),
 ('9-03-04','kaysone','까이썬 폼위한 기념관'),
 ('9-05-02','rocket','화려하게 꾸민 로켓 <span class="lo">ບັ້ງໄຟ</span> <span class="r">방파이</span>'),
 ('9-05-04','boatrace','메콩강의 보트 경주'),
 ('9-07-01','nop','두 손을 모으는 인사 놉 <span class="lo">ນົບ</span>'),
 ('9-07-02','family','라오스의 가족'),
 ('9-08-01','lamvong','둥글게 돌며 추는 람웡 <span class="lo">ລຳວົງ</span>'),
]
ADD=json.load(open(os.path.join(H,'laos_photos_v438.json')))
s=open(R+'/app.js').read()
i=s.find('const LAOINFO=');j=s.find('\n',i);L=s[i:j]
for bid,key,cap in NEW:
  if key not in ADD:print('skip',bid,key);continue
  c=ADD[key];CR[key]=c
  a=L.find('"%s":{"t"'%bid);assert a>0,bid
  e=L.find('"},"9-',a);e=len(L) if e<0 else e
  old='<div class=\\"top1\\"><div>'
  b=L.find(old,a);assert a<b<e,bid
  fig=f'<figure class="ph"><img src="img/la/{key}.jpg" width="{c["w"]}" height="{c["h"]}" loading="lazy" alt=""><figcaption>{cap}<small>사진: {c["a"]} · {c["lic"]} · Wikimedia Commons</small></figcaption></figure>'
  new='<div class=\\"top2\\"><div>'+json.dumps(fig,ensure_ascii=False)[1:-1]+'</div><div>'
  L=L[:b]+new+L[b+len(old):]
  print('ok',bid,key)
s=s[:i]+L+s[j:]
open(R+'/app.js','w').write(s)
json.dump(CR,open(CRF,'w'),ensure_ascii=False,indent=1)
