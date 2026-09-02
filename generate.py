# -*- coding: utf-8 -*-
"""Generate Best Hardware Tools static site: index.html + products/*.html + seo files."""
import os
from datetime import datetime
from products_data import SITE, CATEGORIES, PRODUCTS, RELATED_INDEX

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = SITE["domain"]
URL = f"https://{DOMAIN}/"
YEAR = datetime.now().year

CSS = """
:root{--bg:#0B0F14;--bg2:#11161D;--card:#171E27;--card2:#1C2532;--accent:#FF8A2A;--accent2:#E06B10;--t1:#E8EDF2;--t2:#A7B3C2;--t3:#6E7B8A;--line:#232C38;--gold:#FF8A2A}
*{margin:0;padding:0;box-sizing:border-box}
a{text-decoration:none;color:inherit}
body{background:var(--bg);color:var(--t1);font-family:'Inter',system-ui,-apple-system,sans-serif;line-height:1.6}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}
h1,h2,h3,h4,.logo{font-family:'Oswald',sans-serif;font-weight:600;letter-spacing:.02em}
nav{position:sticky;top:0;z-index:100;background:rgba(11,15,20,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{font-size:1.25rem;color:var(--t1)}.logo b{color:var(--accent)}
.nav-links{display:flex;gap:22px;font-size:.9rem;color:var(--t2)}
.nav-links a:hover{color:var(--accent)}
.hero{background:radial-gradient(ellipse at 70% 20%,#1E2A38 0%,var(--bg) 60%);padding:90px 0 70px;border-bottom:1px solid var(--line)}
.hero h1{font-size:2.9rem;line-height:1.15;margin-bottom:18px}
.hero h1 span{color:var(--accent)}
.hero p{color:var(--t2);max-width:640px;font-size:1.08rem;margin-bottom:28px}
.btn{display:inline-block;padding:12px 28px;border-radius:6px;font-weight:600;font-size:.95rem;transition:.2s}
.btn-p{background:var(--accent);color:#14181d}.btn-p:hover{background:var(--accent2);transform:translateY(-1px)}
.btn-o{border:1px solid var(--line);color:var(--t1)}.btn-o:hover{border-color:var(--accent);color:var(--accent)}
.btn-wa{background:#25D366;color:#0d1216}.btn-wa:hover{filter:brightness(1.08);transform:translateY(-1px)}
.trust{display:flex;gap:40px;flex-wrap:wrap;margin-top:36px}
.trust div b{font-size:1.6rem;color:var(--accent);font-family:'Oswald';display:block}
.trust div span{font-size:.82rem;color:var(--t3)}
section{padding:64px 0;border-bottom:1px solid var(--line)}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:28px}
.sec-head h2{font-size:1.8rem}
.sec-head a{color:var(--t3);font-size:.85rem}.sec-head a:hover{color:var(--accent)}
.cat-tag{display:inline-block;background:rgba(255,138,42,.12);color:var(--accent);border:1px solid rgba(255,138,42,.3);padding:3px 12px;border-radius:20px;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:14px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.pc{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;transition:.25s;display:block}
.pc:hover{transform:translateY(-4px);border-color:rgba(255,138,42,.5);box-shadow:0 12px 34px rgba(0,0,0,.45)}
.pc-img{position:relative;background:#0d131a;overflow:hidden}
.pc-img img{width:100%;height:230px;object-fit:cover;display:block}
.badge{position:absolute;top:12px;left:12px;background:var(--accent);color:#14181d;font-size:.7rem;font-weight:700;padding:3px 10px;border-radius:4px;letter-spacing:.06em}
.pc-body{padding:18px}
.pc-body h3{font-size:1.02rem;margin-bottom:6px;line-height:1.35}
.pc-body p{color:var(--t3);font-size:.84rem;margin-bottom:10px}
.price-row{display:flex;justify-content:space-between;align-items:baseline}
.price{color:var(--accent);font-weight:700;font-size:1.02rem}
.moq{color:var(--t3);font-size:.78rem}
.feats{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.feat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:22px}
.feat h4{color:var(--accent);font-size:1.02rem;margin-bottom:8px}
.feat p{color:var(--t2);font-size:.86rem}
.cta{background:linear-gradient(135deg,#161d26,#1d2a38);text-align:center;padding:70px 24px;border-bottom:1px solid var(--line)}
.cta h2{font-size:2rem;margin-bottom:14px}
.cta p{color:var(--t2);max-width:560px;margin:0 auto 28px}
footer{background:var(--bg2);padding:48px 0 30px;border-top:1px solid var(--line)}
.foot{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:30px}
.foot h5{font-family:'Oswald';font-size:.95rem;margin-bottom:12px;color:var(--t1)}
.foot a{display:block;color:var(--t3);font-size:.85rem;margin-bottom:8px}
.foot a:hover{color:var(--accent)}
.copy{text-align:center;color:var(--t3);font-size:.78rem;margin-top:36px;border-top:1px solid var(--line);padding-top:20px}
/* product page */
.crumb{color:var(--t3);font-size:.82rem;padding:18px 0}
.crumb a:hover{color:var(--accent)}
.pd{display:grid;grid-template-columns:1.1fr 1fr;gap:44px;padding:30px 0 60px}
.pd-img{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;align-self:start}
.pd-img img{width:100%;display:block}
.pd-info h1{font-size:1.9rem;line-height:1.2;margin-bottom:14px}
.pd-price{font-size:1.5rem;color:var(--accent);font-weight:700;margin-bottom:4px}
.pd-moq{color:var(--t3);font-size:.9rem;margin-bottom:18px}
.pd-desc{color:var(--t2);font-size:.95rem;margin-bottom:22px}
.cta-row{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:26px}
.specs{width:100%;border-collapse:collapse;margin-bottom:26px}
.specs td{border:1px solid var(--line);padding:10px 14px;font-size:.88rem}
.specs td:first-child{color:var(--t3);width:38%;background:var(--bg2)}
.specs td:last-child{color:var(--t1)}
.pts{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px}
.pts h4{color:var(--accent);font-family:'Oswald';margin-bottom:12px;font-size:1.05rem}
.pts li{color:var(--t2);font-size:.88rem;margin:8px 0 8px 18px}
.related{margin:0;padding:50px 0}
/* modal */
.modal{display:none;position:fixed;inset:0;z-index:200;background:rgba(5,8,11,.78);backdrop-filter:blur(4px)}
.modal.open{display:flex;align-items:center;justify-content:center}
.mbox{background:var(--bg2);border:1px solid var(--line);border-radius:20px;max-width:520px;width:92%;max-height:90vh;overflow:auto;padding:30px;box-shadow:0 24px 80px rgba(0,0,0,.6)}
.mbox h3{font-size:1.3rem;margin-bottom:6px}
.mbox .prod-line{color:var(--accent);font-size:.85rem;margin-bottom:18px}
.fg{margin-bottom:14px}
.fg label{display:block;color:var(--t3);font-size:.8rem;margin-bottom:6px}
.fg input{width:100%;padding:11px 14px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--t1);font-size:.92rem;outline:none}
.fg input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(255,138,42,.15)}
.mbtn{width:100%;padding:13px;border:none;border-radius:8px;background:var(--accent);color:#14181d;font-weight:700;font-size:.95rem;cursor:pointer;transition:.2s}
.mbtn:hover{background:var(--accent2);transform:translateY(-1px)}
.mclose{position:sticky;float:right;background:none;border:none;color:var(--t3);font-size:1.4rem;cursor:pointer;line-height:1}
.bank{margin-top:18px;border-top:1px solid var(--line);padding-top:16px}
.bank h5{font-family:'Oswald';color:var(--t1);margin-bottom:10px;font-size:.95rem}
.bank-row{display:flex;justify-content:space-between;gap:16px;padding:7px 0;border-bottom:1px dashed var(--line);font-size:.85rem}
.blabel{color:var(--t3)}
.bvalue{color:var(--t1);font-weight:600;text-align:right;word-break:break-all}
.bvalue.hl{color:var(--accent)}
.bank-note{color:var(--t3);font-size:.76rem;line-height:1.5;margin-top:10px}
.success{display:none;text-align:center;padding:22px 0}
.success h4{color:#25D366;font-size:1.2rem;margin-bottom:10px}
.success p{color:var(--t2);font-size:.9rem}
@media(max-width:900px){.grid,.feats{grid-template-columns:repeat(2,1fr)}.pd{grid-template-columns:1fr}.foot{grid-template-columns:1fr 1fr}.hero h1{font-size:2.2rem}}
@media(max-width:560px){.grid{grid-template-columns:1fr}.nav-links{display:none}.trust{gap:20px}}
"""

