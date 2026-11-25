"""The Meridian -- front page for Wednesday 25 November 2026.

Draws a 1024x1024 newspaper front page with PIL and writes entry.png.
Deterministic: no network, no clock, no randomness. The program reads
only the font files shipped in assets/ beside it.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (26, 26, 26)
PAPER = (247, 243, 234)
RED = (163, 18, 18)
RULE = (130, 125, 115)
BLUE = (38, 58, 86)
SKY = (214, 226, 232)

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")


def load_font(filename, size, system_fallback):
    """Load a font: repo asset first, then the system copy, then PIL default."""
    for path in (os.path.join(ASSETS, filename), system_fallback):
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def serif_bold(size):
    return load_font("DejaVuSerif-Bold.ttf", size,
                     "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")


def serif(size):
    return load_font("DejaVuSerif.ttf", size,
                     "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")


def sans(size):
    return load_font("DejaVuSans.ttf", size,
                     "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def sans_bold(size):
    return load_font("DejaVuSans-Bold.ttf", size,
                     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    """Draw lines top-left at (x, y); returns the y below the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_skyline(draw, x, y, width, height):
    """Flat Shanghai-style skyline silhouette with a red seal sun."""
    draw.rectangle([x, y, x + width, y + height], fill=SKY)
    towers = [(0, 0.42), (0.09, 0.30), (0.17, 0.55), (0.26, 0.22),
              (0.33, 0.48), (0.42, 0.34), (0.50, 0.58), (0.58, 0.26),
              (0.66, 0.46), (0.74, 0.36), (0.83, 0.52), (0.91, 0.40)]
    for fx, fh in towers:
        tx = x + int(fx * width)
        tw = int(width * 0.075)
        th = int(height * fh)
        draw.rectangle([tx, y + height - th, tx + tw, y + height], fill=BLUE)
    # Oriental Pearl-style tower: slim spire with two spheres.
    cx = x + int(width * 0.30)
    draw.rectangle([cx - 3, y + int(height * 0.18), cx + 3, y + height],
                   fill=BLUE)
    draw.ellipse([cx - 12, y + int(height * 0.30), cx + 12,
                  y + int(height * 0.30) + 24], fill=BLUE)
    draw.ellipse([cx - 8, y + int(height * 0.58), cx + 8,
                  y + int(height * 0.58) + 16], fill=BLUE)
    # Red seal sun.
    sx, sy, sr = x + width - 52, y + 34, 26
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=RED)
    draw.text((sx - 8, sy - 11), "*", font=sans_bold(22), fill=PAPER)


LEAD_HEADLINE = ["Shanghai party chief falls",
                 "in Xi's widening purge"]
LEAD_DECK = ("Chen Jining, 62, is the fourth Politburo member probed "
             "since 2025 - the first sitting Shanghai boss investigated "
             "since 2006.")

