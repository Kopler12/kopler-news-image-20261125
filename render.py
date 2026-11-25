#!/usr/bin/env python3
"""Render 'The World Today' — one image summing up Wednesday 25 November 2026.
Output: 1024x1024 PNG, well under 1 MiB. Deterministic: no timestamps, no random.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (26, 26, 26)
RED = (178, 28, 28)
MUTED = (96, 90, 80)
PANEL = (255, 255, 255)
BORDER = (206, 199, 186)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 170], fill=(26, 26, 26))
d.text((512, 26), "THE WORLD TODAY", font=F(SERIF_B, 58), fill=(250, 247, 240), anchor="ma")
d.rectangle([28, 104, W - 28, 106], fill=RED)
d.text((512, 122), "WEDNESDAY  \u00b7  25 NOVEMBER 2026", font=F(SANS_B, 30),
       fill=(232, 196, 120), anchor="ma")

# ---------- stories ----------
# (kicker, headline, summary, accent colour, icon key)
STORIES = [
    ("SPACE  \u00b7  CHINA",
     "China launches Shenzhou-24",
     "Crew rocket lifts off from Jiuquan with a Pakistani astronaut aboard, bound for the Tiangong station.",
     (29, 78, 137), "rocket"),
    ("SECURITY  \u00b7  NATO",
     "NATO vows to defend space",
     "Alliance answers reports that Russia is readying a nuclear-armed satellite, possibly for launch in December.",
     (91, 33, 128), "satellite"),
    ("COLOMBIA  \u00b7  CARTAGENA",
     "Gunmen seize hostages in a supermarket",
     "Armed men hold shoppers after a failed armoured-truck robbery; five elderly women are released.",
     (146, 64, 14), "store"),
    ("PACIFIC  \u00b7  SOLOMON ISLANDS",
     "Solomon Islands picks Australia",
     "Security pact names Australia the islands\u2019 top partner and rules out foreign military bases.",
     (4, 120, 87), "shield"),
    ("SOUTH KOREA  \u00b7  SEOUL",
     "Education minister quits over exam scandal",
     "Choi Kyo-jin resigns after a national exam-cheating scandal that shocked the country.",
     (153, 27, 27), "exam"),
    ("TRADE  \u00b7  WASHINGTON",
     "Trump plans new tariffs on 16 partners",
     "US to announce duties on goods from 16 trading partners after a trade investigation ends.",
     (51, 65, 85), "ship"),
]

def wrap(draw, text, font, width):
    """Greedy word wrap to pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def icon_rocket(d, x, y, s, col):
    # simple flat rocket, nose up
    d.polygon([(x + s*0.5, y + s*0.08), (x + s*0.72, y + s*0.45), (x + s*0.62, y + s*0.72),
               (x + s*0.38, y + s*0.72), (x + s*0.28, y + s*0.45)], fill=col)
    d.ellipse([x + s*0.42, y + s*0.30, x + s*0.58, y + s*0.46], fill=(250, 247, 240))
    d.polygon([(x + s*0.28, y + s*0.55), (x + s*0.10, y + s*0.82), (x + s*0.30, y + s*0.72)], fill=col)
    d.polygon([(x + s*0.72, y + s*0.55), (x + s*0.90, y + s*0.82), (x + s*0.70, y + s*0.72)], fill=col)
    d.polygon([(x + s*0.44, y + s*0.72), (x + s*0.56, y + s*0.72), (x + s*0.50, y + s*0.95)], fill=(232, 120, 60))
    for i, (sx, sy) in enumerate([(0.18, 0.18), (0.82, 0.25), (0.88, 0.62), (0.14, 0.55)]):
        d.ellipse([x + s*sx - 3, y + s*sy - 3, x + s*sx + 3, y + s*sy + 3], fill=(232, 196, 120))

def icon_satellite(d, x, y, s, col):
    # body + two solar panels + small antenna
    d.line([x + s*0.50, y + s*0.38, x + s*0.50, y + s*0.14], fill=col, width=4)
    d.ellipse([x + s*0.46, y + s*0.10, x + s*0.54, y + s*0.18], fill=(232, 196, 120))
    d.rectangle([x + s*0.36, y + s*0.38, x + s*0.64, y + s*0.62], fill=col)
    d.rectangle([x + s*0.04, y + s*0.42, x + s*0.34, y + s*0.58], fill=(180, 160, 90))
    d.rectangle([x + s*0.66, y + s*0.42, x + s*0.96, y + s*0.58], fill=(180, 160, 90))
    for px in (0.09, 0.19, 0.29, 0.71, 0.81, 0.91):
        d.line([x + s*px, y + s*0.42, x + s*px, y + s*0.58], fill=(120, 100, 50), width=2)
    d.ellipse([x + s*0.44, y + s*0.46, x + s*0.56, y + s*0.54], fill=(250, 247, 240))
    for sx, sy in [(0.12, 0.85), (0.88, 0.85), (0.88, 0.18)]:
        d.ellipse([x + s*sx - 3, y + s*sy - 3, x + s*sx + 3, y + s*sy + 3], fill=(232, 196, 120))

