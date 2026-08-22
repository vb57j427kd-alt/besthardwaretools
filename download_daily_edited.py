# -*- coding: utf-8 -*-
"""Download edited (translated/debranded) images from CDN, convert to JPG on white bg, save to images/<slug>.jpg."""
import os, io, urllib.request
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

# slug -> edited CDN URL (12v-cordless-drill keeps original, no edit)
EDITED = {
    'loose-pin-door-hinge': 'https://sc02.alicdn.com/kf/Abed66218585e4bc3a3105eb13b8a26dcr.png',
    '360-degree-pivot-door-hinge': 'https://sc02.alicdn.com/kf/A07d75a1cd9a748eaa101f30ef9ce50edH.png',
    'cabinet-hinge-repair-plate': 'https://sc02.alicdn.com/kf/A3c4961a0bc044b4aabd3bc2029af39a3F.png',
    'mini-ratchet-handle-set': 'https://sc02.alicdn.com/kf/Ab54d7c88353443e099f81928b70e0cb1O.png',
    'diagonal-cutting-pliers': 'https://sc02.alicdn.com/kf/A137828c3c3734377a6b482e1222bcfdey.png',
    'brushless-impact-drill-kit': 'https://sc02.alicdn.com/kf/A76818b8de6df4e2da92388f8ed0d89b4l.png',
    'brushless-impact-wrench-kit': 'https://sc02.alicdn.com/kf/Af5f66d0d47414622bdef6bbcc8a50bc6c.png',
    'mining-air-impact-wrench': 'https://sc02.alicdn.com/kf/Aea87bc9f80d249ce8eaa5d7dfa255204z.png',
    'aluminum-siphon-spray-gun': 'https://sc02.alicdn.com/kf/Ade88924864cf45e492a4963e4c0fe5dez.png',
}

report = []
for slug, url in EDITED.items():
    dest = os.path.join(IMG_DIR, slug + '.jpg')
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
        img = Image.open(io.BytesIO(data))
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGBA')
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert('RGB')
        img.save(dest, 'JPEG', quality=95)
        sz = os.path.getsize(dest)
        report.append('%s: %d bytes, %s' % (slug, sz, img.size))
    except Exception as e:
        report.append('%s: FAILED %s' % (slug, e))

# 12v-cordless-drill: keep original download (already in images/)
try:
    sz = os.path.getsize(os.path.join(IMG_DIR, '12v-cordless-drill.jpg'))
    report.append('12v-cordless-drill: kept original, %d bytes' % sz)
except Exception as e:
    report.append('12v-cordless-drill: MISSING %s' % e)

with io.open(os.path.join(BASE, 'download_daily_edited_report.txt'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(report) + '\n')
print('DONE')
