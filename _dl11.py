# -*- coding: utf-8 -*-
import os, json, urllib.request

BASE = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F'
SRC = os.path.join(BASE, 'project', '1688-sourcing', 'results')
TMP = os.path.join(BASE, 'project', 'bht-site', '_tmp_imgs')
os.makedirs(TMP, exist_ok=True)

# slug -> (result file, itemId)
picks = {
    'zinc-alloy-cam-lock-103': ('daily-lock.json', '829116524938'),
    'invisible-magnetic-floor-door-stop': ('daily-door-catch.json', '888776906417'),
    '50pc-crv-screwdriver-bit-set': ('daily-bit-set.json', '737817353518'),
    '5-inch-curved-needle-nose-pliers': ('daily-needle-nose.json', '1006729831775'),
    '8pc-hex-socket-bit-set-100mm': ('daily-bit-set.json', '935974088885'),
    'cordless-paint-sprayer-1830b': ('daily-paint-sprayer.json', '673468201021'),
    'cordless-paint-sprayer-dual-battery': ('daily-paint-sprayer.json', '952491636737'),
    'cordless-paint-sprayer-bare-1000ml': ('daily-paint-sprayer.json', '785541354384'),
    'pneumatic-rivnut-gun': ('daily-rivnut.json', '605815695296'),
    'pneumatic-sandblaster-gun': ('daily-sandblaster.json', '900958824492'),
}

ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}
for slug, (fname, iid) in picks.items():
    data = json.load(open(os.path.join(SRC, fname), encoding='utf-8'))
    url = None
    for it in data:
        cur = it.get('itemId') or str(it.get('detailUrl', '') or '').split('/')[-1].split('?')[0].replace('.html', '')
        if str(cur) == iid:
            url = it.get('imageUrl')
            break
    if not url:
        print(slug, 'NO URL', fname, iid)
        continue
    req = urllib.request.Request(url, headers=ua)
    try:
        img = urllib.request.urlopen(req, timeout=30).read()
        p = os.path.join(TMP, slug + '.jpg')
        open(p, 'wb').write(img)
        print(slug, 'OK', len(img), url[-40:])
    except Exception as e:
        print(slug, 'FAIL', e)
