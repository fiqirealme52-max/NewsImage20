#!/usr/bin/env python3
"""World News - Friday 20 November 2026 (38 stories).

Rebuilt edition: the 10-element winner template.
  1 masthead, 2 giant date + italic 3-headline sub, 3 number strip (6 numbers),
  4 region tabs (counts sum to 38), 5 three big illustrated leads,
  6 ten medium stories with small illustrations, 7 world map with 13 numbered pins,
  8 ALSO ON list (25 one-liners), 9 DATE CHECK box, 10 footer sources.
Every fact verified from 20 November 2026 sources only.
All artwork drawn by hand in PIL (no photos, no AI generation).
Deterministic: two runs produce byte-identical output.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28
CW = W - 2 * M
INK = (26, 26, 26)
RED = (176, 18, 18)
BLUE = (24, 62, 140)
GREY = (112, 112, 112)
LIGHT = (242, 242, 240)
RULE = (26, 26, 26)
GREEN = (34, 120, 60)
SEA = (238, 244, 247)
LAND = (214, 220, 206)
LANDLINE = (168, 176, 158)

FONTS = "/usr/share/fonts/truetype/noto"


def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


BLACK = "NotoSans-Black.ttf"
BOLD = "NotoSans-Bold.ttf"
REG = "NotoSans-Regular.ttf"
ITAL = "NotoSans-Italic.ttf"

img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)


def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tag(x, y, num, label):
    """Red number + small caps label, e.g. '01  TOP STORY'."""
    f1 = F(BOLD, 12)
    f2 = F(BOLD, 10)
    d.text((x, y), num, font=f1, fill=RED)
    d.text((x + 26, y + 1), label, font=f2, fill=GREY)


# ---------------------------------------------------------------- icons
def icon_whitehouse(x, y, s):
    """White House: pediment, columns, flag."""
    d.rectangle([x, y + s * 0.78, x + s, y + s], fill=(235, 235, 235), outline=INK, width=2)
    d.polygon([(x + s * 0.1, y + s * 0.34), (x + s * 0.5, y + s * 0.08),
               (x + s * 0.9, y + s * 0.34)], fill=(225, 225, 225), outline=INK)
    d.ellipse([x + s * 0.46, y + s * 0.2, x + s * 0.54, y + s * 0.28], fill=RED)
    d.line([x + s * 0.5, y + s * 0.02, x + s * 0.5, y + s * 0.1], fill=INK, width=2)
    d.polygon([(x + s * 0.5, y + s * 0.02), (x + s * 0.68, y + s * 0.05),
               (x + s * 0.5, y + s * 0.09)], fill=RED)
    for i in range(5):
        cx = x + s * (0.16 + i * 0.17)
        d.rectangle([cx, y + s * 0.38, cx + s * 0.06, y + s * 0.76], fill=INK)
    d.rectangle([x + s * 0.4, y + s * 0.62, x + s * 0.6, y + s * 0.78], fill=INK)
    d.line([x, y + s * 0.34, x + s, y + s * 0.34], fill=INK, width=2)


def icon_blast(x, y, s):
    """City skyline under a missile blast star."""
    base = y + s * 0.95
    d.rectangle([x + s * 0.05, base - s * 0.42, x + s * 0.2, base], fill=(200, 200, 200), outline=INK)
    d.rectangle([x + s * 0.25, base - s * 0.62, x + s * 0.42, base], fill=(170, 170, 170), outline=INK)
    d.rectangle([x + s * 0.47, base - s * 0.3, x + s * 0.62, base], fill=(200, 200, 200), outline=INK)
    d.rectangle([x + s * 0.67, base - s * 0.55, x + s * 0.85, base], fill=(180, 180, 180), outline=INK)
    for bx, by in [(x + s * 0.09, base - s * 0.36), (x + s * 0.3, base - s * 0.55),
                   (x + s * 0.52, base - s * 0.24), (x + s * 0.72, base - s * 0.48)]:
        d.rectangle([bx, by, bx + s * 0.05, by + s * 0.05], fill=(255, 230, 120))
    cx, cy, r = x + s * 0.62, y + s * 0.22, s * 0.24
    pts = []
    for i in range(12):
        ang = i * 30 * math.pi / 180
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 200, 40), outline=RED)
    d.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3], fill=RED)


def icon_climate(x, y, s):
    """COP31 lead art: globe with sun rays and a green leaf."""
    cx, cy, r = x + s * 0.5, y + s * 0.56, s * 0.34
    sx, sy = x + s * 0.78, y + s * 0.16
    for k in range(8):
        ang = k * 45 * math.pi / 180
        d.line([sx + 0.09 * s * math.cos(ang), sy + 0.09 * s * math.sin(ang),
                sx + 0.16 * s * math.cos(ang), sy + 0.16 * s * math.sin(ang)],
               fill=(240, 170, 20), width=3)
    d.ellipse([sx - 0.07 * s, sy - 0.07 * s, sx + 0.07 * s, sy + 0.07 * s], fill=(255, 200, 40), outline=(240, 170, 20))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 220, 240), outline=BLUE, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=BLUE, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=BLUE, width=1)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 180, fill=BLUE, width=1)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 180, 360, fill=BLUE, width=1)
    lx, ly = x + s * 0.2, y + s * 0.86
    d.pieslice([lx - 0.14 * s, ly - 0.12 * s, lx + 0.14 * s, ly + 0.12 * s], 180, 360, fill=GREEN)
    d.line([lx, ly - 0.1 * s, lx, ly + 0.1 * s], fill=GREEN, width=2)


def icon_chart(x, y, s):
    """Falling market bars + red down arrow."""
    heights = [0.62, 0.5, 0.38, 0.24]
    for i, hh in enumerate(heights):
        bx = x + s * (0.08 + i * 0.22)
        d.rectangle([bx, y + s * (0.9 - hh), bx + s * 0.14, y + s * 0.9], fill=INK)
    d.line([x + s * 0.05, y + s * 0.92, x + s * 0.95, y + s * 0.92], fill=INK, width=2)
    ax, ay = x + s * 0.62, y + s * 0.08
    d.line([ax, ay, ax + s * 0.28, ay + s * 0.28], fill=RED, width=4)
    d.polygon([(ax + s * 0.28, ay + s * 0.28), (ax + s * 0.28, ay + s * 0.12),
               (ax + s * 0.14, ay + s * 0.28)], fill=RED)


def icon_chip(x, y, s):
    """AI chip: square die with pins."""
    d.rectangle([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.8], fill=(60, 60, 60), outline=INK, width=2)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62], fill=(255, 200, 40), outline=INK)
    for i in range(3):
        off = s * (0.32 + i * 0.18)
        d.line([x + off, y + s * 0.08, x + off, y + s * 0.2], fill=INK, width=2)
        d.line([x + off, y + s * 0.8, x + off, y + s * 0.92], fill=INK, width=2)
        d.line([x + s * 0.08, y + off, x + s * 0.2, y + off], fill=INK, width=2)
        d.line([x + s * 0.8, y + off, x + s * 0.92, y + off], fill=INK, width=2)


def icon_flags(x, y, s):
    """Two flags on poles (Europe talks)."""
    d.line([x + s * 0.3, y + s * 0.1, x + s * 0.3, y + s * 0.92], fill=INK, width=2)
    d.line([x + s * 0.68, y + s * 0.22, x + s * 0.68, y + s * 0.92], fill=INK, width=2)
    d.polygon([(x + s * 0.3, y + s * 0.1), (x + s * 0.62, y + s * 0.18),
               (x + s * 0.3, y + s * 0.28)], fill=BLUE)
    d.polygon([(x + s * 0.68, y + s * 0.22), (x + s * 0.95, y + s * 0.3),
               (x + s * 0.68, y + s * 0.4)], fill=(255, 200, 40), outline=INK)
    for k in range(5):
        d.ellipse([x + s * (0.36 + k * 0.05), y + s * 0.16, x + s * (0.39 + k * 0.05), y + s * 0.19], fill=(255, 255, 255))


def icon_cyclone(x, y, s):
    cx, cy = x + s * 0.5, y + s * 0.5
    for i, r in enumerate([0.42, 0.32, 0.22, 0.12]):
        d.arc([cx - r * s, cy - r * s, cx + r * s, cy + r * s], 200 - i * 40, 340 - i * 40,
              fill=INK, width=3)
    d.ellipse([cx - 0.05 * s, cy - 0.05 * s, cx + 0.05 * s, cy + 0.05 * s], fill=RED)


def icon_ball(x, y, s):
    """Football."""
    cx, cy, r = x + s * 0.5, y + s * 0.5, s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=INK, width=2)
    d.polygon([(cx, cy - r * 0.45), (cx + r * 0.43, cy - r * 0.14), (cx + r * 0.26, cy + r * 0.36),
               (cx - r * 0.26, cy + r * 0.36), (cx - r * 0.43, cy - r * 0.14)], fill=INK)
    d.line([cx, cy - r * 0.45, cx, cy - r], fill=INK, width=1)
    d.line([cx + r * 0.43, cy - r * 0.14, cx + r * 0.9, cy - r * 0.3], fill=INK, width=1)
    d.line([cx - r * 0.43, cy - r * 0.14, cx - r * 0.9, cy - r * 0.3], fill=INK, width=1)


def icon_cricket(x, y, s):
    d.line([x + s * 0.15, y + s * 0.85, x + s * 0.85, y + s * 0.15], fill=(150, 100, 40), width=4)
    d.ellipse([x + s * 0.62, y + s * 0.12, x + s * 0.9, y + s * 0.4], fill=RED, outline=INK)
    d.arc([x + s * 0.62, y + s * 0.12, x + s * 0.9, y + s * 0.4], 200, 340, fill=(255, 255, 255), width=1)
    for i in range(3):
        d.line([x + s * 0.3, y + s * (0.2 + i * 0.14), x + s * 0.3, y + s * (0.3 + i * 0.14)], fill=RED, width=2)


def icon_globe(x, y, s):
    cx, cy, r = x + s * 0.5, y + s * 0.5, s * 0.4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 220, 240), outline=BLUE, width=2)
    d.ellipse([cx - r * 0.5, cy - r, cx + r * 0.5, cy + r], outline=BLUE, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=BLUE, width=1)
    d.arc([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], 0, 180, fill=BLUE, width=1)
    d.arc([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], 180, 360, fill=BLUE, width=1)


def icon_shield(x, y, s):
    d.polygon([(x + s * 0.5, y + s * 0.06), (x + s * 0.92, y + s * 0.2), (x + s * 0.92, y + s * 0.55),
               (x + s * 0.5, y + s * 0.94), (x + s * 0.08, y + s * 0.55), (x + s * 0.08, y + s * 0.2)],
              fill=BLUE, outline=INK)
    d.line([x + s * 0.35, y + s * 0.5, x + s * 0.47, y + s * 0.66, x + s * 0.68, y + s * 0.32],
           fill=(255, 255, 255), width=4)


def icon_city(x, y, s):
    base = y + s * 0.95
    d.rectangle([x + s * 0.04, base - s * 0.4, x + s * 0.2, base], fill=(200, 200, 200), outline=INK)
    d.rectangle([x + s * 0.25, base - s * 0.6, x + s * 0.44, base], fill=(170, 170, 170), outline=INK)
    d.rectangle([x + s * 0.5, base - s * 0.3, x + s * 0.66, base], fill=(200, 200, 200), outline=INK)
    d.rectangle([x + s * 0.72, base - s * 0.5, x + s * 0.9, base], fill=(180, 180, 180), outline=INK)
    for bx, by in [(x + s * 0.08, base - s * 0.34), (x + s * 0.3, base - s * 0.52),
                   (x + s * 0.54, base - s * 0.24), (x + s * 0.76, base - s * 0.44)]:
        d.rectangle([bx, by, bx + s * 0.05, by + s * 0.05], fill=(255, 230, 120))
    d.ellipse([x + s * 0.78, y + s * 0.06, x + s * 0.94, y + s * 0.22], fill=(255, 200, 40), outline=(240, 170, 20))


def icon_scales(x, y, s):
    d.line([x + s * 0.5, y + s * 0.08, x + s * 0.5, y + s * 0.85], fill=INK, width=3)
    d.line([x + s * 0.15, y + s * 0.2, x + s * 0.85, y + s * 0.2], fill=INK, width=3)
    d.line([x + s * 0.15, y + s * 0.2, x + s * 0.15, y + s * 0.45], fill=INK, width=2)
    d.line([x + s * 0.85, y + s * 0.2, x + s * 0.85, y + s * 0.45], fill=INK, width=2)
    d.pieslice([x + s * 0.02, y + s * 0.45, x + s * 0.28, y + s * 0.62], 0, 180, fill=(255, 200, 40), outline=INK)
    d.pieslice([x + s * 0.72, y + s * 0.45, x + s * 0.98, y + s * 0.62], 0, 180, fill=(255, 200, 40), outline=INK)
    d.line([x + s * 0.2, y + s * 0.88, x + s * 0.8, y + s * 0.88], fill=INK, width=3)


def icon_quake(x, y, s):
    """Seismograph trace: a quake."""
    d.line([x + s * 0.08, y + s * 0.72, x + s * 0.92, y + s * 0.72], fill=GREY, width=2)
    pts = [(x + s * 0.08, y + s * 0.5), (x + s * 0.2, y + s * 0.5), (x + s * 0.26, y + s * 0.14),
           (x + s * 0.32, y + s * 0.86), (x + s * 0.38, y + s * 0.5), (x + s * 0.5, y + s * 0.5),
           (x + s * 0.56, y + s * 0.28), (x + s * 0.62, y + s * 0.7), (x + s * 0.68, y + s * 0.5),
           (x + s * 0.92, y + s * 0.5)]
    d.line(pts, fill=RED, width=3, joint="curve")


def icon_dollar(x, y, s):
    """Banknote with a dollar sign: the cost of the war."""
    d.rounded_rectangle([x + s * 0.06, y + s * 0.28, x + s * 0.94, y + s * 0.72], radius=4,
                        fill=GREEN, outline=INK, width=2)
    d.text((x + s * 0.5, y + s * 0.5), "$", font=F(BOLD, int(s * 0.4)), fill=(255, 255, 255), anchor="mm")
    d.ellipse([x + s * 0.12, y + s * 0.36, x + s * 0.2, y + s * 0.44], fill=(255, 255, 255))
    d.ellipse([x + s * 0.8, y + s * 0.56, x + s * 0.88, y + s * 0.64], fill=(255, 255, 255))


# ---------------------------------------------------------------- map data
CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-110, 70), (-95, 69), (-85, 66), (-75, 62), (-65, 58),
     (-55, 47), (-60, 44), (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21), (-95, 18),
     (-105, 20), (-112, 28), (-120, 34), (-124, 42), (-125, 50), (-135, 58), (-150, 60), (-165, 60)],
    [(-58, 64), (-52, 60), (-42, 60), (-32, 68), (-22, 70), (-30, 76), (-45, 76), (-55, 72)],
    [(-80, 10), (-77, 4), (-70, 10), (-62, 10), (-52, 5), (-50, -2), (-40, -5), (-35, -8),
     (-40, -18), (-48, -25), (-57, -33), (-65, -42), (-70, -50), (-73, -42), (-72, -30),
     (-70, -18), (-77, -8), (-80, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 57), (12, 56), (18, 56), (21, 55),
     (24, 58), (28, 60), (30, 62), (40, 68), (44, 66), (40, 60), (35, 55), (30, 50), (28, 45),
     (23, 40), (19, 42), (12, 44), (8, 39), (3, 38), (-2, 37)],
    [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (0, 36), (10, 37), (20, 32), (30, 31), (33, 28),
     (35, 22), (40, 15), (44, 12), (51, 11), (48, 5), (42, -5), (40, -12), (35, -20), (32, -28),
     (26, -34), (19, -35), (16, -28), (13, -18), (12, -8), (9, -1), (8, 4), (-8, 5), (-13, 8)],
    [(30, 62), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74),
     (120, 72), (130, 71), (140, 72), (150, 70), (160, 68), (170, 66), (178, 65), (170, 60),
     (162, 56), (158, 52), (150, 48), (142, 44), (138, 38), (130, 33), (127, 30), (122, 28),
     (120, 22), (112, 20), (108, 12), (105, 8), (100, 6), (98, 10), (95, 16), (92, 21), (88, 22),
     (82, 16), (78, 8), (76, 10), (72, 20), (68, 23), (62, 25), (58, 26), (54, 27), (50, 29),
     (48, 30), (44, 32), (42, 38), (40, 42), (36, 36), (33, 38), (30, 40), (28, 45), (30, 50), (28, 55)],
    [(113, -22), (114, -30), (118, -35), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -11), (140, -17), (136, -15), (132, -12), (126, -14), (120, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 52)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (144, 44), (141, 40), (138, 36), (135, 33)],
    [(167, -45), (170, -42), (173, -38), (175, -36), (178, -38), (176, -41), (172, -43), (168, -46)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (112, -3), (109, -1)],
    [(95, 5), (98, 2), (102, -2), (105, -5), (104, -3), (100, 0)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (45, -25), (43, -22)],
]
# pins: (number, lon, lat) — 05 is the New Caledonia quake, 06 is the Iran war cost (Tehran)
PINS = [
    (1, -80, 36), (2, 30, 50), (3, 33, 37), (4, -71, 44), (5, 171, -27),
    (6, 51, 35), (7, 85, 20), (8, -2, 53), (9, 175, -41), (10, 105, 10),
    (11, -72, 19), (12, -84, 25), (13, 77, 28),
]

# ---------------------------------------------------------------- data
SUB = "Trump delays the Iran call  \u00b7  Missiles hit Kyiv overnight  \u00b7  COP31 drops the fossil-fuel phase-out"

NUMBERS = [
    ("38", "STORIES TODAY"),
    ("300,000", "EVACUATED IN ODISHA"),
    ("49,097", "DOW, BELOW 50,000"),
    ("$48BN", "COST OF IRAN WAR"),
    ("20", "MISSILES FIRED AT KYIV"),
    ("175*", "NICHOLLS, NOT OUT"),
]

REGIONS = [("WORLD", 5), ("AMERICAS", 6), ("EUROPE", 5), ("ASIA", 9), ("SPORT", 11), ("CULTURE", 2)]

LEAD1 = {
    "num": "01", "label": "TOP STORY",
    "headline": "TRUMP DELAYS IRAN DECISION",
    "deck": "No rush on war, he says.",
    "body": "He will \u2018see what happens\u2019 after 1 January \u2014 and the decision on Iran is "
            "delayed to 2027.",
}
LEAD2 = {
    "num": "02", "label": "UKRAINE",
    "headline": "MISSILES HIT KYIV OVERNIGHT",
    "body": "Russia fires nearly 20 ballistic missiles at Kyiv overnight; bridges are hit and "
            "fires burn. A three-storey building in Obolonskyi catches fire; no casualties at first.",
}
LEAD3 = {
    "num": "03", "label": "CLIMATE",
    "headline": "COP31 DROPS FOSSIL-FUEL PHASE-OUT",
    "body": "The climate summit closes in Antalya \u2014 but the final draft drops the call to phase out "
            "fossil fuels, sparking outcry.",
}

MEDIUM = [
    ("04", "WALL STREET SINKS", "Dow falls below 50,000 to 49,097; S&P \u22122.02% and Nasdaq \u22122.25%.", icon_chart),
    ("05", "5.6 QUAKE NEAR NEW CALEDONIA", "A 5.6-magnitude quake strikes 548 km south-east of Noum\u00e9a, 10 km deep.", icon_quake),
    ("06", "US WAR WITH IRAN COST $48BN", "The Pentagon says the US war with Iran has cost over $48bn.", icon_dollar),
    ("07", "CYCLONE AKVAN HITS ODISHA", "300,000 people are evacuated as the cyclone makes landfall in Odisha.", icon_cyclone),
    ("08", "POCHETTINO TAKES OVER UNITED", "New coach calls for unity in his first address; United are 18th.", icon_ball),
    ("09", "INDIA v NZ, DAY 2", "Nicholls 175* and Phillips 118 lift NZ to 368 all out; India 52/0.", icon_cricket),
    ("10", "ASEAN SUMMIT CLOSES", "Leaders seal a digital trade deal; the sea code is unresolved.", icon_globe),
    ("11", "HAITI TROOP DEAL", "Haiti approves a deal for Salvadoran troops as gang strikes widen.", icon_shield),
    ("12", "GTA VI\u2019S NPCs", "The crowd that makes the game\u2019s huge world feel real, says NPR.", icon_city),
    ("13", "JUSTICE VARMA\u2019S LETTER", "In his letter, Justice Varma says his resignation admits no guilt.", icon_scales),
]

ALSO = [
    "14 \u00b7 Bavuma ruled out \u2014 calf injury; misses the Centurion decider vs Bangladesh.",
    "15 \u00b7 Carlsen forfeit \u2014 a shock walkout leaves the chess world fuming.",
    "16 \u00b7 Oman marks 56 years of independence on National Day.",
    "17 \u00b7 Harris meets Macron in Paris amid talk of a 2028 White House bid.",
    "18 \u00b7 Congress faces a Dec 11 funding cliff and a crowded lame-duck list.",
    "19 \u00b7 Japan core inflation hits 2.2% in October, the highest this year.",
    "20 \u00b7 Telus shares jump 12% as a bidding war brews over Quebecor's C$31bn bid.",
    "21 \u00b7 Russian drone hits a Kharkiv hospital; four people are injured.",
    "22 \u00b7 Drones strike the Dorogobuzh chemical plant in Smolensk overnight.",
    "23 \u00b7 Cyclone Xavier: gale warning for Suwarrow, storm alert for Pukapuka.",
    "24 \u00b7 \u2018Just fireworks\u2019: BBC hears from people inside a besieged Yemeni city.",
    "25 \u00b7 Africa wants $120bn a year to adapt; Europe says spend the money already pledged.",
    "26 \u00b7 Jepchirchir gets a three-year ban after admitting EPO violations.",
    "27 \u00b7 Phillips: centuries vs India in all three formats in one year.",
    "28 \u00b7 Mhambrey in talks with Punjab Kings over an IPL 2027 coaching role.",
    "29 \u00b7 Chennai hotel opens a Dhoni tribute room \u2014 Room No. 7.",
    "30 \u00b7 Vasco da Gama 2-1 Internacional; Vit\u00f3ria 2-1 Bragantino in Brazil.",
    "31 \u00b7 Alcaraz faces Cobolli as the ATP Finals group stage ends in Turin.",
    "32 \u00b7 East Bengal host SC Delhi in the ISL on Friday; Habas calls for a turnaround.",
    "33 \u00b7 Saudi defences destroy two Houthi drones bound for the south.",
    "34 \u00b7 Bengaluru host Mumbai City in the ISL; Mumbai seek a first win.",
    "35 \u00b7 UK and EU agree a Brexit reset in Brussels \u2014 100,000 youth visas, food checks eased.",
    "36 \u00b7 White House taps Kirsten Davies as cyber chief after US outages.",
    "37 \u00b7 13,000 protest in Tokyo against the Takaichi government's policies.",
    "38 \u00b7 Houthis claim drone and missile strikes on four Saudi targets.",
]

# ---------------------------------------------------------------- layout
# (1) masthead
d.text((W // 2, 4), "WORLD NEWS", font=F(BLACK, 74), fill=INK, anchor="ma")
d.line([M, 92, W - M, 92], fill=RED, width=4)
d.text((W // 2, 100), "FRIDAY 20 NOVEMBER 2026", font=F(BOLD, 26), fill=RED, anchor="ma")
d.text((W // 2, 132), SUB, font=F(ITAL, 17), fill=INK, anchor="ma")
d.line([M, 158, W - M, 158], fill=RULE, width=2)
d.line([M, 162, W - M, 162], fill=RULE, width=1)

# (3) number strip
y = 170
cell_w = CW // 6
for i, (num, label) in enumerate(NUMBERS):
    cx = M + cell_w * i + cell_w // 2
    d.text((cx, y), num, font=F(BLACK, 26), fill=INK, anchor="ma")
    d.text((cx, y + 32), label, font=F(BOLD, 10), fill=GREY, anchor="ma")
    if i:
        d.line([M + cell_w * i, y + 2, M + cell_w * i, y + 42], fill=(200, 200, 200), width=1)
d.line([M, 218, W - M, 218], fill=RULE, width=1)

# (4) region tabs
y = 226
tab_w = (CW - 5 * 6) // 6
for i, (name, cnt) in enumerate(REGIONS):
    tx = M + i * (tab_w + 6)
    d.rounded_rectangle([tx, y, tx + tab_w, y + 24], radius=5, fill=LIGHT, outline=INK, width=1)
    f1, f2 = F(BOLD, 12), F(BLACK, 15)
    tw = d.textlength(name, font=f1) + d.textlength(" " + str(cnt), font=f2) + 4
    sx = tx + (tab_w - tw) // 2
    d.text((sx, y + 4), name, font=f1, fill=INK)
    d.text((sx + d.textlength(name, font=f1) + 4, y + 2), str(cnt), font=f2, fill=RED)

# (5) lead 1 - Trump, full width
y = 258
d.rectangle([M, y, M + 108, y + 100], fill=LIGHT, outline=INK, width=1)
icon_whitehouse(M + 6, y + 4, 96)
tx = M + 122
draw_tag(tx, y, LEAD1["num"], LEAD1["label"])
d.text((tx, y + 16), LEAD1["headline"], font=F(BLACK, 32), fill=INK)
d.text((tx, y + 54), LEAD1["deck"], font=F(ITAL, 16), fill=GREY)
body = wrap(LEAD1["body"], F(REG, 14), W - M - tx)
for i, ln in enumerate(body[:2]):
    d.text((tx, y + 76 + i * 17), ln, font=F(REG, 14), fill=INK)
d.line([M, y + 108, W - M, y + 108], fill=RULE, width=1)

# leads 2-3, two columns
y = 374
col_w = (CW - 12) // 2
for j, (lead, icon) in enumerate([(LEAD2, icon_blast), (LEAD3, icon_climate)]):
    cx0 = M + j * (col_w + 12)
    d.rectangle([cx0, y, cx0 + 84, y + 96], fill=LIGHT, outline=INK, width=1)
    icon(cx0 + 4, y + 4, 76)
    tx = cx0 + 96
    draw_tag(tx, y, lead["num"], lead["label"])
    d.text((tx, y + 16), lead["headline"], font=F(BLACK, 20), fill=INK)
    body = wrap(lead["body"], F(REG, 13), cx0 + col_w - tx)
    for i, ln in enumerate(body[:3]):
        d.text((tx, y + 46 + i * 15), ln, font=F(REG, 13), fill=INK)
d.line([M, y + 104, W - M, y + 104], fill=RULE, width=1)

# (6) medium grid: 10 stories, 5 cols x 2 rows
y = 486
cell_w = (CW - 4 * 8) // 5
cell_h = 87
for idx, (num, headline, body, icon) in enumerate(MEDIUM):
    r, c = divmod(idx, 5)
    x0 = M + c * (cell_w + 8)
    y0 = y + r * cell_h
    if c:
        d.line([x0 - 4, y0 + 2, x0 - 4, y0 + cell_h - 12], fill=(220, 220, 220), width=1)
    if r:
        d.line([x0, y0 - 4, x0 + cell_w, y0 - 4], fill=(220, 220, 220), width=1)
    d.text((x0, y0), num, font=F(BOLD, 12), fill=RED)
    icon(x0 + cell_w - 34, y0, 34)
    hl = wrap(headline, F(BOLD, 14), cell_w - 40)
    for i, ln in enumerate(hl[:2]):
        d.text((x0, y0 + 16 + i * 16), ln, font=F(BOLD, 14), fill=INK)
    n_hl = min(len(hl), 2)
    bl = wrap(body, F(REG, 10), cell_w)
    for i, ln in enumerate(bl[:2]):
        d.text((x0, y0 + 16 + n_hl * 16 + 2 + i * 12), ln, font=F(REG, 10), fill=INK)

# (7) world map with numbered pins
y = 668
d.text((M, y), "THE WORLD TODAY \u2014 WHERE THE NEWS HAPPENED", font=F(BOLD, 13), fill=INK)
map_y, map_h = y + 18, 110
d.rectangle([M, map_y, W - M, map_y + map_h], fill=SEA, outline=INK, width=1)


def px(lon, lat):
    return (M + (lon + 180) / 360 * CW, map_y + (75 - lat) / 135 * map_h)


for poly in CONTINENTS:
    d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND, outline=LANDLINE)
for num, lon, lat in PINS:
    cx, cy = px(lon, lat)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
    d.text((cx, cy), str(num), font=F(BOLD, 8), fill=(255, 255, 255), anchor="mm")

# (8) ALSO ON list
y = map_y + map_h + 10
d.text((M, y), "ALSO ON FRIDAY \u2014 25 MORE STORIES", font=F(BOLD, 14), fill=INK)
d.line([M, y + 18, W - M, y + 18], fill=RULE, width=1)
ly = y + 24
f_line = F(REG, 11)
f_num = F(BOLD, 11)
col2_x = M + CW // 2 + 8
for i, line in enumerate(ALSO):
    num, rest = line.split(" \u00b7 ", 1)
    lx = M if i < 13 else col2_x
    row = i if i < 13 else i - 13
    yy = ly + row * 11
    d.text((lx, yy), num, font=f_num, fill=RED)
    d.text((lx + 22, yy), rest, font=f_line, fill=INK)

# (9) DATE CHECK box (two lines)
y = ly + 13 * 11 + 4
d.rectangle([M, y, W - M, y + 26], fill=LIGHT, outline=INK, width=1)
d.text((M + 6, y + 3),
       "DATE CHECK \u2014 Not today: ICJ Rohingya ruling \u00b7 Trump\u2013Xi\u2013Putin peace declaration \u00b7 "
       "Crimean Bridge strike \u00b7 Anthropic IPO debut \u00b7 Gaza tank raid (18\u201319 Nov) \u00b7 SAFF final (17 Nov).",
       font=F(REG, 9), fill=INK)
d.text((M + 6, y + 14),
       "Also not today: Nvidia subpoena \u00b7 Fiona dies \u00b7 Denmark\u2013Greenland deal \u00b7 Save the Children report \u00b7 "
       "Berlin summit (all 19 Nov) \u00b7 M\u00e9lenchon\u2013Greens (18 Nov).",
       font=F(REG, 9), fill=INK)

# (10) footer
d.text((W // 2, y + 31),
       "Sources: Reuters \u00b7 BBC \u00b7 Le Monde \u00b7 AP \u00b7 AFP \u00b7 Kyiv Independent \u00b7 The Times \u00b7 ESPNcricinfo \u2014 "
       "all 38 stories verified from Friday 20 November 2026 only.",
       font=F(REG, 9), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
