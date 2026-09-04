# -*- coding: utf-8 -*-
import re
from products_data import PRODUCTS

slugs = [p["slug"] for p in PRODUCTS]
print("PRODUCT_COUNT", len(slugs))
print("UNIQUE", len(set(slugs)))
with open("sitemap.xml", encoding="utf-8") as f:
    sm = f.read()
urls = re.findall(r"<loc>(https://besthardwaretools\.com/[^<]*)</loc>", sm)
prod_urls = [u for u in urls if "/products/" in u]
home = [u for u in urls if u == "https://besthardwaretools.com/"]
print("SITEMAP_TOTAL", len(urls))
print("SITEMAP_PROD", len(prod_urls))
print("HOME_INCLUDED", len(home) > 0)
missing = [s for s in slugs if f"https://besthardwaretools.com/products/{s}.html" not in prod_urls]
extra = [u for u in prod_urls if u.split("/products/")[1].replace(".html", "") not in slugs]
print("MISSING", missing)
print("EXTRA", extra)
