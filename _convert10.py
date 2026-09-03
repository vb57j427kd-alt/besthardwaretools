# -*- coding: utf-8 -*-
import os
from PIL import Image

BASE = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F'
MO = os.path.join(BASE, 'project', 'media-output')
SRC = os.path.join(BASE, 'project', 'bht-site', '_tmp_imgs')
DST = os.path.join(BASE, 'project', 'bht-site', 'images')
os.makedirs(DST, exist_ok=True)

mapping = {
    'square-black-aluminum-cabinet-handle': 'img-mtkpl9vn-4aeb86a0.png',
    'ratcheting-combination-wrench-10mm': 'img-mtkpldmv-f40039d2.png',
    '9-inch-chrome-vanadium-combination-pliers': 'img-mtkpldwk-6d2ab0bf.png',
    '6-inch-drop-forged-combination-pliers': 'img-mtkpmvew-e99b7d60.png',
    'cordless-brushless-leaf-blower': 'img-mtkpmk32-6de7ee26.png',
    'cordless-leaf-blower-with-storage-box': 'img-mtkpn7w3-c758e6f1.png',
    'heavy-duty-cordless-leaf-blower': 'img-mtkpqz1f-4b502ca5.png',
    'pneumatic-metal-shear': 'img-mtkpoqhq-762042c3.png',
    'pneumatic-wire-shear-s110': 'img-mtkpp9pb-b95ed0a5.png',
}
# direct-copy ones (no text/brand)
direct = ['folding-table-leaf-hinge-90']

for slug, png in mapping.items():
    src = os.path.join(MO, png)
    if not os.path.exists(src):
        print(slug, 'MISSING SOURCE', png)
        continue
    im = Image.open(src).convert('RGBA')
    bg = Image.new('RGB', im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3])
    out = os.path.join(DST, slug + '.jpg')
    bg.convert('RGB').save(out, 'JPEG', quality=93)
    print(slug, 'saved', os.path.getsize(out), 'bytes', im.size)

for slug in direct:
    src = os.path.join(SRC, slug + '.jpg')
    out = os.path.join(DST, slug + '.jpg')
    if os.path.exists(src):
        im = Image.open(src).convert('RGBA')
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        bg.convert('RGB').save(out, 'JPEG', quality=93)
        print(slug, 'saved direct', os.path.getsize(out), 'bytes')
