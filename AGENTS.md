# saorsadev-blog

Hugo site (theme: Digio, vendored in `themes/digio/`, never edited). Site-level overrides live in
`layouts/`, `static/` and `static/css/amber.css`. Visual identity: amber (`#ffb000`, `#c98500`) on
near-black (`#0b0b08`), chunky pixel art, VT323 headings, serif body.

## Making pixel art / images (read before touching any image)

Claude cannot generate images directly. All art here is **drawn by Python scripts** and judged by looking
at the result. Do not use image-generation models, and do not hand-edit PNG/GIF files.

Tools:
- **Python + Pillow** draws everything. Pillow is not installed globally; run scripts with
  `nix-shell -p 'python3.withPackages(p:[p.pillow])' --run 'python3 tools/art/<script>.py'`
- **Generators** (in `tools/art/`, run from the repo root, write into `static/`):
  - `portrait.py` -> `static/portrait-hero.gif` + `static/portrait-hero.png` (hero animation, 96-frame seamless loop; the portrait panel only, 188x188. The Recent/Topics boxes beside it are HTML in `layouts/home.html`. Filenames are versioned on purpose: renaming busts browser caches)
  - `banner.py` -> `static/border-home1.png` (frog banner) + `static/oggie-v2.png` (frog + wings sprite)
  - `listening_frog.py` -> `static/listening-frog.gif` (slow 1px head nod, 75px) + `static/listening-frog.png` (still first frame, reduced-motion fallback); banner frog with headphones, reuses `oggie-v2.png`
  Edit the script and re-run; both outputs are deterministic, so re-running without edits is a no-op.
- **Look at output with the `Read` tool** on the PNG (composite onto `#0b0b08` and upscale with
  nearest-neighbour first so small sprites are legible). Read individual GIF frames the same way.
- **Check on the real page** with headless Chromium and a cache-busting query:
  `chromium --headless --no-sandbox --disable-gpu --screenshot=shot.png --window-size=1000,720 --virtual-time-budget=3000 "http://localhost:1313/?v=$RANDOM"`
- **Dev server**: `nix shell nixpkgs#hugo -c hugo server -D --bind 0.0.0.0 --port 1313` (Hugo extended,
  v0.152.2 works; `layouts/baseof.html` is a compatibility patch for it).

Rules of thumb:
- Hand-author sprites as pixel grids, scale only with nearest-neighbour, stay on one chunky grid
  (2-3px blocks); fine 1px detail looks out of place next to the panels and text.
- Keep every colour in the amber/brown/black family. Exception: none; the banner is amber too.
- The theme tints `.png` images with a CSS filter; `amber.css` exempts `portrait.*`,
  `border-home1.png` and `listening-frog.png`/`.gif`, so art for those must already be in-palette. Check the filter rules in
  `static/css/amber.css` before adding any new image.
- Text belongs in HTML, not baked into images (use real headings next to a sprite).
- `static/border-home1.png` (frog banner) is approved; don't change it without being asked.
- Use `prefers-reduced-motion` fallbacks for animation (`portrait-hero.png` is the static frame).
