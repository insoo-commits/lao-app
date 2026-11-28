import sys,re,collections
sys.path.insert(0,'.')
from load import *
s,d,N,R=load()
pats={'ເCີຍ':r'ເ[ກ-ຮໜໝ]ຼ?ີ[່້໊໋]?ຍ.{0,4}','ັຍ':r'.{0,3}ັ[່້]?ຍ.{0,2}','ຣ':r'.{0,4}ຣ.{0,4}','ືອ no ເ':r'(?<!ເ)(?<!ເຫ)[ກ-ຮໜໝ]ຼ?[ຶື][່້]?ອ(?![ິີຶືຸູັົາຳໍ່້ອຽວະ]).{0,3}','ຫນ/ຫມ':r'ຫ[ນມ].{0,4}','໌':r'.{0,5}໌','ໍາ':r'.{0,3}ໍ[່້]?າ.{0,2}','double tone':r'.{0,3}[່້໊໋]{2}.{0,3}','ໃ':r'ໃ[ກ-ຮໜໝ]ຼ?[່້]?'}
res={k:collections.Counter() for k in pats}
for wh,lo,rd,ko in items(d):
    for k,p in pats.items():
        for m in re.finditer(p,lo):res[k][m.group(0)]+=1
for k in pats:
    print('==',k,len(res[k]))
    for a,b in res[k].most_common(80):print('  ',a,b)
hw=collections.OrderedDict()
for bid,b in d['B'].items():
    for w in b['w']:hw.setdefault(w[0],(w[2],w[3]))
print('distinct headwords',len(hw))
