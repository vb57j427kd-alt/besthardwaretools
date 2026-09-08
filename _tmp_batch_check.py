# -*- coding: utf-8 -*-
"""Temp: count products, dump slugs, compare historical batch slugs."""
import re, subprocess, sys

repo = r"C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site"
src = open(repo + r"\products_data.py", encoding="utf-8").read()
slugs = re.findall(r'"slug": "([^"]+)"', src)
print("TOTAL_PRODUCTS:", len(slugs))

n = len(slugs)
q = n // 4
print("quarter_size(n//4):", q, "-> first quarter indexes 0..%d" % (q - 1))
print("FIRST_QUARTER_SLUGS:")
for s in slugs[:q]:
    print("  ", s)

for commit in ["06d72f0", "625fd67"]:
    out = subprocess.run(
        ["git", "-C", repo, "show", commit, "--", "products_data.py"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout
    touched = set()
    for line in out.splitlines():
        m = re.search(r'"slug": "([^"]+)"', line)
        if m and (line.startswith("+") or line.startswith("-")):
            touched.add(m.group(1))
    print("\nCOMMIT", commit, "touched slugs:", len(touched))
    for s in sorted(touched)[:10]:
        print("   ", s)
