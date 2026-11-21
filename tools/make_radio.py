import sys, json, math, os, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/"
BLK=lambda s:ImageFont.truetype(F+"InterDisplay-Black.otf",s); BOLD=lambda s:ImageFont.truetype(F+"InterDisplay-Bold.otf",s); REG=lambda s:ImageFont.truetype(F+"Inter-Regular.otf",s)
acc=tuple(cfg["color"])
_lp=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","assets","brand","watermark.png")
LOGO=Image.open(_lp).resize((130,130)) if os.path.exists(_lp) else None
src=Image.open(cfg["bg"]).convert("RGB")
# crop to 9:16 around focus x
sw,sh=src.size; cw=int(sh*9/16); cx=int(sw*cfg.get("focus",0.5)); x0=max(0,min(sw-cw,cx-cw//2))
bg=src.crop((x0,0,x0+cw,sh)).resize((int(W*1.12),int(H*1.12)),Image.LANCZOS)
bgd=ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(2))).enhance(0.72)
shade=Image.new("L",(1,H)); 
for y in range(H): shade.putpixel((0,y),int(60+150*(y/H)))
shade=shade.resize((W,H))
logo=Image.open(cfg["logo"]).convert("RGBA"); logo.thumbnail((560,270))
songs=cfg["songs"][:10]
dur=15.0; N=int(dur*FPS)
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
fr="fr_"+cfg["id"]; shutil.rmtree(fr,ignore_errors=True); os.makedirs(fr)
for n in range(N):
    t=n/FPS; z=1+0.06*t/dur
    b=bgd.resize((int(bgd.width*z/1.12*1.0),int(bgd.height*z/1.12*1.0)))
    ox=(b.width-W)//2; oy=(b.height-H)//2; im=b.crop((ox,oy,ox+W,oy+H))
    im=Image.composite(Image.new("RGB",(W,H),(8,8,18)),im,shade)
    d=ImageDraw.Draw(im,"RGBA")
    # hook
    a=ease(t/0.5)
    d.text((70,110-40*(1-a)),"GTA 6 RADIO",font=BLK(64),fill=acc+(255,))
    d.text((70,190),"Welche Songs laufen hier?",font=BOLD(54),fill=(255,255,255,int(255*a)))
    la=ease((t-0.3)/0.6); lg=logo.copy(); 
    if la<1: lg.putalpha(lg.getchannel("A").point(lambda p:int(p*la)))
    if cfg.get('plate') and la>0:
        px=(W-lg.width)//2; py=300+int(30*(1-la)); d.rounded_rectangle([px-30,py-20,px+lg.width+30,py+lg.height+20],radius=36,fill=(255,255,255,int(225*la)))
    im.paste(lg,((W-lg.width)//2,300+int(30*(1-la))),lg)
    y0=300+logo.height+40
    d.text((W//2,y0),cfg["genre"],font=BOLD(42),fill=(255,255,255,220),anchor="ma")
    y=y0+80
    for i,(s,artist) in enumerate(songs):
        st=1.2+i*0.75; p=ease((t-st)/0.35)
        if p<=0: break
        xo=int(60*(1-p)); al=int(255*p)
        d.rounded_rectangle([60+xo,y,W-60+xo,y+92],radius=24,fill=(255,255,255,int(28*p)))
        d.text((90+xo,y+46),f"{i+1}",font=BLK(46),fill=acc+(al,),anchor="lm")
        tf=BOLD(40); title=s
        while d.textlength(title,font=tf)>760 and len(title)>4: title=title[:-2]
        if title!=s: title=title.rstrip()+"…"
        d.text((170+xo,y+27),title,font=tf,fill=(255,255,255,al),anchor="lm")
        d.text((170+xo,y+68),artist,font=REG(32),fill=(220,220,230,al),anchor="lm")
        y+=100
    if t>dur-2.6:
        p=ease((t-(dur-2.6))/0.4)
        d.rounded_rectangle([50,80,W-50,260],radius=40,fill=acc+(int(255*p),))
        d.text((W//2,170),cfg["cta"],font=BLK(50),fill=(255,255,255,int(255*p)),anchor="mm")
    d.text((W//2,H-60),"Fan-Content · Quelle: Rockstar Games / Community-Liste",font=REG(28),fill=(255,255,255,170),anchor="mm")
    if LOGO is not None: im.paste(LOGO,(W-60-110,1920-60-150),LOGO)
    im.save(f"{fr}/{n:04d}.jpg",quality=88)
subprocess.run(["ffmpeg","-v","error","-y","-framerate",str(FPS),"-i",f"{fr}/%04d.jpg","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart",out],check=True)
shutil.rmtree(fr)
