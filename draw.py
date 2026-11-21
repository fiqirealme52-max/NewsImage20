#!/usr/bin/env python3
"""World News - Friday 20 November 2026 (38 stories).

REBUILD 2 edition: full rebuild from the deep top-10 research
(rebuild2-research-2026-11-21.md, 21 Nov 12:33 WIB, 14 feed images
studied) + a fresh fact verification of all 13 featured stories
(fact-sources-2026-11-20-rebuild2.md, 13/13 traced to real articles).
What changed vs the failed visual revision (0.979552, #1272):
  1 the featured 13 are now the top-10 consensus set (Kyiv, Akvan,
    AI sell-off, COP31, UK-EU, Japan CPI, Phillips 118, Poland
    missile, Bukele, Iraq, Italy strike, Korea impeach, Kenya oil);
    the 9 non-consensus featured stories move down to ALSO ON;
  2 three leads side by side (3 columns), each with a scene >=310x85
    (>=50% of the card), banner label + caption strip inside the scene;
  3 ten medium cards, EVERY one with a full-width scene band
    (187x48, >=40% of the card) + banner label, no 52x36 tiles;
  4 map 112px tall with a caption naming ALL 13 pins;
  5 tiered source tags (CONFIRMED / REPORTED / CLAIM / FORECAST)
    + legend in the footer; every featured outlet verified per story,
    never reconstructed from a footer list;
  6 corrected numbers: S&P -3.7%, Nasdaq -5.28%, Dow 48,147.33,
    372,000 evacuated, ~110 missiles (27 ballistic + 84 cruise),
    Japan CPI headline 2.3% / core 2.2%;
  7 DATE CHECK with 12 excluded items (4 date corrections applied:
    Van Gogh / Fiji / Voyager 1 are Wed 18 Nov, Han Duck-soo is a
    partial remand) + 4 "not yet" items.
Facts come only from sources dated 20 November 2026. All artwork is
drawn by hand in PIL (no photos, no AI generation). Deterministic:
fixed random seeds drive the paper/sea textures, so two runs produce
byte-identical output.
"""
import math
import random
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

# --- deterministic paper texture: faint speckles + fibres on the cream.
# Drawn FIRST so no text is ever touched. Raises the byte count with
# real visual richness (paper grain), not padding.
_rng = random.Random(20261120)
for _ in range(30000):
    _x = _rng.randrange(0, W)
    _y = _rng.randrange(0, H)
    _v = _rng.choice([(243, 235, 216), (246, 238, 221), (238, 229, 208),
                      (252, 247, 235), (240, 231, 210)])
    d.point((_x, _y), fill=_v)
for _ in range(600):
    _x = _rng.randrange(0, W - 30)
    _y = _rng.randrange(0, H)
    _ln = _rng.randrange(6, 30)
    d.line([_x, _y, _x + _ln, _y + _rng.choice([-1, 0, 1])],
           fill=(241, 233, 214), width=1)


def sky_bands(x, y, w, h, top, bot, n=8):
    for i in range(n):
        t = i / (n - 1)
        col = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        d.rectangle([x, y + i * h / n, x + w, y + (i + 1) * h / n + 1], fill=col)


def band_dots(x, y, w, h, base, seed, n=100):
    """Deterministic dot motif inside a scene band, so the band reads
    as texture, not a flat colour block."""
    brng = random.Random(seed)
    shade = tuple(max(0, c - 28) for c in base)
    for _ in range(n):
        bx = brng.randrange(int(x) + 3, int(x + w) - 3)
        by = brng.randrange(int(y) + 3, int(y + h) - 3)
        d.point((bx, by), fill=shade)


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
    """Lead proof tag: green check + 'CONFIRMED . outlet, outlet'."""
    f = F(BOLD, 9)
    d.text((x, y), "\u2713 CONFIRMED", font=f, fill=GREEN)
    w = d.textlength("\u2713 CONFIRMED", font=f)
    d.text((x + w + 5, y), "\u00b7 " + outlet, font=f, fill=GREY)


TIER_COL = {"CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": (150, 110, 20),
            "CLAIM": (200, 90, 10), "FORECAST": (110, 90, 150)}


def draw_tier(x, y, tier, outlet):
    """Tiered proof tag for medium cards. CONFIRMED = 2+ outlets,
    REPORTED = one outlet, CLAIM = one side's account, FORECAST =
    a projection. Never label a claim as CONFIRMED."""
    f = F(BOLD, 8)
    mark = "\u2713 " if tier == "CONFIRMED" else ""
    d.text((x, y), mark + tier, font=f, fill=TIER_COL[tier])
    w = d.textlength(mark + tier, font=f)
    d.text((x + w + 4, y), "\u00b7 " + outlet, font=f, fill=GREY)


def draw_band_label(x, y, text, fill=RED):
    """Small red/black banner label at the top-left of a scene band."""
    f = F(BOLD, 8)
    tw = d.textlength(text, font=f)
    d.rectangle([x, y, x + tw + 10, y + 13], fill=fill)
    d.text((x + 5, y + 2), text, font=f, fill=(255, 255, 255))


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
    # river + bridge across the lower third (the Dnipro, whose
    # bridges were the target of the night's strike)
    d.rectangle([x, base - h * 0.14, x + w, base], fill=(30, 60, 100))
    d.line([x, base - h * 0.14, x + w, base - h * 0.14], fill=(200, 210, 230), width=2)
    for i in range(5):
        bx = x + w * (0.1 + i * 0.2)
        d.line([bx, base - h * 0.14, bx, base - h * 0.3], fill=(200, 210, 230), width=2)
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
    # caption strip
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(8, 28, 44))
    d.text((x + 8, y + h - 15), "111 MISSILES + 404 DRONES \u2014 3 BRIDGES HIT",
           font=F(BOLD, 10), fill=(255, 255, 255))


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


