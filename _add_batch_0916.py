# -*- coding: utf-8 -*-
"""Validate + append the 0916 batch (10 products) into products_data.py."""
import importlib.util
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

spec = importlib.util.spec_from_file_location("pd", os.path.join(BASE, "products_data.py"))
pd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pd)

new = json.load(open("selections_0916.json", encoding="utf-8"))

existing = {p["slug"] for p in pd.PRODUCTS}
cat_ids = {c["id"] for c in pd.CATEGORIES}
new_slugs = {p["slug"] for p in new}
all_slugs = existing | new_slugs
valid_badges = {"Bestseller", "Hot", "New"}

# brand blocklist: no third-party brand may appear in any site-facing text
BLOCK = ["得力", "Deli", "COTA", "沂顺", "YSHUN", "兴博", "XINGBO", "贝德龙", "海飞鲨",
         "帕锐欧", "藤原", "尚艺佳", "贝琪", "聚力安", "胜达", "金烨", "锤工", "诺曼",
         "任士兴", "明辉", "云琦", "欧维尔", "齐正", "鲁珩", "EKM"]

errors = []
WANT_FIELDS = ["slug", "cat", "name", "badge", "price", "moq", "img", "src", "desc", "specs", "points", "related"]

for p in new:
    s = p["slug"]
    missing = [f for f in WANT_FIELDS if f not in p]
    if missing:
        errors.append("%s: missing fields %s" % (s, missing))
    if s in existing:
        errors.append("%s: slug already exists" % s)
    if p["cat"] not in cat_ids:
        errors.append("%s: bad cat %s" % (s, p["cat"]))
    if p["badge"] not in valid_badges:
        errors.append("%s: bad badge %s" % (s, p["badge"]))
    if not re.match(r"^\$\d+\.\d{2} - \$\d+\.\d{2} /(pc|kit|pair|pr)$", p["price"]):
        errors.append("%s: bad price format %s" % (s, p["price"]))
    if not re.match(r"^https://detail\.1688\.com/offer/\d+\.html$", p["src"]):
        errors.append("%s: bad src %s" % (s, p["src"]))
    img_rel = p["img"].lstrip("/")
    if not os.path.isfile(os.path.join(BASE, img_rel)):
        errors.append("%s: image missing %s" % (s, p["img"]))
    for r in p["related"]:
        if r not in all_slugs:
            errors.append("%s: related slug not found -> %s" % (s, r))
    if len(p["related"]) == 0:
        errors.append("%s: no related" % s)
    blob = " ".join([p["name"], p["desc"]] + p["points"] +
                    [k + " " + v for k, v in p["specs"]])
    for b in BLOCK:
        if b.isascii():
            # Latin brand tokens need word boundaries so "Deli" does not match "delivery"
            if re.search(r"\b%s\b" % re.escape(b), blob, re.IGNORECASE):
                errors.append("%s: brand token found -> %s" % (s, b))
        elif b in blob:
            errors.append("%s: brand token found -> %s" % (s, b))

if errors:
    print("VALIDATION FAILED (%d):" % len(errors))
    for e in errors:
        print("  -", e)
    sys.exit(1)

print("validation ok: %d new products, all slugs/related/images/prices/brands clean" % len(new))

# ---- format source block ----
def lit(v):
    return json.dumps(v, ensure_ascii=False)

blocks = []
for p in new:
    L = []
    L.append("    {")
    for k in ["slug", "cat", "name", "badge", "price", "moq", "img", "src", "desc"]:
        L.append('        "%s": %s,' % (k, lit(p[k])))
    L.append('        "specs": [')
    for k, v in p["specs"]:
        L.append("            (%s, %s)," % (lit(k), lit(v)))
    L.append("        ],")
    L.append('        "points": [')
    for pt in p["points"]:
        L.append("            %s," % lit(pt))
    L.append("        ],")
    L.append('        "related": [%s],' % ", ".join(lit(r) for r in p["related"]))
    L.append("    },")
    blocks.append("\n".join(L))

src_path = os.path.join(BASE, "products_data.py")
content = open(src_path, encoding="utf-8").read()
marker = "    },\n]\nRELATED_INDEX"
if content.count(marker) != 1:
    print("ABORT: marker found %d times" % content.count(marker))
    sys.exit(1)

replacement = "    },\n" + "\n".join(blocks) + "\n]\nRELATED_INDEX"
open(src_path, "w", encoding="utf-8").write(content.replace(marker, replacement, 1))
print("appended %d items to products_data.py" % len(blocks))

# ---- re-verify by re-importing ----
spec2 = importlib.util.spec_from_file_location("pd2", src_path)
pd2 = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(pd2)
slugs = [p["slug"] for p in pd2.PRODUCTS]
print("PRODUCTS now: %d (unique: %d)" % (len(slugs), len(set(slugs))))
print("related index keys: %d" % len(pd2.RELATED_INDEX))
for p in new:
    got = pd2.RELATED_INDEX.get(p["slug"])
    print("  ok" if got else "  MISSING", p["slug"], "|", got["cat"] if got else "", "|", got["price"] if got else "")
