import sys,collections
sys.path.insert(0,'.')
from load import *;from tr import *
s,d,N,R=load()
fl=[];n=0
for wh,lo,rd,ko in items(d):
    n+=1
    r=align(lo,rd)
    if r:fl.append((wh,lo,rd,r))
print('items',n,'flags',len(fl))
cnt=collections.Counter()
for wh,lo,rd,(p,k,kor) in fl:
    cnt[(lo[p:p+6],kor[k:k+3])]+=1
for (a,b),c in cnt.most_common(int(sys.argv[1]) if len(sys.argv)>1 else 60):print(c,a,'|',b)
import pickle;pickle.dump(fl,open('fl.pkl','wb'))
