# Builds the new P1 (말소리) bundles from p1_spec.txt.  Used by build_v2.py.
import re,json,copy,collections,os
HERE=os.path.dirname(os.path.abspath(__file__))
SND={'ກ':'k','ຂ':'kh','ຄ':'kh','ງ':'ng','ຈ':'c','ສ':'s','ຊ':'s','ຍ':'ny','ດ':'d','ຕ':'t','ຖ':'th','ທ':'th','ນ':'n','ໜ':'n','ບ':'b','ປ':'p','ຜ':'ph','ພ':'ph','ຝ':'f','ຟ':'f','ມ':'m','ໝ':'m','ຢ':'y','ລ':'l','ຫຼ':'l','ຣ':'l','ວ':'w','ຫວ':'w','ຫ':'h','ຮ':'h','ອ':'q','ຫຍ':'ny','ຫງ':'ng','ຫນ':'n','ຫມ':'m','ຫລ':'l'}
CLS={}
for c in 'ຂສຖຜຝຫໜໝ':CLS[c]='H'
for c in ['ຫນ','ຫມ','ຫຼ','ຫລ','ຫວ','ຫຍ','ຫງ']:CLS[c]='H'
for c in 'ກຈດຕບປຢອ':CLS[c]='M'
for c in 'ຄງຊຍທນພຟມລວຮຣ':CLS[c]='L'
INIT='(ຫ[ງຍນມລວ]|ຫຼ|[ກຂຄງຈສຊຍດຕຖທນບປຜຝພຟມຢຣລວຫອຮໜໝ])(ວ(?=[າັ])|ວ(?=[່້]?າ))?'
T='([່້໊໋]?)';F='([ກງຍດນບມວ])'
PAT=[('ເ'+INIT+'ິ'+T+F,'ə','S'),('ເ'+INIT+'ີ'+T+F+'?','ə','L'),('ເ'+INIT+'[ຶື]'+T+'ອ'+F+'?','ɯa','L'),('ເ'+INIT+T+'ົ'+T+'າ','ao','S'),('ເ'+INIT+T+'າະ','ɔ','S'),('ເ'+INIT+'ັ'+T+F,'e','S'),('ເ'+INIT+T+'ະ','e','S'),('ເ'+INIT+T+'ຍ','ia','L'),('ເ'+INIT+T+F+'?','e','L'),('ແ'+INIT+T+'ະ','ɛ','S'),('ແ'+INIT+'ັ'+T+F,'ɛ','S'),('ແ'+INIT+T+F+'?','ɛ','L'),('ໂ'+INIT+T+'ະ','o','S'),('ໂ'+INIT+T+F+'?','o','L'),('[ໄໃ]'+INIT+T,'ai','S'),(INIT+'ັ'+T+'ອ'+F,'ɔ','S'),(INIT+'ັ'+T+F,'a','S'),(INIT+'ົ'+T+'ວ','ua','L'),(INIT+'ົ'+T+F,'o','S'),(INIT+T+'ະ','a','S'),(INIT+T+'າ'+F+'?','a','L'),(INIT+T+'ຳ','am','S'),(INIT+T+'ໍ'+T,'ɔ','L'),(INIT+'ິ'+T+F+'?','i','S'),(INIT+'ີ'+T+F+'?','i','L'),(INIT+'ຶ'+T+F+'?','ɯ','S'),(INIT+'ື'+T+F+'?','ɯ','L'),(INIT+'ຸ'+T+F+'?','u','S'),(INIT+'ູ'+T+F+'?','u','L'),(INIT+T+'ອ'+F,'ɔ','L'),(INIT+T+'ຽ'+F,'ia','L'),(INIT+T+'ວ'+F,'ua','L')]
PAT=[(re.compile('^'+p+'$'),v,l) for p,v,l in PAT]
TM='່້໊໋'
def parse(w):
    for rx,v,l in PAT:
        m=rx.match(w)
        if m:
            g=list(m.groups());ini=g[0];wv=g[1] or ''
            rest=[x for x in g[2:] if x]
            tone=''.join(x for x in rest if x in TM);fin=''.join(x for x in rest if x not in TM)
            fr=''.join(c for c in w if c not in TM).replace(ini,'◌',1)
            dead=fin in ('ກ','ດ','ບ') and fin!='' or (l=='S' and not fin and v not in('am','ai','ao'))
            return dict(ini=ini,wv=wv,snd=SND[ini],cls=CLS[ini],tone=tone,v=v,len=l,fin=fin,frame=fr,dead=dead)
    return None
