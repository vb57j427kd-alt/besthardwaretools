# -*- coding: utf-8 -*-
import re, io, os

base = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site'

def check(name, html, expected_canonical):
    print('===== %s =====' % name)
    issues = []
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    if not m or not m.group(1).strip():
        issues.append('title: MISSING/EMPTY')
    else:
        print('title OK:', m.group(1)[:60])
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    if not m or not m.group(1).strip():
        issues.append('meta description: MISSING/EMPTY')
    else:
        print('meta description OK (%d chars)' % len(m.group(1)))
    m = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    if not m:
        issues.append('canonical: MISSING')
    elif m.group(1) != expected_canonical:
        issues.append('canonical WRONG: %s != %s' % (m.group(1), expected_canonical))
    else:
        print('canonical OK:', m.group(1))
    og = {}
    for k in ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']:
        mm = re.search(r'property="%s" content="([^"]*)"' % re.escape(k), html)
        og[k] = mm.group(1) if mm else ''
    missing_og = [k for k, v in og.items() if not v]
    if missing_og:
        issues.append('og missing: ' + ', '.join(missing_og))
    else:
        print('og tags OK:', ', '.join(k.split(':')[1] for k in og))
    ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if not ld:
        issues.append('JSON-LD: MISSING')
    else:
        types = []
        for j in ld:
            mm = re.search(r'"@type"\s*:\s*"?([A-Za-z]+)"?', j)
            if mm:
                types.append(mm.group(1))
        need = 'Organization' if 'index' in name else 'Product'
        if need not in types:
            issues.append('JSON-LD missing type: %s (found %s)' % (need, types))
        else:
            print('JSON-LD OK:', types)
    m = re.search(r'<meta name="robots" content="([^"]*)"', html)
    if not m:
        issues.append('robots meta: MISSING')
    elif m.group(1).lower() not in ('index,follow', 'index, follow'):
        issues.append('robots content: %s' % m.group(1))
    else:
        print('robots OK:', m.group(1))
    if issues:
        print('ISSUES:')
        for i in issues:
            print('  -', i)
    else:
        print('ALL OK')

home = io.open(os.path.join(base, 'index.html'), encoding='utf-8').read()
check('index.html', home, 'https://besthardwaretools.com/')

with io.open(os.path.join(base, 'products_data.py'), encoding='utf-8') as f:
    content = f.read()
slugs = re.findall(r'"slug"\s*:\s*"([^"]+)"', content)
for s in slugs[:3]:
    p = os.path.join(base, 'products', s + '.html')
    if os.path.exists(p):
        check(s + '.html', io.open(p, encoding='utf-8').read(), 'https://besthardwaretools.com/products/%s.html' % s)
    else:
        print(s, 'PAGE MISSING')
