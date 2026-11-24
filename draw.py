#!/usr/bin/env python3
"""news-23 b83 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories: 3 heroes + 10 cards + 18 ALSO. Renders entry.png 1024x1024.
Run: python3 draw.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, x, y, s, font, fill, anchor="la"):
    draw.text((x, y), s, font=font, fill=fill, anchor=anchor)


def chip(draw, x, y, label, fill, fg="white", font=None, pad=5, h=13):
    w = int(draw.textlength(label, font=font)) + 2 * pad
    draw.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=fill)
    draw.text((x + pad, y + 1), label, font=font, fill=fg)
    return w


# ---- palette ----
INK = (17, 17, 17)
PAPER = (255, 255, 255)
RED = (178, 34, 34)
DRED = (139, 0, 0)
GOLD = (184, 134, 11)
NAVY = (16, 32, 64)
GREEN = (0, 90, 60)
TEAL = (0, 110, 110)
GREY = (90, 90, 90)
LGREY = (230, 230, 230)
MAPG = (200, 222, 190)
PIN = (178, 34, 34)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ================= MASTHEAD =================
d.rectangle([0, 0, W, 46], fill=INK)
text(d, 10, 2, "THE WORLD TODAY", F(SERIF_B, 38), (255, 255, 255))
text(d, 1014, 12, "MONDAY 23 NOVEMBER 2026", F(SANS_B, 17), (212, 175, 55), anchor="ra")

# ================= KICKER =================
d.rectangle([0, 46, W, 66], fill=RED)
text(d, 512, 50, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
     F(SANS_B, 15), (255, 255, 255), anchor="ma")

# ================= NUMBER STRIP (2 rows x 5) =================
strip = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", (0, 80, 160)),
    ("11,762", "EBOLA CASES, DRC", GREEN), ("10T won", "SEOUL STABILISATION FUND", GOLD),
    ("2%", "BILLIONAIRE TAX IN PARIS", (110, 60, 160)),
    ("$450M", "SKUBAL DEAL", (0, 80, 160)), ("165", "RUSSIAN MISSILES/WEEK", INK),
    ("12,000", "CLEARED IN MANCHESTER", GREEN), ("264 kg", "EXPLOSIVES SEIZED", (110, 60, 160)),
    ("$107.3B", "ANTHROPIC IPO", (110, 60, 160)),
]
cw = W // 5
for i, (val, lab, col) in enumerate(strip):
    r, c = divmod(i, 5)
    x = c * cw + 8
    y = 68 + r * 24
    text(d, x, y, val, F(SANS_B, 19), col)
    text(d, x, y + 17, lab, F(SANS, 8), GREY)
d.line([0, 122, W, 122], fill=INK, width=1)

# ================= REGION BAR =================
regions = [("ASIA-PACIFIC 7", (0, 80, 160)), ("AMERICAS 8", RED), ("MIDDLE EAST 6", GOLD),
           ("EUROPE 5", TEAL), ("AFRICA 3", (90, 90, 90)), ("WORLD 2", INK)]
rx = 0
for name, col in regions:
    seg = W // 6
    d.rectangle([rx, 124, rx + seg - 1, 140], fill=col)
    text(d, rx + seg // 2, 128, name, F(SANS_B, 11), (255, 255, 255), anchor="ma")
    rx += seg

# ================= UTC STRIP =================
d.rectangle([0, 142, W, 158], fill=(245, 245, 240))
text(d, 8, 145, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     F(SANS, 11), INK)
text(d, 1016, 145, "~ APPROX", F(SANS_I, 10), GREY, anchor="ra")

# ================= HEROES =================
# columns: x0=8, x1=352, x2=696 ; col width 320
hero_x = [8, 352, 696]
SCENE_Y, SCENE_H = 162, 104
HEAD_Y = 270          # headline top
BODY_Y = 312          # body top
SRC_Y = 344           # source + chip row (clears strip at 360)
STRIP_Y = 360         # "MORE OF THE DAY" black strip

def scene_kospi(x0):
    d.rectangle([x0, SCENE_Y, x0 + 320, SCENE_Y + SCENE_H], fill=NAVY)
    # lit buildings
    import random
    rnd = random.Random(7)
    for bx in range(x0 + 8, x0 + 312, 26):
        bh = rnd.randint(28, 78)
        by = SCENE_Y + SCENE_H - bh
        d.rectangle([bx, by, bx + 20, SCENE_Y + SCENE_H], fill=(24, 48, 92))
        for wy in range(by + 5, SCENE_Y + SCENE_H - 4, 9):
            for wx in (bx + 3, bx + 11):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill=(255, 214, 90))
    # orange chart line
    pts = [(x0 + 14, SCENE_Y + 84), (x0 + 60, SCENE_Y + 66), (x0 + 110, SCENE_Y + 74),
           (x0 + 160, SCENE_Y + 52), (x0 + 210, SCENE_Y + 58), (x0 + 260, SCENE_Y + 36),
           (x0 + 306, SCENE_Y + 30)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(255, 255, 255))
    text(d, x0 + 8, SCENE_Y + 4, "-3.3%", F(SANS_B, 24), (255, 90, 90))
    d.rectangle([x0, SCENE_Y + SCENE_H - 16, x0 + 320, SCENE_Y + SCENE_H], fill=(0, 0, 0))
    text(d, x0 + 8, SCENE_Y + SCENE_H - 15, "KOSPI 4,708.54  \u00b7  -161 PTS", F(SANS_B, 11), (255, 255, 255))

def scene_guterres(x0):
    d.rectangle([x0, SCENE_Y, x0 + 320, SCENE_Y + SCENE_H], fill=(0, 70, 50))
    # globe
    cx, cy, r = x0 + 252, SCENE_Y + 52, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 220, 190), outline=(255, 255, 255), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(90, 160, 120), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(90, 160, 120), width=1)
    d.arc([cx - r + 8, cy - r + 14, cx + r - 8, cy + r - 14], 200, 340, fill=(90, 160, 120), width=1)
    text(d, x0 + 10, SCENE_Y + 8, "150 DELEGATES", F(SANS_B, 25), (255, 214, 90))
    text(d, x0 + 10, SCENE_Y + 36, "BACK A RISK", F(SANS_B, 25), (255, 214, 90))
    text(d, x0 + 10, SCENE_Y + 64, "FRAMEWORK", F(SANS_B, 25), (255, 214, 90))
    d.rectangle([x0, SCENE_Y + SCENE_H - 16, x0 + 320, SCENE_Y + SCENE_H], fill=(0, 0, 0))
    text(d, x0 + 8, SCENE_Y + SCENE_H - 15, "UN  \u00b7  BRIDGETOWN", F(SANS_B, 11), (255, 255, 255))

def scene_power(x0):
    d.rectangle([x0, SCENE_Y, x0 + 320, SCENE_Y + SCENE_H], fill=(250, 244, 224))
    text(d, x0 + 8, SCENE_Y + 2, "NARROWEST SINCE 2018", F(SANS_B, 10), INK)
    text(d, x0 + 312, SCENE_Y + 2, "GAP 5.3", F(SANS_B, 10), RED, anchor="ra")
    bars = [("US", 78.9, (0, 60, 140)), ("CHINA", 73.6, RED), ("INDIA", 40.5, GOLD)]
    bx = x0 + 30
    for name, val, col in bars:
        bh = int(val * 0.62)
        by = SCENE_Y + SCENE_H - 18 - bh
        text(d, bx + 28, by - 16, f"{val}", F(SANS_B, 15), INK, anchor="ma")
        d.rectangle([bx, by, bx + 56, SCENE_Y + SCENE_H - 18], fill=col)
        # label INSIDE the bar bottom (white), not in the black strip below
        text(d, bx + 28, SCENE_Y + SCENE_H - 32, name, F(SANS_B, 10), (255, 255, 255), anchor="ma")
        bx += 92
    d.rectangle([x0, SCENE_Y + SCENE_H - 16, x0 + 320, SCENE_Y + SCENE_H], fill=(0, 0, 0))
    text(d, x0 + 8, SCENE_Y + SCENE_H - 15, "ASIA POWER INDEX 2026", F(SANS_B, 11), (255, 255, 255))

scene_kospi(hero_x[0])
scene_guterres(hero_x[1])
scene_power(hero_x[2])

heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for x0, (hl, body, src) in zip(hero_x, heroes):
    lines = wrap(d, hl, F(SANS_B, 20), 320)
    y = HEAD_Y
    for ln in lines[:2]:
        text(d, x0, y, ln, F(SANS_B, 20), INK)
        y += 20
    blines = wrap(d, body, F(SANS, 12), 320)
    y = BODY_Y
    for ln in blines[:2]:
        text(d, x0, y, ln, F(SANS, 12), INK)
        y += 14
    text(d, x0, SRC_Y, src, F(SANS, 10), GREY)
    chip(d, x0 + 320 - 62, SRC_Y - 1, "REPORTED", (0, 80, 160), font=F(SANS_B, 9))

# ================= MORE OF THE DAY strip =================
d.rectangle([0, STRIP_Y, W, STRIP_Y + 18], fill=INK)
text(d, 8, STRIP_Y + 2, "MORE OF THE DAY  \u2014  10 STORIES", F(SANS_B, 12), (255, 255, 255))

# ================= 10 CARDS (2 rows x 5) =================
cards = [
    ("AMERICAS", (0, 80, 160), "BESSESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", NAVY, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", GOLD, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", TEAL, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED"),
    ("LEGAL", (110, 60, 160), "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", (0, 80, 160), "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", GOLD, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (110, 60, 160), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
card_w = 200
card_x0 = 8
gap = 4
row_y = [382, 470]
for i, (cat, col, hl, body, src, tag) in enumerate(cards):
    r, c = divmod(i, 5)
    x0 = card_x0 + c * (card_w + gap)
    y0 = row_y[r]
    # category bar
    d.rectangle([x0, y0, x0 + card_w - 4, y0 + 14], fill=col)
    text(d, x0 + 4, y0 + 1, cat, F(SANS_B, 10), (255, 255, 255))
    text(d, x0 + card_w - 8, y0 + 1, str(i + 1), F(SANS_B, 10), (255, 255, 255), anchor="ra")
    # headline (max 2 lines, 15px bold, pitch 16)
    hlines = wrap(d, hl, F(SANS_B, 14), card_w - 8)
    y = y0 + 17
    for ln in hlines[:2]:
        text(d, x0, y, ln, F(SANS_B, 14), INK)
        y += 16
    # body (1 line, 11px)
    text(d, x0, y0 + 51, body, F(SANS, 11), INK)
    # source + chip row at fixed y, clear of body
    text(d, x0, y0 + 68, src, F(SANS, 10), GREY)
    chip_col = RED if tag == "CLAIM" else (0, 80, 160)
    chip(d, x0 + card_w - 66, y0 + 67, tag, chip_col, font=F(SANS_B, 9))

# ================= MAP + ALSO =================
MAP_Y, MAP_H = 580, 244
ALSO_Y = 580
d.rectangle([0, 560, W, 560 + 18], fill=INK)
text(d, 8, 562, "WHERE IT HAPPENED", F(SANS_B, 12), (255, 255, 255))
text(d, 340, 562, "ALSO ON MONDAY", F(SANS_B, 12), (255, 255, 255))

# map box
d.rectangle([8, MAP_Y, 328, MAP_Y + MAP_H], outline=INK, width=1, fill=(255, 255, 255))
# stylised continents (light green blobs)
d.polygon([(30, 600), (70, 580), (120, 585), (150, 610), (140, 660), (110, 700), (70, 710), (40, 680), (20, 640)], fill=MAPG)   # N America
d.polygon([(120, 720), (150, 715), (165, 745), (150, 780), (125, 770), (115, 740)], fill=MAPG)  # S America
d.polygon([(180, 600), (230, 580), (290, 590), (310, 620), (280, 660), (220, 665), (190, 640)], fill=MAPG)  # Eurasia
d.polygon([(190, 690), (220, 680), (240, 700), (225, 730), (195, 725)], fill=MAPG)  # Africa
d.polygon([(270, 760), (300, 750), (315, 770), (295, 790), (272, 782)], fill=MAPG)  # Oceania
pins = [(60, 640, 1), (95, 700, 2), (250, 600, 3), (70, 660, 4), (150, 620, 5),
        (225, 605, 6), (90, 680, 7), (45, 690, 8), (60, 715, 9), (80, 730, 10),
        (205, 595, 11), (185, 615, 12), (265, 590, 13)]
# spread pins so none overlap the legend (legend lives at bottom of box)
for px, py, n in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=PIN, outline=(255, 255, 255), width=1)
    text(d, px, py - 6, str(n), F(SANS_B, 10), (255, 255, 255), anchor="ma")
text(d, 14, MAP_Y + MAP_H - 34, "Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", F(SANS, 9), INK)
text(d, 14, MAP_Y + MAP_H - 23, "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", F(SANS, 9), INK)
text(d, 14, MAP_Y + MAP_H - 12, "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", F(SANS, 9), INK)

# ALSO list (18 items, single column, pitch 13)
also = [
    (14, "Paris: 100+ back 2% billionaire tax", False),
    (15, "Manchester: 12,000 cleared", False),
    (16, "Zelenskyy: 165 missiles in a week", False),
    (17, "COP31: the day after pact rejected", False),
    (18, "Benghazi: UN demands probe of port attacks", True),
    (19, "Israel unity talks resume", False),
    (20, "Gaza: two killed in Israeli strike", False),
    (21, "West Bank settler attacks", False),
    (22, "Iran war: no deal in sight", False),
    (23, "Lebanon seizes 264 kg explosives", False),
    (24, "Bahrain: strike hits plant, 2 hurt", False),
    (25, "Sudan: defences down drones", True),
    (26, "DRC: fighting traps Ebola teams", False),
    (27, "Bangladesh: Hasina jailed if she returns", False),
    (28, "Seoul minister quits in exam row", False),
    (29, "SK Telecom -7.3% as hype cools", False),
    (30, "China eases margin rules", False),
    (31, "Seoul readies 10T-won fund", False),
]
y = ALSO_Y + 6
for n, item, is_claim in also:
    text(d, 340, y, f"{n}. {item}", F(SANS, 12), INK)
    if is_claim:
        tw = d.textlength(f"{n}. {item}", font=F(SANS, 12))
        text(d, 340 + tw + 4, y, "[CLAIM]", F(SANS_B, 11), RED)
    y += 13

# ================= DATE CHECK =================
DC_Y = 836
d.rectangle([8, DC_Y, 1016, DC_Y + 62], outline=RED, width=2, fill=(255, 245, 245))
text(d, 16, DC_Y + 4, "DATE CHECK", F(SANS_B, 13), RED)
text(d, 1010, DC_Y + 4, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", F(SANS_B, 10), RED, anchor="ra")
text(d, 16, DC_Y + 22, "LEFT OUT \u2014 NOT 23 NOV: Dems 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo (22 Nov) \u00b7 EU-Indonesia (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar (19 Nov)",
     F(SANS, 11), INK)
text(d, 16, DC_Y + 40, "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
     F(SANS, 11), INK)

# ================= FOOTER =================
text(d, 8, 910, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
     F(SANS, 11), GREY)
text(d, 8, 926, "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.",
     F(SANS, 11), GREY)
text(d, 8, 942, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
     F(SANS, 11), GREY)
d.line([8, 962, 1016, 962], fill=GOLD, width=2)
text(d, 512, 972, "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
     F(SANS_B, 13), GOLD, anchor="ma")

img.save(os.path.join(HERE, "entry.png"), optimize=True)
print("saved entry.png", os.path.getsize(os.path.join(HERE, "entry.png")), "bytes")
