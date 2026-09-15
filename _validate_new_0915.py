# -*- coding: utf-8 -*-
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from products_data import PRODUCTS  # noqa: E402

new_slugs = [
    "stainless-360-pivot-hinge",
    "detachable-stainless-hinge",
    "self-closing-spring-hinge",
    "14-in-1-insulated-ratchet-screwdriver-set",
    "8-inch-combination-pliers-190mm",
    "6-inch-crv-combination-pliers-160mm",
    "12v-mini-cordless-angle-grinder",
    "brushless-cordless-angle-grinder-21v",
    "hvlp-pneumatic-spray-gun",
    "w71g-pneumatic-spray-gun",
]

slugs = [p["slug"] for p in PRODUCTS]
dupes = [s for s, c in Counter(slugs).items() if c > 1]
print("TOTAL", len(PRODUCTS), dict(Counter(p["cat"] for p in PRODUCTS)))
print("DUPLICATE_SLUGS", dupes)

brands = ["广才", "南威", "佳银", "绿林", "德力西", "五福", "金城", "东成", "GUANGCAI", "NANWEI",
          "JIAY", "GREENER", "DELIXI", "VUFU", "JINCHENG", "DONGCHENG", "WORX", "BOSCH", "MAKITA",
          "DEWALT", "MILWAUKEE", "STANLEY", "BAIYI", "佰毅", "WIN ", "YATO", "DCA"]

img_dir = Path(__file__).parent / "images"
for s in new_slugs:
    p = next((x for x in PRODUCTS if x["slug"] == s), None)
    if p is None:
        print("MISSING", s)
        continue
    blob = " ".join([p["name"], p["desc"], " ".join(p["points"]), " ".join(a + " " + str(b) for a, b in p["specs"])])
    hits = [b for b in brands if b.lower() in blob.lower()]
    img = img_dir / (s + ".jpg")
    related_missing = [r for r in p["related"] if r not in slugs]
    print(f"{s} | cat={p['cat']} | price={p['price']} | img={img.exists()} size={img.stat().st_size if img.exists() else 0} | desc_words={len(p['desc'].split())} | specs={len(p['specs'])} | points={len(p['points'])} | brand_hits={hits} | related_missing={related_missing}")
