# v2.63: 라오스 탭(P8) 정보 화면. usage: python3 build_v263.py /home/user/lao-app credits.json
import sys,json,re,os,importlib.util
R=sys.argv[1];CR=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
sp=importlib.util.spec_from_file_location('li',os.path.join(os.path.dirname(__file__),'laos_info.py'));li=importlib.util.module_from_spec(sp);sp.loader.exec_module(li)
def ph(m):
  k,cap=m.group(1),m.group(2);c=CR.get(k)
  if not c:return ''
  sm=' sm' if k=='emblem' else ''
  return f'<figure class="ph{sm}"><img src="img/la/{k}.jpg" width="{c["w"]}" height="{c["h"]}" loading="lazy" alt=""><figcaption>{cap}<small>사진: {c["a"]} · {c["lic"]} · Wikimedia Commons</small></figcaption></figure>'
B={};blab={}
for bid,(t,lo,html) in li.B.items():
  html=re.sub(r'@@PHOTO:([a-z0-9]+):(.*?)@@',ph,html)
  html=re.sub(r'((?:[가-힣]+ )?[가-힣]+) (<span class="lo">[^<]*</span>) <span class="r">([^<]*)</span>',lambda m:(m.group(1)+' '+m.group(2)) if m.group(1).replace(' ','')==m.group(3).replace(' ','') or m.group(1).split(' ')[-1]==m.group(3) else m.group(0),html)
  html=html.replace('<div class="top2"><div></div><div>','<div class="top1"><div>')
  B[bid]=dict(t=t,h=lo,i="",w=[],tp=[],nx=[],pr=[],dl=[],sm=None,qz=[],info=f'<h2>{t}</h2><div class="sub2 lo">{lo}</div>'+html)
  blab[bid]=[t,lo]
part=dict(id='P8',ko='라오스',desc='라오스를 이해하기 위한 자료',subs=[dict(id=sid,name=nm,b=[k for k in li.B if k.startswith('8-%02d-'%(n+1))]) for n,(sid,nm) in enumerate(li.SUBS)])
part['subs']=[x for x in part['subs'] if x['b']]
line='/* v2.63 RYU: 라오스 탭(P8) = info pages, no words/audio (src/v2/laos_info.py, build_v263.py) */const LAOINFO='+json.dumps(dict(part=part,B=B,blab=blab),ensure_ascii=False,separators=(',',':'))+';DATA.P.push(LAOINFO.part);Object.assign(DATA.B,LAOINFO.B);\n'
s=open(R+'/app.js').read()
_m=re.match(r'const DATA=JSON\.parse\((".*")\)(;?)\s*$',s.split('\n',1)[0]);_D=json.loads(json.loads(_m.group(1)))['B']
_T=lambda i:(B[i]['t'] if i in B else _D[i]['t'])
line=re.sub(r'<button data-goto=\\"([0-9-]+)\\">[0-9-]+</button>',lambda m:('<button data-goto=\\"%s\\">%s %s</button>'%(m.group(1),m.group(1),_T(m.group(1)))) if (m.group(1) in B or m.group(1) in _D) else '',line)
s=re.sub(r'/\* v2\.63 RYU: 라오스 탭[^\n]*\n','',s)
a='const PARTEN={P1:"SOUND",P2:"ROOT",P3:"MEANING",P4:"PAIR",P5:"SCENE",P6:"LETTERS",P7:"GRAMMAR"'
assert a in s
s=s.replace(a,line+a)
s=s.replace('P7:"GRAMMAR"}','P7:"GRAMMAR",P8:"LAOS"}')
open(R+'/app.js','w').write(s)
print('ok',len(line))
