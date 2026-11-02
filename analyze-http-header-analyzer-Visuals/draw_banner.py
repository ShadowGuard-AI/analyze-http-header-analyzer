#!/usr/bin/env python3
"""analyze-http-header-analyzer wordmark banner: night at a land border crossed by rail. Sleeper train at a
floodlit platform in the middle distance, open passport dominating the left foreground on the border office
counter beside the round stamp, pages crowded with maroon and night blue entry marks at angles, brass clip
holding a folded timetable slip, one fresh blank page, departure board behind the counter carrying the single
line analyze-http-header-analyzer in Bitcount Prop Single Ink and no other legible words anywhere."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(43)
V1 = "--v1" in sys.argv
W, H = 1200, 420
MAROON = (122, 30, 44); NIGHT = (16, 28, 58); CREAM = (242, 232, 205); BRASS = (178, 142, 62)
img = Image.new("RGB", (W, H), (9, 16, 38)); d = ImageDraw.Draw(img, "RGBA")
# deep night blue sky, dark country beyond the train
for y in range(0, 130):
    t = y / 130; d.line([(0, y), (W, y)], fill=(int(8 + 6 * t), int(14 + 8 * t), int(36 + 10 * t)))
d.polygon([(0, 128), (300, 96), (620, 122), (900, 100), (1200, 124), (1200, 150), (0, 150)], fill=(12, 20, 34))
# sleeper train at the floodlit platform, middle distance right
d.rectangle([560, 138, 1196, 238], fill=(24, 34, 58))
d.rectangle([560, 138, 1196, 154], fill=(34, 46, 74))
for i in range(7):
    x = 586 + i * 86
    d.rectangle([x, 168, x + 50, 208], fill=(240, 228, 190)); d.rectangle([x, 168, x + 50, 208], outline=(124, 110, 76))
d.rectangle([0, 238, W, 256], fill=(30, 30, 38))
for px in (600, 800, 1000):  # platform floodlight pools
    d.polygon([(px, 60), (px + 26, 60), (px + 90, 250), (px - 40, 250)], fill=(250, 236, 180, 22))
    d.ellipse([px + 4, 48, px + 24, 64], fill=(250, 232, 160))
# single distant signal lamp in brass yellow
d.line([(1188, 96), (1188, 140)], fill=(44, 44, 52), width=3)
d.ellipse([1180, 78, 1196, 96], fill=(236, 196, 88))
# departure board behind the counter, upper middle: one line only
try:
    fb = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/BitcountPropSingleInk.ttf", 30)
    fs = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/BitcountPropSingleInk.ttf", 34)
except Exception:
    fb = fs = ImageFont.load_default()
if V1:  # draft 1 flaw: title hung as a straight station sign over the train, signage not a board line
    d.rectangle([330, 18, 880, 62], fill=(20, 26, 44)); d.text((605, 40), "analyze-http-header-analyzer", font=fs, fill=CREAM, anchor="mm")
else:
    d.rectangle([612, 66, 1128, 116], fill=(14, 20, 38)); d.rectangle([612, 66, 1128, 116], outline=BRASS, width=3)
    d.text((870, 91), "analyze-http-header-analyzer", font=fb, fill=(240, 230, 196), anchor="mm")
# border office counter across the foreground
d.rectangle([0, 256, W, H], fill=(106, 76, 44))
for ly in range(270, H, 20):
    d.line([(0, ly), (W, ly + 4)], fill=(88, 62, 34), width=3)
# open passport dominating the left half: crowded entry marks at angles, blank page waiting on the right
d.polygon([(36, 282), (330, 262), (336, 396), (40, 414)], fill=(238, 229, 200))
d.polygon([(336, 396), (330, 262), (560, 276), (566, 402)], fill=(234, 225, 192))
d.polygon([(322, 262), (346, 262), (350, 398), (326, 398)], fill=(72, 60, 44))
rng = random.Random(11)
for _ in range(10):  # entry marks: rings and blots at different angles, one overlapping another
    cx, cy = rng.uniform(90, 290), rng.uniform(292, 380); r = rng.uniform(15, 34)
    col = MAROON if rng.random() < .6 else (34, 52, 108)
    for rr in (r, r * .62):
        d.ellipse([cx - rr, cy - rr * .72, cx + rr, cy + rr * .72], outline=col, width=3)
    d.line([(cx - r * .5, cy), (cx + r * .5, cy)], fill=col, width=2)
# folded timetable slip held by a brass paper clip on the left leaf
d.polygon([(196, 300), (286, 292), (292, 344), (202, 352)], fill=(226, 218, 186))
for i in range(3):
    d.line([(208, 308 + i * 12), (278, 302 + i * 12)], fill=(150, 142, 118), width=2)
d.polygon([(232, 282), (262, 280), (264, 302), (234, 304)], fill=BRASS); d.ellipse([238, 284, 258, 298], outline=(244, 214, 124), width=3)
# round stamp that has just left the passport, standing on the counter beside it
d.ellipse([592, 300, 724, 402], fill=(236, 226, 196)); d.ellipse([592, 300, 724, 402], outline=MAROON, width=9)
d.arc([606, 314, 710, 388], 0, 300, fill=MAROON, width=4)
d.rectangle([636, 316, 680, 356], outline=MAROON, width=4)
for i in range(3):
    x = 646 + i * 9; d.line([(x, 320), (x, 352)], fill=MAROON, width=3)
d.rectangle([640, 262, 676, 304], fill=BRASS); d.ellipse([628, 232, 688, 268], fill=(198, 160, 76))
# clerk hand at the edge of the counter, out of focus, holding nothing: soft sleeve and relaxed fingers
hand = Image.new("RGBA", (240, 110), (0, 0, 0, 0)); hd = ImageDraw.Draw(hand)
hd.ellipse([10, 26, 150, 84], fill=(214, 178, 144, 255))
for i in range(4):
    hd.ellipse([128 + i * 22, 34 + (i % 2) * 10, 168 + i * 22, 58 + (i % 2) * 10], fill=(214, 178, 144, 255))
hd.rectangle([0, 18, 44, 92], fill=(30, 40, 72, 255))
hand = hand.filter(ImageFilter.GaussianBlur(5)); img.paste(hand, (952, 300), hand); d = ImageDraw.Draw(img, "RGBA")
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = "scratch/banner-v1.png" if V1 else "banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
