import os, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1080,1920
REPO="/home/claude/repo"; SRC="/mnt/user-data/uploads/Levelup/videos"; OUT="/home/claude/work/out"
os.makedirs(OUT,exist_ok=True)
FI="/usr/share/fonts/opentype/inter/"
def font(w,s):
    for n in {"blk":["Inter-Black.otf","Inter-ExtraBold.otf"],"bold":["Inter-Bold.otf"],"reg":["Inter-Regular.otf"]}[w]:
        p=FI+n
        if os.path.exists(p): return ImageFont.truetype(p,s)
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",s)
BLUE=(58,160,255); VIO=(155,92,255)
WM=Image.open(f"{REPO}/assets/brand/watermark.png").convert("RGBA")
MUSIC=f"{REPO}/audio/levelup_vicecity_synthwave.mp3"

def overlay_png(path, lines, sub=None, color=BLUE, top=130, first=(255,255,255)):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    y=top
    for i,(t,sz) in enumerate(lines):
        f=font("blk",sz)
        tw=d.textlength(t,font=f)
        pad=26
        d.rounded_rectangle((W/2-tw/2-pad,y-14,W/2+tw/2+pad,y+sz+22),22,fill=(0,0,0,200),outline=color+(255,) if i==0 else None,width=6)
        d.text((W/2,y),t,font=f,fill=first+(255,) if i==0 else color+(255,),anchor="ma",stroke_width=3,stroke_fill=(0,0,0,255))
        y+=sz+52
    if sub:
        f=font("bold",40); d.text((W/2,y+6),sub,font=f,fill=(230,230,240,255),anchor="ma",stroke_width=3,stroke_fill=(0,0,0,255))
    im.save(path)

def wm_png(path, endcard=False):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    wm=WM.copy(); wm.thumbnail((200,200)); im.alpha_composite(wm,(W-wm.width-40,1250))
    d.text((W/2,H-70),"Fan content · not affiliated with Rockstar Games",font=font("reg",26),fill=(255,255,255,170),anchor="mm")
    im.save(path)

def endcard_png(path,q):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((90,1480,W-90,1700),28,fill=(0,0,0,190),outline=VIO+(255,),width=4)
    d.text((W/2,1530),q,font=font("blk",58),fill=(255,255,255),anchor="ma")
    d.text((W/2,1625),"@levelupplay2026 on YouTube, TikTok & Instagram",font=font("bold",32),fill=BLUE,anchor="ma")
    im.save(path)

def map_png(path):
    # self-drawn schematic map (own drawing, no copy of the in-game map)
    random.seed(7)
    im=Image.new("RGB",(W,H),(14,40,70)); d=ImageDraw.Draw(im)
    def blob(cx,cy,rx,ry,n=26,col=(46,110,70)):
        pts=[(cx+rx*(1+random.uniform(-.15,.15))*math.cos(2*math.pi*i/n),cy+ry*(1+random.uniform(-.15,.15))*math.sin(2*math.pi*i/n)) for i in range(n)]
        d.polygon(pts,fill=col)
    # mainland (north) with swamp, bay, keys
    blob(540,600,620,260)                  # Grassrivers mainland
    blob(330,640,110,70,col=(30,80,120))   # Cottonmouth Lake
    blob(700,560,40,30,col=(30,80,120)); blob(560,700,35,25,col=(30,80,120))
    for x,y,rx in [(220,1230,130),(470,1290,110),(720,1320,120),(930,1260,90)]: blob(x,y,rx,55,col=(56,125,80))  # Keys
    d.text((540,1000),"GAMBIT BAY",font=font("bold",40),fill=(120,170,220),anchor="mm")
    # road
    road=[(60,560),(330,520),(520,470),(760,520),(1020,500)]
    d.line(road,fill=(235,235,235),width=10)
    d.line([(760,520),(800,700)],fill=(235,235,235),width=10)
    def label(x,y,t,c=(255,255,255),sz=34):
        d.text((x,y),t,font=font("bold",sz),fill=c,anchor="mm",stroke_width=4,stroke_fill=(0,0,0))
    d.ellipse((800-14,400-14,800+14,400+14),fill=(255,255,255)); label(800,360,"HAMLET")
    label(330,640,"Cottonmouth Lake",sz=30)
    d.ellipse((470-14,1290-14,470+14,1290+14),fill=(255,200,60)); label(470,1350,"Jason's house (Keys)",c=(255,200,60),sz=30)
    # route arrow: keys -> across bay -> lake road -> on foot
    d.line([(470,1270),(420,1050),(360,760)],fill=(255,200,60),width=8)
    # foot trail dashed
    pts=[(360,740),(450,760),(560,800)]
    for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
        for k in range(0,10,2):
            a=k/10;b=(k+1)/10
            d.line([(x1+(x2-x1)*a,y1+(y2-y1)*a),(x1+(x2-x1)*b,y1+(y2-y1)*b)],fill=(255,255,255),width=7)
    px,py=580,800
    for rr,al in [(120,40),(90,70),(60,120)]:
        ov=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(ov).ellipse((px-rr,py-rr,px+rr,py+rr),fill=VIO+(al,)); im.paste(ov,(0,0),ov)
    d.ellipse((px-34,py-34,px+34,py+34),fill=(255,255,255)); d.ellipse((px-20,py-20,px+20,py+20),fill=VIO)
    label(px+40,py+80,"BIGFOOT",c=(255,220,0),sz=50)
    d.text((W/2,90),"HOW TO GET THERE",font=font("blk",76),fill=(255,220,0),anchor="ma",stroke_width=5,stroke_fill=(0,0,0))
    # steps
    steps=["1  Drive to the swamp road by Cottonmouth Lake",
           "2  Listen for a deep growl",
           "3  L3 + R3 = Focus, follow it on foot",
           "4  Find the wooden effigy on a tree"]
    y=1480
    d.rounded_rectangle((50,y-30,W-50,y+4*78+10),24,fill=(0,0,0,200),outline=BLUE,width=4)
    for t in steps:
        d.text((90,y),t,font=font("bold",38),fill=(255,255,255),anchor="la"); y+=78
    d.text((W/2,1880),"Own schematic map · not to scale · source: gtabase",font=font("reg",26),fill=(200,200,210),anchor="mm")
    im.save(path)