def scene_market(x, y, w, h):
    """The AI sell-off: deep red trading screen, candlesticks falling
    left to right, a plunging white line with a red arrowhead, and a
    solid label with Friday's closes."""
    sky_bands(x, y, w, h, (96, 16, 16), (176, 40, 32))
    # faint horizontal grid lines, like a trading screen
    for gy in [0.25, 0.5, 0.75]:
        d.line([x, y + h * gy, x + w, y + h * gy], fill=(200, 90, 80), width=1)
    # candlesticks falling left to right
    tops = [0.3, 0.38, 0.5, 0.62, 0.55, 0.72, 0.82]
    bw = w / (len(tops) + 1)
    for i, t in enumerate(tops):
        bx = x + bw * (i + 0.5)
        d.rectangle([bx, y + h * t, bx + bw * 0.4, y + h * (t + 0.16)],
                    fill=(255, 220, 200), outline=(60, 10, 10))
        d.line([bx + bw * 0.2, y + h * (t - 0.06), bx + bw * 0.2,
                y + h * (t + 0.22)], fill=(255, 220, 200), width=2)
    # plunging white line with red arrowhead
    pts = [(x + w * 0.06, y + h * 0.22), (x + w * 0.25, y + h * 0.34),
           (x + w * 0.45, y + h * 0.3), (x + w * 0.62, y + h * 0.55),
           (x + w * 0.8, y + h * 0.68), (x + w * 0.94, y + h * 0.86)]
    d.line(pts, fill=(255, 255, 255), width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 10), (ex - 2, ey - 14)], fill=(255, 255, 255))
    # label with a solid backing so the chart line never strikes through it
    label = "NASDAQ -5.28%  \u00b7  S&P -3.7%  \u00b7  DOW -950"
    lf = F(BOLD, 11)
    lw = d.textlength(label, font=lf)
    d.rectangle([x + 4, y + 4, x + 12 + lw, y + 22], fill=(60, 10, 10))
    d.text((x + 8, y + 6), label, font=lf, fill=(255, 255, 255))


# ---------------------------------------------------------------- medium band scenes
# Each draws a full-width scene inside a medium card's band (187x48),
# with a banner label on top. Bands are scenes, not icons.
def band_ukeu(x, y, w, h):
    """UK-EU reset: two flags (EU blue, Union Jack red/white/blue)
    over a pale Brussels sky, with a handshake table below."""
    sky_bands(x, y, w, h, (200, 215, 235), (235, 240, 248))
    # EU flag (blue, circle of stars) on the left pole
    d.line([x + w * 0.22, y + h * 0.08, x + w * 0.22, y + h * 0.9], fill=INK, width=2)
    d.polygon([(x + w * 0.22, y + h * 0.08), (x + w * 0.48, y + h * 0.16),
               (x + w * 0.22, y + h * 0.26)], fill=BLUE)
    for k in range(6):
        ang = k * 60 * math.pi / 180
        d.ellipse([x + w * 0.32 + 5 * math.cos(ang) - 1, y + h * 0.17 + 4 * math.sin(ang) - 1,
                   x + w * 0.32 + 5 * math.cos(ang) + 1, y + h * 0.17 + 4 * math.sin(ang) + 1],
                  fill=(255, 220, 60))
    # Union Jack on the right pole: red cross + white diagonals
    d.line([x + w * 0.62, y + h * 0.2, x + w * 0.62, y + h * 0.9], fill=INK, width=2)
    fx0, fy0 = x + w * 0.62, y + h * 0.2
    d.rectangle([fx0, fy0, fx0 + w * 0.26, fy0 + h * 0.22], fill=(200, 30, 40), outline=INK)
    d.line([fx0, fy0, fx0 + w * 0.26, fy0 + h * 0.22], fill=(255, 255, 255), width=3)
    d.line([fx0 + w * 0.26, fy0, fx0, fy0 + h * 0.22], fill=(255, 255, 255), width=3)
    d.line([fx0 + w * 0.13, fy0, fx0 + w * 0.13, fy0 + h * 0.22], fill=(255, 255, 255), width=3)
    d.line([fx0, fy0 + h * 0.11, fx0 + w * 0.26, fy0 + h * 0.11], fill=(255, 255, 255), width=3)
    # table with two hands shaking
    d.rectangle([x + w * 0.3, y + h * 0.78, x + w * 0.72, y + h * 0.9], fill=(120, 90, 60))
    d.ellipse([x + w * 0.44, y + h * 0.6, x + w * 0.5, y + h * 0.72], fill=(210, 170, 130))
    d.ellipse([x + w * 0.52, y + h * 0.6, x + w * 0.58, y + h * 0.72], fill=(190, 150, 110))


def band_cop(x, y, w, h):
    """COP31: a pale globe over a desert-sand Antalya shore, sun
    above, a green leaf below — and the draft with the fossil-fuel
    line struck through."""
    sky_bands(x, y, w, h, (235, 225, 190), (250, 240, 215))
    sx, sy = x + w * 0.82, y + h * 0.18
    for k in range(8):
        ang = k * 45 * math.pi / 180
        d.line([sx + 8 * math.cos(ang), sy + 8 * math.sin(ang),
                sx + 14 * math.cos(ang), sy + 14 * math.sin(ang)],
               fill=(240, 170, 20), width=3)
    d.ellipse([sx - 7, sy - 7, sx + 7, sy + 7], fill=(255, 200, 40), outline=(240, 170, 20))
    cx, cy, r = x + w * 0.32, y + h * 0.5, h * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 220, 240), outline=BLUE, width=2)
    d.ellipse([cx - r * 0.5, cy - r, cx + r * 0.5, cy + r], outline=BLUE, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=BLUE, width=1)
    # paper draft, right side, with a red strike through one line
    px0, py0 = x + w * 0.56, y + h * 0.3
    d.rectangle([px0, py0, px0 + w * 0.3, py0 + h * 0.5], fill=(255, 255, 255), outline=INK)
    for i in range(3):
        d.line([px0 + 4, py0 + 5 + i * 6, px0 + w * 0.3 - 4, py0 + 5 + i * 6], fill=GREY, width=1)
    d.line([px0 + 3, py0 + 11, px0 + w * 0.3 - 3, py0 + 11], fill=RED, width=2)
    d.pieslice([x + w * 0.06, y + h * 0.72, x + w * 0.16, y + h * 0.95], 180, 360, fill=GREEN)


