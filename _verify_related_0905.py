# -*- coding: utf-8 -*-
"""Verify 'You May Also Like' links on 3 sampled generated product pages."""
import io, os, random, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
base = os.path.dirname(os.path.abspath(__file__))
proddir = os.path.join(base, "products")

# slug set from products_data.py
ns = {}
with open(os.path.join(base, "products_data.py"), encoding="utf-8") as f:
    exec(compile(f.read(), "products_data.py", "exec"), ns)
slugset = set(p["slug"] for p in ns["PRODUCTS"])

pages = [f for f in os.listdir(proddir) if f.endswith(".html")]
print("generated product pages:", len(pages))

random.seed(5)
sample = sorted(random.sample(pages, 3))
all_ok = True
for pg in sample:
    with open(os.path.join(proddir, pg), encoding="utf-8") as f:
        html = f.read()
    m = re.search(r"You May Also Like", html)
    if not m:
        print(pg, "-> NO 'You May Also Like' section!")
        all_ok = False
        continue
    seg = html[m.start():]
    # capture links inside the section: cut at next <h2> or </section> or <footer>
    cut = re.search(r"<h2|<section|<footer", seg[10:])
    bound = seg if not cut else seg[: cut.start() + 10]
    links = re.findall(r'href="(/products/[^"]+\.html)"', bound)
    uniq = []
    for l in links:
        if l not in uniq:
            uniq.append(l)
    if len(uniq) != 3:
        print(pg, "-> WARN related link count =", len(uniq), "| section-bound:", bool(cut))
    bad = [l for l in uniq if l.split("/")[-1][: -len(".html")] not in slugset]
    if bad:
        all_ok = False
    print(pg, "| links:", len(uniq), "| all slugs exist:", not bad)
    for l in uniq:
        print("   ", l)
    if bad:
        for l in bad:
            print("   MISSING SLUG ->", l)

print("ALL_OK" if all_ok else "HAS_ISSUES")
