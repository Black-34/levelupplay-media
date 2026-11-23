import os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
# Mandy-Reel (Figuren-Serie). Aufruf: python3 tools/make_mandy.py queue/19-figur-mandy/video.mp4
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
out=sys.argv[1]
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/"
BLK=lambda s:ImageFont.truetype(F+"InterDisplay-Black.otf",s); BOLD=lambda s:ImageFont.truetype(F+"InterDisplay-Bold.otf",s); REG=lambda s:ImageFont.truetype(F+"Inter-Regular.otf",s)
BLUE=(58,160,255); VIO=(155,92,255)
WM=Image.open(f"{R}/assets/brand/watermark.png").convert("RGBA").resize((130,130))
def fit(path,focus=0.5):
    s=Image.open(path).convert("RGB"); sw,sh=s.size
    bg=s.resize((int(sw*H/sh*1.0),H)) if sw/sh<W/H else None
    # Hintergrund: unscharf füllend, Vordergrund: volle Breite
    cov=s.copy(); sc=max(W*1.2/sw,H*1.2/sh); cov=cov.resize((int(sw*sc),int(sh*sc)))
    cx=int(cov.width*focus); x0=max(0,min(cov.width-int(W*1.2),cx-int(W*0.6))); y0=(cov.height-int(H*1.2))//2
    cov=cov.crop((x0,y0,x0+int(W*1.2),y0+int(H*1.2)))
    return cov
def portrait(path):
    s=Image.open(path).convert("RGB")
    back=ImageEnhance.Brightness(s.resize((int(H*1.2),int(H*1.2))).filter(ImageFilter.GaussianBlur(30))).enhance(0.5)
    x=(back.width-int(W*1.2))//2; back=back.crop((x,0,x+int(W*1.2),int(H*1.2)))
    fg=s.resize((int(W*1.2),int(W*1.2)),Image.LANCZOS); back.paste(fg,(0,int(H*1.2*0.30)))
    return back
P=portrait(f"{R}/assets/fotos_nutzer/mandy_portrait.webp")
BR=fit(f"{R}/assets/rockstar/shots/gta6_18_Brian_Heder_03.jpg",0.5)
JA=fit(f"{R}/assets/rockstar/shots/gta6_02_Jason_Duval_01.jpg",0.78)
# Szenen: (start, ende, bild, zoom-start, zoom-ende, texte)
S=[(0,3.2,P,1.0,1.12,[("EVERYONE IS",96,(255,255,255)),("SEARCHING",96,(255,255,255)),("FOR HER",120,BLUE)]),
   (3.2,5.6,BR,1.0,1.08,[("MANDY RUSSELL",96,(255,255,255)),("Brian's tenant in the",54,(230,230,240)),("Leonida Keys",70,BLUE)]),
   (5.6,8.0,JA,1.08,1.0,[("JASON HAS TO",80,(255,255,255)),("COLLECT HER RENT",80,BLUE),("early in Chapter 1",50,(230,230,240))]),
   (8.0,10.0,P,1.12,1.0,[("SHE HAS A",90,(255,255,255)),("CRUSH ON JASON",90,VIO)]),
   (10.0,12.0,P,1.0,1.05,[("PLAYED BY",70,(255,255,255)),("LEXIE SHOAIBI",96,BLUE)])]
dur=12.0; N=int(dur*FPS)
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
fr="/tmp/fr_mandy"; shutil.rmtree(fr,ignore_errors=True); os.makedirs(fr)
for n in range(N):
    t=n/FPS
    st,en,img,z0,z1,lines=[s for s in S if s[0]<=t<s[1]][0]
    p=(t-st)/(en-st); z=z0+(z1-z0)*p
    cw,ch=int(img.width/z),int(img.height/z); ox=(img.width-cw)//2; oy=(img.height-ch)//2
    im=img.crop((ox,oy,ox+cw,oy+ch)).resize((W,H))
    if st>0 and t-st<0.12: im=ImageEnhance.Brightness(im).enhance(1.6-5*(t-st))  # Blitz-Schnitt
    d=ImageDraw.Draw(im,"RGBA")
    y=150
    for i,(txt,sz,col) in enumerate(lines):
        a=ease((t-st-0.12*i)/0.3) if st>0 else 1.0
        if a<=0: y+=sz+40; continue
        f=BLK(sz) if sz>=70 else BOLD(sz)
        tw=d.textlength(txt,font=f); dx=int(80*(1-a))
        d.rounded_rectangle((W/2-tw/2-28+dx,y-16,W/2+tw/2+28+dx,y+sz+20),22,fill=(0,0,0,int(190*a)))
        d.text((W/2+dx,y),txt,font=f,fill=col+(int(255*a),),anchor="ma",stroke_width=3,stroke_fill=(0,0,0,int(255*a)))
        y+=sz+44
    if t>=10.0:
        a=ease((t-10.3)/0.3)
        d.rounded_rectangle((80,1180,W-80,1420),30,fill=(0,0,0,int(200*a)),outline=VIO+(int(255*a),),width=5)
        d.text((W/2,1230),"Team Mandy? Yes or no?",font=BLK(62),fill=(255,255,255,int(255*a)),anchor="ma")
        d.text((W/2,1330),"@levelupplay2026 on YouTube, TikTok & Instagram",font=BOLD(32),fill=BLUE+(int(255*a),),anchor="ma")
    d.text((W/2,H-60),"Fan content · not affiliated with Rockstar Games",font=REG(28),fill=(255,255,255,170),anchor="mm")
    im.paste(WM,(W-60-110,H-60-150-120),WM)
    im.save(f"{fr}/{n:04d}.jpg",quality=88)
subprocess.run(["ffmpeg","-v","error","-y","-framerate",str(FPS),"-i",f"{fr}/%04d.jpg","-i",f"{R}/audio/levelup_vicecity_synthwave.mp3",
  "-t",str(dur),"-af",f"afade=t=out:st={dur-0.6}:d=0.6","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart",out],check=True)
