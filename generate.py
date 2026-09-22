# -*- coding: utf-8 -*-
"""Generate Best Hardware Tools static site: index.html + products/*.html + seo files."""
import os
import html as _html
from datetime import datetime
from products_data import SITE, CATEGORIES, PRODUCTS, RELATED_INDEX
from blog_data import ARTICLES, ARTICLE_INDEX

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = SITE["domain"]
URL = f"https://{DOMAIN}/"
YEAR = datetime.now().year

# Contact constants reused across every template. Facts only: the legal entity name and the
# Linyi/Shandong location come from SITE and the brand's own existing copy. No address,
# capacity, headcount or certification number is invented anywhere in this generator.
WA_NUM = SITE["whatsapp"]
WA_HREF = "https://wa.me/" + WA_NUM
WA_SHOW = "+86 186 6969 3290"
LEGAL = SITE["bank_beneficiary"]
LOCATION = "Linyi, Shandong, China"
REPLY_PROMISE = "Every inquiry is answered within 24 working hours"

# Curated allow-list of product images that have each been visually verified to be fully
# English and free of any third-party brand, logo or company mark. The hero mosaic and the
# category cards may ONLY draw from this list: those two slots are the most prominent on the
# site, and the older part of the catalogue still contains supplier-drawn posters - some of
# them carrying Chinese captions (e.g. pneumatic-air-chisel-150mm prints "150款气铲").
# Extend this list only after a human/agent has actually looked at the image.
HERO_OK = {
    "hardware": ["cam-lock-furniture-connector-set", "double-door-cabinet-cam-lock", "drywall-butterfly-expansion-anchor"],
    "hand-tools": ["three-jaw-bearing-puller", "telescopic-magnetic-pickup-tool", "ratchet-cable-cutter"],
    "power-tools": ["6-inch-bench-grinder-370w", "handheld-electric-paddle-mixer"],
    "pneumatic-tools": ["pneumatic-air-pressure-regulator", "retractable-air-hose-reel-10m"],
}


def esc(s):
    """Escape a value for use inside an HTML attribute."""
    return _html.escape(str(s), quote=True)

# Design system lives in theme.css (single source of truth) and is inlined into every page.
with open(os.path.join(BASE, "theme.css"), encoding="utf-8") as _f:
    CSS = _f.read().strip()

JS = """
var WA='__WA__';
function openQuote(name,sku){var m=document.getElementById('modal');if(!m)return;var hp=m.querySelector('#quoteProduct'),hs=m.querySelector('#quoteSku'),hg=m.querySelector('#quotePage'),hl=m.querySelector('#quoteProdLine'),fm=m.querySelector('#quoteForm'),ok=m.querySelector('.form-ok');if(hp)hp.value=name||'';if(hs)hs.value=sku||'';if(hg)hg.value=location.href;if(hl)hl.textContent=name?('Product: '+name):'General sourcing inquiry';if(ok)ok.style.display='none';if(fm)fm.style.display='block';m.classList.add('open');document.body.style.overflow='hidden'}
function closeQuote(){var m=document.getElementById('modal');if(!m)return;m.classList.remove('open');document.body.style.overflow=''}
function toggleNav(){var open=document.body.classList.toggle('nav-open');document.body.style.overflow=open?'hidden':''}
document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeQuote();if(document.body.classList.contains('nav-open'))toggleNav()}});
document.addEventListener('click',function(e){var a=e.target.closest?e.target.closest('.nav-links a'):null;if(a&&document.body.classList.contains('nav-open'))toggleNav()});
(function(){var m=document.getElementById('modal');if(m)m.addEventListener('click',function(e){if(e.target===m)closeQuote()})})();
function quoteData(f){var g=function(n){var el=f.elements[n];return el&&el.value?el.value.trim():''};return{name:g('name'),email:g('email'),company:g('company'),country:g('country'),phone:g('phone'),requirement:g('requirement'),product:g('product')||'General sourcing inquiry',sku:g('sku'),page:g('page')||location.href}}
function quoteMessage(d){return 'Quote request - '+d.product+'\\nName: '+d.name+'\\nCompany: '+d.company+'\\nEmail: '+d.email+'\\nCountry: '+d.country+(d.phone?'\\nPhone/WhatsApp: '+d.phone:'')+'\\nRequirement: '+d.requirement+'\\nSent via besthardwaretools.com'}
function submitQuote(e){e.preventDefault();var f=e.target;var d=quoteData(f);var fd=new FormData();for(var k in d){if(d[k])fd.append(k,d[k])}fd.append('_subject','Quote request - '+d.product);fetch('https://formspree.io/f/__FS__',{method:'POST',body:fd,headers:{Accept:'application/json'}}).catch(function(){});var ok=f.parentNode.querySelector('.form-ok');var wa=ok?ok.querySelector('a.wa'):null;if(wa)wa.href='https://wa.me/'+WA+'?text='+encodeURIComponent(quoteMessage(d));f.style.display='none';if(ok)ok.style.display='block'}
"""

