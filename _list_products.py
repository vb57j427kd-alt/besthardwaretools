# -*- coding: utf-8 -*-
import re, io, json

path = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\products_data.py'
with io.open(path, encoding='utf-8') as f:
    content = f.read()

# parse entries as dicts
entries = re.findall(r'\{.*?"slug":\s*"([^"]+)".*?"name":\s*"([^"]+)".*?"cat":\s*"([^"]+)"', content, re.S)
print('parsed:', len(entries))
by_cat = {}
for slug, name, cat in entries:
    by_cat.setdefault(cat, []).append((slug, name))
out = []
for cat in ['hardware', 'hand-tools', 'power-tools', 'pneumatic-tools']:
    out.append('===== %s (%d) =====' % (cat, len(by_cat.get(cat, []))))
    for slug, name in by_cat.get(cat, []):
        out.append('- %s | %s' % (slug, name))
with open(r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\_existing_products.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('written existing list')
