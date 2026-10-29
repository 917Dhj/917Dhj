"""Regenerate the profile assets and the offline README preview.

    python tools/build.py

Writes:
    assets/hj-pixel.png, assets/hj-pixel.gif   the pixel avatar
    tools/preview/preview.html                 GitHub-ish offline preview

README.md is the source of truth and is never rewritten here.
"""
from pathlib import Path
import math
import mistune
from PIL import Image, ImageColor, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets'
PREVIEW = ROOT / 'tools' / 'preview'
ASSETS.mkdir(exist_ok=True)
PREVIEW.mkdir(parents=True, exist_ok=True)

COL = {'ink': '#2B3440', 'clay': '#D97757', 'blue': '#2B8FFF', 'brass': '#C8923A',
       'paper': '#F8F7F3', 'light': '#E7E9E8', 'silver': '#C4CCD0', 'mint': '#78BCAE',
       'screen': '#222F3B', 'gray': '#67727B', 'white': '#FFFFFF', 'cream': '#F3EEE6',
       'cream_shade': '#DCD3C4', 'clay_dark': '#B65A3D', 'clay_light': '#F2A98A',
       'brass_dark': '#94672A', 'amber': '#E8A55A', 'glare': '#3A4D5E',
       'blue_light': '#9CCBFF', 'silver_dark': '#9AA5AB'}


# One character per pixel on a 32x32 grid, so every block scales to the same
# 8px square. Light comes from the top left: highlights there, shade bottom right.
SPRITE = (
    '................................',
    '..............KKKK..............',
    '.............KhhRRK.............',
    '.............KhRRRK.............',
    '.............KRRRQK.............',
    '..............KKKK..............',
    '..............KWLK..............',
    '..............KWLK..............',
    '........KKKKKKKKKKKKKKKK........',
    '......KKWWWWWWWWWWWWWWCCKK......',
    '.....KWWCCCCCCCCCCCCCCCCCSK.....',
    '.....KWCCKKKKKKKKKKKKKKCCSK.....',
    '.....KWCKNggNNNNNNNNNNNKCSK.....',
    '..KK.KWCKNgNbBNNNNbBNNNKCSK.KK..',
    '.KyaKKWCKNNNBBNNNNBBNNNKCSKKyaK.',
    '.KAaKKWCKNNNBBNNNNBBNNNKCSKKAaK.',
    '.KAaKKCCKNNNNNNNNNNNNNNKCSKKAaK.',
    '.KAaKKCCKNrrNBNNNNBNrrNKCSKKAaK.',
    '..KK.KCCKNNNNNBBBBNNNNNKCSK.KK..',
    '.....KCCKNNNNNNNNNNNNNNKCSK.....',
    '.....KCCCKKKKKKKKKKKKKKCCSK.....',
    '.....KCCCCCCCCCCCCCCCMMCCSK.....',
    '.....KSCCCCCCCCCCCCCCCCCSSK.....',
    '......KKSSSSSSSSSSSSSSSSKK......',
    '........KKKKKKKKKKKKKKKK........',
    '.............KGGGGK.............',
    '..........KKKKKKKKKKKK..........',
    '.........KWWLLLLLLLLLLK.........',
    '........KWLLBBLLRRLLBBDK........',
    '........KLLLLLLLQQLLLLDK........',
    '........KKKKKKKKKKKKKKKK........',
    '.......llllllllllllllllll.......',
)
SPRITE_INK = {'K': 'ink', 'W': 'white', 'C': 'cream', 'S': 'cream_shade',
              'R': 'clay', 'Q': 'clay_dark', 'h': 'clay_light', 'r': 'clay_light',
              'A': 'brass', 'a': 'brass_dark', 'y': 'amber',
              'N': 'screen', 'g': 'glare', 'B': 'blue', 'b': 'blue_light',
              'M': 'mint', 'G': 'gray', 'L': 'silver', 'D': 'silver_dark', 'l': 'light'}
EYES = ((12, 13), (18, 19))


