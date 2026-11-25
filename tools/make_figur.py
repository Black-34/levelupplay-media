import os, shutil, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
# Figuren-Reel aus JSON-Konfig. Aufruf: python3 tools/make_figur.py tools/figur_cal.json queue/<ordner>/video.mp4
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/"
BLK=lambda s:ImageFont.truetype(F+"InterDisplay-Black.otf",s); BOLD=lambda s:ImageFont.truetype(F+"InterDisplay-Bold.otf",s); REG=lambda s:ImageFont.truetype(F+"Inter-Regular.otf",s)
COL={"w":(255,255,255),"b":(58,160,255),"v":(155,92,255),"g":(230,230,240)}
WM=Image.open(f"{R}/assets/brand/watermark.png").convert("RGBA").resize((130,130))
cache={}
def fit(path,focus):
    k=(path,focus)
    if k in cache: return cache[k]
    s=Image.open(f"{R}/{path}").convert("RGB"); sw,sh=s.size
    sc=max(W*1.2/sw,H*1.2/sh); cov=s.resize((int(sw*sc),int(sh*sc)),Image.LANCZOS)
    cx=int(cov.width*focus); x0=max(0,min(cov.width-int(W*1.2),cx-int(W*0.6))); y0=(cov.height-int(H*1.2))//2
    cache[k]=cov.crop((x0,y0,x0+int(W*1.2),y0+int(H*1.2))); return cache[k]
S=cfg["scenes"]; dur=S[-1]["end"]; N=int(dur*FPS); endc=cfg["end_card"]
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
fr="/tmp/fr_figur"; shutil.rmtree(fr,ignore_errors=True); os.makedirs(fr)
for n in range(N):
    t=n/FPS
    sc=[s for s in S if s["start"]<=t<s["end"]][0]; st,en=sc["start"],sc["end"]
    img=fit(sc["img"],sc["focus"]); z0,z1=sc["zoom"]
    p=(t-st)/(en-st); z=z0+(z1-z0)*p
    cw,ch=int(img.width/z),int(img.height/z); ox=(img.width-cw)//2; oy=(img.height-ch)//2
    im=img.crop((ox,oy,ox+cw,oy+ch)).resize((W,H))
    if st>0 and t-st<0.12: im=ImageEnhance.Brightness(im).enhance(1.6-5*(t-st))
    d=ImageDraw.Draw(im,"RGBA"); y=sc.get("y",150)
    for i,(txt,sz,col) in enumerate(sc["lines"]):
        a=ease((t-st-0.12*i)/0.3) if st>0 else 1.0
        if a<=0: y+=sz+44; continue
        f=BLK(sz) if sz>=70 else BOLD(sz); c=COL[col]
        tw=d.textlength(txt,font=f); dx=int(80*(1-a))
        d.rounded_rectangle((W/2-tw/2-28+dx,y-16,W/2+tw/2+28+dx,y+sz+20),22,fill=(0,0,0,int(190*a)))
        d.text((W/2+dx,y),txt,font=f,fill=c+(int(255*a),),anchor="ma",stroke_width=3,stroke_fill=(0,0,0,int(255*a)))
        y+=sz+44
    if t>=endc["start"]:
        a=ease((t-endc["start"]-0.3)/0.3)
        d.rounded_rectangle((80,1180,W-80,1420),30,fill=(0,0,0,int(200*a)),outline=COL["v"]+(int(255*a),),width=5)
        d.text((W/2,1230),endc["question"],font=BLK(58),fill=(255,255,255,int(255*a)),anchor="ma")
        d.text((W/2,1330),"@levelupplay2026 on YouTube, TikTok & Instagram",font=BOLD(32),fill=COL["b"]+(int(255*a),),anchor="ma")
    d.text((W/2,H-60),"Fan content · not affiliated with Rockstar Games",font=REG(28),fill=(255,255,255,170),anchor="mm")
    im.paste(WM,(W-60-110,H-60-150-120),WM)
    im.save(f"{fr}/{n:04d}.jpg",quality=88)
subprocess.run(["ffmpeg","-v","error","-y","-framerate",str(FPS),"-i",f"{fr}/%04d.jpg","-i",f"{R}/audio/levelup_vicecity_synthwave.mp3",
  "-t",str(dur),"-af",f"afade=t=out:st={dur-0.6}:d=0.6","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart",out],check=True)
