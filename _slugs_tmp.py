import re, io
src = io.open(r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\products_data.py', encoding='utf-8').read()
slugs = re.findall(r'"slug":\s*"([^"]+)"', src)
print('COUNT:', len(slugs))
print('\n'.join(slugs))