def draw_map(rows):
    """Paint a character map, one pixel per character, '.' left transparent."""
    im = Image.new('RGBA', (len(rows[0]), len(rows)), (0, 0, 0, 0))
    px = im.load()
    for y, row in enumerate(rows):
        assert len(row) == len(rows[0]), (y, row)
        for x, ch in enumerate(row):
            if ch != '.':
                px[x, y] = ImageColor.getcolor(COL[SPRITE_INK[ch]], 'RGBA')
    return im


def pixel_sprite(blink=False, led=True):
    im = draw_map(SPRITE)
    px = im.load()
    if blink:
        # Eyes close to a single line on their bottom row.
        for xs in EYES:
            for x in xs:
                for y in (13, 14):
                    px[x, y] = px[9, 15]
    if not led:
        for x in (21, 22):
            px[x, 21] = px[9, 21]
    return im


# The avatar floats left of the heading, and GitHub gives floated images no
# margin. The gap is therefore baked into the file as transparent columns.
AVATAR_SIZE, AVATAR_PAD_RIGHT = 256, 35

_frames = [pixel_sprite(blink=(i in (12, 13)), led=(i not in (4, 5, 6, 13)))
           for i in range(18)]
frames = []
for f in _frames:
    canvas_im = Image.new('RGBA', (AVATAR_SIZE + AVATAR_PAD_RIGHT, AVATAR_SIZE), (0, 0, 0, 0))
    canvas_im.paste(f.resize((AVATAR_SIZE, AVATAR_SIZE), Image.Resampling.NEAREST), (0, 0))
    frames.append(canvas_im)
frames[0].save(ASSETS / 'hj-pixel.png')

# Project icons: 16x16 maps in the avatar's palette and outline, so the four
# entries under "What I ship" read as one set. Shown at 24px; the 96px file
# lands on whole pixels at 2x and 3x.
ICONS = {
    # a page of notes under a magnifier
    'deeppapernote': (
        '................',
        '.KKKKKKKKK......',
        '.KWWWWWWWKK.....',
        '.KWCCCCCCKSK....',
        '.KWGGGGGCKKKK...',
        '.KWCCCCCCCCSK...',
        '.KWGGGGGGGCSK...',
        '.KWCCCCKKKKSK...',
        '.KWGGGKWbbbKK...',
        '.KWCCCKbbbbKK...',
        '.KWGGCKbbbbKK...',
        '.KWCCCKbbbbKK...',
        '.KSSSSSKKKKRK...',
        '.KKKKKKKKKKKRR..',
        '............RRQ.',
        '.............QQ.',
    ),
    # the avatar's screen face under a chef's hat
    'dkitchen': (
        '.....KK..KK.....',
        '...KKWWKKWWKK...',
        '..KWWWWWWWWWSK..',
        '..KWWWWWWWWWSK..',
        '...KWWWWWWWSK...',
        '...KLLLLLLLDK...',
        '..KKKKKKKKKKKK..',
        '..KWCCCCCCCCSK..',
        '..KCKKKKKKKKSK..',
        '..KCKNBNNBNKSK..',
        '..KCKNBNNBNKSK..',
        '..KCKNNBBNNKSK..',
        '..KCKKKKKKKKSK..',
        '..KSSSSSSSSSSK..',
        '...KKKKKKKKKK...',
        '................',
    ),
    # one task in, routed to three specialists
    'diverter': (
        '................',
        '...........KKKK.',
        '.......GGGGKhRK.',
        '.......GGGGKRQK.',
        '.......GG..KKKK.',
        'KKKKKK.GG.......',
        'KBCCSK.GG..KKKK.',
        'KCBCSGGGGGGKbBK.',
        'KCBCSGGGGGGKBBK.',
        'KBCCSK.GG..KKKK.',
        'KKKKKK.GG.......',
        '.......GG..KKKK.',
        '.......GGGGKyAK.',
        '.......GGGGKAaK.',
        '...........KKKK.',
        '................',
    ),
    # a note pulled down from the menu bar
    'draftbar': (
        '................',
        'KKKKKKKKKKKKKKKK',
        'KDDLDDLLLLRRLDDK',
        'KKKKKKKKKKKKKKKK',
        '..........KK....',
        '..KKKKKKKKKKKK..',
        '..KWWWWWWWWWWK..',
        '..KWRRCGGGGCSK..',
        '..KWCCCCCCCCSK..',
        '..KWGGGGGGGCSK..',
        '..KWCCCCCCCCSK..',
        '..KWGGGGRCCCSK..',
        '..KWCCCCCCCCSK..',
        '..KSSSSSSSSSSK..',
        '..KKKKKKKKKKKK..',
        '................',
    ),
}
for name, rows in ICONS.items():
    draw_map(rows).resize((96, 96), Image.Resampling.NEAREST).save(ASSETS / f'{name}-project.png')

