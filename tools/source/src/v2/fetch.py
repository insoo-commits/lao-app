import json,re,time,urllib.request,urllib.parse,sys
UA={'User-Agent':'LaoLangEduApp/1.0 (educational, low volume)'}
def get(params):
  for k in range(8):
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    try:
      t=urllib.request.urlopen(urllib.request.Request(u,headers=UA)).read().decode()
      if t.startswith('{'):return json.loads(t)
    except Exception as e: print('err',e,flush=True)
    time.sleep(60+40*k)
  raise SystemExit('rate')
out={}
d=get(dict(action='query',titles='File:Emblem of Laos (2025-).svg',prop='imageinfo|revisions',rvprop='content',rvslots='main',iiprop='extmetadata',format='json'))
p=list(d['query']['pages'].values())[0]
out['emblem2025']=p['revisions'][0]['slots']['main']['*'][:2500]
time.sleep(25)
for key,q in [('patuxai','Patuxai Vientiane'),('assembly','National Assembly Laos building'),('train','Laos China railway EMU'),('hmong','Hmong New Year Laos'),('thatluang','Pha That Luang Vientiane')]:
  d=get(dict(action='query',generator='search',gsrsearch=q,gsrnamespace=6,gsrlimit=10,prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=900,format='json'))
  rows=[]
  for pg in sorted(d.get('query',{}).get('pages',{}).values(),key=lambda x:x.get('index',0)):
    ii=pg['imageinfo'][0];m=ii.get('extmetadata',{})
    rows.append(dict(t=pg['title'],lic=m.get('LicenseShortName',{}).get('value',''),a=re.sub('<[^>]+>','',m.get('Artist',{}).get('value','')).strip()[:60],w=ii.get('width'),h=ii.get('height'),th=ii.get('thumburl','')))
  out[key]=rows;json.dump(out,open('found.json','w'),ensure_ascii=False,indent=1);print(key,len(rows),flush=True);time.sleep(25)
json.dump(out,open('found.json','w'),ensure_ascii=False,indent=1)
print('done')
