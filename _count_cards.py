# -*- coding: utf-8 -*-
import io, re

t = io.open(r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\index.html', encoding='utf-8').read()
print('total pc cards:', len(re.findall(r'class="pc"', t)))

cats = re.findall(r'<section id="cat-([a-z-]+)">(.*?)</section>', t, re.S)
total = 0
for cid, body in cats:
    n = len(re.findall(r'class="pc"', body))
    total += n
    print('section', cid, ':', n)
print('category section total:', total)

oem = re.findall(r'<section id="oem">(.*?)</section>', t, re.S)
if oem:
    print('oem section pc cards:', len(re.findall(r'class="pc"', oem[0])))
else:
    print('oem section: not found')