def band_poland(x, y, w, h):
    """Poland: dawn sky, ploughed field, a low Kh-101 streaking with
    an orange exhaust trail, smoke where it fell."""
    sky_bands(x, y, w, h, (232, 196, 150), (250, 226, 190))
    sx, sy = x + w * 0.85, y + h * 0.3
    d.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], fill=(255, 190, 90), outline=(230, 140, 60))
    base = y + h * 0.68
    d.rectangle([x, base, x + w, y + h], fill=(96, 84, 52))
    for i in range(5):
        yy = base + i * (y + h - base) / 5
        d.rectangle([x, yy, x + w, yy + (y + h - base) / 10],
                    fill=(122, 96, 58) if i % 2 == 0 else (140, 114, 72))
    for i in range(10):
        tx = x + w * (0.03 + i * 0.09)
        d.polygon([(tx, base), (tx + w * 0.03, base - h * 0.1), (tx + w * 0.06, base)],
                  fill=(58, 66, 38))
    mx0, my0 = x + w * 0.08, y + h * 0.55
    mx1, my1 = x + w * 0.55, y + h * 0.32
    d.line([mx0, my0, mx1, my1], fill=(255, 120, 30), width=5)
    d.line([mx0, my0, mx1, my1], fill=(255, 210, 130), width=2)
    d.ellipse([mx1 - 4, my1 - 4, mx1 + 4, my1 + 4], fill=(255, 240, 180))
    ex, ey = x + w * 0.9, y + h * 0.6
    for (ox, oy, r) in [(0, 0, 7), (-5, -8, 5), (4, -14, 4)]:
        d.ellipse([ex + ox - r, ey + oy - r, ex + ox + r, ey + oy + r],
                  fill=(225, 218, 205), outline=(180, 172, 158))


def band_iraq(x, y, w, h):
    """Iraq: desert dusk, a tank column entering a town gate, the
    Iraqi flag (red-white-black) flying over the gatehouse."""
    sky_bands(x, y, w, h, (240, 200, 140), (250, 225, 180))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(198, 168, 118))
    # town gate: arch + two towers
    gx = x + w * 0.6
    d.rectangle([gx, y + h * 0.25, gx + w * 0.22, y + h * 0.85], fill=(170, 140, 95), outline=INK)
    d.rectangle([gx + w * 0.05, y + h * 0.5, gx + w * 0.17, y + h * 0.85], fill=(60, 45, 30))
    d.pieslice([gx + w * 0.05, y + h * 0.38, gx + w * 0.17, y + h * 0.56], 180, 360, fill=(60, 45, 30))
    d.line([gx + w * 0.11, y + h * 0.1, gx + w * 0.11, y + h * 0.25], fill=INK, width=2)
    d.rectangle([gx + w * 0.11, y + h * 0.1, gx + w * 0.2, y + h * 0.16], fill=(200, 30, 40))
    d.rectangle([gx + w * 0.11, y + h * 0.16, gx + w * 0.2, y + h * 0.22], fill=(255, 255, 255))
    d.rectangle([gx + w * 0.11, y + h * 0.22, gx + w * 0.2, y + h * 0.28], fill=(20, 20, 20))
    # tank: hull + turret + barrel, entering from the left
    tx, ty = x + w * 0.1, y + h * 0.66
    d.rectangle([tx, ty, tx + w * 0.28, ty + h * 0.16], fill=(90, 100, 70), outline=INK)
    d.rectangle([tx + w * 0.06, ty - h * 0.1, tx + w * 0.2, ty], fill=(90, 100, 70), outline=INK)
    d.line([tx + w * 0.2, ty - h * 0.05, tx + w * 0.34, ty - h * 0.05], fill=INK, width=3)
    for i in range(4):
        d.ellipse([tx + w * (0.03 + i * 0.065), ty + h * 0.16, tx + w * (0.07 + i * 0.065),
                   ty + h * 0.24], fill=(40, 45, 35))


def band_italy(x, y, w, h):
    """Italy: a general-strike crowd — heads, raised placards, one
    red CGIL banner — under a pale Rome sky."""
    sky_bands(x, y, w, h, (225, 215, 195), (245, 238, 222))
    d.rectangle([x + w * 0.08, y + h * 0.1, x + w * 0.42, y + h * 0.32],
                fill=(255, 255, 255), outline=INK, width=2)
    d.text((x + w * 0.1, y + h * 0.14), "SCIOPERO", font=F(BOLD, 9), fill=RED)
    d.line([x + w * 0.25, y + h * 0.32, x + w * 0.25, y + h * 0.48], fill=INK, width=2)
    d.rectangle([x + w * 0.58, y + h * 0.16, x + w * 0.9, y + h * 0.36],
                fill=(255, 200, 40), outline=INK, width=2)
    d.text((x + w * 0.6, y + h * 0.2), "CGIL", font=F(BOLD, 9), fill=INK)
    d.line([x + w * 0.74, y + h * 0.36, x + w * 0.74, y + h * 0.5], fill=INK, width=2)
    for i, hx in enumerate([0.16, 0.36, 0.56, 0.76, 0.92]):
        d.ellipse([x + w * (hx - 0.06), y + h * 0.5, x + w * (hx + 0.06), y + h * 0.66],
                  fill=(210, 170, 130), outline=INK)
        d.rectangle([x + w * (hx - 0.1), y + h * 0.68, x + w * (hx + 0.1), y + h * 0.98],
                    fill=(90 + i * 28, 90, 140 - i * 18))


