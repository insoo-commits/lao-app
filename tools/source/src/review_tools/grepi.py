import sys,re
sys.path.insert(0,'.')
from load import *
s,d,N,R=load()
for wh,lo,rd,ko in items(d):
    if any(re.search(p,lo) for p in sys.argv[1:]):print(wh,'|',lo,'|',rd,'|',ko)
