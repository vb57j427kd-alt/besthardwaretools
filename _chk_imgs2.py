# -*- coding: utf-8 -*-
import os, re
from products_data import PRODUCTS

BASE = os.path.dirname(os.path.abspath(__file__))
slugs = [p["slug"] for p in PRODUCTS]
pick = [slugs[0], slugs[len(slugs) // 2], slugs[-1], "cordless-turbo-fan-blower-kit"]
for x in pick:
    print("FILE_OK", x, os.path.isfile(os.path.join("images", x + ".jpg")))
shared = "cordless-leaf-blower-with-storage-box.jpg"
print("SHARED_IMG_EXISTS", os.path.isfile(os.path.join("images", shared)))
for p in pick:
    page = os.path.join("products", p + ".html")
    if not os.path.isfile(page):
        print("PAGE_MISSING", p)
        continue
    with open(page, encoding="utf-8") as f:
        h = f.read()
    m = re.search(r'<img src="([^"]+)"', h)
    print("PAGE_IMG", p, m.group(1) if m else "NOT_FOUND")
