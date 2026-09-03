# -*- coding: utf-8 -*-
import io, os

base = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site'
slugs = ['folding-table-leaf-hinge-90', 'square-black-aluminum-cabinet-handle', 'ratcheting-combination-wrench-10mm',
         '9-inch-chrome-vanadium-combination-pliers', '6-inch-drop-forged-combination-pliers',
         'cordless-brushless-leaf-blower', 'cordless-turbo-fan-blower-kit', 'heavy-duty-cordless-leaf-blower',
         'pneumatic-metal-shear', 'pneumatic-wire-shear-s110']
pages = all(os.path.exists(os.path.join(base, 'products', s + '.html')) for s in slugs)
sm = io.open(os.path.join(base, 'sitemap.xml'), encoding='utf-8').read()
in_sm = all(('products/%s.html' % s) in sm for s in slugs)
idx = io.open(os.path.join(base, 'index.html'), encoding='utf-8').read()
in_idx = all(('products/%s.html' % s) in idx for s in slugs)
print('pages all exist:', pages)
print('sitemap contains all:', in_sm)
print('index cards contain all:', in_idx)
print('sm total urls:', sm.count('<loc>'))
