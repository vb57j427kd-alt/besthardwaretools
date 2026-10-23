import os, re, io, sys
sys.path.insert(0, r"C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site")
from products_data import PRODUCTS
root = os.getcwd()
sm = io.open(os.path.join(root,"sitemap.xml"), encoding="utf-8").read()
urls = re.findall(r"<loc>([^<]+)</loc>", sm)
prod = [u for u in urls if "/products/" in u]
print("sitemap urls", len(urls), "product urls", len(prod), "products", len(PRODUCTS))
missing_page = [p["slug"] for p in PRODUCTS if not os.path.exists(os.path.join(root,"products",p["slug"]+".html"))]
missing_img = [p["slug"] for p in PRODUCTS if not os.path.exists(os.path.join(root,"images",p["slug"]+".jpg"))]
print("missing pages", len(missing_page), missing_page[:5])
print("missing images", len(missing_img), missing_img[:5])
new = PRODUCTS[-10:]
for p in new:
    f = os.path.join(root,"products",p["slug"]+".html")
    h = io.open(f, encoding="utf-8").read()
    print(p["slug"], os.path.getsize(f), "img" if p["img"] in h else "NOIMG", "inSitemap" if p["slug"] in sm else "NOT-IN-SITEMAP")
