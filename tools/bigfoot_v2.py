import subprocess, sys
sys.path.insert(0, "/home/claude/scripts")
from PIL import Image, ImageDraw, ImageFilter
import importlib.util
W, H = 1080, 1920
OUT = "/home/claude/work/out2"; SRC = "/mnt/user-data/uploads/Levelup/videos/bigfoot.mp4"
REPO = "/home/claude/repo"; MUSIC = f"{REPO}/audio/levelup_vicecity_synthwave.mp3"
import os; os.makedirs(OUT, exist_ok=True)
FI = "/usr/share/fonts/opentype/inter/"
from PIL import ImageFont
def F(n, s): return ImageFont.truetype(FI + n, s)
YEL = (255, 220, 0); BLUE = (58, 160, 255); VIO = (155, 92, 255)
def run(c): subprocess.run(c, check=True)

def box_text(d, y, t, sz, col, outline=None):
    f = F("Inter-Black.otf", sz); tw = d.textlength(t, font=f)
    d.rounded_rectangle((W/2-tw/2-28, y-14, W/2+tw/2+28, y+sz+22), 22, fill=(0,0,0,210), outline=outline, width=6)
    d.text((W/2, y), t, font=f, fill=col, anchor="ma", stroke_width=3, stroke_fill=(0,0,0))

# overlays
im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
box_text(d, 120, "FIND BIGFOOT", 130, YEL, YEL); box_text(d, 300, "IN GTA 6", 100, YEL)
d.text((W/2, 450), "Follow the growl...", font=F("Inter-Bold.otf", 46), fill=(255,255,255), anchor="ma", stroke_width=4, stroke_fill=(0,0,0))
im.save(f"{OUT}/hook.png")
im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
box_text(d, 120, "FOUND HIM", 130, YEL, YEL)
im.save(f"{OUT}/found.png")
im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
wm = Image.open(f"{REPO}/assets/brand/watermark.png").convert("RGBA"); wm.thumbnail((190, 190)); im.alpha_composite(wm, (W-wm.width-40, 1250))
d.text((W/2, H-70), "Fan content · not affiliated with Rockstar Games", font=F("Inter-Regular.otf", 26), fill=(255,255,255,170), anchor="mm")
im.save(f"{OUT}/wm.png")

# map card from the user's map: crop removes the Portuguese menu texts, English labels added
m = Image.open("/mnt/user-data/uploads/Levelup/fotos/GTA-6-Bigfoot-Location-1536x864.webp").convert("RGB")
crop = m.crop((330, 78, 1230, 864))          # no top menu bar, no side menu, no button hints
cw = W; ch = int(crop.height * W / crop.width)
crop = crop.resize((cw, ch), Image.LANCZOS)
bg = m.resize((int(m.width*H/m.height), H)).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(30))
card = bg.copy(); d = ImageDraw.Draw(card, "RGBA"); d.rectangle((0, 0, W, H), fill=(0, 0, 0, 120))
top = 560; card.paste(crop, (0, top))
d = ImageDraw.Draw(card, "RGBA")
px, py = int((767-330)*W/900), top + int((430-78)*W/900)
for r in (95, 80): d.ellipse((px-r, py-r, px+r, py+r), outline=YEL, width=8)
d.text((px, py+140), "BIGFOOT HERE", font=F("Inter-Black.otf", 52), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=(0,0,0))
cx, cy = int((751-330)*W/900), top + int((352-78)*W/900)
d.text((cx+60, cy-10), "park car", font=F("Inter-Bold.otf", 36), fill=(255,255,255), anchor="lm", stroke_width=4, stroke_fill=(0,0,0))
box_text(d, 100, "HOW TO GET THERE", 82, YEL, YEL)
d.text((W/2, 250), "Grassrivers swamp · south Leonida", font=F("Inter-Bold.otf", 44), fill=(255,255,255), anchor="ma", stroke_width=4, stroke_fill=(0,0,0))
d.text((W/2, 320), "Cottonmouth Lake road, south of Hamlet", font=F("Inter-Bold.otf", 38), fill=(220,230,255), anchor="ma", stroke_width=4, stroke_fill=(0,0,0))
y = top + ch + 50
for t in ["1  Park at the end of the dirt road", "2  Listen for the growl, L3 + R3 = Focus", "3  Follow on foot through the water"]:
    d.text((70, y), t, font=F("Inter-Bold.otf", 42), fill=(255,255,255), anchor="la", stroke_width=4, stroke_fill=(0,0,0)); y += 70
d.text((W/2, 1790), "@levelupplay2026 on YouTube, TikTok & Instagram", font=F("Inter-Bold.otf", 34), fill=BLUE, anchor="ma", stroke_width=3, stroke_fill=(0,0,0))
card.save(f"{OUT}/map.jpg", quality=95)

VF = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.15[bg];"
      "[b]crop=810:1080:(in_w-810)/2:0,scale=1080:1440[fg];[bg][fg]overlay=0:240,fps=30")
def seg(name, ss, t, speed, keep_audio):
    vf = f"setpts=PTS/{speed},{VF}"
    af = f"atempo={speed}" if speed != 1 else "anull"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(t), "-i", SRC]
    if keep_audio:
        cmd += ["-vf", vf, "-af", af + ",aresample=44100", "-ac", "2"]
    else:
        cmd += ["-f", "lavfi", "-t", str(t/speed), "-i", "anullsrc=r=44100:cl=stereo", "-vf", vf, "-map", "0:v", "-map", "1:a"]
    run(cmd + ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", f"{OUT}/{name}.mp4"])
seg("b", 19, 5.6, 2, True)       # chase through the water (2x)
seg("c", 40.5, 7.5, 2.5, True)     # closing in (2.5x)
seg("d", 49.8, 3.2, 1, True)   # Bigfoot reveal
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", "3", "-i", f"{OUT}/map.jpg", "-f", "lavfi", "-t", "3", "-i", "anullsrc=r=44100:cl=stereo",
     "-vf", "zoompan=z='1+0.0004*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=96:s=1080x1920:fps=30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", f"{OUT}/e.mp4"])
# durations: a1.5 b3 c3.2 d3.4 e3.2 = 14.3 -> trim c to keep <=12
run(["ffmpeg", "-v", "error", "-y"] + sum([["-i", f"{OUT}/{x}.mp4"] for x in "bcde"], []) + ["-i", f"{OUT}/hook.png", "-i", f"{OUT}/found.png", "-i", f"{OUT}/wm.png", "-i", MUSIC,
     "-filter_complex",
     "[0:v]setsar=1[s0];[1:v]setsar=1[s1];[2:v]setsar=1[s2];[3:v]setsar=1[s3];[s0][0:a][s1][1:a][s2][2:a][s3][3:a]concat=n=4:v=1:a=1[v0][ga];"
     "[v0][4:v]overlay=enable='lt(t,5.8)'[v1];[v1][5:v]overlay=enable='between(t,5.8,9)'[v2];[v2][6:v]overlay=enable='lt(t,9)'[v];"
     "[ga]volume=1.6[g];[7:a]atrim=0:12,volume=0.45[mu];[g][mu]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=11.4:d=0.6[a]",
     "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{OUT}/bigfoot_v2.mp4"])
print("ok")
