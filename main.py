#!/usr/bin/env python3
"""The World Today - front page for Tuesday, 24 November 2026.

Draws an editorial newspaper front page (1024x1024 PNG) that sums up the
world's news of Tuesday 24 November 2026: five real, verifiable stories
from five regions and fields, with the date named up front.

Python 3.13 standard library only. No network, no randomness, no clock.
The program runs twice and both runs write the same bytes.
Writes /output/entry.png (the graded file) and a byte-identical copy at
/output/cover.jpg. The output directory is MAKEFUN_OUTPUT_DIR when set,
else /output.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- colours
PAPER = (248, 245, 236)      # warm newsprint
INK = (17, 17, 17)           # headline black
BODY = (51, 51, 51)          # body grey
NAVY = (16, 36, 62)          # masthead + lead panel
NAVY2 = (18, 58, 92)         # lead panel inner blue
GOLD = (232, 184, 75)        # masthead rule + date
RED = (185, 28, 28)          # kickers
SKY = (127, 179, 213)        # globe ocean
LAND = (76, 175, 80)         # globe land
WHITE = (255, 255, 255)
SEA = (31, 90, 140)          # ship panel sea
CHIPBG = (24, 52, 32)        # chip panel
WARNBG = (252, 243, 207)     # warning panel
COURTBG = (233, 230, 222)    # courthouse panel
GREY = (120, 120, 120)

# ------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 cells; '#' is ink, '.' is blank.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": (".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "/": ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    "(": ("...##", "..#..", "..#..", "..#..", "..#..", "..#..", "...##"),
    ")": ("##...", "..#..", "..#..", "..#..", "..#..", "..#..", "##..."),
    "&": (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "#": (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    "@": (".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."),
    "*": (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    "_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
}


def text_width(text, scale):
    """Pixel width of text at the given scale (6 units per char)."""
    return len(text) * 6 * scale


def wrap_text(text, max_chars):
    """Word-wrap text to lines of at most max_chars characters."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= max_chars:
            cur += " " + word
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------ pixel buffer
def new_canvas():
    """A fresh 1024x1024 RGB buffer, filled with newsprint paper."""
    buf = bytearray(W * H * 3)
    r, g, b = PAPER
    row = bytes((r, g, b)) * W
    for y in range(H):
        base = y * W * 3
        buf[base:base + W * 3] = row
    return buf


def fill_rect(buf, x, y, w, h, color):
    """Fill an axis-aligned rectangle (clipped to the canvas)."""
    if w <= 0 or h <= 0:
        return
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x0 >= x1 or y0 >= y1:
        return
    r, g, b = color
    row = bytes((r, g, b)) * (x1 - x0)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        buf[base:base + (x1 - x0) * 3] = row


def fill_circle(buf, cx, cy, r, color):
    """Fill a circle by horizontal scanlines."""
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(r * r - dy * dy))
        fill_rect(buf, cx - dx, cy + dy, 2 * dx + 1, 1, color)


