# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

FONT = "C:/Windows/Fonts/msyh.ttc"  # Microsoft YaHei

def vertical_gradient(w, h, top=(90,200,250), bottom=(0,95,245)):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img

def rounded_mask(w, h, radius):
    m = Image.new("L", (w * 4, h * 4), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], radius=radius * 4, fill=255)
    return m.resize((w, h), Image.LANCZOS)

def make_icon(size, maskable=False):
    # background: full square for maskable, rounded square otherwise
    if maskable:
        bg = vertical_gradient(size, size)
        radius = 0
    else:
        bg = vertical_gradient(size, size)
        icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        mask = rounded_mask(size, size, int(size * 0.225))
        icon.paste(bg, (0, 0), mask)
        bg = icon

    d = ImageDraw.Draw(bg)
    glyph_size = int(size * (0.52 if maskable else 0.6))
    font = ImageFont.truetype(FONT, glyph_size)
    text = "语"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1] - (size * 0.02 if not maskable else 0)
    # subtle soft shadow
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((x, y + size * 0.015), text, font=font, fill=(0, 40, 120, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.02))
    if maskable:
        bg = bg.convert("RGBA")
    bg = Image.alpha_composite(bg.convert("RGBA"), shadow)
    d = ImageDraw.Draw(bg)
    d.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    return bg.convert("RGBA")

out = "C:/Users/90310/WorkBuddy/2026-08-21-17-58-06/"
for s in (192, 512):
    make_icon(s, False).save(out + f"icon-{s}.png")
    make_icon(s, True).save(out + f"icon-maskable-{s}.png")
# favicon 32 + apple-touch-icon 180 (apple: no transparency)
make_icon(180, False).convert("RGB").save(out + "apple-touch-icon.png")
make_icon(32, False).save(out + "favicon-32.png")
print("done")
