# Lao digits -> spoken Lao words (for TTS) and Korean reading
import re
LW=['ສູນ','ໜຶ່ງ','ສອງ','ສາມ','ສີ່','ຫ້າ','ຫົກ','ເຈັດ','ແປດ','ເກົ້າ'];KW=['쑨','능','썽','쌈','씨','하','혹','쩯','뺃','까오']
def words(n):
    if n==0:return [(LW[0],KW[0])]
    out=[]
    if n>=1000:out.append((LW[n//1000]+'ພັນ',KW[n//1000]+' 판'));n%=1000
    if n>=100:out.append((LW[n//100]+'ຮ້ອຍ',KW[n//100]+' 허이'));n%=100
    t,o=divmod(n,10)
    if t:out.append(('ສິບ' if t==1 else 'ຊາວ' if t==2 else LW[t]+'ສິບ','씹' if t==1 else '싸오' if t==2 else KW[t]+'씹'))
    if o:out.append(('ເອັດ','엗') if (o==1 and t) else (LW[o],KW[o]))
    return out
DIG='໐໑໒໓໔໕໖໗໘໙'
def num(s):
    return int(''.join(str(DIG.index(c)) for c in s))
def lao(s):  # TTS text
    return re.sub('['+DIG+']+',lambda m:''.join(a for a,b in words(num(m.group(0)))),s)
def kor(s):
    return ' '.join(b for a,b in words(num(s)))
