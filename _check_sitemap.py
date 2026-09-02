# -*- coding: utf-8 -*-
import re, io

base = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site'
with io.open(base + r'\products_data.py', encoding='utf-8') as f:
    content = f.read()
slugs = re.findall(r'"slug"\s*:\s*"([^"]+)"', content)
print('PRODUCTS count:', len(slugs))

with io.open(base + r'\sitemap.xml', encoding='utf-8') as f:
    sm = f.read()
urls = re.findall(r'<loc>(.*?)</loc>', sm)
print('SITEMAP count:', len(urls))
home = 'https://besthardwaretools.com/'
print('has home url:', home in urls)
missing = [s for s in slugs if ('https://besthardwaretools.com/products/%s.html' % s) not in urls]
print('missing products:', len(missing))
if missing:
    print('missing sample:', missing[:8])
dup = len(urls) - len(set(urls))
print('duplicate urls:', dup)