def icon_store(d, x, y, s, col):
    # storefront with awning
    d.rectangle([x + s*0.12, y + s*0.42, x + s*0.88, y + s*0.88], fill=col)
    for i in range(5):
        cx = x + s*(0.12 + i*0.152)
        d.polygon([(cx, y + s*0.28), (cx + s*0.152, y + s*0.28),
                   (cx + s*0.152, y + s*0.42), (cx, y + s*0.42)],
                  fill=(232, 196, 120) if i % 2 == 0 else (250, 247, 240))
    d.rectangle([x + s*0.40, y + s*0.58, x + s*0.60, y + s*0.88], fill=(250, 247, 240))
    d.rectangle([x + s*0.20, y + s*0.52, x + s*0.32, y + s*0.68], fill=(250, 247, 240))
    d.rectangle([x + s*0.68, y + s*0.52, x + s*0.80, y + s*0.68], fill=(250, 247, 240))

def icon_shield(d, x, y, s, col):
    # shield with checkmark
    d.polygon([(x + s*0.5, y + s*0.08), (x + s*0.88, y + s*0.22), (x + s*0.88, y + s*0.52),
               (x + s*0.5, y + s*0.92), (x + s*0.12, y + s*0.52), (x + s*0.12, y + s*0.22)], fill=col)
    d.line([x + s*0.30, y + s*0.50, x + s*0.46, y + s*0.66, x + s*0.72, y + s*0.34],
           fill=(250, 247, 240), width=int(s*0.09), joint="curve")

def icon_exam(d, x, y, s, col):
    # exam paper + pencil + check
    d.rectangle([x + s*0.22, y + s*0.10, x + s*0.72, y + s*0.88], fill=(255, 255, 255), outline=col, width=4)
    for i, ly in enumerate((0.24, 0.38, 0.52, 0.66)):
        d.line([x + s*0.30, y + s*ly, x + s*0.64, y + s*ly], fill=(150, 145, 135), width=3)
    d.polygon([(x + s*0.66, y + s*0.55), (x + s*0.86, y + s*0.28), (x + s*0.92, y + s*0.34),
               (x + s*0.72, y + s*0.61)], fill=(232, 120, 60))
    d.polygon([(x + s*0.86, y + s*0.28), (x + s*0.92, y + s*0.22), (x + s*0.97, y + s*0.29),
               (x + s*0.92, y + s*0.34)], fill=(232, 196, 120))
    d.line([x + s*0.30, y + s*0.82, x + s*0.44, y + s*0.82], fill=RED, width=4)

def icon_ship(d, x, y, s, col):
    # container ship
    d.polygon([(x + s*0.08, y + s*0.62), (x + s*0.92, y + s*0.62), (x + s*0.84, y + s*0.86),
               (x + s*0.16, y + s*0.86)], fill=col)
    for i, cc in enumerate([(178, 28, 28), (29, 78, 137), (4, 120, 87)]):
        d.rectangle([x + s*(0.22 + i*0.20), y + s*0.38, x + s*(0.40 + i*0.20), y + s*0.60], fill=cc)
    d.rectangle([x + s*0.68, y + s*0.30, x + s*0.84, y + s*0.60], fill=(250, 247, 240), outline=col, width=3)
    d.arc([x + s*0.06, y + s*0.88, x + s*0.30, y + s*1.02], 180, 360, fill=(120, 115, 105), width=3)
    d.arc([x + s*0.38, y + s*0.88, x + s*0.62, y + s*1.02], 180, 360, fill=(120, 115, 105), width=3)
    d.arc([x + s*0.70, y + s*0.88, x + s*0.94, y + s*1.02], 180, 360, fill=(120, 115, 105), width=3)

ICONS = {"rocket": icon_rocket, "satellite": icon_satellite, "store": icon_store,
         "shield": icon_shield, "exam": icon_exam, "ship": icon_ship}

MARGIN = 28
GRID_TOP = 186
GRID_H = 1024 - GRID_TOP - 52  # leave room for footer
COLS, ROWS = 2, 3
GAP = 16
PW = (W - 2 * MARGIN - GAP) // COLS
PH = (GRID_H - (ROWS - 1) * GAP) // ROWS

f_kick = F(SANS_B, 17)
f_head = F(SANS_B, 26)
f_body = F(SANS, 19)

for i, (kicker, headline, summary, accent, icon) in enumerate(STORIES):
    r, c = divmod(i, COLS)
    x0 = MARGIN + c * (PW + GAP)
    y0 = GRID_TOP + r * (PH + GAP)
    d.rectangle([x0, y0, x0 + PW, y0 + PH], fill=PANEL, outline=BORDER, width=2)
    # icon tile
    tile = 132
    d.rectangle([x0, y0, x0 + tile, y0 + PH], fill=(238, 233, 222))
    d.rectangle([x0 + tile, y0, x0 + tile + 3, y0 + PH], fill=accent)
    ICONS[icon](d, x0 + 14, y0 + (PH - 104) // 2, 104, accent)
    tx = x0 + tile + 18
    tw = PW - tile - 36
    ty = y0 + 18
    d.text((tx, ty), kicker, font=f_kick, fill=RED)
    ty += 28
    for line in wrap(d, headline, f_head, tw):
        d.text((tx, ty), line, font=f_head, fill=INK)
        ty += 31
    ty += 6
    for line in wrap(d, summary, f_body, tw):
        d.text((tx, ty), line, font=f_body, fill=(64, 60, 54))
        ty += 25

# ---------- footer ----------
fy = GRID_TOP + GRID_H + 12
d.rectangle([MARGIN, fy, W - MARGIN, fy + 2], fill=RED)
d.text((512, fy + 14),
       "Six stories that defined the day  \u00b7  compiled from wire reports, 25 November 2026",
       font=F(SANS, 17), fill=MUTED, anchor="ma")

out = os.environ.get("OUT", "entry.png")
img.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out), "bytes,", img.size)