EXTRA = ['#DDE2E1', '#EBC3B1', '#EDF0EF', '#F0E4DD',
         '#141413', '#3D3D3A', '#6C6A64', '#CC785C', '#E8A55A', '#E8E0D2', '#E6DFD8',
         '#CDBB9C', '#E6EDF3', '#B1BAC4', '#8B949E']


def save_gif(frames, path, frame_ms):
    """Write RGBA frames to a paletted GIF. One shared palette keeps hues stable."""
    hexes = list(dict.fromkeys(list(COL.values()) + EXTRA))
    colors = [(0, 0, 0)] + [tuple(bytes.fromhex(v.lstrip('#'))) for v in hexes]
    assert len(colors) < 256
    palette = [ch for rgb in colors for ch in rgb] + [0] * (768 - 3 * len(colors))
    lookup = {(*rgb, 255): i for i, rgb in enumerate(colors) if i > 0}
    out_frames = []
    for f in frames:
        out = Image.new('P', f.size, 0)
        out.putpalette(palette)
        out.putdata([0 if px[3] == 0 else lookup[px] for px in f.getdata()])
        out_frames.append(out)
    duration = frame_ms if isinstance(frame_ms, (list, tuple)) else [frame_ms] * len(frames)
    out_frames[0].save(path, save_all=True, append_images=out_frames[1:], duration=duration,
                       loop=0, optimize=True, disposal=2, transparency=0)


save_gif(frames, ASSETS / 'hj-pixel.gif', 300)

# --- decorative accents ------------------------------------------------------
# A 2x2 pixel cluster that breathes, used as the marker on every section heading.
# Same visual language as the avatar's status LED: alive, but never demanding.

MARK = 12
MARK_CELLS = ((1, 1), (7, 1), (1, 7), (7, 7))