JS = """
function openOrder(name){currentOrderProduct=name;document.getElementById('orderProduct').textContent=name;document.getElementById('modal').classList.add('open');document.getElementById('orderSuccess').style.display='none';document.getElementById('orderFormWrap').style.display='block'}
function closeOrder(){document.getElementById('modal').classList.remove('open')}
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeOrder()});
document.getElementById('modal').addEventListener('click',function(e){if(e.target===this)closeOrder()});
function submitOrder(e){e.preventDefault();var n=document.getElementById('orderName').value.trim(),p=document.getElementById('orderPhone').value.trim(),a=document.getElementById('orderAddress').value.trim(),c=document.getElementById('orderCityZip').value.trim();if(!n||!p||!a||!c)return;var d=new Date().toISOString().split('T')[0];var m='New Order - '+currentOrderProduct+'\\nName: '+n+'\\nPhone: '+p+'\\nAddress: '+a+'\\nCity/ZIP: '+c+'\\nDate: '+d+'\\n\\u2014 Sent via besthardwaretools.com';window.open('https://wa.me/8618669693290?text='+encodeURIComponent(m),'_blank');var fd=new FormData();fd.append('product',currentOrderProduct);fd.append('name',n);fd.append('phone',p);fd.append('address',a);fd.append('cityzip',c);fd.append('date',d);fetch('https://formspree.io/f/xeeynyba',{method:'POST',body:fd,headers:{Accept:'application/json'}}).catch(function(){});document.getElementById('orderFormWrap').style.display='none';document.getElementById('orderSuccess').style.display='block'}
"""

