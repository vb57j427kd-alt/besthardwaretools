# -*- coding: utf-8 -*-
import sys
from collections import Counter
sys.path.insert(0, r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site')
import products_data as pd

slugs = [p['slug'] for p in pd.PRODUCTS]
print('total:', len(slugs))
print('cats:', dict(Counter(p['cat'] for p in pd.PRODUCTS)))
print('dup slugs:', len(slugs) - len(set(slugs)))

bad_rel = []
for p in pd.PRODUCTS:
    for r in p.get('related', []):
        if r not in slugs:
            bad_rel.append((p['slug'], r))
print('bad related:', bad_rel if bad_rel else 'NONE')

new10 = slugs[-10:]
print('new 10:', new10)
imgs_missing = [s for s in new10 if not __import__('os').path.exists(
    r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\images\%s.jpg' % s)]
print('missing imgs:', imgs_missing if imgs_missing else 'NONE')
