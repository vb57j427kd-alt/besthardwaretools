# -*- coding: utf-8 -*-
"""Confirm every new product reaches the homepage featured window within a rotation cycle."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from products_data import PRODUCTS  # noqa: E402

NEW = [
    "stainless-360-pivot-hinge", "detachable-stainless-hinge", "self-closing-spring-hinge",
    "14-in-1-insulated-ratchet-screwdriver-set", "8-inch-combination-pliers-190mm",
    "6-inch-crv-combination-pliers-160mm", "12v-mini-cordless-angle-grinder",
    "brushless-cordless-angle-grinder-21v", "hvlp-pneumatic-spray-gun", "w71g-pneumatic-spray-gun",
]
CATS = ["hardware", "hand-tools", "power-tools", "pneumatic-tools"]

days_on_home = {s: [] for s in NEW}
for day in range(1, 61):
    for cid in CATS:
        items = [p for p in PRODUCTS if p["cat"] == cid]
        o = (day * 3) % len(items)
        shown = {p["slug"] for p in (items[o:] + items[:o])[:9]}
        for s in NEW:
            if s in shown:
                days_on_home[s].append(day)

for s in NEW:
    d = days_on_home[s]
    print(f"{s}: appears_on_home_days={len(d)} first_day={d[0] if d else None}")
