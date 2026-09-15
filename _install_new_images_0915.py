# -*- coding: utf-8 -*-
import re
from pathlib import Path
from PIL import Image

MEDIA = Path(r"C:\Users\sy911\AccioWork\2026-09-01-09-34-57-985-c27dbc9c\media-output")
CAND = Path(r"C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\1688-sourcing\candidates-0915")
SITE = Path(r"C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site")
IMG = SITE / "images"

mapping = [
    (MEDIA / "img-mu20zxt3-2183a57c.png", "stainless-360-pivot-hinge.jpg"),
    (MEDIA / "img-mu2130u5-7b2bc758.png", "detachable-stainless-hinge.jpg"),
    (MEDIA / "img-mu212joc-d7026cf7.png", "self-closing-spring-hinge.jpg"),
    (MEDIA / "img-mu213afg-32c29485.png", "14-in-1-insulated-ratchet-screwdriver-set.jpg"),
    (MEDIA / "img-mu2151mr-8efd78a4.png", "8-inch-combination-pliers-190mm.jpg"),
    (MEDIA / "img-mu214u6l-39e0105f.png", "6-inch-crv-combination-pliers-160mm.jpg"),
    (MEDIA / "img-mu2150qj-b8b2fa05.png", "12v-mini-cordless-angle-grinder.jpg"),
    (CAND / "cordless-angle-grinder-b.jpg", "brushless-cordless-angle-grinder-21v.jpg"),
    (CAND / "pneumatic-spray-gun-h827.jpg", "hvlp-pneumatic-spray-gun.jpg"),
    (MEDIA / "img-mu21510z-39aa2da5.png", "w71g-pneumatic-spray-gun.jpg"),
]

text = (SITE / "products_data.py").read_text(encoding="utf-8-sig")
existing = set(re.findall(r'"slug"\s*:\s*"([^"]+)"', text))

for src, name in mapping:
    slug = name[:-4]
    if slug in existing:
        print("SLUG CONFLICT", slug)
    im = Image.open(src).convert("RGB")
    if im.size != (800, 800):
        im = im.resize((800, 800), Image.LANCZOS)
    dst = IMG / name
    im.save(dst, "JPEG", quality=88, optimize=True)
    print(name, im.size, dst.stat().st_size)