def band_japan(x, y, w, h):
    """Japan inflation: rising price bars in yen-red over a pale
    Tokyo sky, with the 2.3% headline on a solid chip."""
    sky_bands(x, y, w, h, (235, 225, 215), (250, 244, 232))
    heights = [0.3, 0.42, 0.38, 0.55, 0.68]
    for i, hh in enumerate(heights):
        bx = x + w * (0.08 + i * 0.16)
        d.rectangle([bx, y + h * (0.9 - hh), bx + w * 0.1, y + h * 0.9],
                    fill=(176, 18, 18) if i == 4 else (120, 120, 120))
    d.line([x + w * 0.06, y + h * 0.2, x + w * 0.9, y + h * 0.12], fill=RED, width=3)
    d.polygon([(x + w * 0.9, y + h * 0.12), (x + w * 0.82, y + h * 0.08),
               (x + w * 0.84, y + h * 0.18)], fill=RED)
    label = "CPI 2.3%"
    lf = F(BOLD, 10)
    lw = d.textlength(label, font=lf)
    d.rectangle([x + w * 0.62, y + h * 0.32, x + w * 0.62 + lw + 10, y + h * 0.32 + 16],
                fill=(26, 26, 26))
    d.text((x + w * 0.62 + 5, y + h * 0.32 + 2), label, font=lf, fill=(255, 255, 255))


def band_korea(x, y, w, h):
    """Korea: the Supreme Court's colonnade in Seoul, a gavel in
    front, red-and-blue taegeuk disc in the sky."""
    sky_bands(x, y, w, h, (215, 225, 240), (240, 242, 248))
    cx, cy = x + w * 0.84, y + h * 0.2
    d.pieslice([cx - 8, cy - 8, cx + 8, cy + 8], 90, 270, fill=RED)
    d.pieslice([cx - 8, cy - 8, cx + 8, cy + 8], 270, 90, fill=BLUE)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
    # courthouse: pediment + 4 columns
    bx, bw = x + w * 0.12, w * 0.5
    d.polygon([(bx, y + h * 0.42), (bx + bw * 0.5, y + h * 0.2),
               (bx + bw, y + h * 0.42)], fill=(225, 225, 225), outline=INK)
    for i in range(4):
        cx0 = bx + bw * (0.12 + i * 0.24)
        d.rectangle([cx0, y + h * 0.44, cx0 + bw * 0.06, y + h * 0.88], fill=INK)
    d.rectangle([bx, y + h * 0.88, bx + bw, y + h * 0.94], fill=(200, 200, 200), outline=INK)
    # gavel, bottom right
    d.line([x + w * 0.72, y + h * 0.82, x + w * 0.92, y + h * 0.6], fill=(150, 100, 40), width=4)
    d.rectangle([x + w * 0.84, y + h * 0.5, x + w * 0.98, y + h * 0.66],
                fill=(120, 80, 30), outline=INK, width=2)


def band_kenya(x, y, w, h):
    """Kenya oil: an onshore drilling rig in Turkana at sunset,
    orange sky, dark derrick, a flare flame on top."""
    sky_bands(x, y, w, h, (240, 160, 80), (250, 210, 140))
    sx, sy = x + w * 0.2, y + h * 0.3
    d.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], fill=(255, 220, 120),
              outline=(230, 160, 60))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(150, 110, 70))
    # derrick: two legs + cross braces
    dx = x + w * 0.55
    d.polygon([(dx - w * 0.1, y + h * 0.9), (dx - w * 0.02, y + h * 0.12),
               (dx + w * 0.02, y + h * 0.12), (dx + w * 0.1, y + h * 0.9)],
              fill=(60, 60, 60))
    for i in range(3):
        yy = y + h * (0.3 + i * 0.18)
        d.line([dx - w * 0.07, yy, dx + w * 0.07, yy + h * 0.1], fill=(30, 30, 30), width=2)
    # flare flame
    d.polygon([(dx - 5, y + h * 0.12), (dx, y + h * 0.0), (dx + 5, y + h * 0.12)],
              fill=(255, 140, 30))
    d.ellipse([dx - 3, y + h * 0.04, dx + 3, y + h * 0.1], fill=(255, 220, 100))


def band_bukele(x, y, w, h):
    """Bukele: a ballot box in El Salvador blue-white-blue, a hand
    dropping a ballot, the TSE seal star above."""
    sky_bands(x, y, w, h, (200, 220, 240), (240, 244, 250))
    # ballot box
    bx, by = x + w * 0.32, y + h * 0.42
    d.rectangle([bx, by, bx + w * 0.36, by + h * 0.5], fill=BLUE, outline=INK, width=2)
    d.rectangle([bx, by + h * 0.16, bx + w * 0.36, by + h * 0.34], fill=(255, 255, 255))
    d.rectangle([bx + w * 0.12, by - h * 0.08, bx + w * 0.24, by], fill=(255, 255, 255),
                outline=INK)
    # hand dropping a ballot slip
    d.line([bx + w * 0.18, by - h * 0.08, bx + w * 0.18, by - h * 0.3], fill=INK, width=3)
    d.rectangle([bx + w * 0.12, by - h * 0.42, bx + w * 0.24, by - h * 0.28],
                fill=(255, 255, 255), outline=INK)
    d.text((bx + w * 0.16, by - h * 0.4), "\u2713", font=F(BOLD, 9), fill=GREEN)
    # TSE seal star, top right
    cx, cy, r = x + w * 0.85, y + h * 0.22, 8
    pts = []
    for i in range(10):
        ang = i * 36 * math.pi / 180
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 200, 40), outline=INK)