def head(title, desc, canonical, ogimg):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="google-site-verification" content="34SoIYpfZyiFCfgYUijxbkcMA456YX6Yut8l1RegbqU">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="hardware tools supplier, hand tools, power tools, pneumatic tools, cabinet hardware, wholesale tools, factory direct, OEM tools, Best Hardware Tools">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{ogimg}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ogimg}">
<meta name="theme-color" content="#0B0F14">
<link rel="preconnect" href="https://sc04.alicdn.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5J9VBPKTB4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-5J9VBPKTB4')</script>
<script type="text/javascript">(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)}})(window,document,"clarity","script","xtrv7vr8dn")</script>
<style>{CSS}</style>
</head>
"""

def nav(active=""):
    links = "".join(f'<a href="/#cat-{c["id"]}"{" style=\"color:var(--accent)\"" if active==c["id"] else ""}>{c["nav"]}</a>' for c in CATEGORIES)
    return f"""<nav><div class="wrap nav-in">
<a href="/" class="logo">BEST <b>HARDWARE</b> TOOLS</a>
<div class="nav-links"><a href="/">Home</a>{links}<a href="/#contact">Contact</a></div>
</div></nav>"""

def order_modal():
    return f"""<div class="modal" id="modal"><div class="mbox">
<button class="mclose" onclick="closeOrder()">&times;</button>
<div id="orderFormWrap">
<h3>Order Now</h3>
<p class="prod-line">Product: <span id="orderProduct"></span></p>
<form onsubmit="submitOrder(event)">
<div class="fg"><label>Full Name *</label><input type="text" id="orderName" required></div>
<div class="fg"><label>Phone / WhatsApp *</label><input type="tel" id="orderPhone" placeholder="+1 234 567 8900" required></div>
<div class="fg"><label>Address *</label><input type="text" id="orderAddress" required></div>
<div class="fg"><label>City / State / ZIP *</label><input type="text" id="orderCityZip" required></div>
<button class="mbtn" type="submit">Submit Order</button>
</form>
<div class="bank"><h5>Bank Transfer Details</h5>
<div class="bank-row"><span class="blabel">Beneficiary</span><span class="bvalue">{SITE['bank_beneficiary']}</span></div>
<div class="bank-row"><span class="blabel">Account No.</span><span class="bvalue hl">{SITE['bank_account']}</span></div>
<div class="bank-row"><span class="blabel">Swift Code</span><span class="bvalue">{SITE['bank_swift']}</span></div>
<p class="bank-note">{SITE['bank_note']}</p></div>
</div>
<div class="success" id="orderSuccess"><h4>Request Received</h4><p>Thank you! We have opened WhatsApp with your order details and emailed our team. We will confirm within 24 hours.</p><a class="btn btn-o" style="margin-top:16px" href="mailto:{SITE['email']}">Email us: {SITE['email']}</a></div>
</div></div>"""

def footer():
    return f"""<footer><div class="wrap">