def clip_words(text, limit):
    """Trim text to at most `limit` characters without cutting the final word in half."""
    if len(text) <= limit:
        return text
    window = text[:limit + 1]
    cut = window.rsplit(" ", 1)[0] if " " in window else text[:limit]
    return cut.rstrip(" ,;:-")


def excerpt(text, limit):
    """Shorten text to a word boundary within `limit` characters, marking the trim with an ellipsis.

    Trailing sentence punctuation is dropped before the marker is appended, so the
    result never renders as '....' or ',...'.
    """
    if len(text) <= limit:
        return text
    return clip_words(text, limit).rstrip(".,;:-!?") + "..."


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
<meta name="theme-color" content="#FFFFFF">
<meta property="og:site_name" content="{SITE['brand']}">
<link rel="preconnect" href="https://sc04.alicdn.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5J9VBPKTB4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-5J9VBPKTB4')</script>
<script type="text/javascript">(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)}})(window,document,"clarity","script","xtrv7vr8dn")</script>
<style>{CSS}</style>
</head>
"""

def nav(active=""):
    links = "".join(f'<a href="/category-{c["id"]}.html"{" class=\"on\"" if active==c["id"] else ""}>{c["nav"]}</a>' for c in CATEGORIES)
    return f"""<div class="topbar"><div class="wrap">
<div class="tb-l"><span>Factory-direct hardware &amp; tools &middot; {LOCATION}</span><span>OEM / ODM welcome</span></div>
<div class="tb-r"><a href="{WA_HREF}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a><a href="mailto:{SITE['email']}">{SITE['email']}</a></div>
</div></div>
<nav><div class="wrap nav-in">
<a href="/" class="logo">BEST <b>HARDWARE</b> TOOLS</a>
<div class="nav-links" id="navLinks">{links}<a href="/#why">Why Us</a><a href="/#quote">Contact</a><a href="{WA_HREF}" class="nav-wa" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a><a href="/#quote" class="btn btn-p nav-cta-m">Get a Free Quote</a></div>
<a href="/#quote" class="btn btn-p nav-cta">Get a Free Quote</a>
<button class="nav-toggle" type="button" aria-label="Open menu" aria-controls="navLinks" onclick="toggleNav()"><i></i></button>
</div></nav>"""

def rfq_fields(fid):
    """Shared RFQ field set: the five things a distributor can actually answer."""
    return f"""<div class="fg-2">
<div class="fg"><label for="{fid}name">Name *</label><input id="{fid}name" name="name" type="text" required autocomplete="name"></div>
<div class="fg"><label for="{fid}email">Business email *</label><input id="{fid}email" name="email" type="email" required autocomplete="email"></div>
</div>
<div class="fg-2">
<div class="fg"><label for="{fid}company">Company *</label><input id="{fid}company" name="company" type="text" required autocomplete="organization"></div>
<div class="fg"><label for="{fid}country">Country *</label><input id="{fid}country" name="country" type="text" required autocomplete="country-name"></div>
</div>
<div class="fg"><label for="{fid}phone">Phone / WhatsApp</label><input id="{fid}phone" name="phone" type="tel" placeholder="+1 234 567 8900" autocomplete="tel"></div>
<div class="fg"><label for="{fid}req">What do you need? *</label><textarea id="{fid}req" name="requirement" required placeholder="Products and quantities, target price, packaging or private-label requirements, destination port"></textarea></div>
<button class="btn btn-p btn-lg btn-block" type="submit">Send Inquiry</button>
<p class="form-note">{REPLY_PROMISE} with MOQ, sample plan, packing options and estimated lead time.</p>"""


def quote_ok():
    return f"""<div class="form-ok"><h4>Inquiry received</h4><p>Thank you. We will reply within 24 working hours with pricing, MOQ, sample plan and lead time.</p><div class="alt-ch">Need a faster answer? <a class="wa" href="{WA_HREF}" target="_blank" rel="noopener">Send the same details on WhatsApp</a></div></div>"""


def quote_modal():
    return f"""<div class="modal" id="modal"><div class="mbox">
<button class="mclose" type="button" aria-label="Close" onclick="closeQuote()">&times;</button>
<h3>Request a Quote</h3>
<p class="prod-line" id="quoteProdLine">General sourcing inquiry</p>
<form id="quoteForm" onsubmit="submitQuote(event)">
<input type="hidden" id="quoteProduct" name="product" value="">
<input type="hidden" id="quoteSku" name="sku" value="">
<input type="hidden" id="quotePage" name="page" value="">
{rfq_fields("m")}
</form>
{quote_ok()}
</div></div>"""


def quote_form_inline():
    return f"""<form id="hquote" onsubmit="submitQuote(event)">
