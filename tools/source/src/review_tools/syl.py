import re
C0='[ກຂຄງຈສຊຍດຕຖທນບປຜຝພຟມຢຣລວຫອຮໜໝ]'
INIT='(?:ຫ[ງຍນມລວ]|ຫຼ|'+C0+'ວ|'+C0+'ຣ|'+C0+')ຼ?'
T='[່້໊໋]?'
F='[ກງຍດນບມວ]'
ALTS=[
 'ເ'+INIT+'[ິີ]'+T+F+'?',
 'ເ'+INIT+'[ຶື]'+T+'ອ'+F+'?',
 'ເ'+INIT+T+'ົ'+T+'າ',
 'ເ'+INIT+T+'າະ',
 'ເ'+INIT+'ັ'+T+F,
 'ເ'+INIT+T+'ະ',
 'ເ'+INIT+T+F+'?',
 'ແ'+INIT+T+'ະ','ແ'+INIT+'ັ'+T+F,'ແ'+INIT+T+F+'?',
 'ໂ'+INIT+T+'ະ','ໂ'+INIT+T+F+'?',
 'ໄ'+INIT+T,'ໃ'+INIT+T,
 INIT+'ັ'+T+'[ອຽວ]'+F, INIT+'ັ'+T+F,
 INIT+'ົ'+T+'ວະ', INIT+'ົ'+T+'ວ', INIT+'ົ'+T+F,
 INIT+T+'ະ', INIT+T+'າ'+F+'?', INIT+T+'ຳ', INIT+T+'ໍ'+T+'າ', INIT+T+'ໍ'+T,
 INIT+'[ິີຶືຸູ]'+T+F+'?',
 INIT+T+'ອ'+F, INIT+T+'ຽ'+F, INIT+T+'ວ'+F,
 'ໆ','ຯ',
]
SYL='(?:'+'|'.join(ALTS)+')'
FULL=re.compile('^'+SYL+'+$')
ONE=re.compile(SYL)
RUN=re.compile('[ກ-ໍໜ-ໟ]+')
def bad_runs(text):
    out=[]
    for m in RUN.finditer(text):
        r=m.group(0)
        if not FULL.match(r):out.append(r)
    return out
def longest_prefix(r):
    # find the longest prefix that parses, to locate the problem
    best=0
    for k in range(len(r),0,-1):
        if FULL.match(r[:k]):best=k;break
    return best
