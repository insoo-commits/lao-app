# v3.14+ RYU: replace example sentences that were copied into 3+ places (keep the first, give the copies new examples)
# usage: python3 build_rep.py app.js rep/bNN.txt readings.json [--check]
#  rep line: bid|word index|example index|lao|ko      readings.json: {lao: reading}
import json,re,sys,collections
APP,REP,RDF=sys.argv[1:4];CHECK='--check' in sys.argv
L=open(APP,encoding='utf-8').read().split('\n')
m=re.match(r'^const DATA=JSON\.parse\((".*")\)(.*)$',L[0]);D=json.loads(json.loads(m.group(1)));B=D['B']
occ=collections.Counter(e[0] for b in B.values() for w in b['w'] for e in w[4])
rows=[l.split('|') for l in open(REP,encoding='utf-8').read().strip().split('\n')]
RD=json.load(open(RDF,encoding='utf-8')) if not CHECK else {}
seen=set();bad=0
for bid,wi,ei,lo,ko in rows:
    wi,ei=int(wi),int(ei);w=B[bid]['w'][wi];old=w[4][ei][0]
    if occ[old]<2:print('not a copy now',bid,wi,ei,old);bad+=1
    if occ[lo]>=2:print('already used',occ[lo],bid,lo)
    if lo in seen:print('dup in batch',lo)
    seen.add(lo)
    hw=w[0].split('/')[0].strip().replace('…','')
    if hw not in lo:print('no headword',bid,w[0],lo)
    if not CHECK:
        w[4][ei]=[lo,RD[lo],ko];occ[old]-=1
if CHECK:
    json.dump([r[3] for r in rows],open(REP+'.lo.json','w'),ensure_ascii=False);print('rows',len(rows),'bad',bad);sys.exit()
L[0]='const DATA=JSON.parse('+json.dumps(json.dumps(D,ensure_ascii=False,separators=(',',':')),ensure_ascii=False)+')'+m.group(2)
open(APP,'w',encoding='utf-8').write('\n'.join(L));print('replaced',len(rows))
