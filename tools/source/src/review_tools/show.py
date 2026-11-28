import sys
sys.path.insert(0,'.')
from load import *
s,d,N,R=load()
want=set(sys.argv[1:])
for wh,lo,rd,ko in items(d):
    if wh in want:print(wh,'|',lo,'|',rd,'|',ko)
