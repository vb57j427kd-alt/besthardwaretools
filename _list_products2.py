# -*- coding: utf-8 -*-
import sys, io
sys.path.insert(0, r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site')
import products_data as pd

out = []
for cat in ['hardware', 'hand-tools', 'power-tools', 'pneumatic-tools']:
    items = [p for p in pd.PRODUCTS if p.get('cat') == cat]
    out.append('===== %s (%d) =====' % (cat, len(items)))
    for p in items:
        out.append('- %s | %s' % (p['slug'], p['name']))
with io.open(r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\_existing_products.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('total', len(pd.PRODUCTS))
