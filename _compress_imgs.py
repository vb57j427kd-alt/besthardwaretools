# -*- coding: utf-8 -*-
import os
from PIL import Image

DST = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\images'
files = sorted(f for f in os.listdir(DST) if f.endswith('.jpg'))
total_before = total_after = 0
changed = 0
for fn in files:
    p = os.path.join(DST, fn)
    before = os.path.getsize(p)
    total_before += before
    if before <= 80 * 1024:
        total_after += before
        continue
    try:
        im = Image.open(p)
        w, h = im.size
        if max(w, h) > 900:
            ratio = 900 / max(w, h)
            im = im.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
        im = im.convert('RGB')
        im.save(p, 'JPEG', quality=78, optimize=True, progressive=True)
        after = os.path.getsize(p)
        total_after += after
        changed += 1
        print('%-58s %6.0f KB -> %6.0f KB' % (fn, before / 1024, after / 1024))
    except Exception as e:
        total_after += before
        print('SKIP', fn, e)
print('---')
print('changed:', changed, '| total: %.1f MB -> %.1f MB' % (total_before / 1048576, total_after / 1048576))
