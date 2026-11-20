#!/usr/bin/env python3
"""Draw the World News front page for Friday 20 November 2026.

Pure PIL, no network, fully deterministic. Writes entry.png (1024x1024)
next to this file.
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_BLACK = font("NotoSans-Black.ttf", 88)
F_DATE = font("NotoSans-Bold.ttf", 36)
F_KICKER = font("NotoSans-Bold.ttf", 20)
F_LEAD_HEAD = font("NotoSans-Black.ttf", 40)
F_LEAD_CAP = font("NotoSans-Regular.ttf", 23)
F_HEAD = font("NotoSans-Bold.ttf", 22)
F_CAP = font("NotoSans-Regular.ttf", 15)
F_TAG = font("NotoSans-Bold.ttf", 15)
F_FOOT = font("NotoSans-Regular.ttf", 15)

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
def icon_cyclone(d, x, y, s):
    # spiral storm: concentric arcs + rain slashes
    cx, cy = x + s // 2, y + s // 2
    for r in (s // 2 - 4, s // 3, s // 5):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300, fill=NAVY, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    for dx in (-s // 3, 0, s // 3):
        d.line([x + s // 2 + dx, y + s - 14, x + s // 2 + dx - 6, y + s - 2],
               fill=NAVY, width=4)


def icon_scales(d, x, y, s):
    # scales of justice
    cx = x + s // 2
    d.line([cx, y + 8, cx, y + s - 18], fill=NAVY, width=5)
    d.line([x + 8, y + 18, x + s - 8, y + 18], fill=NAVY, width=5)
    d.arc([x + 2, y + 16, x + s // 3 + 6, y + s - 6], start=0, end=180,
          fill=NAVY, width=4)
    d.arc([x + 2 * s // 3 - 6, y + 16, x + s - 2, y + s - 6], start=0, end=180,
          fill=NAVY, width=4)
    d.ellipse([cx - 5, y + 4, cx + 5, y + 14], fill=RED)


def icon_globe(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    r = s // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=5)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=TEAL, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=TEAL, width=3)
    d.line([cx - r + 8, cy - r // 2, cx + r - 8, cy - r // 2], fill=TEAL, width=2)
    d.line([cx - r + 8, cy + r // 2, cx + r - 8, cy + r // 2], fill=TEAL, width=2)
    # ten small stars around the globe for ASEAN
    import math
    for k in range(10):
        a = math.pi * 2 * k / 10 - math.pi / 2
        sx = cx + int((r + 12) * math.cos(a))
        sy = cy + int((r + 12) * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)


def icon_shield(d, x, y, s):
    pts = [(x + s // 2, y + 4), (x + s - 6, y + 16), (x + s - 6, y + s // 2),
           (x + s // 2, y + s - 6), (x + 6, y + s // 2), (x + 6, y + 16)]
    d.polygon(pts, outline=NAVY, width=5)
    d.line([x + s // 2, y + 22, x + s // 2, y + s - 22], fill=RED, width=4)
    d.line([x + 18, y + s // 2, x + s - 18, y + s // 2], fill=RED, width=4)


def icon_city(d, x, y, s):
    # skyline + a game controller below
    base = y + s - 26
    heights = [0.55, 0.85, 0.45, 0.95, 0.65, 0.8, 0.5]
    bw = s // 7
    for i, h in enumerate(heights):
        top = base - int((s - 40) * h)
        d.rectangle([x + i * bw + 2, top, x + (i + 1) * bw - 2, base],
                    fill=NAVY)
        d.rectangle([x + i * bw + 5, top + 6, x + (i + 1) * bw - 5, top + 12],
                    fill=GOLD)
    d.ellipse([x + s - 22, y + 2, x + s - 8, y + 16], fill=RED)


def icon_cricket(d, x, y, s):
    # stumps + bat + ball
    for dx in (-14, 0, 14):
        d.line([x + s // 2 + dx, y + 12, x + s // 2 + dx, y + s - 30],
               fill=GOLD, width=6)
    d.line([x + s // 2 - 20, y + 12, x + s // 2 + 20, y + 12], fill=GOLD, width=5)
    d.line([x + 14, y + s - 8, x + s // 2 - 6, y + s // 2 + 6], fill=NAVY, width=9)
    d.ellipse([x + s - 26, y + 8, x + s - 8, y + 26], fill=RED)


def icon_cross(d, x, y, s):
    # medical cross over a bat: player ruled out
    d.rectangle([x + s // 2 - 10, y + 8, x + s // 2 + 10, y + s - 8], fill=RED)
    d.rectangle([x + 10, y + s // 2 - 10, x + s - 10, y + s // 2 + 10], fill=RED)
    d.line([x + 6, y + s - 6, x + s - 6, y + 6], fill=NAVY, width=4)


def icon_chess(d, x, y, s):
    # king piece
    cx = x + s // 2
    d.line([cx - 16, y + 10, cx + 16, y + 10], fill=NAVY, width=5)
    d.line([cx, y + 2, cx, y + 20], fill=NAVY, width=5)
    d.ellipse([cx - 16, y + 20, cx + 16, y + 52], fill=NAVY)
    d.polygon([(cx - 22, y + s - 6), (cx + 22, y + s - 6),
               (cx + 12, y + 52), (cx - 12, y + 52)], fill=NAVY)
    d.line([x + s - 22, y + 8, x + s - 4, y + 26], fill=RED, width=5)
    d.line([x + s - 4, y + 8, x + s - 22, y + 26], fill=RED, width=5)


def icon_flag56(d, x, y, s):
    # Oman flag stripes + 56 emblem
    d.rectangle([x + 6, y + 8, x + s - 6, y + s - 8], outline=NAVY, width=3)
    d.rectangle([x + 9, y + 11, x + s - 9, y + s // 3], fill=(0, 122, 61))
    d.rectangle([x + 9, y + s // 3, x + s - 9, y + 2 * s // 3], fill=RED)
    d.rectangle([x + 9, y + 2 * s // 3, x + s - 9, y + s - 11], fill=(0, 122, 61))
    d.rectangle([x + 9, y + 11, x + 30, y + s - 11], fill=(255, 255, 255))
    d.text((x + s // 2 - 4, y + s // 2 - 14), "56", font=font("NotoSans-Black.ttf", 30),
           fill=(255, 255, 255))


def icon_whitehouse(d, x, y, s):
    # columned building + clock
    base = y + s - 8
    d.rectangle([x + 8, base - 14, x + s - 8, base], fill=NAVY)
    for i in range(5):
        cx = x + 22 + i * (s - 44) // 4
        d.rectangle([cx - 6, base - 70, cx + 6, base - 14], fill=NAVY)
    d.polygon([(x + 4, base - 70), (x + s // 2, base - 100), (x + s - 4, base - 70)],
              fill=NAVY)
    d.ellipse([x + s - 52, y + 6, x + s - 12, y + 46], outline=RED, width=5)
    d.line([x + s - 32, y + 26, x + s - 32, y + 12], fill=RED, width=4)
    d.line([x + s - 32, y + 26, x + s - 18, y + 30], fill=RED, width=4)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- masthead
    title = "WORLD NEWS"
    tw = d.textlength(title, font=F_BLACK)
    d.text(((W - tw) / 2, 6), title, font=F_BLACK, fill=INK)
    d.rectangle([M, 108, W - M, 114], fill=RED)
    date = "FRIDAY 20 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 122), date, font=F_DATE, fill=RED)
    kicker = "THE DAY IN TEN STORIES  •  POLITICS  •  WEATHER  •  SPORT  •  CULTURE"
    kw = d.textlength(kicker, font=F_KICKER)
    d.text(((W - kw) / 2, 168), kicker, font=F_KICKER, fill=GREY)
    d.line([M, 196, W - M, 196], fill=INK, width=2)

    # ---- lead story: Trump / Iran
    ly = 210
    d.rectangle([M, ly, W - M, ly + 200], fill=CELL_BG, outline=LINE, width=2)
    icon_whitehouse(d, M + 18, ly + 14, 176)
    tx = M + 216
    d.text((tx, ly + 14), "TOP STORY", font=F_TAG, fill=RED)
    head = wrap(d, "TRUMP DELAYS IRAN DECISION", F_LEAD_HEAD, W - M - tx - 18)
    y = draw_lines(d, head, tx, ly + 38, F_LEAD_HEAD, INK, 46)
    cap = wrap(d, "No rush on war, he says \u2014 he will \u201csee what happens\u201d "
                  "after 1 January and decide in 2027.", F_LEAD_CAP, W - M - tx - 18)
    draw_lines(d, cap, tx, y + 8, F_LEAD_CAP, INK, 30)

    # ---- grid of 9 stories
    stories = [
        ("CYCLONE AKVAN HITS ODISHA",
         "300,000 evacuated as the storm hits the coast.",
         icon_cyclone, "WEATHER"),
        ("JUSTICE VARMA'S LETTER",
         "Resignation is no admission of guilt, he says.",
         icon_scales, "INDIA"),
        ("ASEAN SUMMIT CLOSES",
         "Digital trade deal sealed; sea code still unresolved.",
         icon_globe, "ASIA"),
        ("HAITI TROOP DEAL",
         "Salvadoran troops approved as gang strikes widen.",
         icon_shield, "AMERICAS"),
        ("GTA VI'S NPCs",
         "The crowd that makes the game's huge world feel real.",
         icon_city, "CULTURE"),
        ("INDIA v NZ, DAY 2",
         "Nicholls' unbeaten 113 builds New Zealand's lead.",
         icon_cricket, "CRICKET"),
        ("BAVUMA RULED OUT",
         "Proteas captain misses the Bangladesh series decider.",
         icon_cross, "CRICKET"),
        ("CARLSEN FORFEIT",
         "Shock walkout leaves the chess world fuming.",
         icon_chess, "CHESS"),
        ("OMAN NATIONAL DAY",
         "The Sultanate marks 56 years of independence.",
         icon_flag56, "GULF"),
    ]
    gy = 422
    cw = (W - 2 * M - 24) // 3
    ch = 182
    for i, (headline, caption, icon, tag) in enumerate(stories):
        r, c = divmod(i, 3)
        x0 = M + c * (cw + 12)
        y0 = gy + r * (ch + 12)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CELL_BG, outline=LINE, width=2)
        d.text((x0 + 14, y0 + 10), tag, font=F_TAG, fill=RED)
        icon(d, x0 + cw - 96, y0 + 8, 84)
        hl = wrap(d, headline, F_HEAD, cw - 28)
        y = draw_lines(d, hl, x0 + 14, y0 + 88, F_HEAD, INK, 26)
        cp = wrap(d, caption, F_CAP, cw - 28)
        draw_lines(d, cp, x0 + 14, y + 4, F_CAP, GREY, 19)

    # ---- footer
    d.line([M, 998, W - M, 998], fill=INK, width=2)
    foot = "WORLD NEWS \u2022 FRIDAY 20 NOVEMBER 2026 \u2022 TEN STORIES, ONE DAY"
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 1002), foot, font=F_FOOT, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
