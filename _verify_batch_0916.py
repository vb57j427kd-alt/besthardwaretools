# -*- coding: utf-8 -*-
"""Verify the regenerated site after the 0916 batch."""
import glob
import importlib.util
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

spec = importlib.util.spec_from_file_location("pd", os.path.join(BASE, "products_data.py"))
pd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pd)

NEW = [p["slug"] for p in pd.PRODUCTS][-10:]
print("new slugs:", len(NEW))
print("total products:", len(pd.PRODUCTS))

fails = []

# 1. product pages
missing_pages = [s for s in NEW if not os.path.isfile(os.path.join("products", s + ".html"))]
print("1) product pages present for new slugs:", "OK" if not missing_pages else "MISSING %s" % missing_pages)
if missing_pages:
    fails.append("product pages")

all_page_files = glob.glob(os.path.join("products", "*.html"))
print("   total product html files: %d (expected %d)" % (len(all_page_files), len(pd.PRODUCTS)))
if len(all_page_files) != len(pd.PRODUCTS):
    fails.append("product page count")

# 2. index.html links every product
idx = open("index.html", encoding="utf-8").read()
not_linked = [s for s in NEW if ("products/%s.html" % s) not in idx]
print("2) index.html links all new products:", "OK" if not not_linked else "MISSING %s" % not_linked)
if not_linked:
    fails.append("index links")

# 3. category pages
cat_map = {}
for c in pd.CATEGORIES:
    fn = "category-%s.html" % c["id"]
    if not os.path.isfile(fn):
        fails.append("missing category page %s" % fn)
        continue
    txt = open(fn, encoding="utf-8").read()
    cat_map[c["id"]] = txt
for p in pd.PRODUCTS[-10:]:
    txt = cat_map.get(p["cat"], "")
    ok = ("products/%s.html" % p["slug"]) in txt
    print("3) %-45s -> category-%s.html : %s" % (p["slug"], p["cat"], "OK" if ok else "NOT FOUND"))
    if not ok:
        fails.append("category placement %s" % p["slug"])

# 4. sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
sm_missing = [s for s in NEW if ("/products/%s.html" % s) not in sm]
print("4) sitemap contains new urls:", "OK" if not sm_missing else "MISSING %s" % sm_missing)
if sm_missing:
    fails.append("sitemap")
print("   sitemap url count: %d" % sm.count("<url>"))

# 5. every image referenced exists
bad_imgs = []
for p in pd.PRODUCTS:
    rel = p["img"].lstrip("/")
    if not os.path.isfile(os.path.join(BASE, rel)):
        bad_imgs.append((p["slug"], p["img"]))
print("5) all %d product images exist on disk:" % len(pd.PRODUCTS),
      "OK" if not bad_imgs else "BROKEN %s" % bad_imgs[:10])
if bad_imgs:
    fails.append("missing images")

# 6. brand cleanliness of the newly generated pages
BLOCK_ASCII = ["Deli", "COTA", "YSHUN", "XINGBO", "EKM"]
BLOCK_CJK = ["得力", "沂顺", "兴博", "贝德龙", "海飞鲨", "帕锐欧", "藤原", "尚艺佳",
             "贝琪", "聚力安", "胜达", "金烨", "锤工", "诺曼", "任士兴", "明辉",
             "云琦", "欧维尔", "齐正", "鲁珩"]
leaks = []
for s in NEW:
    html = open(os.path.join("products", s + ".html"), encoding="utf-8").read()
    for b in BLOCK_ASCII:
        if re.search(r"\b%s\b" % re.escape(b), html, re.IGNORECASE):
            leaks.append((s, b))
    for b in BLOCK_CJK:
        if b in html:
            leaks.append((s, b))
    if "\ufffd" in html or "?" * 4 in html:
        leaks.append((s, "encoding-artifact"))
print("6) no third-party brand / mojibake on new pages:", "OK" if not leaks else "LEAK %s" % leaks[:10])
if leaks:
    fails.append("brand leaks")

# 7. price sanity vs CNY source (CNY/7.1, +-20%)
CNY = {
    "frameless-glass-door-hinge-304": 1.0,
    "matte-silver-aluminum-arched-pull": 2.4,
    "heavy-duty-concealed-window-hinge-90": 7.2,
    "solid-rubber-mallet-non-bounce": 28.8,
    "curved-jaw-locking-pliers-10-inch": 6.99,
    "aluminum-rotary-caulking-gun": 3.3,
    "cordless-electric-grease-gun-24v": 171.0,
    "brushless-right-angle-ratchet-wrench-21v": 235.0,
    "pneumatic-caulking-gun-310-600ml": 182.0,
    "pneumatic-paint-mixer-10-30l": 517.0,
}
print("7) price check (CNY/7.1, x0.8 .. x1.2):")
for p in pd.PRODUCTS[-10:]:
    lo, hi = [float(x.strip("$")) for x in re.findall(r"\$([\d.]+)", p["price"])]
    base = CNY[p["slug"]] / 7.1
    e_lo, e_hi = round(base * 0.8, 2), round(base * 1.2, 2)
    ok = abs(lo - e_lo) <= 0.011 and abs(hi - e_hi) <= 0.011
    print("   %-45s %-22s expect %s - %s  %s" % (p["slug"], p["price"], e_lo, e_hi, "OK" if ok else "MISMATCH"))
    if not ok:
        fails.append("price %s" % p["slug"])

print("")
print("RESULT:", "ALL CHECKS PASSED" if not fails else "FAILURES: %s" % fails)
