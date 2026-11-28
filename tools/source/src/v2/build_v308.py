# v3.08 RYU: 단어 카드 두 번째 줄에 형태소 풀이 (morph_v308.txt), '원래 x-xx-xx' 메모 삭제, 몇 곳 형식 통일
import json,re,sys,os
APP=sys.argv[1];HERE=os.path.dirname(os.path.abspath(__file__))
M={}
for l in open(os.path.join(HERE,'morph_v308.txt'),encoding='utf8'):
    if '=' in l and not l.startswith('#'):
        a,b=l.split('=',1);a=a.strip();b=b.strip()
        parts=re.findall(r'([຀-໿]+)\(',b);assert ''.join(parts)==a.replace('ໆ','ໆ'),(a,parts);M[a]=b
FIX={('ເວລາ','ເວ + ລາ'):None,('ນ້ຳໝາກໄມ້','ນ້ຳ(물) + 과일'):'ນ້ຳ(물) + ໝາກໄມ້(과일)',('ສີຟ້າອ່ອນ','ສີຟ້າ + ອ່ອນ(연하다)'):'ສີຟ້າ(하늘색) + ອ່ອນ(연하다)',('ສີຂຽວອ່ອນ','ສີຂຽວ + ອ່ອນ(연하다)'):'ສີຂຽວ(초록색) + ອ່ອນ(연하다)'}
L=open(APP,encoding='utf8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0]);D=json.loads(json.loads(m.group(1)))
na=nr=nf=0;used=set()
for b,x in D['B'].items():
    for w in x['w']:
        h=w[1];seg=[s for s in h.split(' · ')] if h else []
        k=len(seg);seg=[s for s in seg if not re.fullmatch(r'원래 \d+-\d\d-\d\d',s)];nr+=k-len(seg)
        seg=[FIX.get((w[0],s),s) for s in seg];nf+=sum(1 for s in seg if s is None);seg=[s for s in seg if s is not None]
        if w[0] in M and '+' not in h and b[0] in '134589':
            if not seg:seg=[w[3]]
            seg.insert(1,M[w[0]]);na+=1;used.add(w[0])
        w[1]=' · '.join(seg)
print('added',na,'removed 원래',nr,'fixed',nf,'unused',set(M)-used)
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
open(APP,'w',encoding='utf8').write('\n'.join(L))
# colour words: drop notes that only repeat the new analysis
CL={'ສີສົ້ມ':'귤 색','ສີຟ້າ':'하늘색도 포함','ສີນ້ຳເງິນ':'짙은 파랑','ສີເທົາ':'ເທົ່າ(만큼)과 구별','ສີນ້ຳຕານ':'설탕(캐러멜) 색','ສີເຂັ້ມ':None,'ສີອ່ອນ':None,'ສີບົວ':'연꽃 색','ສີຄຳ':None,'ສີເງິນ':'ເງິນ은 돈이라는 뜻도 있어요'}
L=open(APP,encoding='utf8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0]);D=json.loads(json.loads(m.group(1)))
for b in ('1-11-05','1-11-06'):
    for w in D['B'][b]['w']:
        if w[0] in CL:
            s=w[1].split(' · ')
            if len(s)>=3 and '=' in s[2]:s=s[:2]+([CL[w[0]]] if CL[w[0]] else [])+s[3:]
            w[1]=' · '.join(s)
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
open(APP,'w',encoding='utf8').write('\n'.join(L))
