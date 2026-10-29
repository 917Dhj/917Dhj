"""Screenshot tools/preview/preview.html at desktop and mobile widths.

    python tools/render_preview.py

Writes tools/preview/desktop.png and tools/preview/mobile.png (git-ignored).
Requires: pip install playwright && python -m playwright install chromium
"""
import asyncio
import base64
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = ROOT / 'tools' / 'preview'
MIME = {'png': 'image/png', 'gif': 'image/gif', 'svg': 'image/svg+xml'}


def embed_assets(html: str) -> str:
    for f in (ROOT / 'assets').iterdir():
        if f.is_file():
            mime = MIME.get(f.suffix[1:], 'application/octet-stream')
            uri = 'data:' + mime + ';base64,' + base64.b64encode(f.read_bytes()).decode('ascii')
            html = html.replace('./assets/' + f.name, uri)
    return html


async def main():
    html = embed_assets((PREVIEW / 'preview.html').read_text(encoding='utf-8'))
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        for name, w, h, scale in [('desktop', 1240, 980, 1.5), ('mobile', 390, 844, 2)]:
            page = await browser.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale)
            await page.set_content(html, wait_until='domcontentloaded')
            await page.evaluate(
                "() => Promise.all(Array.from(document.images).map(img => img.complete"
                " ? Promise.resolve() : new Promise(r => { img.onload = r; img.onerror = r; })))"
            )
            await page.screenshot(path=str(PREVIEW / f'{name}.png'), full_page=True, animations='disabled')
            print(name, await page.evaluate(
                "() => ({w: document.body.scrollWidth, h: document.body.scrollHeight,"
                " broken: Array.from(document.images).filter(i => !i.naturalWidth).map(i => i.alt || i.src)})"
            ))
            await page.close()
        await browser.close()


asyncio.run(main())