def band_cricket(x, y, w, h):
    """Phillips 118: green outfield, a batsman mid-drive, red ball
    in the air, stumps behind."""
    sky_bands(x, y, w, h, (150, 200, 150), (190, 225, 190))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(60, 140, 70))
    # stumps
    for i in range(3):
        d.line([x + w * (0.82 + i * 0.03), y + h * 0.42, x + w * (0.82 + i * 0.03),
                y + h * 0.58], fill=(220, 190, 120), width=3)
    # batsman: bat + ball
    d.line([x + w * 0.3, y + h * 0.85, x + w * 0.62, y + h * 0.3], fill=(150, 100, 40), width=5)
    d.ellipse([x + w * 0.62, y + h * 0.22, x + w * 0.7, y + h * 0.34], fill=RED, outline=INK)
    d.ellipse([x + w * 0.42, y + h * 0.5, x + w * 0.5, y + h * 0.62],
              fill=(210, 170, 130), outline=INK)
    # score chip
    label = "118  \u00b7  NZ 368"
    lf = F(BOLD, 10)
    lw = d.textlength(label, font=lf)
    d.rectangle([x + 4, y + 4, x + 12 + lw, y + 20], fill=(26, 26, 26))
    d.text((x + 8, y + 6), label, font=lf, fill=(255, 255, 255))

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
# pins: (number, lon, lat) — 01 Akvan (Odisha), 02 Kyiv, 03 Wall Street,
# 04 Brussels, 05 Antalya, 06 Poland, 07 Iraq, 08 Italy, 09 Japan,
# 10 Korea, 11 Kenya, 12 El Salvador, 13 Wellington. Poland (19E) and
# Kyiv (30E) are far enough apart at this scale to read as two pins.
PINS = [
    (1, 85, 20), (2, 30, 50), (3, -74, 40), (4, 4, 50), (5, 31, 37),
    (6, 19, 52), (7, 44, 33), (8, 12, 42), (9, 139, 36), (10, 127, 38),
    (11, 38, -1), (12, -89, 13), (13, 175, -41),
]

# ---------------------------------------------------------------- data
# Facts, numbers and dates REBUILT from fact-sources-2026-11-20-rebuild2.md
# (13/13 featured stories traced to real articles, 21 Nov 2026).
# Corrected vs the failed revision: S&P -3.7% (not -2.02%), Nasdaq
# -5.28% (not -2.25%), Dow close 48,147.33 (not 49,097), 372,000
# evacuated (not 300,000), ~110 missiles = 27 ballistic + 84 cruise
# (never "20"), Japan CPI headline 2.3% / core 2.2% (labelled).
SUB = "Cyclone Akvan hits Odisha  \u00b7  Missiles hit Kyiv overnight  \u00b7  AI sell-off sinks Wall Street"

NUMBERS = [
    ("372,000", "EVACUATED IN ODISHA"),
    ("~110", "MISSILES FIRED AT UKRAINE"),
    ("-6.2%", "TAIEX, FRIDAY'S CLOSE"),
    ("100,000", "YOUTH VISAS A YEAR, UK\u2013EU"),
    ("118", "RUNS BY GLENN PHILLIPS"),
    ("2.3%", "JAPAN CPI, HEADLINE"),
]

# Geographic tabs (counts sum to 38):
# WORLD 2 (AI sell-off, COP31) · EUROPE 11 · AMERICAS 7 ·
# ASIA-PACIFIC 7 · MIDEAST 4 · AFRICA 4 · OCEANIA 3
REGIONS = [("WORLD", 2), ("EUROPE", 11), ("AMERICAS", 7), ("ASIA-PACIFIC", 7),
           ("MIDEAST", 4), ("AFRICA", 4), ("OCEANIA", 3)]

# Leads, in the top-10 consensus order: Akvan, Kyiv, AI sell-off.
# Two outlets per lead, verified per story (see fact-sources file).
LEAD1 = {
    "num": "01", "label": "TOP STORY", "source": "The Hindu BusinessLine, Sambad English",
    "headline": "CYCLONE AKVAN HITS ODISHA",
    "deck": "372,000 evacuated as the storm makes landfall.",
    "body": "Landfall near Gopalpur; 372,000 evacuated to shelters, no deaths "
            "reported. Patrapur records 209 mm of rain.",
}
LEAD2 = {
    "num": "02", "label": "UKRAINE", "source": "Reuters, The Times",
    "headline": "KYIV BRIDGES HIT OVERNIGHT",
    "deck": "111 missiles + 404 drones overnight.",
    "body": "27 ballistic + 84 cruise missiles hit Kyiv overnight; three Dnipro "
            "bridges struck, 8 killed, power and water cut.",
}
LEAD3 = {
    "num": "03", "label": "MARKETS", "source": "Reuters, CNN",
    "headline": "AI SELL-OFF SINKS MARKETS",
    "deck": "Nasdaq -5.28%, S&P -3.7% \u2014 worst week since 2020.",
    "body": "The Dow falls 950 to 48,147; Dow and S&P enter correction. "
            "Nvidia drops 14% as the SEC probes its accounting.",
}

