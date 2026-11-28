import json,re
APP='/home/user/lao-app/app.js'
def load():
    s=open(APP,encoding='utf-8').read()
    i=s.find('const DATA=');j=s.find('\n',i);lit=s[i+11:j].rstrip(';')
    d=json.loads(json.loads(lit[11:-1]))
    m=re.search(r'const NDICT=(\{.*?\}),NRD=(\{.*?\}),NFREQ=',s)
    return s,d,json.loads(m.group(1)),json.loads(m.group(2))
def items(d):
    """yield (where, lo, rd, ko) for every Lao string with a reading"""
    for bid,b in d['B'].items():
        for wi,w in enumerate(b['w']):
            yield (bid+' w%d'%wi,w[0],w[2],w[3])
            for ei,e in enumerate(w[4]):yield (bid+' w%d e%d'%(wi,ei),e[0],e[1],e[2])
        for pi,p in enumerate(b['pr']):
            for xi,x in enumerate(p):yield (bid+' pr%d.%d'%(pi,xi),x[0],x[1],x[2])
        for di,dd in enumerate(b['dl']):yield (bid+' dl%d'%di,dd[1],dd[2],dd[3])
        if b.get('sm') and b['sm'][0]:yield (bid+' sm',b['sm'][0],b['sm'][1],b['sm'][2])
