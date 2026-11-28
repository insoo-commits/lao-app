# v2.94 RYU: 듣기연습 readings (from the script xlsx) aligned to the app's own word readings.
# Usage: python3 fix_rd_v294.py app.js rdfix93.json   (rdfix93.json from scratch rdfix93.js: "id|dl|i" / "id|w|i" / "id|exI|q" -> reading)
import json,re,sys
L=open(sys.argv[1],encoding='utf8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0]);D=json.loads(json.loads(m.group(1)));B=D['B']
P=json.load(open(sys.argv[2],encoding='utf8'))
SKIPLO=('ຄົນລາວເຊື່ອວ່າ ນາຄອາໄສ','ເກົາຫຼີ ແລະ ລາວ ໄດ້ຟື້ນຟູ')  # bad auto-alignments (ນາຄ, year 1995)
MAN=[('뜱','띱'),('퓯','푿'),('싸이쏘타티랏','싸이쎋타티랃'),('뽁컭','뽁컹'),('썸붵','썸뺑'),('버 붓','버 붇'),('카닛싸앋','카닏싿'),('오깟','오깓'),('유 왓','유 왇'),('수파씯','쑤파씯'),('쑤팝','쑤팝'),('쏜나봍','쏜나볻'),('나컬루앙','나컨루앙'),('왓투','왇투'),('땱훅','땜훕'),('쨜아','찌야'),('매남컵','매남컹'),(' 컯 ',' 컹 '),('콰이','쿠아이'),('콰킫','쿠암킫'),('빠숴','빠쑴')]
NEW=json.load(open('/tmp/claude-0/up2/new.json'))
n=0
def fx(key,cur,lo):
    global n
    r=cur if lo.startswith(SKIPLO) else P.get(key,cur)
    for a,b in MAN: r=r.replace(a,b)
    if r!=cur: n+=1
    return r
for id in NEW:
    b=B[id]
    for i,d in enumerate(b['dl']): d[2]=fx(f'{id}|dl|{i}',d[2],d[1])
    for i,w in enumerate(b['w']):
        w[2]=fx(f'{id}|w|{i}',w[2],w[0])
        for q,e in enumerate(w[4] or []): e[1]=fx(f'{id}|ex{i}|{q}',e[1],e[0])
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
open(sys.argv[1],'w',encoding='utf8').write('\n'.join(L));print('changed',n)
