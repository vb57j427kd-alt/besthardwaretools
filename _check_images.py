# -*- coding: utf-8 -*-
import re, io, os

base = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site'
with io.open(base + r'\products_data.py', encoding='utf-8') as f:
    content = f.read()
slugs = re.findall(r'"slug"\s*:\s*"([^"]+)"', content)
print('PRODUCTS count:', len(slugs))

img_dir = os.path.join(base, 'images')
missing = []
small = []
for s in slugs:
    p = os.path.join(img_dir, s + '.jpg')
    if not os.path.exists(p):
        missing.append(s)
    else:
        sz = os.path.getsize(p)
        if sz <= 10240:
            small.append((s, sz))
print('missing jpg:', len(missing), missing[:8])
print('small jpg (<=10KB):', len(small), small[:8])

# index.html product cards count (product_card generates div class="card" or similar)
with io.open(os.path.join(base, 'index.html'), encoding='utf-8') as f:
    idx = f.read()
cards = len(re.findall(r'class="card"', idx))
print('index cards:', cards)

# spot check 3 product pages
for s in slugs[:3]:
    pp = os.path.join(base, 'products', s + '.html')
    if os.path.exists(pp):
        t = io.open(pp, encoding='utf-8').read()
        m = re.search(r'<img src="([^"]+)"', t)
        print('spot', s, '->', m.group(1) if m else 'NO-IMG')
    else:
        print('spot', s, '-> PAGE MISSING')
