# -*- coding: utf-8 -*-
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from products_data import PRODUCTS

BASE = os.path.dirname(os.path.abspath(__file__))
slugs = [p["slug"] for p in PRODUCTS]
print("PRODUCT_COUNT", len(slugs), "UNIQUE", len(set(slugs)))

missing, small, badref = [], [], []
for p in PRODUCTS:
    path = os.path.join(BASE, "images", p["slug"] + ".jpg")
    if not os.path.isfile(path):
        missing.append(p["slug"])
    elif os.path.getsize(path) <= 10240:
        small.append((p["slug"], os.path.getsize(path)))
    expected = "/images/" + p["slug"] + ".jpg"
    if p.get("img") != expected:
        badref.append((p["slug"], p.get("img")))
print("MISSING_JPG", missing)
print("SMALL_JPG", small)
print("IMG_FIELD_DIFF", badref)

# spot check 3 real product pages
import random
random.seed(5)
picks = [slugs[0], slugs[len(slugs) // 2], slugs[-1]]
for s in picks:
    page = os.path.join(BASE, "products", s + ".html")
    if not os.path.isfile(page):
        print("PAGE_MISSING", s)
        continue
    h = open(page, encoding="utf-8").read()
    srcs = re.findall(r'<img src="([^"]+)"', h)
    hit = any("/images/%s.jpg" % s in x for x in srcs)
    print("PAGE", s, "EXISTS", True, "IMG_HIT", hit, "SRCS", srcs[:2])

# homepage cards
h = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
cards = re.findall(r'href="/products/([^"]+)\.html"', h)
uniq = sorted(set(cards))
print("CARDS_TOTAL", len(cards), "CARDS_UNIQUE", len(uniq))
want = set(slugs)
not_covered = sorted(want - set(uniq))
print("NOT_COVERED", not_covered)
print("CARD_EXTRA", sorted(set(uniq) - want))