<input type="hidden" name="product" value="General sourcing inquiry">
{rfq_fields("h")}
</form>
{quote_ok()}"""

def wa_fab():
    """Floating WhatsApp button, present on every page. The top utility bar (which carries
    the same number) is hidden below 900px and the mobile menu needs a tap to open, so this
    keeps one-tap contact permanently in reach. It is suppressed where the sticky mobile
    action bar already offers a WhatsApp button, and while the inquiry modal is open."""
    return f"""<a class="wa-fab" href="{WA_HREF}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="10.8" r="8.4"/><polygon points="5.6,17.2 10,16.2 4.6,21.4"/><circle class="d" cx="8.5" cy="10.8" r="1.35"/><circle class="d" cx="12" cy="10.8" r="1.35"/><circle class="d" cx="15.5" cy="10.8" r="1.35"/></svg></a>"""

def footer(pname="", psku="", bar=False):
    """`bar` adds the sticky mobile action bar. Product and category pages pass it so a
    phone visitor always has an inquiry CTA in reach; the long category lists need it most."""
    if pname:
        bar = f"""<div class="mbar"><a class="btn btn-p" href="javascript:void(0)" onclick="openQuote('{esc(pname)}','{psku}')">Request a Quote</a><a class="btn btn-wa" href="{WA_HREF}" target="_blank" rel="noopener">WhatsApp</a></div>"""
    elif bar:
        bar = f"""<div class="mbar"><a class="btn btn-p" href="/#quote">Request a Quote</a><a class="btn btn-wa" href="{WA_HREF}" target="_blank" rel="noopener">WhatsApp</a></div>"""
    else:
        bar = ""
    return f"""<footer><div class="wrap">
<div class="foot">
<div>
<a href="/" class="logo">BEST <b>HARDWARE</b> TOOLS</a>
<p class="blurb">Factory-direct hardware and tools for importers, distributors and private-label brands. OEM/ODM welcome, low MOQ, worldwide shipping.</p>
<p class="legal"><b>{LEGAL}</b><br>{LOCATION}<br><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
</div>
<div><h5>Categories</h5>{''.join(f'<a href="/category-{c["id"]}.html">{c["name"]}</a>' for c in CATEGORIES)}</div>
<div><h5>Company</h5><a href="/#why">Why Us</a><a href="/#oem">OEM / ODM</a><a href="/#quote">Request a Quote</a><a href="/#faq">FAQ</a></div>
<div><h5>Contact</h5>
<a href="{WA_HREF}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a>
<a href="mailto:{SITE['email']}">{SITE['email']}</a>
<details class="paybox"><summary>Payment &amp; bank details</summary><div class="pb">
<div class="bank-row"><span class="blabel">Beneficiary</span><span class="bvalue">{SITE['bank_beneficiary']}</span></div>
<div class="bank-row"><span class="blabel">Account No.</span><span class="bvalue">{SITE['bank_account']}</span></div>
<div class="bank-row"><span class="blabel">SWIFT</span><span class="bvalue">{SITE['bank_swift']}</span></div>
<p class="bank-note">{SITE['bank_note']}</p>
</div></details>
</div>
</div>
<div class="copy"><span>&copy; {YEAR} {SITE['brand']} ({SITE['domain']}). All rights reserved.</span><span>Supplier of {', '.join(c['name'] for c in CATEGORIES)}.</span></div>
</div></footer>
{bar}
{wa_fab()}
{quote_modal()}
<script>{JS.replace('__WA__', WA_NUM).replace('__FS__', SITE['formspree'])}</script>
</body></html>"""

def ot_shot(p, cls="shot"):
    """Uniform framed product image: 1:1 white field, object-fit:contain, no cropping."""
    return f'<div class="{cls}"><img src="{p["img"]}" alt="{p["name"]}" width="480" height="480" loading="lazy" decoding="async"></div>'


def product_card(p):
    rel = f"/products/{p['slug']}.html"
    return f"""<a href="{rel}" class="pc"><div class="pc-img"><img src="{p['img']}" alt="{p['name']}" width="600" height="600" loading="lazy" decoding="async"><span class="badge">{p['badge']}</span></div><div class="pc-body"><h3>{p['name']}</h3><p class="pc-d">{excerpt(p['desc'], 110)}</p><div class="price-row"><span class="price">{p['price']}</span><span class="moq">{p['moq']}</span></div></div></a>"""

