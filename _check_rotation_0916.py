# -*- coding: utf-8 -*-
"""Confirm every new product surfaces on the homepage within the rotation cycle."""
import importlib.util
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pd", os.path.join(BASE, "products_data.py"))
pd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pd)

NEW = [p["slug"] for p in pd.PRODUCTS][-10:]
by_cat = {}
for p in pd.PRODUCTS:
    by_cat.setdefault(p["cat"], []).append(p["slug"])

for cid, items in by_cat.items():
    n = len(items)
    covered = {s: [] for s in NEW}
    for day in range(1, 32):
        off = (day * 3) % n
        disp = (items[off:] + items[:off])[:9]
        for s in NEW:
            if s in disp:
                covered[s].append(day)
    print("category %-16s items=%d" % (cid, n))
    for s in NEW:
        if s not in items:
            continue
        days = covered[s]
        print("   %-45s homepage days: %s" % (s, days if days else "NEVER IN 31 DAYS"))
