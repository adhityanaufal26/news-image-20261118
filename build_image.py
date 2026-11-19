#!/usr/bin/env python3
"""Draw the 18 November 2026 front page: 'THE WORLD TODAY'.

Fresh build for make.fun news-image-20261118. Pillow only.
Writes entry.png (1024x1024) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

INK = (20, 20, 20)
PAPER = (250, 246, 235)
RED = (178, 34, 34)
NAVY = (20, 38, 63)
AMBER = (255, 190, 80)
GREY = (90, 90, 90)
RULE = (120, 110, 95)
SEA = (198, 222, 236)
LAND = (232, 220, 188)
LAND_EDGE = (150, 135, 95)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, max_w, leading, color=INK):
    for ln in wrap(d, text, f, max_w):
        d.text((x, y), ln, font=f, fill=color)
        y += leading
    return y


def rule(d, x, y, w, color=RULE, width=1):
    d.line([(x, y), (x + w, y)], fill=color, width=width)


# ---------------------------------------------------------------- continents
# Simplified hand-drawn polygons, (lon, lat). Equirectangular projection.
NORTH_AMERICA = [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60),
                 (-135, 58), (-130, 54), (-125, 49), (-124, 42), (-120, 34),
                 (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
                 (-90, 14), (-86, 12), (-83, 9), (-80, 8), (-79, 9), (-81, 13),
                 (-83, 15), (-87, 16), (-88, 18), (-90, 21), (-91, 19),
                 (-95, 19), (-97, 22), (-97, 26), (-93, 30), (-89, 30),
                 (-84, 30), (-81, 26), (-80, 32), (-76, 35), (-74, 40),
                 (-70, 42), (-68, 45), (-65, 44), (-60, 47), (-55, 52),
                 (-60, 55), (-65, 60), (-68, 58), (-72, 62), (-78, 62),
                 (-85, 66), (-90, 69), (-95, 69), (-110, 68), (-125, 70),
                 (-140, 70), (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68), (-22, 70),
             (-20, 74), (-25, 76), (-35, 77), (-50, 76), (-58, 74)]
SOUTH_AMERICA = [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
                 (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
                 (-74, -50), (-70, -54), (-66, -55), (-65, -45), (-62, -41),
                 (-58, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17),
                 (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0),
                 (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-77, 8)]
AFRICA = [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36),
          (10, 37), (11, 34), (20, 32), (25, 32), (30, 31), (32, 31),
          (35, 28), (37, 22), (39, 20), (43, 12), (48, 11), (51, 10),
          (46, 5), (42, 0), (40, -5), (40, -10), (36, -18), (33, -26),
          (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -10),
          (9, -1), (9, 4), (-8, 5), (-13, 8), (-17, 12)]
EURASIA = [(-10, 36), (-9, 43), (-2, 44), (-4, 48), (0, 51), (5, 53),
           (8, 57), (10, 59), (6, 62), (12, 66), (18, 69), (25, 71),
           (30, 70), (40, 68), (50, 69), (60, 69), (68, 70), (75, 72),
           (85, 73), (95, 74), (105, 74), (115, 73), (125, 72), (135, 71),
           (150, 70), (160, 69), (170, 67), (178, 65), (178, 62), (170, 60),
           (162, 56), (158, 52), (150, 59), (142, 55), (140, 50), (135, 44),
           (130, 42), (127, 40), (126, 38), (122, 38), (120, 35), (122, 31),
           (120, 28), (115, 23), (110, 20), (108, 18), (105, 10), (103, 8),
           (100, 8), (98, 10), (95, 15), (92, 20), (90, 22), (86, 20),
           (82, 17), (80, 13), (77, 8), (75, 12), (72, 20), (68, 23),
           (65, 25), (62, 25), (58, 26), (55, 26), (52, 26), (50, 28),
           (48, 30), (44, 30), (42, 29), (40, 28), (39, 24), (37, 22),
           (36, 36), (33, 36), (30, 36), (27, 37), (26, 38), (23, 36),
           (22, 37), (19, 40), (16, 38), (12, 44), (8, 44), (3, 43),
           (0, 40), (-2, 37), (-6, 36), (-9, 37)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -12),
             (132, -11), (130, -13), (126, -14), (122, -17), (118, -20)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -4),
           (100, 1)]
JAVA = [(105, -6), (110, -7), (114, -8), (114, -7), (108, -6)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 1), (117, -2), (113, -3),
          (110, -1)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8),
              (146, -8), (141, -8), (136, -7), (131, -3)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 35), (141, 38),
         (141, 42), (143, 44), (142, 45), (140, 41), (137, 37), (133, 35)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
      (-3, 50)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24),
              (44, -25), (43, -21)]
NEW_ZEALAND = [(167, -45), (170, -42), (173, -40), (176, -38), (178, -38),
               (175, -41), (172, -43), (168, -46)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EURASIA,
              AUSTRALIA, SUMATRA, JAVA, BORNEO, NEW_GUINEA, JAPAN, UK,
              MADAGASCAR, NEW_ZEALAND]


def draw_map(d, mx, my, mw, mh):
    """Wide equirectangular map: 360 deg lon across mw, lat -50..64.75."""
    lat_top, lat_bot = 64.75, -50.0

    def px(lon, lat):
        x = mx + (lon + 180.0) / 360.0 * mw
        y = my + (lat_top - lat) / (lat_top - lat_bot) * mh
        return (x, y)

    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA, outline=RULE, width=1)
    # graticule
    for lon in range(-150, 181, 30):
        x = mx + (lon + 180.0) / 360.0 * mw
        d.line([(x, my), (x, my + mh)], fill=(175, 200, 215), width=1)
    for lat in (-30, 0, 30, 60):
        y = my + (lat_top - lat) / (lat_top - lat_bot) * mh
        d.line([(mx, y), (mx + mw, y)], fill=(175, 200, 215), width=1)
    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # equator label
    f = font(SANS, 9)
    d.text((mx + 4, my + (lat_top - 0) / (lat_top - lat_bot) * mh + 2),
           "EQUATOR", font=f, fill=(110, 140, 160))
    return px


# ---------------------------------------------------------------- illustrations
def illo_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(244, 227, 200))
    # sun
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(255, 200, 90))
    # sea
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(127, 179, 213))
    d.line([(x, y + h * 0.55), (x + w, y + h * 0.55)], fill=(90, 140, 180),
           width=2)
    # far shore (Iran, top) and near shore (Arabia, bottom)
    d.polygon([(x, y + h * 0.42), (x + w * 0.45, y + h * 0.48),
               (x + w * 0.7, y + h * 0.42), (x + w, y + h * 0.5),
               (x + w, y + h * 0.55), (x, y + h * 0.55)], fill=(196, 170, 120))
    d.polygon([(x, y + h), (x, y + h * 0.88), (x + w * 0.4, y + h * 0.92),
               (x + w, y + h * 0.86), (x + w, y + h)], fill=(210, 185, 135))
    # missile site on the far shore + blast
    bx, by = x + w * 0.30, y + h * 0.40
    d.polygon([(bx - 16, by + 8), (bx, by - 14), (bx + 16, by + 8)],
              fill=(255, 140, 40))
    d.ellipse([bx - 22, by - 22, bx + 22, by + 14], outline=(255, 90, 20),
              width=3)
    d.ellipse([bx - 10, by - 10, bx + 10, by + 6], fill=(255, 190, 60))
    # missile arcs
    for (sx, sy, ex, ey, col) in [
            (bx, by - 10, x + w * 0.62, y + h * 0.30, (200, 40, 40)),
            (bx + 8, by - 6, x + w * 0.72, y + h * 0.62, (200, 40, 40)),
            (x + w * 0.55, y + h * 0.95, x + w * 0.30, y + h * 0.45,
             (160, 30, 30))]:
        d.arc([min(sx, ex) - 30, min(sy, ey) - 40, max(sx, ex) + 30,
               max(sy, ey) + 40], start=200, end=340, fill=col, width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=col)
    # ships in the strait
    for sx in (w * 0.52, w * 0.70):
        hx, hy = x + sx, y + h * 0.68
        d.polygon([(hx - 26, hy), (hx + 26, hy), (hx + 18, hy + 10),
                   (hx - 18, hy + 10)], fill=(40, 50, 60))
        d.line([(hx, hy), (hx, hy - 16)], fill=(40, 50, 60), width=3)
        d.rectangle([hx - 8, hy - 12, hx + 8, hy - 2], fill=(90, 100, 110))
    # label
    f = font(SANS_B, 10)
    d.text((x + 6, y + h - 16), "STRAIT OF HORMUZ", font=f, fill=(30, 60, 90))


def illo_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 218))
    # hall backdrop
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(196, 52, 48))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(120, 90, 60))
    # flags on poles
    def flag(fx, kind):
        d.line([(fx, y + 8), (fx, y + h * 0.55)], fill=(60, 45, 30), width=3)
        fw, fh = 52, 30
        if kind == "cn":
            d.rectangle([fx + 2, y + 10, fx + 2 + fw, y + 10 + fh],
                        fill=(222, 41, 16))
            for (sx, sy) in [(12, 8), (24, 6), (28, 14), (20, 20), (10, 16)]:
                d.ellipse([fx + 2 + sx - 2, y + 10 + sy - 2,
                           fx + 2 + sx + 2, y + 10 + sy + 2],
                          fill=(255, 222, 0))
        elif kind == "ru":
            for i, col in enumerate([(255, 255, 255), (0, 60, 160),
                                    (220, 30, 30)]):
                d.rectangle([fx + 2, y + 10 + i * 10, fx + 2 + fw,
                             y + 20 + i * 10], fill=col)
        else:  # us
            for i in range(7):
                col = (200, 40, 40) if i % 2 == 0 else (255, 255, 255)
                d.rectangle([fx + 2, y + 10 + i * 4, fx + 2 + fw,
                             y + 14 + i * 4], fill=col)
            d.rectangle([fx + 2, y + 10, fx + 26, y + 24], fill=(30, 50, 120))
            for (sx, sy) in [(6, 4), (14, 4), (10, 10), (18, 10), (6, 10)]:
                d.ellipse([fx + 2 + sx - 1, y + 10 + sy - 1,
                           fx + 2 + sx + 1, y + 10 + sy + 1],
                          fill=(255, 255, 255))
    flag(x + 18, "cn")
    flag(x + w // 2 - 26, "ru")
    flag(x + w - 72, "us")
    # summit table + three figures
    ty = y + h * 0.66
    d.rectangle([x + 12, ty, x + w - 12, ty + 10], fill=(90, 60, 30))
    d.rectangle([x + 20, ty + 10, x + w - 20, y + h - 6], fill=(70, 45, 25))
    for i, col in enumerate([(40, 40, 40), (60, 60, 70), (30, 50, 90)]):
        cx = x + w * (0.2 + 0.3 * i)
        d.ellipse([cx - 13, ty - 34, cx + 13, ty - 8], fill=(235, 200, 170))
        d.polygon([(cx - 20, ty - 2), (cx + 20, ty - 2), (cx + 26, ty + 2),
                   (cx - 26, ty + 2)], fill=col)
    f = font(SANS_B, 10)
    d.text((x + 6, y + h - 16), "SHENZHEN · APEC SUMMIT", font=f,
           fill=(255, 255, 255))


def illo_kerch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 214, 222))
    # sea
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(110, 155, 190))
    # bridge deck: left span, gap, right span
    dy = y + h * 0.52
    d.rectangle([x, dy, x + w * 0.42, dy + 8], fill=(70, 75, 80))
    d.rectangle([x + w * 0.60, dy, x + w, dy + 8], fill=(70, 75, 80))
    # collapsed span tilted into the water
    d.polygon([(x + w * 0.44, dy + 2), (x + w * 0.58, dy + 2),
               (x + w * 0.55, y + h * 0.78), (x + w * 0.47, y + h * 0.78)],
              fill=(90, 95, 100))
    # pylons
    for px in (w * 0.18, w * 0.80):
        d.rectangle([x + px - 3, dy - 34, x + px + 3, dy + 2],
                    fill=(60, 65, 70))
        d.line([(x + px - 3, dy - 34), (x + px - 40, dy)],
               fill=(60, 65, 70), width=2)
        d.line([(x + px + 3, dy - 34), (x + px + 40, dy)],
               fill=(60, 65, 70), width=2)
    # smoke plumes from the gap
    for (sx, sy, r) in [(0.50, 0.44, 12), (0.53, 0.36, 16), (0.47, 0.30, 10)]:
        d.ellipse([x + w * sx - r, y + h * sy - r, x + w * sx + r,
                   y + h * sy + r], fill=(120, 120, 125))
    # blast at the waterline
    bx, by = x + w * 0.51, y + h * 0.74
    d.polygon([(bx - 18, by + 6), (bx, by - 16), (bx + 18, by + 6)],
              fill=(255, 150, 40))
    d.ellipse([bx - 9, by - 9, bx + 9, by + 7], fill=(255, 200, 80))
    # drones with trails
    for (dx, dy2) in [(0.12, 0.16), (0.30, 0.10), (0.85, 0.14), (0.68, 0.08)]:
        d.ellipse([x + w * dx - 3, y + h * dy2 - 2, x + w * dx + 3,
                   y + h * dy2 + 2], fill=(30, 30, 30))
        d.line([(x + w * dx - 22, y + h * dy2 + 8), (x + w * dx - 3,
                y + h * dy2)], fill=(90, 90, 90), width=1)
    f = font(SANS_B, 10)
    d.text((x + 6, y + h - 16), "KERCH STRAIT", font=f, fill=(30, 50, 70))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx, cw = 14, 996

    # ---- top dateline bar
    f_small = font(SANS, 11)
    f_small_b = font(SANS_B, 11)
    d.text((mx, 10), "WEDNESDAY 18 NOVEMBER 2026", font=f_small_b, fill=INK)
    right = "No. 323  ·  WORLD EDITION  ·  40 STORIES"
    d.text((mx + cw - d.textlength(right, font=f_small), 10), right,
           font=f_small, fill=GREY)
    rule(d, mx, 28, cw, width=2)

    # ---- masthead
    f_mast = font(SERIF, 56)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 32), title,
           font=f_mast, fill=INK)
    f_tag = font(SERIF_IT, 14)
    tag = "The day's news, in one page  —  Wednesday 18 November 2026"
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, 92), tag, font=f_tag,
           fill=GREY)
    rule(d, mx, 110, cw, width=2)
    rule(d, mx, 113, cw, width=1)

    # ---- day in numbers strip
    ny, nh = 118, 76
    d.rectangle([mx, ny, mx + cw, ny + nh], fill=NAVY)
    numbers = [
        ("11,000+", "Ebola cases, DR Congo; 5,400 dead"),
        ("5,412", "US measles cases; free status lost"),
        ("$115.8bn", "Nvidia record quarter"),
        ("56–44", "Senate to Democrats; Peltola wins AK"),
        ("1 light-day", "Voyager 1 now 16bn miles from Earth"),
        ("950,000", "displaced Palestinians on flood-prone Gaza ground"),
        ("19 killed", "Russian military plane crash in Siberia"),
    ]
    f_num = font(SANS_B, 15)
    f_lab = font(SANS, 10)
    # row 1: 4 cells, row 2: 3 cells; number stacked above its label
    for row, items, cols in ((0, numbers[:4], 4), (1, numbers[4:], 3)):
        cell_w = cw // cols
        for i, (num, lab) in enumerate(items):
            cx = mx + i * cell_w + 10
            cy = ny + 4 + row * 36
            d.text((cx, cy), num, font=f_num, fill=AMBER)
            d.text((cx, cy + 18), lab, font=f_lab, fill=(220, 225, 235))
    # ---- leads
    leads = [
        ("GULF WAR ESCALATES", "U.S. jets hit Iran missile site; Tehran strikes back",
         "US jets struck a Revolutionary Guard missile site on Qeshm Island "
         "in the Strait of Hormuz. Iran hit back early Wednesday, striking "
         "Kuwait's Ali Al Salem Air Base, home to US forces, and Bahrain, "
         "which says it stopped several attacks before dawn.", illo_gulf),
        ("XI AND PUTIN OPEN APEC", "Shenzhen summit opens; Trump trilateral due Thursday",
         "Xi and Putin opened APEC in Shenzhen; a trilateral with Trump is "
         "set for Thursday, with no published agenda. Xi pledged to stand "
         "against trade protectionism; Putin attacked Western sanctions. "
         "Trump met Marcos Jr. in Manila and announced a US–Philippines "
         "trade deal.", illo_summit),
        ("KERCH BRIDGE HIT AGAIN", "Road span collapses into the strait on a second day",
         "Ukraine hit the Kerch Bridge for a second day — part of the road "
         "span collapsed into the strait. 141 drones were counted and 126 "
         "downed or suppressed by 08:00; six were injured in Dnipro. Putin "
         "is “not ready” for serious peace talks, sources told the NYT.",
         illo_kerch),
    ]
    ly, lh, lw, gap = 200, 236, 322, 15
    f_kick = font(SANS_B, 12)
    f_head = font(SERIF, 20)
    f_body = font(SANS, 11)
    for i, (kick, head, body, illo) in enumerate(leads):
        x = mx + i * (lw + gap)
        d.rectangle([x, ly, x + lw, ly + lh], outline=RULE, width=1)
        illo(d, x + 1, ly + 1, lw - 2, 100)
        ty = ly + 108
        d.text((x + 8, ty), kick, font=f_kick, fill=RED)
        ty += 16
        for ln in wrap(d, head, f_head, lw - 16):
            d.text((x + 8, ty), ln, font=f_head, fill=INK)
            ty += 22
        ty += 2
        para(d, x + 8, ty, body, f_body, lw - 16, 13)

    # ---- mid stories
    my = 442
    f_sec = font(SANS_B, 13)
    d.text((mx, my), "AROUND THE WORLD", font=f_sec, fill=INK)
    rule(d, mx, my + 17, cw, width=2)
    mid_left = [
        ("Board of Peace faults both sides",
         "Accuses Israel and Hamas of failing ceasefire commitments."),
        ("Kahana elected Knesset speaker",
         "Win for PM-elect Eisenkot as Israel's parliament picks a speaker."),
        ("Cyclone Xavier slams Cook Islands",
         "Category 5 storm hits the Northern Cook Islands."),
        ("World Court to rule on Myanmar",
         "Judges to decide the genocide case against Myanmar."),
        ("Troops mass on Ethiopia–Eritrea border",
         "Forces build up along the shared frontier."),
        ("Myanmar reviews ASEAN ties",
         "Junta weighs its place in the regional bloc."),
        ("Russian jets buzz Taiwan, Japan",
         "Two jets off Taiwan violated Japan airspace; 10 PLA sorties, 11 ships."),
    ]
    mid_right = [
        ("OpenAI launches GPT-6.2",
         "New models Astra and Sol arrive."),
        ("Lammy presses Burnham on EU",
         "Urges a pledge to rejoin the EU — and a referendum."),
        ("US officer held in spy case",
         "Lt Col Tyner, accused of spying for Russia, is in custody."),
        ("Kalshi halts “mention” markets",
         "Prediction site acts after a CFTC order."),
        ("Cook skips White House hearing",
         "Fed governor will not attend on Dec 14 unless Hassett is removed."),
        ("FDA nominee dropped",
         "White House withdraws Heidi Overton's nomination."),
        ("FAA halts router installs",
         "Suspended after a nationwide ground stop."),
    ]
    f_mh = font(SANS_B, 12)
    f_ms = font(SANS, 11)
    col_w = 488
    for ci, col in enumerate((mid_left, mid_right)):
        x = mx + ci * (col_w + 20)
        y = my + 24
        for head, summ in col:
            d.text((x, y), "▪ " + head, font=f_mh, fill=INK)
            y += 14
            for ln in wrap(d, summ, f_ms, col_w - 12):
                d.text((x + 12, y), ln, font=f_ms, fill=(50, 50, 50))
                y += 12
            y += 1

    # ---- also today
    ay = 660
    d.text((mx, ay), "ALSO TODAY", font=f_sec, fill=INK)
    rule(d, mx, ay + 17, cw, width=2)
    also = [
        "NJ sues DHS over Delaney Hall",
        "DHS won't use ships for deportations",
        "Garcia letters to Trump Jr., Vance, Miller",
        "Huang to testify to Senate Banking",
        "Hassan plans AI hearings",
        "Xi greets Trump on tarmac, breaks protocol",
        "Critical Java flaw found by AI startup",
        "Omnilert sued: chips bag read as a gun",
        "Vals: AI mistook civilians for targets",
        "Oil slips as Hormuz risk caps losses",
        "Trump weighs Iran 'dirty bomb' report",
        "Quad meets at leader level, first in 2 yrs",
        "Carney to meet Trump at APEC",
        "Houthis hit Saudi pipeline near Riyadh",
        "Bahrain says it stopped dawn attacks",
        "126 of 141 drones downed; 6 hurt in Dnipro",
    ]
    f_also = font(SANS, 10)
    acol_w = cw // 4
    for i, item in enumerate(also):
        col, row = i % 4, i // 4
        x = mx + col * acol_w
        y = ay + 24 + row * 13
        d.text((x, y), "• " + item, font=f_also, fill=INK)

    # ---- map + legend
    py = 742
    d.text((mx, py), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    rule(d, mx, py + 17, cw, width=2)
    map_x, map_y, map_w, map_h = mx, py + 24, 640, 204
    px = draw_map(d, map_x, map_y, map_w, map_h)
    pins = [
        (54, 26.5), (36.5, 45.3), (114, 22.5), (121, 14.6), (23, -2),
        (-160, -21), (34.5, 31.5), (105, 62), (96, 21), (-152, 64),
    ]
    f_pin = font(SANS_B, 10)
    for i, (lon, lat) in enumerate(pins, 1):
        x, y = px(lon, lat)
        # keep the whole pin inside the panel
        x = min(max(x, map_x + 10), map_x + map_w - 10)
        y = min(max(y, map_y + 10), map_y + map_h - 10)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        t = str(i)
        d.text((x - d.textlength(t, font=f_pin) / 2,
                y - 7), t, font=f_pin, fill=(255, 255, 255))
    legend = [
        ("GULF", "Qeshm hit; Iran strikes Kuwait, Bahrain"),
        ("KERCH BRIDGE", "Road span falls into strait, day two"),
        ("SHENZHEN", "Xi, Putin open APEC; Trump talks Thu"),
        ("MANILA", "Trump, Marcos Jr. announce trade deal"),
        ("DR CONGO", "Ebola 11,000+ cases; 5,400 dead"),
        ("COOK ISLANDS", "Cyclone Xavier, Cat 5, hits north"),
        ("GAZA", "950,000 displaced on flood-prone land"),
        ("SIBERIA", "Military plane crash kills 19"),
        ("MYANMAR", "World Court ruling; ASEAN ties reviewed"),
        ("ALASKA", "Peltola wins; Senate 56–44 Democrat"),
    ]
    lx = map_x + map_w + 16
    lw2 = mx + cw - lx
    f_lh = font(SANS_B, 10)
    f_ls = font(SANS, 10)
    y = map_y + 2
    for i, (place, txt) in enumerate(legend, 1):
        d.ellipse([lx, y + 1, lx + 15, y + 16], fill=RED)
        t = str(i)
        d.text((lx + 7.5 - d.textlength(t, font=f_pin) / 2, y + 3), t,
               font=f_pin, fill=(255, 255, 255))
        d.text((lx + 20, y), place, font=f_lh, fill=INK)
        d.text((lx + 20 + d.textlength(place + "  ", font=f_lh), y + 1),
               txt, font=f_ls, fill=(50, 50, 50))
        y += 20

    # ---- footer
    fy = 976
    rule(d, mx, fy, cw, width=2)
    f_foot = font(SANS_B, 11)
    f_foot2 = font(SANS, 10)
    d.text((mx, fy + 7),
           "Wednesday 18 November 2026  ·  40 stories  ·  Sources: Reuters, "
           "AP, NYT, WSJ, BBC, AFP, Axios  ·  Contested claims marked as claims",
           font=f_foot, fill=INK)
    d.text((mx, fy + 24),
           "A drawn front page built by an AI agent for make.fun — "
           "news-image-20261118. A summary, not a photograph.",
           font=f_foot2, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
