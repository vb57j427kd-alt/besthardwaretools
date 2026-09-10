# -*- coding: utf-8 -*-
"""
Professional BHT Live Monitor v1.0
Checks H1 brand name, product card counts, and footer integrity using live fetch.
"""
import urllib.request
import re
import sys

URL = "https://besthardwaretools.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def check():
    print(f"Fetching {URL}...")
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Failed to fetch URL. Error: {e}")
        return False

    errors = []
    
    # 1. Check H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
    if not h1_match:
        errors.append("MISSING: <h1> tag not found.")
    else:
        h1_text = h1_match.group(1).strip()
        if "BEST HARDWARE TOOLS" not in h1_text.upper():
            errors.append(f"SEO FAIL: <h1> does not contain brand name. Found: '{h1_text}'")
        else:
            print("OK: H1 contains brand name.")

    # 2. Check Product Cards
    card_count = len(re.findall(r'class="pc"', html))
    if card_count < 10:
        errors.append(f"CONTENT FAIL: Too few product cards found ({card_count}). Expected > 10.")
    else:
        print(f"OK: Found {card_count} product cards.")

    # 3. Check Footer
    if "Best Hardware Tools" not in html or "2026" not in html:
        errors.append("INTEGRITY FAIL: Footer brand or year missing.")
    else:
        print("OK: Footer integrity verified.")

    if errors:
        print("\n--- MONITORING ALERTS ---")
        for err in errors:
            print(f"!! {err}")
        return False
    
    print("\nSUCCESS: All homepage checks passed.")
    return True

if __name__ == "__main__":
    if not check():
        sys.exit(1)
