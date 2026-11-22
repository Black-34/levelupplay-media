import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
OUT = "/home/claude/work/out2"; SRC = "/mnt/user-data/uploads/Levelup/videos/aggressivpolice.mp4"
REPO = "/home/claude/repo"
FI = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FI + n, s)
RED = (255, 70, 90); YEL = (255, 220, 0); BLUE = (58, 160, 255)
def run(c): subprocess.run(c, check=True)
def png(name, draw):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im); draw(d, im); im.save(f"{OUT}/{name}.png")
def box_text(d, y, t, sz, col, outline=None):
    f = F("Inter-Black.otf", sz); tw = d.textlength(t, font=f)
    d.rounded_rectangle((W/2-tw/2-28, y-14, W/2+tw/2+28, y+sz+22), 22, fill=(0,0,0,210), outline=outline, width=6)
    d.text((W/2, y), t, font=f, fill=col, anchor="ma", stroke_width=3, stroke_fill=(0,0,0))

png("p_hook", lambda d, im: (box_text(d, 110, "I HONKED ONCE...", 104, (255,255,255), RED), box_text(d, 280, "COP GOES CRAZY", 110, RED)))
def honk(d, im):
    f = F("Inter-Black.otf", 150)
    d.text((W/2, 820), "HONK!", font=f, fill=YEL, anchor="mm", stroke_width=10, stroke_fill=(0,0,0))
png("honk", honk)
def wm(d, im):
    w = Image.open(f"{REPO}/assets/brand/watermark.png").convert("RGBA"); w.thumbnail((190, 190)); im.alpha_composite(w, (W-w.width-40, 1250))
    d.text((W/2, H-70), "Fan content · not affiliated with Rockstar Games", font=F("Inter-Regular.otf", 26), fill=(255,255,255,170), anchor="mm")
png("p_wm", wm)
def endc(d, im):
    d.rounded_rectangle((90, 1430, W-90, 1690), 28, fill=(0,0,0,220), outline=(155,92,255), width=4)
    d.text((W/2, 1480), "Would you get away?", font=F("Inter-Black.otf", 60), fill=(255,255,255), anchor="ma")
    d.text((W/2, 1590), "@levelupplay2026 on YouTube, TikTok & Instagram", font=F("Inter-Bold.otf", 32), fill=BLUE, anchor="ma")
png("p_end", endc)
# English subtitles covering the German in-game subtitles (they sit around y=1540-1640 in the 9:16 frame)
SUBS = [(3.8, 7.0, "COP: What are you doing?!"),
        (7.8, 9.1, "COP: Hey junkie, knock it off!"),
        (9.1, 10.1, "COP: Unbelievable! So irresponsible!"),
        (10.1, 11.8, "COP: Get out of the vehicle!"),
        (11.8, 13.8, "COP: Hands behind your back! Now!"),
        (13.8, 15.0, "ME: Mm-mm. Nope!")]
for i, (_, _, t) in enumerate(SUBS):
    def sd(d, im, t=t):
        f = F("Inter-Black.otf", 52); tw = d.textlength(t, font=f)
        d.rounded_rectangle((min(60,W/2-tw/2-30), 1350, max(W-60,W/2+tw/2+30), 1650), 20, fill=(0,0,0,235))
        d.text((W/2, 1535), t, font=f, fill=(255,255,255) if t.startswith("COP") else YEL, anchor="mm")
    png(f"sub{i}", sd)

VF = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.15[bg];"
      "[b]crop=810:1080:(in_w-810)/2-120:0,scale=1080:1440[fg];[bg][fg]overlay=0:240,fps=30,setsar=1[base]")
inputs = ["-ss", "14", "-t", "17", "-i", SRC] + sum([["-i", f"{OUT}/{n}.png"] for n in ["p_hook", "honk", "p_wm", "p_end"] + [f"sub{i}" for i in range(len(SUBS))]], [])
fc = "[0:v]" + VF + ";"
fc += "[base][1:v]overlay=enable='lt(t,4)'[x1];"
fc += "[x1][2:v]overlay=enable='between(t,0.9,1.9)+between(t,3.6,4.2)'[x2];"
fc += "[x2][3:v]overlay[x3];"
last = "x3"
for i, (a, b, _) in enumerate(SUBS):
    fc += f"[{last}][{5+i}:v]overlay=enable='between(t,{a},{b})'[s{i}];"; last = f"s{i}"
fc += f"[{last}][4:v]overlay=enable='gte(t,15)'[v];[0:a]volume=1.4,afade=t=out:st=16.4:d=0.6[a]"
run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{OUT}/police_v2.mp4"])
print("ok")
