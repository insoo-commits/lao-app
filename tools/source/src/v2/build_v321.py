# v3.21 RYU: 듣기연습 P9-I 라오 노래 (lis_songs_v321.py). usage: python3 build_v321.py app.js readings_v313.json
import json,re,sys,os,urllib.parse
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import lis_songs_v321 as C
APP=sys.argv[1];RD=json.load(open(sys.argv[2],encoding='utf-8'))
L=open(APP,encoding='utf-8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0]);D=json.loads(json.loads(m.group(1)));B=D['B']
def rd(lo):
    r=RD.get(lo);assert r and '[' not in r,('no reading',lo,r);return r
INTRO='라오스 노래를 소개하는 듣기예요. 저작권 때문에 가사 전체는 싣지 않았어요. 듣는 순서: ❶ 노래 소개 듣기 → ❷ 문장별로 다시 듣기 → ❸ 확인퀴즈 → ❹ YouTube에서 노래 듣고 따라 부르기.'
P9=[p for p in D['P'] if p['id']=='P9'][0]
assert not any(s['id']=='P9-I' for s in P9['subs'])
sub={'id':'P9-I','name':'라오 노래','b':[]};P9['subs'].append(sub)
for bid,title,lt,lines,words,qz,tp,q in C.SONGS:
    assert bid not in B,bid
    W=[[lo,ko+(' · '+note if note else ''),rd(lo),ko,[[lines[li][0],rd(lines[li][0]),lines[li][1]]]] for lo,ko,note,li in words]
    B[bid]={'t':title,'h':' · '.join(w[0] for w in W),'i':INTRO,'w':W,'tp':list(tp),'nx':[],'pr':[],
            'dl':[['',lo,rd(lo),ko] for lo,ko in lines],'sm':None,'qz':[list(x) for x in qz]+[[W[0][0]+' 의 뜻을 쓰세요.',W[0][3]]],
            'lis':1,'nar':1,'yt':'https://www.youtube.com/results?search_query='+urllib.parse.quote_plus(q)}
    sub['b'].append(bid)
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
i=next(k for k,l in enumerate(L) if l.startswith('const BLAB='))
L.insert(i+1,'/* v3.21 RYU: 라오 노래 */Object.assign(BLAB,'+json.dumps({s[0]:[s[1],''] for s in C.SONGS},ensure_ascii=False)+');')
s='\n'.join(L)
old='${bb&&bb.tp.length?`<div class="box">${bb.tp.map(t=>`<p>${laoWrap(t)}</p>`).join("")}</div>`:""}'
assert s.count(old)==1
s=s.replace(old,old+'${bb&&bb.yt?`<p class="ytrow"><a class="ytbtn" href="${bb.yt}" target="_blank" rel="noopener">▶ YouTube에서 노래 찾아 듣기</a></p>`:""}')
open(APP,'w',encoding='utf-8').write(s);print('ok',len(C.SONGS),[x['id'] for x in P9['subs']])
