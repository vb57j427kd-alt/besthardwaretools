# -*- coding: utf-8 -*-
import os, shutil
from PIL import Image

BASE = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F'
MO = os.path.join(BASE, 'project', 'media-output')
SRC = os.path.join(BASE, 'project', 'bht-site', '_tmp_imgs')
DST = os.path.join(BASE, 'project', 'bht-site', 'images')

mapping = {
    'zinc-alloy-cam-lock-103': 'img-mtm4xh5m-e879df46.png',
    'invisible-magnetic-floor-door-stop': 'img-mtm4zkzz-ae2d91df.png',
    '50pc-crv-screwdriver-bit-set': 'img-mtm4xrvt-0e43ba67.png',
    '5-inch-curved-needle-nose-pliers': 'img-mtm51475-990cd293.png',
    '8-inch-needle-nose-pliers': 'img-mtm50x6k-6e95cf71.png',
    'cordless-paint-sprayer-1830b': 'img-mtm5136s-fd51201f.png',
    'cordless-paint-sprayer-dual-battery': 'img-mtm52kfv-98b0cb15.png',
    'cordless-paint-sprayer-bare-1000ml': 'img-mtm52h14-c3c30a44.png',
    'pneumatic-rivnut-gun': 'img-mtm52mz9-dbdc7b80.png',
}
for slug, png in mapping.items():
    im = Image.open(os.path.join(MO, png)).convert('RGBA')
    bg = Image.new('RGB', im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3])
    out = os.path.join(DST, slug + '.jpg')
    bg.save(out, 'JPEG', quality=92)
    print(slug, os.path.getsize(out), im.size)

# sandblaster original is clean -> copy direct
shutil.copyfile(os.path.join(SRC, 'pneumatic-sandblaster-gun.jpg'),
                os.path.join(DST, 'pneumatic-sandblaster-gun.jpg'))
print('pneumatic-sandblaster-gun direct-copy',
      os.path.getsize(os.path.join(DST, 'pneumatic-sandblaster-gun.jpg')))
