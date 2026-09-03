# -*- coding: utf-8 -*-
import io, os, re, datetime

base = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site'
cur = datetime.datetime.now().year
print('current year:', cur)

# footer copyright in index.html
idx = io.open(os.path.join(base, 'index.html'), encoding='utf-8').read()
m = re.search(r'&copy;\s*(\d{4})\s*', idx)
print('index footer year:', m.group(1) if m else 'NOT FOUND')

# scan all generated html for stale years (c) YYYY where YYYY != current
stale = []
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d not in ('.git', 'images')]
    for fn in files:
        if fn.endswith('.html'):
            p = os.path.join(root, fn)
            t = io.open(p, encoding='utf-8', errors='replace').read()
            for mm in re.finditer(r'&copy;\s*(\d{4})', t):
                if mm.group(1) != str(cur):
                    stale.append((os.path.relpath(p, base), mm.group(1)))
print('stale copyright years:', stale if stale else 'NONE')

# scan for obvious expired date phrases in generated html (e.g. "2025-", "as of 2025", "until 2025")
ph = []
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d not in ('.git', 'images')]
    for fn in files:
        if fn.endswith('.html'):
            p = os.path.join(root, fn)
            t = io.open(p, encoding='utf-8', errors='replace').read()
            for mm in re.finditer(r'(?:20(?:2[0-5]|1[0-9]))', t):
                ph.append((os.path.relpath(p, base), mm.group(0)))
print('expired year mentions:', ph[:10] if ph else 'NONE')
