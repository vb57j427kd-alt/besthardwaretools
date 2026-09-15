# -*- coding: utf-8 -*-
import re
from pathlib import Path

base = Path(__file__).parent
h = (base / "index.html").read_text(encoding="utf-8")
links = re.findall(r'href="([^"]*products/[^"]+)"', h)
print("index_product_links", len(links), "unique", len(set(links)))
print("sample", links[:3])
new = [
    "stainless-360-pivot-hinge", "detachable-stainless-hinge", "self-closing-spring-hinge",
    "14-in-1-insulated-ratchet-screwdriver-set", "8-inch-combination-pliers-190mm",
    "6-inch-crv-combination-pliers-160mm", "12v-mini-cordless-angle-grinder",
    "brushless-cordless-angle-grinder-21v", "hvlp-pneumatic-spray-gun", "w71g-pneumatic-spray-gun",
]
for s in new:
    print(s, "in_index=", any(s in l for l in links))