def fill_polygon(buf, points, color):
    """Fill a simple polygon by scanline (nonzero winding)."""
    if len(points) < 3:
        return
    min_y = max(0, min(p[1] for p in points))
    max_y = min(H - 1, max(p[1] for p in points))
    n = len(points)
    for y in range(min_y, max_y + 1):
        xs = []
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            if y1 == y2:
                continue
            if (y1 <= y < y2) or (y2 <= y < y1):
                t = (y - y1) / (y2 - y1)
                xs.append(x1 + t * (x2 - x1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            x0 = int(round(xs[i]))
            x1 = int(round(xs[i + 1]))
            fill_rect(buf, x0, y, x1 - x0 + 1, 1, color)


def draw_text(buf, x, y, text, scale, color):
    """Draw text with the 5x7 bitmap font, scaled by `scale`.

    The font holds capitals only, so text is uppercased first: body copy
    is written in sentence case in the story data but renders in capitals,
    which keeps every letter legible instead of dropping the lowercase.
    """
    text = text.upper()
    cx = x
    for ch in text:
        glyph = FONT.get(ch)
        if glyph is None:
            cx += 6 * scale
            continue
        for row_i, row in enumerate(glyph):
            for col_i, bit in enumerate(row):
                if bit == "#":
                    fill_rect(buf, cx + col_i * scale, y + row_i * scale,
                              scale, scale, color)
        cx += 6 * scale
    return cx


def draw_text_block(buf, x, y, text, scale, color, max_width, line_gap=4):
    """Draw word-wrapped text; returns the y just below the last line."""
    max_chars = max(1, max_width // (6 * scale))
    lines = wrap_text(text, max_chars)
    line_h = 7 * scale + line_gap
    for i, line in enumerate(lines):
        draw_text(buf, x, y + i * line_h, line, scale, color)
    return y + len(lines) * line_h


# ---------------------------------------------------------------- PNG out
def _chunk(ctype, data):
    out = struct.pack(">I", len(data)) + ctype + data
    out += struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)
    return out


def write_png(path, buf):
    """Encode the RGB buffer as a PNG (colour type 2, 8-bit)."""
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)  # filter: none
        raw += buf[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ------------------------------------------------------------ illustrations
def draw_globe(buf, cx, cy, r):
    """A stylised globe: ocean, meridians, green landmasses."""
    fill_circle(buf, cx, cy, r, SKY)
    # meridian + parallel chords, clipped to the circle
    dark = (86, 130, 170)
    for dy in (-r // 2, r // 2):
        half = int(math.sqrt(max(0, r * r - dy * dy)))
        fill_rect(buf, cx - half, cy + dy, 2 * half, 3, dark)
    for dx in (-r // 2, r // 2):
        half = int(math.sqrt(max(0, r * r - dx * dx)))
        fill_rect(buf, cx + dx, cy - half, 3, 2 * half, dark)
    # landmasses: a few green blobs
    for (lx, ly, lr) in ((-r // 3, -r // 4, r // 4),
                         (r // 4, r // 5, r // 5),
                         (-r // 5, r // 3, r // 6),
                         (r // 2, -r // 2, r // 7)):
        fill_circle(buf, cx + lx, cy + ly, lr, LAND)


def draw_dove(buf, x, y, s):
    """A small white dove in flight (body, head, beak, wing, tail)."""
    # tail fan
    fill_polygon(buf, [(x, y + 6 * s), (x - 16 * s, y + 14 * s),
                       (x - 14 * s, y + 2 * s)], WHITE)
    # body
    fill_circle(buf, x, y, 9 * s, WHITE)
    # raised wing
    fill_polygon(buf, [(x - 4 * s, y - 2 * s), (x + 2 * s, y - 20 * s),
                       (x + 10 * s, y - 2 * s)], WHITE)
    # head
    fill_circle(buf, x + 10 * s, y - 8 * s, 5 * s, WHITE)
    # beak
    fill_polygon(buf, [(x + 14 * s, y - 9 * s), (x + 20 * s, y - 7 * s),
                       (x + 14 * s, y - 5 * s)], (232, 184, 75))


def draw_flag_ukraine(buf, x, y, w, h):
    fill_rect(buf, x, y, w, h // 2, (0, 87, 183))
    fill_rect(buf, x, y + h // 2, w, h - h // 2, (255, 215, 0))


def draw_flag_eu(buf, x, y, w, h):
    fill_rect(buf, x, y, w, h, (0, 51, 153))
    # ring of small gold stars
    for k in range(8):
        ang = 2 * math.pi * k / 8
        sx = int(x + w // 2 + (w // 3) * math.cos(ang))
        sy = int(y + h // 2 + (h // 3) * math.sin(ang))
        fill_rect(buf, sx - 1, sy - 1, 3, 3, (255, 204, 0))


def draw_flag_us(buf, x, y, w, h):
    stripe = max(1, h // 13)
    for i in range(13):
        fill_rect(buf, x, y + i * stripe, w, stripe,
                  (178, 34, 52) if i % 2 == 0 else WHITE)
    fill_rect(buf, x, y, w * 2 // 5, stripe * 7, (60, 59, 110))


def draw_ship(buf, x, y, w, h):
    """A tanker on waves (Venezuela / Caribbean)."""
    fill_rect(buf, x, y, w, h, SEA)
    # waves
    for wy in (y + h - 26, y + h - 14):
        for wx in range(x, x + w, 24):
            fill_circle(buf, wx + 12, wy, 7, WHITE)
    # hull
    fill_polygon(buf, [(x + 12, y + h - 60), (x + w - 12, y + h - 60),
                       (x + w - 30, y + h - 30), (x + 30, y + h - 30)],
                 (30, 30, 30))
    # containers
    for i, c in enumerate(((200, 60, 60), (60, 120, 180), (232, 184, 75))):
        fill_rect(buf, x + 22 + i * 34, y + h - 96, 30, 34, c)
    # bridge tower
    fill_rect(buf, x + w - 52, y + h - 110, 26, 50, WHITE)
    fill_rect(buf, x + w - 52, y + h - 110, 26, 8, (30, 30, 30))


def draw_chip(buf, x, y, w, h):
    """A computer chip with a rising chart (Nvidia)."""
    fill_rect(buf, x, y, w, h, CHIPBG)
    # gold pins around the chip
    cx, cy = x + w // 2, y + h // 2
    s = 74
    for i in range(6):
        off = -40 + i * 16
        fill_rect(buf, cx + off, cy - s // 2 - 14, 6, 14, GOLD)
        fill_rect(buf, cx + off, cy + s // 2, 6, 14, GOLD)
        fill_rect(buf, cx - s // 2 - 14, cy + off, 14, 6, GOLD)
        fill_rect(buf, cx + s // 2, cy + off, 14, 6, GOLD)
    fill_rect(buf, cx - s // 2, cy - s // 2, s, s, (16, 16, 16))
    fill_rect(buf, cx - s // 2 + 8, cy - s // 2 + 8, s - 16, s - 16,
              (34, 139, 34))
    draw_text(buf, cx - 14, cy - 8, "NV", 2, WHITE)
    # rising chart line
    pts = [(x + 12, y + h - 22), (x + 48, y + h - 44),
           (x + 84, y + h - 36), (x + 120, y + h - 62)]
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for t in range(steps + 1):
            px = int(x1 + (x2 - x1) * t / steps)
            py = int(y1 + (y2 - y1) * t / steps)
            fill_rect(buf, px - 2, py - 2, 5, 5, (120, 220, 120))


def draw_warning(buf, x, y, w, h):
    """A hazard triangle over a bunker (Iowa)."""
    fill_rect(buf, x, y, w, h, WARNBG)
    # bunker dome
    fill_circle(buf, x + w // 2, y + h - 34, 42, (120, 120, 120))
    fill_rect(buf, x + w // 2 - 42, y + h - 34, 84, 34, (120, 120, 120))
    fill_rect(buf, x + w // 2 - 8, y + h - 22, 16, 22, (60, 60, 60))
    # warning triangle
    cx, cy = x + w // 2, y + 62
    fill_polygon(buf, [(cx, cy - 44), (cx - 46, cy + 34), (cx + 46, cy + 34)],
                 (255, 193, 7))
    fill_polygon(buf, [(cx, cy - 34), (cx - 36, cy + 26), (cx + 36, cy + 26)],
                 (0, 0, 0))
    fill_polygon(buf, [(cx, cy - 28), (cx - 30, cy + 20), (cx + 30, cy + 20)],
                 (255, 193, 7))
    fill_rect(buf, cx - 3, cy - 14, 6, 22, (0, 0, 0))
    fill_rect(buf, cx - 3, cy + 12, 6, 6, (0, 0, 0))


def draw_court(buf, x, y, w, h):
    """A courthouse with columns and the Spanish flag (Puigdemont)."""
    fill_rect(buf, x, y, w, h, COURTBG)
    # flag pole + Spanish flag
    fill_rect(buf, x + 14, y + 14, 4, 66, (90, 90, 90))
    fill_rect(buf, x + 18, y + 14, 44, 8, (170, 21, 27))
    fill_rect(buf, x + 18, y + 22, 44, 12, (255, 198, 11))
    fill_rect(buf, x + 18, y + 34, 44, 8, (170, 21, 27))
    # pediment
    fill_polygon(buf, [(x + 30, y + 84), (x + w - 30, y + 84),
                       (x + w // 2, y + 52)], (160, 156, 148))
    # columns
    for i in range(4):
        colx = x + 34 + i * 26
        fill_rect(buf, colx, y + 86, 12, 62, (210, 206, 196))
    # steps
    fill_rect(buf, x + 24, y + 150, w - 48, 8, (150, 146, 138))
    fill_rect(buf, x + 18, y + 158, w - 36, 8, (140, 136, 128))
    fill_rect(buf, x + 12, y + 166, w - 24, 8, (130, 126, 118))


# ------------------------------------------------------------------- page
def build_page():
    buf = new_canvas()

    # ---- masthead ------------------------------------------------------
    fill_rect(buf, 0, 0, W, 116, NAVY)
    name = "THE WORLD TODAY"
    draw_text(buf, (W - text_width(name, 7)) // 2, 16, name, 7, WHITE)
    date = "TUESDAY, 24 NOVEMBER 2026"
    draw_text(buf, (W - text_width(date, 3)) // 2, 72, date, 3, GOLD)
    tag = "FIVE STORIES FROM FIVE REGIONS"
    draw_text(buf, (W - text_width(tag, 2)) // 2, 98, tag, 2,
              (200, 200, 200))
    fill_rect(buf, 0, 116, W, 4, GOLD)

    # ---- lead story ----------------------------------------------------
    draw_text(buf, 24, 134, "UKRAINE - PEACE TALKS", 2, RED)
    draw_text(buf, 24, 158, "ZELENSKY PRESSES ALLIES AS", 4, INK)
    draw_text(buf, 24, 194, "TRUMP'S 28-POINT PEACE PLAN", 4, INK)
    draw_text(buf, 24, 230, "SPLITS EUROPE", 4, INK)

    # lead illustration panel: globe, dove, three flags
    fill_rect(buf, 24, 280, 560, 268, NAVY2)
    fill_circle(buf, 470, 300, 26, GOLD)  # low sun
    draw_globe(buf, 210, 414, 92)
    draw_dove(buf, 430, 380, 2)
    draw_flag_ukraine(buf, 60, 500, 66, 38)
    draw_flag_eu(buf, 150, 500, 66, 38)
    draw_flag_us(buf, 240, 500, 66, 38)
    draw_text(buf, 330, 512, "STOCKHOLM", 2, WHITE)

    # lead summary
    draw_text(buf, 608, 282, "STOCKHOLM", 2, RED)
    lead = ("Ukraine's president addressed the Crimea Platform summit in "
            "Stockholm as European leaders weighed the US plan. Kyiv rejects "
            "any deal that hands Russia the land it seized.")
    draw_text_block(buf, 608, 310, lead, 2, BODY, 392, line_gap=6)

    # ---- divider -------------------------------------------------------
    fill_rect(buf, 24, 564, 976, 3, GOLD)

    # ---- four secondary stories (2 x 2 grid) ---------------------------
    cells = [
        # (x, y, kicker, kicker colour, headline, summary, illustrator)
        (24, 580, "VENEZUELA", RED,
         "US CALLS CARTEL DE LOS SOLES A TERROR GROUP",
         "Washington designates the cartel tied to Maduro; US strikes on "
         "alleged drug boats pass 21 since September.",
         draw_ship),
        (512, 580, "TECH", (34, 139, 34),
         "HUANG BACK AS NVIDIA CHIEF AFTER TRUMP STEPS IN",
         "The chipmaker's founder returns as chief executive as the firm "
         "faces a US securities regulator inquiry.",
         draw_chip),
        (24, 792, "UNITED STATES", RED,
         "TRUMP HALTS ARMY PLAN TO BLOW UP TOXIC STOCKPILE",
         "Five tonnes of unstable lead azide will stay buried at an Iowa "
         "munitions plant until a court and the governor agree.",
         draw_warning),
        (512, 792, "SPAIN", RED,
         "SPAIN DROPS ALL CHARGES AGAINST PUIGDEMONT",
         "The Supreme Court halts the case under an amnesty law, clearing "
         "the exiled Catalan leader's return before the election.",
         draw_court),
    ]
    for (cx, cy, kicker, kcolor, headline, summary, illustrator) in cells:
        illustrator(buf, cx, cy, 150, 196)
        tx = cx + 166
        tw = 488 - 166
        draw_text(buf, tx, cy + 6, kicker, 2, kcolor)
        draw_text_block(buf, tx, cy + 28, headline, 2, INK, tw, line_gap=4)
        # summary starts below the headline (2 lines at scale 2)
        draw_text_block(buf, tx, cy + 28 + 2 * 18 + 10, summary, 2, BODY,
                        tw, line_gap=4)

    # ---- footer: where the stories were reported -----------------------
    fill_rect(buf, 24, 992, 976, 2, GOLD)
    src = "SOURCES: CBC NEWS, CNN, FRANCE 24, DAILY CALLER, TASR"
    draw_text(buf, (W - text_width(src, 2)) // 2, 1000, src, 2, GREY)

    return buf


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    buf = build_page()
    png = write_png(os.path.join(outdir, "entry.png"), buf)
    # byte-identical copy under the cover name the brief asked for
    with open(os.path.join(outdir, "entry.png"), "rb") as f:
        data = f.read()
    with open(os.path.join(outdir, "cover.jpg"), "wb") as f:
        f.write(data)
    print("wrote entry.png (%d bytes) + cover.jpg copy" % png)


if __name__ == "__main__":
    main()
