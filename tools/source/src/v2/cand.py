# usage: cand.py key:idx,idx ...  -> downloads thumbs, makes sheet.jpg
import json,urllib.request,time,sys,os
from PIL import Image,ImageDraw
UA={'User-Agent':'LaoLangEduApp/1.0 (educational app; low volume)'}
d=json.load(open('found.json'));ims=[]
for a in sys.argv[1:]:
  k,ix=a.split(':')
  for i in map(int,ix.split(',')):
    if i>=len(d.get(k,[])):continue
    f=f'th/{k}_{i}.jpg'
    if not os.path.exists(f):
      import subprocess
      for t in range(2):
        b=subprocess.run(['curl','-s','-L','-m','60','-A','language-app-builder/1.0',d[k][i]['th'].replace('/640px-','/960px-')],capture_output=True).stdout
        time.sleep(4)
        if b[:2]==b'\xff\xd8' or b[:4]==b'\x89PNG':open(f,'wb').write(b);break
        print(k,i,'fail',b[:40])
    if os.path.exists(f):
      im=Image.open(f).convert('RGB');im.thumbnail((330,250));c=Image.new('RGB',(340,275),'white');c.paste(im,(5,20));ImageDraw.Draw(c).text((5,3),f'{k}:{i} {d[k][i]["lic"]}',fill='black');ims.append(c)
n=len(ims);cols=5;rows=(n+cols-1)//cols
s=Image.new('RGB',(340*cols,275*rows),'white')
for j,c in enumerate(ims):s.paste(c,(340*(j%cols),275*(j//cols)))
s.save('sheet.jpg',quality=80);print(n)
