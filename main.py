#!/usr/bin/env python3
"""THE WORLD TODAY - front page for Tuesday 17 November 2026.

Pure-stdlib Python: draws a 1024x1024 newspaper front page (40 real stories
from 17 Nov 2026, six continents, lead illustration of the Kerch Bridge,
world map with numbered pins, number strip) and writes /output/entry.png.
Deterministic: no randomness, no clock, no network.
"""
import os
import struct
import sys
import zlib

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (17, 17, 17)
INK_SOFT = (60, 58, 52)
RED = (178, 34, 28)
NAVY = (28, 48, 92)
SKY = (176, 205, 224)
SEA = (64, 110, 148)
SEA_DARK = (42, 84, 122)
SAND = (226, 211, 170)
GREY = (120, 118, 110)
RULE = (150, 145, 132)

# ---------------------------------------------------------------- font 5x7
# Each glyph: 7 rows of 5 cells, '#' = ink. Lowercase included.
FONT = {
 'A': (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
 'B': ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
 'C': (" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"),
 'D': ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
 'E': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
 'F': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
 'G': (" ####", "#    ", "#    ", "# ###", "#   #", "#   #", " ### "),
 'H': ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
 'I': ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"),
 'J': ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
 'K': ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
 'L': ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
 'M': ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
 'N': ("#   #", "##  #", "##  #", "# # #", "#  ##", "#  ##", "#   #"),
 'O': (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
 'P': ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
 'Q': (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
 'R': ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
 'S': (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
 'T': ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
 'U': ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
 'V': ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
 'W': ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
 'X': ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
 'Y': ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
 'Z': ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
 '0': (" ### ", "#  ##", "# # #", "##  #", "#   #", "#   #", " ### "),
 '1': ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
 '2': (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
 '3': ("#### ", "    #", "    #", " ### ", "    #", "    #", "#### "),
 '4': ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
 '5': ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
 '6': (" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "),
 '7': ("#####", "    #", "   # ", "   # ", "  #  ", "  #  ", "  #  "),
 '8': (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
 '9': (" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "),
 'a': ("     ", "     ", " ### ", "    #", " ####", "#   #", " ### "),
 'b': ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#### "),
 'c': ("     ", "     ", " ### ", "#    ", "#    ", "#    ", " ### "),
 'd': ("    #", "    #", " ####", "#   #", "#   #", "#   #", " ####"),
 'e': ("     ", "     ", " ### ", "#   #", "#####", "#    ", " ### "),
 'f': ("  ## ", " #   ", " #   ", "#### ", " #   ", " #   ", " #   "),
 'g': ("     ", "     ", " ####", "#   #", "#   #", " ####", "  ## "),
 'h': ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#   #"),
 'i': ("     ", "  #  ", "     ", " ##  ", "  #  ", "  #  ", " ### "),
 'j': ("    #", "     ", "   ##", "    #", "    #", "    #", "  ## "),
 'k': ("#    ", "#    ", "#  # ", "# #  ", "##   ", "# #  ", "#  # "),
 'l': (" ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
 'm': ("     ", "     ", "## # ", "# # #", "# # #", "# # #", "# # #"),
 'n': ("     ", "     ", "#### ", "#   #", "#   #", "#   #", "#   #"),
 'o': ("     ", "     ", " ### ", "#   #", "#   #", "#   #", " ### "),
 'p': ("     ", "     ", "#### ", "#   #", "#   #", "#### ", "#    "),
 'q': ("     ", "     ", " ####", "#   #", "#   #", " ####", "    #"),
 'r': ("     ", "     ", "# ## ", "##  #", "#    ", "#    ", "#    "),
 's': ("     ", "     ", " ####", "#    ", " ### ", "    #", "#### "),
 't': (" #   ", " #   ", "#### ", " #   ", " #   ", " #   ", "  ## "),
 'u': ("     ", "     ", "#   #", "#   #", "#   #", "#   #", " ### "),
 'v': ("     ", "     ", "#   #", "#   #", "#   #", " # # ", "  #  "),
 'w': ("     ", "     ", "#   #", "#   #", "# # #", "# # #", " # # "),
 'x': ("     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"),
 'y': ("     ", "     ", "#   #", "#   #", "#   #", " ####", "    #"),
 'z': ("     ", "     ", "#####", "   # ", "  #  ", " #   ", "#####"),
 '.': ("     ", "     ", "     ", "     ", "     ", "     ", "  #  "),
 ',': ("     ", "     ", "     ", "     ", "     ", "  #  ", " #   "),
 ':': ("     ", "     ", "  #  ", "     ", "     ", "  #  ", "     "),
 ';': ("     ", "     ", "  #  ", "     ", "     ", "  #  ", " #   "),
 "'": ("     ", "  #  ", "  #  ", "     ", "     ", "     ", "     "),
 '"': ("     ", " # # ", " # # ", "     ", "     ", "     ", "     "),
 '!': ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
 '?': (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
 '-': ("     ", "     ", "     ", "#####", "     ", "     ", "     "),
 '(': ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
 ')': (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
 '/': ("    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "),
 '%': ("##  #", "## # ", "   # ", "  #  ", " #   ", "# ## ", "#  ##"),
 '$': ("  #  ", " ####", "# #  ", " ### ", "  # #", "#### ", "  #  "),
 '&': (" ##  ", "#  # ", "#  # ", " #   ", "# # #", "#  # ", " ## #"),
 '+': ("     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "),
 '=': ("     ", "     ", "#####", "     ", "#####", "     ", "     "),
 '*': ("     ", " # # ", "  #  ", "#####", "  #  ", " # # ", "     "),
 '#': (" # # ", " # # ", "#####", " # # ", "#####", " # # ", " # # "),
 '@': (" ### ", "#   #", "# ###", "# # #", "# ## ", "#    ", " ### "),
 '_': ("     ", "     ", "     ", "     ", "     ", "     ", "#####"),
 ' ': ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
}

# ---------------------------------------------------------------- raster
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.rect(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            if fill:
                self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, c)
            else:
                self.set(cx - dx, cy + dy, c)
                self.set(cx + dx, cy + dy, c)

    def poly(self, pts, c):
        # scanline fill
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    t = (y - y0) / (y1 - y0)
                    xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                self.rect(int(xs[k]), y, int(xs[k + 1]) - int(xs[k]) + 1, 1, c)

    def text(self, x, y, s, scale=1, c=INK, align="l"):
        if align in ("c", "r"):
            wdt = self.text_width(s, scale)
            if align == "c":
                x -= wdt // 2
            else:
                x -= wdt
        cx = x
        for ch in s:
            g = FONT.get(ch)
            if g is None:
                g = FONT['?']
            for r, row in enumerate(g):
                for col, bit in enumerate(row):
                    if bit == '#':
                        self.rect(cx + col * scale, y + r * scale, scale, scale, c)
            cx += 6 * scale
        return cx

    @staticmethod
    def text_width(s, scale=1):
        return len(s) * 6 * scale - scale

    def wrap(self, s, max_chars):
        words, lines, cur = s.split(" "), [], ""
        for wd in words:
            nxt = (cur + " " + wd).strip()
            if len(nxt) <= max_chars:
                cur = nxt
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


def png_bytes(cv):
    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


# ---------------------------------------------------------------- stories
# 40 real stories from Tuesday 17 November 2026, grouped by continent.
# (headline, deck) - headlines wrap to at most 2 lines, decks to 1 line.
STORIES = [
 ("EUROPE", [
  ("KERCH BRIDGE SPAN FALLS INTO SEA",
   "Seven-stage op, 2 dead, traffic halted"),
  ("RUSSIA HITS KYIV'S DNIPRO BRIDGES",
   "Strikes kill 2, cut heat and water"),
  ("ESTONIA TO SHUT RUSSIAN BORDER",
   "Closure follows alleged arson attack"),
  ("LATVIA BACKS NEW GOVERNMENT",
   "Coalition to focus on economy, defence"),
  ("FRENCH MARCHES DRAW SMALL CROWDS",
   "Turnout falls; marches stay peaceful"),
  ("MOLDOVA SHUTS AIRSPACE",
   "Russian drones cross Chisinau skies"),
  ("TRUMP, XI, PUTIN SUMMIT NEARS",
   "Three-way talks set for Shenzhen"),
  ("DEUTSCHE BANK LEAK TESTS CEO",
   "Sewing's reform pledge under scrutiny"),
 ]),
 ("MIDDLE EAST", [
  ("US JETS STRIKE IRAN'S QESHM",
   "Jets hit missile site after Bahrain"),
  ("IRAN DRONES TARGET BAHRAIN BASE",
   "Third strike in five days, all stopped"),
  ("KUWAIT INTERCEPTS IRANIAN DRONES",
   "Gulf states on alert after Qeshm strike"),
  ("FIVE SHIPS HIT MINES IN HORMUZ",
   "Tankers ablaze on routes Iran bars"),
  ("GAZA FACES HYPOTHERMIA DEATHS",
   "UN warns of winter toll, wants shelter"),
  ("ISRAEL KILLS SENIOR HAMAS CHIEF",
   "Oct 7-linked chief dies despite truce"),
  ("IRAQ TO CRACK DOWN ON MILITIAS",
   "PM's riskiest move yet, analysts say"),
 ]),
 ("ASIA-PACIFIC", [
  ("NVIDIA SALES DOUBLE TO $115.8BN",
   "Q3 beats forecasts; Huang stays out"),
  ("CHINA OCTOBER DATA MISSES",
   "Asian chips slump ahead of Nvidia"),
  ("APEC SUMMIT OPENS IN SHENZHEN",
   "Xi urges open trade; Trump to attend"),
  ("TRUMP STARTS ASIA TRIP IN MANILA",
   "Quad talks first, then China visit"),
  ("TAIWAN IN TOUCH WITH US ON APEC",
   "Envoy to speak with members at summit"),
  ("AUSTRALIA SANCTIONS SETTLERS",
   "Three people, four groups sanctioned"),
  ("AUSTRALIA EASES BACKPACKER VISAS",
   "Farm-work rules softened after outcry"),
  ("JAPAN: BOJ TO KEEP RAISING RATES",
   "Governor signals more hikes ahead"),
 ]),
 ("AMERICAS", [
  ("US SENATOR TARGETS CHINA STATUS",
   "Bill filed ahead of Trump-Xi meeting"),
  ("FAA GROUND STOP HALTS ROUTERS",
   "Juniper installs paused nationwide"),
  ("WALL STREET FALLS 1.9%",
   "Fear gauge jumps ahead of Nvidia"),
  ("DISNEY TOPS EARNINGS ESTIMATES",
   "Theme parks, NFL lift results"),
  ("MEXICO: RATE PAUSE LENGTH UNCLEAR",
   "Cenbank flags inflation risks"),
  ("HAITI MARCH PRAISES BUKELE",
   "Thousands back Salvadoran troops"),
  ("BRAZIL: TAX REFORM MAY LIFT PRICES",
   "Finance chief warns of inflation hit"),
 ]),
 ("AFRICA", [
  ("MALAWI OPENS $6M HEART CENTRE",
   "Anadkat Adventist facility launches"),
  ("NIGERIA ELECTION CHIEF STAYS",
   "INEC denies chairman resignation"),
  ("ZAMFARA MAN FREED AFTER 5 MONTHS",
   "Held over witchcraft claims, now free"),
  ("DANGOTE IS AFRICA ENERGY PERSON",
   "Named Africa's Energy Person of 2026"),
  ("MALAWI FACES EGYPT: WIN OR DIE",
   "Flames in AFCON qualifier showdown"),
 ]),
 ("WORLD, SPORT & CULTURE", [
  ("27 YEARS FOR TRUMP MURDER PLOT",
   "Iran-linked case ends in US court"),
  ("BEZOS HELPED PICK NEW BOND",
   "Pattinson to play 007, Bezos says"),
  ("ANTHROPIC PLANS $1.4TN IPO",
   "Pricing looms on Nasdaq"),
  ("NSA NETWORK GOES OFFLINE",
   "Classified net down in maintenance"),
  ("F1 RACES GO AHEAD DESPITE WAR",
   "Finales on as other events axed"),
 ]),
]

# flat list with running numbers 1..40
FLAT = []
for _sec, items in STORIES:
    for _h, _d in items:
        FLAT.append((_sec, _h, _d))

# ---------------------------------------------------------------- world map
# lon/lat polygons, drawn inside a 640x170 box (lon -170..190, lat 75..-55)
MAP_X, MAP_Y, MAP_W, MAP_H = 18, 410, 620, 146

def _mx(lon, lat):
    x = MAP_X + (lon + 170.0) / 360.0 * MAP_W
    y = MAP_Y + (75.0 - lat) / 130.0 * MAP_H
    return (int(x), int(y))

def _poly_ll(cv, pts, c):
    cv.poly([_mx(lo, la) for lo, la in pts], c)

CONTINENTS = [
 # North America
 [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
  (-75, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
  (-80, 32), (-85, 30), (-90, 29), (-97, 26), (-105, 20), (-95, 16),
  (-87, 13), (-83, 9), (-79, 9), (-90, 14), (-105, 20), (-115, 30),
  (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
 # Greenland
 [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-20, 70), (-25, 76),
  (-40, 80), (-58, 76), (-60, 70)],
 # South America
 [(-79, 9), (-75, 11), (-65, 11), (-60, 8), (-52, 5), (-50, 0), (-40, -5),
  (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -50),
  (-73, -53), (-70, -40), (-72, -20), (-78, -10), (-80, -3), (-81, 3)],
 # Africa
 [(-17, 15), (-15, 27), (-10, 31), (-5, 35), (10, 37), (20, 32), (30, 31),
  (35, 28), (40, 15), (43, 11), (48, 10), (51, 12), (45, 5), (40, -5),
  (35, -15), (32, -25), (28, -33), (20, -35), (15, -30), (12, -18),
  (9, -1), (9, 4), (-8, 5), (-15, 11)],
 # Eurasia
 [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
  (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (40, 68), (50, 69),
  (60, 70), (70, 72), (80, 73), (100, 76), (120, 73), (140, 72),
  (160, 70), (178, 66), (170, 60), (162, 56), (158, 52), (150, 59),
  (142, 55), (140, 45), (135, 43), (130, 42), (127, 40), (122, 38),
  (120, 32), (115, 23), (108, 18), (105, 10), (100, 8), (98, 12),
  (95, 16), (92, 21), (88, 22), (80, 15), (76, 10), (72, 20), (66, 25),
  (60, 25), (57, 26), (52, 26), (50, 29), (48, 30), (44, 29), (40, 31),
  (36, 36), (30, 36), (26, 38), (23, 36), (20, 40), (15, 44), (10, 44),
  (3, 43), (-2, 37), (-6, 36)],
 # Britain
 [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53)],
 # Japan
 [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 43),
  (141, 45), (139, 39), (135, 34), (131, 33)],
 # Australia
 [(113, -22), (114, -30), (115, -34), (120, -34), (129, -32), (132, -32),
  (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
  (150, -23), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
  (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
 # New Zealand
 [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (174, -41)],
]

# (story number, lon, lat) pins on the map
PINS = [
 (1, 37.5, 45.3),    # Kerch Bridge
 (2, 30.5, 50.4),    # Kyiv
 (9, 56.3, 26.9),    # Qeshm Island
 (12, 58.5, 25.5),   # Strait of Hormuz
 (16, -122.0, 37.4), # Nvidia, Santa Clara
 (18, 114.0, 22.5),  # Shenzhen, APEC
 (21, 151.0, -33.9), # Sydney
 (31, 34.0, -13.5),  # Malawi
]

PIN_KEY = [
 (1, "KERCH BRIDGE FALLS"),
 (2, "KYIV BRIDGES HIT"),
 (9, "US JETS HIT QESHM"),
 (12, "MINES IN HORMUZ"),
 (16, "NVIDIA $115.8BN"),
 (18, "APEC IN SHENZHEN"),
 (21, "SYDNEY SANCTIONS"),
 (31, "MALAWI HEART CENTRE"),
]

# ---------------------------------------------------------------- illustration
def draw_kerch(cv, x, y, w, h):
    """Flat illustration: the Kerch Bridge over the strait, broken span,
    smoke plume, dawn sky. All shapes, no external assets."""
    cv.rect(x, y, w, h, SKY)
    # sun + haze bands
    cv.circle(x + w - 70, y + 42, 26, (240, 214, 140))
    cv.rect(x, y + 78, w, 10, (206, 222, 232))
    cv.rect(x, y + 96, w, 8, (196, 216, 230))
    # distant shore
    cv.rect(x, y + h - 78, w, 14, SAND)
    cv.rect(x, y + h - 64, w, h - (h - 64), SEA)
    # sea waves
    for i, wy in enumerate(range(y + h - 56, y + h - 6, 12)):
        off = (i % 2) * 26
        for wx in range(x + 8 + off, x + w - 20, 52):
            cv.line(wx, wy, wx + 22, wy, (140, 178, 205), 2)
    # bridge deck (left + right of the gap)
    deck_y = y + h - 108
    cv.rect(x, deck_y, 190, 7, (52, 52, 54))
    cv.rect(x + w - 190, deck_y, 190, 7, (52, 52, 54))
    # fallen span, tilted into the sea
    cv.poly([(x + 200, deck_y + 4), (x + 268, deck_y + 4),
             (x + 252, deck_y + 46), (x + 196, deck_y + 40)], (74, 72, 70))
    # pylons + cables
    for px in (x + 60, x + w - 70):
        cv.rect(px, deck_y - 62, 6, 62, (52, 52, 54))
        cv.line(px + 3, deck_y - 62, px - 58, deck_y, (110, 108, 104), 1)
        cv.line(px + 3, deck_y - 62, px + 64, deck_y, (110, 108, 104), 1)
    # arch over the gap (broken)
    cv.line(x + 190, deck_y, x + 232, deck_y - 44, (52, 52, 54), 3)
    cv.line(x + w - 190, deck_y, x + w - 236, deck_y - 40, (52, 52, 54), 3)
    # smoke plume from the gap
    for cx, cy, r, c in ((x + 232, deck_y - 30, 16, (90, 88, 84)),
                         (x + 246, deck_y - 52, 20, (110, 108, 104)),
                         (x + 228, deck_y - 74, 24, (130, 128, 122)),
                         (x + 252, deck_y - 96, 18, (150, 148, 142))):
        cv.circle(cx, cy, r, c)
    # fire flash at the break
    cv.circle(x + 226, deck_y - 6, 10, (232, 120, 40))
    cv.circle(x + 226, deck_y - 6, 5, (250, 200, 90))
    # caption bar
    cv.rect(x, y + h - 26, w, 26, INK)
    cv.text(x + 12, y + h - 19, "THE KERCH BRIDGE, 17 NOVEMBER: THE ROAD SPAN IS DOWN",
            1, (247, 243, 232))


# ---------------------------------------------------------------- layout
def draw_masthead(cv):
    cv.text(512, 14, "THE WORLD TODAY", 7, INK, "c")
    cv.hline(16, 70, 992, INK, 2)
    cv.text(512, 78, "TUESDAY, 17 NOVEMBER 2026  -  40 STORIES  -  SIX CONTINENTS  -  ONE FRONT PAGE",
            2, INK_SOFT, "c")
    cv.hline(16, 96, 992, INK, 3)
    cv.hline(16, 101, 992, INK, 1)


def draw_lead(cv):
    draw_kerch(cv, 16, 106, 500, 224)
    x = 532
    cv.text(x, 110, "UKRAINE - CRIMEA - LEAD STORY", 2, RED)
    cv.text(x, 136, "BRIDGE FALLS", 4, INK)
    cv.text(x, 166, "INTO THE SEA", 4, INK)
    cv.hline(x, 202, 476, RULE, 1)
    deck = ("Ukraine says drones, Neptune and Flamingo missiles dropped the "
            "road span in a seven-stage operation weeks in the making.")
    yy = 210
    for ln in cv.wrap(deck, 39):
        cv.text(x, yy, ln, 2, INK)
        yy += 16
    # two mini-leads under the deck
    for bx, kick, head, dk in (
            (532, "THE GULF", "US JETS HIT QESHM",
             "Fighters strike a missile site after the Bahrain drone raid."),
            (772, "MARKETS", "NVIDIA $115.8BN",
             "Q3 revenue doubles; the board bars Huang's return.")):
        cv.text(bx, 282, kick, 1, RED)
        cv.text(bx, 294, head, 2, INK)
        yy = 312
        for ln in cv.wrap(dk, 38):
            cv.text(bx, yy, ln, 1, INK_SOFT)
            yy += 9


def draw_strip(cv):
    stats = [
        ("$115.8BN", "NVIDIA Q3 REVENUE, UP 103%"),
        ("1,441", "DRONES RUSSIA SAYS IT DOWNED"),
        ("5", "SHIPS HIT BY MINES IN HORMUZ"),
        ("$130BN", "NVIDIA Q4 SALES GUIDANCE"),
        ("3RD", "US CARRIER GROUP IN THE GULF"),
    ]
    y, h = 338, 46
    cv.rect(16, y, 992, h, (238, 232, 214))
    cv.hline(16, y, 992, INK, 1)
    cv.hline(16, y + h - 1, 992, INK, 1)
    for i, (num, lab) in enumerate(stats):
        bx = 16 + i * 199
        if i:
            cv.vline(bx - 4, y + 5, h - 10, RULE, 1)
        cv.text(bx + 96, y + 7, num, 3, NAVY, "c")
        cv.text(bx + 96, y + 32, lab, 1, INK_SOFT, "c")


def draw_map(cv):
    cv.text(18, 392, "THE WORLD IN ONE LOOK", 2, INK)
    cv.text(656, 392, "ON THE MAP", 2, RED)
    # map frame
    cv.rect(MAP_X, MAP_Y, MAP_W, MAP_H, (232, 238, 240))
    cv.hline(MAP_X, MAP_Y, MAP_W, INK, 1)
    cv.hline(MAP_X, MAP_Y + MAP_H - 1, MAP_W, INK, 1)
    cv.vline(MAP_X, MAP_Y, MAP_H, INK, 1)
    cv.vline(MAP_X + MAP_W - 1, MAP_Y, MAP_H, INK, 1)
    for pts in CONTINENTS:
        _poly_ll(cv, pts, (196, 186, 158))
    for num, lon, lat in PINS:
        px, py = _mx(lon, lat)
        # offset pins that would overlap a neighbour, with a leader line
        off = {2: (-17, -13), 12: (18, 11)}.get(num, (0, 0))
        if off != (0, 0):
            cv.line(px, py, px + off[0], py + off[1], RED, 1)
            px, py = px + off[0], py + off[1]
        cv.circle(px, py, 9, RED)
        cv.circle(px, py, 9, (255, 255, 255), fill=False)
        s = str(num)
        cv.text(px - (len(s) * 6 - 1) // 2, py - 3, s, 1, (255, 255, 255))
    # key panel
    yy = 414
    for num, label in PIN_KEY:
        cv.text(656, yy, str(num), 2, RED)
        cv.text(680, yy + 2, label, 1, INK)
        yy += 17
    cv.text(656, yy + 4, "Every story numbered 1-40 below.", 1, INK_SOFT)


def draw_grid(cv):
    cols_x = (16, 264, 512, 760)
    col_w = 232
    y0 = 566
    # columns hold stories 1-10, 11-20, 21-30, 31-40
    for ci in range(4):
        x = cols_x[ci]
        yy = y0
        prev_sec = None
        for idx in range(ci * 10, ci * 10 + 10):
            sec, head, deck = FLAT[idx]
            if sec != prev_sec:
                cv.text(x, yy, sec, 1, RED)
                cv.hline(x, yy + 10, col_w, RULE, 1)
                yy += 18
                prev_sec = sec
            num = str(idx + 1)
            cv.text(x, yy, num, 2, RED)
            hx = x + len(num) * 12 + 6
            max_h = (col_w - (hx - x) + 2) // 12
            hlines = cv.wrap(head, max_h)
            hy = yy
            for ln in hlines[:2]:
                cv.text(hx, hy, ln, 2, INK)
                hy += 15
            dlines = cv.wrap(deck, 38)
            cv.text(x, yy + 31, dlines[0], 1, INK_SOFT)
            yy += 40
        if ci < 3:
            cv.vline(cols_x[ci] + col_w + 8, y0, 436, RULE, 1)


def draw_footer(cv):
    cv.hline(16, 1006, 992, INK, 1)
    cv.text(512, 1012, "THE WORLD TODAY - TUESDAY 17 NOVEMBER 2026 - 40 STORIES FROM SIX CONTINENTS",
            1, INK_SOFT, "c")


def build():
    cv = Canvas(W, H, PAPER)
    # frame
    cv.hline(4, 4, 1016, INK, 3)
    cv.hline(4, 1017, 1016, INK, 3)
    cv.vline(4, 4, 1016, INK, 3)
    cv.vline(1017, 4, 1016, INK, 3)
    draw_masthead(cv)
    draw_lead(cv)
    draw_strip(cv)
    draw_map(cv)
    draw_grid(cv)
    draw_footer(cv)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(build())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
