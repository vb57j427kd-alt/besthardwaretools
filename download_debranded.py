# -*- coding: utf-8 -*-
"""Download AI-edited (brand-removed) product images and replace local files."""
import os, urllib.request
from PIL import Image
from io import BytesIO

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "images")

URLS = {
    "brushless-cordless-drill": "https://sc02.alicdn.com/kf/A886cbce26c574174a1172776d9bdc0d7w.png",
    "black-aluminum-cabinet-handle": "https://sc02.alicdn.com/kf/Ae1c773e2b4fe428eadf167943bd85248J.png",
    "72-tooth-ratchet-wrench-set": "https://sc02.alicdn.com/kf/A60caae9bb7f54c4f99fcb524a1582f04s.png",
    "industrial-lineman-pliers": "https://sc02.alicdn.com/kf/A8b2764ff999940109f009f9c66afb638I.png",
    "brushless-cordless-angle-grinder": "https://sc02.alicdn.com/kf/Afb4526074445425b9bc568a6c549f679c.png",
    "brushless-impact-wrench": "https://sc02.alicdn.com/kf/A4393df79236b417dada7eec856c9bc334.png",
    "air-impact-wrench": "https://sc02.alicdn.com/kf/A53b24a6ec8f14e229db322be0055fd1fq.png",
    "pneumatic-air-nailer": "https://sc02.alicdn.com/kf/Ace38a5124c4b4b14868367665f45862dg.png",
}

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"}

for slug, url in URLS.items():
    try:
        req = urllib.request.Request(url, headers=UA)
        data = urllib.request.urlopen(req, timeout=90).read()
        img = Image.open(BytesIO(data))
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGBA")
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")
        dest = os.path.join(IMG_DIR, slug + ".jpg")
        img.save(dest, "JPEG", quality=92)
        print(f"{slug}: {len(data)} bytes -> {os.path.getsize(dest)} bytes jpg {img.size}")
    except Exception as e:
        print(f"{slug}: FAILED {e}")
