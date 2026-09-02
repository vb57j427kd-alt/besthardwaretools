# -*- coding: utf-8 -*-
import re, io
from collections import Counter

path = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\products_data.py'
with io.open(path, encoding='utf-8') as f:
    content = f.read()

slugs = re.findall(r'"slug"\s*:\s*"([^"]+)"', content)
cats = re.findall(r'"cat"\s*:\s*"([^"]+)"', content)
names = re.findall(r'"name"\s*:\s*"([^"]+)"', content)

print('total products:', len(slugs))
print('cat distribution:', dict(Counter(cats)))
print('--- slug: cat ---')
for i, s in enumerate(slugs):
    c = cats[i] if i < len(cats) else '?'
    print(c + ' :: ' + s)
