# v2.6: tone marks and 말소리 pitch notes follow RYU's textbook 6-tone system (1성~6성), RYU chose 2026-11-17.
# Book table (기본 성조-1: live; 기본 성조-2: consonant + short vowel + stop ກ ດ ບ):
#   no mark: H 4, M 1, L 3 | ◌່: all 5 | ◌້: H 6, M 2, L 2 | dead: H 6, M 6, L 2 (dead long follows dead short)
# Book shapes: 1 mid level, 2 very high then falling, 3 high-mid level rising at the end, 4 below mid rising,
#              5 high-mid level, 6 high-mid level then dropping.
# (build_v26_audio_draft.py = the rejected alternative that followed the measured Edge voice.)
# v2.7 (RYU 2026-11-17): low class unmarked shown as 1성 like the book's notation; 3성 no longer used.
# usage: python3 build_v26.py /home/user/lao-app/app.js /home/user/lao-app/index.html
import json,re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import build_p1
APP,IDX=sys.argv[1],sys.argv[2]
src=open(APP,encoding='utf-8').read();first,rest=src.split('\n',1)
m=re.match(r'const DATA=JSON\.parse\((".*")\)(;?)\s*$',first);D=json.loads(json.loads(m.group(1)));B=D['B']
def tone(f):
    # v2.11 (RYU 2026-11-17): follow the numbers the book prints in its lessons (pp.32-35):
    #   ຂອບ 커-4업, ໂຊກ 쏘-옥 (no number), ພົບ 폽 (no number), ສະ 싸4, ເຊັ່ນ 쎈3, ກ່ອນ 꺼5-언, ໃໝ່ 마5이, ຂ້ອຍ 커6-이, ແລ້ວ 래2-우
    #   => syllables ending in ກ ດ ບ follow the same table as the rest; low class + ◌່ is written 3 (book notation)
    c,t=f['cls'],f['tone']
    if t=='່':return 3 if c=='L' else 5
    if t=='້':return 6 if c=='H' else 2
    return {'H':4,'M':1,'L':1}[c]
KO={1:'1성(중간에서 평평)',2:'2성(아주 높게 시작해 떨어짐)',3:'3성(조금 높게, 끝이 살짝 올라감)',4:'4성(낮게 시작해 올라감)',5:'5성(높게 평평)',6:'6성(조금 높게 가다 떨어짐)'}
TIP='• 성조 번호는 교재의 6성조(1~6성)를 따랐어요. 앱 음성은 컴퓨터 음성이라 몇몇 낱말은 높낮이가 다르게 들릴 수 있어요.'
ch=0
for bid,b in B.items():
    if not bid.startswith('5-'):continue
    tp=b['tp'];new=[];words=None
    for t in tp:
        if t.startswith('• 소리 높이: '):
            los=[x.split(' ',1)[0] for x in t[len('• 소리 높이: '):].split(' / ')]
            fs=[build_p1.parse(lo) for lo in los];assert all(fs),(bid,los);words=list(zip(los,fs))
            new.append('• 소리 높이: '+' / '.join(f"{lo} {KO[tone(f)]}" for lo,f in words))
        elif t.startswith('• 소리 높이까지 같은 짝: '):
            if bid.startswith('5-04-'):
                prs=[x.split(' = ') for x in t[len('• 소리 높이까지 같은 짝: '):].split('. ')[0].split(', ')]
                keep=[a+' = '+b for a,b in prs if tone(build_p1.parse(a))==tone(build_p1.parse(b))]
                if keep:new.append('• 소리 높이까지 같은 짝: '+', '.join(keep)+'. 글자와 문맥으로 구별합니다.')
            continue
        elif t.startswith('• 소리 높이는 비엔티안 발음 기준이에요.'):
            if words:
                same=[f"{words[x][0]} = {words[y][0]}" for x in range(len(words)) for y in range(x+1,len(words)) if tone(words[x][1])==tone(words[y][1])]
                if same:new.append("• 소리 높이까지 같은 짝: "+', '.join(same)+". 글자와 문맥으로 구별합니다.")
            new.append(TIP)
        elif t=='• ◌່ 가 붙으면 중간 높이로 평평하게, ◌້ 가 붙으면 떨어지는 소리가 됩니다.':
            new.append('• ◌່ 가 붙으면 5성(높게 평평, 낮은 자음은 3성으로 적음), ◌້ 가 붙으면 2성(높게 시작해 떨어짐)이 됩니다. 높은 자음에 ◌້ 는 6성이에요.')
        elif t=='• 부호가 없으면 높은 자음(ຂ ສ ຖ ຜ ຝ ຫ)은 낮게 시작해 올라가고, 낮은 자음(ຄ ຊ ທ ພ ຟ ຮ)은 높게 읽습니다.':
            new.append('• 부호가 없으면 높은 자음(ຂ ສ ຖ ຜ ຝ ຫ)은 4성(낮게 시작해 올라감), 낮은 자음(ຄ ຊ ທ ພ ຟ ຮ)은 가운데 자음처럼 1성(평성)입니다. 받침 ກ ດ ບ로 끝나도 같아요.')
        elif t.startswith('• ‘능’ 둘: 하나 ໜຶ່ງ(ໜ)·찌다 ນຶ່ງ(ນ). 높낮이가 다릅니다.'):
            new.append('• ‘능’ 둘: 하나 ໜຶ່ງ(ໜ)·찌다 ນຶ່ງ(ນ). ໜຶ່ງ은 5성, ນຶ່ງ은 3성으로 적어요(책 표기). 글자와 문맥으로 구별합니다.')
        else:new.append(t)
    if new!=tp:b['tp']=new;ch+=1