<div class="foot">
<div><a href="/" class="logo">BEST <b>HARDWARE</b> TOOLS</a><p style="color:var(--t3);font-size:.85rem;margin-top:12px">Factory-direct hardware and tools for global buyers. OEM/ODM welcome.</p></div>
<div><h5>Categories</h5>{''.join(f'<a href="/#cat-{c["id"]}">{c["name"]}</a>' for c in CATEGORIES)}</div>
<div><h5>Company</h5><a href="/#why">Why Us</a><a href="/#oem">OEM/ODM</a><a href="/#contact">Contact</a></div>
<div><h5>Contact</h5><a href="https://wa.me/8618669693290" target="_blank" rel="noopener">WhatsApp: +86 186 6969 3290</a><a href="mailto:{SITE['email']}">{SITE['email']}</a></div>
</div>
<div class="copy">&copy; {YEAR} {SITE['brand']} ({SITE['domain']}). All rights reserved. Supplier of {', '.join(c['name'] for c in CATEGORIES)}.</div>
</div></footer>
<script>var currentOrderProduct='';</script>
{order_modal()}
<script>{JS}</script>
</body></html>"""

def product_card(p, full=True):
    rel = f"/products/{p['slug']}.html"
    d = p['desc'][:110] + ("..." if len(p['desc'])>110 else "")
    return f"""<a href="{rel}" class="pc"><div class="pc-img"><img src="{p['img']}" alt="{p['name']}" width="400" height="280" loading="lazy" decoding="async"><span class="badge">{p['badge']}</span></div><div class="pc-body"><h3>{p['name']}</h3><p>{d}</p><div class="price-row"><span class="price">{p['price']}</span><span class="moq">{p['moq']}</span></div></div></a>"""

def index_html():
    sections = ""
    for cid in ["power-tools", "pneumatic-tools", "hand-tools", "hardware"]:
        c = next(c for c in CATEGORIES if c["id"] == cid)
        items = [p for p in PRODUCTS if p["cat"] == c["id"]]
        cards = "".join(product_card(p) for p in items)
        sections += f"""<section id="cat-{c['id']}"><div class="wrap">
