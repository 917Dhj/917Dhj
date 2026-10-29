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

- `assets/hj-pixel.gif` and `assets/hj-pixel.png` — the avatar, drawn from scratch in `build.py`.
  The canvas is 291×256: the extra 35 columns on the right are transparent padding, because
  GitHub gives floated images no margin and the avatar sits left of the heading.
- `assets/px-mark.gif` — the breathing pixel marker used in section headings, also generated.
- `assets/px-caret.gif` — the blinking terminal cursor that closes the page.
- `assets/px-scale.gif` — the animated print-head wave across the top. 4px columns on a 16px pitch
  (53 bars), 6px row seams, gentle 9–19px amplitude,
  10 frames at 300ms (deliberately stepped). Colours are Claude's design tokens:
  `#141413` ink → `#3D3D3A` → `#6C6A64` → `#CC785C` coral → `#E8A55A` amber → `#E8E0D2` cream,
  with `#E6DFD8` as the seam.
- `assets/*-project.png` — 128px icons derived from each project's own artwork. Commit them;
  `tools/assets-src/` holds the full-resolution originals locally (git-ignored) if you want to re-export.
- `README.md` — hand-written source of truth. `build.py` only reads it.
- `README.zh-CN.md` — Chinese translation, deliberately **not published**: it is listed in
  `.git/info/exclude` so it stays local. Remove that line when you want to ship it.

## Before pushing

The preview is an approximation of GitHub's markdown typography, not a replica. Open the real
profile once after pushing and check light mode, dark mode, and a narrow window.

Two numbers are hardcoded and will drift: `1.2k★` in both READMEs. The shields.io badges at the
top are live, so bump the hardcoded figure only when it is visibly out of date.
