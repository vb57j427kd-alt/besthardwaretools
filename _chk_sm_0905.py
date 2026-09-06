# -*- coding: utf-8 -*-
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from products_data import PRODUCTS

BASE = os.path.dirname(os.path.abspath(__file__))
slugs = [p["slug"] for p in PRODUCTS]
sm = open(os.path.join(BASE, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(https://besthardwaretools\.com/[^<]*)</loc>", sm)
home = "https://besthardwaretools.com/" in locs
prod_locs = {u.replace("https://besthardwaretools.com/products/", "").replace(".html", "") for u in locs if "/products/" in u}
want = set(slugs)
missing = sorted(want - prod_locs)
extra = sorted(prod_locs - want)
print("PRODUCTS", len(slugs), "| SITEMAP_LOCS", len(locs), "| HOME", home)
print("MISSING", missing)
print("EXTRA", extra)
print("RESULT", "OK" if home and not missing and not extra and len(locs) == len(slugs) + 1 else "MISMATCH")
