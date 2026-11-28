# v3.01 RYU (점검표 2번): 듣기연습 확인 문제 = 내용 이해 4 + 단어 1, 듣기 팁 채우기 (lis_qz_v301.json)
import json,re,sys,os
APP=sys.argv[1];L=open(APP,encoding='utf8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0]);D=json.loads(json.loads(m.group(1)));B=D['B']
J=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'lis_qz_v301.json'),encoding='utf8'))
for id,o in J.items():
    b=B[id];assert b.get('lis')
    word=[q for q in b['qz'] if '뜻을 쓰세요' in q[0]][:1]
    b['qz']=[list(q) for q in o['q']]+word
    if o.get('tp') and len(b.get('tp') or [])<2:b['tp']=o['tp']
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
open(APP,'w',encoding='utf8').write('\n'.join(L));print('ok',len(J))
