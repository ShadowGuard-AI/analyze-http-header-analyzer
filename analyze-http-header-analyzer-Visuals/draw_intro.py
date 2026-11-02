#!/usr/bin/env python3
"""analyze-http-header-analyzer intro: border office counter at the pause before the next traveller.
Wooden counter close, maroon ink pad with lid leaning open, brass clip, night blue passport cover edge,
open passport as pure ring and blot texture with NO readable mark, stamp on its side die facing away,
platform and sleeper train dissolving into night behind. No letters, numerals or signs anywhere."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
random.seed(41)
V1 = "--v1" in sys.argv
W, H = 1200, 520
MAROON = (122, 30, 44); NIGHT = (16, 28, 58); CREAM = (242, 232, 205); BRASS = (178, 142, 62)
img = Image.new("RGB", (W, H), (10, 18, 40)); d = ImageDraw.Draw(img, "RGBA")
# background: night sky and platform dissolving into dark
for y in range(0, 300):
    t = y / 300; d.line([(0, y), (W, y)], fill=(int(12 + 8 * t), int(22 + 10 * t), int(48 + 14 * t)))
# roof ironwork above the platform
for x in range(40, W, 130):
    d.line([(x, 26), (x + 60, 96)], fill=(30, 36, 52), width=5); d.line([(x + 60, 96), (x + 120, 26)], fill=(30, 36, 52), width=5)
d.line([(0, 28), (W, 28)], fill=(34, 40, 58), width=6)
# standing train: dark body, carriage windows as plain cream rectangles only
d.rectangle([430, 150, 1180, 268], fill=(22, 30, 52))
d.rectangle([430, 150, 1180, 168], fill=(30, 40, 66))
for i in range(8):
    x = 462 + i * 88
    d.rectangle([x, 188, x + 52, 232], fill=(238, 226, 188))
    d.rectangle([x, 188, x + 52, 232], outline=(120, 108, 74))
d.rectangle([0, 268, W, 292], fill=(26, 28, 36))  # platform edge
# lone signal lamp beyond the last carriage
d.line([(1192, 180), (1192, 268)], fill=(40, 42, 50), width=4)
d.ellipse([1182, 158, 1202, 180], fill=(232, 192, 84)); d.ellipse([1186, 162, 1198, 176], fill=(250, 226, 140))
# wooden counter filling the foreground, warm pool of platform light
d.rectangle([0, 292, W, H], fill=(104, 74, 44))
for ly in range(306, H, 22):
    d.line([(0, ly), (W, ly + 5)], fill=(86, 60, 34), width=3)
for _ in range(500):
    x, y = random.uniform(0, W), random.uniform(292, H); d.point((x, y), fill=random.choice([(126, 94, 56), (92, 64, 38)]))
d.polygon([(0, 292), (760, 292), (520, H), (0, H)], fill=(250, 230, 170, 26))  # light pool thinning toward the train
# open passport midground, oblique: two cream leaves, deep gutter shadow, rings as soft blot texture only
d.polygon([(300, 330), (610, 306), (616, 452), (306, 486)], fill=(238, 229, 200))
d.polygon([(616, 452), (610, 306), (936, 322), (946, 458)], fill=(232, 222, 188))
d.polygon([(600, 306), (626, 306), (630, 454), (604, 454)], fill=(70, 58, 44))  # gutter shadow
rng = random.Random(7)
for leaf in range(2):
    for _ in range(9):
        cx = rng.uniform(360, 560) if leaf == 0 else rng.uniform(680, 890)
        cy = rng.uniform(330, 440); r = rng.uniform(16, 42)
        col = MAROON if rng.random() < .55 else (36, 54, 110)
        if V1:  # draft 1 flaw: hard perfect target rings, far too crisp to count as unreadable texture
            for rr in (r, r * .66, r * .33):
                d.ellipse([cx - rr, cy - rr * .7, cx + rr, cy + rr * .7], outline=col, width=3)
        else:  # shipped: broken, offset, faded arcs and blots only
            for k in range(3):
                a0 = rng.uniform(0, 300); rr = r * (1 - k * .26)
                d.arc([cx - rr, cy - rr * .7, cx + rr, cy + rr * .7], a0, a0 + rng.uniform(120, 240), fill=col + (120,), width=4)
            d.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], fill=col + (90,))
# passport cover in night blue entering from the lower left, curved edge
d.pieslice([-160, 420, 300, 640], 270, 360, fill=(24, 40, 84))
d.arc([-160, 420, 300, 640], 270, 360, fill=(52, 74, 130), width=5)
# round ink pad in sleeper maroon with its lid leaning open, on the counter at right
d.ellipse([966, 356, 1150, 424], fill=(40, 34, 30)); d.ellipse([976, 360, 1140, 416], fill=MAROON)
d.ellipse([992, 368, 1124, 408], fill=(138, 40, 56))
lean = Image.new("RGBA", (190, 90), (0, 0, 0, 0)); ld = ImageDraw.Draw(lean)
ld.ellipse([6, 10, 184, 82], fill=(52, 44, 38, 255), outline=(150, 124, 70, 255))
lean = lean.rotate(24, expand=True); img.paste(lean, (1006, 268), lean); d = ImageDraw.Draw(img, "RGBA")
# brass clip catching the light, beside the pad
d.polygon([(902, 330), (946, 322), (952, 344), (908, 352)], fill=BRASS); d.ellipse([916, 326, 940, 342], outline=(240, 210, 120), width=3)
# underside of the stamp resting on its side, die facing AWAY: wooden back and brass neck only, no face shown
d.ellipse([120, 330, 252, 452], fill=(96, 64, 36)); d.ellipse([138, 348, 234, 434], fill=(116, 80, 46))
d.rectangle([196, 372, 268, 404], fill=BRASS); d.ellipse([252, 362, 282, 414], fill=(150, 116, 54))
img = img.filter(ImageFilter.GaussianBlur(0.9 if not V1 else 0.2))
out = "scratch/intro-v1.png" if V1 else "intro-banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
