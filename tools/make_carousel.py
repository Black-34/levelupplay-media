# Usage: python3 make_carousel.py config.json outdir   -> 1.jpg..N.jpg (1080x1350)
import sys, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
cfg=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
W,H=1080,1350; F="/usr/share/fonts/opentype/inter/"
BLK=lambda s:ImageFont.truetype(F+"InterDisplay-Black.otf",s); BOLD=lambda s:ImageFont.truetype(F+"InterDisplay-Bold.otf",s); REG=lambda s:ImageFont.truetype(F+"Inter-Regular.otf",s)
acc=tuple(cfg["color"]); base=os.path.dirname(os.path.abspath(sys.argv[1]))
def bg(path,dark=0.45,blur=0,focus=0.5):
    im=Image.open(os.path.join(base,path) if not path.startswith('/') else path).convert("RGB"); sw,sh=im.size
    cw=int(sh*W/H)
    if cw<=sw: x0=max(0,min(sw-cw,int(sw*focus-cw/2))); im=im.crop((x0,0,x0+cw,sh))
    im=im.resize((W,H),Image.LANCZOS)
    if blur: im=im.filter(ImageFilter.GaussianBlur(blur))
    im=ImageEnhance.Brightness(im).enhance(dark)
    g=Image.new("L",(1,H)); [g.putpixel((0,y),int(255*min(1,max(0,(y-H*0.25)/(H*0.6))))) for y in range(H)]
    return Image.composite(Image.new("RGB",(W,H),(10,10,20)),im,g.resize((W,H)))
def wrap(d,text,font,maxw):
    lines=[]
    for para in text.split("\n"):
        line=""
        for w in para.split():
            t=(line+" "+w).strip()
            if d.textlength(t,font=font)>maxw and line: lines.append(line); line=w
            else: line=t
        lines.append(line)
    return lines
n=len(cfg["slides"])
for i,s in enumerate(cfg["slides"]):
    kind=s.get("kind","tip")
    im=bg(s.get("bg",cfg["bg"]),dark=0.75 if kind=="cover" else 0.4,blur=0 if kind=="cover" else 2,focus=s.get("focus",0.5))
    d=ImageDraw.Draw(im,"RGBA")
    if kind=="cover":
        d.rounded_rectangle([60,70,60+d.textlength(cfg["kicker"],font=BLK(40))+48,140],radius=20,fill=acc+(255,))
        d.text((84,105),cfg["kicker"],font=BLK(40),fill=(255,255,255),anchor="lm")
        y=H-560
        for ln in wrap(d,s["title"],BLK(104),W-120): d.text((60,y),ln,font=BLK(104),fill=(255,255,255)); y+=112
        y+=10
        for ln in wrap(d,s["sub"],BOLD(50),W-120): d.text((60,y),ln,font=BOLD(50),fill=acc+(255,)); y+=62
        d.text((60,H-90),"Wischen →",font=BOLD(40),fill=(255,255,255))
    elif kind=="cta":
        y=300
        for ln in wrap(d,s["title"],BLK(88),W-120): d.text((60,y),ln,font=BLK(88),fill=(255,255,255)); y+=98
        y+=30
        for ln in wrap(d,s["text"],BOLD(46),W-120): d.text((60,y),ln,font=BOLD(46),fill=(235,235,245)); y+=60
        d.rounded_rectangle([60,H-330,W-60,H-200],radius=40,fill=acc+(255,))
        d.text((W//2,H-265),s.get("button","Folgen für mehr GTA 6 Tipps"),font=BLK(46),fill=(255,255,255),anchor="mm")
    else:
        d.text((60,80),f"{s['num']}",font=BLK(150),fill=acc+(255,))
        y=270
        for ln in wrap(d,s["title"],BLK(78),W-120): d.text((60,y),ln,font=BLK(78),fill=(255,255,255)); y+=88
        y+=30
        top=y; lines=wrap(d,s["text"],REG(44),W-180)
        h=len(lines)*60+60
        d.rounded_rectangle([50,top,W-50,top+h],radius=30,fill=(255,255,255,235))
        d.rectangle([50,top+24,62,top+h-24],fill=acc+(255,))
        y=top+30
        for ln in lines: d.text((90,y),ln,font=REG(44),fill=(25,25,35)); y+=60
    d.text((60,H-50),cfg.get("footer","Fan-Content · nicht mit Rockstar Games verbunden"),font=REG(24),fill=(255,255,255,170))
    d.text((W-60,H-50),f"{i+1}/{n}",font=BOLD(28),fill=(255,255,255,200),anchor="ra")
    lp=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","assets","brand","watermark.png")
    if os.path.exists(lp):
        lg=Image.open(lp).resize((130,130)); lg.putalpha(lg.getchannel("A").point(lambda p:int(p*0.85))); im.paste(lg,(W-60-110,60),lg)
    im.save(f"{out}/{i+1}.jpg",quality=90)
