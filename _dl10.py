# -*- coding: utf-8 -*-
import os, urllib.request

BASE = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site'
TMP = os.path.join(BASE, '_tmp_imgs')
os.makedirs(TMP, exist_ok=True)

imgs = {
    'folding-table-leaf-hinge-90': 'https://cbu01.alicdn.com/img/ibank/O1CN01ssRjp21lqVZ1duWGn_!!955624870-0-cib.jpg',
    'square-black-aluminum-cabinet-handle': 'https://cbu01.alicdn.com/img/ibank/O1CN01SGY4NxcVikJ1chua_!!2222216890665-0-cib.jpg',
    'ratcheting-combination-wrench-10mm': 'https://cbu01.alicdn.com/img/ibank/O1CN01f1r8jH23JgfzZ4VMc_!!2222458657235-0-cib.jpg',
    '9-inch-chrome-vanadium-combination-pliers': 'https://cbu01.alicdn.com/img/ibank/O1CN01YhrvEq26PaYTcetcb_!!2213254657654-0-cib.jpg',
    '6-inch-drop-forged-combination-pliers': 'https://cbu01.alicdn.com/img/ibank/O1CN01yIctwl2B5VITsnwE8_!!2220586258287-0-cib.jpg',
    'cordless-turbo-leaf-blower': 'https://cbu01.alicdn.com/img/ibank/O1CN01O8LVWT27o9U9Wxviq_!!2222465347843-0-cib.jpg',
    'cordless-leaf-blower-with-storage-box': 'https://cbu01.alicdn.com/img/ibank/O1CN01aGgdVn1n9ZytqRq1Z_!!2219390735047-0-cib.jpg',
    'heavy-duty-cordless-leaf-blower': 'https://cbu01.alicdn.com/img/ibank/O1CN01taYux51raNhy1ve8X_!!2206749095647-0-cib.jpg',
    'pneumatic-metal-shear': 'https://cbu01.alicdn.com/img/ibank/O1CN01xvCLQR26m1jljxIub_!!2647737703-0-cib.jpg',
    'pneumatic-wire-shear-s110': 'https://cbu01.alicdn.com/img/ibank/O1CN013DHaqK27k1QKybf18_!!6000000007834-0-cib.jpg',
}

ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
ok = 0
for slug, url in imgs.items():
    p = os.path.join(TMP, slug + '.jpg')
    try:
        req = urllib.request.Request(url, headers=ua)
        data = urllib.request.urlopen(req, timeout=30).read()
        with open(p, 'wb') as f:
            f.write(data)
        sz = os.path.getsize(p)
        print(slug, 'OK', sz)
        ok += 1
    except Exception as e:
        print(slug, 'FAIL', e)
print('downloaded', ok, '/', len(imgs))
