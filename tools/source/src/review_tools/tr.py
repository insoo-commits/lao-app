# Lao syllable -> expected Korean reading alternatives; joint DP alignment against the app's Korean reading
import re
C0='ກຂຄງຈສຊຍດຕຖທນບປຜຝພຟມຢຣລວຫອຮໜໝ'
TONE='່້໊໋'
FIN={'ກ':1,'ງ':21,'ດ':7,'ນ':4,'ບ':17,'ມ':16}
L={'ກ':1,'ຂ':15,'ຄ':15,'ຈ':13,'ສ':10,'ຊ':10,'ດ':3,'ຕ':4,'ຖ':16,'ທ':16,'ນ':2,'ບ':7,'ປ':8,'ຜ':17,'ຝ':17,'ພ':17,'ຟ':17,'ມ':6,'ຣ':5,'ລ':5,'ຫ':18,'ອ':11,'ຮ':18,'ໜ':2,'ໝ':6}
A,AE,YA,YAE,EO,E,YEO,YE,O,WA,WAE,OE,YO,U,WEO,WE,WI,YU,EU,UI,I=range(21)
YG={A:[YA],AE:[YAE],EO:[YEO],E:[YE,E],O:[YO],U:[YU],I:[I],EU:[EU,YU]}
WG={A:[WA],AE:[WAE],EO:[WEO],E:[WE],I:[WI],O:[O,WEO],U:[U],EU:[EU,U]}
def H(l,v,t=0):return chr(0xAC00+l*588+v*28+t)
def onset(init):
    """returns list of (prefix_str, Lidx, glide) ; init = string of initial consonant(s)"""
    i=init.replace('ຼ','')
    if len(i)==2 and i[0]=='ຫ' and i[1] in 'ງຍນມລວ': i=i[1]
    if init in('ຫຼ',):i='ລ'
    cl=None
    if len(i)==2 and i[1]=='ວ':cl='w';i=i[0]
    elif len(i)==2 and i[1]=='ຣ':cl='r';i=i[0]
    if i=='ງ':base=[('응',11,None)]
    elif i=='ຍ':base=[('',2,'y')]
    elif i=='ຢ':base=[('',11,'y'),('이',11,'yy')]
    elif i=='ວ':base=[('',11,'w')]
    else:base=[('',L[i],None)]
    out=[]
    for pre,l,g in base:
        if cl=='w':
            out.append((pre,l,'w'));out.append((pre+H(l,U),11,None));out.append((pre+H(l,A),11,'w'))
        elif cl=='r':
            out.append((pre+H(l,EU),5,None));out.append((pre,l,None))
        else:out.append((pre,l,g))
    return out
def build(init,pieces,fin,offs=()):
    """pieces: list of vowel idx (first combines with onset); fin: T idx; offs: list of alternative offglide lists appended as ㅇ-syllables"""
    res=[]
    for pre,l,g in onset(init):
        v0=pieces[0]
        if g=='yy':
            if v0!=EU:continue
            vs=[EU]
        else:vs=[v0] if g is None else (YG if g=='y' else WG).get(v0,[v0])
        for v in vs:
            for off in (offs or [[]]):
                seq=[(l,v)]+[(11,p) for p in pieces[1:]]+[(11,p) for p in off]
                s=pre
                for k,(ll,vv) in enumerate(seq):
                    s+=H(ll,vv,fin if k==len(seq)-1 else 0)
                res.append(s)
    return res
T='['+TONE+']?'
Fc='[ກງດນບມ]'
def P(p):return re.compile(p)
# (regex with named groups i=init, f=final cons, y/w offglide), handler -> list of korean alts
RULES=[]
def R(pat,fn):RULES.append((P(pat),fn))
def fin(m):
    f=m.groupdict().get('f');return FIN[f] if f else 0
def offg(m,vy=None):
    o=m.groupdict().get('o')
    if o=='ຍ':return [[I]]
    if o=='ວ':return [[U],[O]]
    return None