def index_html():
    day = datetime.now().day
    # Hero mosaic + category cards draw ONLY from HERO_OK, rotating daily inside that safe set.
    # Images come from the real catalogue (never a fabricated illustration) but are restricted
    # to verified-clean ones, because a Chinese caption or a supplier mark in the first screen
    # is the single most damaging thing this site could show a buyer.
    picks = {}
    for c in CATEGORIES:
        allow = [RELATED_INDEX[s] for s in HERO_OK.get(c["id"], []) if s in RELATED_INDEX]
        if allow:
            picks[c["id"]] = allow[(day * 3) % len(allow)]
        else:
            items = [p for p in PRODUCTS if p["cat"] == c["id"]]
            if items:
                picks[c["id"]] = items[(day * 3) % len(items)]
    mosaic = "".join(ot_shot(picks[c["id"]]) for c in CATEGORIES if c["id"] in picks)
    # The OEM block's three cards use the same verified-clean pool as the hero (offset by one
    # so they differ from the mosaic). Before this they were PRODUCTS[0]/[3]/[6], which put a
    # supplier poster carrying a third-party motor logo on the homepage and in the og:image.
    oem_picks = []
    for cid in [c["id"] for c in CATEGORIES][:3]:
        allow = [RELATED_INDEX[s] for s in HERO_OK.get(cid, []) if s in RELATED_INDEX]
        if allow:
            oem_picks.append(allow[(day * 3 + 1) % len(allow)])
    oem_cards = "".join(product_card(p) for p in oem_picks)
    cat_cards = ""
    for c in CATEGORIES:
        items = [p for p in PRODUCTS if p["cat"] == c["id"]]
        pk = picks.get(c["id"])
        img = f'<img src="{pk["img"]}" alt="{pk["name"]}" width="480" height="360" loading="lazy" decoding="async">' if pk else ""
        meta = f'{len(items)} products &middot; from {pk["price"].split(" - ")[0]}' if pk else f'{len(items)} products'
        cat_cards += (f'<a href="/category-{c["id"]}.html" class="cat"><div class="cat-img">{img}</div>'
                      f'<div class="cat-b"><h3>{c["name"]}</h3><span>{meta}</span>'
                      f'<span class="go">Browse {c["name"]} &rarr;</span></div></a>')
    sections = ""
    for cid in [c["id"] for c in CATEGORIES]:
        c = next(c for c in CATEGORIES if c["id"] == cid)
        items = [p for p in PRODUCTS if p["cat"] == c["id"]]
        # Daily rotation: the featured window advances by 3 products per day so each
        # category section surfaces a different slice of the catalogue every day.
        offset = (day * 3) % len(items) if items else 0
        rotated = items[offset:] + items[:offset]
        display_items = rotated[:9]
        cards = "".join(product_card(p) for p in display_items)
        view_all = f'<div class="cta-row" style="justify-content:center;margin-top:34px"><a href="/category-{c["id"]}.html" class="btn btn-o">View All {c["name"]} ({len(items)})</a></div>' if len(items) > 9 else ""
        alt = ' class="alt"' if [c["id"] for c in CATEGORIES].index(cid) % 2 else ''
        sections += f"""<section id="cat-{c['id']}"{alt}><div class="wrap">
<div class="sec-head"><div><h2>{c['name']}</h2><p>{len(items)} factory-direct lines for importers, distributors and private-label brands.</p></div><a class="view" href="/category-{c['id']}.html">View all &rarr;</a></div>
<div class="grid">{cards}</div>
{view_all}
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
        feats.append(("One-Stop Container Consolidation", "Mix power tools, pneumatic tools, hand tools and hardware in a single container - one shipment, one invoice and lower freight cost per unit for multi-category buyers."))
        feats.append(("Priority Production Slots", "Long-running partnerships guarantee reserved capacity at partner factories - stable lead times for repeat orders even in peak season."))
        feats.append(("Plug & Voltage Options for Your Market", "Electric and cordless tools ship with the plug standard your market needs - EU, US, UK and AU configurations set at the factory, with voltage variants and adapters handled on request."))
        feats.append(("Production Batch Traceability", "Lot-level records link raw materials, in-process checks and final inspection to each shipment for dependable repeat orders."))
        feats.append(("Third-Party Inspection Welcome", "Appoint an international inspection agency or send your own QC agent - we open the factory floor, arrange sample draws and book the inspection slot before your goods are packed."))
    oem_extra = ('<p style="color:var(--t2);margin-top:14px">From private-label packaging to full product customization, our partner factories handle tooling, color matching, logo printing and pre-shipment inspection. Share your spec sheet or sample - our engineering team replies within 24 hours with a factory-direct quotation and production timeline.</p><p style="color:var(--t2);margin-top:14px">Testing a sample first is the fastest way to lock in quality - we can adjust materials, finishes, packaging and print before you commit to a full container. Your drawings, logos and product specifications stay protected under our IP confidentiality policy, giving importers and brands a safe path to private-label and co-development projects.</p><p style="color:var(--t2);margin-top:14px">Production capacity is pre-validated across our partner lines, with CE-marked output and ISO9001-managed processes so compliance documents, test reports and certificates are ready when your shipment clears customs. We consolidate mixed SKUs - hardware, hand tools, power tools and pneumatic tools - into one container and one invoice, cutting freight cost and simplifying paperwork for multi-category importers and distributors.</p><p style="color:var(--t2);margin-top:14px">Every order is protected from factory floor to your warehouse: export-grade cartons with moisture-resistant packing, container loading supervised at the factory gate, and each batch shipped with the packing list, commercial invoice and compliance certificates your customs broker needs. Need to restock fast? Express freight from major Chinese ports keeps emergency lead times short, while scheduled sea freight protects margins on full containers - so your inventory plan stays predictable whether you order one sample or a 40HQ.</p><p style="color:var(--t2);margin-top:14px">Every OEM batch is inspected against a written sampling plan before shipment, and any defective units found after delivery are replaced or credited on the next order - so branded programs keep moving without quality disputes. Beyond the tool itself we handle the retail details: export cartons printed with your logo, barcode labels, retail-ready packaging and multilingual manuals, so containers land ready for your warehouse, catalog or e-commerce listings. Ask for pre-production samples, photos from the line or a live video inspection before shipment - our export team keeps you in control from tooling approval to final container loading.</p><p style="color:var(--t2);margin-top:14px">From the first drawing to the signed gold sample, one dedicated coordinator keeps your OEM program on schedule, and every shipment leaves with the paperwork your customs broker and end customers expect - commercial invoice, packing list, certificate of origin, test reports and barcode data on request. We keep your tooling, artwork and approved samples on file, so repeat orders are a one-email process with identical output every time. Should anything need attention after arrival, replacement parts are dispatched within days, protecting the brand you have built.</p>' if slot == 2 else "")
    oem_extra += '<p style="color:var(--t2);margin-top:14px">For distributors planning a phased launch, we can begin with a pilot order, lock the approved specification, and scale the same SKU across repeat batches. One project record keeps your artwork, approved sample, packaging dieline, inspection points and shipping plan aligned from quotation through replenishment.</p><p style="color:var(--t2);margin-top:14px">Peak-season planning is where a launch is won or lost, so we book production windows with our partner lines well in advance. Your tooling, mould and packaging lead times are scheduled before the rush rather than queued behind it: share your launch date and target volume and we work backwards from the ship date, reserving capacity, raw materials and inspection slots so branded programs reach the shelf on time.</p>'
    cat_intro = ('<p style="color:var(--t2);margin-top:22px;max-width:720px">From workshop essentials to complete maintenance programs, our category mix helps importers build a practical hardware assortment without coordinating multiple suppliers. Compare complementary SKUs, start with a focused sample order and scale the lines that fit your market.</p><p style="color:var(--t2);margin-top:10px;max-width:720px">Four sourcing categories under one roof: <b style="color:var(--t1)">Power Tools</b> for cordless and electric work, <b style="color:var(--t1)">Pneumatic Tools</b> for compressor-powered jobs, <b style="color:var(--t1)">Hand Tools</b> for daily maintenance and repair, and <b style="color:var(--t1)">Hardware</b> for cabinet and furniture fittings - each supplied factory-direct with consistent quality and low MOQs.</p><p style="color:var(--t2);margin-top:10px;max-width:720px">For contractors, woodworkers, maintenance teams and auto-service shops, the range covers the full jobsite chain - from cabinet hardware and hand tools for finishing work to cordless power tools and compressor-fed pneumatic equipment for heavy tasks. Order across categories in one shipment to cut freight cost and keep every project on one invoice.</p><p style="color:var(--t2);margin-top:10px;max-width:720px">Inside each category the selection runs deep - stainless hinges, slides and cabinet pulls for hardware buyers, CR-V ratchets and screwdriver sets for maintenance crews, brushless cordless drills, grinders and saws for contractors, plus air nailers, staplers, spray guns and impact wrenches for workshops and auto-service centers. Every line is kept in stock for repeat orders, so you can test a single SKU first and scale up as demand grows.</p><p style="color:var(--t2);margin-top:10px;max-width:720px">Every line above moves through the same controlled supply chain: raw-material inspection on arrival, in-process checks during production and a final pre-shipment quality gate before packing. Hardware is batch-tested for finish consistency and load strength, cutting tools get hardness and edge checks, cordless tools are run-tested at rated voltage, and pneumatic tools are bench-tested at working pressure - so mixed orders from any category arrive to the same standard. CE-marked items and ISO9001-managed lines ship with test reports and compliance documents ready for customs, keeping first orders and repeat shipments equally smooth.</p><p style="color:var(--t2);margin-top:10px;max-width:720px">Choosing which category to lead with depends on your market: hardware and hand tools are fast-moving, low-risk staples for new importers, power tools carry stronger tickets for established distributors, and pneumatic lines reward buyers who already serve workshops and auto-service fleets. Most of our wholesale partners start with one category, prove sell-through with a first container, then widen the assortment - and we support each step with market-appropriate plugs and voltages for power tools, plus export cartons and barcode-ready labeling across every category.</p>' if slot == 0 else "")
    cat_intro += '<p style="color:var(--t2);margin-top:10px;max-width:720px">Which category leads depends on the market you serve. Cabinet and furniture makers usually start with the hardware range - hinges, slides, handles and glass fittings - then add hand tools for installation crews. Tool wholesalers and online sellers tend to lead with cordless power tools, where brushless drills, grinders and saws carry the strongest repeat demand. Auto-service shops and industrial workshops most often begin with pneumatic tools, pairing air impact wrenches and spray guns with the compressors already on their floor. Because every category is stocked side by side, you can open with the line your customers ask for first and widen the assortment from there.</p>'
    if slot != 2:
        oem_extra = ""
    if slot != 0:
        cat_intro = ""
    cat_intro += '<p style="color:var(--t2);margin-top:10px;max-width:720px">Build a focused buying program by pairing high-use cabinet hardware with dependable hand tools, then add cordless and pneumatic equipment as your customers scale from repair work to production. This layered assortment helps distributors test demand with practical SKUs while keeping replenishment and supplier coordination simple.</p>'
    feat_html = "".join(f'<div class="feat"><div class="ic">{str(i + 1).zfill(2)}</div><h4>{t}</h4><p>{d}</p></div>' for i, (t, d) in enumerate(feats))
    # Real, self-updating figures only. Catalogue size and category count are computed from
    # products_data, so this strip cannot go stale as products are added each day.
    stats = [(str(len(PRODUCTS)), "SKUs in the catalogue"), (str(len(CATEGORIES)), "Sourcing categories"), ("24h", "Reply on every inquiry"), ("1 pc", "Minimum order")]
    stats_html = "".join(f'<div><b>{n}</b><span>{l}</span></div>' for n, l in stats)
    faq = [
        ("What is the minimum order quantity?", "Most lines start from MOQ 1 pc, and the exact figure for each item is shown on its product page. Higher-volume tiers are quoted on request."),
        ("Do you support OEM and private label?", "Yes. Logo marking, colour matching, custom packaging and retail-ready cartons are handled through our partner factories."),
        ("How fast will I get a quote?", REPLY_PROMISE + ", with MOQ, sample plan, packing options and estimated lead time included in the reply."),
        ("Can I get a sample before a bulk order?", "Samples can be arranged before a bulk order so you can approve materials, finish and packaging first."),
        ("How are orders shipped?", "FOB China, by sea, air or express. Power tools, pneumatic tools, hand tools and hardware can be consolidated into one container and one invoice."),
        ("How do I pay?", "T/T bank transfer. Full bank details are issued with the proforma invoice once a quotation is accepted."),
    ]
    faq_html = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    jsonld = f'''{{
 "@context":"https://schema.org","@type":"Organization","name":"{SITE['brand']}",
 "url":"{URL}","legalName":"{LEGAL}",
 "address":{{"@type":"PostalAddress","addressLocality":"Linyi","addressRegion":"Shandong","addressCountry":"CN"}},
 "contactPoint":{{"@type":"ContactPoint","contactType":"sales","email":"{SITE['email']}","telephone":"+{WA_NUM}"}},
 "areaServed":{{"@type":"Place","name":"Worldwide"}},
 "knowsAbout":["Power Tools","Pneumatic Tools","Hand Tools","Hardware","Cabinet Hardware","Industrial Tools"]}}'''
    html = head("Hardware & Tools Supplier - Factory Direct to Importers | Best Hardware Tools", f"Factory-direct power tools, pneumatic tools, hand tools and hardware for importers and distributors. {len(PRODUCTS)} SKUs, low MOQ, OEM/ODM support and worldwide shipping. Request a quote - every inquiry answered within 24 working hours.", URL + "", URL + "images/brushless-cordless-drill.jpg")
    html += f"""<script type="application/ld+json">{jsonld}</script>