<div class="sec-head"><div><span class="cat-tag">{c['name']}</span><h2>{c['name']}</h2></div></div>
<div class="grid">{cards}</div>
</div></section>"""
    feats = [
        ("Factory Direct Pricing", "No middlemen - wholesale prices straight from Chinese manufacturing clusters."),
        ("OEM / ODM Support", "Custom branding, packaging, colors and specifications for your market."),
        ("Global Export Experience", "Shipping to 100+ countries with export documentation support."),
        ("Quality Control", "Multi-step inspection and durable materials you can rely on."),
        ("Low MOQ", "Most items start from MOQ 1 - perfect for testing new markets."),
        ("Fast Response", "WhatsApp and email support answered within 24 hours."),
    ]
    # Daily rotating homepage content (day of month % 3): 1 = extra Why Us feat, 2 = OEM/ODM paragraph, 0 = category intro under hero
    day = datetime.now().day
    slot = day % 3
    if slot == 1:
        feats.append(("Certified Manufacturing Base", "Audited partner factories with verified capacity and export-grade quality procedures."))
        feats.append(("Flexible Shipping Options", "Sea, air and express freight with container consolidation, live tracking and customs paperwork handled for you."))
        feats.append(("Compliance & Test Reports", "CE-marked products from ISO9001-managed lines - share test reports and compliance documents to clear customs and satisfy EU, US and MENA buyers."))
        feats.append(("One-Stop Container Consolidation", "Mix hardware, hand tools, power tools and pneumatic tools in a single container - one shipment, one invoice and lower freight cost per unit for multi-category buyers."))
        feats.append(("Priority Production Slots", "Long-running partnerships guarantee reserved capacity at partner factories - stable lead times for repeat orders even in peak season."))
    oem_extra = ('<p style="color:var(--t2);margin-top:14px">From private-label packaging to full product customization, our partner factories handle tooling, color matching, logo printing and pre-shipment inspection. Share your spec sheet or sample - our engineering team replies within 24 hours with a factory-direct quotation and production timeline.</p><p style="color:var(--t2);margin-top:14px">Testing a sample first is the fastest way to lock in quality - we can adjust materials, finishes, packaging and print before you commit to a full container. Your drawings, logos and product specifications stay protected under our IP confidentiality policy, giving importers and brands a safe path to private-label and co-development projects.</p><p style="color:var(--t2);margin-top:14px">Production capacity is pre-validated across our partner lines, with CE-marked output and ISO9001-managed processes so compliance documents, test reports and certificates are ready when your shipment clears customs. We consolidate mixed SKUs - hardware, hand tools, power tools and pneumatic tools - into one container and one invoice, cutting freight cost and simplifying paperwork for multi-category importers and distributors.</p><p style="color:var(--t2);margin-top:14px">Every order is protected from factory floor to your warehouse: export-grade cartons with moisture-resistant packing, container loading supervised at the factory gate, and each batch shipped with the packing list, commercial invoice and compliance certificates your customs broker needs. Need to restock fast? Express freight from major Chinese ports keeps emergency lead times short, while scheduled sea freight protects margins on full containers - so your inventory plan stays predictable whether you order one sample or a 40HQ.</p>' if slot == 2 else "")
    cat_intro = ('<p style="color:var(--t2);margin-top:22px;max-width:720px">Four sourcing categories under one roof: <b style="color:var(--t1)">Hardware</b> for cabinet and furniture fittings, <b style="color:var(--t1)">Hand Tools</b> for daily maintenance and repair, <b style="color:var(--t1)">Power Tools</b> for cordless and electric work, and <b style="color:var(--t1)">Pneumatic Tools</b> for compressor-powered jobs - each supplied factory-direct with consistent quality and low MOQs.</p><p style="color:var(--t2);margin-top:10px;max-width:720px">For contractors, woodworkers, maintenance teams and auto-service shops, the range covers the full jobsite chain - from cabinet hardware and hand tools for finishing work to cordless power tools and compressor-fed pneumatic equipment for heavy tasks. Order across categories in one shipment to cut freight cost and keep every project on one invoice.</p><p style="color:var(--t2);margin-top:10px;max-width:720px">Inside each category the selection runs deep - stainless hinges, slides and cabinet pulls for hardware buyers, CR-V ratchets and screwdriver sets for maintenance crews, brushless cordless drills, grinders and saws for contractors, plus air nailers, staplers, spray guns and impact wrenches for workshops and auto-service centers. Every line is kept in stock for repeat orders, so you can test a single SKU first and scale up as demand grows.</p>' if slot == 0 else "")
    feat_html = "".join(f'<div class="feat"><h4>{t}</h4><p>{d}</p></div>' for t, d in feats)
    stats = [("12+", "Core Product Lines"), ("100+", "Countries Served"), ("24h", "Response Time"), ("1 pc", "Minimum Order")]
    stats_html = "".join(f'<div><b>{n}</b><span>{l}</span></div>' for n, l in stats)
    jsonld = f'''{{
"@context":"https://schema.org","@type":"Organization","name":"{SITE['brand']}",
"url":"{URL}","parentOrganization":{{"@type":"Organization","name":"Linyi Strawberry International Trade Co., Ltd"}},
"contactPoint":{{"@type":"ContactPoint","contactType":"sales","email":"{SITE['email']}"}},
"areaServed":{{"@type":"Place","name":"Worldwide"}},
"knowsAbout":["Hardware","Hand Tools","Power Tools","Pneumatic Tools","Cabinet Hardware","Industrial Tools"]}}'''
    html = head("Best Hardware Tools - Factory Direct Hardware, Hand Tools, Power Tools & Pneumatic Tools Supplier", "Best Hardware Tools supplies factory-direct hardware, hand tools, power tools and pneumatic tools worldwide. Low MOQ, OEM/ODM support, wholesale pricing. WhatsApp +86 186 6969 3290.", URL + "", URL + "images/brushless-cordless-drill.jpg")
    html += f"""<script type="application/ld+json">{jsonld}</script>
