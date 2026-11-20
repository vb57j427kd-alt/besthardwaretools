import json, re, io
p = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\_tmp_batch20b\copy_p2.json'
s = r'C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site\_tmp_batch20b\chunk2.txt'
d = json.load(io.open(p, encoding='utf-8'))
src = io.open(s, encoding='utf-8').read()
slugs = re.findall(r'^slug: (\S+)', src, re.M)
print('objects', len(d), 'src', len(slugs))
print('order match', [x['slug'] for x in d] == slugs)
print('unique', len(set(x['slug'] for x in d)))
print('desc', sum(1 for x in d if x['field'] == 'desc'), 'points', sum(1 for x in d if x['field'] == 'points'))
for x in d:
    t = x['text']; n = len(t.split()); bad = []
    if not t.isascii(): bad.append('nonascii')
    if '"' in t: bad.append('quote')
    if x['field'] == 'desc' and (not t.endswith('.') or n < 20 or n > 45): bad.append('desc%d' % n)
    if x['field'] == 'points' and (t.endswith('.') or n < 15 or n > 40): bad.append('pt%d' % n)
    if bad: print(x['slug'], bad, n)
print('wordcounts', [len(x['text'].split()) for x in d])