CLSN={'H':'높은 자음','M':'가운데 자음','L':'낮은 자음'}
def pitch(f):
    c,t=f['cls'],f['tone']
    if t=='່':return '중간 높이로 평평하게'
    if t=='້':return '낮게 떨어짐' if c=='H' else '높은 데서 떨어짐'
    if f['dead']:
        if f['len']=='L':return '높은 데서 떨어짐' if c=='L' else '낮게 떨어짐'
        return '중간 높이로 짧게' if c=='L' else '높게 짧게'
    return {'H':'낮게 시작해 올라감','M':'낮게','L':'높게'}[c]
def spell(f):
    return f"{CLSN[f['cls']]} {f['ini']}"+(f" + ◌{f['tone']}" if f['tone'] else ", 부호 없음")
ASP={'ກ':'ㄲ (숨 없이)','ຂ':'ㅋ (숨을 내며)','ຄ':'ㅋ (숨을 내며)','ຕ':'ㄸ (숨 없이)','ຖ':'ㅌ (숨을 내며)','ທ':'ㅌ (숨을 내며)','ປ':'ㅃ (숨 없이)','ຜ':'ㅍ (숨을 내며)','ພ':'ㅍ (숨을 내며)','ຈ':'ㅉ (숨 없이)','ສ':'ㅆ (바람 소리)','ຊ':'ㅆ (바람 소리)','ບ':'ㅂ (목을 울려 부드럽게)','ດ':'ㄷ (목을 울려 부드럽게)','ຝ':'f (윗니를 아랫입술에 대고)','ຟ':'f (윗니를 아랫입술에 대고)'}
VOW={'e':'ㅔ (입을 조금만 벌려)','ɛ':'ㅐ (입을 크게 벌려)','o':'ㅗ (입술을 둥글게 모아)','ɔ':'ㅓ (입을 크게 벌린 오)','u':'ㅜ (입술을 둥글게)','ɯ':'ㅡ (입술을 옆으로 당겨)','ə':'ㅓ와 ㅡ 사이 소리','ia':'이아','ɯa':'으아','ua':'우아','i':'ㅣ','a':'ㅏ','ai':'아이','ao':'아오','am':'암'}
INI={'ງ':'응 (콧소리 ng)','ຍ':'냐 (ㄴ에 y를 붙인 소리)','ຢ':'야 (y)','ນ':'ㄴ','ໜ':'ㄴ','ຫຍ':'냐 (ㄴ에 y를 붙인 소리)'}
FIN={'ກ':'ㄱ','ດ':'ㄷ','ບ':'ㅂ','ງ':'ㅇ','ນ':'ㄴ','ມ':'ㅁ'}
def feat(kind,f):
    if kind in('tone','mark','cls'):return spell(f)
    if kind=='len':return ('짧은 ' if f['len']=='S' else '긴 ')+f['frame']
    if kind in('asp','cs','bp','dt','tri','ff'):return f"{f['ini']} = {ASP[f['ini']]}"
    if kind=='vow':return f"{f['frame']} = {VOW[f['v']]}"
    if kind=='ini':return f"{f['ini']} = {INI[f['ini']]}"
    if kind=='wcl':return (f"{f['ini']}ວ = ㅘ가 낌" if f['wv'] else f"{f['ini']} = ㅘ 없이")
    if kind=='fin':return f"받침 {f['fin']} = {FIN[f['fin']]}"
