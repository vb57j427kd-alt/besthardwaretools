# -*- coding: utf-8 -*-
"""Download AI-edited (English-only) product images and replace local files."""
import os, urllib.request
from PIL import Image
from io import BytesIO

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "images")

URLS = {
    "brushless-cordless-drill": "https://sc02.alicdn.com/kf/A4db5991074024160bfefdd630f4f30dcO.png",
    "stainless-steel-soft-close-hinge": "https://sc02.alicdn.com/kf/Aad39a6e9d7ec42f8a2a3008b01547e3dK.png",
    "black-aluminum-cabinet-handle": "https://sc02.alicdn.com/kf/A48fa671b712e4d9f941ade2e5cb70f8f6.png",
    "heavy-duty-swivel-caster": "https://sc02.alicdn.com/kf/A16b1a59aa4ff4aaab4b000dc2bfc3e2fe.png",
    "72-tooth-ratchet-wrench-set": "https://sc02.alicdn.com/kf/Af4e31741cf8045528e3bc6b12bef0cccv.png",
    "magnetic-screwdriver-set": "https://sc02.alicdn.com/kf/A2b3ce28f9c61427996297402476bc084w.png",
    "industrial-lineman-pliers": "https://sc02.alicdn.com/kf/A499fc6d33fbd48aabe7c34df0c223050z.png",
    "brushless-cordless-angle-grinder": "https://sc02.alicdn.com/kf/A8c5cf6b0ba42415abbde825d86ba399bc.png",
    "brushless-impact-wrench": "https://sc02.alicdn.com/kf/A58573715e6984529bfc4d05099980a61Z.png",
    "air-impact-wrench": "https://sc02.alicdn.com/kf/Ab66caaff2ec446fd8d4f6289f116ace78.png",
    "pneumatic-air-nailer": "https://sc02.alicdn.com/kf/A35cfcf82eec7460195a59229b99b96ecx.png",
}

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"}

for slug, url in URLS.items():
    try:
        req = urllib.request.Request(url, headers=UA)
        data = urllib.request.urlopen(req, timeout=60).read()
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
