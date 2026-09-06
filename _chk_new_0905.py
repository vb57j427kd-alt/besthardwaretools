# -*- coding: utf-8 -*-
import os, io, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from products_data import PRODUCTS

slugs = [p["slug"] for p in PRODUCTS]
print("TOTAL", len(slugs), "UNIQUE", len(set(slugs)))
new = slugs[-10:]
print("NEW", new)
from collections import Counter
print("CAT", Counter(p["cat"] for p in PRODUCTS))
print("NEWCAT", Counter(p["cat"] for p in PRODUCTS if p["slug"] in new))

banned = ["DELIXI", "GREENER", "VUFU", "JINCHENG", "GUANGCAI", "NANWEI", "JIAY", "永冠", "重吾", "三丰",
          "广陆", "高宝", "牧田", "东成", "德力西", "Milwaukee", "DeWalt", "Makita", "Bosch", "Mitutoyo",
          "GREENER", "PURIMA", "普瑞玛", "奥力晟", "立宇", "保联", "钢盾", "佳捷仕", "雷霆", "乐高", "聚仁",
          "NEWBEAT", "拓", "五福", "金城", "绿林", "广才", "南威", "佳银", "亚固"]
hits = []
for p in PRODUCTS:
    if p["slug"] in new:
        text = (p["name"] + "|" + p["desc"]).upper()
        for b in banned:
            if b.upper() in text:
                hits.append((p["slug"], b))
print("BANNED_HITS", hits)

for p in PRODUCTS:
    if p["slug"] in new:
        wc = len(p["desc"].split())
        ok = 120 <= wc <= 180
        img_ok = os.path.isfile(os.path.join("images", p["slug"] + ".jpg"))
        rel_ok = all(r in slugs for r in p["related"])
        sp_ok = len(p["specs"]) == 6
        pt_ok = 3 <= len(p["points"]) <= 4
        print(p["slug"], "| words", wc, "| img", img_ok, "| related", rel_ok, "| specs6", sp_ok, "| pts", pt_ok, "| price", p["price"], "| moq", p["moq"], "| badge", p["badge"])
print("IMG_SIZES")
for p in PRODUCTS:
    if p["slug"] in new:
        sz = os.path.getsize(os.path.join("images", p["slug"] + ".jpg"))
        print(p["slug"], sz, ">10KB", sz > 10240)
