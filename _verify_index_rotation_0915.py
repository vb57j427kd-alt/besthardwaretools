# -*- coding: utf-8 -*-
"""Confirm generated index.html matches today's rotation window."""
import re
from datetime import datetime
from pathlib import Path
import sys

base = Path(__file__).parent
sys.path.insert(0, str(base))
from products_data import PRODUCTS  # noqa: E402

html = (base / "index.html").read_text(encoding="utf-8")
links = re.findall(r'href="[^"]*products/([^"]+?)\.html"', html)
print("index_product_links", len(links), "unique", len(set(links)))
print("sample", links[:3])
link_set = set(links)

day = datetime.now().day
print("today day =", day)

ok = True
for cid in ["power-tools", "pneumatic-tools", "hand-tools", "hardware"]:
    items = [p for p in PRODUCTS if p["cat"] == cid]
    o = (day * 3) % len(items)
    expected = [p["slug"] for p in (items[o:] + items[:o])[:9]]
    present = [s for s in expected if s in link_set]
    missing = [s for s in expected if s not in link_set]
    print(f"{cid}: expected={len(expected)} present={len(present)} missing={missing}")
    if missing:
        ok = False
print("ALL_CATEGORY_WINDOWS_MATCH_INDEX", ok)