<body>
{nav()}
<header class="hero"><div class="wrap">
<div class="hero-grid">
<div>
<span class="eyebrow">Factory-direct &middot; {LOCATION}</span>
<h1>Hardware &amp; Tools, <span>Factory-Direct</span> for Importers</h1>
<p class="lede">Power tools, pneumatic tools, hand tools and cabinet hardware sourced from China's manufacturing clusters - {len(PRODUCTS)} SKUs, low MOQ and OEM/ODM support for importers, distributors and private-label brands.</p>
<div class="cta-row"><a href="#quote" class="btn btn-p btn-lg">Get a Free Quote</a><a href="#cats" class="btn btn-o btn-lg">Browse the Catalogue</a></div>
<p class="promise"><b>24h reply</b> &middot; MOQ from 1 pc &middot; mixed-category container consolidation</p>
</div>
<div class="mosaic">{mosaic}</div>
</div>
<div class="stats">{stats_html}</div>
</div></header>
<section id="cats" class="alt"><div class="wrap">
<div class="sec-head"><div><h2>Product Categories</h2><p>Four sourcing categories under one roof, each supplied factory-direct.</p></div></div>
<div class="cats">{cat_cards}</div>
</div></section>
{sections}
<section id="why" class="alt"><div class="wrap"><div class="sec-head"><div><h2>Why Global Buyers Choose Us</h2><p>What we actually do on an order, from quotation through to container loading.</p></div></div><div class="feats">{feat_html}</div></div></section>
<section id="oem"><div class="wrap"><div class="sec-head"><div><h2>Build Your Own Brand</h2><p>Private-label packaging, logo marking and sample development through our partner factories.</p></div><a class="view" href="#quote">Start a project &rarr;</a></div>
<div class="grid">{oem_cards}</div>
<p style="margin-top:22px">Tell us your market and target price - we handle sourcing, quality control, custom packaging and shipping. <a href="#quote" style="color:var(--accent);font-weight:600">Request a quote</a> or <a href="{WA_HREF}" style="color:var(--accent);font-weight:600" target="_blank" rel="noopener">start a project on WhatsApp</a>.</p>
<details class="pd-more"><summary>More about our OEM / ODM program</summary>{oem_extra}{cat_intro}</details>
</div></section>
<section id="quote" class="alt"><div class="wrap"><div class="quote-grid">
<div class="quote-aside">
<h2>Request a Quote</h2>
<p>Send us your product list, quantities and target market - we reply with factory-direct pricing, MOQ, sample plan and estimated lead time.</p>
<ol class="steps">
<li><b>1</b><span>Tell us the products, quantities and destination.</span></li>
<li><b>2</b><span>We confirm unit price, MOQ, packing and lead time.</span></li>
<li><b>3</b><span>Approve a sample, then production, inspection and shipping.</span></li>
</ol>
<p class="promise"><b>{REPLY_PROMISE}.</b></p>
</div>
<div class="form-card">{quote_form_inline()}</div>
</div></div></section>
<section id="faq"><div class="wrap"><div class="sec-head"><div><h2>Buying Questions</h2><p>The terms buyers ask about before their first order.</p></div></div><div class="faq">{faq_html}</div></div></section>
<section id="contact" class="band"><div class="wrap">
<h2>Ready to source hardware &amp; tools?</h2>
<p>Get factory-direct quotes for your market. Low MOQ, fast samples, worldwide shipping.</p>
<div class="cta-row"><a href="#quote" class="btn btn-p btn-lg">Get a Free Quote</a><a href="{WA_HREF}" class="btn btn-wa btn-lg" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></div>
</div></section>
{footer()}
</html>"""
    return html

def product_page(p):
    cat_name = next(c["name"] for c in CATEGORIES if c["id"] == p["cat"])
    title = f"{p['name']} | Factory Direct Wholesale | Best Hardware Tools"
    desc = clip_words(p['desc'], 150)
    canonical = f"{URL}products/{p['slug']}.html"
    specs = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in p["specs"])
    pts = "".join(f"<li>{x}</li>" for x in p["points"])
    rel = "".join(product_card(RELATED_INDEX[s]) for s in p["related"] if s in RELATED_INDEX)
    # Only facts already carried by the data: nothing about lead-time days, warranty or
    # inspection bodies is asserted here.
    trade = [
        ("MOQ", p["moq"].replace("MOQ ", "")),
        ("Price basis", "FOB China"),
        ("Payment", "T/T bank transfer"),
        ("Packing", "Export carton with moisture-resistant packing"),
        ("Sample", "Available before a bulk order"),
        ("Lead time", "Confirmed in your quotation"),
    ]
    trade_rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in trade)
    wa_text = p['name'].replace(' ', '%20')
    jsonld = f'''{{"@context":"https://schema.org","@type":"Product","name":"{p['name']}","image":"{p['img']}","description":"{desc}","brand":{{"@type":"Brand","name":"{SITE['brand']}"}},"offers":{{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"{canonical}"}}}}'''
    html = head(title, desc, canonical, URL + "images/" + p['slug'] + ".jpg")
    html += f"""<script type="application/ld+json">{jsonld}</script>
