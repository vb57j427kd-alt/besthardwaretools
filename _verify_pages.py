# -*- coding: utf-8 -*-
import io, os, sys
sys.path.insert(0, r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site')
import products_data as pd

base = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site'
slugs = [p['slug'] for p in pd.PRODUCTS]
missing_pages = [s for s in slugs if not os.path.exists(os.path.join(base, 'products', s + '.html'))]
print('pages missing:', missing_pages if missing_pages else 'NONE')

sm = io.open(os.path.join(base, 'sitemap.xml'), encoding='utf-8').read()
missing_sm = [s for s in slugs if 'products/%s.html' % s not in sm]
print('sitemap missing:', missing_sm if missing_sm else 'NONE')

idx = io.open(os.path.join(base, 'index.html'), encoding='utf-8').read()
missing_idx = [s for s in slugs if '/products/%s.html' % s not in idx]
print('index missing:', missing_idx if missing_idx else 'NONE')