print('bundles changed',ch)
for bid,b in B.items():
    for t in b['tp']+[b['i']]:
        if '낮게 시작해 올라가고' in t or '중간 높이로 평평' in t or '비엔티안 발음 기준' in t:print('LEFT',bid,t)
lit=json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)
def rep(s,old,new):
    assert s.count(old)==1,old[:60];return s.replace(old,new)
rest=rep(rest,"if(t==='່')return 'mid';if(t==='້')return c==='H'?'lf':'hf';\n  if(dead){if(y.len==='L')return c==='L'?'hf':'lf';return c==='L'?'mid':'hi'}\n  return {H:'rise',M:'low',L:'hi'}[c]};",
 "/* RYU v2.11: numbers as printed in the book's lessons (1성~6성); ກ ດ ບ endings follow the same table, low class + ◌່ is written 3 */\n  if(t==='່')return c==='L'?'t3':'t5';if(t==='້')return c==='H'?'t6':'t2';\n  return {H:'t4',M:'t1',L:'t1'}[c]};")
rest=rep(rest,"const MK={hi:'M2 2H14',mid:'M2 6H14',low:'M2 10H14',rise:'M2 10L14 2',hf:'M2 6L7 2L14 10',lf:'M2 5L14 10'};",
 "const MK={t1:'M2 6.5H14',t2:'M2 3Q8 0.5 13.5 10',t3:'M2 4.5H9.5L14 1.5',t4:'M2 7Q6 10.5 14 2.5',t5:'M2 3H14',t6:'M2 4H10L13.5 10'};")
rest=rep(rest,'const TLEG=[["hi","높게"],["mid","중간"],["low","낮게"],["rise","올라감"],["hf","높은 데서 떨어짐"],["lf","낮게 떨어짐"]];',
 'const TLEG=[["t1","1성 평평"],["t2","2성 높게 떨어짐"],["t3","3성 끝이 올라감"],["t4","4성 낮게 올라감"],["t5","5성 높게 평평"],["t6","6성 가다 떨어짐"]];')
open(APP,'w',encoding='utf-8').write('const DATA=JSON.parse('+lit+')'+m.group(2)+'\n'+rest)
h=open(IDX,encoding='utf-8').read()
for old,new in (('hi','t3'),('mid','t1'),('low','t5'),('rise','t4'),('hf','t2'),('lf','t6')):
    n=h.count(f'[data-tn={old}]');assert n==3,(old,n);h=h.replace(f'[data-tn={old}]',f'[data-tn={new}]')
open(IDX,'w',encoding='utf-8').write(h)
