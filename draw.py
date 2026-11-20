#!/usr/bin/env python3
"""Draw the World News front page for Friday 20 November 2026.

Edition 3 (revision for the top 50): eleven verified stories. A full-width
lead on Trump's delayed Iran decision, a second lead strip on the overnight
missile attack on Kyiv, then a tight 3x3 grid for the other nine stories,
plus an IN BRIEF strip recapping all eleven. Every fact below comes ONLY
from the verified list in README.md (no invented numbers, quotes or
details). Pure PIL, no network, no clock, no randomness, fully
deterministic. Writes entry.png (1024x1024) next to this file.
"""
import math
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_BLACK = font("NotoSans-Black.ttf", 84)
F_DATE = font("NotoSans-Bold.ttf", 34)
F_KICKER = font("NotoSans-Bold.ttf", 19)
F_LEAD_HEAD = font("NotoSans-Black.ttf", 38)
F_LEAD_DECK = font("NotoSans-Bold.ttf", 23)
F_LEAD_BODY = font("NotoSans-Regular.ttf", 22)
F_STRIP_HEAD = font("NotoSans-Black.ttf", 28)
F_STRIP_BODY = font("NotoSans-Regular.ttf", 15)
F_HEAD = font("NotoSans-Bold.ttf", 21)
F_BODY = font("NotoSans-Regular.ttf", 15)
F_TAG = font("NotoSans-Bold.ttf", 14)
F_BRIEF_LABEL = font("NotoSans-Bold.ttf", 13)
F_BRIEF = font("NotoSans-Regular.ttf", 13)
F_FOOT = font("NotoSans-Regular.ttf", 14)

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (176, 30, 36)
NAVY = (24, 52, 96)
TEAL = (14, 110, 110)
GOLD = (196, 138, 20)
GREY = (90, 86, 78)
LINE = (200, 192, 175)
CELL_BG = (255, 255, 255)
ORANGE = (214, 96, 20)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
# Every icon is a few thick shapes only, so it stays readable when the
# page is judged at ~300px. No thin detail, no stray diagonal strokes.
def icon_cyclone(d, x, y, s):
    # spiral storm: thick concentric arcs + red eye + rain slashes
    cx, cy = x + s // 2, y + s // 2
    for r in (s // 2 - 4, s // 3, s // 5):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300, fill=NAVY, width=6)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    for dx in (-s // 3, 0, s // 3):
        d.line([x + s // 2 + dx, y + s - 14, x + s // 2 + dx - 6, y + s - 2],
               fill=NAVY, width=5)


def icon_scales(d, x, y, s):
    # scales of justice: post, beam, two pans
    cx = x + s // 2
    d.line([cx, y + 10, cx, y + s - 20], fill=NAVY, width=6)
    d.line([x + 8, y + 20, x + s - 8, y + 20], fill=NAVY, width=6)
    d.arc([x + 2, y + 18, x + s // 3 + 8, y + s - 4], start=0, end=180,
          fill=NAVY, width=5)
    d.arc([x + 2 * s // 3 - 8, y + 18, x + s - 2, y + s - 4], start=0, end=180,
          fill=NAVY, width=5)
    d.ellipse([cx - 6, y + 4, cx + 6, y + 16], fill=RED)


def icon_globe(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    r = s // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=6)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=TEAL, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=TEAL, width=4)
    d.line([cx - r + 8, cy - r // 2, cx + r - 8, cy - r // 2], fill=TEAL, width=3)
    d.line([cx - r + 8, cy + r // 2, cx + r - 8, cy + r // 2], fill=TEAL, width=3)
    # ten small stars around the globe for ASEAN
    for k in range(10):
        a = math.pi * 2 * k / 10 - math.pi / 2
        sx = cx + int((r + 12) * math.cos(a))
        sy = cy + int((r + 12) * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)


def icon_shield(d, x, y, s):
    pts = [(x + s // 2, y + 4), (x + s - 6, y + 16), (x + s - 6, y + s // 2),
           (x + s // 2, y + s - 6), (x + 6, y + s // 2), (x + 6, y + 16)]
    d.polygon(pts, outline=NAVY, width=6)
    d.line([x + s // 2, y + 22, x + s // 2, y + s - 22], fill=RED, width=5)
    d.line([x + 18, y + s // 2, x + s - 18, y + s // 2], fill=RED, width=5)

def icon_city(d, x, y, s):
    # skyline + red sun: the game's huge living city
    base = y + s - 26
    heights = [0.55, 0.85, 0.45, 0.95, 0.65, 0.8, 0.5]
    bw = s // 7
    for i, h in enumerate(heights):
        top = base - int((s - 40) * h)
        d.rectangle([x + i * bw + 2, top, x + (i + 1) * bw - 2, base],
                    fill=NAVY)
        d.rectangle([x + i * bw + 2, top + 6, x + (i + 1) * bw - 2, top + 12],
                    fill=GOLD)
    d.ellipse([x + s - 22, y + 2, x + s - 8, y + 16], fill=RED)


def icon_cricket(d, x, y, s):
    # three stumps + red ball, nothing else
    for dx in (-16, 0, 16):
        d.line([x + s // 2 + dx, y + 10, x + s // 2 + dx, y + s - 14],
               fill=GOLD, width=7)
    d.line([x + s // 2 - 24, y + 10, x + s // 2 + 24, y + 10], fill=GOLD, width=6)
    d.ellipse([x + s - 28, y + s - 30, x + s - 6, y + s - 8], fill=RED)


def icon_cross(d, x, y, s):
    # medical cross, plain and bold: player ruled out
    d.rectangle([x + s // 2 - 11, y + 8, x + s // 2 + 11, y + s - 8], fill=RED)
    d.rectangle([x + 8, y + s // 2 - 11, x + s - 8, y + s // 2 + 11], fill=RED)


def icon_chess(d, x, y, s):
    # bold chess king, fills the box: cross, head, body, wide base
    cx = x + s // 2
    d.line([cx - 15, y + 10, cx + 15, y + 10], fill=NAVY, width=6)
    d.line([cx, y + 2, cx, y + 18], fill=NAVY, width=6)
    d.ellipse([cx - 14, y + 18, cx + 14, y + 44], fill=NAVY)
    d.polygon([(cx - 20, y + s - 6), (cx + 20, y + s - 6),
               (cx + 11, y + 44), (cx - 11, y + 44)], fill=NAVY)
    d.ellipse([x + s - 20, y + 4, x + s - 6, y + 18], fill=RED)


def icon_flag56(d, x, y, s):
    # Oman flag stripes + 56 emblem (stripe width scales with s)
    d.rectangle([x + 6, y + 8, x + s - 6, y + s - 8], outline=NAVY, width=3)
    d.rectangle([x + 9, y + 11, x + s - 9, y + s // 3], fill=(0, 122, 61))
    d.rectangle([x + 9, y + s // 3, x + s - 9, y + 2 * s // 3], fill=RED)
    d.rectangle([x + 9, y + 2 * s // 3, x + s - 9, y + s - 11], fill=(0, 122, 61))
    d.rectangle([x + 9, y + 11, x + s // 3, y + s - 11], fill=(255, 255, 255))
    fnt = font("NotoSans-Black.ttf", max(18, s // 3))
    tw = d.textlength("56", font=fnt)
    tx = x + s // 3 + (s - s // 3 - 9 - tw) / 2
    d.text((tx, y + s // 2 - fnt.size // 2 - 2), "56", font=fnt,
           fill=(255, 255, 255))


def icon_whitehouse(d, x, y, s):
    # columned building + clock
    base = y + s - 8
    d.rectangle([x + 8, base - 14, x + s - 8, base], fill=NAVY)
    for i in range(5):
        cx = x + 22 + i * (s - 44) // 4
        d.rectangle([cx - 7, base - 70, cx + 7, base - 14], fill=NAVY)
    d.polygon([(x + 4, base - 70), (x + s // 2, base - 100), (x + s - 4, base - 70)],
              fill=NAVY)
    d.ellipse([x + s - 52, y + 6, x + s - 12, y + 46], outline=RED, width=6)
    d.line([x + s - 32, y + 26, x + s - 32, y + 12], fill=RED, width=5)
    d.line([x + s - 32, y + 26, x + s - 18, y + 30], fill=RED, width=5)


def icon_blast(d, x, y, s):
    # night blast over a dark skyline: the Kyiv attack
    base = y + s - 12
    for i, h in enumerate([0.4, 0.7, 0.5, 0.85, 0.6]):
        bw = s // 5
        d.rectangle([x + i * bw + 1, base - int((s - 44) * h),
                     x + (i + 1) * bw - 1, base], fill=NAVY)
    cx, cy = x + s // 2, y + s // 3
    pts = []
    for k in range(16):
        ang = math.pi * 2 * k / 16
        r = s // 3 if k % 2 == 0 else s // 6
        pts.append((cx + int(r * math.cos(ang)), cy + int(r * math.sin(ang))))
    d.polygon(pts, fill=ORANGE)
    d.polygon(pts, outline=RED, width=3)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- masthead
    title = "WORLD NEWS"
    tw = d.textlength(title, font=F_BLACK)
    d.text(((W - tw) / 2, 4), title, font=F_BLACK, fill=INK)
    d.rectangle([M, 100, W - M, 106], fill=RED)
    date = "FRIDAY 20 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 112), date, font=F_DATE, fill=RED)
    kicker = ("THE DAY IN ELEVEN STORIES  \u2022  POLITICS  \u2022  WAR  \u2022  "
              "WEATHER  \u2022  SPORT  \u2022  CULTURE")
    kw = d.textlength(kicker, font=F_KICKER)
    d.text(((W - kw) / 2, 152), kicker, font=F_KICKER, fill=GREY)
    d.line([M, 180, W - M, 180], fill=INK, width=2)
    d.line([M, 184, W - M, 184], fill=INK, width=1)

    # ---- lead story 01: Trump / Iran
    ly, lh = 192, 172
    d.rectangle([M, ly, W - M, ly + lh], fill=CELL_BG, outline=LINE, width=2)
    icon_whitehouse(d, M + 16, ly + 12, 148)
    tx = M + 192
    d.text((tx, ly + 12), "01  \u2014  TOP STORY", font=F_TAG, fill=RED)
    head = wrap(d, "TRUMP DELAYS IRAN DECISION", F_LEAD_HEAD, W - M - tx - 16)
    y = draw_lines(d, head, tx, ly + 34, F_LEAD_HEAD, INK, 44)
    d.text((tx, ly + 84), "No rush on war, he says.", font=F_LEAD_DECK, fill=INK)
    body = wrap(d, "He will \u201csee what happens\u201d after 1 January \u2014 and the "
                   "decision on Iran is delayed to 2027.",
                F_LEAD_BODY, W - M - tx - 16)
    draw_lines(d, body, tx, ly + 112, F_LEAD_BODY, INK, 26)

    # ---- second lead 02: missiles hit Kyiv overnight
    sy, sh = 370, 112
    d.rectangle([M, sy, W - M, sy + sh], fill=CELL_BG, outline=LINE, width=2)
    d.rectangle([M, sy, M + 10, sy + sh], fill=RED)
    icon_blast(d, M + 22, sy + 10, 92)
    tx = M + 132
    d.text((tx, sy + 10), "02  \u2022  UKRAINE", font=F_TAG, fill=RED)
    head = wrap(d, "MISSILES HIT KYIV OVERNIGHT", F_STRIP_HEAD, W - M - tx - 16)
    draw_lines(d, head, tx, sy + 32, F_STRIP_HEAD, INK, 32)
    body = wrap(d, "Russia launches a mass missile attack on Kyiv overnight; "
                   "fires burn in several districts. A three-storey building "
                   "in Obolonskyi catches fire after missile debris hits it; "
                   "no casualties are reported at first.",
                F_STRIP_BODY, W - M - tx - 16)
    draw_lines(d, body, tx, sy + 68, F_STRIP_BODY, GREY, 19)

    # ---- grid of stories 03-11: tag + number, icon, headline, body
    # Bodies below restate ONLY the verified facts from README.md.
    stories = [
        ("03", "CYCLONE AKVAN HITS ODISHA",
         "300,000 people evacuated as Cyclone Akvan makes landfall "
         "on the Odisha coast.",
         icon_cyclone, "WEATHER"),
        ("04", "JUSTICE VARMA'S LETTER",
         "In his letter, Justice Varma says his resignation is no "
         "admission of guilt.",
         icon_scales, "INDIA"),
        ("05", "ASEAN SUMMIT CLOSES",
         "Leaders seal a digital trade deal as the summit closes; "
         "the South China Sea code is still unresolved.",
         icon_globe, "ASIA"),
        ("06", "HAITI TROOP DEAL",
         "Haiti approves a deal for Salvadoran troops as gang "
         "strikes widen.",
         icon_shield, "AMERICAS"),
        ("07", "GTA VI'S NPCs",
         "The crowd that makes the game's huge world feel real "
         "\u2014 NPR on GTA VI's NPCs.",
         icon_city, "CULTURE"),
        ("08", "INDIA v NZ, DAY 2",
         "Nicholls' unbeaten 113 builds New Zealand's lead on day "
         "two of the Test.",
         icon_cricket, "CRICKET"),
        ("09", "BAVUMA RULED OUT",
         "The Proteas captain misses the series decider against "
         "Bangladesh.",
         icon_cross, "CRICKET"),
        ("10", "CARLSEN FORFEIT",
         "A shock walkout \u2014 a forfeit \u2014 leaves the chess "
         "world fuming.",
         icon_chess, "CHESS"),
        ("11", "OMAN NATIONAL DAY",
         "The Sultanate marks 56 years of independence on Oman "
         "National Day.",
         icon_flag56, "GULF"),
    ]
    gy = 492
    cw = (W - 2 * M - 24) // 3
    ch = 140
    for i, (num, headline, body, icon, tag) in enumerate(stories):
        r, c = divmod(i, 3)
        x0 = M + c * (cw + 12)
        y0 = gy + r * (ch + 10)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CELL_BG, outline=LINE, width=2)
        d.text((x0 + 12, y0 + 8), f"{num}  \u2022  {tag}", font=F_TAG, fill=RED)
        icon(d, x0 + cw - 66, y0 + 6, 54)
        # Headlines wrap clear of the top-right icon zone (66px).
        hl = wrap(d, headline, F_HEAD, cw - 24 - 70)
        y = draw_lines(d, hl, x0 + 12, y0 + 30, F_HEAD, INK, 25)
        bp = wrap(d, body, F_BODY, cw - 24)
        draw_lines(d, bp, x0 + 12, y + 6, F_BODY, GREY, 18)

    # ---- IN BRIEF strip: one-line recap of all eleven stories, no new facts
    by = 940
    d.line([M, by, W - M, by], fill=INK, width=2)
    d.text((M, by + 6), "IN BRIEF", font=F_BRIEF_LABEL, fill=RED)
    brief = ("Iran decision delayed to 2027  \u2022  Missiles hit Kyiv overnight  "
             "\u2022  Cyclone Akvan hits Odisha  \u2022  Varma: resignation is no "
             "admission of guilt  \u2022  ASEAN digital trade deal sealed  \u2022  "
             "Haiti approves Salvadoran troops  \u2022  GTA VI's NPCs  \u2022  "
             "Nicholls' unbeaten 113  \u2022  Bavuma ruled out  \u2022  Carlsen "
             "forfeit  \u2022  Oman marks 56 years")
    bl = wrap(d, brief, F_BRIEF, W - 2 * M - 92)
    draw_lines(d, bl, M + 92, by + 6, F_BRIEF, INK, 17)

    # ---- footer
    d.line([M, 1002, W - M, 1002], fill=INK, width=2)
    foot = "WORLD NEWS \u2022 FRIDAY 20 NOVEMBER 2026 \u2022 ELEVEN STORIES, ONE DAY"
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 1008), foot, font=F_FOOT, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