def run(cmd): subprocess.run(cmd,check=True)

# vertical base: 3:4 crop of gameplay over blurred fill
def vfilter(cx="(in_w-810)/2"):
    return (f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.15[bg];"
            f"[b]crop=810:1080:{cx}:0,scale=1080:1440[fg];[bg][fg]overlay=0:240,fps=30[base]")

# ---- Reel 1: Bigfoot ----
overlay_png(f"{OUT}/b_hook.png",[("FIND BIGFOOT",130),("IN GTA 6",100)],sub="He is REAL. Map at the end",color=(255,220,0),first=(255,220,0))
wm_png(f"{OUT}/wm.png"); map_png(f"{OUT}/map.png"); endcard_png(f"{OUT}/b_end.png","Did you find him? 👀".replace(" 👀","?") if False else "Have you met him?")
endcard_png(f"{OUT}/p_end.png","Cop: \"License, please\"")
run(["ffmpeg","-v","error","-y","-ss","50","-t","6.5","-i",f"{SRC}/bigfoot.mp4","-filter_complex",vfilter()+";[base]null[v]","-map","[v]","-an","-c:v","libx264","-preset","veryfast","-crf","19",f"{OUT}/b_clip.mp4"])
run(["ffmpeg","-v","error","-y","-loop","1","-t","5","-i",f"{OUT}/map.png","-vf","zoompan=z='1+0.0003*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p",f"{OUT}/b_map.mp4"])
run(["ffmpeg","-v","error","-y","-i",f"{OUT}/b_clip.mp4","-i",f"{OUT}/b_map.mp4","-i",f"{OUT}/b_hook.png","-i",f"{OUT}/wm.png","-i",f"{OUT}/b_end.png","-i",MUSIC,
     "-filter_complex","[0:v]setsar=1[c];[1:v]setsar=1[m];[c][m]concat=n=2:v=1[v0];[v0][2:v]overlay=enable='lt(t,6.5)'[v1];[v1][3:v]overlay=enable='lt(t,6.5)'[v];[5:a]atrim=0:11.5,afade=t=in:d=0.3,afade=t=out:st=10.9:d=0.6[a]",
     "-map","[v]","-map","[a]","-t","11.5","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",f"{OUT}/bigfoot_reel.mp4"])

# ---- Reel 2: Police ----
overlay_png(f"{OUT}/p_hook.png",[("POV: I FORGOT",104),("MY BLINKER ONCE",88)],sub="Leonida PD has zero chill",color=(255,70,90),first=(255,255,255))
run(["ffmpeg","-v","error","-y","-ss","14","-t","11.2","-i",f"{SRC}/aggressivpolice.mp4","-i",f"{OUT}/p_hook.png","-i",f"{OUT}/wm.png","-i",f"{OUT}/p_end.png","-i",MUSIC,
     "-filter_complex",vfilter("(in_w-810)/2-120")+";[base][1:v]overlay=enable='lt(t,8.2)'[v1];[v1][2:v]overlay[v2];[v2][3:v]overlay=enable='gte(t,8.4)'[v];[4:a]atrim=20:31.2,asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st=10.6:d=0.6[a]",
     "-map","[v]","-map","[a]","-t","11.2","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",f"{OUT}/police_reel.mp4"])
print("ok")
