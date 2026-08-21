# -*- coding: utf-8 -*-
"""Download 1688 product images into repo and switch pages to local paths."""
import os, re, urllib.request, sys

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "images")
os.makedirs(IMG_DIR, exist_ok=True)

sys.path.insert(0, BASE)
import products_data as pd

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

results = []
for p in pd.PRODUCTS:
    slug, url = p["slug"], p["img"]
    dest = os.path.join(IMG_DIR, slug + ".jpg")
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(dest, "wb") as f:
            f.write(data)
        results.append(f"{slug}: {len(data)} bytes")
    except Exception as e:
        results.append(f"{slug}: FAILED {e}")

# rewrite products_data.py: swap remote img URLs for local paths
data_path = os.path.join(BASE, "products_data.py")
src = open(data_path, encoding="utf-8").read()
for p in pd.PRODUCTS:
    src = src.replace('"' + p["img"] + '"', '"/images/' + p["slug"] + '.jpg"')
open(data_path, "w", encoding="utf-8").write(src)

print("\n".join(results))
