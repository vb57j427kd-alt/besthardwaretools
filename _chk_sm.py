# -*- coding: utf-8 -*-
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from products_data import PRODUCTS

BASE = os.path.dirname(os.path.abspath(__file__))
slugs = set(p["slug"] for p in PRODUCTS)
sm = open(os.path.join(BASE, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(https://besthardwaretools\.com/[^<]*)</loc>", sm)
home = "https://besthardwaretools.com/" in locs
prod = set()
for u in locs:
    if u.startswith("https://besthardwaretools.com/products/"):
        prod.add(u.replace("https://besthardwaretools.com/products/", "").replace(".html", ""))
print("PRODUCT_SLUGS", len(slugs))
print("SITEMAP_LOCS", len(locs), "HOME", home)
print("MISSING", sorted(slugs - prod) or 0)
print("EXTRA", sorted(prod - slugs) or 0)
