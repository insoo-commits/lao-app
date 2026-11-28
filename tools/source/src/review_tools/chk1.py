import sys,json,re,collections
sys.path.insert(0,'.')
from load import *;from syl import *
s,d,N,R=load()
bad=collections.OrderedDict()
n=0
for wh,lo,rd,ko in items(d):
    n+=1
    for r in bad_runs(lo):
        k=longest_prefix(r)
        bad.setdefault(r[max(0,k-6):k+8],[]).append(wh)
for k in N:
    for r in bad_runs(k):bad.setdefault(r,[]).append('NDICT')
print('items',n,'bad kinds',len(bad))
for k,v in bad.items():print(k,len(v),v[:3])