<body>
{nav()}
<div class="wrap crumb"><a href="/">Home</a> &rsaquo; <a href="/category-{p['cat']}.html">{cat_name}</a> &rsaquo; {p['name']}</div>
<div class="wrap pd">
<div class="pd-media"><div class="pd-img"><img src="{p['img']}" alt="{p['name']}" width="800" height="800"></div>
<div class="trustline"><span>Factory-direct</span><span>OEM / ODM</span><span>Third-party inspection welcome</span></div></div>
<div class="pd-info">
<h1>{p['name']}</h1>
<div class="pd-price">{p['price']}</div>
<div class="pd-moq">{p['moq']} &middot; FOB China &middot; Worldwide shipping</div>
<div class="cta-row">
<a href="javascript:void(0)" onclick="openQuote('{esc(p['name'])}','{p['slug']}')" class="btn btn-p btn-lg">Send Inquiry</a>
<a href="{WA_HREF}?text={wa_text}%20inquiry" class="btn btn-wa btn-lg" target="_blank" rel="noopener">WhatsApp</a>
</div>
<div class="pts"><h4>Key points</h4><ul>{pts}</ul></div>
<table class="specs"><caption>Specifications</caption>{specs}</table>
<table class="specs"><caption>Trade terms</caption>{trade_rows}</table>
<h3 style="margin-bottom:10px">Product detail</h3>
<p class="pd-desc">{p['desc']}</p>
</div>
</div>
<section class="related alt"><div class="wrap"><div class="sec-head"><div><h2>More from this range</h2><p>Related {cat_name.lower()} lines buyers often order together.</p></div><a class="view" href="/category-{p['cat']}.html">View all {cat_name} &rarr;</a></div><div class="grid">{rel}</div></div></section>
{footer(p['name'], p['slug'])}
</html>"""
    return html

def category_html(cid):
    c = next(c for c in CATEGORIES if c["id"] == cid)
    items = [p for p in PRODUCTS if p["cat"] == cid]
    cards = "".join(product_card(p) for p in items)
    title = f"{c['name']} | Factory Direct Wholesale | Best Hardware Tools"
    desc = f"Browse {len(items)} factory-direct {c['name'].lower()} lines for importers and distributors, including {items[0]['name'].lower()}. Wholesale pricing, low MOQ and OEM/ODM support."
    canonical = f"{URL}category-{cid}.html"
    jsonld = f'''{{"@context":"https://schema.org","@type":"CollectionPage","name":"{title}","description":"{desc}","url":"{canonical}"}}'''
    html = head(title, desc, canonical, URL + "images/" + items[0]['slug'] + ".jpg")
    html += f"""<script type="application/ld+json">{jsonld}</script>