F_='(?P<f>'+Fc+')?'
O_='(?P<o>[ຍວ])?'
def make(I_):
    def V3(pre,mid,pieces):
        """register: with final consonant, with offglide ຍ/ວ, bare"""
        R(pre+I_+mid+'(?P<f>'+Fc+')',lambda m,p=pieces:build(m['i'],p,fin(m)))
        R(pre+I_+mid+'(?P<o>[ຍວ])',lambda m,p=pieces:build(m['i'],p,0,offg(m)))
        R(pre+I_+mid,lambda m,p=pieces:build(m['i'],p,0))
    # ə
    R('ເ'+I_+'[ິີ]'+T+'(?P<f>'+Fc+')',lambda m:build(m['i'],[EU],fin(m)))
    R('ເ'+I_+'[ິີ]'+T+'ຍ',lambda m:build(m['i'],[EU],0,[[I]]))
    R('ເ'+I_+'[ິີ]'+T,lambda m:build(m['i'],[EO],0))
    # ʉa
    V3('ເ','[ຶື]'+T+'ອ',[EU,A])
    # ao
    R('ເ'+I_+T+'ົ'+T+'າ',lambda m:build(m['i'],[A,O],0)+build(m['i'],[A,U],0))
    R('ເ'+I_+T+'າະ',lambda m:build(m['i'],[EO],0))
    R('ເ'+I_+'ັ'+T+'ຍ',lambda m:build(m['i'],[I,A],0))
    R('ເ'+I_+'ັ'+T+'(?P<f>'+Fc+')',lambda m:build(m['i'],[E],fin(m)))
    R('ເ'+I_+T+'ະ',lambda m:build(m['i'],[E],0))
    R('ເ'+I_+T+'ຍ',lambda m:build(m['i'],[I,A],0))
    V3('ເ',T,[E])
    R('ແ'+I_+T+'ະ',lambda m:build(m['i'],[AE],0))
    R('ແ'+I_+'ັ'+T+'(?P<f>'+Fc+')',lambda m:build(m['i'],[AE],fin(m)))
    V3('ແ',T,[AE])
    R('ໂ'+I_+T+'ະ',lambda m:build(m['i'],[O],0))
    V3('ໂ',T,[O])
    R('[ໄໃ]'+I_+T,lambda m:build(m['i'],[A,I],0))
    R(I_+'ັ'+T+'ອ(?P<f>'+Fc+')',lambda m:build(m['i'],[EO],fin(m)))
    R(I_+'ັ'+T+'ຽ(?P<f>'+Fc+')',lambda m:build(m['i'],[I,A],fin(m)))
    R(I_+'ັ'+T+'ວ(?P<f>'+Fc+')',lambda m:build(m['i'],[U,A],fin(m)))
    R(I_+'ັ'+T+'(?P<f>'+Fc+')',lambda m:build(m['i'],[A],fin(m)))
    R(I_+'ັ'+T+'(?P<o>[ຍວ])',lambda m:build(m['i'],[A],0,offg(m)))
    R(I_+'ົ'+T+'ວະ?',lambda m:build(m['i'],[U,A],0))
    R(I_+'ົ'+T+'(?P<f>'+Fc+')',lambda m:build(m['i'],[O],fin(m)))
    R(I_+'ົ'+T+'(?P<o>[ຍວ])',lambda m:build(m['i'],[O],0,offg(m)))
    R(I_+T+'ະ',lambda m:build(m['i'],[A],0))
    V3('',T+'າ',[A])
    R(I_+T+'(?:ຳ|ໍ'+T+'າ)',lambda m:build(m['i'],[A],16))
    R(I_+T+'ໍ'+T,lambda m:build(m['i'],[EO],0))
    V3('','[ິີ]'+T,[I])
    V3('','[ຶື]'+T,[EU])
    V3('','[ຸູ]'+T,[U])
    R(I_+T+'ອ(?P<f>'+Fc+')',lambda m:build(m['i'],[EO],fin(m)))
    R(I_+T+'ອ(?P<o>ຍ)',lambda m:build(m['i'],[EO],0,[[I]]))
    R(I_+T+'ຽ(?P<f>'+Fc+')',lambda m:build(m['i'],[I,A],fin(m)))
    R(I_+T+'ຽວ',lambda m:build(m['i'],[I,A],0,[[U],[O]]))
    R(I_+T+'ວ(?P<f>'+Fc+')',lambda m:build(m['i'],[U,A],fin(m)))
    R(I_+T+'ວຍ',lambda m:build(m['i'],[U,A],0,[[I]]))

make('(?P<i>(?:ຫ[ງຍນມລວ]|ຫຼ|['+C0+'])ຼ?)')
make('(?P<i>['+C0+'][ວຣ])')
LAO=re.compile('[ກ-ໍໜ-ໟ]')
HANG=re.compile('[가-힣]')
def cands(lo,p):
    """syllable candidates starting at lo[p]: list of (end, [korean alts])"""
    out=[]
    for rx,fn in RULES:
        m=rx.match(lo,p)
        if m:
            try:ks=fn(m)
            except KeyError:ks=[]
            if ks:out.append((m.end(),ks))
    return out
def lrule(k):
    # optional ㄹ받침 on an open last syllable
    c=k[-1];v=ord(c)-0xAC00
    if v%28==0:return k[:-1]+chr(ord(c)+8)
    return None
def align(lo,rd):
    kor=''.join(HANG.findall(rd))
    n=len(lo);K=len(kor)
    seen=set();stack=[(0,0)];best=(0,0)
    while stack:
        p,k=stack.pop()
        if (p,k) in seen:continue
        seen.add((p,k))
        if p>best[0] or (p==best[0] and k>best[1]):best=(p,k)
        if p>=n:
            if k==K:return None
            continue
        ch=lo[p]
        if ch=='ໆ':
            for r in range(1,9):
                if k-r>=0 and kor[k:k+r]==kor[k-r:k]:stack.append((p+1,k+r))
            continue
        if not LAO.match(ch):
            # skip non-Lao; digits/latin may consume korean freely
            q=p
            while q<n and not LAO.match(lo[q]):q+=1
            seg=lo[p:q]
            if re.search('[0-9A-Za-z໐-໙]',seg):
                for r in range(0,16):
                    if k+r<=K:stack.append((q,k+r))
            else:stack.append((q,k))
            continue
        for e,ks in cands(lo,p):
            nxt=lo[e:e+3].lstrip('ເແໂໄໃ')[:2]
            for kk in ks:
                alts=[kk]
                if nxt[:1] in('ລ','ຣ') or nxt=='ຫຼ' or nxt=='ຫລ':
                    x=lrule(kk)
                    if x:alts.append(x)
                for a in alts:
                    if kor.startswith(a,k):stack.append((e,k+len(a)))
    return (best[0],best[1],kor)
