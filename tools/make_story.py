import sys,re
from PIL import Image,ImageFilter,ImageDraw,ImageFont,ImageEnhance
F="/usr/share/fonts/opentype/inter/"
fr=Image.open(sys.argv[1]).convert('RGB')
bg=ImageEnhance.Brightness(fr.resize((1080,1920)).filter(ImageFilter.GaussianBlur(40))).enhance(0.45)
w=860; h=int(w*1920/1080); sm=fr.resize((w,h))
bg.paste(sm,((1080-w)//2,70))
d=ImageDraw.Draw(bg); f=ImageFont.truetype(F+"InterDisplay-Black.otf",60)
t="Neuer Beitrag – jetzt ansehen"; tw=d.textlength(t,font=f)
d.rounded_rectangle((80,1640,1000,1760),radius=60,fill="#9b5cff")
d.text((540,1700),t,font=f,fill="white",anchor="mm")
bg.save(sys.argv[2],quality=90)