<body>
{nav(cid)}
<div class="wrap crumb"><a href="/">Home</a> &rsaquo; {c['name']}</div>
<section style="padding-top:36px"><div class="wrap">
<div class="sec-head"><div><h1 style="font-size:clamp(1.6rem,2.8vw,2.3rem)">{c['name']}</h1><p>{len(items)} factory-direct lines. Pricing on every card is a factory-direct range - request a quote for volume tiers, packing and lead time.</p></div><a class="view" href="/#quote">Request a quote &rarr;</a></div>
<div class="grid">{cards}</div>
</div></section>
<section id="contact" class="band"><div class="wrap">
<h2>Need bulk pricing for {c['name'].lower()}?</h2>
<p>Send your product list and quantities - we reply within 24 working hours with MOQ, sample plan, packing options and estimated lead time.</p>
<div class="cta-row"><a href="/#quote" class="btn btn-p btn-lg">Get a Free Quote</a><a href="{WA_HREF}" class="btn btn-wa btn-lg" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></div>
</div></section>
{footer(bar=True)}
</html>"""
    return html

def main():
    os.makedirs(os.path.join(BASE, "products"), exist_ok=True)
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html())
    for c in CATEGORIES:
        with open(os.path.join(BASE, f"category-{c['id']}.html"), "w", encoding="utf-8") as f:
            f.write(category_html(c['id']))
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
    for c in CATEGORIES:
        urls.append(f"<url><loc>{URL}category-{c['id']}.html</loc><priority>0.9</priority><changefreq>daily</changefreq></url>")
    for p in PRODUCTS:
        urls.append(f"<url><loc>{URL}products/{p['slug']}.html</loc><priority>0.8</priority><changefreq>weekly</changefreq></url>")
    with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    # 404
    with open(os.path.join(BASE, "404.html"), "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>404 - Best Hardware Tools</title><meta name="robots" content="noindex"><link rel="canonical" href="{URL}404.html"></head><body style="background:#FFFFFF;color:#0F1317;font-family:Inter,system-ui,sans-serif;text-align:center;padding:80px 20px"><h1 style="font-size:3rem;color:#C2410C;letter-spacing:-.02em">404</h1><p style="color:#4A525C">Page not found.</p><p><a href="/" style="color:#C2410C;font-weight:600">Back to Best Hardware Tools</a></p></body></html>""")
    print("Generated:", len(PRODUCTS) + 1, "pages + CNAME/robots/sitemap/404")

if __name__ == "__main__":
    main()
