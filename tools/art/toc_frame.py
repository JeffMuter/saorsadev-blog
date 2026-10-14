"""Post TOC panel: a 9-slice game-menu frame + Oggie peeking over its top edge.
Writes static/toc-frame.png (27x27, 9x9 grid at 3x; CSS border-image slices it)
and static/toc-peek.png (Oggie's head and wing tips, 54x10 grid at 3x)."""
from PIL import Image
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
S = os.path.join(ROOT, 'static') + '/'
SCALE = 3
C = {'O': (34, 20, 4), 'G': (255, 176, 0), 'g': (201, 133, 0), 'Y': (255, 211, 106),
     'E': (255, 227, 160), 'k': (60, 30, 0), 'K': (190, 100, 10), 'L': (255, 211, 106),
     'D': (138, 90, 0), 'Q': (138, 90, 0), 'f': (255, 227, 160)}
def render(rows, name):
    h, w = len(rows), len(rows[0])
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch != '.': im.putpixel((i, j), C[ch] + (255,))
    im.resize((w * SCALE, h * SCALE), Image.NEAREST).save(S + name)
    return im

# frame: notched corners, dim outer line, bright inner line
render([".DDDDDDD.",
        "DGGGGGGGD",
        "DG.....GD",
        "DG.....GD",
        "DG.....GD",
        "DG.....GD",
        "DG.....GD",
        "DGGGGGGGD",
        ".DDDDDDD."], 'toc-frame.png')

# Oggie, same drawing as the banner frog (head rows + wing tips only)
frog_half = [
    "....OOOOOO...", "..OOGGGGGGOOO", ".OGGEEEEEEGGG", ".OGEEkkkkEEGG",
    ".OGEkEEEEkEGG", ".OGEEEEEEEEGG", ".OGGEEEEEEGGG", "OLGGGGkGGGGGG",
    "OGKKGGGkkkkkk", "OGGGGGGGGGGGG"]
wing = [
    ".QQQ..........", ".QffQQ........", ".QffffQQ......", ".QffffffQQ....",
    ".QQfffffffQ...", "QQfQQQfffffQ..", "QfffffffffffQ.", "QfffffffffffQ.",
    ".QfffffQQQfffQ", "..QQffQfffQffQ"]
rows = []
for f, w in zip(frog_half, wing):
    left = w + f + f[::-1] + w[::-1]
    rows.append(left)
render(rows, 'toc-peek.png')