INTRO={'tone':"한글로 쓰면 모두 ‘{rd}’예요. 첫 자음의 종류(높은·가운데·낮은 자음)와 성조 부호가 뜻을 가릅니다.",
 'mark':"글자는 같고 성조 부호만 다른 짝이에요. 부호 하나로 소리 높이와 뜻이 바뀝니다.",
 'cls':"한글로는 같은 소리인데 첫 자음이 높은 자음이냐 낮은 자음이냐에 따라 성조가 달라지는 짝이에요.",
 'len':"모음 길이만 다른 짝이에요. 앞 낱말은 짧게, 뒤 낱말은 길게 읽습니다.",
 'asp':"숨을 내느냐 안 내느냐로 갈리는 짝이에요. 앞 낱말은 된소리, 뒤 낱말은 거센소리.",
 'cs':"ຈ(ㅉ)와 ສ·ຊ(ㅆ)로 갈리는 짝이에요. 라오어에는 ㅊ 소리가 없어서 이 둘만 구별하면 됩니다.",
 'bp':"ບ(ㅂ)와 ປ(ㅃ)로 갈리는 짝이에요. 한국어 ㅂ보다 ບ는 더 부드럽게, ປ는 숨 없이 단단하게 읽습니다.",
 'dt':"ດ(ㄷ)와 ຕ(ㄸ)로 갈리는 짝이에요. ດ는 부드럽게, ຕ는 숨 없이 단단하게 읽습니다.",
 'tri':"ㅂ·ㅃ·ㅍ, ㄷ·ㄸ·ㅌ 세 갈래를 한 번에 비교해요.",
 'ff':"한글로는 둘 다 ㅍ으로 적지만 ຜ·ພ는 ㅍ, ຝ·ຟ는 영어 f 소리예요.",
 'vow':"모음이 비슷해서 헷갈리는 짝이에요. 입 모양을 다르게 해서 읽습니다.",
 'ini':"한국어에는 없는 첫소리라서 헷갈리는 짝이에요.",
 'wcl':"ກ·ຂ·ຄ 뒤에 ວ가 끼면 ‘꽈·콰’처럼 ㅘ 소리가 됩니다.",
 'fin':"받침만 다른 짝이에요. 라오어 받침은 터뜨리지 않고 끊어서 읽습니다."}
TIP={'tone':"소리 높이는 비엔티안 발음 기준이에요. 한글 독음은 같으니 음성을 듣고 높낮이를 따라 하세요.",
 'mark':"◌່ 가 붙으면 중간 높이로 평평하게, ◌້ 가 붙으면 떨어지는 소리가 됩니다.",
 'cls':"부호가 없으면 높은 자음(ຂ ສ ຖ ຜ ຝ ຫ)은 낮게 시작해 올라가고, 낮은 자음(ຄ ຊ ທ ພ ຟ ຮ)은 높게 읽습니다.",
 'len':"짧은 모음은 한 박자로 끊듯이, 긴 모음은 두 박자로 늘여서 읽어요. 한글 독음은 같아도 길이가 다릅니다.",
 'asp':"입 앞에 손바닥을 대고 읽어 보세요. ກ·ຕ·ປ는 바람이 거의 없고, ຂ ຄ·ຖ ທ·ຜ ພ는 바람이 느껴집니다.",
 'cs':"ຈ는 ‘ㅉ’에 가깝게 숨 없이, ສ·ຊ는 ‘ㅆ’처럼 바람 소리로 읽습니다.",
 'bp':"ບ는 목을 울리는 영어 b, ປ는 숨이 없는 ㅃ에 가깝습니다.",
 'dt':"ດ는 목을 울리는 영어 d, ຕ는 숨이 없는 ㄸ에 가깝습니다.",
 'tri':"ບ·ດ는 목을 울려 부드럽게, ປ·ຕ는 숨 없이 단단하게, ຜ ພ·ຖ ທ는 숨을 내며 읽습니다.",
 'ff':"f는 윗니를 아랫입술에 살짝 대고 바람을 냅니다. ㅍ은 두 입술을 붙였다 뗍니다.",
 'vow':"한글 독음이 같거나 비슷해도 입을 벌리는 크기와 입술 모양이 다릅니다. 음성을 듣고 따라 하세요.",
 'ini':"ງ은 ‘응’의 받침 ㅇ 소리를 첫소리로 내고, ຍ는 ‘냐’처럼 콧소리가 섞이며, ຢ는 콧소리 없는 ‘야’예요.",
 'wcl':"ວ가 낀 쪽은 입술을 둥글게 모았다가 펴면서 읽습니다.",
 'fin':"ㄱ·ㄷ·ㅂ, ㅇ·ㄴ·ㅁ은 한국어 받침과 같아요. 끝소리를 분명하게 끊어 주세요."}
def first_sense(w):
    h=w[1].split(' · ')[0].strip() if w[1] else ''
    if not h or re.search(r'[຀-໿◌+]',h): h=re.split(r'[;,]',w[3])[0].strip()
    return re.sub(r'^[①②③]\s*','',h)
