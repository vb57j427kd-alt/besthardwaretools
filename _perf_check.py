# -*- coding: utf-8 -*-
import io, os, re

base = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site'
idx = io.open(os.path.join(base, 'index.html'), encoding='utf-8').read()
print('index.html size: %.1f KB' % (len(idx.encode('utf-8')) / 1024))

imgs = re.findall(r'<img[^>]*>', idx)
print('img tags:', len(imgs))
lazy = sum(1 for t in imgs if 'loading="lazy"' in t)
print('lazy images:', lazy)

sizes = []
for d in os.listdir(os.path.join(base, 'images')):
    if d.endswith('.jpg'):
        sizes.append(os.path.getsize(os.path.join(base, 'images', d)))
sizes.sort()
print('images count:', len(sizes))
print('median: %.0f KB, avg: %.0f KB, max: %.0f KB, p90: %.0f KB' % (
    sizes[len(sizes)//2]/1024, sum(sizes)/len(sizes)/1024, sizes[-1]/1024,
    sizes[int(len(sizes)*0.9)]/1024))
total = sum(sizes)
print('TOTAL all images: %.1f MB' % (total/1024/1024))

css = re.findall(r'<link[^>]+stylesheet[^>]*>', idx)
js = re.findall(r'<script[^>]*src=', idx)
print('css links:', len(css), '| external js:', len(js))