<body>
{nav()}
<header class="hero"><div class="wrap">
<h1>Hardware &amp; Tools, <span>Factory Direct</span> to the World</h1>
<p>{SITE['tagline']}. From cabinet hardware to cordless power tools and pneumatic equipment - sourced from China's manufacturing clusters with wholesale pricing, low MOQ and OEM/ODM support for importers, distributors and brands worldwide.</p>
<a href="#cat-hardware" class="btn btn-p">Shop Categories</a> <a href="https://wa.me/8618669693290" class="btn btn-wa" target="_blank" rel="noopener">WhatsApp Inquiry</a>
<div class="trust">{stats_html}</div>
{cat_intro}
</div></header>
{sections}
<section id="why"><div class="wrap"><div class="sec-head"><div><span class="cat-tag">Why Us</span><h2>Why Global Buyers Choose Us</h2></div></div><div class="feats">{feat_html}</div></div></section>
<section id="oem"><div class="wrap"><div class="sec-head"><div><span class="cat-tag">OEM / ODM</span><h2>Build Your Own Brand</h2></div></div>
<div class="grid">{product_card(PRODUCTS[0])}{product_card(PRODUCTS[3])}{product_card(PRODUCTS[6])}</div>
<p style="color:var(--t2);margin-top:22px">Tell us your market and target price - we handle sourcing, quality control, custom packaging and shipping. <a href="https://wa.me/8618669693290" style="color:var(--accent)" target="_blank" rel="noopener">Start a project on WhatsApp</a>.</p>
{oem_extra}
</div></section>
<section id="contact" class="cta"><div class="wrap">
<h2>Ready to Source Hardware &amp; Tools?</h2>
<p>Get factory-direct quotes for your market. Low MOQ, fast samples, worldwide shipping.</p>
<a href="https://wa.me/8618669693290" class="btn btn-wa" target="_blank" rel="noopener">Chat on WhatsApp +86 186 6969 3290</a> <a href="mailto:{SITE['email']}" class="btn btn-o">Email {SITE['email']}</a>
</div></section>
{footer()}
</html>"""
    return html

def product_page(p):
    title = f"{p['name']} | Factory Direct | Best Hardware Tools"
    desc = p['desc'][:150]
    canonical = f"{URL}products/{p['slug']}.html"
    specs = "".join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in p["specs"])
    pts = "".join(f"<li>{x}</li>" for x in p["points"])
    rel = "".join(product_card(RELATED_INDEX[s]) for s in p["related"] if s in RELATED_INDEX)
    jsonld = f'''{{"@context":"https://schema.org","@type":"Product","name":"{p['name']}","image":"{p['img']}","description":"{desc}","brand":{{"@type":"Brand","name":"{SITE['brand']}"}},"offers":{{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"{canonical}"}}}}'''
    html = head(title, desc, canonical, URL + "images/" + p['slug'] + ".jpg")
    html += f"""<script type="application/ld+json">{jsonld}</script>
