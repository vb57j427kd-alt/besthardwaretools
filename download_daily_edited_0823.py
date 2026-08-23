# -*- coding: utf-8 -*-
"""Download edited images from CDN, convert to JPG on white bg, save to images/<slug>.jpg (day 0823)."""
import os, io, urllib.request
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

# slug -> edited CDN URL (rectangular-air-sander keeps original, no edit needed)
EDITED = {
    'soft-close-drawer-slide-45mm': 'https://sc02.alicdn.com/kf/A86dd240302ce460284ce0bd6f42157cfG.png',
    'no-drill-magnetic-door-stop': 'https://sc02.alicdn.com/kf/Ac6f217a9e30f4929b98e87d359f5dc24K.png',
    'magnetic-glass-door-catch': 'https://sc02.alicdn.com/kf/Abb7eeb9c1bb745698f807e7f7ba85ad5K.png',
    'rubber-grip-adjustable-wrench': 'https://sc02.alicdn.com/kf/A03fae2bf342c4382aea4e1d2d0f8dfbbq.png',
    'heavy-duty-tape-measure-5m': 'https://sc02.alicdn.com/kf/A616ccc2dc3b24cfc848223d6845dd97eR.png',
    '5-inch-brushless-circular-saw-kit': 'https://sc02.alicdn.com/kf/A9bfc809155bc4596a76b260ec8164bb0d.png',
    'brushless-cordless-rotary-hammer': 'https://sc02.alicdn.com/kf/Adb6f741e55234705966cb681ca4ef815V.png',
    'corded-impact-drill-13mm': 'https://sc02.alicdn.com/kf/Aad0758ce88654a499e88bc01d1b0687fp.png',
    'high-pressure-air-blow-gun': 'https://sc02.alicdn.com/kf/A8398bc680e89487cbbc060a84e3f9d16s.png',
}

report = []
ok = fail = 0
for slug, url in EDITED.items():
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        im = Image.open(io.BytesIO(data))
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA')
            bg = Image.new('RGB', im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert('RGB')
        dest = os.path.join(IMG_DIR, slug + '.jpg')
        im.save(dest, 'JPEG', quality=92)
        report.append('%s: %d bytes, %s' % (slug, os.path.getsize(dest), im.size))
        ok += 1
    except Exception as e:
        report.append('%s: FAILED %s' % (slug, e))
        fail += 1

io.open(os.path.join(BASE, 'download_daily_edited_report_0823.txt'), 'w', encoding='utf-8').write('\n'.join(report) + '\n')
print('OK=%d FAIL=%d' % (ok, fail))
