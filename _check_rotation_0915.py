# -*- coding: utf-8 -*-
"""Verify the daily homepage rotation window for each category."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from products_data import PRODUCTS  # noqa: E402

CATS = ["power-tools", "pneumatic-tools", "hand-tools", "hardware"]
NEW = {
    "stainless-360-pivot-hinge", "detachable-stainless-hinge", "self-closing-spring-hinge",
    "14-in-1-insulated-ratchet-screwdriver-set", "8-inch-combination-pliers-190mm",
    "6-inch-crv-combination-pliers-160mm", "12v-mini-cordless-angle-grinder",
    "brushless-cordless-angle-grinder-21v", "hvlp-pneumatic-spray-gun", "w71g-pneumatic-spray-gun",
}

for day in (15, 16, 17):
    print(f"--- day {day} ---")
    for cid in CATS:
        items = [p for p in PRODUCTS if p["cat"] == cid]
        offset = (day * 3) % len(items)
        rotated = items[offset:] + items[:offset]
        shown = rotated[:9]
        print(f"  {cid}: offset={offset} shown={len(shown)} new_in_view={sum(1 for p in shown if p['slug'] in NEW)}")
        print(f"    first={shown[0]['slug']}")
        print(f"    last ={shown[-1]['slug']}")

# confirm each day's window differs from the next day's
print("--- window changes day to day ---")
for cid in CATS:
    items = [p for p in PRODUCTS if p["cat"] == cid]
    def win(d):
        o = (d * 3) % len(items)
        return [p["slug"] for p in (items[o:] + items[:o])[:9]]
    a, b, c = win(15), win(16), win(17)
    print(f"  {cid}: day15!=day16 -> {a != b}; day16!=day17 -> {b != c}")