<body>
{nav()}
<div class="wrap crumb"><a href="/">Home</a> &rsaquo; <a href="/#cat-{p['cat']}">{next(c['name'] for c in CATEGORIES if c['id']==p['cat'])}</a> &rsaquo; {p['name']}</div>
<div class="wrap pd">
<div class="pd-img"><img src="{p['img']}" alt="{p['name']}" width="600" height="450"></div>
<div class="pd-info">
<h1>{p['name']}</h1>
<div class="pd-price">{p['price']}</div>
<div class="pd-moq">{p['moq']} &middot; FOB China &middot; Worldwide shipping</div>
<p class="pd-desc">{p['desc']}</p>
<div class="cta-row">
<a href="javascript:void(0)" onclick="openOrder('{p['name']}')" class="btn btn-p">Order Now</a>
<a href="https://wa.me/8618669693290?text={p['name'].replace(' ','%20')}%20inquiry" class="btn btn-wa" target="_blank" rel="noopener">WhatsApp Inquiry</a>
</div>
<table class="specs">{specs}</table>
<div class="pts"><h4>Why Buyers Choose This Product</h4><ul>{pts}</ul></div>
</div>
</div>
<section class="related"><div class="wrap"><div class="sec-head"><div><span class="cat-tag">Related</span><h2>You May Also Like</h2></div></div><div class="grid">{rel}</div></div></section>
{footer()}
</html>"""
    return html

def main():
    os.makedirs(os.path.join(BASE, "products"), exist_ok=True)
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html())
    for p in PRODUCTS:
        with open(os.path.join(BASE, "products", f"{p['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(product_page(p))
    # CNAME
    with open(os.path.join(BASE, "CNAME"), "w", encoding="utf-8") as f:
        f.write(DOMAIN + "\n")
    # robots.txt
    with open(os.path.join(BASE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {URL}sitemap.xml\n")
    # sitemap.xml
    urls = [f"<url><loc>{URL}</loc><priority>1.0</priority><changefreq>daily</changefreq></url>"]
    for p in PRODUCTS:
        urls.append(f"<url><loc>{URL}products/{p['slug']}.html</loc><priority>0.8</priority><changefreq>weekly</changefreq></url>")
    with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    # 404
    with open(os.path.join(BASE, "404.html"), "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>404 - Best Hardware Tools</title><meta name="robots" content="noindex"><link rel="canonical" href="{URL}404.html"></head><body style="background:#0B0F14;color:#E8EDF2;font-family:Inter,sans-serif;text-align:center;padding:80px 20px"><h1 style="font-family:Oswald;font-size:3rem;color:#FF8A2A">404</h1><p>Page not found.</p><p><a href="/" style="color:#FF8A2A">Back to Best Hardware Tools</a></p></body></html>""")
    print("Generated:", len(PRODUCTS) + 1, "pages + CNAME/robots/sitemap/404")

if __name__ == "__main__":
    main()