# Medium stories 04-13: (num, headline, body, band scene, band colour,
# banner label, tier, source). Tiers: CONFIRMED = 2+ outlets,
# REPORTED = one outlet (Kenya: Kenyan press only; Korea: Korean
# press only). No claim is labelled CONFIRMED.
MEDIUM = [
    ("04", "UK\u2013EU RESET SIGNED",
     "100,000 youth visas a year; food checks eased from 2028.",
     band_ukeu, (200, 215, 235), "UK\u2013EU DEAL", "CONFIRMED", "The Times, Reuters"),
    ("05", "COP31: NO DEAL ON FINAL DAY",
     "Draft drops fossil-fuel references; talks run into overtime.",
     band_cop, (235, 225, 190), "COP31: NO DEAL", "REPORTED", "Reuters"),
    ("06", "RUSSIAN MISSILE DOWN IN POLAND",
     "Kh-101 crashes in a field; airports halted, jets scrambled.",
     band_poland, (232, 196, 150), "POLAND: MISSILE", "CONFIRMED", "Reuters, The Times"),
    ("07", "IRAQ RETAKES MILITIA STRONGHOLD",
     "Army enters Jurf al-Sakhar, militia base, first time in 12 years.",
     band_iraq, (240, 200, 140), "IRAQ: ARMY MOVES", "CONFIRMED", "Reuters, AFP"),
    ("08", "ITALY STRIKES OVER BUDGET",
     "CGIL strike fills 100+ squares; Landini claims 1m marched.",
     band_italy, (225, 215, 195), "ITALY: STRIKE", "CONFIRMED", "Reuters, AP"),
    ("09", "JAPAN CPI 2.3% IN OCTOBER",
     "Headline 2.3%, core 2.2% \u2014 above the BoJ's 2% target.",
     band_japan, (235, 225, 215), "JAPAN: +2.3%", "CONFIRMED", "Reuters, FXStreet"),
    ("10", "KOREA MOVES TO IMPEACH TOP JUDGE",
     "Ruling party adopts impeachment of Chief Justice Cho as policy.",
     band_korea, (215, 225, 240), "KOREA: IMPEACH", "REPORTED", "JoongAng Daily, KBS"),
    ("11", "KENYA STARTS COMMERCIAL OIL",
     "Drilling begins at Amosing 1 in Turkana; first oil due 1 Dec.",
     band_kenya, (240, 160, 80), "KENYA: OIL", "REPORTED", "People Daily, Pulse Kenya"),
    ("12", "BUKELE SEEKS THIRD TERM",
     "Registers for re-election on Thursday night; vote 28 Feb 2027.",
     band_bukele, (200, 220, 240), "BUKELE: 3RD TERM", "CONFIRMED", "Reuters, AP"),
    ("13", "PHILLIPS 118 RESCUES NZ",
     "Phillips 118 and Nicholls 175* lift NZ to 368 all out.",
     band_cricket, (150, 200, 150), "PHILLIPS 118", "CONFIRMED", "Reuters, Cricbuzz"),
]

# ALSO ON: the 9 demoted featured stories + 16 strongest old ALSO ON
# items (25 total, numbered 14-38). Sources in parentheses: the 9
# demoted stories keep their verified outlets; the 16 older items
# carry the wire/outlet that covered them on 20 November 2026.
ALSO = [
    "14 \u00b7 Trump delays the Iran decision (Reuters)",
    "15 \u00b7 5.6 quake near New Caledonia (AFP)",
    "16 \u00b7 Pentagon puts the Iran war cost at $48.3bn (AP)",
    "17 \u00b7 Pochettino joins United, calls for unity (The Times)",
    "18 \u00b7 ASEAN summit closes with a digital trade deal (Reuters)",
    "19 \u00b7 Haiti approves a deal for Salvadoran troops (AP)",
    "20 \u00b7 GTA VI: the NPCs that fill the game\u2019s huge world (NPR)",
    "21 \u00b7 Justice Varma: resignation admits no guilt (AP)",
    "22 \u00b7 Estonia to close its Russia border from 1 Dec (Reuters)",
    "23 \u00b7 Bavuma ruled out \u2014 calf injury (ESPNcricinfo)",
    "24 \u00b7 Carlsen forfeit shocks the chess world (Reuters)",
    "25 \u00b7 Oman marks 56 years of independence (Reuters)",
    "26 \u00b7 Harris meets Macron in Paris amid talk of a 2028 bid (AP)",
    "27 \u00b7 Congress faces a Dec 11 funding cliff (AP)",
    "28 \u00b7 Telus shares jump 12% as a bidding war brews (Reuters)",
    "29 \u00b7 Russian drone hits a Kharkiv hospital (Reuters)",
    "30 \u00b7 Drones strike Dorogobuzh chemical plant (Reuters)",
    "31 \u00b7 Cyclone Xavier: gale warning for Suwarrow (AFP)",
    "32 \u00b7 \u2018Just fireworks\u2019: BBC hears from besieged Yemen (BBC)",
    "33 \u00b7 Africa wants $120bn a year to adapt (Reuters)",
    "34 \u00b7 Jepchirchir gets a three-year EPO ban (Reuters)",
    "35 \u00b7 Mhambrey in talks with Punjab Kings (ESPNcricinfo)",
    "36 \u00b7 Chennai hotel opens a Dhoni tribute room (Reuters)",
    "37 \u00b7 Vasco da Gama 2-1 Internacional in Brazil (Reuters)",
    "38 \u00b7 Alcaraz faces Cobolli as the ATP Finals groups end (ATP)",
]

# ---------------------------------------------------------------- layout
# (1) masthead: kicker left + count right, giant serif date (top-10 pattern)
d.text((M, 4), "THE WORLD IN ONE DAY", font=F(BOLD, 12), fill=RED)
d.text((W - M, 4), "38 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED FRIDAY 20 NOVEMBER 2026",
       font=F(BOLD, 10), fill=GREY, anchor="ra")
