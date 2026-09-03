# -*- coding: utf-8 -*-
"""Build the 1200x630 social share card (og:image / twitter:image)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "images", "og-card.jpg")
PORTRAIT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "images", "尤俊硯大頭貼-24.jpg")

BG      = (22, 25, 29)
BG2     = (31, 37, 44)
INK     = (238, 243, 246)
MUTED   = (150, 165, 176)
ACCENT  = (110, 196, 209)
RULE    = (58, 70, 80)

F = r"C:\Windows\Fonts"
def font(name, size, idx=0):
    p = os.path.join(F, name)
    return ImageFont.truetype(p, size, index=idx)

f_label = font("segoeuib.ttf", 24)
f_zh    = font("msjhbd.ttc", 92)
f_en    = font("segoeuib.ttf", 52)
f_kw    = font("msjh.ttc", 30)
f_url   = font("consola.ttf", 26)

# ── ground: soft diagonal gradient ────────────────────────────────
card = Image.new("RGB", (W, H), BG)
grad = Image.new("RGB", (W, H))
gd = grad.load()
for y in range(H):
    for x in range(0, W, 4):
        t = (x / W * 0.65 + y / H * 0.35)
        c = tuple(int(BG[i] + (BG2[i] - BG[i]) * t) for i in range(3))
        for dx in range(4):
            if x + dx < W:
                gd[x + dx, y] = c
card = grad.filter(ImageFilter.GaussianBlur(2))
d = ImageDraw.Draw(card)

# ── portrait, circular ────────────────────────────────────────────
D = 372
px, py = 96, (H - D) // 2
src = Image.open(PORTRAIT).convert("RGB")
# cover-crop to square, biased to the upper half so the face is not cut off
w, h = src.size
side = min(w, h)
left = (w - side) // 2
top = int((h - side) * 0.18)
src = src.crop((left, top, left + side, top + side)).resize((D, D), Image.LANCZOS)

mask = Image.new("L", (D * 4, D * 4), 0)
ImageDraw.Draw(mask).ellipse((0, 0, D * 4, D * 4), fill=255)
mask = mask.resize((D, D), Image.LANCZOS)

# accent ring behind the portrait
ring = 8
d.ellipse((px - ring, py - ring, px + D + ring, py + D + ring), outline=ACCENT, width=3)
card.paste(src, (px, py), mask)

# ── right column ──────────────────────────────────────────────────
x = px + D + 88
y = 150

d.text((x, y), "ALGORITHM ENGINEER", font=f_label, fill=ACCENT)
y += 52

d.text((x, y), "尤俊硯", font=f_zh, fill=INK)
y += 116

d.text((x, y), "Alex Yu", font=f_en, fill=(196, 210, 219))
y += 84

d.line((x, y, x + 470, y), fill=RULE, width=2)
y += 34

kws = ["生醫訊號", "醫療 AI", "航太工程"]
cx = x
for i, k in enumerate(kws):
    if i:
        d.text((cx, y + 2), "·", font=f_kw, fill=RULE)
        cx += d.textlength("·", font=f_kw) + 18
    d.text((cx, y), k, font=f_kw, fill=MUTED)
    cx += d.textlength(k, font=f_kw) + 18

d.text((x, H - 92), "ycy1997alex.github.io", font=f_url, fill=(112, 128, 139))

card.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
print("%s  %dx%d  %d KB" % (OUT, card.width, card.height, os.path.getsize(OUT) // 1024))