def load_spec():
    subs=[];cur=None
    for ln in open(os.path.join(HERE,'p1_spec.txt'),encoding='utf-8'):
        ln=ln.rstrip('\n')
        if not ln or ln.startswith('#'):continue
        p=ln.split('|')
        if p[0]=='SUB':cur=dict(id=p[1],name=p[2],items=[]);subs.append(cur);continue
        p+=['']*(7-len(p))
        cur['items'].append(dict(kind=p[0],title=p[1],base=p[2],groups=p[3],sm=[p[4],p[5],p[6]] if p[4] else []))
    return subs
def build(D,report=None):
    B=D['B']
    order=sorted(B,key=lambda b:({'5':0,'1':1,'2':2,'3':3,'4':4}[b[0]],b))
    idx=collections.defaultdict(list)
    for bid in order:
        for w in B[bid]['w']: idx[w[0]].append((bid,w))
    def get(tok):
        lo,_,src=tok.partition('@')
        c=idx.get(lo)
        assert c,('missing word',tok)
        if src:
            c=[x for x in c if x[0]==src];assert c,('missing src',tok)
        return copy.deepcopy(c[0][1]),c[0][0]
    subs=load_spec();NB={};psubs=[];idmap_base={}
    for si,s in enumerate(subs,1):
        ids=[]
        for bi,it in enumerate(s['items'],1):
            nid=f"5-{si:02d}-{bi:02d}";ids.append(nid);kind=it['kind']
            if kind=='keep':
                NB[nid]=copy.deepcopy(B[it['groups']]);NB[nid]['nx']=[];idmap_base[it['groups']]=nid;continue
            if kind=='sim':
                ob=copy.deepcopy(B[it['base']]);idmap_base[it['base']]=nid
                if it['groups']:W=[get(t)[0] for t in it['groups'].split()]
                else:W=[w for w in ob['w'] if parse(w[0])]
                kept={w[0] for w in W};removed=[w[0] for w in ob['w'] if w[0] not in kept]
                krd=[];[krd.append(w[2]) for w in W if w[2] not in krd]
                trd=[x for x in ob['t'].replace("'",'').split('·') if x in krd]
                for r in krd:
                    if len(trd)>=min(3,len(krd)):break
                    if r not in trd:trd.append(r)
                trd.sort(key=krd.index)
                title="'"+'·'.join(trd)+"'"
                qz=[q for q in ob['qz'] if not any(r in q[0] or r in q[1] for r in removed)]
                have=' '.join(q[0]+q[1] for q in qz)
                def exof(w):
                    c=[e for e in w[4] if e[0].count(w[0])==1]
                    return min(c,key=lambda e:len(e[0])) if c else None
                cand=[]
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
                ob.update(t=title,h=' · '.join(w[0] for w in W),w=W,nx=[],qz=qz)
                lw=[next(w[0] for w in W if w[2]==r) for r in trd]
                ob['_lab']=[title.replace("'",''),'·'.join(lw)]
                ob['_removed']=removed
                NB[nid]=ob
                if report is not None:report.append((nid,title+(' [-'+' '.join(removed)+']' if removed else ''),[(w[0],w[3][:12],'') for w in W]))
                continue
            groups=[g.split() for g in it['groups'].split(' / ')]
            ws=[];gi=[];seen={}
            for g in groups:
                gg=[]
                for tok in g:
                    lo=tok.split('@')[0]
                    if lo in seen: gg.append(seen[lo]);continue
                    w,src=get(tok);f=parse(lo);assert f,('unparsed',lo)
                    w[1]=f"{first_sense(w)} · {feat(kind,f)}"
                    seen[lo]=len(ws);gg.append(len(ws));ws.append((w,f,src))
                gi.append(gg)
            base=B.get(it['base']) if it['base'] else None
            if it['base']:idmap_base[it['base']]=nid
            rd0=ws[0][0][2]
            if kind=='tone':
                rds=[];[rds.append(ws[g[0]][0][2]) for g in gi if ws[g[0]][0][2] not in rds]
                title=it['title'] or "'"+'·'.join(rds)+"'"
            elif it['title']:title=it['title']
            else:
                rds=[];[rds.append(ws[g[0]][0][2]) for g in gi if ws[g[0]][0][2] not in rds]
                title="'"+'·'.join(rds)+"'"
            lolab='·'.join(ws[g[0]][0][0] for g in gi) if len(gi)>1 else '·'.join(w[0][0] for w in ws[:4])
            m=lambda k:f"{ws[k][0][0]}({first_sense_cache[k]})"
            first_sense_cache=[w[0][1].split(' · ')[0] for w in ws]
            tp=["• "+' / '.join(' ↔ '.join(m(k) for k in g) for g in gi)]
            if kind in('tone','mark','cls'):
                tp.append("• 소리 높이: "+' / '.join(f"{w[0][0]} {pitch(w[1])}" for w in ws))
            if kind in('tone','mark','cls'):
                same=[]
                for g in gi:
                    for x,y in zip(g,g[1:]):
                        if pitch(ws[x][1])==pitch(ws[y][1]) and ws[x][1]['len']==ws[y][1]['len']:same.append(f"{ws[x][0][0]} = {ws[y][0][0]}")
                if same:tp.append("• 소리 높이까지 같은 짝: "+', '.join(same)+". 글자와 문맥으로 구별합니다.")
            tp.append("• "+TIP[kind])
            intro=INTRO[kind].format(rd=rd0)
            pr=[]
            for g in gi:
                for a,b in zip(g,g[1:]):
                    pr.append([[ws[a][0][0],ws[a][0][2],ws[a][0][3]],[ws[b][0][0],ws[b][0][2],ws[b][0][3]]])
            if kind=='tone' and len(gi)>1:
                pr.append([[ws[gi[0][0]][0][0],ws[gi[0][0]][0][2],ws[gi[0][0]][0][3]],[ws[gi[1][0]][0][0],ws[gi[1][0]][0][2],ws[gi[1][0]][0][3]]])
            dl=copy.deepcopy(base['dl']) if base else []
            sm=it['sm'] or (copy.deepcopy(base['sm']) if base else [])
            # quiz
            W=[w[0] for w in ws];qz=[]
            def exof(w,need=True):
                c=[e for e in w[4] if e[0].count(w[0])==1] if need else list(w[4])
                return min(c,key=lambda e:len(e[0])) if c else None
            e=exof(W[0],False);qz.append([f"{e[0]} 의 뜻을 쓰세요.",e[2].rstrip('.')])
            w=W[1%len(W)];qz.append([f"‘{w[3]}’를 라오스어로 쓰세요.",f"{w[0]} ({w[2]})"])
            for w in W[2%len(W):]+W:
                e=exof(w)
                if e:qz.append([f"빈칸에 알맞은 말: {e[0].replace(w[0],' ____ ').strip()}  ({e[2].rstrip('.')})",w[0]]);break
            a,b=gi[-1][0],gi[-1][1]
            if (si+bi)%2:qz.append([f"‘{W[b][3]}’는 어느 쪽?  ① {W[a][0]}  ② {W[b][0]}","②"])
            else:qz.append([f"‘{W[b][3]}’는 어느 쪽?  ① {W[b][0]}  ② {W[a][0]}","①"])
            w=W[-1] if len(W)>3 else W[0];qz.append([f"{w[0]} 의 한국어 독음과 뜻은?",f"{w[2]}, {w[3]}"])
            NB[nid]=dict(t=title,h=' · '.join(w[0] for w in W),i=intro,w=W,tp=tp,nx=[],pr=pr,dl=dl,sm=sm,qz=qz)
            NB[nid]['_lab']=[title.replace("'",''),lolab]
            if report is not None:report.append((nid,title,[(w[0][0],w[0][3][:12],w[2]) for w in ws]))
        psubs.append(dict(id=s['id'],name=s['name'],b=ids))
    return NB,psubs,idmap_base
if __name__=='__main__':
    first=open('/home/user/lao-app/app.js',encoding='utf-8').readline()
    m=re.match(r'const DATA=JSON\.parse\((".*")\)(;?)\s*$',first)
    D=json.loads(json.loads(m.group(1)))
    rep=[];NB,psubs,ib=build(D,rep)
    for nid,t,ws in rep:print(nid,t,' ; '.join(f"{a} {b}<{c}>" for a,b,c in ws))
    print(len(NB),[ (s['name'],len(s['b'])) for s in psubs])
    # leftovers
    newlo={w[0] for b in NB.values() for w in b['w']}
    other=collections.defaultdict(list)
    for bid,b in D['B'].items():
        if bid[0]!='5':
            for w in b['w']:other[w[0]].append(bid)
    lost=[(bid,w[0],w[2],w[3][:14]) for bid,b in D['B'].items() if bid[0]=='5' for w in b['w'] if w[0] not in newlo and w[0] not in other]
    seen=set();lost=[x for x in lost if not (x[1] in seen or seen.add(x[1]))]
    print('LOST unique:',len(lost))
    for x in lost:print('  ',*x)
