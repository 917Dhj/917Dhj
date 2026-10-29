# tools

Build helpers for this profile repo. Nothing here ships to the rendered page — the two
READMEs and `assets/` are the whole deliverable.

```bash
python -m pip install pillow mistune playwright
python -m playwright install chromium

python tools/build.py           # regenerate the avatar + tools/preview/preview.html
python tools/render_preview.py  # screenshot it at desktop and mobile widths
```

Output lands in `tools/preview/` (git-ignored): `preview.html`, `desktop.png`, `mobile.png`.

## What is generated vs. what is committed

- `assets/hj-pixel.gif` and `assets/hj-pixel.png` — the avatar, drawn from scratch in `build.py`
  as a 32×32 character map (`SPRITE`), one character per pixel, scaled 8× with nearest-neighbour.
  The canvas is 291×256: the extra 35 columns on the right are transparent padding, because
  GitHub gives floated images no margin and the avatar sits left of the heading.
- `assets/px-mark.gif` — the breathing pixel marker used in section headings, also generated.
- `assets/px-caret.gif` — the blinking terminal cursor that closes the page.
- `assets/px-scale.gif` and `assets/px-scale-dark.gif` — the animated print-head wave across the top,
  swapped by a `<picture>` on `prefers-color-scheme`. 4px columns on a 16px pitch (53 bars),
  transparent 1px row seams every 6px, gentle 9–19px amplitude, 10 frames at 300ms (deliberately
  stepped). Drawn at 2× (1720×46) and shown at `width="860"` with no height, so it scales in
  proportion on narrow screens. Light: `#141413` ink → `#3D3D3A` → `#6C6A64` → `#CC785C` coral →
  `#E8A55A` amber → `#CDBB9C` sand. Dark swaps the ink end for `#E6EDF3` → `#B1BAC4` → `#8B949E`
  and ends on `#E8E0D2` cream.
- `assets/*-project.png` — the project icons, 16×16 character maps (`ICONS` in `build.py`) in the
  avatar's palette, exported at 96px and shown at 24px.
- `README.md` — hand-written source of truth. `build.py` only reads it.
- `README.zh-CN.md` — Chinese translation, deliberately **not published**: it is listed in
  `.git/info/exclude` so it stays local. Remove that line when you want to ship it.

## Before pushing

The preview is an approximation of GitHub's markdown typography, not a replica. Open the real
profile once after pushing and check light mode, dark mode, and a narrow window.

Star counts live only in the shields.io badges at the top, so nothing there drifts. The version
and release numbers in each project's subtitle (`PyPI 0.5.8 · 17 releases`, `v2.0.3`) are still
hand-written: bump them when you cut a release.
