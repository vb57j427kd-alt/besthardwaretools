# -*- coding: utf-8 -*-
import os, re
from products_data import PRODUCTS

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")

slugs = [p["slug"] for p in PRODUCTS]
print("PRODUCT_COUNT", len(slugs))

missing, small, badref = [], [], []
for p in PRODUCTS:
    path = os.path.join(IMG, p["slug"] + ".jpg")
    if not os.path.isfile(path):
        missing.append(p["slug"])
    elif os.path.getsize(path) <= 10240:
        small.append((p["slug"], os.path.getsize(path)))
    ref = p.get("img", "")
    if ref != f"/images/{p['slug']}.jpg":
        badref.append((p["slug"], ref))
print("MISSING_IMG", len(missing), missing[:10])
print("SMALL_IMG(<=10KB)", len(small), small[:10])
print("BAD_IMG_FIELD", len(badref), badref[:10])

with open(os.path.join(BASE, "index.html"), encoding="utf-8") as f:
    idx = f.read()
cards = re.findall(r'<a href="/products/([^/]+\.html)" class="pc">', idx)
uniq = sorted(set(cards))
print("INDEX_CARD_TOTAL", len(cards))
print("INDEX_CARD_UNIQUE", len(uniq))
not_covered = [s for s in slugs if f"{s}.html" not in set(cards)]
print("INDEX_NOT_COVERED", not_covered)
extra_cards = [c for c in set(cards) if c.replace(".html", "") not in slugs]
print("INDEX_EXTRA", extra_cards)

# spot-check 3 product pages
for slug in ["brushless-cordless-drill", "stainless-steel-cabinet-hinge", "air-nailer-50mm"]:
    page = os.path.join(BASE, "products", slug + ".html")
    if not os.path.isfile(page):
        print("PAGE_MISSING", slug)
        continue
    with open(page, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'<img src="([^"]+)" alt="([^"]*)"', html)
    print("PAGE", slug, "IMG_SRC", m.group(1) if m else "NOT_FOUND", "EXPECTED", f"/images/{slug}.jpg")
