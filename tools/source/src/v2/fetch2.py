import json,re,time,urllib.request,urllib.parse,os
UA={'User-Agent':'LaoLangEduApp/1.0 (educational app; low volume)'}
Q={'central':'Thakhek loop landscape','colonial':'Luang Prabang Sisavangvong road','kaysone':'Kaysone Phomvihane Memorial','rocket':'Bun Bang Fai','boatlight':'Ok Phansa Laos boats candles','boatrace':'Luang Prabang boat racing','nop':'Laos wai greeting','family':'Laos family','lamvong':'Laos dance traditional Luang Prabang','mural':'Wat Xieng Thong tree of life'}
out=json.load(open('found.json')) if os.path.exists('found.json') else {}
for key,q in Q.items():
  if key in out:continue
  for k in range(3):
    try:
      u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',generator='search',gsrsearch=q+' filetype:bitmap' if key!='emblem' else q,gsrnamespace=6,gsrlimit=8,prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=960,format='json'))
      import subprocess
      d=json.loads(subprocess.run(['curl','-s','-L','-m','60','-A','language-app-builder/1.0',u],capture_output=True).stdout.decode());break
    except Exception as e:
      print(key,'err',e,flush=True);d=None;time.sleep(20+20*k)
  if d is None:continue
  rows=[]
  for pg in sorted(d.get('query',{}).get('pages',{}).values(),key=lambda x:x.get('index',0)):
    ii=pg['imageinfo'][0];m=ii.get('extmetadata',{})
    rows.append(dict(t=pg['title'],lic=m.get('LicenseShortName',{}).get('value',''),a=re.sub('<[^>]+>','',m.get('Artist',{}).get('value','')).strip()[:60],w=ii.get('width'),h=ii.get('height'),th=ii.get('thumburl','')))
  if not rows:print(key,'empty',flush=True);time.sleep(20);continue
  out[key]=rows;json.dump(out,open('found.json','w'),ensure_ascii=False,indent=1);print(key,len(rows),flush=True);time.sleep(8)
print('done')
