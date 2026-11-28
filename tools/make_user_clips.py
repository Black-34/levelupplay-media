"""Reels aus Gameplay-Clips des Nutzers (16:9 -> 9:16), deutsche Untertitel weggeschnitten, englische Texte."""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
REPO = "/home/claude/levelupplay-media"; OUT = "/home/claude/work/clips"; UP = "/mnt/user-data/uploads"
FI = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FI + n, s)
RED = (255, 70, 90); YEL = (255, 220, 0); BLUE = (58, 160, 255); VIO = (155, 92, 255); ORA = (255, 120, 40)
FG_Y = 400  # Spielbild 1080x880 bei y=400..1280
def run(c): subprocess.run(c, check=True)
def png(name, draw):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im); draw(d, im); p = f"{OUT}/{name}.png"; im.save(p); return p
def box_text(d, y, t, sz, col, outline=None):
    f = F("Inter-Black.otf", sz); tw = d.textlength(t, font=f)
    d.rounded_rectangle((W/2-tw/2-28, y-14, W/2+tw/2+28, y+sz+22), 22, fill=(0,0,0,215), outline=outline, width=6)
    d.text((W/2, y), t, font=f, fill=col, anchor="ma", stroke_width=3, stroke_fill=(0,0,0))
def hook(name, l1, l2, c2):
    return png(name, lambda d, im: (box_text(d, 90, l1, 96, (255,255,255), c2), box_text(d, 250, l2, 96, c2)))
def wm(d, im):
    w = Image.open(f"{REPO}/assets/brand/watermark.png").convert("RGBA"); w.thumbnail((130, 130)); im.alpha_composite(w, (W-w.width-24, FG_Y+16))
    d.text((W/2, H-60), "Fan content · not affiliated with Rockstar Games", font=F("Inter-Regular.otf", 26), fill=(255,255,255,170), anchor="mm")
def endcard(name, q):
    def dr(d, im):
        d.rounded_rectangle((70, 1500, W-70, 1760), 28, fill=(0,0,0,225), outline=VIO, width=4)
        d.text((W/2, 1550), q, font=F("Inter-Black.otf", 58), fill=(255,255,255), anchor="ma")
        d.text((W/2, 1660), "@levelupplay2026 on YouTube, TikTok & Instagram", font=F("Inter-Bold.otf", 32), fill=BLUE, anchor="ma")
    return png(name, dr)
def label(name, t, col=(255,255,255), sz=56, y=1330):
    def dr(d, im):
        f = F("Inter-Black.otf", sz); lines = t.split("\n")
        hh = len(lines)*(sz+16)
        mw = max(d.textlength(l, font=f) for l in lines)
        d.rounded_rectangle((W/2-mw/2-34, y-18, W/2+mw/2+34, y+hh+14), 22, fill=(0,0,0,230))
        for i, l in enumerate(lines): d.text((W/2, y+i*(sz+16)), l, font=f, fill=col, anchor="ma")
    return png(name, dr)
BASE = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.2[bg];"
        "[b]crop=1080:880:{cx}:0[fg];[bg][fg]overlay=0:%d,fps=30,setsar=1" % FG_Y)
def render(src, segs, overlays, out, cx=420):
    """segs: [(start,end)], overlays: [(png, t0, t1)] auf der Ausgabezeitachse"""
    inputs = []; fc = ""
    for i, (a, b) in enumerate(segs):
        inputs += ["-ss", str(a), "-t", str(b-a), "-i", src]
        fc += f"[{i}:v]" + BASE.format(cx=cx) + f"[v{i}];[{i}:a]aresample=48000,afade=t=in:d=0.08,afade=t=out:st={b-a-0.1:.2f}:d=0.1[a{i}];"
    n = len(segs)
    fc += "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca];"
    last = "cv"
    for j, (p, t0, t1) in enumerate(overlays):
        inputs += ["-i", p]; k = n + j
        fc += f"[{last}][{k}:v]overlay=enable='between(t,{t0},{t1})'[o{j}];"; last = f"o{j}"
    total = sum(b-a for a, b in segs)
    fc += f"[{last}]null[v];[ca]volume=1.3,afade=t=out:st={total-0.6:.2f}:d=0.6[aout]"
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[v]", "-map", "[aout]", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])

if "bagger" in sys.argv:
    src = f"{UP}/lustigbaggerangriff.mp4"; T = 18.4
    ov = [(hook("b_hook", "ROAD RAGE?", "EXCAVATOR EDITION", ORA), 0, 3.6), (png("b_wm", wm), 0, T)]
    subs = [(4.4, 6.1, "\u201cWatch the road, a**hole!\u201d"), (6.4, 7.6, "\u201cMove it already!\u201d"),
            (7.9, 9.1, "\u201cVice City hates you!\u201d"), (9.15, 10.4, "\u201cYo! I'm gonna miss\nmy testosterone shot!\u201d"),
            (14.4, 15.2, "\u201cOkay... can you just die?\u201d")]
    for i, (a, b, t) in enumerate(subs): ov.append((label(f"b_sub{i}", t, YEL if i == 4 else (255,255,255), 54), a, b))
    ov.append((endcard("b_end", "Would you do this?"), 16.0, T))
    render(src, [(0, T)], ov, f"{OUT}/bagger.mp4", cx=460)
if "auto" in sys.argv:
    src = f"{UP}/kapitel2bestesauto.mp4"
    segs = [(42.5, 45.5), (10.6, 13.6), (17.0, 20.0), (30.0, 37.0), (37.0, 46.5), (50.0, 52.4)]
    # Ausgabe-Zeiten: 0-3, 3-6, 6-9, 9-16, 16-25.5, 25.5-27.9
    T = 27.9
    ov = [(hook("a_hook", "BEST CAR", "IN CHAPTER 2?", RED), 0, 3.0), (png("a_wm", wm), 0, T),
          (label("a_s1", "1. Go to Port Gellhorn\n(the pin by the pier)", (255,255,255)), 3.0, 6.0),
          (label("a_s2", "2. Walk into the yard –\nno need to shoot anyone", (255,255,255)), 6.0, 9.0),
          (label("a_s3", "3. Red Vapid Dominator:\nsmash the window, get in", YEL), 9.0, 16.0),
          (label("a_s4", "4. It has NITRO!\nHold the button & go", YEL), 16.0, 22.0),
          (label("a_s5", "No shooting needed –\njust drive off", (255,255,255)), 22.0, 25.5),
          (label("a_s6", "Counts as a suitable car\nfor the Moses job", (255,255,255)), 25.5, T),
          (endcard("a_end", "Would you take this car?"), 23.0, T)]
    render(src, segs, ov, f"{OUT}/auto.mp4", cx=420)
print("ok")
