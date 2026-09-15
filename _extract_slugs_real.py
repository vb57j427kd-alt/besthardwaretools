# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(r"C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\products_data.py")
text = p.read_text(encoding="utf-8")
slugs = re.findall(r'"slug"\s*:\s*"([^"]+)"', text)
cats = re.findall(r'"cat"\s*:\s*"([^"]+)"', text)
out = Path(r"C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\_slugs_real.txt")
from collections import Counter
lines = [f"TOTAL slugs={len(slugs)} cats={len(cats)}", f"COUNTS={dict(Counter(cats))}", ""]
lines += sorted(slugs)
out.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print("TOTAL", len(slugs), dict(Counter(cats)))
