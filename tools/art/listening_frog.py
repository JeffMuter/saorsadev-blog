"""Compose the 'listening' frog: the banner frog (static/oggie-v2.png, reused
pixel-for-pixel) wearing chunky amber/brown headphones. No text, no lilypad.
Run from anywhere; paths are relative to the repo root. Output: static/listening-frog.png (still) + static/listening-frog.gif (slow 1px nod)
Art grid is 2px per "pixel", matching the frog sprite."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
frog = Image.open(ROOT / "static/oggie-v2.png").convert("RGBA")
PAD = 6                      # extra rows on top for the headband arch
W, H = frog.size
out = Image.new("RGBA", (W, H + PAD), (0, 0, 0, 0))
out.paste(frog, (0, PAD))
d = ImageDraw.Draw(out)

BAND, HI, CUP, EDGE = "#5a3a10", "#c98500", "#ffb000", "#5a3a10"

def r(x0, y0, x1, y1, c):    # inclusive rect in 2px art units -> canvas px
    d.rectangle([x0 * 2, y0 * 2, x1 * 2 + 1, y1 * 2 + 1], fill=c)

# headband: stepped arch over the head, between the wings (art units)
r(18, 0, 31, 1, BAND)        # top bar
r(18, 0, 31, 0, HI)          # highlight on top edge
r(14, 1, 17, 2, BAND); r(32, 1, 35, 2, BAND)
r(12, 3, 13, 5, BAND);  r(36, 3, 37, 5, BAND)
r(14, 2, 15, 2, HI) ; r(34, 2, 35, 2, HI)
r(12, 6, 13, 12, BAND); r(36, 6, 37, 12, BAND)   # sides run down to the cups

# ear cups on the cheeks: outline + amber fill + small highlight
for x0 in (8, 36):
    r(x0, 10, x0 + 5, 18, EDGE)
    r(x0 + 1, 11, x0 + 4, 17, CUP)
    r(x0 + 1, 11, x0 + 1, 15, "#ffd36a")


# ---- animation + downscale ------------------------------------------------
# Work on the native grid (2px art unit -> 1px), nod the head 1 native px down,
# then scale 1.5x nearest-neighbour (75px wide; 1.4x/70px drops thin eye pixels).
nat = out.resize((W // 2, (H + PAD) // 2), Image.NEAREST)
NW, NH = nat.size
SCALE = 1.5
OUT = (round(NW * SCALE), round(NH * SCALE))

def nod(dy):
    """Head/headphones/body shift down dy native px; outer wings stay put."""
    px = nat.load()
    base = Image.new("RGBA", nat.size, (0, 0, 0, 0))
    head = Image.new("RGBA", nat.size, (0, 0, 0, 0))
    bp, hp = base.load(), head.load()
    for y in range(NH):
        for x in range(NW):
            in_head = (8 <= x <= 41) if y <= 18 else (12 <= x <= 37)
            (hp if in_head else bp)[x, y] = px[x, y]
    base.alpha_composite(head, (0, dy))
    return base

def scaled(im):
    return im.resize(OUT, Image.NEAREST)

frames = [scaled(nod(0)), scaled(nod(1))]
delays = [1800, 1600]        # slow nod: ~3.4s loop, seamless (2-frame cycle)
frames[0].save(ROOT / "static/listening-frog.png")

# palette GIF with transparent index 0, disposal 2 (no ghosting)
pal = []
for f in frames:
    for c in f.getdata():
        if c[3] and c[:3] not in pal:
            pal.append(c[:3])
flat = [0, 0, 0] + [v for c in pal for v in c]
flat += [0] * (768 - len(flat))
pimgs = []
for f in frames:
    q = Image.new("P", f.size, 0)
    q.putpalette(flat)
    q.putdata([0 if c[3] == 0 else pal.index(c[:3]) + 1 for c in f.getdata()])
    pimgs.append(q)
pimgs[0].save(ROOT / "static/listening-frog.gif", save_all=True,
              append_images=pimgs[1:], duration=delays, loop=0,
              transparency=0, disposal=2, optimize=False)
