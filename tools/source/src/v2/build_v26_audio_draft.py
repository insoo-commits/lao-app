# v2.6: tone descriptions follow the pitch the app's Edge Lao voices actually produce (measured 2026-11-17,
# RYU heard ມາ as low).  Measured (semitones, word inside a sentence): L/M live = mid falling to low,
# H live = high falling, ◌່ = mid, ◌້ = rising (H class: high), dead syllables = high (L class: mid).
# usage: python3 build_v26.py /home/user/lao-app/app.js
import json,re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import build_p1
APP=sys.argv[1]
src=open(APP,encoding='utf-8').read();first,rest=src.split('\n',1)
m=re.match(r'const DATA=JSON\.parse\((".*")\)(;?)\s*$',first);D=json.loads(json.loads(m.group(1)));B=D['B']
def tone(f):
    c,t=f['cls'],f['tone']
    if t=='່':return 'mid'
    if t=='້':return 'hi' if c=='H' else 'rise'
    if f['dead']:return 'mid' if c=='L' else 'hi'
    return 'hf' if c=='H' else 'lf'
KO={'hi':'높게','mid':'중간 높이','rise':'중간에서 올라감','hf':'높은 데서 떨어짐','lf':'중간에서 낮게 떨어짐'}
n=collections=0;ch=0
for bid,b in B.items():
    if not bid.startswith('5-'):continue
    tp=b['tp'];new=[]
    lines=[t for t in tp]
    words=None
    for t in lines:
        if t.startswith('• 소리 높이: '):
            ws=[x.rsplit(' ',0)[0] for x in t[len('• 소리 높이: '):].split(' / ')]
            los=[x.split(' ',1)[0] for x in ws];fs=[build_p1.parse(lo) for lo in los]
            assert all(fs),(bid,los)
            words=list(zip(los,fs))
            new.append('• 소리 높이: '+' / '.join(f"{lo} {KO[tone(f)]}" for lo,f in words))
        elif t.startswith('• 소리 높이까지 같은 짝: '):
            if bid.startswith('5-04-'):new.append(t)
            continue
        elif t.startswith('• 소리 높이는 비엔티안 발음 기준이에요.'):
            if words:
                same=[]
                for x in range(len(words)):
                    for y in range(x+1,len(words)):
                        if tone(words[x][1])==tone(words[y][1]) and words[x][1]['len']==words[y][1]['len']:same.append(f"{words[x][0]} = {words[y][0]}")
                if same:new.append("• 소리 높이까지 같은 짝: "+', '.join(same)+". 글자와 문맥으로 구별합니다.")
            new.append('• 소리 높이는 앱 음성(비엔티안 말씨)을 직접 재서 적었어요. 한글 독음은 같으니 음성을 듣고 높낮이를 따라 하세요.')
        elif t=='• ◌່ 가 붙으면 중간 높이로 평평하게, ◌້ 가 붙으면 떨어지는 소리가 됩니다.':
            new.append('• ◌່ 가 붙으면 중간 높이, ◌້ 가 붙으면 올라가는 소리가 됩니다. 부호가 없으면 떨어지는 소리예요.')
        elif t=='• 부호가 없으면 높은 자음(ຂ ສ ຖ ຜ ຝ ຫ)은 낮게 시작해 올라가고, 낮은 자음(ຄ ຊ ທ ພ ຟ ຮ)은 높게 읽습니다.':
            new.append('• 부호가 없으면 높은 자음(ຂ ສ ຖ ຜ ຝ ຫ)은 높은 데서 떨어지고, 낮은 자음(ຄ ຊ ທ ພ ຟ ຮ)은 중간에서 낮게 떨어집니다. 받침 ກ ດ ບ로 끊기면 높은 자음이 더 높아요.')
        elif t.startswith('• ‘능’ 둘: 하나 ໜຶ່ງ(ໜ)·찌다 ນຶ່ງ(ນ). 높낮이가 다릅니다.'):
            new.append('• ‘능’ 둘: 하나 ໜຶ່ງ(ໜ)·찌다 ນຶ່ງ(ນ). 둘 다 ◌່ 라서 높낮이도 거의 같아요. 글자와 문맥으로 구별합니다.')
        else:new.append(t)
    if new!=tp:b['tp']=new;ch+=1
print('bundles changed',ch)
# any leftover old-table wording?
for bid,b in B.items():
    for t in b['tp']+[b['i']]:
        if '낮게 시작해 올라' in t or '중간 높이로 평평' in t or '비엔티안 발음 기준' in t:print('LEFT',bid,t)
lit=json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)
# card tone marks: same table in app.js
old="if(t==='່')return 'mid';if(t==='້')return c==='H'?'lf':'hf';\n  if(dead){if(y.len==='L')return c==='L'?'hf':'lf';return c==='L'?'mid':'hi'}\n  return {H:'rise',M:'low',L:'hi'}[c]};"
assert rest.count(old)==1,'tone fn'
rest=rest.replace(old,"/* RYU v2.6: measured from the app's Edge voices, not the textbook table */\n  if(t==='່')return 'mid';if(t==='້')return c==='H'?'hi':'rise';\n  if(dead)return c==='L'?'mid':'hi';\n  return c==='H'?'hf':'lf'};")
old='const TLEG=[["hi","높게"],["mid","중간"],["low","낮게"],["rise","올라감"],["hf","높은 데서 떨어짐"],["lf","낮게 떨어짐"]];'
assert rest.count(old)==1,'tleg'
rest=rest.replace(old,'const TLEG=[["hi","높게"],["mid","중간"],["rise","올라감"],["hf","높은 데서 떨어짐"],["lf","낮게 떨어짐"]];')
old="rise:'M2 10L14 2'";assert rest.count(old)==1
rest=rest.replace(old,"rise:'M2 8.5L14 3'")
open(APP,'w',encoding='utf-8').write('const DATA=JSON.parse('+lit+')'+m.group(2)+'\n'+rest)
