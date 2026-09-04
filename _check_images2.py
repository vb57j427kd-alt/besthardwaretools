# -*- coding: utf-8 -*-
import sys, os, io, re
sys.path.insert(0, r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site')
import products_data as pd

base = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site'
slugs = [p['slug'] for p in pd.PRODUCTS]
print('PRODUCTS count:', len(slugs))

img_dir = os.path.join(base, 'images')
missing, small = [], []
for s in slugs:
    p = os.path.join(img_dir, s + '.jpg')
    if not os.path.exists(p):
        missing.append(s)
    elif os.path.getsize(p) <= 10 * 1024:
        small.append(s)
print('missing jpg:', len(missing))
print('small jpg (<=10KB):', len(small))
if missing[:5]:
    print('missing sample:', missing[:5])

# product page img src spot check (first 3)
for s in slugs[:3]:
    page = io.open(os.path.join(base, 'products', s + '.html'), encoding='utf-8').read()
    m = re.search(r'<img[^>]+src="([^"]+)"', page)
    print('page', s, 'img src:', m.group(1) if m else 'NONE')

# index card count
idx = io.open(os.path.join(base, 'index.html'), encoding='utf-8').read()
cats = re.findall(r'<section id="cat-([a-z-]+)">(.*?)</section>', idx, re.S)
total = 0
for cid, body in cats:
    n = len(re.findall(r'class="pc"', body))
    total += n
    print('section', cid, ':', n)
print('category card total:', total, '== products:', total == len(slugs))