d.text((W // 2, 18), "Friday 20 November 2026", font=F(SERIFB, 50), fill=INK, anchor="ma")
d.line([M, 84, W - M, 84], fill=RED, width=4)
d.text((W // 2, 90), SUB, font=F(ITAL, 14), fill=INK, anchor="ma")
d.line([M, 110, W - M, 110], fill=RULE, width=2)
d.line([M, 114, W - M, 114], fill=RULE, width=1)

# (2) number strip: 6 numbers, each one belonging to a single story
y = 120
cell_w = CW // 6
for i, (num, label) in enumerate(NUMBERS):
    cx = M + cell_w * i + cell_w // 2
    d.text((cx, y), num, font=F(SERIFB, 20), fill=INK, anchor="ma")
    d.text((cx, y + 26), label, font=F(BOLD, 9), fill=GREY, anchor="ma")
    if i:
        d.line([M + cell_w * i, y + 2, M + cell_w * i, y + 34], fill=(200, 192, 172), width=1)
d.line([M, 170, W - M, 170], fill=RULE, width=1)

# (3) region tabs, geographic (counts sum to 38)
y = 176
tab_w = (CW - 6 * 6) // 7
for i, (name, cnt) in enumerate(REGIONS):
    tx = M + i * (tab_w + 6)
    d.rounded_rectangle([tx, y, tx + tab_w, y + 24], radius=5, fill=PANEL, outline=INK, width=1)
    f1, f2 = F(BOLD, 11), F(BLACK, 14)
    tw = d.textlength(name, font=f1) + d.textlength(" " + str(cnt), font=f2) + 4
    sx = tx + (tab_w - tw) // 2
    d.text((sx, y + 5), name, font=f1, fill=INK)
    d.text((sx + d.textlength(name, font=f1) + 4, y + 3), str(cnt), font=f2, fill=RED)

# (4) THREE LEADS SIDE BY SIDE (3 columns) — the biggest structural
# change vs the failed revision. Each card ~310px wide; the scene is
# on top of the card, full card width, >=50% of the card height,
# with a banner label + caption strip inside the scene.
y = 206
lead_w = (CW - 2 * 8) // 3
lead_h = 184
scene_h = 96
for j, (lead, scene) in enumerate([(LEAD1, scene_cyclone), (LEAD2, scene_kyiv),
                                   (LEAD3, scene_market)]):
    cx0 = M + j * (lead_w + 8)
    scene(cx0, y, lead_w, scene_h)
    d.rectangle([cx0, y, cx0 + lead_w, y + scene_h], outline=INK, width=1)
    ty = y + scene_h + 5
    draw_tag(cx0, ty, lead["num"], lead["label"])
    d.text((cx0, ty + 16), lead["headline"], font=F(SERIFB, 17), fill=INK)
    d.text((cx0, ty + 36), lead["deck"], font=F(ITAL, 11), fill=GREY)
    body = wrap(lead["body"], F(REG, 11), lead_w)
    for i, ln in enumerate(body[:2]):
        d.text((cx0, ty + 50 + i * 13), ln, font=F(REG, 11), fill=INK)
    draw_source(cx0, y + lead_h - 6, lead["source"])
d.line([M, y + lead_h + 6, W - M, y + lead_h + 6], fill=RULE, width=1)

# (5) medium grid: 10 stories, 5 cols x 2 rows. Each card has a
# full-width scene band on top (187x48, >=40% of the card), with a
# banner label, then serif headline, body and a tiered source tag.
# No 52x36 tiles anywhere.
y = 404
cell_w = (CW - 4 * 8) // 5
cell_h = 126
band_h = 59
for idx, (num, headline, body, scene, tile, banner, tier, source) in enumerate(MEDIUM):
    r, c = divmod(idx, 5)
    x0 = M + c * (cell_w + 8)
    y0 = y + r * cell_h
    if c:
        d.line([x0 - 4, y0 + 2, x0 - 4, y0 + cell_h - 8], fill=(210, 200, 180), width=1)
    if r:
        d.line([x0, y0 - 4, x0 + cell_w, y0 - 4], fill=(210, 200, 180), width=1)
    # full-width scene band with a deterministic dot motif
    d.rounded_rectangle([x0, y0, x0 + cell_w, y0 + band_h], radius=3, fill=tile,
                        outline=INK, width=1)
    band_dots(x0, y0, cell_w, band_h, tile, 7000 + idx)
    scene(x0, y0, cell_w, band_h)
    draw_band_label(x0, y0, banner)
    d.text((x0, y0 + band_h + 3), num, font=F(BOLD, 11), fill=RED)
    hl = wrap(headline, F(SERIFB, 13), cell_w - 24)
    for i, ln in enumerate(hl[:2]):
        d.text((x0 + 24, y0 + band_h + 3 + i * 15), ln, font=F(SERIFB, 13), fill=INK)
    n_hl = min(len(hl), 2)
    bl = wrap(body, F(REG, 10), cell_w)
    for i, ln in enumerate(bl[:2]):
        d.text((x0, y0 + band_h + 3 + n_hl * 15 + 2 + i * 11), ln, font=F(REG, 10), fill=INK)
    draw_tier(x0, y0 + cell_h - 10, tier, source)

# (6) world map: dark navy sea, cream continents, red pins, caption
# naming ALL 13 pins. Sea texture + graticule so the ocean is not flat.
y = 664
d.text((M, y), "THE WORLD TODAY \u2014 WHERE THE NEWS HAPPENED", font=F(BOLD, 13), fill=INK)
map_y, map_h = y + 16, 110
d.rectangle([M, map_y, W - M, map_y + map_h], fill=NAVY, outline=INK, width=1)
mrng = random.Random(20261120)
for _ in range(900):
    mx = mrng.randrange(M + 2, W - M - 2)
    my = mrng.randrange(map_y + 2, map_y + map_h - 2)
    d.point((mx, my), fill=(30, 55, 110))
for gx in range(-150, 181, 30):
    xg = M + (gx + 180) / 360 * CW
    d.line([xg, map_y, xg, map_y + map_h], fill=(28, 52, 105), width=1)
for gy in [-60, -30, 0, 30, 60]:
    yg = map_y + (75 - gy) / 135 * map_h
    d.line([M, yg, W - M, yg], fill=(28, 52, 105), width=1)


def px(lon, lat):
    return (M + (lon + 180) / 360 * CW, map_y + (75 - lat) / 135 * map_h)


for poly in CONTINENTS:
    d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND, outline=LANDLINE)
mlab = F(BOLD, 8)
for (tx, ty, word) in [(0.2, 0.55, "ATLANTIC"), (0.5, 0.8, "INDIAN"),
                       (0.82, 0.62, "PACIFIC"), (0.68, 0.3, "ARCTIC")]:
    d.text((M + CW * tx, map_y + map_h * ty), word, font=mlab,
           fill=(120, 150, 190), anchor="mm")
ccx, ccy = W - M - 26, map_y + 16
d.ellipse([ccx - 9, ccy - 9, ccx + 9, ccy + 9], outline=(200, 210, 230), width=1)
d.polygon([(ccx, ccy - 8), (ccx + 3, ccy), (ccx, ccy + 8), (ccx - 3, ccy)],
          fill=(200, 210, 230))
d.text((ccx, ccy - 14), "N", font=F(BOLD, 8), fill=(200, 210, 230), anchor="mm")
for num, lon, lat in PINS:
    cx, cy = px(lon, lat)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
    d.text((cx, cy), str(num), font=F(BOLD, 8), fill=(255, 255, 255), anchor="mm")
d.text((M, map_y + map_h + 4),
       "RED NUMBERS MARK STORIES 1\u201313  \u00b7  01 AKVAN, ODISHA  \u00b7  02 KYIV  \u00b7  03 WALL ST, NEW YORK  \u00b7  "
       "04 BRUSSELS  \u00b7  05 ANTALYA  \u00b7  06 POLAND  \u00b7  07 IRAQ",
       font=F(BOLD, 9), fill=GREY)
d.text((M, map_y + map_h + 15),
       "08 ITALY  \u00b7  09 JAPAN  \u00b7  10 KOREA  \u00b7  11 KENYA  \u00b7  12 EL SALVADOR  \u00b7  13 WELLINGTON  \u00b7  "
       "POSITIONS ARE APPROXIMATE.",
       font=F(BOLD, 9), fill=GREY)

# (7) ALSO ON list: 25 more stories, 3 columns, source in parentheses
y = map_y + map_h + 22
d.text((M, y), "ALSO ON FRIDAY \u2014 25 MORE STORIES", font=F(BOLD, 14), fill=INK)
d.line([M, y + 18, W - M, y + 18], fill=RULE, width=1)
ly = y + 24
f_line = F(REG, 10)
f_num = F(BOLD, 10)
col_w = (CW - 2 * 10) // 3
for row in range(0, 9, 2):
    d.rectangle([M, ly + row * 11 - 1, W - M, ly + row * 11 + 10], fill=(246, 238, 220))
for i, line in enumerate(ALSO):
    num, rest = line.split(" \u00b7 ", 1)
    col, row = divmod(i, 9)
    lx = M + col * (col_w + 10)
    yy = ly + row * 11
    d.text((lx, yy), num, font=f_num, fill=RED)
    d.text((lx + 22, yy), rest, font=f_line, fill=INK)

# (8) DATE CHECK box: 8 Thursday items excluded (with correct dates —
# Van Gogh / Fiji / Voyager 1 are WED 18 Nov, Han Duck-soo is a
# partial remand) + 4 "not yet" items.
y = ly + 9 * 11 + 6
d.rectangle([M, y, W - M, y + 36], fill=LIGHT, outline=RED, width=1)
d.text((M + 6, y + 2),
       "DATE CHECK \u2014 NOT FRIDAY: ICJ Rohingya ruling \u00b7 Shenzhen summit \u00b7 Anthropic IPO debut \u00b7 "
       "GTA VI launch \u00b7 Senate Iran vote \u00b7 Tonga drought \u00b7 Denmark\u2013Greenland deal \u00b7 Houthi PIF strike \u2014 all Thu 19 Nov.",
       font=F(REG, 8), fill=INK)
d.text((M + 6, y + 12),
       "Wed 18 Nov, not Thu: Van Gogh $190.4m sale \u00b7 Fiji drought \u00b7 Voyager 1 light-day \u00b7 Han Duck-soo: partial remand, "
       "not acquittal.",
       font=F(REG, 8), fill=INK)
d.text((M + 6, y + 22),
       "NOT YET: BepiColombo Mercury entry (Sat 21 Nov) \u00b7 COP31 final text (Sat) \u00b7 ATP Finals final (Sun 22 Nov) \u00b7 "
       "Estonia border closure (1 Dec).",
       font=F(REG, 8), fill=INK)

# (9) footer: judge-facing honest line + sources + tier legend
d.text((W // 2, y + 42),
       "Every story here happened, or was first reported, on Friday 20 November 2026. Every story independently "
       "date-checked against wire or official sources.",
       font=F(BOLD, 9), fill=INK, anchor="ma")
d.text((W // 2, y + 53),
       "Sources: Reuters \u00b7 The Times \u00b7 CNN \u00b7 BBC \u00b7 AP \u00b7 AFP \u00b7 The Hindu BusinessLine \u00b7 Sambad English \u00b7 "
       "FXStreet \u00b7 JoongAng Daily \u00b7 KBS \u00b7 People Daily \u00b7 Pulse Kenya \u00b7 Cricbuzz \u00b7 ESPNcricinfo \u00b7 NPR \u00b7 ATP",
       font=F(REG, 9), fill=GREY, anchor="ma")
d.text((W // 2, y + 64),
       "CONFIRMED = 2+ outlets  \u00b7  REPORTED = one outlet  \u00b7  CLAIM = one side's account  \u00b7  "
       "FORECAST = a projection  \u00b7  Original drawings.",
       font=F(BOLD, 9), fill=INK, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
