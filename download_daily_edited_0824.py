# -*- coding: utf-8 -*-
"""Download edited images from CDN, convert to JPG on white bg, save to images/<slug>.jpg (day 0824)."""
import os, io, urllib.request
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

# slug -> edited CDN URL (hex-key-set and jigsaw keep original downloads)
edited = {
    'stainless-corner-brace-40mm': 'https://sc02.alicdn.com/kf/A08dd5484f8224f5a9aa19ce396c5362ez.png',
    'no-drill-heavy-duty-shelf-bracket': 'https://sc02.alicdn.com/kf/Aa6b1833765254d07af8b04c5d8f36dab3.png',
    'adjustable-l-bracket-58mm': 'https://sc02.alicdn.com/kf/Ae7a11d9240184a5b88e5fe14db99918cz.png',
    'bakelite-grip-claw-hammer': 'https://sc02.alicdn.com/kf/A61cff0005c724831a5d7bd7700d6b527d.png',
    'dual-temperature-heat-gun-110v': 'https://sc02.alicdn.com/kf/A719e8a20062d4f4d9f3a9f62efafba6bx.png',
    'hot-air-rework-station-858d': 'https://sc02.alicdn.com/kf/Aba42a804028f4204b7054aec49834d78r.png',
    'pistol-air-screwdriver-5h': 'https://sc02.alicdn.com/kf/Aae793dbcfd1d49b3aa21b41f3165bb48g.png',
    '5-inch-air-polisher': 'https://sc02.alicdn.com/kf/Aee4ecbfde5914ca6b7f0a1d3f1e89425i.png',
}

report = []
ok = fail = 0
for slug, url in edited.items():
    out = os.path.join(IMG_DIR, slug + '.jpg')
    try:
        req = urllib.request.Request(url, headers=UA)
        data = urllib.request.urlopen(req, timeout=30).read()
        img = Image.open(io.BytesIO(data))
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGBA')
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert('RGB')
        img.save(out, 'JPEG', quality=92)
        sz = os.path.getsize(out)
        ok += 1
        report.append('%s: %d bytes, %s -> saved' % (slug, sz, str(img.size)))
    except Exception as e:
        fail += 1
        report.append('%s: FAIL %s' % (slug, e))

io.open(os.path.join(BASE, 'download_daily_edited_report_0824.txt'), 'w', encoding='utf-8').write('\n'.join(report))
print('OK=%d FAIL=%d' % (ok, fail))
