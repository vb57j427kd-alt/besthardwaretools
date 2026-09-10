import os, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)

items = [
    ("heavy-duty-locking-drawer-slide", "https://cbu01.alicdn.com/img/ibank/O1CN01vblQdp1W2qoMVlyVu_!!2200619922731-0-cib.jpg"),
    ("industrial-drawer-sliding-track", "https://cbu01.alicdn.com/img/ibank/O1CN01TeykeQ1mWBzsapCYl_!!2216799944961-0-cib.jpg"),
    ("soft-close-cabinet-slide", "https://cbu01.alicdn.com/img/ibank/O1CN01cwzuiP1kG2ewlVGGz_!!3893524655-0-cib.jpg"),
    ("crv-woodworking-chisel-set", "https://cbu01.alicdn.com/img/ibank/O1CN01OePq2s25wHA6jg5qM_!!2206913207590-0-cib.jpg"),
    ("wide-opening-short-wrench", "https://cbu01.alicdn.com/img/ibank/O1CN01w99lga1n3cttnwcrJ_!!2215898835034-0-cib.jpg"),
    ("mini-adjustable-wrench-set", "https://cbu01.alicdn.com/img/ibank/O1CN01kWitNe1kZjUP0Dwfi_!!2206862114698-0-cib.jpg"),
    ("precision-electric-screwdriver-pen", "https://cbu01.alicdn.com/img/ibank/O1CN01Yx7SFn1HK3KAbXhzg_!!2218882270738-0-cib.jpg"),
    ("high-speed-cordless-drill-kit", "https://cbu01.alicdn.com/img/ibank/O1CN01Xbb9LK23ki17is4Du_!!2218151047294-0-cib.jpg"),
    ("pneumatic-reciprocating-file-machine", "https://cbu01.alicdn.com/img/ibank/O1CN01W1zKM626m1jtpUblL_!!2647737703-0-cib.jpg"),
    ("professional-pneumatic-air-saw", "https://cbu01.alicdn.com/img/ibank/O1CN0180krQA1Lmgd80vhhI_!!2209647711342-0-cib.jpg")
]

for slug, url in items:
    dest = os.path.join(IMG_DIR, slug + "_raw.jpg")
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(dest, "wb") as f:
            f.write(data)
        print(f"Downloaded {slug}")
    except Exception as e:
        print(f"Failed {slug}: {e}")