def mark_frames():
    out = []
    for colour in ('#D97757', '#D97757', '#D97757', '#D97757', '#EBC3B1', '#EBC3B1'):
        im = Image.new('RGBA', (MARK, MARK), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for x, y in MARK_CELLS:
            d.rectangle((x, y, x + 3, y + 3), fill=colour)
        out.append(im)
    return out


save_gif(mark_frames(), ASSETS / 'px-mark.gif', 300)

# The band across the top of the page: pixel bars of uneven length hanging from
# the top edge, like an upside-down equaliser. Colours walk the profile palette
# left to right, so the strip doubles as the page's legend.

SCALE_W = 860
SCALE_COL, SCALE_COL_GAP = 4, 12
SCALE_RAIL, SCALE_LEAD = 2, 2
SCALE_TOP, SCALE_BOTTOM = 9, 19
SCALE_ROW = 6                      # print-head row pitch, the "printed" texture
SCALE_H = SCALE_RAIL + SCALE_LEAD + SCALE_BOTTOM
SCALE_FRAMES, SCALE_MS = 10, 300   # 10 * 300ms = 3.0s loop, deliberately stepped
SCALE_PX = 2                       # drawn at 2x so retina screens get whole pixels
# Claude's own tokens: warm ink, warm greys, coral, amber, cream. The dark-mode
# strip inverts the ink end so it does not vanish into GitHub's #0d1117, and the
# light strip ends on a deeper sand so the last bars still read on white.
SCALE_THEMES = {
    'light': ('#141413', ('#141413', '#3D3D3A', '#6C6A64', '#CC785C', '#E8A55A', '#CDBB9C')),
    'dark': ('#E6EDF3', ('#E6EDF3', '#B1BAC4', '#8B949E', '#CC785C', '#E8A55A', '#E8E0D2')),
}
SCALE_COLS = SCALE_W // (SCALE_COL + SCALE_COL_GAP)
# centre the bars under the rail so neither end overhangs
SCALE_X0 = (SCALE_W - (SCALE_COLS * (SCALE_COL + SCALE_COL_GAP) - SCALE_COL_GAP)) // 2


def scale_height(i, t):
    """Travelling wave: one dominant term carries the motion, a short one adds grain."""
    phase = 2 * math.pi * (i / 30.0 - t / SCALE_FRAMES)
    grain = 2 * math.pi * (i / 7.0 + t / SCALE_FRAMES)
    value = 0.5 + 0.40 * math.sin(phase) + 0.10 * math.sin(grain + 1.3)
    span = SCALE_BOTTOM - SCALE_TOP
    return int(max(SCALE_TOP, min(SCALE_BOTTOM, round(SCALE_TOP + span * value))))


def scale_frames(ink, palette):
    out = []
    for t in range(SCALE_FRAMES):
        im = Image.new('RGBA', (SCALE_W, SCALE_H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        # the rail is the ceiling the bars hang from; without it they read as floating
        d.rectangle((0, 0, SCALE_W - 1, SCALE_RAIL - 1), fill=ink)
        for i in range(SCALE_COLS):
            h = scale_height(i, t)
            x = SCALE_X0 + i * (SCALE_COL + SCALE_COL_GAP)
            top = SCALE_RAIL + SCALE_LEAD
            colour = palette[min(len(palette) - 1, i * len(palette) // SCALE_COLS)]
            # every print row ends in a transparent seam: the print-head rhythm,
            # and it shows the page through in either theme
            for k in range(h):
                if k % SCALE_ROW != SCALE_ROW - 1:
                    d.rectangle((x, top + k, x + SCALE_COL - 1, top + k), fill=colour)
        out.append(im.resize((SCALE_W * SCALE_PX, SCALE_H * SCALE_PX), Image.Resampling.NEAREST))
    return out


for theme, (ink, palette) in SCALE_THEMES.items():
    name = 'px-scale.gif' if theme == 'light' else 'px-scale-dark.gif'
    save_gif(scale_frames(ink, palette), ASSETS / name, SCALE_MS)

# A terminal block cursor at the very end of the page: the document stops where
# you would start typing. Blinks slower than a real caret so it reads as calm.
CARET_W, CARET_H = 7, 14
_caret_on = Image.new('RGBA', (CARET_W, CARET_H), (0, 0, 0, 0))
ImageDraw.Draw(_caret_on).rectangle((0, 1, CARET_W - 1, CARET_H - 2), fill='#D97757')
_caret_off = Image.new('RGBA', (CARET_W, CARET_H), (0, 0, 0, 0))
save_gif([_caret_on, _caret_on, _caret_off], ASSETS / 'px-caret.gif', 400)

# Offline preview: approximates GitHub's markdown typography. The real page is
# whatever github.com renders, so treat this as a layout sanity check only.
md = mistune.create_markdown(escape=False, plugins=['table', 'strikethrough'])

import sys
source = sys.argv[1] if len(sys.argv) > 1 else 'README.md'
body = md((ROOT / source).read_text(encoding='utf-8'))
out_name = 'preview.html' if source == 'README.md' else Path(source).stem + '.html'

CSS = '''
*{box-sizing:border-box}
html{background:#f6f8fa}
body{margin:0;color:#1f2328;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Arial,sans-serif;font-size:16px;line-height:1.5}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}
.wrapper{max-width:1010px;margin:24px auto 70px;padding:0 18px}
.toolbar{display:flex;justify-content:space-between;align-items:center;margin:0 6px 14px;font-size:13px;color:#59636e}
.toolbar strong{font-weight:600;color:#24292f}
.pill{font-size:11px;border-radius:20px;background:#eef2f7;color:#4a5563;padding:4px 12px;letter-spacing:.4px;font-weight:700}
.chrome{background:#fff;border:1px solid #d1d9e0;border-radius:7px;overflow:hidden;box-shadow:0 8px 24px rgba(31,35,40,.035)}
.file-header{height:45px;background:#f6f8fa;border-bottom:1px solid #d1d9e0;display:flex;align-items:center;gap:9px;padding:0 17px;color:#59636e;font-size:12px}
.dot{width:7px;height:7px;border-radius:50%;background:#8b949e}
.file-header .right{margin-left:auto;display:flex;gap:12px}
.markdown-body{padding:32px 38px;overflow-wrap:break-word}
.markdown-body>*:first-child{margin-top:0!important}
.markdown-body h1{font-size:2em;line-height:1.25;padding-bottom:.3em;border-bottom:1px solid #d8dee4;margin:24px 0 16px;font-weight:650;letter-spacing:-.8px}
.markdown-body h2{font-size:1.5em;padding-bottom:.3em;border-bottom:1px solid #d8dee4;margin:32px 0 16px;font-weight:650;letter-spacing:-.3px}
.markdown-body h3{font-size:1.25em;font-weight:650;margin:24px 0 16px;line-height:1.25}
.markdown-body p{margin:0 0 16px}
.markdown-body a:hover{color:#0550ae}
.markdown-body strong{font-weight:650}
.markdown-body code{background:#eff1f3;padding:.18em .36em;border-radius:5px;font-size:.85em;font-family:ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,monospace}
.markdown-body table{border-spacing:0;border-collapse:collapse;width:100%;margin:0 0 16px}
.markdown-body table td,.markdown-body table th{padding:6px 13px 6px 0;border:0;vertical-align:top}
.markdown-body table td:last-child{padding-right:0}
.markdown-body table td>p:last-child{margin-bottom:0}
.markdown-body img{max-width:100%;vertical-align:middle}
.markdown-body img[align="right"]{max-width:96px;margin-left:20px;image-rendering:pixelated}
.markdown-body ul{padding-left:2em;margin:0 0 16px}
.markdown-body li{margin:.4em 0}
.markdown-body sub{color:#59636e;font-size:12px}
.markdown-body blockquote{margin:0 0 16px;padding:0 1em;color:#59636e;border-left:.25em solid #d1d9e0}
.markdown-body blockquote>p{margin:0}
.markdown-body table img[src*="shields.io"],.markdown-body p img[src*="shields.io"]{image-rendering:auto}
.markdown-body hr{height:2px;margin:24px 0;background:#d8dee4;border:0}
@media(max-width:650px){
 .wrapper{margin:0 auto;padding:0}
 .toolbar{display:none}
 .chrome{border:0;border-radius:0;box-shadow:none}
 .file-header .right{display:none}
 .markdown-body{padding:21px 18px 30px;font-size:14px}
 .markdown-body h1{font-size:1.78em;letter-spacing:-.5px}
 .markdown-body h2{font-size:1.3em}
 .markdown-body img[align="right"]{width:76px;max-width:76px;margin-left:9px}
 .markdown-body table td[width]{width:88px!important;padding-right:10px}
 .markdown-body table td img{width:76px}
}
'''

HTML = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HJ Ding — GitHub profile README preview</title><style>{CSS}</style></head><body>
<main class="wrapper"><div class="toolbar"><span><strong>917Dhj</strong> / README.md</span><span class="pill">LOCAL PREVIEW</span></div>
<div class="chrome"><div class="file-header"><span class="dot"></span><strong>README.md</strong><span class="right"><span>Preview</span><span>Code</span></span></div>
<article class="markdown-body">{body}</article></div></main></body></html>'''
(PREVIEW / out_name).write_text(HTML, encoding='utf-8')
print('wrote', ASSETS / 'hj-pixel.gif', 'and', PREVIEW / out_name)
