#!/usr/bin/env python3
"""World News - Friday 20 November 2026 (38 stories).

VISUAL REVISION edition: same 38 verified stories, same 10-element
winner template, rebuilt presentation from the top-10/top-50 research
(13:50 WIB, 17 feed images studied):
  1 big coloured scene illustrations for the 3 leads (Akvan is lead #01),
  2 giant serif date masthead + "THE WORLD IN ONE DAY" kicker,
  3 small coloured illustrations for all 10 medium stories,
  4 dark navy map with cream continents, red pins, legend + caption,
  5 visible source tags per story ("CONFIRMED . outlet") + HOW SURE line,
  6 warm cream paper + serif headlines (body stays sans, readable small),
  7 geographic region tabs.
Facts, numbers and dates are UNCHANGED from the 38-story edition
(commit 2b4d0dcd): every story still verified from 20 November 2026
sources only. All artwork drawn by hand in PIL (no photos, no AI
generation). Deterministic: two runs produce byte-identical output.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28
CW = W - 2 * M
PAPER = (250, 243, 228)          # warm cream newspaper paper
PANEL = (253, 250, 242)          # slightly lighter cream for tiles
INK = (26, 26, 26)
RED = (176, 18, 18)
BLUE = (24, 62, 140)
NAVY = (16, 36, 86)              # dark navy map + night scenes
GREY = (110, 104, 92)
LIGHT = (238, 230, 212)
RULE = (26, 26, 26)
GREEN = (34, 120, 60)
LAND = (233, 224, 196)           # cream continents on the navy map
LANDLINE = (198, 188, 158)

NOTO = "/usr/share/fonts/truetype/noto"


def F(name, size):
    return ImageFont.truetype(os.path.join(NOTO, name), size)


BLACK = "NotoSans-Black.ttf"
BOLD = "NotoSans-Bold.ttf"
REG = "NotoSans-Regular.ttf"
ITAL = "NotoSans-Italic.ttf"
SERIF = "NotoSerif-Bold.ttf"
SERIFB = "NotoSerif-Black.ttf"
SERIFREG = "NotoSerif-Regular.ttf"

img = Image.new("RGB", (W, H), PAPER)
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


def draw_source(x, y, outlet):
    """Visible proof tag: green check + 'CONFIRMED . outlet'."""
    f = F(BOLD, 9)
    d.text((x, y), "\u2713 CONFIRMED", font=f, fill=GREEN)
    w = d.textlength("\u2713 CONFIRMED", font=f)
    d.text((x + w + 5, y), "\u00b7 " + outlet, font=f, fill=GREY)


# ---------------------------------------------------------------- icons
# (same hand-drawn icons as the 38-story edition; now drawn inside
# coloured tiles so they read as small illustrations, not line art)
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


# ---------------------------------------------------------------- big lead scenes
def scene_cyclone(x, y, w, h):
    """Cyclone Akvan over the Bay of Bengal: spiral bands over a dark
    teal sea, red eye, sand coastline at the bottom, rain streaks."""
    # sea: horizontal bands, darker toward the bottom
    bands = 10
    top = (14, 74, 96)
    bot = (8, 42, 62)
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        d.rectangle([x, y + i * h / bands, x + w, y + (i + 1) * h / bands + 1], fill=col)
    # coastline: sand strip along the bottom-left (Odisha coast)
    coast = [(x, y + h), (x, y + h - 24), (x + w * 0.22, y + h - 28),
             (x + w * 0.45, y + h - 16), (x + w * 0.62, y + h - 22),
             (x + w * 0.8, y + h - 8), (x + w, y + h - 12), (x + w, y + h)]
    d.polygon(coast, fill=(214, 196, 150))
    d.line(coast[:-1], fill=(255, 255, 255), width=2)
    # spiral: wide elliptical bands around the eye, pale cyan + white,
    # big enough to fill the panel (the top-10 leads are dominated by
    # their scene, not by a small icon in a corner)
    cx, cy = x + w * 0.58, y + h * 0.52
    cols = [(235, 245, 250), (170, 215, 232), (235, 245, 250), (120, 185, 210),
            (235, 245, 250)]
    radii = [(0.40, 0.48), (0.32, 0.40), (0.24, 0.30), (0.16, 0.20), (0.09, 0.12)]
    for i, (rx, ry) in enumerate(radii):
        d.arc([cx - rx * w, cy - ry * h, cx + rx * w, cy + ry * h],
              195 - i * 55, 345 - i * 55, fill=cols[i], width=5)
    # eye: red dot with white ring
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED, outline=(255, 255, 255), width=2)
    # rain streaks around the spiral
    for (rx, ry, ln) in [(0.12, 0.25, 14), (0.2, 0.55, 11), (0.3, 0.18, 12),
                         (0.82, 0.2, 13), (0.88, 0.6, 11), (0.72, 0.78, 12),
                         (0.45, 0.12, 10), (0.55, 0.82, 10), (0.06, 0.7, 12),
                         (0.94, 0.45, 11)]:
        sx, sy = x + w * rx, y + h * ry
        d.line([sx, sy, sx - 4, sy + ln], fill=(200, 225, 238), width=2)
    # caption strip
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(8, 28, 44))
    d.text((x + 8, y + h - 15), "CYCLONE AKVAN MAKES LANDFALL \u2014 ODISHA COAST",
           font=F(BOLD, 10), fill=(255, 255, 255))


def scene_kyiv(x, y, w, h):
    """Kyiv at night: navy sky, black skyline with lit windows,
    orange missile trails with bright heads, one blast star."""
    bands = 8
    top = (14, 22, 52)
    bot = (52, 38, 78)
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        d.rectangle([x, y + i * h / bands, x + w, y + (i + 1) * h / bands + 1], fill=col)
    # stars
    for (sx, sy) in [(0.08, 0.2), (0.2, 0.12), (0.35, 0.28), (0.5, 0.1),
                     (0.68, 0.22), (0.82, 0.12), (0.93, 0.3), (0.6, 0.35)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(255, 255, 255))
    # skyline silhouette along the bottom
    base = y + h
    heights = [0.42, 0.62, 0.35, 0.55, 0.3, 0.66, 0.45, 0.38, 0.58, 0.33]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 1, base - h * hh, bx + bw - 1, base], fill=(8, 10, 18))
        for wy in range(2):
            for wx in range(2):
                wx0 = bx + bw * (0.25 + wx * 0.4)
                wy0 = base - h * hh + 6 + wy * 12
                d.rectangle([wx0, wy0, wx0 + 3, wy0 + 4], fill=(255, 210, 110))
    # missile trails: diagonal orange lines with bright heads
    for (tx0, ty0, tx1, ty1) in [(0.12, 0.85, 0.3, 0.25), (0.45, 0.9, 0.62, 0.3),
                                 (0.72, 0.88, 0.86, 0.35)]:
        ax, ay = x + w * tx0, y + h * ty0
        bx, by = x + w * tx1, y + h * ty1
        d.line([ax, ay, bx, by], fill=(255, 140, 40), width=5)
        d.line([ax, ay, bx, by], fill=(255, 210, 120), width=2)
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 230, 150))
    # blast star where the middle trail lands
    cx, cy, r = x + w * 0.62, y + h * 0.3, 9
    pts = []
    for i in range(12):
        ang = i * 30 * math.pi / 180
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 200, 40), outline=RED)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)


def scene_trump(x, y, w, h):
    """The White House at dusk: deep blue sky, warm horizon, cream
    building with flag, lit windows."""
    bands = 8
    top = (26, 40, 92)
    bot = (214, 122, 62)
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        d.rectangle([x, y + i * h / bands, x + w, y + (i + 1) * h / bands + 1], fill=col)
    # stars in the upper sky
    for (sx, sy) in [(0.06, 0.18), (0.18, 0.1), (0.3, 0.22), (0.85, 0.12),
                     (0.92, 0.25), (0.72, 0.08)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(255, 255, 255))
    # White House silhouette, centred and large
    bx, bw = x + w * 0.28, w * 0.44
    base = y + h
    d.rectangle([bx, base - h * 0.66, bx + bw, base], fill=(240, 235, 220), outline=INK, width=1)
    d.polygon([(bx - bw * 0.06, base - h * 0.66), (bx + bw * 0.5, base - h * 0.88),
               (bx + bw * 1.06, base - h * 0.66)], fill=(232, 226, 208), outline=INK)
    for i in range(5):
        cx = bx + bw * (0.14 + i * 0.17)
        d.rectangle([cx, base - h * 0.64, cx + bw * 0.05, base - h * 0.08], fill=INK)
    d.rectangle([bx + bw * 0.42, base - h * 0.34, bx + bw * 0.58, base - h * 0.08], fill=INK)
    for wx in [0.2, 0.68]:
        d.rectangle([bx + bw * wx, base - h * 0.56, bx + bw * (wx + 0.1), base - h * 0.46],
                    fill=(255, 200, 90))
    # flag on the pediment
    fx, fy = bx + bw * 0.5, base - h * 0.88
    d.line([fx, fy, fx, fy - 10], fill=INK, width=2)
    d.polygon([(fx, fy - 10), (fx + 14, fy - 7), (fx, fy - 4)], fill=RED)
    # low trees at the far edges
    for tx in [x + w * 0.03, x + w * 0.9]:
        d.ellipse([tx, base - h * 0.26, tx + w * 0.07, base - h * 0.08], fill=(24, 60, 36))

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
# pins: (number, lon, lat) — renumbered for the new lead order:
# 01 Akvan (Odisha), 02 Trump (Washington), 03 Kyiv, 04 COP31 (Antalya),
# 05 Wall Street, 06 New Caledonia quake, 07 Iran war cost (Tehran),
# 08 Pochettino (Manchester), 09 India v NZ, 10 ASEAN, 11 Haiti,
# 12 GTA VI (Florida), 13 Justice Varma (Delhi)
PINS = [
    (1, 85, 20), (2, -80, 36), (3, 30, 50), (4, 33, 37), (5, -74, 40),
    (6, 171, -27), (7, 51, 35), (8, -2, 53), (9, 175, -41), (10, 105, 10),
    (11, -72, 19), (12, -84, 25), (13, 77, 28),
]

# ---------------------------------------------------------------- data
# Facts, numbers and dates are UNCHANGED from the 38-story edition.
SUB = "Cyclone Akvan hits Odisha  \u00b7  Trump delays the Iran call  \u00b7  Missiles hit Kyiv overnight"

NUMBERS = [
    ("38", "STORIES TODAY"),
    ("300,000", "EVACUATED IN ODISHA"),
    ("49,097", "DOW, BELOW 50,000"),
    ("$48BN", "COST OF IRAN WAR"),
    ("20", "MISSILES FIRED AT KYIV"),
    ("175*", "NICHOLLS, NOT OUT"),
]

# Geographic tabs (counts sum to 38):
# WORLD 1 (COP31, a global summit) · EUROPE 8 · AMERICAS 7 ·
# ASIA-PACIFIC 10 · MIDEAST 6 · AFRICA 3 · OCEANIA 3
REGIONS = [("WORLD", 1), ("EUROPE", 8), ("AMERICAS", 7), ("ASIA-PACIFIC", 10),
           ("MIDEAST", 6), ("AFRICA", 3), ("OCEANIA", 3)]

# Leads, reordered: the most visual story (Akvan) is now lead #01,
# as in 7-8 of the top 10. Text is unchanged from the 38-story edition.
LEAD1 = {
    "num": "01", "label": "TOP STORY", "source": "Reuters",
    "headline": "CYCLONE AKVAN HITS ODISHA",
    "deck": "300,000 evacuated as the storm makes landfall.",
    "body": "The cyclone makes landfall on the Odisha coast; 300,000 people are evacuated "
            "to shelters as winds and rain lash the coast.",
}
LEAD2 = {
    "num": "02", "label": "WHITE HOUSE", "source": "Reuters",
    "headline": "TRUMP DELAYS IRAN DECISION",
    "deck": "No rush on war, he says.",
    "body": "He will \u2018see what happens\u2019 after 1 January \u2014 and the decision on Iran is "
            "delayed to 2027.",
}
LEAD3 = {
    "num": "03", "label": "UKRAINE", "source": "Kyiv Independent",
    "headline": "MISSILES HIT KYIV OVERNIGHT",
    "body": "Russia fires nearly 20 ballistic missiles at Kyiv overnight; bridges are hit and "
            "fires burn. A three-storey building in Obolonskyi catches fire; no casualties at first.",
}

# Medium stories 04-13, renumbered for the new lead order.
# (num, headline, body, icon, tile colour, source)
# Sources are the outlets the 38-story edition verified each story from
# (footer list); Kyiv Independent, ESPNcricinfo and NPR are named in the
# README for those stories.
MEDIUM = [
    ("04", "COP31 DROPS PHASE-OUT",
     "The climate summit closes in Antalya \u2014 but the final draft drops the call to phase out "
     "fossil fuels, sparking outcry.", icon_climate, (150, 200, 185), "Reuters"),
    ("05", "WALL STREET SINKS",
     "Dow falls below 50,000 to 49,097; S&P \u22122.02% and Nasdaq \u22122.25%.", icon_chart,
     (215, 140, 130), "Reuters"),
    ("06", "5.6 QUAKE NEAR NEW CALEDONIA",
     "A 5.6-magnitude quake strikes 548 km south-east of Noum\u00e9a, 10 km deep.", icon_quake,
     (215, 195, 150), "AFP"),
    ("07", "US WAR WITH IRAN COST $48BN",
     "The Pentagon says the US war with Iran has cost over $48bn.", icon_dollar,
     (225, 215, 170), "AP"),
    ("08", "POCHETTINO JOINS UNITED",
     "New coach calls for unity in his first address; United are 18th.", icon_ball,
     (120, 175, 115), "The Times"),
    ("09", "INDIA v NZ, DAY 2",
     "Nicholls 175* and Phillips 118 lift NZ to 368 all out; India 52/0.", icon_cricket,
     (140, 190, 140), "ESPNcricinfo"),
    ("10", "ASEAN SUMMIT CLOSES",
     "Leaders seal a digital trade deal; the sea code is unresolved.", icon_flags,
     (150, 170, 215), "Reuters"),
    ("11", "HAITI TROOP DEAL",
     "Haiti approves a deal for Salvadoran troops as gang strikes widen.", icon_shield,
     (225, 215, 170), "AP"),
    ("12", "GTA VI\u2019S NPCs",
     "The crowd that makes the game\u2019s huge world feel real, says NPR.", icon_city,
     (205, 145, 185), "NPR"),
    ("13", "JUSTICE VARMA\u2019S LETTER",
     "In his letter, Justice Varma says his resignation admits no guilt.", icon_scales,
     (215, 200, 160), "AP"),
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
# (1) masthead: kicker + giant serif date (the top-10 pattern)
d.text((W // 2, 6), " ".join("THE WORLD IN ONE DAY"), font=F(BOLD, 12),
       fill=GREY, anchor="ma")
d.text((W // 2, 20), "Friday 20 November 2026", font=F(SERIFB, 54), fill=INK, anchor="ma")
d.line([M, 90, W - M, 90], fill=RED, width=4)
d.text((W // 2, 96), SUB, font=F(ITAL, 15), fill=INK, anchor="ma")
d.line([M, 120, W - M, 120], fill=RULE, width=2)
d.line([M, 124, W - M, 124], fill=RULE, width=1)

# (3) number strip (facts unchanged)
y = 130
cell_w = CW // 6
for i, (num, label) in enumerate(NUMBERS):
    cx = M + cell_w * i + cell_w // 2
    d.text((cx, y), num, font=F(SERIFB, 22), fill=INK, anchor="ma")
    d.text((cx, y + 28), label, font=F(BOLD, 9), fill=GREY, anchor="ma")
    if i:
        d.line([M + cell_w * i, y + 2, M + cell_w * i, y + 38], fill=(200, 192, 172), width=1)
d.line([M, 180, W - M, 180], fill=RULE, width=1)

# (4) region tabs, geographic (counts sum to 38)
y = 188
tab_w = (CW - 6 * 6) // 7
for i, (name, cnt) in enumerate(REGIONS):
    tx = M + i * (tab_w + 6)
    d.rounded_rectangle([tx, y, tx + tab_w, y + 24], radius=5, fill=PANEL, outline=INK, width=1)
    f1, f2 = F(BOLD, 11), F(BLACK, 14)
    tw = d.textlength(name, font=f1) + d.textlength(" " + str(cnt), font=f2) + 4
    sx = tx + (tab_w - tw) // 2
    d.text((sx, y + 5), name, font=f1, fill=INK)
    d.text((sx + d.textlength(name, font=f1) + 4, y + 3), str(cnt), font=f2, fill=RED)

# (5) lead 1 - Akvan, full width: text left, big scene right
y = 220
scene_x, scene_w, scene_h = 620, W - M - 620, 112
scene_cyclone(scene_x, y, scene_w, scene_h)
d.rectangle([scene_x, y, scene_x + scene_w, y + scene_h], outline=INK, width=1)
tx = M
draw_tag(tx, y, LEAD1["num"], LEAD1["label"])
d.text((tx, y + 18), LEAD1["headline"], font=F(SERIFB, 26), fill=INK)
d.text((tx, y + 50), LEAD1["deck"], font=F(ITAL, 14), fill=GREY)
body = wrap(LEAD1["body"], F(REG, 12), scene_x - 12 - tx)
for i, ln in enumerate(body[:2]):
    d.text((tx, y + 68 + i * 15), ln, font=F(REG, 12), fill=INK)
draw_source(tx, y + 100, LEAD1["source"])
d.line([M, y + scene_h + 6, W - M, y + scene_h + 6], fill=RULE, width=1)

# leads 2-3, two columns: full-width scene band on top of each column
y = 342
col_w = (CW - 12) // 2
for j, (lead, scene) in enumerate([(LEAD2, scene_trump), (LEAD3, scene_kyiv)]):
    cx0 = M + j * (col_w + 12)
    scene(cx0, y, col_w, 50)
    d.rectangle([cx0, y, cx0 + col_w, y + 50], outline=INK, width=1)
    ty = y + 56
    draw_tag(cx0, ty, lead["num"], lead["label"])
    d.text((cx0, ty + 16), lead["headline"], font=F(SERIFB, 19), fill=INK)
    body = wrap(lead["body"], F(REG, 12), col_w)
    for i, ln in enumerate(body[:2]):
        d.text((cx0, ty + 42 + i * 13), ln, font=F(REG, 12), fill=INK)
    draw_source(cx0, ty + 70, lead["source"])
d.line([M, y + 136, W - M, y + 136], fill=RULE, width=1)

# (6) medium grid: 10 stories, 5 cols x 2 rows, each with a small
# coloured illustration tile at top-right + visible source tag
y = 486
cell_w = (CW - 4 * 8) // 5
cell_h = 84
for idx, (num, headline, body, icon, tile, source) in enumerate(MEDIUM):
    r, c = divmod(idx, 5)
    x0 = M + c * (cell_w + 8)
    y0 = y + r * cell_h
    if c:
        d.line([x0 - 4, y0 + 2, x0 - 4, y0 + cell_h - 10], fill=(210, 200, 180), width=1)
    if r:
        d.line([x0, y0 - 4, x0 + cell_w, y0 - 4], fill=(210, 200, 180), width=1)
    d.text((x0, y0), num, font=F(BOLD, 11), fill=RED)
    # coloured illustration tile
    tx0, ty0, tw, th = x0 + cell_w - 52, y0, 52, 36
    d.rounded_rectangle([tx0, ty0, tx0 + tw, ty0 + th], radius=3, fill=tile, outline=INK, width=1)
    icon(tx0 + 7, ty0 + 1, 34)
    hl = wrap(headline, F(SERIFB, 13), cell_w - 58)
    for i, ln in enumerate(hl[:2]):
        d.text((x0, y0 + 13 + i * 15), ln, font=F(SERIFB, 13), fill=INK)
    n_hl = min(len(hl), 2)
    bl = wrap(body, F(REG, 10), cell_w)
    for i, ln in enumerate(bl[:2]):
        d.text((x0, y0 + 13 + n_hl * 15 + 2 + i * 12), ln, font=F(REG, 10), fill=INK)
    draw_source(x0, y0 + 73, source)

# (7) world map: dark navy sea, cream continents, red pins, legend
y = 662
d.text((M, y), "THE WORLD TODAY \u2014 WHERE THE NEWS HAPPENED", font=F(BOLD, 13), fill=INK)
map_y, map_h = y + 16, 88
d.rectangle([M, map_y, W - M, map_y + map_h], fill=NAVY, outline=INK, width=1)


def px(lon, lat):
    return (M + (lon + 180) / 360 * CW, map_y + (75 - lat) / 135 * map_h)


for poly in CONTINENTS:
    d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND, outline=LANDLINE)
for num, lon, lat in PINS:
    cx, cy = px(lon, lat)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
    d.text((cx, cy), str(num), font=F(BOLD, 8), fill=(255, 255, 255), anchor="mm")
d.text((M, map_y + map_h + 4),
       "RED NUMBERS MARK STORIES 1\u201313  \u00b7  01 CYCLONE AKVAN, ODISHA  \u00b7  02 TRUMP, WASHINGTON  \u00b7  03 KYIV",
       font=F(BOLD, 9), fill=GREY)

# (8) ALSO ON list (unchanged text)
y = map_y + map_h + 20
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

# (9) DATE CHECK box (unchanged text)
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

# (10) footer: sources + HOW SURE line
d.text((W // 2, y + 31),
       "Sources: Reuters \u00b7 BBC \u00b7 Le Monde \u00b7 AP \u00b7 AFP \u00b7 Kyiv Independent \u00b7 The Times \u00b7 ESPNcricinfo \u2014 "
       "all 38 stories verified from Friday 20 November 2026 only.",
       font=F(REG, 9), fill=GREY, anchor="ma")
d.text((W // 2, y + 42),
       "HOW SURE \u2014 Every story above is confirmed from a source dated 20 November 2026.",
       font=F(BOLD, 9), fill=INK, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
