#!/usr/bin/env python3
"""analyze-http-header-analyzer logo: round border entry stamp from directly above, brass handle rising
out of the top of the frame, inked die face in sleeper maroon filling the lower two thirds: outer ring,
broken inner ring worn by years of pressure, small open grille at the centre with three horizontal
field lines beside it, one segment of the outer ring darker and double struck. Name below in
Bitcount Prop Single Ink, night blue on corridor cream."""
import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V1 = "--v1" in sys.argv
W, H = 900, 560
MAROON = (122, 30, 44); DARKMAROON = (84, 18, 32); NIGHT = (18, 32, 64); CREAM = (242, 232, 205); BRASS = (178, 142, 62)
img = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(img, "RGBA")
cx, cy, R = 450, 268, 168
# brass handle rising out of the top of the frame: neck and knob cropped by the frame edge
d.rectangle([424, 0, 476, 118], fill=BRASS)
for ly in range(8, 112, 18):
    d.line([(428, ly), (472, ly)], fill=(140, 108, 44), width=3)
d.ellipse([398, -58, 502, 42], fill=(196, 158, 74)); d.ellipse([412, -46, 488, 30], fill=(216, 182, 96))
d.rectangle([408, 96, 492, 128], fill=(150, 116, 54))  # collar where handle meets the die
# die face: pale inked disc, outer ring, broken inner ring
d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(236, 226, 196))
d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=MAROON, width=13)
d.ellipse([cx - R + 22, cy - R + 22, cx + R - 22, cy + R - 22], outline=MAROON, width=4)
for a0 in range(0, 360, 57):  # broken inner ring: worn gaps where pressure ate the metal
    d.arc([cx - 118, cy - 118, cx + 118, cy + 118], a0, a0 + 34, fill=MAROON, width=6)
if not V1:
    # one segment darker and slightly double struck, lower right of the outer ring
    d.arc([cx - R, cy - R, cx + R, cy + R], 18, 74, fill=DARKMAROON, width=15)
    d.arc([cx - R + 7, cy - R + 5, cx + R + 7, cy + R + 5], 22, 70, fill=DARKMAROON + (170,), width=9)
# centre: small open grille, the barred clerk window
gx, gy = cx - 58, cy - 34
d.rectangle([gx, gy, gx + 76, gy + 68], outline=MAROON, width=5)
for i in range(4):
    x = gx + 12 + i * 17; d.line([(x, gy + 6), (x, gy + 62)], fill=MAROON, width=4)
d.line([(gx + 4, gy + 34), (gx + 72, gy + 34)], fill=MAROON, width=3)
# three horizontal lines beside the grille: the blank fields a stamp leaves for a date
for i in range(3):
    y = cy - 22 + i * 22; d.line([(cx + 36, y), (cx + 104, y)], fill=MAROON, width=5)
# faint ink wear speckles on the face
import random; random.seed(5)
for _ in range(120):
    x, y = random.uniform(cx - R + 16, cx + R - 16), random.uniform(cy - R + 16, cy + R - 16)
    if (x - cx) ** 2 + (y - cy) ** 2 < (R - 18) ** 2:
        d.point((x, y), fill=(200, 188, 160))
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/BitcountPropSingleInk.ttf", 34)
except Exception:
    f = ImageFont.load_default()
d.text((450, 496), "analyze-http-header-analyzer", font=f, fill=NIGHT, anchor="mm")
img = img.filter(ImageFilter.GaussianBlur(0.3))
out = "scratch/logo-v1.png" if V1 else "logo.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out)
if not V1:
    img.resize((103, 64)).save(__file__.rsplit("/", 1)[0] + "/scratch/logo64-ship.png")
print("saved", out)