STORIES = [
    ("CONGO", "WHO flees Ebola hospital as fighting closes in",
     "Staff sheltered three days in a maternity ward in Ituri before "
     "evacuation; the Ebola team has pulled out of Mongbwalu."),
    ("UNITED NATIONS", "Five women an hour killed by partners or family",
     "UN counts 47,000 such killings in 2025 - 60% of all female "
     "homicides - as its 16 Days campaign opens."),
    ("UNITED STATES", "Huawei guilty in US trade-secrets trial",
     "A New York jury convicts the telecom giant on 10 of 12 counts, "
     "including bank fraud and theft of trade secrets."),
    ("UKRAINE", "Kyiv owns Baltic ship strike; Moscow cries terror",
     "Zelenskiy confirms the drone attack on a Russian cargo ship as "
     "Russia warns of severe consequences."),
    ("MIDDLE EAST", "Houthis hit Riyadh's tallest tower; 11 hurt",
     "Saudi civil defence says the PIF Tower was struck as the Houthis "
     "push toward Aden."),
    ("WASHINGTON", "Giuliani awarded the Medal of Freedom",
     "Trump bestows the top US civilian honour on his longtime ally "
     "at the White House."),
    ("BUSINESS", "Shein to pay $100m over shopping claims",
     "The FTC says the retailer hid bad reviews and broke shipping "
     "promises; Shein denies wrongdoing."),
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 36  # side margin

    # Masthead.
    draw.line([(mx, 26), (W - mx, 26)], fill=INK, width=3)
    mast = serif_bold(62)
    draw.text((W // 2, 34), "THE MERIDIAN", font=mast, fill=INK,
              anchor="ma")
    date_font = sans_bold(20)
    draw.text((W // 2, 108), "WEDNESDAY, 25 NOVEMBER 2026",
              font=date_font, fill=INK, anchor="ma")
    draw.line([(mx, 138), (W - mx, 138)], fill=INK, width=2)

    # Lead story.
    y = 152
    draw.text((mx, y), "CHINA  --  PURGE WIDENS", font=sans_bold(17),
              fill=RED)
    y = 178
    head_font = serif_bold(54)
    y = draw_lines(draw, mx, y, LEAD_HEADLINE, head_font, INK, 62)
    y += 6
    deck_font = sans(21)
    deck_lines = wrap(draw, LEAD_DECK, deck_font, W - 2 * mx)
    y = draw_lines(draw, mx, y, deck_lines, deck_font, INK, 28)
    draw_skyline(draw, mx, y + 10, W - 2 * mx, 46)
    draw.line([(mx, y + 66), (W - mx, y + 66)], fill=RULE, width=1)

    # Story grid: two columns, left 4 stories, right 3. The grid must
    # end above the footer rule at y=972; fail loudly if it does not.
    grid_top = y + 82
    col_w = 464
    cols = [(mx, STORIES[:4]), (W - mx - col_w, STORIES[4:])]
    block_h, gap = 118, 10
    grid_bottom = grid_top
    for cx, stories in cols:
        by = grid_top
        for kicker, headline, deck in stories:
            draw.text((cx, by), kicker, font=sans_bold(15), fill=RED)
            h_font = serif_bold(25)
            h_lines = wrap(draw, headline, h_font, col_w)
            hy = draw_lines(draw, cx, by + 20, h_lines[:2], h_font,
                            INK, 29)
            d_font = sans(16)
            d_lines = wrap(draw, deck, d_font, col_w)
            draw_lines(draw, cx, hy + 2, d_lines[:2], d_font, INK, 21)
            by += block_h + gap
        grid_bottom = max(grid_bottom, by - gap)
    if grid_bottom > 966:
        raise ValueError("story grid overflows into the footer")

    # Footer.
    draw.line([(mx, 972), (W - mx, 972)], fill=INK, width=2)
    foot = sans(13)
    draw.text((W // 2, 980),
              "THE MERIDIAN  --  Every story verified against reporting "
              "of 25 November 2026.",
              font=foot, fill=INK, anchor="ma")
    return img


def validate(img, path):
    """Gate checks, run before the entry is accepted: exact size, file
    size, every headline fits its two lines, and the lead headline still
    carries ink when the page is shrunk to the judges' ~300px test size."""
    if img.size != (W, H):
        raise ValueError("bad size %r, want 1024x1024" % (img.size,))
    if os.path.getsize(path) > 1048576:
        raise ValueError("entry.png over the 1 MiB limit")
    probe = ImageDraw.Draw(Image.new("RGB", (W, H), PAPER))
    for kicker, headline, deck in STORIES:
        if len(wrap(probe, headline, serif_bold(25), 464)) > 2:
            raise ValueError("headline overflows two lines: %r" % headline)
    if len(LEAD_HEADLINE) != 2:
        raise ValueError("lead headline must be exactly two lines")
    small = img.resize((300, 300), Image.LANCZOS).convert("L")
    lead = small.crop((10, 50, 290, 110))
    dark = sum(1 for px in lead.getdata() if px < 120)
    if dark < 200:
        raise ValueError("lead headline unreadable at 300px")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = render()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    validate(img, path)
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
