# v12.32: Lao ə vowel (ເ◌ີ, ເ◌ິ+final) -> Korean ㅡ (RYU 2026-11-13: "으로 하자"). Aligns ə/ɔ syllables to Korean ㅓ syllables in order.
import json,re,sys
APP=sys.argv[1];DRY=len(sys.argv)>2
s=open(APP,encoding='utf-8').read()
i=s.find('const DATA=');j=s.find('\n',i);lit=s[i+11:j].rstrip(';');d=json.loads(json.loads(lit[11:-1]))
INI={'ກ':1,'ຂ':15,'ຄ':15,'ງ':11,'ຈ':13,'ສ':10,'ຊ':10,'ຍ':2,'ດ':3,'ຕ':4,'ຖ':16,'ທ':16,'ນ':2,'ບ':7,'ປ':8,'ຜ':17,'ຝ':17,'ພ':17,'ຟ':17,'ມ':6,'ຢ':11,'ຣ':5,'ລ':5,'ວ':11,'ຫ':18,'ອ':11,'ຮ':18,'ໜ':2,'ໝ':6}
FIN={'ກ':1,'ດ':7,'ບ':17,'ນ':4,'ມ':16,'ງ':21}
C='[ກ-ຮໜໝ]';T='[່້໊໋]?'
pat=re.compile(r'(?P<schwa>ເ(?P<c1>ຫ[ງຍນມລວ]|'+C+')ຼ?[ິີ]'+T+'(?P<f1>[ກດບນມງ](?![ິີາັຽົໍີຸູືຶ່້ະ]))?)|(?<![ເແໂໄໃ])(?P<o>(?P<c2>ຫ[ງຍນມລວ]|'+C+')ຼ?'+T+'(?:ໍ'+T+'|ອ(?P<f2>[ກດບນມງ](?![ິີາັຽົໍີຸູືຶ່້ະ]))?))')
def ini(c):return INI.get(c[-1] if len(c)==2 else c,None)
def prods(lo):
    out=[]
    for m in pat.finditer(lo):
        if m.group('schwa'):out.append((ini(m.group('c1')),FIN.get(m.group('f1') or '',0),bool(m.group('f1'))))  # open ə (ເດີ, ເຝີ, ເບີ) stays 어
        else:out.append((ini(m.group('c2')),FIN.get(m.group('f2') or '',0),False))
    return out
CH=[]
def fix(lo,rd):
    P=prods(lo)
    if not any(p[2] for p in P):return rd
    used=[False]*len(P);o=list(rd)
    for k,ch in enumerate(rd):
        if not('가'<=ch<='힣'):continue
        v=ord(ch)-0xAC00;L,V,Tt=v//588,(v%588)//28,v%28
        if V!=4:continue  # ㅓ
        for n,p in enumerate(P):
            if used[n]:continue
            if p[0]==L and p[1]==Tt:
                used[n]=True
                if p[2]:o[k]=chr(0xAC00+L*588+18*28+Tt)
                break
    r=''.join(o)
    if r!=rd:CH.append((lo,rd,r))
    return r
for b in d['B'].values():
    for w in b['w']:
        w[2]=fix(w[0],w[2])
        for e in w[4]:e[1]=fix(e[0],e[1])
    for p in b['pr']:
        for x in p:x[1]=fix(x[0],x[1])
    for dd in b['dl']:dd[2]=fix(dd[1],dd[2])
    if b.get('sm') and len(b['sm'])>1:b['sm'][1]=fix(b['sm'][0],b['sm'][1])
m=re.search(r'NRD=(\{.*?\}),NFREQ',s);R=json.loads(m.group(1))
for k in R:R[k]=fix(k,R[k])
print(len(CH))
for c in CH[:int(sys.argv[2]) if DRY else 0]:print(c[0],'|',c[1],'→',c[2])
if not DRY:
    new='const DATA=JSON.parse('+json.dumps(json.dumps(d,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+');'
    s2=s[:i]+new+s[j:]
    m=re.search(r'NRD=(\{.*?\}),NFREQ',s2)
    s2=s2[:m.start(1)]+json.dumps(R,ensure_ascii=False,separators=(',',':'))+s2[m.end(1):]
    open(APP,'w',encoding='utf-8').write(s2)
# pass 2 (run with "qz"): quiz answers and tips "ລາວ(독음)"
