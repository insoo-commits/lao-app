# usage: inst.py key=srckey:idx ...   (key = photo key in content)
import json,sys,os,re
from PIL import Image
R='/home/user/lao-app';CF='/mnt/project-files/lao-app/src/v2/laos_credits.json'
d=json.load(open('found.json'));C=json.load(open(CF)) if os.path.exists(CF) else {}
os.makedirs(R+'/img/la',exist_ok=True)
for a in sys.argv[1:]:
  key,src=a.split('=');sk,i=src.split(':');i=int(i);r=d[sk][i]
  im=Image.open(f'th/{sk}_{i}.jpg')
  if im.mode in('RGBA','LA','P'):
    im=im.convert('RGBA');bg=Image.new('RGB',im.size,'white');bg.paste(im,mask=im.split()[3]);im=bg
  im=im.convert('RGB')
  if key=='emblem':im.thumbnail((360,360))
  if im.width>640:im=im.resize((640,round(im.height*640/im.width)),Image.LANCZOS)
  if im.height>im.width*0.8:  # crop tall images to 4:3
    h=round(im.width*0.75);t=(im.height-h)//3;im=im.crop((0,t,im.width,t+h))
  im.save(f'{R}/img/la/{key}.jpg',quality=70,optimize=True,progressive=True)
  a_=re.sub(r'\s+',' ',r['a']).strip();a_=re.sub(r' from .*$','',a_) or 'Wikimedia Commons'
  C[key]=dict(w=im.width,h=im.height,a=a_,lic=r['lic'],src=r['t'])
  print(key,os.path.getsize(f'{R}/img/la/{key}.jpg'),a_,r['lic'])
json.dump(C,open(CF,'w'),ensure_ascii=False,indent=1)
