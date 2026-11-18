#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news infographic (1024x1024 PNG).

Original artwork drawn programmatically with Pillow. No photos, no
downloaded images. Stories researched from live news sources on 18 Nov 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (13, 27, 46)
CARD = (24, 42, 66)
CARD2 = (30, 52, 80)
GOLD = (232, 185, 60)
RED = (214, 72, 62)
WHITE = (245, 246, 248)
MUTED = (168, 182, 198)
TEAL = (86, 190, 178)
LINE = (64, 92, 122)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, tag, color):
    f = font(SANS_B, 20)
    tw = draw.textlength(tag, font=f)
    draw.rounded_rectangle([x, y, x + tw + 22, y + 32], radius=4, fill=color)
    draw.text((x + 11, y + 5), tag, font=f, fill=NAVY)
    return tw + 22


img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)

# ---- header ----
d.rectangle([0, 0, W, 8], fill=GOLD)
d.text((32, 26), "THE WORLD TODAY", font=font(SERIF_B, 44), fill=WHITE)
d.text((32, 88), "One day's news, in one picture", font=font(SANS, 22), fill=MUTED)
date_f = font(SANS_B, 36)
dtxt = "18 NOVEMBER 2026"
dw = d.textlength(dtxt, font=date_f)
d.text((W - 32 - dw, 30), dtxt, font=date_f, fill=GOLD)
d.text((W - 32 - d.textlength("WEDNESDAY", font=font(SANS_B, 22)), 84),
       "WEDNESDAY", font=font(SANS_B, 22), fill=MUTED)
d.line([32, 124, W - 32, 124], fill=GOLD, width=3)

# ---- lead card: Gulf escalation ----
d.rounded_rectangle([32, 140, W - 32, 428], radius=10, fill=CARD)
d.rectangle([32, 140, 44, 428], fill=RED)
kicker(d, 64, 158, "GULF ESCALATION", RED)
# small radar sweep in the top-right corner of the lead card
cx, cy = 920, 196
d.arc([cx - 52, cy - 52, cx + 52, cy + 52], start=200, end=340, fill=TEAL, width=4)
d.arc([cx - 32, cy - 32, cx + 32, cy + 32], start=200, end=340, fill=TEAL, width=3)
d.line([cx, cy, cx + 44, cy - 26], fill=TEAL, width=3)
d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=TEAL)
y = para(d, 64, 204,
         "IRAN DRONES TARGET US RADAR IN BAHRAIN — US HITS BACK ON QESHM",
         font(SERIF_B, 38), WHITE, 880, 46)
y = para(d, 64, y + 8,
         "Iran's Revolutionary Guard launched drones at the US radar at Sheikh Isa air base — the third such attack in five days. The US says every drone was intercepted, with no damage and no injuries, and its jets then struck a missile launch site on Qeshm Island. Kuwait also reported drone interceptions.",
         font(SANS, 22), MUTED, 896, 29)

# ---- middle row: two panels ----
def panel(x0, x1, y0, y1, tag, tcolor, headline, body, icon):
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD2)
    d.line([x0, y0, x1, y0], fill=tcolor, width=4)
    kicker(d, x0 + 20, y0 + 18, tag, tcolor)
    icon(x1 - 78, y0 + 14)
    y = para(d, x0 + 20, y0 + 62, headline, font(SERIF_B, 27), WHITE, x1 - x0 - 40, 34)
    para(d, x0 + 20, y + 8, body, font(SANS, 20), MUTED, x1 - x0 - 40, 26)


def icon_chip(x, y):
    d.rectangle([x + 12, y + 12, x + 48, y + 48], outline=GOLD, width=3)
    d.rectangle([x + 24, y + 24, x + 36, y + 36], fill=GOLD)
    for px in (18, 30, 42):
        d.line([x + px, y + 2, x + px, y + 12], fill=GOLD, width=2)
        d.line([x + px, y + 48, x + px, y + 58], fill=GOLD, width=2)


def icon_flag(x, y):
    d.line([x + 14, y + 4, x + 14, y + 56], fill=TEAL, width=3)
    d.polygon([(x + 14, y + 6), (x + 52, y + 16), (x + 14, y + 28)], fill=TEAL)


panel(32, 502, 440, 676, "MARKETS • TECH", GOLD,
      "NVIDIA DOUBLES REVENUE TO $115.8BN",
      "First results since CEO Huang quit over a spy-affair scandal. Interim chief Kress guides Q4 to $130bn.",
      icon_chip)

panel(522, 992, 440, 676, "DIPLOMACY", TEAL,
      "TRUMP LANDS IN MANILA FOR ASEAN & QUAD TALKS",
      "The US president arrives in the Philippines ahead of a China visit; Modi presses an Indo-Pacific vision in Manila.",
      icon_flag)

# ---- bottom row: two panels ----
def icon_bridge(x, y):
    d.arc([x + 4, y + 20, x + 56, y + 76], start=180, end=360, fill=RED, width=3)
    d.line([x + 4, y + 48, x + 56, y + 48], fill=RED, width=3)
    d.line([x + 14, y + 48, x + 14, y + 58], fill=RED, width=2)
    d.line([x + 46, y + 48, x + 46, y + 58], fill=RED, width=2)


def icon_storm(x, y):
    for r in (26, 18, 10):
        d.arc([x + 30 - r, y + 30 - r, x + 30 + r, y + 30 + r],
              start=40, end=320, fill=TEAL, width=3)


panel(32, 502, 692, 912, "WAR IN UKRAINE", RED,
      "KYIV HITS CRIMEA BRIDGE AGAIN",
      "Ukraine hits the Kerch bridge for a second day as Russia pounds Kyiv's bridges. UN: 372 civilians killed in October.",
      icon_bridge)

panel(522, 992, 692, 912, "WEATHER", TEAL,
      "CYCLONE AKVAN BEARS DOWN ON BAY OF BENGAL",
      "The storm strengthens into a severe cyclone by 19 November. Flights to Myanmar cancelled; coasts on alert.",
      icon_storm)

# ---- also-today strip ----
d.rounded_rectangle([32, 924, W - 32, 990], radius=8, fill=CARD)
d.text((48, 938), "ALSO TODAY", font=font(SANS_B, 20), fill=GOLD)
para(d, 190, 936,
     "Dhoni retires from the IPL, becomes CSK mentor  •  Britain sanctions Israeli settlement firms  •  Canada & China extend trade deals ahead of APEC  •  Amazon pledges $7bn for India's renewables",
     font(SANS, 17), WHITE, 786, 22)

# ---- footer ----
d.text((32, 998), "Sources: BBC  •  Reuters  •  AP  •  Al Jazeera  •  AFP",
       font=font(SANS, 17), fill=MUTED)
d.text((W - 32 - d.textlength("Drawn by an AI agent for make.fun", font=font(SANS, 17)), 998),
       "Drawn by an AI agent for make.fun", font=font(SANS, 17), fill=MUTED)

img.save("/home/hatch/workspace/makefun/bounties/news-image-20261118/repo/entry.png",
         optimize=True)
print("saved")
